---
title: tdc update
summary: Check for or install a tdc release update.
---

# tdc update

Checks for or installs a tdc release update. This command does not read or modify profiles and credentials.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
tdc update
  [--check]
  [--dry-run]
  [--fail-if-update-available]
  [--help]
  [--target-version <string>]
  [--version]
```

## Options

- `--check`: Check whether a newer tdc release is available without updating.
- `--dry-run`: Show the update plan without changing the local binary.
- `--fail-if-update-available`: With `--check`, exit with code 1 when an update is available.
- `--help`: Display help information.
- `--target-version <string>`: Target tdc version, such as `latest` or `vX.Y.Z`. \[default: latest]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Check for an update

```bash
tdc update --check
```

### Install a specific version

```bash
tdc update --target-version <version>
```
