---
title: Get Started with TiDB Cloud Filesystem
summary: Create a TiDB Cloud Filesystem with the CLI, write and read a file, and keep the workspace available for another session.
---

# Get Started with TiDB Cloud Filesystem

Create a workspace when your application's or agent's files need to outlive the machine that produces them. This quick start writes and reads a remote file without requiring a mount. You can mount the same Filesystem afterward.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Prerequisites

Obtain a TiDB Cloud API public key and private key from the [API Keys page](https://tidbcloud.com/org-settings/api-keys). The keys must have permission to create a Filesystem in your organization.

If someone has already supplied you with an FS token, skip resource creation and follow [Mounting Locally](/tidb-cloud-filesystem/filesystem-mount.md#use-a-token-without-configuring-a-profile).

## Step 1. Install the CLI

<SimpleTab>

<div label="macOS or Linux">

Run the installer:

```bash
# Install the CLI and its bundled Filesystem runtime.
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, add the binary directory to your current shell:

```bash
# Make the installed CLI available in this terminal.
export PATH="$HOME/.ti/bin:$PATH"
ti --version
```

Add the same `export PATH` line to your shell profile to use `ti` in future terminals.

</div>

<div label="Windows PowerShell">

Run the installer:

```powershell
# Download and run the PowerShell installer.
$script = "$env:TEMP\install-ti.ps1"
Invoke-WebRequest https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
```

After installation, add the binary directory to your current session:

```powershell
# Make the installed CLI available in this PowerShell session.
$env:Path = "$HOME\.ti\bin;$env:Path"
ti --version
```

Add `$HOME\.ti\bin` to your user `PATH` for future sessions.

</div>
</SimpleTab>

> **Note:**
>
> On Windows, the direct file commands in this quick start are supported, but native Filesystem mounts through `ti` are not.

For other installation and upgrade details, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 2. Configure access

```shell
# Follow the prompts to save your API keys and default region.
ti configure
```

Choose one of these Filesystem regions:

- `aws-us-east-1`
- `aws-ap-southeast-1`
- `aws-us-west-2`
- `alicloud-ap-southeast-1`

Choose a region where you want to store the Filesystem's data. For the provider and location of each region, see [Supported regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions).

Configuration saves the inputs locally. Your first remote command verifies the credentials with the service.

## Step 3. Create the Filesystem

```shell
# Wait until the new Filesystem's root is readable.
ti fs create-file-system --display-name my-workspace --wait
```

Copy the returned `file_system_id` for the next step. The CLI stores this Filesystem's token locally, so you do not need to export a token. Treat the returned `fs_token` as a secret; do not paste the output into a public issue or log.

Display names help identify resources but are not unique selectors. Subsequent commands use the ID. A failed wait does not automatically delete the created Filesystem; inspect the reported resource before creating another one. If creation reports a free-plan quota error, follow its billing link to add a payment method.

## Step 4. Write and read a file

Replace `<file-system-id>` with the ID returned by creation:

```shell
# Store a file in the remote workspace.
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
```

```shell
# Read the same file from the service.
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

The read returns `Hello from my workspace`. The file remains available after you close the terminal. There is no local mount to keep running for this workflow.

## What's next

- [Manage the Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect, check, select, and delete Filesystem resources.
- [Mount the Filesystem](/tidb-cloud-filesystem/filesystem-mount.md) to use it through a local directory.
- [Share the workspace](/tidb-cloud-filesystem/filesystem-sharing.md) with another machine or agent.
- [Manage layers and checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to review changes before publishing them.

## Clean up (optional)

When you no longer need this tutorial Filesystem, delete it using your TiDB Cloud API credentials:

```shell
# Permanently request deletion of only the tutorial resource.
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Deletion removes the remote resource and its data, not just a local registration. The command reports `deleting` when the asynchronous request is accepted.
