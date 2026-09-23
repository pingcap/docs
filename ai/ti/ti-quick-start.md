---
title: Get Started with TiDB Cloud CLI
summary: Install and configure TiDB Cloud CLI, then create and use a file system or query a TiDB Cloud Starter database.
---

# Get Started with TiDB Cloud CLI

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) is a command-line tool for managing [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) instances and [file systems in TiDB Cloud Filesystem](/ai/ti/ti-overview.md#tidb-cloud-filesystem). It supports both interactive use and automation, with JSON as the default output format for commands.

This guide walks you through installing and configuring TiDB Cloud CLI (`ti`), and then completing a basic workflow with TiDB Cloud Starter or TiDB Cloud Filesystem. For an overview of the CLI, its capabilities, and supported workflows, see [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md).

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/). The keys must have the `Organization Owner` access to your organization.

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

    - A default region for CLI operations, specified as a region code (such as `aws-us-east-1`). For a list of regions that are supported by TiDB Cloud CLI, see [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).
    - Your TiDB Cloud API public key and private key.

3. Run a read-only command to verify that the CLI can access TiDB Cloud using the saved credentials:

    ```bash
    ti db list-db-clusters --db-cluster-type starter --output text
    ```

    Example output:

    ```bash
    {
      "profile": "default",
      "region_code": "aws-us-east-1",
      "credentials_stored": true
    }
    ```

## Step 3. Choose a workflow

Complete either of the following workflows.

- [Option A: Create and use a file system](/ai/ti/ti-quick-start.md#option-a-create-and-use-a-file-system)
- [Option B: Create a TiDB Cloud Starter instance and query the database](/ai/ti/ti-quick-start.md#option-b-create-a-tidb-cloud-starter-instance-and-query-the-database)

### Option A: Create and use a file system

TiDB Cloud Filesystem is a persistent, shareable cloud file system that you can use across local machines, CI jobs, sandboxes, and other ephemeral environments.

1. Create a file system, wait until it is ready, and save its server-assigned ID:

    ```bash
    export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
      --wait \
      --query file_system_id \
      --output text)"
    ```

    `ti` stores the file system credential locally, so you do not need to provide it for subsequent file operations.

2. Write a file to the file system, and then read the file:

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

3. Delete the file system:

    ```bash
    ti fs delete-file-system \
      --file-system-id "$TI_FS_FILE_SYSTEM_ID"
    unset TI_FS_FILE_SYSTEM_ID
    ```

### Option B: Create a TiDB Cloud Starter instance and query the database

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

    The `ti db execute-sql-statement` command executes the query through the HTTPS SQL API. The output includes `ready = 1`.

3. Delete the TiDB Cloud Starter instance:

    ```bash
    ti db delete-db-cluster \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --wait
    unset TI_DB_CLUSTER_ID
    ```

## What's next

- Read the [TiDB Cloud Command Line Interface Overview](/ai/ti/ti-overview.md) to understand what `ti` manages and when to use it.
- Follow the task guides to manage [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) or [TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md).
- Explore the [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md) for command groups, global options, and shared CLI behavior.
- Learn about [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md) to set up multiple profiles or non-interactive authentication.
