---
title: tdc configure
summary: Configure a local TiDB Cloud CLI profile interactively or non-interactively.
---

# tdc configure

Configures a local TiDB Cloud CLI profile. Without flags, this is the only interactive TiDB Cloud CLI command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

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
- `--non-interactive`: Use this option to avoid being prompted for configuration values. You must provide at least three configuration values (`--tdc-public-key`, `--tdc-private-key`, and `--region-code`) when using this option. This is useful when running `tdc` in a script or automated environment.
- `--region-code <string>`: Default region code, for example `aws-us-east-1` or `aws-ap-southeast-1`.
- `--tdc-private-key <string>`: TiDB Cloud API private key.
- `--tdc-public-key <string>`: TiDB Cloud API public key.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

- Configure `tdc` interactively:

    ```bash
    # Enter the default region code and TiDB Cloud API keys when prompted.
    tdc configure
    ```

- Configure `tdc` for automation:

    ```bash
    # Supply all required values without interactive prompts.
    TDC_REGION_CODE="aws-us-east-1" \
    TDC_PUBLIC_KEY="<public-key>" \
    TDC_PRIVATE_KEY="<private-key>" \
    tdc configure --profile ci --non-interactive
    ```

## Related documentation

- [Install, Configure, and Update TiDB Cloud CLI](/ai/tdc/reference/tdc-install-configure-update.md)
