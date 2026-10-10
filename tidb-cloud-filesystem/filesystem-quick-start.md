---
title: Get Started with TiDB Cloud Filesystem via CLI
summary: Learn how to create a persistent TiDB Cloud file system, read and write files, and optionally access them through a local mount.
---

# Get Started with TiDB Cloud Filesystem via CLI

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) is a persistent, shared cloud file system for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so you can reuse a workspace across sessions and environments.

This quick start guide walks you through how to create a file system, write and read files, and optionally mount it as a local directory.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/). The keys must grant `Organization Owner` access to your organization.

If someone has already provided you with a file system token, skip resource creation and follow [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

Use Bash or Zsh on macOS and Linux, or PowerShell on Windows. Keep the same shell open throughout the tutorial. If an agent starts a new shell for each command, pass the environment variables and saved path values to each shell.

## Step 1. Install TiDB Cloud CLI

Choose your operating system:

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. Install TiDB Cloud CLI:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. Add `ti` to your shell and check the version:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    ti --version
    ```

3. To keep `ti` available in new terminals, add it to your shell profile. For Zsh:

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    ```

    For Bash, add the same `export` line to the startup file your terminal uses, commonly `~/.bashrc` on Linux or `~/.bash_profile` on macOS.

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. Install TiDB Cloud CLI:

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. Add `ti` to your PowerShell session and check the version:

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"

    ti --version
    ```

</div>

</SimpleTab>

For permanent `PATH` setup on Windows and other installation options, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 2. Configure TiDB Cloud CLI

Choose a [supported region](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions) where you want to store your files, such as `aws-us-west-2`. The free tier allows one file system per region. If your organization already has one, [reuse it](/tidb-cloud-filesystem/access-filesystem.md), choose another region, or [add a payment method](https://tidbcloud.com/org-settings/billing/payments).

1. Run the interactive configuration:

    ```bash
    ti configure
    ```

2. Provide the following information:

    - The region you selected.
    - Your TiDB Cloud API public key and private key.

The CLI saves your credentials and default region locally. The creation command in the next step uses this region.

> **Tip:**
>
> For CI or agents, use non-interactive configuration instead. Inject `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY` from a secret manager, set `TI_REGION_CODE`, and run `ti configure --non-interactive`. For more information, see [Configure for automation](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation).

## Step 3. Create and use a file system

1. Create a file system:

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait
    ```

    Copy the returned `file_system_id` for the next step. The CLI stores the owner token and region for the file system locally, so you do not need to enter the token again on the same machine.

    > **Note:**
    >
    > If you need to access the file system from another machine, also save the returned `fs_token` and `region_code`. The owner token grants full access and does not expire, so store it securely. For limited access, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

2. Select your new file system. Replace `<file-system-id>` with the returned `file_system_id`:

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    $env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
    ```

    </div>

    </SimpleTab>

3. Create a directory, upload a sample file, and read it back:

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    ti fs create-directory --path /quick-start
    printf 'Hello from TiDB Cloud Filesystem\n' | ti fs copy-file \
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    ti fs create-directory --path /quick-start
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --from-stdin --to-remote /quick-start/hello.txt
    ti fs read-file --path /quick-start/hello.txt
    ```

    </div>

    </SimpleTab>

    Expected output from `read-file`:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    Your first file is now stored in TiDB Cloud Filesystem. To access it from another environment, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md). To provide access to another user, application, or agent, see [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md).

## Step 4. Mount the file system (optional)

Mount the file system if your application needs local file paths. Mounting is not supported on Windows. If you are using Windows or only need CLI access, skip to [Step 5](#step-5-clean-up-the-example-optional).

1. Create an empty local directory for the mount:

    ```bash
    mount_dir="$(mktemp -d "$HOME/ti-fs-quick-start.XXXXXX")"
    ```

2. Mount the `/quick-start` directory using the command for your operating system:

    <SimpleTab>

    <div label="macOS WebDAV">

    This command uses macOS's built-in WebDAV support:

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver webdav
    ```

    </div>

    <div label="Linux FUSE">

    Linux requires the `fuse3` package and access to `/dev/fuse`. If needed, follow [Install FUSE userspace tools](/tidb-cloud-filesystem/filesystem-mount-linux.md#install-fuse-userspace-tools) before running the mount command.

    ```bash
    ti fs mount-file-system --remote-path /quick-start \
      --mount-path "$mount_dir" --driver fuse
    ```

    </div>

    </SimpleTab>

3. Read your file using its local path:

    ```bash
    cat "$mount_dir/hello.txt"
    ```

    Expected output:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

For write verification and troubleshooting, see [Verify a mount before using it](/tidb-cloud-filesystem/filesystem-mount.md#verify-a-mount-before-using-it).

## Step 5. Clean up the example (optional)

If you mounted the directory in Step 4, close applications using it, then unmount and remove the empty local mount directory:

```bash
ti fs unmount-file-system --mount-path "$mount_dir"
rmdir "$mount_dir"
```

If unmount fails, follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) before continuing.

Delete the example directory and its files. This command works on all supported operating systems:

```shell
ti fs delete-file --path /quick-start --recursive
```

The file system and its token remain available for reuse. To remove the entire file system, see [Delete a file system](/tidb-cloud-filesystem/manage-filesystem-resources.md#delete-a-file-system).

## What's next

- [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md) to reuse locally stored credentials or connect from another environment.
- [Configure for automation](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation) to set up CLI credentials for CI jobs or agents.
- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, inspect, and manage tokens for file system access.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
