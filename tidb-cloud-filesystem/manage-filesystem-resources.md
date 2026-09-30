---
title: Manage File Systems in TiDB Cloud Filesystem
summary: Learn how to create, inspect, check, select, and delete file systems in TiDB Cloud Filesystem by using TiDB Cloud CLI.
aliases: ['/ai/manage-filesystem-resources']
---

# Manage File Systems in TiDB Cloud Filesystem

You can use [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) to create, inspect, check, select, and delete file systems in TiDB Cloud Filesystem.

For command syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).

## Prerequisites

Before you begin, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md) to install TiDB Cloud CLI (`ti`) and configure the access.

## Create a file system

Create a file system and wait until it is ready:

```shell
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait
```

From the output, you can get the file system ID in the `file_system_id` field and the file system owner token in the `fs_token` field. The CLI automatically stores the file system owner token locally.

Copy the returned `file_system_id` and select the file system for subsequent commands in the current shell:

```shell
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

Setting `TI_FS_FILE_SYSTEM_ID` lets subsequent commands identify the target file system without requiring `--file-system-id` on every command. For data-access commands, the CLI uses the locally stored file system token for the selected file system.

> **Warning:**
>
> The file system owner token plaintext in `fs_token` is returned only when the token is issued. Treat it as a secret and do not expose it in logs, issues, or source control. If you need to use the token on another machine or store a backup, save it securely in a secret manager. For more information, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

> **Note:**
>
> Do not put credentials, connection strings, private paths, or personal data in file system labels.

## List and inspect file systems

List the file systems available in the current region:

```shell
ti fs list-file-systems --output text
```

View metadata for a file system:

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

If you work with more than one file system, specify the target file system in one of the following ways:

- Pass `--file-system-id "<file-system-id>"` to an individual command.
- Set `TI_FS_FILE_SYSTEM_ID` to select a file system for subsequent commands in the current shell.

The CLI does not automatically select a file system based on the number of file systems or locally stored credentials.

The current CLI does not provide a command to change a file system's display name or labels after creation. Choose these values when you create the file system.

## Check access

Check whether the CLI can access a file system:

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

The result includes an overall `status` and checks local credentials, endpoint selection, the bundled file system runtime, and remote connectivity.

- `passed` means all checks succeeded.
- `warning` or `failed` identifies a check that needs attention.

For common access and connectivity issues, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## Delete a file system

> **Warning:**
>
> Deleting a file system permanently removes its remote data. Before deletion, stop applications that are using the file system and successfully unmount any active local mounts. For information about finishing pending writes safely, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

Delete a file system by its ID:

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

File system deletion is asynchronous. After the service accepts the request, the CLI reports the file system status as `deleting` and removes the matching locally stored credential. This status means that deletion has started, not that the remote file system and its data have already been removed.

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to generate, delegate, rotate, or revoke file system access.
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) to copy, read, organize, and search file system data.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access remote files through a local directory.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for command syntax, flags, and output fields.
