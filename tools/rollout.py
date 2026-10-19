"""Read-only rollout preflight by default; public writes require --execute."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen


BASE = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '__pycache__', '.venv', 'node_modules', 'dist', '.rollout-work'}


def run(args, *, data=None, env=None):
    result = subprocess.run(args, input=data, capture_output=True, text=True, env=env)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or 'Command failed: ' + args[0])
    return result.stdout.strip()


def api(path, method='GET', payload=None, *, missing=False, pages=False):
    args = ['gh', 'api', path, '--method', method]
    if pages:
        args += ['--paginate', '--slurp']
    if payload is not None:
        args += ['--input', '-']
    try:
        raw = run(args, data=json.dumps(payload) if payload is not None else None)
    except RuntimeError as error:
        if missing and 'HTTP 404' in str(error):
            return None
        raise
    value = json.loads(raw) if raw else None
    return [item for page in value for item in page] if pages else value


def candidate_digest(root):
    digest = hashlib.sha256()
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root)
        if any(part in IGNORED for part in relative.parts):
            continue
        if relative.name in {'.rollout-state.json', '.rollout-state.json.tmp'} or path.suffix in {'.pyc', '.pyo'}:
            continue
        if path.is_symlink():
            raise RuntimeError('Candidate contains a symlink: ' + str(relative))
        if path.is_file():
            digest.update(str(relative).encode() + b'\0' + path.read_bytes() + b'\0')
    return digest.hexdigest()


class Rollout:
    def __init__(self, root=BASE):
        self.root = Path(root).resolve()
        self.baseline = json.loads((self.root/'rollout/baseline.json').read_text())
        self.state_path = self.root/'.rollout-state.json'
        if self.state_path.is_symlink():
            raise RuntimeError('Refusing a symlink journal')
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else {}
        self.digest = candidate_digest(self.root)
        if self.state and self.state.get('candidate_sha256') != self.digest:
            raise RuntimeError('Candidate changed since rollout started; preserve the journal and review the change')
        self.marker = '<!-- chatgpt-seo-rollout:' + self.baseline['head'] + ' -->'
        self.comment = (self.root/'rollout/closing-comment.md').read_text().strip() + '\n\n' + self.marker

    def save(self, event):
        self.state['candidate_sha256'] = self.digest
        self.state.setdefault('events', []).append(event)
        temporary = self.state_path.with_suffix('.json.tmp')
        if temporary.is_symlink():
            raise RuntimeError('Refusing a symlink temporary journal')
        temporary.write_text(json.dumps(self.state, indent=2) + '\n')
        temporary.replace(self.state_path)

    def comment_exists(self, repo, number):
        comments = api(f'repos/{repo}/issues/{number}/comments?per_page=100', pages=True)
        return any(item.get('body') == self.comment and
                   item.get('user', {}).get('login', '').casefold() == self.baseline['account'].casefold()
                   for item in comments)

    def tag_commit(self, repo):
        tag = api(f"repos/{repo}/git/ref/tags/{self.baseline['legacy_tag']}", missing=True)
        if tag is None:
            return None
        obj = tag['object']
        for _ in range(8):
            if obj['type'] == 'commit':
                return obj['sha']
            if obj['type'] != 'tag':
                break
            obj = api(f"repos/{repo}/git/tags/{obj['sha']}")['object']
        raise RuntimeError('Rollback tag does not resolve to a commit')

    def check_closed(self, repo, item):
        number = item['number']
        current = api(f'repos/{repo}/issues/{number}')
        if current['node_id'] != item['node_id'] or current['state'] != 'closed':
            raise RuntimeError(f'Unexpected state for item {number}')
        if item['kind'] == 'issue' and current.get('state_reason') != 'not_planned':
            raise RuntimeError(f'Issue {number} was not closed as not planned')
        if item['kind'] == 'pr' and api(f'repos/{repo}/pulls/{number}').get('merged'):
            raise RuntimeError(f'PR {number} was merged; refusing to treat it as a legacy closure')

    def preflight(self):
        b = self.baseline
        if api('user')['login'].casefold() != b['account'].casefold():
            raise RuntimeError('Wrong GitHub account')
        repository = api(f"repositories/{b['repository']['id']}")
        repo = repository['full_name']
        if repository['id'] != b['repository']['id'] or repository['private'] or repo not in {b['repository']['full_name'], b['target']}:
            raise RuntimeError('Repository ID, name, or public visibility changed')
        if repository['default_branch'] != b['repository']['default_branch']:
            raise RuntimeError('Default branch changed')
        if not repository.get('permissions', {}).get('admin'):
            raise RuntimeError('Repository administration permission is required')
        head = api(f"repos/{repo}/git/ref/heads/{b['repository']['default_branch']}")['object']['sha']
        if head not in {b['head'], self.state.get('new_commit')}:
            raise RuntimeError('Public HEAD changed since review')
        target = api('repos/' + b['target'], missing=True)
        if target is not None and target['id'] != b['repository']['id']:
            raise RuntimeError('Destination name belongs to another repository')
        tag = self.tag_commit(repo)
        if tag is not None and tag != b['head']:
            raise RuntimeError('Conflicting rollback tag')
        opened = api(f'repos/{repo}/issues?state=open&per_page=100', pages=True)
        expected = {item['number']: item for item in b['items']}
        actual = {item['number']: item for item in opened}
        if actual.keys() - expected.keys():
            raise RuntimeError('Open-item inventory changed: an unreviewed item is present')
        for number, item in expected.items():
            if number in actual:
                current = actual[number]
                kind = 'pr' if 'pull_request' in current else 'issue'
                if current['node_id'] != item['node_id'] or kind != item['kind']:
                    raise RuntimeError('Reviewed item identity changed')
            else:
                self.check_closed(repo, item)
                if not self.comment_exists(repo, number):
                    raise RuntimeError('Open-item inventory changed without a matching rollout comment')
        return repository, head, actual

    def prepare_commit(self, repository):
        work = self.root/'.rollout-work'
        env = {**os.environ, 'GIT_AUTHOR_NAME': 'Daniel Agrici',
               'GIT_AUTHOR_EMAIL': '223140489+AgriciDaniel@users.noreply.github.com',
               'GIT_COMMITTER_NAME': 'Daniel Agrici',
               'GIT_COMMITTER_EMAIL': '223140489+AgriciDaniel@users.noreply.github.com'}
        if not (work/'.git').exists():
            run(['git', '-c', 'core.hooksPath=/dev/null', 'clone', '--quiet', '--no-checkout',
                 'https://github.com/' + repository['full_name'] + '.git', str(work)])
        git = ['git', '-c', 'core.hooksPath=/dev/null', '--git-dir', str(work/'.git'), '--work-tree', str(self.root)]
        run(git + ['read-tree', self.baseline['head']])
        run(git + ['add', '-A'], env=env)
        tree = run(git + ['write-tree'])
        if self.state.get('new_commit'):
            previous_tree = run(git + ['rev-parse', self.state['new_commit'] + '^{tree}'])
            if tree != previous_tree:
                raise RuntimeError('Prepared tree changed since rollout started')
        else:
            self.state['new_commit'] = run(git + ['commit-tree', tree, '-p', self.baseline['head'],
                                                  '-m', 'Repurpose repository for the ChatGPT SEO plugin'], env=env)
            self.state['tree'] = tree
            self.save('replacement commit prepared locally')
        return work

    def verify_urls(self):
        manifest = json.loads((self.root/'plugins/ai-marketing-hub-seo/plugin.json').read_text())
        interface = manifest['extensions']['com.openai']['interface']
        for key in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
            with urlopen(interface[key], timeout=30) as response:
                if response.status != 200 or 'SEO-pro' not in response.read().decode('utf-8'):
                    raise RuntimeError('Public listing URL does not serve the expected product: ' + key)
        for path in ('README.md', 'SUPPORT.md', 'plugins/ai-marketing-hub-seo/legal/PRIVACY.md',
                     'plugins/ai-marketing-hub-seo/legal/TERMS.md'):
            url = 'https://raw.githubusercontent.com/' + self.baseline['target'] + '/main/' + path
            with urlopen(url, timeout=30) as response:
                if response.read() != (self.root/path).read_bytes():
                    raise RuntimeError('Public file differs from the reviewed candidate: ' + path)

    def execute(self):
        if run(['git', '-C', str(self.root), 'status', '--porcelain', '--untracked-files=all']):
            raise RuntimeError('Candidate checkout has uncommitted files; review and commit them before rollout')
        repository, head, opened = self.preflight()
        run([sys.executable, str(self.root/'tools/validate_plugin.py')])
        run([sys.executable, '-m', 'unittest', 'discover', '-s', str(self.root/'tests'), '-q'])
        work = self.prepare_commit(repository)
        repo = repository['full_name']
        if self.tag_commit(repo) is None:
            api(f'repos/{repo}/git/refs', 'POST', {'ref': 'refs/tags/' + self.baseline['legacy_tag'], 'sha': self.baseline['head']})
        if self.tag_commit(repo) != self.baseline['head']:
            raise RuntimeError('Rollback tag verification failed')
        self.save('rollback tag verified')
        for item in self.baseline['items']:
            number = item['number']
            if number not in opened:
                continue
            if not self.comment_exists(repo, number):
                api(f'repos/{repo}/issues/{number}/comments', 'POST', {'body': self.comment})
            endpoint = 'issues' if item['kind'] == 'issue' else 'pulls'
            payload = {'state': 'closed'}
            if item['kind'] == 'issue':
                payload['state_reason'] = 'not_planned'
            api(f'repos/{repo}/{endpoint}/{number}', 'PATCH', payload)
            self.check_closed(repo, item)
            self.save('closed ' + item['kind'] + ' ' + str(number))
        desired = self.baseline['desired']
        updated = api(f'repos/{repo}', 'PATCH',
                      {'name': self.baseline['target'].split('/')[1],
                       'description': desired['description'], 'homepage': desired['homepage']})
        if updated['id'] != repository['id'] or updated['private'] or updated['full_name'] != self.baseline['target']:
            raise RuntimeError('Rename did not preserve the public repository identity')
        api('repos/' + self.baseline['target'] + '/topics', 'PUT', {'names': desired['topics']})
        self.save('repository renamed and metadata updated')
        run(['git', '-C', str(work), 'remote', 'set-url', 'origin',
             'https://github.com/' + self.baseline['target'] + '.git'])
        run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(work), 'push', 'origin',
             self.state['new_commit'] + ':refs/heads/' + self.baseline['repository']['default_branch']])
        self.save('replacement pushed without force')
        final, final_head, remaining = self.preflight()
        if final_head != self.state['new_commit'] or remaining:
            raise RuntimeError('Final public HEAD or item-state verification failed')
        if final['description'] != desired['description'] or final['homepage'] != desired['homepage'] or set(final['topics']) != set(desired['topics']):
            raise RuntimeError('Final repository metadata differs')
        self.verify_urls()
        self.save('public URLs and final repository state verified')
        return {'status': 'public_repository_updated', 'repository': final['full_name'],
                'commit': final_head, 'journal': str(self.state_path), 'openai_submission': 'not_performed'}

    def dry_run(self):
        repository, head, opened = self.preflight()
        return {'mode': 'read_only_dry_run', 'repository': repository['full_name'], 'head': head,
                'remaining_reviewed_issues': sum('pull_request' not in item for item in opened.values()),
                'remaining_reviewed_prs': sum('pull_request' in item for item in opened.values()),
                'candidate_sha256': self.digest,
                'steps': ['preserve rollback tag', 'comment and close reviewed legacy items',
                          'rename the existing public repository and update metadata',
                          'push a descendant commit without force', 'verify public URLs'],
                'public_writes': False, 'journal_written': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Public writes; run only after the owner says ship it')
    args = parser.parse_args()
    rollout = None
    try:
        rollout = Rollout()
        result = rollout.execute() if args.execute else rollout.dry_run()
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError, RuntimeError) as error:
        if rollout is not None and args.execute and rollout.state:
            rollout.save('stopped: ' + str(error))
        print(json.dumps({'status': 'stopped', 'reason': str(error),
                          'public_writes_authorized': args.execute,
                          'recovery': 'Inspect the journal and remote state; no automatic rollback is performed.'}), file=sys.stderr)
        raise SystemExit(1)


if __name__ == '__main__':
    main()
