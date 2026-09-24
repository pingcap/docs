---
title: Get Started with TiDB Cloud Filesystem
summary: Create a file system, write and read a persistent file, and keep the workspace available across sessions.
---

# Get Started with TiDB Cloud Filesystem

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) is a persistent, shared cloud file system for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so you can reuse the same workspace across sessions and environments.

Currently, you can access and manage TiDB Cloud Filesystem using the [TiDB Cloud CLI (`ti`)](/ai/ti/ti-quick-start.md).

This guide walks you through installing and configuring TiDB Cloud CLI (`ti`), creating a file system, and writing and reading a file directly from the CLI without mounting the file system. You can mount the same file system afterward.

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

    - A default region for CLI operations, specified as a region code such as `aws-us-east-1`. Choose a region where you want to store the file system data. For the regions supported by TiDB Cloud Filesystem, see [Supported regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions).

        The free tier allows one file system for each region. If your organization already has a file system in the region you choose, select a different supported region, add a payment method in the [TiDB Cloud console](https://tidbcloud.com/org-settings/billing/payments), or reuse the existing file system.

    - Your TiDB Cloud API public key and private key.

The CLI saves the configuration locally and returns `"credentials_stored": true`. This confirms that the keys were saved on this machine, not that they are valid. The file system creation command in the next step makes the first request that requires authentication and fails if the key pair is invalid.

To learn more about installing, configuring, and updating TiDB Cloud CLI, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 3. Create a file system

Create a file system. With the `--wait` option, the command returns only after the file system is usable, so you do not need to check its status:

```bash
ti fs create-file-system --display-name my-workspace --wait
```

The command returns information about the new file system. Copy the returned `file_system_id` for use in the next step.

> **Warning:**
>
> The output also contains a file system owner token in the `fs_token` field. This token grants full access to the file system and is returned only when it is issued. It does not expire, so revoke it when it is no longer needed. Treat it as a secret and keep it out of logs, issues, chat messages, and source control. For more information, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

The CLI stores the file system owner token locally, so you do not need to provide it for subsequent file operations on this machine.

The display name helps you identify the file system, while the file system ID uniquely identifies the resource.

## Step 4. Write and read a file

Write a file to the file system as follows. You need to replace `<file-system-id>` with the file system ID returned in the previous step.

```bash
echo "Hello from my workspace" | ti fs copy-file \
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
Hello from my workspace
```

The file is stored in TiDB Cloud Filesystem rather than in the local terminal session. It remains available after you close the terminal, and you can access it again from another session or supported environment with access to the file system.

> **Note:**
>
> This example accesses files in the file system directly using `ti fs` commands, without mounting it to your machine.
>
> - On macOS or Linux, in addition to [using `ti fs` commands](/tidb-cloud-filesystem/work-with-filesystem-data.md), you can also [mount the file system](/tidb-cloud-filesystem/filesystem-mount.md) as a local directory and work with its files using standard local file operations.
> - On Windows, native file system mounting is not supported. Use `ti fs` commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` to work with files. For more information, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).

## (Optional) Clean up

When you no longer need the file system created in this quick start, delete it:

```bash
ti fs delete-file-system \
  --file-system-id "<file-system-id>"
```

Replace `<file-system-id>` with the file system ID returned in Step 3.

Deleting the file system removes the remote resource and its data.

## What's next

- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
