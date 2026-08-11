---
title: Install, Configure, and Update TiDB Cloud CLI
summary: Install TiDB Cloud CLI releases, configure profiles, check versions, apply updates, and uninstall the CLI.
---

# Install, Configure, and Update TiDB Cloud CLI

This reference documents the supported release installers, top-level configuration and update commands, help and version behavior, and uninstallation.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
ti
├── configure
└── update
```

| Command | Required inputs | Main optional inputs | Example |
| --- | --- | --- | --- |
| `ti configure` | Interactive input, or region and TiDB Cloud API keys in non-interactive mode | `--profile`, `--non-interactive`, `--region-code`, key flags | `ti configure --profile staging` |
| `ti update` | None | `--check`, `--fail-if-update-available`, `--dry-run`, `--target-version` | `ti update --check` |

Run `ti configure help` or `ti update help` for the complete generated flag list.

## Install TiDB Cloud CLI

### macOS and Linux

Run the installer:

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

After installation, add `ti` to the current shell and verify it:

```bash
export PATH="$HOME/.ti/bin:$PATH"
ti --version
```

The installer places `ti` and its `ti-drive9` companion in `~/.ti/bin`. Add the `PATH` export to your shell profile. The installer does not require `sudo` and does not write credentials.

After installation, the installer displays the anonymous telemetry fields, prohibited data, persistent opt-out path, and process-scoped `TI_TELEMETRY=off` override. It does not prompt for a telemetry choice or create the optional preferences file.

### Windows

Run the installer:

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

The Windows installer displays the same anonymous telemetry and opt-out notice without creating a preference or installation identity.

## Configure a profile

Interactive configuration is the only TiDB Cloud CLI workflow that prompts:

```bash
ti configure
```

The TiDB Cloud CLI requests a TiDB Cloud API public key, private key, and canonical region code, validates those values locally, and stores the selected profile. Configuration makes no network request. The first remote command reports authentication or authorization errors for the permission it requires.

Configure a named profile:

```bash
ti configure --profile staging
```

For CI or another non-interactive environment, prefer environment variables:

```bash
TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
TI_REGION_CODE="aws-us-east-1" \
ti configure --profile ci --non-interactive
```

You can also provide `--tidb-cloud-public-key`, `--tidb-cloud-private-key`, and `--region-code`, but secret flags can remain in shell history or process listings.

Configuration precedence is command flag, environment variable, then saved profile. The global `--region` overrides only the placement for the current command:

```bash
ti db list-db-clusters --db-cluster-type starter --profile staging --region aws-us-west-2
```

## Get help and version information

All command levels support `help`, `--help`, and `--version`:

```bash
ti help
ti fs help
ti db create-db-cluster help
ti --version
ti fs --version
```

Required flags appear before optional flags in generated usage. The TiDB Cloud CLI supports long flags only.

## Update TiDB Cloud CLI

Check without changing files:

```bash
ti update --check
```

In automation, fail when an update exists:

```bash
ti update --check --fail-if-update-available
```

Preview and apply an update:

```bash
ti update --dry-run
ti update
```

Install a specific TiDB Cloud CLI release:

```bash
ti update --target-version v0.1.2
```

The update command replaces both binaries in the user-owned install directory. An active Filesystem mount keeps running the already loaded companion process. To avoid mixing the old mount runtime with new CLI commands, stop writers and unmount before updating. Graceful unmount automatically flushes and drains pending FUSE work:

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
ti update
```

For WebDAV, close writers and unmount. Use the FUSE-only drain command separately only when you need a durability barrier without unmounting. Installations in protected or package-manager-owned locations are not modified. Run the installer once to migrate an older `/usr/local/bin` installation to `~/.ti/bin`.

## Migrate from tdc v0.1.x

The `ti` installer and the first non-update `ti` command migrate supported local state from `~/.tdc/` to `~/.ti/` when `~/.tdc/` exists and `~/.ti/` does not. The migration includes profiles, TiDB Cloud API credentials, global preferences, the telemetry installation identity, DB SQL credentials, and Filesystem registrations and credentials. It preserves `~/.tdc/` as a rollback copy and does not copy binaries, logs, caches, local overlays, mount locators, or companion runtime state. A hidden owner-only marker under `~/.ti/` records that the old and new directories coexist because migration completed successfully.

Before installing `ti`, unmount active tdc Filesystem and Vault mounts. The migration refuses to proceed while an old mount is active because copying runtime state cannot transfer a live FUSE or WebDAV process safely.

If both directories were created independently, or the migration marker is absent, invalid, or points to a different source, `ti` stops without merging or overwriting either directory. Move or remove the directory that is not your intended source of truth, and then run the command again. Do not combine credential or Filesystem registry directories manually.

During the v0.2.x transition, `ti` accepts legacy `TDC_*` environment variables only when the corresponding canonical variable is absent. If both forms are set to different values, the command fails before changing local or remote state. New automation should use `TI_*` and `TIDB_CLOUD_*` variables. Legacy environment variable support is removed in v0.3.0.

## Uninstall TiDB Cloud CLI

Remove only the binaries:

```bash
rm -f "$HOME/.ti/bin/ti" "$HOME/.ti/bin/ti-drive9"
```

On Windows:

```powershell
Remove-Item "$HOME\.ti\bin\ti.exe", "$HOME\.ti\bin\ti-drive9.exe"
```

Removing binaries preserves profiles, credentials, Filesystem registrations, DB SQL credentials, logs, and mount locators. Remove `~/.ti/` only when you intend to delete all local TiDB Cloud CLI state:

```bash
rm -rf "$HOME/.ti"
```

Deleting local state does not delete remote Starter clusters or Filesystem resources.

## What's next

- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud Starter CLI Command Reference](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
