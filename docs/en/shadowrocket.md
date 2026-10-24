# iPhone: Shadowrocket with your own VPS

[简体中文](../shadowrocket.md) | **English** · [Guide home](../../README.en.md)

This mobile workflow uses an existing sing-box + VLESS Reality server and **Johnshall's blacklist with ad blocking**, as recommended in the linked tutorial. Unmatched traffic goes directly. The Windows guide uses a whitelist with unmatched traffic proxied. Our extension is an additional configuration, not the tutorial author's original file.

## Import and activate

1. Import your own VLESS node. Check its address, port, UUID, Reality public key, short ID, SNI, and Vision settings. Node links and QR codes contain credentials: keep them private.
2. Add the [community blacklist](https://raw.githubusercontent.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever/release/sr_top500_banlist_ad.conf) on the **Config** page, retaining the filename `sr_top500_banlist_ad.conf`. It is not a server subscription for the Home page.
3. Download the [extension template](../../examples/shadowrocket-ai-extension.example.conf). Replace every `MY-US-VPS` with your node's name; a simple ASCII name avoids encoding issues in DNS parameters.
4. Import and activate the extension, and select **Config** under Global Routing. Its `include` inherits the community file. Only the extension needs the active checkmark; keep the base file installed.

A Windows local file link cannot be downloaded directly on an iPhone. Transfer it through iCloud Drive / Files, or open **Config → Wi-Fi Upload** and use a computer on the same LAN to upload through the address displayed by the phone.

The template contains no server credentials and adds fixed AI routing and proxy DNS without bundling the upstream list. Back up your current configuration. Text checks do not replace testing on your device.

## Updates and list size

Keep the base profile's remote update source and enable configuration updates and iOS background refresh. Manually update once and inspect the timestamp and compiled rules. Server subscriptions update separately. Keep custom rules in the extension so an upstream replacement does not overwrite them. Recheck inheritance after upstream filename or syntax changes; background updates are subject to iOS scheduling and network availability.

Large lists can increase download, compilation, and memory costs. Compiled sizes differ from source sizes. File size alone does not explain slow WeChat uploads: inspect actual connections first.

## Verify each path separately

| Observation | Meaning |
|---|---|
| HTTP exit | Check that protected requests use your fixed VPS |
| DNS resolver exit | May differ from the VPS; verify protected queries' path too |
| Domestic WebRTC / STUN public address | That probe learned a domestic exit, even if DNS passed |
| Domestic direct IPv4 | Can be expected for an allowed direct test endpoint; does not prove Claude's main request went directly |

A WebRTC candidate is an address collected for establishing a connection. A VPS candidate alone is not evidence of domestic IP exposure. A real domestic public candidate requires investigation. Third-party scores are not Claude enforcement decisions.

The template's `ipv6 = false` applies to Shadowrocket, not all of iOS. Do not infer that every IPv6 bypass is blocked. A blanket IPv6 rejection can break domestic apps.

For domestic WebRTC candidates, close Claude, try **Settings → UDP → Disable STUN**, keep UDP forwarding enabled, reconnect, and retest in a fresh page. Check calls and P2P afterward. Do not fake STUN responses to obtain a green score. The template rejects unsupported UDP instead of falling back directly; inspect other fallback settings too. None of these settings proves every UDP path is protected.

## Acceptance and troubleshooting

- Rule Test should send `claude.ai` to `AI-US`, containing only your VPS and no `DIRECT`. Inspect real connections under **Data** as well.
- Test HTTP, DNS, WebRTC, IPv6, and Wi-Fi / cellular changes separately. Record the time, network, and active profile.
- With Claude closed, simulate an unavailable node and verify protected requests fail without direct fallback. Restore the node before reopening Claude. Failure, sleep, and network-switch behavior has not been validated on every supported version.
- For slow WeChat uploads, inspect destination, matched rule, and actual policy during an upload. Investigate the local network if direct, or routing and the VPS if proxied. Avoid blanket bypasses for the entire app or Tencent ASN.
- App Store uses multiple Apple/CDN destinations. Inspect their rules rather than assuming one policy for the whole app.

**A blacklist cannot guarantee that arbitrary pages or probes never learn your domestic IP.** Unmatched direct traffic is intentional. Fixed AI rules protect only their matching scope; stricter requirements need a separately designed and tested routing, isolation, and failure-blocking setup.

References: [original tutorial](https://x.com/zureA255062/status/2107655494034989058), [Johnshall rules](https://github.com/Johnshall/Shadowrocket-ADBlock-Rules-Forever), and the [LOWERTOP community manual](https://github.com/LOWERTOP/Shadowrocket). The manual is unofficial; menus and fields depend on your installed version.
