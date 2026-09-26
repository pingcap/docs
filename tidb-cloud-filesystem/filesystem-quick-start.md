---
title: Get Started with TiDB Cloud Filesystem
summary: Create a file system, write and read a persistent file, and keep the workspace available across sessions.
---

# Get Started with TiDB Cloud Filesystem

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) is a persistent, shared cloud file system for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so you can reuse the same workspace across sessions and environments.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/). The keys must have the `Organization Owner` access to your organization.

If someone has already provided you with a file system token, skip resource creation and follow [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

## Step 1. Install TiDB Cloud CLI

Depending on your operating system, take the following steps to install TiDB Cloud CLI.

<SimpleTab>

<div label="macOS or Linux">

1. On macOS or Linux, run the following command to install TiDB Cloud CLI:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. Add `ti` to the current shell and verify it:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"

    ti --version
    ```

3. Add `export PATH="$HOME/.ti/bin:$PATH"` to your shell profile to keep `ti` available in new terminals.

    For example, if you use `zsh`, run the following command:

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

</div>

<div label="Windows PowerShell">

1. On Windows PowerShell, run the following command to install TiDB Cloud CLI:

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. Add `ti` to the current PowerShell session and verify it:

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"

    ti --version
    ```

3. Add `$HOME\.ti\bin` to your user `PATH` to keep `ti` available in new PowerShell sessions:

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    [Environment]::SetEnvironmentVariable("Path", "$tiBin;$([Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
    ```

</div>

</SimpleTab>

## Step 2. Configure TiDB Cloud CLI

1. Run the interactive configuration:

    ```bash
    ti configure
    ```

2. Provide the following information:

    - A default region for CLI operations, specified as a region code such as `aws-us-west-2`. Choose a region where you want to store the file system data. For the regions supported by TiDB Cloud Filesystem, see [Supported regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions).

        The free tier allows one file system for each region. If your organization already has a file system in the region you choose, select a different supported region, add a payment method in the [TiDB Cloud console](https://tidbcloud.com/org-settings/billing/payments), or reuse the existing file system.

    - Your TiDB Cloud API public key and private key.

The CLI saves the configuration locally and returns `"credentials_stored": true`. This confirms that the keys were saved on this machine, not that they are valid. The file system creation command in the next step makes the first request that requires authentication and fails if the key pair is invalid.

To learn more about installing, configuring, and updating TiDB Cloud CLI, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 3. Create and use a file system

1. Create a file system:

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait --region aws-us-west-2
    ```

    The command returns information about the new file system. Save the following values for later use:

    - `file_system_id`: uniquely identifies the file system.
    - `fs_token`: the owner token for the file system.

    > **Note:**
    >
    > - The owner token grants full access to the file system and is returned only when it is issued. It does not expire, so revoke it when it is no longer needed. Treat it as a secret and keep it out of logs, issues, chat messages, and source control.
    >
    > - For least-privilege access, you can generate a scoped token to restrict access to specific paths and operations. For more information, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

2. Depending on your operating system, use one of the following methods to access and work with the file system.

    The environment where you access the file system can be the same machine where you created it, another machine, or an AI agent sandbox.

    <SimpleTab>

    <div label="macOS or Linux">

    On macOS or Linux, you can either mount the file system as a local directory or use `ti fs` commands to work with its files directly.

    **Option 1: Mount the file system (recommended)**

    Set the owner token returned in the previous step as the `TI_FS_TOKEN` environment variable:

    ```bash
    export TI_FS_TOKEN="<owner-token>"
    ```

    Create a local directory and mount the file system to it:

    ```bash
    mkdir ~/mnt-test
    ti fs mount --mount-path ~/mnt-test --region aws-us-west-2
    ```

    > **Tip:**
    >
    > The `mount` subcommand can run without prior CLI configuration, so you do not need to run `ti configure` beforehand. This is useful when, for example, you create a file system on an admin node where `ti` is configured, but mount the file system from another node or environment. In this case, set `TI_FS_TOKEN` before running `ti fs mount`.

    After mounting, you can work with the files using standard local file operations. For example, write and read a file:

    ```bash
    echo 'Hello from TiDB Cloud Filesystem' > ~/mnt-test/hello.txt
    cat ~/mnt-test/hello.txt
    ```

    Expected output:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    When you finish using the mounted file system, unmount it:

    ```bash
    ti fs umount --mount-path ~/mnt-test --region aws-us-west-2
    ```

    Unmounting removes the local mount, but the files remain in TiDB Cloud Filesystem and can be accessed again from the same or another environment.

    **Option 2: Use `ti fs` commands**

    You can also work with files directly using `ti fs` commands without mounting the file system.

    Write a file:

    ```bash
    echo "Hello from TiDB Cloud Filesystem" | ti fs copy-file \
      --file-system-id "<file-system-id>" \
      --from-stdin \
      --to-remote /hello.txt
    ```

    Then read the file:

    ```bash
    ti fs read-file \
      --file-system-id "<file-system-id>" \
      --path /hello.txt
    ```

    Expected output:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    The file is stored in TiDB Cloud Filesystem rather than in the local terminal session. It remains available after you close the terminal, and you can access it again from another session or supported environment with access to the file system.

    For more information about working with files using `ti fs` commands, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).

    </div>

    <div label="Windows">

    On Windows, you can use `ti fs` commands to work with files directly as follows. File system mounting is not supported on Windows.

    Write a file:

    ```powershell
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --file-system-id "<file-system-id>" `
      --from-stdin `
      --to-remote /hello.txt
    ```

    Then read the file:

    ```powershell
    ti fs read-file `
      --file-system-id "<file-system-id>" `
      --path /hello.txt
    ```

    Expected output:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    The file is stored in TiDB Cloud Filesystem rather than in the local PowerShell session. It remains available after you close the session, and you can access it again from another session or supported environment with access to the file system.

    For more information about working with files using `ti fs` commands, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).

    </div>

    </SimpleTab>

## What's next

- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, inspect, and manage tokens for file system access.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
