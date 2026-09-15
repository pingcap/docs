---
title: ti fs describe-file-system-embedding-configuration
summary: Describe embedding configuration for a TiDB Cloud Filesystem.
---

# ti fs describe-file-system-embedding-configuration

Shows the embedding configuration for a Filesystem. This configuration is optional and does not affect normal Filesystem operations when it is not customized. This command requires TiDB Cloud API credentials and does not use a Filesystem token.

The `source` field reports whether the configuration is `custom`, `default`, `none`, or `database_auto`.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Syntax

```text
ti fs describe-file-system-embedding-configuration
  --file-system-id <string>
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable Filesystem ID. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Inspect effective embedding configuration:

    ```bash
    # Show provider metadata, masked credentials, source, and generation.
    ti fs describe-file-system-embedding-configuration \
      --file-system-id <file-system-id>
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
