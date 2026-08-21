---
title: ti configure
summary: Configure a local TiDB Cloud CLI profile interactively or non-interactively.
---

# ti configure

Configures a local TiDB Cloud CLI profile. Without flags, this is the only interactive TiDB Cloud CLI command.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti configure
  [--help]
  [--non-interactive]
  [--region-code <string>]
  [--tidb-cloud-private-key <string>]
  [--tidb-cloud-public-key <string>]
  [--version]
```

## Options

- `--help`: Display help information.
- `--non-interactive`: Use this option to avoid being prompted for configuration values. You must provide at least three configuration values (`--tidb-cloud-public-key`, `--tidb-cloud-private-key`, and `--region-code`) when using this option. This is useful when running `ti` in a script or automated environment.
- `--region-code <string>`: Default region code, for example `aws-us-east-1` or `aws-ap-southeast-1`.
- `--tidb-cloud-private-key <string>`: TiDB Cloud API private key.
- `--tidb-cloud-public-key <string>`: TiDB Cloud API public key.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Configure `ti` interactively:

    ```bash
    # Enter the default region code and TiDB Cloud API keys when prompted.
    ti configure
    ```

- Configure `ti` for automation:

    ```bash
    # Supply all required values without interactive prompts.
    TI_REGION_CODE="aws-us-east-1" \
    TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
    TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
    ti configure --profile ci --non-interactive
    ```

## Related documentation

- [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
