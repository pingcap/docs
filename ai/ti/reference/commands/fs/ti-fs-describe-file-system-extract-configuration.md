---
title: ti fs describe-file-system-extract-configuration
summary: Describe media extraction configuration for a TiDB Cloud Filesystem.
---

# ti fs describe-file-system-extract-configuration

Describes the effective image, audio, or video extraction configuration for one Filesystem. This optional configuration does not affect normal Filesystem operations when it is not customized. The command requires TiDB Cloud API credentials and does not use an FS token.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs describe-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--help]
  [--version]
```

## Options

- `--file-system-id <string>`: Set the immutable Filesystem ID. \[required]
- `--media-type <string>`: Select `image`, `audio`, or `video`. \[required]
- `--help`: Display help information.
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Inspect image extraction:

    ```bash
    # Show whether image extraction uses a custom, default, or absent provider configuration.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image
    ```

- Print only the effective provider source:

    ```bash
    # Return custom, default, or none for use in a script.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --query source \
      --output text
    ```

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
