"""Render a private Mihomo client without changing the active network."""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request
import uuid

import yaml

SOURCE = 'https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/release/sr_top500_whitelist_ad.conf'
NESTED = 'https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Shadowrocket/AppleNews/AppleNews.list'
GROUP = 'US-VPS'
NODE = 'US-VPS-Reality'
REMOTE_DNS = ['https://1.1.1.1/dns-query#US-VPS', 'https://8.8.8.8/dns-query#US-VPS']
LOCAL_DNS = ['https://223.5.5.5/dns-query#DIRECT', 'https://1.12.12.12/dns-query#DIRECT']
PROTECTED = [
    'anthropic.com', 'claude.ai', 'claude.com', 'clau.de', 'claudeusercontent.com',
    'claudemcpclient.com', 'claudemcpcontent.com', 'openai.com', 'chatgpt.com',
    'oaistatic.com', 'oaiusercontent.com', 'oaistatsig.com', 'statsig.com',
    'statsigapi.net', 'featuregates.org', 'featureassets.org', 'cloudflare.com',
    'cloudflare.net', 'cloudflareinsights.com', 'google.com', 'gstatic.com',
    'hcaptcha.com', 'recaptcha.net', 'arkoselabs.com', 'auth0.com',
    'workos.com', 'workos.dev', 'authkit.app',
]
EXACT = ['servd-anthropic-website.b-cdn.net', 'cdn.usefathom.com']


def fetch(url: str) -> str:
    # Only the fixed reviewed upstreams are passed by this script.
    with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'claude-network-guide/1'}), timeout=30) as response:
        raw = response.read(10_000_001)
    if len(raw) > 10_000_000:
        raise ValueError('Rule source exceeds size limit')
    return raw.decode('utf-8-sig')


def match_parts(parts: list[str]) -> list[str]:
    kind = parts[0].upper()
    if kind == 'IP-CIDR':
        kind = 'IP-CIDR6' if ipaddress.ip_network(parts[1], strict=False).version == 6 else kind
    if kind not in {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6', 'IP-ASN', 'GEOIP'}:
        raise ValueError('Unsupported rule type: ' + kind)
    parts[0] = kind
    return parts


def convert(source: str, load_nested) -> list[str]:
    section, rules, final_seen = '', [], False
    for raw in source.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('['):
            section = line
            continue
        if section != '[Rule]':
            continue
        if final_seen:
            raise ValueError('Rule appears after FINAL')
        parts = [x.strip() for x in line.split(',')]
        kind = parts[0].upper()
        if kind == 'FINAL':
            if parts != ['FINAL', 'PROXY'] and [x.upper() for x in parts] != ['FINAL', 'PROXY']:
                raise ValueError('Whitelist must end with FINAL,PROXY')
            rules.append('MATCH,' + GROUP)
            final_seen = True
            continue
        if len(parts) < 3:
            raise ValueError('Malformed rule')
        action = {'DIRECT': 'DIRECT', 'PROXY': GROUP, 'REJECT': 'REJECT'}.get(parts[2].upper())
        if action is None:
            raise ValueError('Unsupported rule action')
        if kind == 'RULE-SET':
            if len(parts) != 3 or parts[1] != NESTED:
                raise ValueError('Unreviewed nested source')
            for child in load_nested(parts[1]).splitlines():
                child = child.strip()
                if not child or child.startswith('#'):
                    continue
                child_parts = match_parts(child.split(','))
                if len(child_parts) != 2:
                    raise ValueError('Unexpected nested rule fields')
                rules.append(','.join(child_parts + [action]))
        else:
            parts = match_parts(parts)
            if any(x not in {'no-resolve'} for x in parts[3:]):
                raise ValueError('Unsupported rule option')
            parts[2] = action
            rules.append(','.join(parts))
    if not final_seen:
        raise ValueError('Missing proxy default')
    result = []
    for rule in rules:
        if rule.startswith(('IP-CIDR,', 'IP-CIDR6,', 'IP-ASN,', 'GEOIP,')) and 'no-resolve' not in rule.split(',')[3:]:
            rule += ',no-resolve'
        result.append(rule)
    return result


def validate_node(data: dict, allow_example: bool = False) -> dict:
    server = str(data['server'])
    address = ipaddress.ip_address(server)  # IP endpoint avoids circular bootstrap DNS.
    identity = uuid.UUID(str(data['uuid']))
    port = data.get('port', 443)
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise ValueError('Invalid node port')
    if not allow_example and (not address.is_global or identity.int <= 1):
        raise ValueError('Documentation/private endpoint rejected; supply your own node')
    public = str(data['public_key'])
    if not re.fullmatch(r'[A-Za-z0-9_-]{43}', public) or len(base64.urlsafe_b64decode(public + '=')) != 32:
        raise ValueError('Reality public_key must encode 32 bytes')
    short = str(data['short_id'])
    if not re.fullmatch(r'(?:[0-9a-fA-F]{2}){1,8}', short):
        raise ValueError('short_id must be 1 to 8 bytes of hex')
    sni = str(data['server_name'])
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?', sni):
        raise ValueError('Invalid server_name')
    return {'name': NODE, 'type': 'vless', 'server': server, 'port': port, 'uuid': str(identity),
            'udp': True, 'flow': 'xtls-rprx-vision', 'network': 'tcp', 'tls': True,
            'servername': sni, 'client-fingerprint': 'chrome', 'skip-cert-verify': False,
            'reality-opts': {'public-key': public, 'short-id': short}}


def build(node: dict, source_rules: list[str]) -> dict:
    if not source_rules or source_rules[-1] != 'MATCH,' + GROUP:
        raise ValueError('A proxy default is required')
    ai = ['DOMAIN-SUFFIX,' + name + ',' + GROUP for name in PROTECTED]
    ai += ['DOMAIN,' + name + ',' + GROUP for name in EXACT]
    ai += ['DOMAIN-KEYWORD,' + name + ',' + GROUP for name in ['claude', 'anthropic', 'openai']]
    # Preserve ad precedence, then override broad direct allowlists for protected services.
    split = next((i for i, rule in enumerate(source_rules) if (rule.split(',')[2] if len(rule.split(',')) > 2 else rule.split(',')[-1]) != 'REJECT'), len(source_rules) - 1)
    own_ip = ipaddress.ip_address(node['server'])
    prefix = [f"{'IP-CIDR6' if own_ip.version == 6 else 'IP-CIDR'},{own_ip}/{own_ip.max_prefixlen},DIRECT,no-resolve"]
    policy = {'geosite:cn,private': list(LOCAL_DNS)}
    policy.update({'+.' + name: list(REMOTE_DNS) for name in PROTECTED})
    policy.update({name: list(REMOTE_DNS) for name in EXACT})
    return {
        'mode': 'rule', 'mixed-port': 7897, 'allow-lan': False, 'bind-address': '127.0.0.1',
        'log-level': 'info', 'ipv6': True, 'profile': {'store-selected': True},
        'tun': {'enable': True, 'stack': 'gvisor', 'auto-route': True, 'strict-route': True,
                'auto-detect-interface': True, 'dns-hijack': ['any:53', 'tcp://any:53'],
                'inet6-address': ['fdfe:dcba:9876::1/126'],
                'route-address': ['0.0.0.0/1', '128.0.0.0/1', '::/1', '8000::/1']},
        'dns': {'enable': True, 'listen': '127.0.0.1:1053', 'ipv6': True,
                'enhanced-mode': 'fake-ip', 'fake-ip-range': '198.18.0.1/16',
                'fake-ip-filter': ['*.lan', '*.local', '*.localhost', 'localhost', '+.msftncsi.com', '+.msftconnecttest.com'],
                'default-nameserver': ['223.5.5.5', '119.29.29.29'],
                'proxy-server-nameserver': list(LOCAL_DNS), 'nameserver': list(REMOTE_DNS),
                'nameserver-policy': policy, 'direct-nameserver': list(LOCAL_DNS),
                'direct-nameserver-follow-policy': True, 'fallback': [], 'prefer-h3': False},
        'proxies': [node], 'proxy-groups': [{'name': GROUP, 'type': 'select', 'proxies': [NODE]}],
        'rules': prefix + source_rules[:split] + ai + source_rules[split:],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--node', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-file', type=Path)
    parser.add_argument('--nested-file', type=Path)
    parser.add_argument('--allow-example', action='store_true')
    parser.add_argument('--mihomo', type=Path)
    parser.add_argument('--data-dir', type=Path)
    args = parser.parse_args(argv)
    node = validate_node(json.loads(args.node.read_text(encoding='utf-8-sig')), args.allow_example)
    sources = {}
    def get(url):
        local = args.source_file if url == SOURCE else args.nested_file
        text = local.read_text(encoding='utf-8-sig') if local else fetch(url)
        sources[url] = hashlib.sha256(text.encode()).hexdigest()
        return text
    config = build(node, convert(get(SOURCE), get))
    manifest = {'source_sha256': sources, 'generated': dt.datetime.now(dt.timezone.utc).isoformat(),
                'rule_count': len(config['rules']), 'core_validated': bool(args.mihomo)}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix='.candidate-', suffix='.yaml', dir=args.output.parent)
    temp = Path(temp_name)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write('# PRIVATE GENERATED CONFIG — do not publish\n')
            yaml.safe_dump(config, stream, allow_unicode=True, sort_keys=False)
        if args.mihomo:
            cmd = [str(args.mihomo), '-t', '-f', str(temp)]
            if args.data_dir:
                cmd += ['-d', str(args.data_dir)]
            subprocess.run(cmd, check=True)
        # All network, parsing and optional core checks finish before replacing output.
        os.replace(temp, args.output)
        manifest_path = args.output.with_suffix('.sources.json')
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    finally:
        temp.unlink(missing_ok=True)
    print(f'Generated {len(config["rules"])} rules. Active Clash configuration was not changed.')
    print('Core validation passed.' if args.mihomo else 'Core validation not performed; validate before applying.')


if __name__ == '__main__':
    main()
