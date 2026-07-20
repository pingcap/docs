---
title: Install, Configure, and Update tdc
summary: Install tdc release binaries, configure profiles interactively or in automation, update safely, and remove the CLI.
---

# Install, Configure, and Update tdc

This guide covers the supported release installers, profile configuration, help and version behavior, updates, and uninstallation.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Install tdc

### macOS and Linux

Run the installer:

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, add tdc to the current shell and verify it:

```bash
export PATH="$HOME/.tdc/bin:$PATH"
tdc --version
```

The installer places `tdc` and its `tdc-drive9` companion in `~/.tdc/bin`. Add the `PATH` export to your shell profile. The installer does not require `sudo` and does not write credentials.

### Windows

Run the installer:

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

## Configure a profile

Interactive configuration is the only tdc workflow that prompts:

```bash
tdc configure
```

tdc requests a TiDB Cloud API public key, private key, and canonical region code. It validates the key by listing projects and records the unique `tidbx_virtual` project as the profile's default project.

Configure a named profile:

```bash
tdc configure --profile staging
```

For CI or another non-interactive environment, prefer environment variables:

```bash
TDC_PUBLIC_KEY="<public-key>" \
TDC_PRIVATE_KEY="<private-key>" \
TDC_REGION_CODE="aws-us-east-1" \
tdc configure --profile ci --non-interactive
```

You can also provide `--tdc-public-key`, `--tdc-private-key`, and `--region-code`, but secret flags can remain in shell history or process listings.

Configuration precedence is command flag, environment variable, then saved profile. The global `--region` overrides only the placement for the current command:

```bash
tdc db list-db-clusters --profile staging --region aws-us-west-2
```

## Get help and version information

All command levels support `help`, `--help`, and `--version`:

```bash
tdc help
tdc fs help
tdc db create-db-cluster help
tdc --version
tdc fs --version
```

Required flags appear before optional flags in generated usage. tdc supports long flags only.

## Update tdc

Check without changing files:

```bash
tdc update --check
```

In automation, fail when an update exists:

```bash
tdc update --check --fail-if-update-available
```

Preview and apply an update:

```bash
tdc update --dry-run
tdc update
```

Install a specific tdc release:

```bash
tdc update --target-version v0.1.2
```

The update command replaces both binaries in the user-owned install directory. An active Filesystem mount keeps running the already loaded companion process. To avoid mixing the old mount runtime with new CLI commands, stop writers and unmount before updating. Graceful unmount automatically flushes and drains pending FUSE work:

```bash
tdc fs unmount-file-system --mount-path /path/to/workspace
tdc update
```

For WebDAV, close writers and unmount. Use the FUSE-only drain command separately only when you need a durability barrier without unmounting. Installations in protected or package-manager-owned locations are not modified. Run the installer once to migrate an older `/usr/local/bin` installation to `~/.tdc/bin`.

## Uninstall tdc

Remove only the binaries:

```bash
rm -f "$HOME/.tdc/bin/tdc" "$HOME/.tdc/bin/tdc-drive9"
```

On Windows:

```powershell
Remove-Item "$HOME\.tdc\bin\tdc.exe", "$HOME\.tdc\bin\tdc-drive9.exe"
```

Removing binaries preserves profiles, credentials, Filesystem registrations, DB SQL credentials, logs, and mount locators. Remove `~/.tdc/` only when you intend to delete all local tdc state:

```bash
rm -rf "$HOME/.tdc"
```

Deleting local state does not delete remote Starter clusters or Filesystem resources.

## What's next

- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [Manage TiDB Cloud Starter Databases](/ai/tdc/guides/tdc-starter-database.md)
- [Manage TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem.md)
