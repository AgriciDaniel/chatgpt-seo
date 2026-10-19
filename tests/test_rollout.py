import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
import rollout


class GitHub:
    def __init__(self, baseline):
        self.b = baseline
        self.repository = {**baseline['repository'], 'permissions': {'admin': True}}
        self.user = baseline['account']
        self.head = baseline['head']
        self.tag = None
        self.items = {}
        for item in baseline['items']:
            self.items[item['number']] = {**item, 'state': 'open'}
            if item['kind'] == 'pr':
                self.items[item['number']]['pull_request'] = {}
        self.comments = {number: [] for number in self.items}
        self.writes = []
        self.fail_after_comment = False
        self.destination_collision = False

    def api(self, path, method='GET', payload=None, **kwargs):
        repo = self.repository['full_name']
        prefix = f'repos/{repo}/'
        if method != 'GET':
            self.writes.append((path, method, payload))
        if method == 'GET':
            if path == 'user':
                return {'login': self.user}
            if path == f"repositories/{self.b['repository']['id']}":
                return copy.deepcopy(self.repository)
            if path == 'repos/' + self.b['target']:
                if self.destination_collision:
                    return {'id': 999}
                return copy.deepcopy(self.repository) if repo == self.b['target'] else None
            if path == prefix + 'git/ref/heads/main':
                return {'object': {'sha': self.head}}
            if path == prefix + 'git/ref/tags/' + self.b['legacy_tag']:
                return {'object': {'type': 'commit', 'sha': self.tag}} if self.tag else None
            if path == prefix + 'issues?state=open&per_page=100':
                return [copy.deepcopy(item) for item in self.items.values() if item['state'] == 'open']
            if path.startswith(prefix + 'issues/'):
                number = int(path[len(prefix):].split('/')[1])
                if '/comments?' in path:
                    return copy.deepcopy(self.comments[number])
                return copy.deepcopy(self.items[number])
            if path.startswith(prefix + 'pulls/'):
                return {'merged': False}
        elif method == 'POST' and path == prefix + 'git/refs':
            self.tag = payload['sha']
            return {}
        elif method == 'POST' and path.endswith('/comments'):
            number = int(path[len(prefix):].split('/')[1])
            self.comments[number].append({'body': payload['body'], 'user': {'login': self.user}})
            if self.fail_after_comment:
                self.fail_after_comment = False
                raise RuntimeError('Connection lost after the server saved the comment')
            return {}
        elif method == 'PATCH' and path == 'repos/' + repo:
            self.repository.update(full_name=self.b['target'], description=payload['description'], homepage=payload['homepage'])
            return copy.deepcopy(self.repository)
        elif method == 'PATCH' and (path.startswith(prefix + 'issues/') or path.startswith(prefix + 'pulls/')):
            number = int(path[len(prefix):].split('/')[1])
            self.items[number].update(payload)
            return copy.deepcopy(self.items[number])
        elif method == 'PUT' and path == 'repos/' + self.b['target'] + '/topics':
            self.repository['topics'] = payload['names']
            return {}
        raise AssertionError((path, method, payload))


class RolloutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root/'rollout').mkdir()
        self.b = {'account': 'AgriciDaniel', 'repository': {'id': 123, 'full_name': 'AgriciDaniel/legacy',
                  'private': False, 'default_branch': 'main', 'description': 'old', 'homepage': 'https://example.test/old', 'topics': ['old']},
                  'target': 'AgriciDaniel/product', 'head': 'a'*40, 'legacy_tag': 'legacy-final',
                  'desired': {'description': 'new', 'homepage': 'https://example.test/new', 'topics': ['new']},
                  'items': [{'number': 1, 'kind': 'issue', 'node_id': 'I_1'},
                            {'number': 2, 'kind': 'pr', 'node_id': 'PR_2'}]}
        (self.root/'rollout/baseline.json').write_text(json.dumps(self.b))
        (self.root/'rollout/closing-comment.md').write_text('Thank you. Closing as not planned.\n')
        self.gh = GitHub(self.b)
        self.commands = []

    def run_command(self, args, **kwargs):
        self.commands.append(args)
        if 'push' in args:
            self.gh.head = 'b'*40
        return ''

    def prepare_commit(self, task, repository):
        task.state['new_commit'] = 'b'*40
        task.save('prepared test commit')
        return self.root/'.rollout-work'

    def execute(self):
        with patch.object(rollout, 'api', self.gh.api), patch.object(rollout, 'run', self.run_command), \
             patch.object(rollout.Rollout, 'prepare_commit', autospec=True, side_effect=self.prepare_commit), \
             patch.object(rollout.Rollout, 'verify_urls'):
            return rollout.Rollout(self.root).execute()

    def test_default_dry_run_makes_no_writes_or_journal(self):
        with patch.object(rollout, 'api', self.gh.api):
            result = rollout.Rollout(self.root).dry_run()
        self.assertFalse(result['public_writes'])
        self.assertEqual(self.gh.writes, [])
        self.assertFalse((self.root/'.rollout-state.json').exists())

    def test_wrong_account_stops_before_public_writes(self):
        self.gh.user = 'someone-else'
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'Wrong GitHub'):
            rollout.Rollout(self.root).preflight()
        self.assertEqual(self.gh.writes, [])

    def test_stale_head_stops_before_public_writes(self):
        self.gh.head = 'c'*40
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'HEAD changed'):
            rollout.Rollout(self.root).preflight()
        self.assertEqual(self.gh.writes, [])

    def test_conflicting_tag_stops_before_public_writes(self):
        self.gh.tag = 'c'*40
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'Conflicting'):
            rollout.Rollout(self.root).preflight()
        self.assertEqual(self.gh.writes, [])

    def test_changed_inventory_and_destination_are_rejected(self):
        self.gh.items[3] = {'number': 3, 'node_id': 'I_3', 'state': 'open'}
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'inventory changed'):
            rollout.Rollout(self.root).preflight()
        del self.gh.items[3]
        self.gh.destination_collision = True
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'Destination'):
            rollout.Rollout(self.root).preflight()
        self.assertEqual(self.gh.writes, [])

    def test_private_repository_and_changed_candidate_are_rejected(self):
        self.gh.repository['private'] = True
        with patch.object(rollout, 'api', self.gh.api), self.assertRaisesRegex(RuntimeError, 'public visibility'):
            rollout.Rollout(self.root).preflight()
        task = rollout.Rollout(self.root)
        task.save('fixture')
        (self.root/'changed.md').write_text('unreviewed change')
        with self.assertRaisesRegex(RuntimeError, 'Candidate changed'):
            rollout.Rollout(self.root)

    def test_interrupted_comment_is_not_sent_twice_on_resume(self):
        self.gh.fail_after_comment = True
        with self.assertRaisesRegex(RuntimeError, 'Connection lost'):
            self.execute()
        result = self.execute()
        self.assertEqual(result['status'], 'public_repository_updated')
        self.assertEqual(len(self.gh.comments[1]), 1)
        self.assertEqual(len(self.gh.comments[2]), 1)
        self.assertEqual(self.gh.items[1]['state_reason'], 'not_planned')
        self.assertEqual(self.gh.items[2]['state'], 'closed')
        self.assertEqual(self.gh.tag, self.b['head'])
        pushes = [args for args in self.commands if 'push' in args]
        self.assertTrue(pushes)
        self.assertFalse(any('--force' in arg or arg.startswith('+') for args in pushes for arg in args))
        self.assertFalse(any(payload and 'private' in payload for _, _, payload in self.gh.writes))
        self.execute()
        self.assertEqual(len(self.gh.comments[1]), 1)

    def test_404_is_the_only_missing_repository_fallback(self):
        with patch.object(rollout, 'run', side_effect=RuntimeError('HTTP 403')):
            with self.assertRaisesRegex(RuntimeError, '403'):
                rollout.api('repos/example/test', missing=True)
        with patch.object(rollout, 'run', side_effect=RuntimeError('HTTP 404')):
            self.assertIsNone(rollout.api('repos/example/test', missing=True))

    def test_real_git_commit_preserves_parent_and_excludes_runtime_state(self):
        import os
        env = {**os.environ, 'GIT_AUTHOR_NAME': 'Fixture', 'GIT_COMMITTER_NAME': 'Fixture',
               'GIT_AUTHOR_EMAIL': 'fixture@example.test', 'GIT_COMMITTER_EMAIL': 'fixture@example.test'}
        work = self.root/'.rollout-work'
        work.mkdir()
        rollout.run(['git', 'init', '--quiet', '--initial-branch=main', str(work)])
        (work/'legacy.txt').write_text('legacy fixture')
        rollout.run(['git', '-C', str(work), 'add', '.'])
        rollout.run(['git', '-c', 'core.hooksPath=/dev/null', '-C', str(work), 'commit', '--quiet', '-m', 'fixture'], env=env)
        self.b['head'] = rollout.run(['git', '-C', str(work), 'rev-parse', 'HEAD'])
        (self.root/'rollout/baseline.json').write_text(json.dumps(self.b))
        (self.root/'.gitignore').write_text('.rollout-work/\n.rollout-state.json\n')
        (self.root/'README.md').write_text('reviewed product fixture')
        task = rollout.Rollout(self.root)
        task.prepare_commit(self.b['repository'])
        commit = task.state['new_commit']
        parent = rollout.run(['git', '-C', str(work), 'show', '-s', '--format=%P', commit])
        files = rollout.run(['git', '-C', str(work), 'ls-tree', '-r', '--name-only', commit]).splitlines()
        self.assertEqual(parent, self.b['head'])
        self.assertIn('README.md', files)
        self.assertNotIn('legacy.txt', files)
        self.assertFalse(any('.rollout' in name for name in files))


if __name__ == '__main__':
    unittest.main()
