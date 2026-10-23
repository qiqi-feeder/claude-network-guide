# Maintain and validate the guide

[简体中文](../maintaining.md) | **English** · [Guide home](../../README.en.md)

Run from the repository root with Python 3.10 or later:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python skills/claude-network-setup/scripts/check_delivery.py .
```

The builder generates files; it does not deploy them. Use the sample node only for syntax testing:

```powershell
python skills/claude-network-setup/scripts/build_client.py --node examples/node.example.json --source-file tests/fixtures/whitelist.conf --nested-file tests/fixtures/apple-news.list --output outputs/example.yaml --allow-example
```

If Mihomo is installed, add `--mihomo` with the real core path and `--data-dir` with an existing rule database directory for core validation. Do not start this example as the active network profile. Unit tests do not install software, sign in, or change live networking.

## Update rules

Run the builder again with the same private node file. It downloads and converts the whitelist and records source hashes. Validate, back up the active profile, import or reload the output using your client's supported mechanism, and verify relevant behavior. The builder does not apply profiles or schedule updates.

Stop on new unsupported rules, external sources, or validation failures, preserving the previous profile. Do not silently discard rules. An upstream update does not mean each entry has been manually reviewed again. Keep protected routing and DNS domains aligned, including shared verification and static resources.

## Before publishing

Review the working tree and staged changes. Never publish private files, generated profiles, backups, reports, real node settings, or unredacted screenshots. Automated scanning supplements manual review.

Report only tests actually run. Avoid guarantees of account safety, zero leakage, or universal compatibility. Update VPS check dates and affiliate disclosures together.

## Translation layout

`README.md` is the Chinese entry point; `README.en.md` is the English entry point. English guides live in `docs/en/` and link to their Chinese counterparts. Keep prices, routing boundaries, commands, and privacy guidance aligned when editing either language. The executable Skill and scripts remain shared; do not fork code for each language. New languages should include a guide index and translated user documentation, with any remaining untranslated content explicitly identified.
