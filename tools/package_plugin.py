"""Build a reproducible ZIP with the portable manifest at archive root."""

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from validate_plugin import BASE, DEFAULT_ROOT, inside, inventory_digest, package_files, validate


def build(root=DEFAULT_ROOT, destination=None):
    root = Path(root).resolve()
    output = Path(destination).resolve() if destination else BASE / 'dist'
    if inside(root, output):
        raise ValueError('Package output must be outside the source plugin directory')
    result = validate(root)
    if not result['valid']:
        raise ValueError(json.dumps(result['errors']))
    manifest = json.loads((root / 'plugin.json').read_text())
    output.mkdir(parents=True, exist_ok=True)
    name = manifest['name'] + '-' + manifest['version']
    archive = output / (name + '.zip')
    temporary = output / (name + '.zip.tmp')
    entries = []
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in package_files(root):
            relative = path.relative_to(root).as_posix()
            data = path.read_bytes()
            info = zipfile.ZipInfo(relative, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            handle.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
            entries.append({'path': relative, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()})
    temporary.replace(archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / (name + '.sha256')).write_text(digest + '  ' + archive.name + '\n')
    inventory = {'plugin': manifest['name'], 'version': manifest['version'],
                 'archive_sha256': digest, 'package_content_sha256': inventory_digest(entries), 'files': entries}
    (output / (name + '.inventory.json')).write_text(json.dumps(inventory, indent=2) + '\n')
    return {'archive': str(archive), 'sha256': digest, 'package_content_sha256': inventory_digest(entries), 'files': len(entries),
            'bytes': archive.stat().st_size, 'public_release_status': 'not_approved'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.root, args.output), indent=2))


if __name__ == '__main__':
    main()
