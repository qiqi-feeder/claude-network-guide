# Verify the setup and prepare rollback

[简体中文](../../skills/claude-network-setup/references/verification.md) | **English** · [Guide home](../../README.en.md)

Back up first, validate the candidate profile with the core, then apply changes in stages while preserving management access. Test the behavior affected by each change.

| Check | Evidence to collect | Limit |
|---|---|---|
| Node exit | HTTPS through the isolated node; use two check sources if needed | Does not establish account eligibility or lasting IP reputation |
| Claude routing | Real TLS connection, live connection chain, matched rule | Configuration text alone is insufficient |
| Domestic sites | Sample requests and confirmed DIRECT routes | Does not cover every service |
| DNS | System queries, core DNS paths, browser tests | Resolver IP need not equal VPS IP |
| UDP/WebRTC | Browser STUN tests and candidate addresses | A candidate address alone is not a real-IP leak |
| IPv6 | Both routes and actual AAAA/Fake AAAA connection chains | A top-level setting alone is insufficient |
| Failure behavior | Fresh connections while only the private node is unavailable | Does not establish protection after quitting Clash |
| App compatibility | User retries WeChat images, files, and normal workflows | A good test score does not prove apps work |
| Persistence | Restart the client and recheck profile and live paths | Saving a file alone is insufficient |

You can use [ip.net.coffee's Claude check](https://ip.net.coffee/claude/) alongside independent tools. Record third-party scores, HTTP responses, TLS results, and browser login as separate observations. Do not log in or accept terms on the user's behalf merely to complete a network check.

## Test a node failure safely

Save the running configuration and selection state. In a candidate copy, change only the private node's port to an unavailable value. Validate and temporarily load it, then attempt new protected IPv4 and IPv6 connections. Both should fail without `DIRECT` fallback.

Restore in `try/finally`, even if testing raises an exception. Retest after restoring and stop temporary processes. Do not switch the group to `DIRECT` to simulate a failure or disrupt the server firewall and the only SSH path.

This test keeps the core running. Client exit, sleep, startup gaps, and network changes require separate checks.

## Handoff and rollback

Record versions, source dates and hashes, configuration entry points, actual changes, results, untested items, user-confirmed app behavior, and recovery locations. Keep screenshots private unless redacted; they can expose addresses, email, and history.

Restore original source profiles and preferences, restart the client, and verify connectivity. Restoring only a generated file may not persist. Preserve server services the user still needs. On update failure, retain the previous working profile instead of deploying empty rules.
