"""Local package preflight, separate from installed-host and public approval."""

import argparse
import ast
import hashlib
import json
import math
import re
import struct
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from urllib.parse import urlsplit

BASE = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = BASE / 'plugins/ai-marketing-hub-seo'
EXCLUDED = {'__pycache__', '.git', '.venv', 'node_modules'}
SECRET_PATTERNS = [r'sk-[A-Za-z0-9_-]{24,}', r'AIza[A-Za-z0-9_-]{30,}',
                   r'gh[pousr]_[A-Za-z0-9]{30,}', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
PROVIDER_PATTERN = r'data[ _-]?for[ _-]?seo'
OFFLINE_IMPORTS = {'argparse', 'collections', 'csv', 'datetime', 'decimal', 'hashlib',
                   'html.parser', 'io', 'json', 'math', 'pathlib', 're', 'struct',
                   'sys', 'urllib.parse', 'xml.etree.ElementTree'}


def package_files(root):
    return sorted(p for p in root.rglob('*') if not p.is_symlink() and p.is_file() and
                  not any(x in EXCLUDED for x in p.relative_to(root).parts) and
                  p.suffix not in {'.pyc', '.pyo'})


def inventory_digest(entries):
    encoded = json.dumps(entries, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def package_content_digest(root):
    entries = [{'path': path.relative_to(root).as_posix(), 'bytes': path.stat().st_size,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()} for path in package_files(root)]
    return inventory_digest(entries)


def png_dimensions(path):
    with path.open('rb') as handle:
        raw = handle.read(5 * 1024 * 1024 + 1)
    if len(raw) > 5 * 1024 * 1024:
        raise ValueError('PNG exceeds the 5 MiB icon limit')
    if not raw.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('PNG signature is missing')
    position, chunks = 8, []
    while position < len(raw):
        if position + 12 > len(raw):
            raise ValueError('PNG chunk is truncated')
        length = struct.unpack('>I', raw[position:position+4])[0]
        end = position + 12 + length
        if end > len(raw):
            raise ValueError('PNG chunk is truncated')
        kind, data = raw[position+4:position+8], raw[position+8:end-4]
        crc = struct.unpack('>I', raw[end-4:end])[0]
        if zlib.crc32(kind + data) != crc:
            raise ValueError('PNG chunk checksum is invalid')
        chunks.append((kind, data))
        position = end
    if not chunks or chunks[0][0] != b'IHDR' or len(chunks[0][1]) != 13:
        raise ValueError('PNG dimension header is missing or invalid')
    if chunks[-1] != (b'IEND', b'') or sum(kind == b'IHDR' for kind, _ in chunks) != 1 or sum(kind == b'IEND' for kind, _ in chunks) != 1:
        raise ValueError('PNG header or final chunk is invalid')
    idat_indices = [i for i, (kind, _) in enumerate(chunks) if kind == b'IDAT']
    if not idat_indices or idat_indices != list(range(idat_indices[0], idat_indices[-1] + 1)):
        raise ValueError('PNG needs consecutive pixel-data chunks')
    if any(not re.fullmatch(b'[A-Za-z]{4}', kind) for kind, _ in chunks):
        raise ValueError('PNG chunk name is invalid')
    width, height, depth, color, compression, filtering, interlace = struct.unpack('>IIBBBBB', chunks[0][1])
    if width != height or not 48 <= width <= 4096:
        raise ValueError('PNG must be square, from 48 through 4096 pixels')
    depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
    if color not in depths or depth not in depths[color] or compression or filtering or interlace not in (0, 1):
        raise ValueError('PNG encoding fields are invalid')
    palettes = [(i, data) for i, (kind, data) in enumerate(chunks) if kind == b'PLTE']
    if color == 3 and len(palettes) != 1:
        raise ValueError('Indexed PNG needs a single valid palette before pixel data')
    if palettes:
        index, palette = palettes[0]
        if len(palettes) != 1 or index > idat_indices[0] or color in (0, 4) or not 0 < len(palette) <= 768 or len(palette) % 3:
            raise ValueError('PNG palette is invalid or appears after pixel data')
        if color == 3 and len(palette) // 3 > 2**depth:
            raise ValueError('PNG palette exceeds the indexed bit-depth limit')
    if any(kind[0] < 97 and kind not in {b'IHDR', b'PLTE', b'IDAT', b'IEND'} for kind, _ in chunks):
        raise ValueError('PNG has an unsupported critical chunk')
    bits = depth * {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    passes = [(0, 0, 1, 1)] if not interlace else [(0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8),
              (2, 0, 4, 4), (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2)]
    rows = []
    for x, y, dx, dy in passes:
        w, h = max(0, (width-x+dx-1)//dx), max(0, (height-y+dy-1)//dy)
        if w and h:
            rows.extend([1 + (w*bits+7)//8] * h)
    expected = sum(rows)
    compressed = b''.join(data for kind, data in chunks if kind == b'IDAT')
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(compressed, expected + 1)
    if len(pixels) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError('PNG pixel stream is truncated, oversized or invalid')
    offset = 0
    for length in rows:
        if pixels[offset] > 4:
            raise ValueError('PNG row filter is invalid')
        offset += length
    return width, height


def inside(root, path):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def https_url(value):
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        parsed.port
        return parsed.scheme == 'https' and bool(parsed.hostname) and parsed.username is None and parsed.password is None and not any(c.isspace() for c in value)
    except ValueError:
        return False


def validate(root=DEFAULT_ROOT, public=False, acceptance_path=None):
    root = Path(root)
    errors, warnings = [], []
    try:
        manifest = json.loads((root / 'plugin.json').read_text())
    except (OSError, ValueError) as error:
        return {'valid': False, 'errors': [str(error)], 'warnings': [], 'files': 0, 'skills': 0}
    if not isinstance(manifest, dict):
        return {'valid': False, 'errors': ['Root manifest must be a JSON object'], 'warnings': [], 'files': 0, 'skills': 0}
    extensions = manifest.get('extensions', {})
    if not isinstance(extensions, dict) or not isinstance(extensions.get('com.openai', {}), dict):
        return {'valid': False, 'errors': ['Manifest extensions must contain JSON objects'], 'warnings': [], 'files': 0, 'skills': 0}
    extension = extensions.get('com.openai', {})
    interface = extension.get('interface', {})
    if not isinstance(interface, dict):
        return {'valid': False, 'errors': ['OpenAI interface must be a JSON object'], 'warnings': [], 'files': 0, 'skills': 0}
    files = package_files(root)
    included_paths = {path.resolve() for path in files}
    allowed = {'$schema', 'name', 'version', 'description', 'author', 'homepage',
               'repository', 'license', 'keywords', 'extensions'}
    if set(manifest) - allowed:
        errors.append('Root manifest contains fields outside the portable schema')
    if manifest.get('$schema') != 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json':
        errors.append('Portable manifest schema identifier is missing or incorrect')
    if not isinstance(manifest.get('name'), str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', manifest['name']) or len(manifest['name']) > 64:
        errors.append('Invalid portable plugin name')
    if not isinstance(manifest.get('version'), str) or not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?', manifest['version']):
        errors.append('Explicit semantic package version required')
    for field, limit in [('displayName', 30), ('shortDescription', 30),
                         ('longDescription', 4000), ('developerName', 80), ('category', 120)]:
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip() or len(value) > limit:
            errors.append(f'Listing {field} must be nonempty and at most {limit} characters')
    prompts = interface.get('defaultPrompt', [])
    if isinstance(prompts, str):
        prompts = [prompts]
    if not isinstance(prompts, list) or len(prompts) > 3 or any(not isinstance(x, str) or len(x) > 128 or '@' in x for x in prompts):
        errors.append('Starter prompts must be at most three unique prompts of at most 128 characters, without @mentions')
    elif len(set(prompts)) != len(prompts):
        errors.append('Starter prompts must be unique')
    for field in ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL'):
        if field in interface and not https_url(interface[field]):
            errors.append(f'{field} must be an HTTPS URL without credentials')
    for field in ('composerIcon', 'composerIconDark', 'logo', 'logoDark', 'onboardingSkill'):
        value = extension.get(field) if field == 'onboardingSkill' else interface.get(field)
        if not value:
            if field in ('composerIcon', 'logo'):
                errors.append(f'Missing {field}')
            continue
        if not isinstance(value, str) or not value.startswith('./'):
            errors.append(f'{field} must be a ./-prefixed package path')
            continue
        path = root / value
        if not inside(root, path) or not path.is_file() or path.resolve() not in included_paths:
            errors.append(f'{field} does not resolve to a bundled package file')
            continue
        if field != 'onboardingSkill' and path.suffix == '.svg':
            try:
                raw = path.read_text()
                if '<!DOCTYPE' in raw.upper() or '<!ENTITY' in raw.upper():
                    raise ValueError('SVG entity declarations are not allowed')
                svg = ET.fromstring(raw)
                if svg.tag != '{http://www.w3.org/2000/svg}svg':
                    raise ValueError('SVG namespace/root is invalid')
                box = [float(item) for item in svg.get('viewBox', '').split()]
                if len(box) != 4 or not all(math.isfinite(item) for item in box) or box[2] != box[3] or not 48 <= box[2] <= 4096:
                    errors.append(f'{field} needs a finite square viewBox from 48 through 4096 pixels')
                for element in svg.iter():
                    if element.tag.rsplit('}', 1)[-1] in {'script', 'foreignObject'}:
                        raise ValueError('Active SVG content is unsupported')
                    for key, value in element.attrib.items():
                        local = key.rsplit('}', 1)[-1]
                        if local.lower().startswith('on') or (local == 'href' and not value.startswith(('#', 'data:image/png;base64,'))):
                            raise ValueError('External or active SVG resources are unsupported')
                if re.search(r'@import', raw, re.I) or any(not reference.strip().strip('\"\x27').startswith('#') for reference in re.findall(r'url\(([^)]*)\)', raw, re.I)):
                    raise ValueError('SVG stylesheet resource is unsupported')
                if path.stat().st_size > 5 * 1024 * 1024:
                    errors.append(f'{field} exceeds the 5 MiB icon limit')
            except (ValueError, ET.ParseError):
                errors.append(f'{field} is not a valid supported SVG')
        if field != 'onboardingSkill' and path.suffix == '.png':
            try:
                png_dimensions(path)
            except (OSError, ValueError, zlib.error) as error:
                errors.append(f'{field}: {error}')
        if field != 'onboardingSkill' and path.suffix not in {'.png', '.svg'}:
            errors.append(f'{field} must use a supported PNG or SVG asset')
    for forbidden in ('apps', 'hooks'):
        if forbidden in extension:
            errors.append(f'{forbidden} is outside this public skills package architecture')
    if (root / 'mcp.json').exists() or (root / '.app.json').exists() or (root / 'hooks').exists():
        errors.append('This skills-only package must not imply an undeclared hosted integration')
    skills = sorted((root / 'skills').glob('*/SKILL.md'))
    if not skills:
        errors.append('No bundled skills')
    names = []
    for skill in skills:
        text = skill.read_text()
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f'{skill.parent.name}: invalid frontmatter')
            continue
        header = {}
        for line in parts[1].splitlines():
            if ':' in line:
                key, value = line.split(':', 1)
                value = value.strip()
                try:
                    header[key.strip()] = json.loads(value) if value.startswith('"') else value
                except ValueError:
                    errors.append(f'{skill.parent.name}: invalid quoted frontmatter')
        name = header.get('name')
        names.append(name)
        if name != skill.parent.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name or ''):
            errors.append(f'{skill.parent.name}: skill name/folder mismatch')
        if not isinstance(header.get('description'), str) or not header['description'].strip():
            errors.append(f'{skill.parent.name}: missing description')
        if any(x in text for x in ('${CLAUDE_PLUGIN_ROOT}', 'claude-seo run', 'Task tool', 'maxTurns:')):
            errors.append(f'{skill.parent.name}: unresolved source-runtime assumption')
        ui = skill.parent / 'agents/openai.yaml'
        if not ui.exists():
            errors.append(f'{skill.parent.name}: missing skill UI metadata')
    if len(names) != len(set(names)):
        errors.append('Duplicate skill names')
    local_modules = {p.stem for p in (root / 'scripts').glob('*.py')}
    for path in root.rglob('*'):
        if path.is_symlink():
            errors.append('Package contains a symlink')
    for path in files:
        relative = path.relative_to(root).as_posix()
        if '\\' in relative or ':' in relative or any(part in ('.', '..') for part in Path(relative).parts):
            errors.append(f'Nonportable archive path: {relative}')
        if any(part.startswith('.') and part not in ('.codex-plugin',) for part in path.relative_to(root).parts):
            errors.append(f'Unexpected hidden package file: {relative}')
        if re.search(PROVIDER_PATTERN, relative, re.I):
            errors.append(f'Excluded provider material in package file: {relative}')
        raw = path.read_bytes()
        if re.search(PROVIDER_PATTERN.encode(), raw, re.I):
            errors.append(f'Excluded provider material in package file: {relative}')
        if any(re.search(pattern.encode(), raw) for pattern in SECRET_PATTERNS):
            errors.append(f'Possible secret in package file: {relative}')
        if path.suffix == '.png':
            continue
        if path.suffix not in {'.json', '.md', '.py', '.yaml', '.svg'} and path.name != 'LICENSE':
            errors.append(f'Unsupported package file type: {relative}')
            continue
        try:
            value = raw.decode('utf-8')
        except UnicodeError:
            errors.append(f'Package text is not UTF-8: {relative}')
            continue
        if '\u2014' in value:
            errors.append(f'Em dash in authored package file: {relative}')
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', value):
                if target.startswith(('https://', 'http://', '#')):
                    continue
                target = target.strip('<>').split('#')[0]
                destination = path.parent / target
                if not inside(root, destination) or not destination.is_file() or destination.resolve() not in included_paths:
                    errors.append(f'Broken or escaping Markdown resource in {relative}: {target}')
        if path.suffix == '.py':
            try:
                syntax = ast.parse(value)
                for node in ast.walk(syntax):
                    imports = ([x.name for x in node.names] if isinstance(node, ast.Import)
                               else [node.module or ''] if isinstance(node, ast.ImportFrom) else [])
                    if any(x not in OFFLINE_IMPORTS | local_modules for x in imports):
                        errors.append(f'Network/process or unreviewed import in offline helper: {relative}')
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {'__import__', 'eval', 'exec', 'compile'}:
                        errors.append(f'Dynamic import or code execution in offline helper: {relative}')
            except SyntaxError:
                errors.append(f'Invalid Python syntax: {relative}')
    for needed in ('LICENSE', 'NOTICE.md', 'provenance.json', 'legal/PRIVACY.md'):
        if not (root / needed).is_file():
            errors.append(f'Missing attribution or data behavior resource: {needed}')
    try:
        source = json.loads((root / 'provenance.json').read_text())
        adapted = set(source['adapted_workflows'])
        deferred = set(source['deferred_source_workflows'])
        if adapted | deferred != set(source['source_workflows']) or adapted & deferred:
            errors.append('Source workflow coverage does not reconcile')
        if len(source['source_workflows']) + source.get('excluded_source_workflow_count', 0) != source['upstream'].get('source_skill_count', len(source['source_workflows'])):
            errors.append('Source inclusion and exclusion counts do not reconcile')
        if set(names) != adapted | set(source['new_workflows']):
            errors.append('Bundled workflows do not match provenance')
        if not re.fullmatch(r'[0-9a-f]{40}', source['upstream']['commit']):
            errors.append('Source provenance needs an exact commit')
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        errors.append('Invalid source provenance')
    content_digest = package_content_digest(root)
    if public:
        if not https_url(interface.get('privacyPolicyURL')):
            errors.append('Public release: published privacy policy URL is missing')
        acceptance = {}
        if acceptance_path and Path(acceptance_path).is_file():
            try:
                acceptance = json.loads(Path(acceptance_path).read_text())
                if not isinstance(acceptance, dict):
                    raise ValueError('Acceptance receipt must be an object')
            except (OSError, ValueError):
                acceptance = {}
                errors.append('Public release: invalid acceptance receipt')
        if acceptance:
            if acceptance.get('plugin_name') != manifest.get('name') or acceptance.get('version') != manifest.get('version'):
                errors.append('Public release: acceptance receipt is for another plugin or version')
            if acceptance.get('manifest_sha256') != hashlib.sha256((root / 'plugin.json').read_bytes()).hexdigest():
                errors.append('Public release: acceptance receipt does not match this manifest')
            if acceptance.get('package_content_sha256') != content_digest:
                errors.append('Public release: acceptance receipt does not match package content')
        for gate in ('chatgpt_installed_acceptance', 'publisher_verification', 'openai_approval'):
            if not isinstance(acceptance.get(gate), dict) or acceptance[gate].get('status') != 'passed':
                errors.append(f'Public release: {gate} is not evidenced')
        warnings.append('A local release preflight does not verify portal state or directory eligibility')
    else:
        warnings.append('Installed ChatGPT behavior and public-directory approval are unverified')
    warnings.append('Offline-helper static lint is a limited guard; manual code review and host sandboxing remain necessary')
    return {'valid': not errors, 'mode': 'public_release' if public else 'local_package',
            'errors': sorted(set(errors)), 'warnings': sorted(set(warnings)),
            'skills': len(skills), 'files': len(files),
            'manifest_sha256': hashlib.sha256((root / 'plugin.json').read_bytes()).hexdigest(),
            'package_content_sha256': content_digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--public', action='store_true', help='Separate public release evidence gate')
    parser.add_argument('--acceptance', type=Path, help='External acceptance receipt; never put credentials here')
    args = parser.parse_args()
    result = validate(args.root, args.public, args.acceptance)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()
