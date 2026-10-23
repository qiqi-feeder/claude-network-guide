import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'skills/claude-network-setup/scripts'
spec = importlib.util.spec_from_file_location('build_client', SCRIPTS / 'build_client.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.source = (ROOT / 'tests/fixtures/whitelist.conf').read_text()
        self.nested = (ROOT / 'tests/fixtures/apple-news.list').read_text()
        self.node = json.loads((ROOT / 'examples/node.example.json').read_text())

    def rules(self, source=None):
        return m.convert(source or self.source, lambda _: self.nested)

    def config(self):
        return m.build(m.validate_node(self.node, allow_example=True), self.rules())

    def test_example_cannot_be_accidentally_deployed(self):
        with self.assertRaises(ValueError):
            m.validate_node(self.node)

    def test_final_is_required_and_cannot_be_direct(self):
        for source in [self.source.replace('FINAL,PROXY', ''), self.source.replace('FINAL,PROXY', 'FINAL,DIRECT')]:
            with self.assertRaises(ValueError):
                self.rules(source)

    def test_unknown_rule_or_external_source_stops_conversion(self):
        for source in [self.source.replace('DOMAIN-SUFFIX,qq.com', 'SCRIPT,qq.com'), self.source.replace(m.NESTED, 'https://unreviewed.example/rules')]:
            with self.assertRaises(ValueError):
                self.rules(source)

    def test_ipv6_domestic_endpoints_are_not_blanket_blocked(self):
        c = self.config()
        self.assertIn('IP-CIDR6,2409:8c20:818:113::14/128,DIRECT,no-resolve', c['rules'])
        self.assertFalse(any(r.startswith('IP-CIDR6,::/0,REJECT') for r in c['rules']))
        self.assertIn('::/1', c['tun']['route-address'])

    def test_ai_overrides_upstream_direct_but_ads_remain_first(self):
        rules = self.config()['rules']
        self.assertLess(rules.index('DOMAIN-SUFFIX,claude.ai,US-VPS'), rules.index('DOMAIN-SUFFIX,claude.ai,DIRECT'))
        self.assertLess(rules.index('DOMAIN-SUFFIX,ads.example,REJECT'), rules.index('DOMAIN-SUFFIX,claude.ai,US-VPS'))

    def test_ai_dns_and_failure_policy(self):
        c = self.config()
        self.assertEqual(c['proxy-groups'][0]['proxies'], [m.NODE])
        self.assertEqual(c['rules'][-1], 'MATCH,US-VPS')
        for domain in ['claude.ai', 'claudeusercontent.com', 'claudemcpclient.com']:
            self.assertTrue(all(x.endswith('#US-VPS') for x in c['dns']['nameserver-policy']['+.' + domain]))
        self.assertEqual(c['dns']['fallback'], [])

    def test_no_resolve_for_all_ip_rules(self):
        for rule in self.rules():
            if rule.startswith(('IP-CIDR,', 'IP-CIDR6,', 'IP-ASN,', 'GEOIP,')):
                self.assertIn('no-resolve', rule.split(',')[3:])

    def test_no_mitm_or_source_dns_imported(self):
        c = self.config()
        self.assertNotIn('MITM', c)
        self.assertNotIn('127.0.0.1', c['dns']['nameserver'])

    def test_nested_rules_expanded(self):
        rules = self.rules()
        self.assertIn('DOMAIN,news.example,US-VPS', rules)
        self.assertFalse(any(r.startswith('RULE-SET,') for r in rules))

    def test_failed_conversion_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            output = d / 'output.yaml'
            output.write_text('previous usable config')
            source = d / 'source.conf'
            source.write_text('[Rule]\nFINAL,DIRECT\n')
            with self.assertRaises(ValueError):
                m.main(['--node', str(ROOT / 'examples/node.example.json'), '--source-file', str(source), '--output', str(output), '--allow-example'])
            self.assertEqual(output.read_text(), 'previous usable config')

    def test_shell_injection_is_not_a_valid_node(self):
        for key, value in [('server', '203.0.113.1;whoami'), ('server_name', 'example.com\ninvalid'), ('port', True), ('short_id', 'f')]:
            data = dict(self.node)
            data[key] = value
            with self.assertRaises(ValueError):
                m.validate_node(data, allow_example=True)


if __name__ == '__main__':
    unittest.main()
