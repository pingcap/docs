---
title: tdc fs-git clone-git-workspace
summary: Clone a Git repository into a mounted TiDB Cloud Filesystem.
---

# tdc fs-git clone-git-workspace

Clones a repository into a mounted Filesystem path. Hydration can run synchronously or in the background.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
  tdc fs-git clone-git-workspace
    --repo-url <string>
    --target-path <string>
    [--blobless]
    [--dry-run]
    [--file-system-name <string>]
    [--fs-token <string>]
    [--help]
    [--hydrate <string>]
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
tdc fs-git clone-git-workspace --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb
tdc fs-git clone-git-workspace --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate background
```
