# Set up sing-box with VLESS Reality

[简体中文](../../skills/claude-network-setup/references/server.md) | **English** · [Guide home](../../README.en.md)

Use this workflow only for a Linux VPS whose owner has authorized deployment. Inspect and back up existing workloads first. Preserve the OS and unknown services, and check port 443 before using it.

## Install and configure

Use a stable release from the [official package source](https://sing-box.sagernet.org/installation/package-manager/). Record the installed version and check its current VLESS and Reality fields.

On Debian or Ubuntu, check for conflicting sources, create the official APT keyring, add the signed repository, refresh the package index, and install sing-box. Keep signature verification enabled. Inspect the service unit's actual user and startup path. Avoid unreviewed third-party installation scripts.

Generate a unique UUID with `sing-box generate uuid`, a key pair with `sing-box generate reality-keypair`, and a Short ID using secure randomness. Keep the private key on the server and out of logs.

The configuration needs a VLESS inbound, an explicit listen address and TCP port, `users.uuid`, `flow: xtls-rprx-vision`, enabled TLS and Reality, handshake server and port, `private_key`, and `short_id`, with a direct outbound. Validate exact fields against the current documentation and `sing-box check`.

Test the handshake site's TLS, SNI, and certificate from the VPS. An example site is not guaranteed to remain suitable. The client connects to the VPS address and uses the agreed Reality server name.

Back up existing configuration before editing. Set minimum required file permissions for the service user. For a unit running as `sing-box`, ownership `root:sing-box` and mode `640` may be appropriate; confirm the unit first. Preserve existing keys unless rotating them deliberately.

## Enable and verify

Run `sing-box check -C /etc/sing-box` before enabling and starting the service. Inspect logs, listeners, and resource use. A running service does not establish that a client can connect.

Before enabling a firewall, allow the actual SSH and node ports, check cloud security groups, and confirm a second SSH session works. Do not assume SSH uses port 22. Restrict inbound access within the agreed scope; do not expose management panels or recursive DNS.

First test a temporary client on Windows without TUN, using separate ports. Check HTTPS and the exit IP before routing the whole PC through it. Stop the test process afterwards.

## Maintain the server

Back up, review migration notes, validate, restart, and retest when updating. Check service restarts, log growth, and SSH security periodically. Verify key authentication before disabling password login.

Deliver private node settings and recovery locations privately, never through GitHub. If the VPS cannot reach a target over IPv6, that connection should fail; do not add a direct client fallback.
