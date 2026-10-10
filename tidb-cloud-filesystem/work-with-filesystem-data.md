---
title: Work with Files and Directories in TiDB Cloud Filesystem
summary: Learn how to view file metadata in the console and upload, download, read, organize, and search files with TiDB Cloud CLI.
aliases: ['/ai/work-with-filesystem-data']
---

# Work with Files and Directories in TiDB Cloud Filesystem

In TiDB Cloud Filesystem, you can browse file and directory metadata in the TiDB Cloud console or use TiDB Cloud CLI (`ti`) to upload, download, read, organize, and search files without mounting the file system. For all commands and options, see the [`ti fs` reference](/ai/ti/reference/ti-filesystem.md).

If you [mount the file system](/tidb-cloud-filesystem/filesystem-mount.md) to your machine, you can work with files and directories as you do with a local file system.

## Prerequisites

The following prerequisites apply to CLI operations. If you only need to browse file metadata in the TiDB Cloud console, see [View files](#view-files-via-the-console).

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- [Create a file system](/tidb-cloud-filesystem/manage-filesystem-resources.md) or obtain access to an existing one.
- Select the file system and make its token available to `ti`. For available access options, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

## View files

<SimpleTab>

<div label="Console">

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**File Systems**](https://tidbcloud.com/filesystems) page for your organization, select the cloud provider and region, and then click the name of your target file system.
2. In the left navigation pane, click **Files**. The page lists directories and files with their type, size, and modification time.
3. Expand a directory to browse its contents, use **Search** to filter the visible file tree, or click a file name to view its metadata.

The console displays file metadata. To read file contents or change files and directories, use the CLI commands or [mount the file system](/tidb-cloud-filesystem/filesystem-mount.md).

</div>

<div label="CLI">

List the contents of a directory:

```shell
ti fs list-files --path /reports --output text
```

Example output:

```text
NAME       TYPE  SIZE  MTIME
archive    dir   0     0
report.md  file  23    0
```

Inspect metadata for a file or directory:

```shell
ti fs describe-file --path /reports/report.md
```

</div>

</SimpleTab>

## Upload and download files

Upload a local file to the file system:

```shell
ti fs copy-file \
  --from-local ./report.md \
  --to-remote /reports/report.md
```

Download a file from the file system:

```shell
ti fs copy-file \
  --from-remote /reports/report.md \
  --to-local ./downloads/report.md \
  --create-parents
```

You can also use `copy-file` to copy files or directories within the file system, stream data through standard input or output, append to a file, or resume an interrupted transfer.

To copy a directory recursively, use `--recursive`. For all supported copy operations and options, see the [`copy-file` reference](/ai/ti/reference/ti-fs-copy-file.md).

## Read files

Read the complete contents of a file:

```shell
ti fs read-file --path /reports/report.md
```

The command writes file contents directly to standard output; it does not wrap them in JSON.

To read only part of a file, use `--offset` and `--length`. For example, the following command reads the first 1024 bytes:

```shell
ti fs read-file \
  --path /reports/report.md \
  --offset 0 \
  --length 1024
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

Use `search-file-content` to find files by their content:

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

Tags are set when you upload a file, with `copy-file --tag key=value`. Supplying `--tag` on a later upload of the same path replaces the previous tags instead of adding to them.

The result lists matching paths. An empty table means that nothing matched, not that the command failed.

For all available filters, see the [`find-files` reference](/ai/ti/reference/ti-fs-find-files.md).

## Use command output in scripts

Check the exit status before using command output. `read-file` and `copy-file --to-stdout` stream file contents, not CLI metadata. Keep stderr separate when capturing those contents.

In `ti` v0.2.6 and v0.2.7, `create-directory` can print a `created ...` line before its JSON result, even with `--output json`. Its output cannot be parsed as a single JSON document. Check the exit status, then verify the directory with `describe-file` or `list-files`. Check your installed version's output format before relying on it in scripts.

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to work with file system data through a local directory and existing local tools.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to make and review isolated changes before applying them to the base file system.
- [Share a File System Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md) to give another machine or environment access to the file system.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for complete command syntax and options.
