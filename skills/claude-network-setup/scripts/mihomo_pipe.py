"""Read local Mihomo status through a Windows named pipe; never mutate configuration."""
import argparse
import json
import os


def read_status(pipe_name='verge-mihomo'):
    if os.name != 'nt':
        raise RuntimeError('Windows named pipes are required')
    if not pipe_name.replace('-', '').replace('_', '').isalnum():
        raise ValueError('Invalid pipe name')
    with open('\\\\.\\pipe\\' + pipe_name, 'r+b', buffering=0) as pipe:
        pipe.write(b'GET /configs HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n')
        header = bytearray()
        while not header.endswith(b'\r\n\r\n'):
            value = pipe.read(1)
            if not value or len(header) > 65536:
                raise RuntimeError('Invalid HTTP response')
            header.extend(value)
        lines = header.decode().split('\r\n')
        if ' 200 ' not in lines[0]:
            raise RuntimeError('Local API did not return success')
        fields = {line.split(':', 1)[0].lower(): line.split(':', 1)[1].strip() for line in lines[1:] if ':' in line}
        def exact(count):
            data = bytearray()
            while len(data) < count:
                part = pipe.read(count - len(data))
                if not part:
                    raise RuntimeError('Unexpected end of response')
                data.extend(part)
            return data
        if 'content-length' in fields:
            length = int(fields['content-length'])
            if not 0 <= length <= 5_000_000:
                raise RuntimeError('Response too large')
            raw = exact(length)
        elif fields.get('transfer-encoding') == 'chunked':
            raw = bytearray()
            while True:
                line = bytearray()
                while not line.endswith(b'\r\n'):
                    line.extend(exact(1))
                    if len(line) > 1024:
                        raise RuntimeError('Invalid chunk header')
                size = int(line.strip().split(b';')[0], 16)
                if size == 0:
                    break
                if size < 0 or len(raw) + size > 5_000_000:
                    raise RuntimeError('Response too large')
                raw.extend(exact(size))
                if exact(2) != b'\r\n':
                    raise RuntimeError('Invalid chunk ending')
        else:
            raise RuntimeError('Unsupported HTTP framing')
    config = json.loads(raw)
    tun = config.get('tun', {})
    return {'mode': config.get('mode'), 'ipv6': config.get('ipv6'),
            'tun': {key: tun.get(key) for key in ['enable', 'stack', 'auto-route', 'strict-route', 'dns-hijack', 'route-address']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pipe', default='verge-mihomo')
    print(json.dumps(read_status(parser.parse_args().pipe), ensure_ascii=False, indent=2))
