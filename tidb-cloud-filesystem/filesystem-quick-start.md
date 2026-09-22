---
title: Get Started with TiDB Cloud Filesystem
summary: Create a TiDB Cloud Filesystem, write and read a persistent file, and keep the workspace available across sessions.
---

# Get Started with TiDB Cloud Filesystem

[TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-intro.md) is a persistent, shared cloud file system for applications, automation, and AI agents. Files remain available independently of the machine or process that creates them, so you can reuse the same workspace across sessions and environments.

Currently, you can access and manage TiDB Cloud Filesystems using the [TiDB Cloud CLI (`ti`)](/ai/ti/ti-quick-start.md).

This guide walks you through installing and configuring TiDB Cloud CLI (`ti`), creating a Filesystem, and writing and reading a file directly from the CLI without mounting the Filesystem. You can mount the same Filesystem afterward.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/). The keys must have the `Organization Owner` access to your organization.

If someone has already provided you with a Filesystem token, skip resource creation and follow [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

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

    - A default region for CLI operations, specified as a region code such as `aws-us-east-1`. Choose a region where you want to store the Filesystem data. For the regions supported by TiDB Cloud Filesystem, see [Supported regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions).

    - Your TiDB Cloud API public key and private key.

The CLI saves the configuration locally. The Filesystem creation command in the next step verifies that the CLI can access TiDB Cloud using the saved credentials.

To learn more about installing, configuring, and updating TiDB Cloud CLI, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 3. Create a Filesystem

Create a Filesystem and wait until it is ready:

```bash
ti fs create-file-system --display-name my-workspace --wait
```

The command returns information about the new Filesystem. Copy the returned `file_system_id` for use in the next step.

The CLI stores the Filesystem credential locally, so you do not need to provide a Filesystem token for subsequent file operations.

The display name helps you identify the Filesystem, while the Filesystem ID uniquely identifies the resource.

## Step 4. Write and read a file

Write a file to the Filesystem as follows. You need to replace `<file-system-id>` with the Filesystem ID returned in the previous step.

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

The file is stored in TiDB Cloud Filesystem rather than in the local terminal session. It remains available after you close the terminal, and you can access it again from another session or supported environment with access to the Filesystem.

> **Note:**
>
> This example accesses files in the Filesystem directly using `ti fs` commands, without mounting it to your machine.
>
> - On macOS or Linux, in addition to [using `ti fs` commands](/tidb-cloud-filesystem/work-with-filesystem-data.md), you can also [mount the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) as a local directory and work with its files using standard local file operations.
> - On Windows, native Filesystem mounting is not supported. Use `ti fs` commands such as `ti fs copy-file`, `ti fs read-file`, and `ti fs list-files` to work with files. For more information, see [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md).

## (Optional) Clean up

When you no longer need the Filesystem created in this quick start, delete it:

```bash
ti fs delete-file-system \
  --file-system-id "<file-system-id>"
```

Replace `<file-system-id>` with the Filesystem ID returned in Step 3.

Deleting the Filesystem removes the remote resource and its data.

## What's next

- [Manage TiDB Cloud Filesystem resources](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your Filesystems.
- [Mount a Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a Filesystem](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage Filesystem layers and checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
