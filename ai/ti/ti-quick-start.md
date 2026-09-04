---
title: Get Started with TiDB Cloud CLI
summary: Install and configure the TiDB Cloud CLI, then complete a first TiDB Cloud Starter database or Filesystem operation.
---

# Get Started with TiDB Cloud CLI

This quick start installs the TiDB Cloud CLI, configures one profile, and gets a successful result from either TiDB Cloud Starter or TiDB Cloud Filesystem.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## When to use this quick start

Use this quick start when you want to automate a new Starter database or create a persistent workspace for a user, script, or AI agent. It follows the TiDB Cloud CLI workflow. If you manage TiDB Cloud Essential or need an operation that the TiDB Cloud CLI does not provide, use the [`ticloud` CLI documentation](/tidb-cloud/get-started-with-cli.md).

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page.

## Step 1. Install TiDB Cloud CLI

On macOS or Linux, run the installer:

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, add `ti` to the current shell and verify it:

```bash
export PATH="$HOME/.ti/bin:$PATH"
ti --version
```

Add `export PATH="$HOME/.ti/bin:$PATH"` to your shell profile to keep `ti` available in new terminals.

On Windows PowerShell, run the installer:

```powershell
$script = "$env:TEMP\install-ti.ps1"
iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
```

After installation, add `ti` to the current PowerShell session and verify it:

```powershell
$env:Path = "$HOME\.ti\bin;$env:Path"
ti --version
```

Add `$HOME\.ti\bin` to your user `PATH` to keep `ti` available in new PowerShell sessions.

## Step 2. Configure TiDB Cloud CLI

Run the interactive configuration:

```bash
ti configure
```

Enter your API public key, private key, and a canonical region code such as `aws-us-east-1`.

Run a read-only command to verify the saved credentials and selected region:

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

## Step 3. Choose a first workflow

Complete either the Filesystem workflow or the Starter database workflow.

### Option A: Write and read a file

Create a Filesystem, wait until it is ready, and save its server-assigned ID:

```bash
export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
  --wait \
  --query file_system_id \
  --output text)"
```

`ti` stores the Filesystem credential locally. Write and read a file directly:

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

Clean up:

```bash
ti fs delete-file-system \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID"
unset TI_FS_FILE_SYSTEM_ID
```

### Option B: Query a Starter database

Create a Starter cluster and save its ID:

```bash
export TI_DB_CLUSTER_ID="$(ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name quickstart-db \
  --wait \
  --query id \
  --output text)"
```

Create the SQL users and run a read-only verification query:

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

Clean up:

```bash
ti db delete-db-cluster \
  --db-cluster-id "$TI_DB_CLUSTER_ID" \
  --wait
unset TI_DB_CLUSTER_ID
```

## What's next

- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
