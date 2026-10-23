# Configure Windows, routing, and DNS

[简体中文](../../skills/claude-network-setup/references/windows.md) | **English** · [Guide home](../../README.en.md)

## Build a local profile

Use Python 3.10 or later and the root `requirements.txt`. Store real node parameters outside the repository. `examples/node.example.json` contains unusable documentation addresses and sample credentials; the builder rejects them unless `--allow-example` is explicitly used for testing.

From the repository root, adjust paths to match your installation:

```powershell
python -m pip install -r requirements.txt
python skills/claude-network-setup/scripts/build_client.py --node C:\private\node.json --output outputs\clash.yaml --mihomo "C:\Program Files\Clash Verge\verge-mihomo.exe" --data-dir "$env:APPDATA\io.github.clash-verge-rev.clash-verge-rev"
```

The builder downloads the specified Johnshall whitelist and its reviewed AppleNews reference, recording source hashes and the build date. Use `--source-file` and `--nested-file` for existing local snapshots. Unknown rule types, actions, or unreviewed external sources stop the build.

`--mihomo` runs actual core syntax validation without applying the profile. Without it, report only that generation succeeded. Configuration and source records are replaced atomically; a failed build preserves the previous output. Back up the active configuration separately before deployment.

## Import and preserve changes

Import the YAML as a separate local profile in Clash Verge and select it. Keep existing subscription profiles available. Inspect the current profile structure instead of guessing IDs or copying another user's data directory. Back up any registration edits and ensure the app will not overwrite them.

Subscription updates can overwrite generated files. Make persistent changes in the local source or the appropriate override mechanism for the installed version. Editing only `clash-verge.yaml` is not sufficient.

## Routing and DNS

- The fixed `US-VPS` group contains only the private node. Final `MATCH` uses it, with no `DIRECT` fallback.
- Preserve upstream ad-rule order. Add protected domains and keywords before general direct rules. Test any ad-blocking exceptions rather than disabling the entire list.
- The domestic whitelist includes some overseas exceptions. Review that boundary. Apply `no-resolve` to IP and GEOIP rules so unknown domains are not resolved merely to check domestic IP matching.
- Default overseas DoH explicitly uses `#US-VPS`; domestic exceptions use `#DIRECT`. Protected domains use overseas resolution. A literal VPS IP does not require hostname bootstrap resolution.
- Fake-IP addresses are not evidence of a leak. DNS tests may correctly show Cloudflare or Google recursive resolver addresses.

## TUN and IPv6

Enable TUN automatic routing, strict routing, interface detection, and TCP/UDP port 53 interception. On an IPv6-capable network, verify that both IP families enter TUN and follow the same policy: domestic IPv6 may go direct; protected services and unmatched overseas traffic use the VPS. A blanket IPv6 rejection can break applications.

Verge can overwrite `dns.ipv6` and `fake-ip-range6`. Read the live configuration, inspect IPv6 routes, and test protected connections using AAAA records. Avoid disabling physical adapter IPv6, strict routing, or TUN just to make the YAML look consistent.

Inspect browser secure DNS, proxy extensions, other VPNs, WSL, and virtual machines separately. Explain the scope before changing them. Browser DoH behavior must be tested rather than assumed to leak.
