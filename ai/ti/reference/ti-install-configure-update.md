---
title: Install, Configure, and Update TiDB Cloud CLI
summary: Install TiDB Cloud CLI releases, configure profiles, check versions, apply updates, and uninstall the CLI.
---

# Install, Configure, and Update TiDB Cloud CLI

Use this guide to install and configure TiDB Cloud CLI (`ti`), check for and apply updates, and uninstall the CLI when needed.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Prerequisites

To configure TiDB Cloud CLI, obtain a TiDB Cloud API public key and private key from the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the TiDB Cloud console first.

> **Note:**
>
> If you previously used TiDB Cloud CLI `tdc` v0.1.x, unmount any Filesystem or Vault mounts started by `tdc`, and read [Migrate from tdc to TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md) before installing `ti`.

## Install TiDB Cloud CLI

Depending on your operating system, follow the steps below to install the TiDB Cloud CLI.

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. On macOS or Linux, run the following command to install the TiDB Cloud CLI:

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. Add `ti` to the current shell and verify it:

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. To keep `ti` available in new terminal sessions, add it to your shell profile. For example, if you use `zsh`, run the following commands:

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

    If you use Bash, add the same `export` command to the startup file used by your terminal, commonly `~/.bashrc` on Linux or `~/.bash_profile` on macOS.

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. On Windows PowerShell, run the following command to install the TiDB Cloud CLI:

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

The installer writes to your home directory and does not require elevated privileges.

The installer also displays a notice about anonymous usage telemetry and how to opt out. Installation does not require you to make a telemetry choice. For details, see [Anonymous telemetry](/ai/ti/reference/ti-configuration-and-credentials.md#anonymous-telemetry).

## Configure a profile

A profile is a named set of TiDB Cloud API public key, private key, and region code.

This section describes how to configure a profile for the TiDB Cloud CLI.

### Configure interactively

By default, `ti configure` prompts you for the information required to configure a profile:

```bash
ti configure
```

`ti configure` prompts you for your TiDB Cloud API public key and private key, and a default region code. The CLI uses this region for commands unless you override it for an individual command. For available regions, see [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).

The command validates the input format locally and saves the profile without making a request to TiDB Cloud. Your credentials are verified when you run a command that accesses TiDB Cloud. To change the default profile, run `ti configure` again. To change a named profile, include its name, for example, `ti configure --profile staging`.

### Configure a named profile

Pass `--profile` to configure a named profile:

```bash
ti configure --profile staging
```

### Configure for automation

For CI or another non-interactive environment, prefer environment variables:

```bash
TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
TI_REGION_CODE="aws-us-east-1" \
ti configure --profile ci --non-interactive
```

You can also provide `--tidb-cloud-public-key`, `--tidb-cloud-private-key`, and `--region-code`, but secret flags can remain in shell history or process listings.

## Select a profile and override its region

To use a named profile and override its default region for one command, use the global `--profile` and `--region` options:

```bash
ti --profile staging --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
```

For detailed profile, credential, and region precedence rules, see [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md).

## Get help and check the version

Use `help` or `--help` to inspect commands and `--version` to check the installed version:

```bash
ti help
ti fs help
ti --version
```

For command groups and CLI conventions, see [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md).

## Update TiDB Cloud CLI

Check without changing files:

```bash
ti update --check
```

In automation, return exit code `1` when a newer version is available:

```bash
ti update --check --fail-if-update-available
```

Preview an update:

```bash
ti update --dry-run
```

> **Note:**
>
> If you have an active Filesystem or Vault mount, stop writers and unmount it before updating so that `ti` and the Filesystem runtime are updated together. For example:
>
> ```bash
> ti fs unmount-file-system --mount-path <mount-path>
> ```
>
> For a Vault mount, use `ti fs-vault unmount-vault --mount-path <mount-path>`. For details, see [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md) and [Manage Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md).

Apply the latest update:

```bash
ti update
```

Install a specific release:

```bash
ti update --target-version <version>
```

The update command replaces both `ti` and `ti-drive9` in a user-owned installation. It does not modify installations in protected or package-manager-owned locations. To migrate an older `/usr/local/bin` installation to `~/.ti/bin`, run the installer once.

## Migrate from tdc v0.1.x

If you have never used `tdc` v0.1.x, skip this section.

If you previously used `tdc` v0.1.x, `ti` can migrate supported local profiles, credentials, preferences, and Filesystem state from `~/.tdc/` to `~/.ti/`. Before installing `ti`, unmount any Filesystem or Vault mounts started by `tdc`.

For the complete migration procedure, including migrated and excluded state, directory conflict resolution, and legacy environment variable compatibility, see [Migrate from tdc to TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md).

## Uninstall TiDB Cloud CLI

Before uninstalling, stop writers and unmount any active Filesystem or Vault mounts.

For example, run the command that corresponds to the type of mount:

```bash
# Filesystem mount
ti fs unmount-file-system --mount-path <filesystem-mount-path>

# Vault mount
ti fs-vault unmount-vault --mount-path <vault-mount-path>
```

For details, see [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md) and [Manage Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md).

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. Remove the binaries:

    ```bash
    rm -f "$HOME/.ti/bin/ti" "$HOME/.ti/bin/ti-drive9"
    ```

2. Remove the `~/.ti/bin` entry that you added to your shell profile during installation.

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. Remove the binaries:

    ```powershell
    Remove-Item "$HOME\.ti\bin\ti.exe", "$HOME\.ti\bin\ti-drive9.exe"
    ```

2. Remove `$HOME\.ti\bin` from your user `PATH`:

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $newPath = (($userPath -split ";") | Where-Object { $_ -and $_ -ne $tiBin }) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    ```

</div>
</SimpleTab>

### Remove local state

Removing binaries preserves profiles, credentials, Filesystem registrations, DB SQL credentials, logs, and mount locators.

> **Note:**
>
> Remove `~/.ti/` only when you intend to permanently delete all local TiDB Cloud CLI state. Deleting local state does not delete remote TiDB Cloud Starter instances or Filesystem resources.

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

On macOS or Linux:

```bash
rm -rf "$HOME/.ti"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

On Windows PowerShell:

```powershell
Remove-Item "$HOME\.ti" -Recurse -Force
```

</div>
</SimpleTab>

## See also

- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
