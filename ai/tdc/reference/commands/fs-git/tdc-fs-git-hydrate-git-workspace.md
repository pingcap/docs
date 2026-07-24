---
title: tdc fs-git hydrate-git-workspace
summary: Hydrate clean Git objects in a tdc Git workspace.
---

# tdc fs-git hydrate-git-workspace

Hydrates clean Git objects for an existing tdc Git workspace.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-git hydrate-git-workspace
    --target-path <string>
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--timeout <duration>]
    [--version]
    [--debug]
    [--output <string>]
    [--profile <string>]
    [--query <string>]
    [--region <string>]
```

Filesystem selection can come from `--file-system-name`, `TDC_FS_FILE_SYSTEM_NAME`, or the selected profile. For shared global flags, see [tdc CLI Reference](/ai/tdc/reference/tdc-cli-reference.md).

## Examples

```shell
tdc fs-git hydrate-git-workspace --target-path /path/to/workspace/tidb
tdc fs-git hydrate-git-workspace --target-path /path/to/workspace/tidb --timeout 30m
```
