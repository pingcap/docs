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

3. Set the same region for every command in this tutorial. Replace `<filesystem-region-code>` with the region you chose above. On another machine, set this variable again to the region of the existing file system.

    <SimpleTab>

    <div label="macOS or Linux">

    ```bash
    export TI_REGION_CODE="<filesystem-region-code>"
    ```

    </div>

    <div label="Windows PowerShell">

    ```powershell
    $env:TI_REGION_CODE = "<filesystem-region-code>"
    ```

    </div>

    </SimpleTab>

The examples below use `TI_REGION_CODE`. If you add `--region` to a command, it overrides this variable; use the same region throughout.

The CLI saves the configuration locally and returns `"credentials_stored": true`. This confirms that the keys were saved on this machine, not that they are valid. The file system creation command in the next step makes the first request that requires authentication and fails if the key pair is invalid.

To learn more about installing, configuring, and updating TiDB Cloud CLI, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

## Step 3. Create and use a file system

1. Create a file system:

    ```bash
    ti fs create-file-system --display-name agent-workspace --wait
    ```

    The command returns information about the new file system. Save the following values for later use:

    - `file_system_id`: uniquely identifies the file system.
    - `fs_token`: the owner token for the file system.

    > **Note:**
    >
    > - The owner token grants full access to the file system and is returned only when it is issued. It does not expire, so revoke it when it is no longer needed. Treat it as a secret and keep it out of logs, issues, chat messages, and source control.
    >
    > - For least-privilege access, you can generate a scoped token to restrict access to specific paths and operations. For more information, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

2. Set the returned owner token in the environment where you will access the file system. Keep `TI_REGION_CODE` set to the file system's region. The token identifies the file system, so the following data commands do not need a separate file system ID or TiDB Cloud API keys. If you have set `TI_FS_FILE_SYSTEM_ID` for another file system, unset it first.

    <SimpleTab>

    <div label="macOS or Linux">

    ```bash
    unset TI_FS_FILE_SYSTEM_ID
    export TI_FS_TOKEN="<owner-token>"
    ```

    </div>

    <div label="Windows PowerShell">

    ```powershell
    Remove-Item Env:TI_FS_FILE_SYSTEM_ID -ErrorAction SilentlyContinue
    $env:TI_FS_TOKEN = "<owner-token>"
    ```

    </div>

    </SimpleTab>

3. Verify direct file access before mounting. Use a new example directory so that the tutorial does not overwrite existing files. Run the remaining examples in the same shell to retain the path variables.

    <SimpleTab>

    <div label="macOS or Linux">

    ```bash
    example_dir="/quick-start-$(date +%s)-$$"
    ti fs create-directory --path "$example_dir"
    printf 'Hello from TiDB Cloud Filesystem\n' | ti fs copy-file \
      --from-stdin --to-remote "$example_dir/hello.txt"
    ti fs read-file --path "$example_dir/hello.txt"
    ```

    </div>

    <div label="Windows PowerShell">

    ```powershell
    $exampleDir = "/quick-start-$([guid]::NewGuid().ToString('N'))"
    ti fs create-directory --path $exampleDir
    "Hello from TiDB Cloud Filesystem" | ti fs copy-file `
      --from-stdin --to-remote "$exampleDir/hello.txt"
    ti fs read-file --path "$exampleDir/hello.txt"
    ```

    </div>

    </SimpleTab>

    The read must print `Hello from TiDB Cloud Filesystem`. It runs in a separate CLI process and reads the stored file. If a command fails, resolve the [access or region error](/tidb-cloud-filesystem/filesystem-troubleshooting.md) before proceeding.

    To repeat the read from another machine or a clean environment, install `ti`, set `TI_FS_TOKEN` and `TI_REGION_CODE` as above, and read the same remote path. Save the value of `example_dir` (or `exampleDir`) for that environment. You do not need to copy the creator's CLI profile or API keys.

## Step 4. Mount and verify file access (optional)

Use a mount when your application needs local file paths. Direct `ti fs` commands do not require mounting and are also available on Windows, where mounting is not supported.

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

WebDAV does not support `--read-only`, layer or checkpoint mounts, or `drain-file-system`. For FUSE-specific features, install macFUSE and use `--driver fuse` instead. See [Mount a File System on macOS](/tidb-cloud-filesystem/filesystem-mount-macos.md).

</div>

</SimpleTab>

A successful mount command confirms startup, not that file I/O works. Run the following checks one at a time. If an operation has not returned after 30 seconds, interrupt it with Ctrl+C and follow [Mount succeeds but file access hangs](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs). Do not continue with writes or start a workload on an unverified mount.

```bash
cat "$mount_dir/hello.txt"
printf 'Written through the mount\n' > "$mount_dir/mounted.txt"
cat "$mount_dir/mounted.txt"
```

The reads must print `Hello from TiDB Cloud Filesystem` and `Written through the mount`, respectively. The 30-second cutoff is a diagnostic limit for this small-file smoke test, not a service latency guarantee.

Close files and applications using the mount, then unmount normally:

```bash
ti fs unmount-file-system --mount-path "$mount_dir"
```

After **successful** unmount, verify the mounted write through a new direct CLI request:

```bash
ti fs read-file --path "$example_dir/mounted.txt"
```

Expected output:

```text
Written through the mount
```

This remote read is the persistence check; reading through the same mount can use cached data. If unmount fails, keep the machine and local mount data available and follow [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

## Step 5. Clean up the example

After verification and, if applicable, successful unmount, delete only the example directory created in Step 3:

<SimpleTab>

<div label="macOS or Linux">

```bash
ti fs delete-file --path "${example_dir:?Set the example directory first}" --recursive
ti fs describe-file --path "$example_dir/hello.txt"
```

If you mounted the example, remove the now-empty local mount directory with `rmdir "$mount_dir"`.

</div>

<div label="Windows PowerShell">

```powershell
if (-not $exampleDir) { throw "Set the example directory first" }
ti fs delete-file --path $exampleDir --recursive
ti fs describe-file --path "$exampleDir/hello.txt"
```

</div>

</SimpleTab>

The describe command must report that the file does not exist. An authentication or network error does not confirm cleanup.

These commands keep the file system and its tokens available for reuse. If you created a disposable file system and no longer need any of its data, follow [Delete a file system](/tidb-cloud-filesystem/manage-filesystem-resources.md#delete-a-file-system). Otherwise, revoke any temporary tokens you issued using [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md#rotate-or-revoke-a-token); unsetting an environment variable does not revoke a token.

## What's next

- [Manage File Systems in TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md) to inspect and manage your file systems.
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) to create, inspect, and manage tokens for file system access.
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md) to access its files through a local directory.
- [Share a File System](/tidb-cloud-filesystem/filesystem-sharing.md) to make the same files available to another machine, user, application, or agent.
- [Manage File System Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md) to isolate, review, and apply file changes.
