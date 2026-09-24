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

## Step 3. Create a new file system

1. Create a file system and obtain its default file system token:

    ```bash
    export TI_FS_TOKEN="$(ti fs create-file-system --display-name agent-workspace --wait --query fs_token --output text --region aws-us-west-2)"
    ```

    > **Tip:**
    >
    > For simplicity, this quick start uses the token returned when the file system is created. For least-privilege access, you can generate a scoped token to restrict access to specific paths and operations. For more information, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

2. In the environment where you want to use the file system, set the file system token from the previous step as `TI_FS_TOKEN`, and then mount the file system to a local path as follows. This environment can be the same machine where you created the file system, another machine, or an AI agent sandbox.

    ```bash
    export TI_FS_TOKEN="<owner-token>" # Skip this line if you are continuing in the same terminal as step 1, where TI_FS_TOKEN is already set.
    mkdir ~/mnt-test
    ti fs mount --mount-path ~/mnt-test --region aws-us-west-2
    echo 'Hello from TiDB Cloud Filesystem' >> ~/mnt-test/hello.txt
    ls -l ~/mnt-test/hello.txt
    ```

    > **Tip:**
    >
    > The `mount` subcommand supports configuration-free execution, so you do not need to run `ti configure` beforehand. This is common when, for example, you create a file system on an admin node (where `ti-cli` is configured), but access the file system from another node or environment. In such cases, you can use the `ti fs mount` command by simply specifying the `TI_FS_TOKEN` environment variable, without any prior CLI configuration.

    After mounting, you can work with the files using standard local file operations.

3. After you finish using the mounted file system in that environment, unmount it:

    ```bash
    ti fs unmount --mount-path ~/mnt-test --region aws-us-west-2
    ```

    Unmounting removes the local mount, but the files remain in TiDB Cloud Filesystem and can be accessed again from the same or another environment.

## What's next

- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
