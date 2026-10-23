# Troubleshoot the actual connection path

[简体中文](../../skills/claude-network-setup/references/troubleshooting.md) | **English** · [Guide home](../../README.en.md)

## WeChat text works, but images fail

Read live core connections and logs first. If domestic IPv6 connections on ports such as 443 or 8000 repeatedly match `IPCIDR(::/0) REJECT`, remove the blanket IPv6 rejection and let domestic IP rules select direct access. IPv6 should still enter TUN; protected overseas traffic must retain its proxy route.

WeChat may cache a failed state. Ask the user to exit it fully from the tray, reopen it, and retry. Do not send images to contacts without explicit authorization. Report recovery only after user confirmation, and retest protected routes and node failure behavior.

If traffic actually goes through the VPS, inspect domain rules, process identification, and Tencent's overseas endpoints. Broad Tencent ASN or whole-process bypasses can expand direct access substantially; use a scoped fix with a rollback path.

## DNS warnings

Check the tested domain, resolver ownership, and query path. Domestic DNS for an allowed domestic domain is expected under split routing. Protected domains unexpectedly using domestic resolution need investigation. Test browser secure DNS and extensions before attributing the cause.

## WebRTC reports “candidate leak”

If the candidate is the VPS IP, that test used the proxy exit; it did not reveal a Chinese public IP. Domestic STUN endpoints may show a direct address under split routing. One test does not cover all endpoints or future page dependencies.

## HTTP 403 or an account hold

A command-line 403 does not establish that browser login will fail. `Account on hold` is an account-side state. Use the official review process; cache cleanup or timezone changes do not resolve it.

## Timezone and language

Switching between UTC+8 zones usually preserves the displayed clock while changing the timezone name exposed to websites. Change it only when requested and explain calendar and app effects. Timezone changes do not fix routing or establish service eligibility.
