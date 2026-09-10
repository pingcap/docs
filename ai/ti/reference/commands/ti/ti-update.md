---
title: ti update
summary: Check for or install a TiDB Cloud CLI release update.
---

# ti update

Checks for or installs a TiDB Cloud CLI release update. This command does not read or modify settings, profiles, credentials, operation logs, or other state under `~/.ti/`.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti update
  [--check]
  [--dry-run]
  [--fail-if-update-available]
  [--help]
  [--target-version <string>]
  [--version]
```

## Options

- `--check`: Check whether a newer `ti` release is available without updating.
- `--dry-run`: Show the update plan without changing the local binary.
- `--fail-if-update-available`: With `--check`, exit with code 1 when an update is available.
- `--help`: Display help information.
- `--target-version <string>`: Target `ti` version, such as `latest` or `vX.Y.Z`. \[default: latest]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Check whether an update is available:

    ```bash
    # Compare the installed version with the latest GitHub release without changing files.
    ti update --check
    ```

- Preview an update:

    ```bash
    # Show the files and versions that an update would change.
    ti update --dry-run
    ```

- Install a specific release:

    ```bash
    # Replace an eligible installation with the requested release version.
    ti update --target-version <version>
    ```

## Related documentation

- [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
