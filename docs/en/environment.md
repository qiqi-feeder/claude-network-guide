# Inspect your environment

[简体中文](../../skills/claude-network-setup/references/environment.md) | **English** · [Guide home](../../README.en.md)

## Windows

Start with `skills/claude-network-setup/scripts/inspect_windows.ps1`. It reports proxy processes, TUN and default routes, DNS, timezone, and whether relevant environment variables exist. It does not read token values.

Locate the actual Clash Verge data directory, version, selected profile, and configuration source. A common directory is `%APPDATA%\io.github.clash-verge-rev.clash-verge-rev`, but check rather than assume. `profiles.yaml` may contain private subscription URLs; never publish the whole file.

Inspect the source profile, generated file, and live core configuration separately. Verify system proxy, TUN, strict routing, IPv6, and DNS overrides in the running setup. Identify the browser profile actually in use; checking only Chrome's Default profile does not cover all profiles.

## VPS

Collect the public address, actual SSH port, username, and authentication method. Test direct TCP connectivity without an existing proxy. Failed ICMP does not prove the server is unreachable. Verify the first SSH host fingerprint against the provider console or another trusted record; do not permanently disable host-key checking.

After login, inspect the OS, architecture, memory, disk, time synchronization, listeners, existing sing-box/Xray installations or panels, services, firewall, public IPv6, package sources, and TLS connectivity to candidate handshake sites. A login banner can be stale.

Check IPv6 separately on Windows and the VPS. A server without public IPv6 says nothing about the PC's IPv6 connectivity. Check cloud security groups independently from the OS firewall.

## Record the results

Label each item **verified**, **configured but untested**, **not checked**, or **needs repair**. SSH reachability, a successful Reality handshake, a target service response, and account login are separate results.

An HTTP 403 can reflect authentication, bot protection, or site policy; it is not proof that an IP is banned. A 404 at a root path proves a response was received, not that API authentication works.
