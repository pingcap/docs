---
title: Manage File Systems in TiDB Cloud Filesystem
summary: Learn how to create, inspect, and delete file systems by using the TiDB Cloud console or CLI, rename them in the console, and check access with CLI.
aliases: ['/ai/manage-filesystem-resources']
---

# Manage File Systems in TiDB Cloud Filesystem

You can use the [TiDB Cloud console](https://tidbcloud.com/) or [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) to create, inspect, and delete file systems in TiDB Cloud Filesystem. The console also lets you rename a file system; the CLI provides access diagnostics.

For command syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).

## Prerequisites

- To use the [TiDB Cloud console](https://tidbcloud.com/) to manage file systems, log in to the console and select your organization.
- To use the TiDB Cloud CLI (`ti`) to manage file systems, follow [Quick Start via CLI](/tidb-cloud-filesystem/filesystem-quick-start.md) to install `ti` and configure access.

## Create a file system

<SimpleTab>

<div label="Console">

1. In the left navigation pane of the [TiDB Cloud console](https://tidbcloud.com), select your organization and click **File Systems**.
2. In the upper-right corner, click **Create File System**.
3. On the **Create File System** page, enter a file system name, and select a **Cloud Provider** and **Region**.
4. (Optional) Review and edit the usage limits in the summary.

    To edit the usage limits, add a credit card to your organization. Without a credit card, the free limits cannot be edited during creation. For more information, see [Manage Usage Limit](/tidb-cloud-filesystem/manage-filesystem-limits.md).

5. Click **Create**. The **Your File System is Ready!** dialog offers optional steps to install TiDB Cloud CLI and mount the file system on macOS or Linux. The default owner token in the mount command is shown only once; save it securely before closing the dialog.

</div>

<div label="CLI">

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

</div>

</SimpleTab>

## List and inspect file systems

<SimpleTab>

<div label="Console">

1. In the left navigation pane of the [TiDB Cloud console](https://tidbcloud.com), select your organization and click **File Systems**.
2. On the [**File Systems**](https://tidbcloud.com/filesystems) page, select a cloud provider and region to list file systems in that location. Use **Search Name** or **Status** to narrow the list.

To view details of a file system, click the file system's name to go to its overview page.

To change its display name, click **...** in the upper-right corner of the overview page and select **Rename**.

</div>

<div label="CLI">

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

</div>

</SimpleTab>

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

<SimpleTab>

<div label="Console">

1. In the TiDB Cloud console, open your organization's [**File Systems**](https://tidbcloud.com/filesystems) page, then select the **Cloud Provider** and **Region** for the target file system.
2. In the row of the target file system, click **...**, and then select **Delete**.
3. In the confirmation dialog, enter the requested region and file system name in the form `region/name`, then click **I understand, delete it.**

Deletion is asynchronous. After the request is submitted, the file system might remain visible with the status `deleting` until deletion finishes.

</div>

<div label="CLI">

Delete a file system by its ID:

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

File system deletion is asynchronous. After the service accepts the request, the CLI reports the file system status as `deleting` and removes the matching locally stored credential. This status means that deletion has started, not that the remote file system and its data have already been removed.

</div>

</SimpleTab>

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to generate, delegate, rotate, or revoke file system access.
- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md) to copy, read, organize, and search file system data.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access remote files through a local directory.
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md) for command syntax, flags, and output fields.
