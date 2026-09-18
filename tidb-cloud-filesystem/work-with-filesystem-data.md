---
title: Work with Files and Directories in TiDB Cloud Filesystem
summary: Learn how to copy, read, organize, search, and inspect files and directories in TiDB Cloud Filesystem by using the CLI.
aliases: ['/ai/work-with-filesystem-data']
---

# Work with Files and Directories in TiDB Cloud Filesystem

In TiDB Cloud CLI, you can use [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) to transfer data between local storage and TiDB Cloud Filesystem and to manage its remote namespace.

## Prerequisites

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- [Create a Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) or obtain access to an existing one.
- Select the Filesystem and make its token available to `ti`. For available access options, see [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

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

You can also use [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md), [`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md), and [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md) to manage POSIX-style metadata and links.

> **Warning:**
>
> `delete-file --recursive` permanently deletes the target directory and its contents. Verify the remote path before you run the command.

## Search for data

Search file content below a path:

```shell
ti fs search-file-content --path /reports --pattern "TODO"
```

`--pattern` is a text query, not a regular expression or glob. Use `--limit` to cap the number of results; `0` uses the service default. See the [`search-file-content` reference](/ai/ti/reference/ti-fs-search-file-content.md).

Find paths by name, type, tags, size, or timestamps:

```shell
ti fs find-files --path /reports --file-name-pattern "*.md" --tag stage=review
```

`find-files` searches beneath the specified path and can filter by file name, type, tags, size, or modification time. See its [options and result limit](/ai/ti/reference/ti-fs-find-files.md).

For supported regions and current Filesystem and platform limitations, see [Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md).

## What's next

- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md)
- [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
