---
title: Get Started with TiDB Cloud Filesystem via Console
summary: Create a file system in the TiDB Cloud console, connect to it from your computer, write a test file, and view the file in the console.
---

# Get Started with TiDB Cloud Filesystem via Console

Create a file system in the [TiDB Cloud console](https://tidbcloud.com/), mount it on a macOS or Linux computer, write a test file, and view its metadata in the console.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Step 1. Create a file system

1. If you do not have a TiDB Cloud account, [sign up for one](https://tidbcloud.com/free-trial).
2. Log in to the [TiDB Cloud console](https://tidbcloud.com/) with your TiDB Cloud account.
3. In the left navigation pane, select your organization and click **File Systems**.
4. In the upper-right corner, click **Create File System**.
5. On the **Create File System** page, enter a file system name, and select a cloud provider and region. Review the usage limits in the summary.

    > **Tip:**
    >
    > For organizations without a credit card, the file system limits are fixed. To edit the usage limit, add a credit card to your organization. For more information, see [Manage TiDB Cloud Filesystem Usage Limit](/tidb-cloud-filesystem/manage-filesystem-limits.md).

6. Click **Create**. When the **Your File System is Ready!** dialog appears, keep the dialog open for the next step.

## Step 2. Mount the file system

On macOS or Linux, follow the steps in the **Your File System is Ready!** dialog to install TiDB Cloud CLI and mount the file system. On Windows, follow [Quick Start via CLI](/tidb-cloud-filesystem/filesystem-quick-start.md) to work with files without a mount.

1. Install the TiDB Cloud CLI `ti`.

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh
    ```

2. Copy and run the command under **Mount Your File System** in the same shell. The command adds `ti` to `PATH`, sets `TI_FS_TOKEN`, creates `~/tidbcloudfs`, and mounts the file system there.

    > **Note:**
    >
    > - The mount command includes the [default owner token](/tidb-cloud-filesystem/filesystem-authorization.md#owner-tokens) in `TI_FS_TOKEN`. This token grants full access to the file system and is displayed only once. Save it securely. Do not put the command or token in logs, issues, chat messages, or source control.
    > - On Linux, mounting requires `fuse3` and access to `/dev/fuse`. If needed, follow [Install FUSE userspace tools](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools) before running the mount command.

3. Copy and run the command under **Start Using It** to list the mounted directory.
4. Click **Done** to open the file system overview.

You can click **Connect** on the overview page to reopen the connection guidance, but you cannot retrieve the default owner token later.

## Step 3. Write and view a file

After mounting the file system, use the mounted directory to write and read a test file.

Write a file in the mounted directory:

```bash
echo 'Hello from TiDB Cloud Filesystem' > ~/tidbcloudfs/hello.txt
cat ~/tidbcloudfs/hello.txt
```

In the left navigation pane of the file system, click **Files**. The root directory lists `hello.txt`. You can search for the file or click its name to view its metadata. The console displays file information, but reading file contents and changing files require the TiDB Cloud CLI `ti` or a mount.

## (Optional) Step 4. Unmount the file system

If you do not need to access the file system from the mounted directory, you can unmount it:

```bash
ti fs unmount-file-system --mount-path ~/tidbcloudfs
```

On Linux, FUSE can buffer writes locally until a successful unmount. If unmounting fails, follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) before leaving the machine or removing its local cache.

## What's next

- [Manage File Systems](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect, rename, or delete a file system.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create tokens with limited access.
- [Quick Start via CLI](/tidb-cloud-filesystem/filesystem-quick-start.md) for a CLI-only creation workflow.
