---
title: Work with TiDB Cloud Filesystem Data
summary: Learn how to copy, read, organize, search, and inspect files and directories in TiDB Cloud Filesystem by using the CLI.
---

# Work with TiDB Cloud Filesystem Data

Use `ti fs` commands to transfer data between local storage and TiDB Cloud Filesystem and to manage its remote namespace.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Obtain access to a Filesystem and select it by ID when necessary.

## Copy data

Upload a local file to a remote path:

```shell
ti fs copy-file --from-local ./report.md --to-remote /reports/report.md
```

[`copy-file`](/ai/ti/reference/commands/fs/ti-fs-copy-file.md) also supports downloads, streaming, appending, resuming, and recursive copies.

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
ti fs create-directory --path /reports/archive --mode 0755
ti fs move-file --from-remote /draft.md --to-remote /reports/final.md
ti fs delete-file --path /scratch --recursive
```

You can also use `chmod-file`, `create-symlink`, and `create-hardlink` to manage POSIX-style metadata and links.

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

- [Manage Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md)
- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
