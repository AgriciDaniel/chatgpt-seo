"""Read dimensions from PNG, JPEG or GIF headers without decoding or editing pixels."""

import argparse
import struct

from seo_io import read_bytes, run


def inspect_image(data):
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        if len(data) < 33 or data[12:16] != b'IHDR' or struct.unpack('>I', data[8:12])[0] != 13:
            raise ValueError('Incomplete or invalid PNG dimension header')
        width, height = struct.unpack('>II', data[16:24])
        fmt, alpha = 'PNG', data[25] in {4, 6}
    elif data.startswith((b'GIF87a', b'GIF89a')):
        if len(data) < 13:
            raise ValueError('Incomplete GIF dimension header')
        width, height = struct.unpack('<HH', data[6:10])
        fmt, alpha = 'GIF', None
    elif data.startswith(b'\xff\xd8'):
        position, dimensions = 2, None
        while position < len(data):
            if data[position] != 255:
                raise ValueError('Invalid JPEG marker stream before dimensions')
            while position < len(data) and data[position] == 255:
                position += 1
            if position >= len(data):
                break
            marker = data[position]
            position += 1
            if marker in {0xD9, 0xDA}:
                break
            if marker in {0x01, *range(0xD0, 0xD9)}:
                continue
            if position + 2 > len(data):
                break
            length = struct.unpack('>H', data[position:position+2])[0]
            if length < 2 or position + length > len(data):
                raise ValueError('Truncated JPEG segment')
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                if length < 8:
                    raise ValueError('Invalid JPEG frame header')
                height, width = struct.unpack('>HH', data[position+3:position+7])
                dimensions = width, height
                break
            position += length
        if not dimensions:
            raise ValueError('JPEG dimensions were not found')
        width, height = dimensions
        fmt, alpha = 'JPEG', False
    else:
        raise ValueError('Supported headers are PNG, JPEG and GIF; use a host tool for other formats')
    if width <= 0 or height <= 0:
        raise ValueError('Image dimensions must be positive')
    return {'format_version': 1, 'evidence_level': 'supplied_binary_header',
            'format': fmt, 'bytes': len(data), 'width': width, 'height': height,
            'aspect_ratio': round(width / height, 6), 'alpha_channel_in_header': alpha,
            'limitations': ['Header inspection does not decode pixels or verify image integrity',
                            'An alpha channel does not prove pixels are transparent',
                            'No compression, resizing, visual, copyright or performance check was performed']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', help='Selected PNG/JPEG/GIF file, up to 30 MiB')
    args = parser.parse_args()
    run(lambda: inspect_image(read_bytes(args.file, 30 * 1024 * 1024)))


if __name__ == '__main__':
    main()
