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
```

## Options

- `--repo-url <string>`: Git repository URL. \[required]
- `--target-path <string>`: The mounted file system path to clone into. \[required]
- `--blobless`: Create a blobless partial local `.git` and hydrate clean blobs separately.
- `--dry-run`: Validate the request without applying changes.
- `--file-system-name <string>`: Select the file system. You can also set `TDC_FS_FILE_SYSTEM_NAME`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TDC_FS_TOKEN`.
- `--help`: Display help information.
- `--hydrate <string>`: Blobless hydrate mode: `auto`, `background`, `sync`, or `off`. \[default: auto]
- `--version`: Display tdc version information.

For options shared by all commands, see [Global options](/ai/tdc/reference/tdc-cli-reference.md#global-options).

## Examples

### Clone a repository

```bash
tdc fs-git clone-git-workspace --file-system-name workspace --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb
```

### Clone a blobless repository and hydrate in the background

```bash
tdc fs-git clone-git-workspace --file-system-name workspace --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate background
```
