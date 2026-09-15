---
title: Work with TiDB Cloud Filesystem Data
summary: Learn how to copy, read, organize, search, and inspect files and directories in TiDB Cloud Filesystem by using the CLI.
---

# Work with TiDB Cloud Filesystem Data

In TiDB Cloud CLI, you can use [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) to transfer data between local storage and TiDB Cloud Filesystem and to manage its remote namespace.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- [Create a Filesystem](/ai/ti/guides/manage-filesystem-resources.md) or obtain access to an existing one.
- Select the Filesystem by passing `--file-system-id`, setting `TI_FS_FILE_SYSTEM_ID`, or supplying an FS token that identifies it. Provide an FS token with the permissions required for each operation.

## Copy data

Upload a local file to a remote path:

```shell
ti fs copy-file --from-local ./report.md --to-remote /reports/report.md
```

[`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) also supports downloads, streaming, appending, resuming, and recursive copies.

## Read and inspect data

Read a file or byte range to standard output:

```shell
ti fs read-file --path /reports/report.md --offset 0 --length 1024
```

List a directory and inspect one path:

```shell
ti fs list-files --path /reports --output text
ti fs describe-file --path /reports/report.md
```

## Organize the namespace

Create a directory, move a file, and remove data with the corresponding commands:

```shell
ti fs create-directory --path /reports/archive
ti fs move-file --from-remote /draft.md --to-remote /reports/final.md
ti fs delete-file --path /scratch --recursive
```

You can also use `chmod-file`, `create-symlink`, and `create-hardlink` to manage POSIX-style metadata and links.

> **Warning:**
>
> `delete-file --recursive` permanently deletes the target directory and its contents. Verify the remote path before you run the command.

## Search for data

Search file content below a path:

```shell
ti fs search-file-content --path /reports --pattern "TODO"
```

Find paths by name, type, tags, size, or timestamps:

```shell
ti fs find-files --path /reports --file-name-pattern "*.md" --tag stage=review
```

## What's next

- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md)
- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
