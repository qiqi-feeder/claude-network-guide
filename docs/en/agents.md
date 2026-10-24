# Use the guide as a Skill in different agents

[简体中文](../agents.md) | **English** · [Guide home](../../README.en.md)

`skills/claude-network-setup/` is the complete Skill package: `SKILL.md`, teaching references, scripts, and a mobile configuration template. It branches between Windows and iPhone workflows. Copy the whole directory, not just the entry file.

## Installation or direct reading

For agents with Skills support, follow that product's installation instructions and select this Skill directory. Discovery paths and invocation syntax vary; there is no universal installation command.

For an agent that can read a repository but does not support Skills, ask it to read the entry file and load the referenced resources as needed. This is prompt-based use, not native installation. A text-only agent needs the relevant material pasted in stages and cannot assume it has read missing files.

Example request:

```text
Read skills/claude-network-setup/SKILL.md and guide me step by step in English.
Identify my device, client, existing VPS, and current progress; ask only for missing details.
Give one manageable step at a time, explain the expected result, and use my feedback.
Start with read-only checks and a plan. Wait for my authorization before making changes.
If you cannot control my device, provide menu instructions and do not claim it is configured.
Do not request passwords in chat or publish private node credentials.
```

Add your actual setup, for example “iPhone + Shadowrocket, existing VPS, community blacklist with a separate extension.” The agent should preserve that choice rather than applying the Windows default everywhere.

## Capabilities and limits

The agent can explain steps, inspect sanitized configurations, generate files, and guide routing, DNS, WebRTC, and failure tests. Direct changes require suitable tools, device access, and user authorization. An ordinary chat agent cannot inspect local live connections or operate an iPhone. Screenshots do not prove every network path was tested.

The package does not depend on a specific agent's tools. Skill structure, resource links, and scripts are checked; installation and end-to-end execution have not been tested on every agent. Check the target product's documentation. Request English guidance if preferred; the executable entry and some underlying references remain in Chinese.
