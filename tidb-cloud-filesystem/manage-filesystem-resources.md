---
title: Manage TiDB Cloud Filesystems
summary: Learn how to create, inspect, check, select, and delete TiDB Cloud Filesystems by using TiDB Cloud CLI.
aliases: ['/ai/manage-filesystem-resources']
---

# Manage TiDB Cloud Filesystems

You can use [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) to create, inspect, check, select, and delete TiDB Cloud Filesystems.

For command syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).

## Prerequisites

Before you begin, follow [Get Started with TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-quick-start.md) to install TiDB Cloud CLI (`ti`) and configure the access.

## Create a Filesystem

Create a Filesystem and wait until it is ready:

```shell
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait
```

From the output, you can get the Filesystem ID in the `file_system_id` field and the Filesystem owner token in the `fs_token` field. The CLI automatically stores the Filesystem owner token locally.

Copy the returned `file_system_id` and select the Filesystem for subsequent commands in the current shell:

```shell
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

Setting `TI_FS_FILE_SYSTEM_ID` lets subsequent commands identify the target Filesystem without requiring `--file-system-id` on every command. For data-access commands, the CLI uses the locally stored Filesystem token for the selected Filesystem.

> **Warning:**
>
> The Filesystem owner token plaintext in `fs_token` is returned only when the token is issued. Treat it as a secret and do not expose it in logs, issues, or source control. If you need to use the token on another machine or store a backup, save it securely in a secret manager. For more information, see [Manage Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

> **Note:**
>
> Do not put credentials, connection strings, private paths, or personal data in Filesystem labels.

## List and inspect Filesystems

List the Filesystems available in the current region:

```shell
ti fs list-file-systems --output text
```

View metadata for a Filesystem:

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

If you work with more than one Filesystem, specify the target Filesystem in one of the following ways:

- Pass `--file-system-id "<file-system-id>"` to an individual command.
- Set `TI_FS_FILE_SYSTEM_ID` to select a Filesystem for subsequent commands in the current shell.

The CLI does not automatically select a Filesystem based on the number of Filesystems or locally stored credentials.

The current CLI does not provide a command to change a Filesystem's display name or labels after creation. Choose these values when you create the Filesystem.

## Check access

Check whether the CLI can access a Filesystem:

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

The result includes an overall `status` and checks local credentials, endpoint selection, the bundled Filesystem runtime, and remote connectivity.

- `passed` means all checks succeeded.
- `warning` or `failed` identifies a check that needs attention.

For common access and connectivity issues, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md).

## Delete a Filesystem

> **Warning:**
>
> Deleting a Filesystem permanently removes its remote data. Before deletion, stop applications that are using the Filesystem and successfully unmount any active local mounts. For information about finishing pending writes safely, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

Delete a Filesystem by its ID:

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Filesystem deletion is asynchronous. After the service accepts the request, the CLI reports the Filesystem status as `deleting` and removes the matching locally stored credential. This status means that deletion has started, not that the remote Filesystem and its data have already been removed.

## What's next

- [Manage Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to generate, delegate, rotate, or revoke Filesystem access.
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) to copy, read, organize, and search Filesystem data.
- [Mount a Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) to access remote files through a local directory.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for command syntax, flags, and output fields.
