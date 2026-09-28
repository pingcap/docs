---
title: Get Started with TiDB Cloud Filesystem
summary: Learn how to create a persistent TiDB Cloud file system, verify CLI reads and writes, and optionally access its files through a local mount.
---

# Get Started with TiDB Cloud Filesystem

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

For CI or agents, inject `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY` from a secret manager and set `TI_REGION_CODE`. Run `ti configure --non-interactive`, then continue to Step 3. See [Configure for automation](/ai/ti/reference/ti-install-configure-update.md#configure-for-automation) for details.

For an interactive terminal:

1. Run the interactive configuration:

    ```bash
    ti configure
    ```

2. Provide the following information:

    - The region you selected.
    - Your TiDB Cloud API public key and private key.

3. Set the region for this tutorial. Replace `<filesystem-region-code>` with the region you just selected:

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    export TI_REGION_CODE="<filesystem-region-code>"
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    $env:TI_REGION_CODE = "<filesystem-region-code>"
    ```

    </div>

    </SimpleTab>

The commands use `TI_REGION_CODE` unless you specify `--region`. Configuration saves your credentials locally; creating the file system in the next step validates them.

## Step 3. Create and use a file system

For CI or agents, disable command tracing before handling tokens. Capture the creation command's JSON response in a protected variable or secret store, and exclude it from job logs. Save both `file_system_id` and `fs_token` from the captured response.

1. Create a file system:

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait
    ```

    This command uses the region set in `TI_REGION_CODE` in Step 2. If you open a new shell, set that variable again before continuing.

    Save these values from the response:

    - `file_system_id`: uniquely identifies the file system.
    - `fs_token`: the owner token for the file system.

    > **Note:**
    >
    > The owner token grants full access, does not expire, and is shown only when issued. Store it securely. For limited access or revocation, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

2. Load the owner token. Paste the returned `fs_token` at the prompt and press Enter; input is hidden. These commands also clear any previous file system selection. Keep `TI_REGION_CODE` set.

    In automation, set `TI_FS_TOKEN` from the captured `fs_token` and clear `TI_FS_FILE_SYSTEM_ID`. Skip the input prompts.

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    `read` captures your token without displaying it, and `export` makes it available to subsequent `ti` commands in this shell. The token you enter at the `read` prompt is not recorded in shell history.

    ```bash
    unset TI_FS_FILE_SYSTEM_ID
    printf 'Owner token: '
    read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    Remove-Item Env:TI_FS_FILE_SYSTEM_ID -ErrorAction SilentlyContinue
    $env:TI_FS_TOKEN = [System.Net.NetworkCredential]::new(
      "", (Read-Host "Owner token" -AsSecureString)
    ).Password
    ```

    </div>

    </SimpleTab>

3. Create a unique directory, upload a sample file, and read it back:

    <SimpleTab groupId="operating-systems">

    <div label="macOS or Linux" value="macos-or-linux">

    ```bash
    example_dir="/quick-start-$(date +%s)-$$"
    ti fs create-directory --path "$example_dir"
    printf 'Hello from TiDB Cloud Filesystem\n' | ti fs copy-file \
      --from-stdin --to-remote "$example_dir/hello.txt"
    ti fs read-file --path "$example_dir/hello.txt"
    ```

    </div>

    <div label="Windows PowerShell" value="windows-powershell">

    ```powershell
    $exampleDir = "/quick-start-$([guid]::NewGuid().ToString('N'))"
    ti fs create-directory --path $exampleDir
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --from-stdin --to-remote "$exampleDir/hello.txt"
    ti fs read-file --path "$exampleDir/hello.txt"
    ```

    </div>

    </SimpleTab>

    Expected output from `read-file`:

    ```text
    Hello from TiDB Cloud Filesystem
    ```

    Your file is now stored remotely. If a command fails, [resolve the error](/tidb-cloud-filesystem/filesystem-troubleshooting.md) before continuing. To access it from another environment, see [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md).

## Step 4. Mount and verify file access (optional)

Mount the file system if your application needs local file paths. On Windows, or if you only need CLI access, skip to [Step 5](#step-5-clean-up-the-example).

On macOS or Linux, first complete the [mount prerequisites for your platform](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method). Create a new local directory:

```bash
mount_dir="$(mktemp -d "$HOME/ti-fs-quick-start.XXXXXX")"
```

Choose **one** mount command:

<SimpleTab>

<div label="Linux FUSE">

```bash
ti fs mount-file-system --remote-path "$example_dir" \
  --mount-path "$mount_dir" --driver fuse
```

</div>

<div label="macOS WebDAV">

```bash
ti fs mount-file-system --remote-path "$example_dir" \
  --mount-path "$mount_dir" --driver webdav
```

For FUSE-specific features, see [Mount a File System on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md).

</div>

</SimpleTab>

A successful mount command confirms startup. Verify file access before using the mount. If a check takes longer than 30 seconds, interrupt it with Ctrl+C and follow [mount troubleshooting](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs) before continuing.

1. Read the uploaded file through the mount:

    ```bash
    cat "$mount_dir/hello.txt"
    ```

    Expected output: `Hello from TiDB Cloud Filesystem`.

2. Write a new file through the mount:

    ```bash
    printf 'Written through the mount\n' > "$mount_dir/mounted.txt"
    ```

3. Close applications using the mount and unmount it:

    ```bash
    ti fs unmount-file-system --mount-path "$mount_dir"
    ```

    If unmount fails, keep the machine and local mount data available and follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

4. After successful unmount, read the new file directly from the service:

    ```bash
    ti fs read-file --path "$example_dir/mounted.txt"
    ```

    Expected output: `Written through the mount`. This confirms that the write reached the service, independently of the mount's cache.

## Step 5. Clean up the example

After verification and, if applicable, successful unmount, delete only the example directory created in Step 3:

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```bash
ti fs delete-file --path "${example_dir:?Set the example directory first}" --recursive
ti fs describe-file --path "$example_dir"
```

If you mounted the example, remove the now-empty local mount directory with `rmdir "$mount_dir"`.

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
if (-not $exampleDir) { throw "Set the example directory first" }
ti fs delete-file --path $exampleDir --recursive
ti fs describe-file --path $exampleDir
```

</div>

</SimpleTab>

Expect a not-found error from `describe-file`. Other errors do not confirm deletion.

The file system and its token remain available for reuse. To remove the entire file system, see [Delete a file system](/tidb-cloud-filesystem/manage-filesystem-resources.md#delete-a-file-system).

## What's next

- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, inspect, and manage tokens for file system access.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
