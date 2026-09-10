---
title: ti fs-git clone-git-workspace
summary: Clone a Git repository into a mounted TiDB Cloud Filesystem.
---

# ti fs-git clone-git-workspace

Clones a repository into a mounted Filesystem path. Hydration can run synchronously or in the background.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Syntax

```text
ti fs-git clone-git-workspace
  --repo-url <string>
  --target-path <string>
  [--blobless]
  [--dry-run]
  [--file-system-id <string>]
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
- `--file-system-id <string>`: Select the file system. You can also set `TI_FS_FILE_SYSTEM_ID`.
- `--fs-token <string>`: Set the file system user token. If omitted, uses `TI_FS_TOKEN`.
- `--help`: Display help information.
- `--hydrate <string>`: Blobless hydrate mode: `auto`, `background`, `sync`, or `off`. \[default: auto]
- `--version`: Display version information.

For options shared by all commands, see [Global options](/ai/ti/reference/ti-cli-reference.md#global-options).

## Examples

- Clone a repository normally:

    ```bash
    # Create a complete Git checkout in the mounted Filesystem path.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb
    ```

- Start a blobless workspace immediately:

    ```bash
    # Expose the repository tree while clean Git objects hydrate in the background.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate background
    ```

- Wait for blobless hydration:

    ```bash
    # Keep the clone command running until clean Git objects finish hydrating.
    ti fs-git clone-git-workspace --file-system-id <file-system-id> --repo-url https://github.com/pingcap/tidb.git --target-path /path/to/workspace/tidb --blobless --hydrate sync
    ```

## Related documentation

- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)
