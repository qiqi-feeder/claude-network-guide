# Claude Network Setup Guide

[简体中文](README.md) | **English**

A practical guide for **Windows, Clash Verge Rev, and your own VPS**, with a reusable AI Skill to help inspect, configure, and test the setup.

Start with an environment check, deploy sing-box with VLESS Reality, configure community routing rules, then test DNS, WebRTC, IPv6, node failures, and everyday apps. This repository contains general instructions and examples, with no personal server or account credentials.

Network checks cannot guarantee account access or change your location or eligibility. Check [Anthropic's supported countries](https://www.anthropic.com/supported-countries) and current terms before using its services.

## Get started

Give your AI assistant this repository and the following request:

```text
Read skills/claude-network-setup/SKILL.md in this repository.
Start with a read-only inspection of my Windows PC, Clash Verge, and VPS.
Report what works, what is missing, and the proposed changes in English.
Route local networks and recognized mainland China services directly.
Route protected services such as Claude, their DNS, and unmatched traffic through my VPS.
Connections that require the VPS must fail when it is unavailable, with no direct fallback.
Preserve UDP support, existing data, and domestic app compatibility.
Include real verification and rollback instructions.
Do not install or change anything until I approve the plan.
Let me enter passwords in a secure interface.
```

Review the plan before authorizing deployment. Keep an existing VPS if it works for you. If you need one, see [BandwagonHost and DMIT: plans, prices, and availability](docs/en/vps.md).

## Follow the guide

| Step | Guide | Outcome |
|---|---|---|
| 1 | [Inspect your environment](docs/en/environment.md) | Identify proxy, DNS, IPv6, and server issues |
| 2 | [Set up the VPS](docs/en/server.md) | Install and verify sing-box and Reality |
| 3 | [Configure Windows and Clash](docs/en/windows.md) | Create a local YAML profile, routing, DNS, and TUN |
| 4 | [Verify and roll back](docs/en/verification.md) | Test exits, DNS, UDP, IPv6, and node failures |
| 5 | [Troubleshoot](docs/en/troubleshooting.md) | Fix issues such as WeChat uploads |
| Optional | [Clean up old credentials](docs/en/privacy.md) | Remove selected data while preserving current sessions |

After network verification, read [First use, Google account region, and privacy](docs/en/claude-first-run.md).

For iPhone, see [Shadowrocket: blacklist, updates, and leak checks](docs/en/shadowrocket.md), including a credential-free extension template.

## Where Windows traffic goes

| Traffic | Connection | DNS |
|---|---|---|
| Local networks | Direct | Local resolution or explicit exceptions |
| Recognized mainland China services | Direct | Domestic encrypted DNS |
| Protected domains, including Claude and Anthropic | Fixed VPS | Overseas DoH through the VPS |
| Unmatched traffic | Fixed VPS | Default overseas DoH through the VPS |

The configuration uses Johnshall's whitelist with additional protection rules. The upstream whitelist includes some overseas direct exceptions. Review these before applying it.

## Understand the limits

- **Split routing does not provide anonymity across all sites.** A page can contact an allowed direct endpoint and learn your direct public IP. Stricter needs require an isolated environment or a different routing design.
- **Node failure protection depends on Clash and TUN running.** Test startup gaps, client exit, sleep, and network changes separately.
- **A DNS resolver's IP can differ from your VPS IP.** Verify the query path rather than relying on an address comparison alone.

## Use the Skill

The Skill supports step-by-step Windows and iPhone guidance, adapting to progress and available tools. See [Using it in different agents](docs/en/agents.md) for installation, direct reading, and capability limits.

You can ask an assistant to read the Skill directly. To install it, copy the entire `skills/claude-network-setup` directory into your tool's Skill directory, checking its current documentation first. Common locations are `~/.codex/skills/` for Codex and `~/.claude/skills/` for Claude Code. Preserve any existing customized copy.

```text
Use $claude-network-setup to inspect my network without making changes.
Respond in English and use the English guides linked from README.en.md.
```

The executable Skill instructions remain in Chinese; the English guides cover the same workflow. Scripts and configuration keys are shared across languages.

## Project information

- [Maintenance and checks](docs/en/maintaining.md)
- [Sources and acknowledgments](docs/en/sources.md)
- [Security](docs/en/security.md) · [Contributing](docs/en/contributing.md)
- [VPS recommendations and affiliate disclosure](docs/en/vps.md)

Tests cover conversion and configuration invariants. A real deployment still needs live verification.

Original documentation and scripts use the [MIT License](LICENSE). Community rules are downloaded at runtime and retain their upstream licenses. This project is independent of Anthropic, Clash Verge, and the VPS providers.
