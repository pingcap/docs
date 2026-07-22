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
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

For global flags such as `--profile`, `--region`, `--output`, and `--query`, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc update --check
tdc update --target-version v0.1.4
```
