---
title: Get Started with TiDB Cloud CLI
summary: Install and configure the TiDB Cloud CLI, then complete a first TiDB Cloud Starter database or Filesystem operation.
---

# Get Started with TiDB Cloud CLI

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) is a command-line tool for managing TiDB Cloud Starter instances and TiDB Cloud Filesystems. It supports both interactive use and automation, with JSON as the default output format for commands.

This guide walks you through installing `ti`, configuring a profile, and running your first command with TiDB Cloud Starter or TiDB Cloud Filesystem. For an overview of the CLI, its capabilities, and supported workflows, see [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md).

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/).

## Step 1. Install TiDB Cloud CLI

Depending on your operating system, take the following steps to install TiDB Cloud CLI.

<SimpleTab>

<div label="macOS or Linux">

1. On macOS or Linux, run the installer:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. Add `ti` to the current shell and verify it:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. Add `export PATH="$HOME/.ti/bin:$PATH"` to your shell profile to keep `ti` available in new terminals.

</div>

<div label="Windows PowerShell">

1. On Windows PowerShell, run the installer:

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

3. Add `$HOME\.ti\bin` to your user `PATH` to keep `ti` available in new PowerShell sessions.

</div>
</SimpleTab>

## Step 2. Configure TiDB Cloud CLI

1. Run the interactive configuration:

    ```bash
    ti configure
    ```

2. Enter your TiDB Cloud API public key, private key, and a canonical region code such as `aws-us-east-1`.

3. Run a read-only command to verify the saved credentials and selected region:

    ```bash
    ti db list-db-clusters --db-cluster-type starter --output text
    ```

## Step 3. Choose a first workflow

Complete either the Filesystem workflow or the Starter database workflow.

- [Option A: Write and read a file](/ai/ti/ti-quick-start.md#option-a-write-and-read-a-file)
- [Option B: Query a Starter database](/ai/ti/ti-quick-start.md#option-b-query-a-starter-database)

### Option A: Write and read a file

1. Create a Filesystem, wait until it is ready, and save its server-assigned ID:

    ```bash
    export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
      --wait \
      --query file_system_id \
      --output text)"
    ```

    `ti` stores the Filesystem credential locally.

2. Write and read a file directly:

    ```bash
    printf 'hello from ti\n' | ti fs copy-file \
      --from-stdin \
      --to-remote /hello.txt

    ti fs read-file \
      --path /hello.txt
    ```

    Expected output:

    ```text
    hello from ti
    ```

3. Delete the Filesystem:

    ```bash
    ti fs delete-file-system \
      --file-system-id "$TI_FS_FILE_SYSTEM_ID"
    unset TI_FS_FILE_SYSTEM_ID
    ```

### Option B: Query a Starter database

1. Create a TiDB Cloud Starter instance and save its ID:

    ```bash
    export TI_DB_CLUSTER_ID="$(ti db create-db-cluster \
      --db-cluster-type starter \
      --db-cluster-name quickstart-db \
      --wait \
      --query id \
      --output text)"
    ```

2. Create the SQL users and run a read-only query to verify the connection:

    ```bash
    ti db create-db-sql-users \
      --db-cluster-id "$TI_DB_CLUSTER_ID"

    ti db execute-sql-statement \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --read-only \
      --sql "SELECT 1 AS ready" \
      --output text
    ```

    The command executes one statement through the HTTPS SQL API and returns a result containing `ready = 1`.

3. Delete the TiDB Cloud Starter instance:

    ```bash
    ti db delete-db-cluster \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --wait
    unset TI_DB_CLUSTER_ID
    ```

## What's next

- Read the [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md) to understand what `ti` manages and when to use it.
- Follow the task guides to manage [TiDB Cloud Starter instances](/ai/ti/guides/manage-starter-instances.md) or [Filesystem resources](/ai/ti/guides/manage-filesystem-resources.md).
- Explore the [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md) for the full command list.
- Learn about [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md) to set up multiple profiles or non-interactive authentication.
