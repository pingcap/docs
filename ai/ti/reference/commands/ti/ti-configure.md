---
title: ti configure
summary: Configure a local TiDB Cloud CLI profile interactively or non-interactively.
---

# ti configure

Configures a local TiDB Cloud CLI profile. Without flags, this is the only interactive TiDB Cloud CLI command.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

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
- `--non-interactive`: Avoid prompts. Provide the region code, public key, and private key through the corresponding command options or environment variables. This is useful when running `ti` in a script or automated environment.
- `--region-code <string>`: Default region code, for example `aws-us-east-1` or `aws-ap-southeast-1`.
- `--tidb-cloud-private-key <string>`: TiDB Cloud API private key.
- `--tidb-cloud-public-key <string>`: TiDB Cloud API public key.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Configuration value sources

The following command options and environment variables provide the same configuration values:

| Configuration value | Command option | Environment variable |
| --- | --- | --- |
| Default region code | `--region-code` | `TI_REGION_CODE` |
| TiDB Cloud API public key | `--tidb-cloud-public-key` | `TIDB_CLOUD_PUBLIC_KEY` |
| TiDB Cloud API private key | `--tidb-cloud-private-key` | `TIDB_CLOUD_PRIVATE_KEY` |

For each value, an explicitly provided command option takes precedence over its environment variable. With `--non-interactive`, all three values must resolve from these sources.

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
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
