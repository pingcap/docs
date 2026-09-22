---
title: Work with Files and Directories in TiDB Cloud Filesystem
summary: Learn how to upload, download, read, organize, inspect, and search files and directories in TiDB Cloud Filesystem.
aliases: ['/ai/work-with-filesystem-data']
---

# Work with Files and Directories in TiDB Cloud Filesystem

You can work with files and directories in a TiDB Cloud Filesystem directly from TiDB Cloud CLI (`ti`) without mounting the Filesystem.

Use `ti fs` commands to upload and download files, read file contents, list and inspect paths, organize files and directories, and search for data. For the complete command reference, see [`ti fs` reference](/ai/ti/reference/ti-filesystem.md).

> **Tip:**
>
> If you want to work with files and directories in TiDB Cloud Filesystem through local file paths, see [mount the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md).

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- [Create a Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) or obtain access to an existing one.
- Select the Filesystem and make its token available to `ti`. For available access options, see [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

## Upload and download files

Upload a local file to the Filesystem:

```shell
ti fs copy-file \
  --from-local ./report.md \
  --to-remote /reports/report.md
```

Download a file from the Filesystem:

```shell
ti fs copy-file \
  --from-remote /reports/report.md \
  --to-local ./downloads/report.md \
  --create-parents
```

You can also use `copy-file` to copy files or directories within the Filesystem, stream data through standard input or output, append to a file, or resume an interrupted transfer.

To copy a directory recursively, use `--recursive`. For all supported copy operations and options, see the [`copy-file` reference](/ai/ti/reference/ti-fs-copy-file.md).

## Read and inspect files and directories

Read the complete contents of a file:

```shell
ti fs read-file --path /reports/report.md
```

To read only part of a file, use `--offset` and `--length`. For example, the following command reads the first 1024 bytes:

```shell
ti fs read-file \
  --path /reports/report.md \
  --offset 0 \
  --length 1024
```

List the contents of a directory:

```shell
ti fs list-files --path /reports --output text
```

Inspect metadata for a file or directory:

```shell
ti fs describe-file --path /reports/report.md
```

## Organize files and directories

Create a directory:

```shell
ti fs create-directory --path /reports/archive
```

Move a file to another path:

```shell
ti fs move-file \
  --from-remote /draft.md \
  --to-remote /reports/final.md
```

Delete a file or directory:

```shell
ti fs delete-file --path /scratch --recursive
```

> **Warning:**
>
> `delete-file --recursive` permanently deletes the specified directory and its contents. Verify the path before deleting it. You can use `--dry-run` to validate the request without deleting data.

For workflows that need POSIX-style metadata or links, you can also use [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md), [`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md), and [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md).

## Search files and content

Use `search-file-content` when you want to find files based on their content:

```shell
ti fs search-file-content \
  --path /reports \
  --pattern "TODO"
```

`--pattern` is a text query, not a regular expression or glob. Use `--limit` to control the maximum number of results.

For details, see the [`search-file-content` reference](/ai/ti/reference/ti-fs-search-file-content.md).

If you know something about the file itself rather than its contents, use `find-files`. You can filter by file name, type, tags, size, or modification time.

For example, find Markdown files tagged `stage=review`:

```shell
ti fs find-files \
  --path /reports \
  --file-name-pattern "*.md" \
  --tag stage=review
```

For all available filters, see the [`find-files` reference](/ai/ti/reference/ti-fs-find-files.md).

## What's next

- [Mount a TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) to work with Filesystem data through a local directory and existing local tools.
- [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to make and review isolated changes before applying them to the base Filesystem.
- [Share a TiDB Cloud Filesystem Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another machine or environment access to the Filesystem.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for complete command syntax and options.
