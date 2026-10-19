"""URL values for offline evidence; these functions never fetch a URL."""

from urllib.parse import urljoin, urlsplit, urlunsplit


def absolute_url(value, base=None):
    if not isinstance(value, str) or not value:
        raise ValueError('A nonempty URL is required')
    if any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in value):
        raise ValueError('URL whitespace or controls are not supported')
    if base is not None:
        base = absolute_url(base)
        value = urljoin(base, value)
    parsed = urlsplit(value)
    if parsed.scheme not in {'http', 'https'} or not parsed.hostname:
        raise ValueError('An absolute HTTP(S) URL is required')
    if parsed.username is not None or parsed.password is not None:
        raise ValueError('URL credentials are not supported')
    try:
        port = parsed.port
    except ValueError:
        raise ValueError('Invalid URL port') from None
    hostname = parsed.hostname.lower()
    netloc = '[' + hostname + ']' if ':' in hostname else hostname
    if port is not None and port != {'http': 80, 'https': 443}[parsed.scheme]:
        netloc += ':' + str(port)
    return urlunsplit((parsed.scheme.lower(), netloc, parsed.path or '/', parsed.query, ''))


def origin(value):
    parsed = urlsplit(absolute_url(value))
    port = parsed.port if parsed.port is not None else {'http': 80, 'https': 443}[parsed.scheme]
    return parsed.scheme, parsed.hostname, port
