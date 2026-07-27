---
title: tdc configure
summary: Configure a local tdc profile interactively or non-interactively.
---

# tdc configure

Configures a local tdc profile. Without flags, this is the only interactive tdc command.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc configure
  [--help]
  [--non-interactive]
  [--region-code <string>]
  [--tdc-private-key <string>]
  [--tdc-public-key <string>]
  [--version]
```

## Options

- `--help`: Display help information.
- `--non-interactive`: Use this option to avoid being prompted for configuration values. You must provide at least three configuration values (`--tdc-public-key`, `--tdc-private-key`, and `--region-code`) when using this option. This is useful when running tdc in a script or automated environment.
- `--region-code <string>`: Default region code, for example `aws-us-east-1` or `aws-ap-southeast-1`.
- `--tdc-private-key <string>`: TiDB Cloud API private key.
- `--tdc-public-key <string>`: TiDB Cloud API public key.
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Configure tdc interactively

```bash
tdc configure
```

### Configure tdc for automation

```bash
TDC_REGION_CODE="aws-us-east-1" \
TDC_PUBLIC_KEY="<public-key>" \
TDC_PRIVATE_KEY="<private-key>" \
tdc configure --profile ci --non-interactive
```
