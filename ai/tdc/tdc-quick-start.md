---
title: Get Started with TiDB Cloud CLI (tdc)
summary: Install and configure tdc, then complete a first TiDB Cloud Starter database or Filesystem operation.
---

# Get Started with TiDB Cloud CLI (tdc)

This quick start installs tdc, configures one profile, and gets a successful result from either TiDB Cloud Starter or TiDB Cloud Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

Before you begin, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page.

## Step 1. Install tdc

On macOS or Linux, run the installer:

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, add tdc to the current shell and verify it:

```bash
export PATH="$HOME/.tdc/bin:$PATH"
tdc --version
```

Add `export PATH="$HOME/.tdc/bin:$PATH"` to your shell profile to keep tdc available in new terminals.

On Windows PowerShell, run the installer:

```powershell
$script = "$env:TEMP\install-tdc.ps1"
iwr https://github.com/tidbcloud/tdc/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
```

After installation, add tdc to the current PowerShell session and verify it:

```powershell
$env:Path = "$HOME\.tdc\bin;$env:Path"
tdc --version
```

Add `$HOME\.tdc\bin` to your user `PATH` to keep tdc available in new PowerShell sessions.

## Step 2. Configure tdc

Run the interactive configuration:

```bash
tdc configure
```

Enter your API public key, private key, and a canonical region code such as `aws-us-east-1`.

Verify the configuration:

```bash
tdc organization list-projects --output text
```

## Step 3. Choose a first workflow

Complete either the Filesystem workflow or the Starter database workflow.

### Option A: Write and read a file

Create a Filesystem and make it the default:

```bash
tdc fs create-file-system \
  --file-system-name quickstart-fs \
  --set-default \
  --wait \
  --output text
```

tdc stores the Filesystem credential locally. Write and read a file directly:

```bash
printf 'hello from tdc\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /hello.txt

tdc fs read-file --path /hello.txt
```

Expected output:

```text
hello from tdc
```

Clean up:

```bash
tdc fs delete-file-system \
  --file-system-name quickstart-fs
```

### Option B: Query a Starter database

Create a Starter cluster and save its ID:

```bash
export TDC_DB_CLUSTER_ID="$(tdc db create-db-cluster \
  --db-cluster-name quickstart-db \
  --db-cluster-type starter \
  --wait \
  --query id \
  --output text)"
```

Create the SQL users and run a read-only verification query:

```bash
tdc db create-db-sql-users \
  --db-cluster-id "$TDC_DB_CLUSTER_ID"

tdc db execute-sql-statement \
  --db-cluster-id "$TDC_DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT 1 AS ready" \
  --output text
```

The command executes one statement through the HTTPS SQL API and returns a result containing `ready = 1`.

Clean up:

```bash
tdc db delete-db-cluster \
  --db-cluster-id "$TDC_DB_CLUSTER_ID" \
  --wait
unset TDC_DB_CLUSTER_ID
```

## What's next

- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [Manage TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
