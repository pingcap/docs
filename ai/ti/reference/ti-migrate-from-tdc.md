---
title: Migrate from tdc to TiDB Cloud CLI
summary: Migrate supported local state and automation from tdc v0.1.x to TiDB Cloud CLI.
---

# Migrate from tdc to TiDB Cloud CLI

This migration applies only if you previously used `tdc` v0.1.x. New TiDB Cloud CLI installations do not require it.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Before you begin

- Stop writers and unmount every Filesystem and Vault mount started by `tdc`. Migration stops if an old mount is still active because it cannot transfer a running FUSE or WebDAV process.

    Run the commands that match each active mount. For a FUSE Filesystem mount, run `drain-file-system` to flush pending writes, and then run `unmount-file-system` to detach the mount. For a WebDAV Filesystem mount, stop writers and run only `unmount-file-system`. A Vault mount only requires `unmount-vault`.

    ```bash
    # FUSE Filesystem mount
    tdc fs drain-file-system --mount-path <filesystem-mount-path>
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # WebDAV Filesystem mount
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # Vault mount
    tdc fs-vault unmount-vault --mount-path <vault-mount-path>
    ```

- Back up `~/.tdc/` and any existing `~/.ti/` directory before resolving a directory conflict.

## Install ti and migrate local state

The old `tdc update` command cannot install the renamed `ti` executable, and `ti` does not provide a `tdc` command alias. Install `ti` directly by following [Install TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli).

The installer and the first non-update `ti` command automatically migrate supported local state when `~/.tdc/` exists and `~/.ti/` does not. The migration preserves `~/.tdc/` as a rollback copy and creates an owner-only marker under `~/.ti/` to record the completed migration.

The following table summarizes which state is migrated:

| Migrated | Not migrated |
| --- | --- |
| Profiles and TiDB Cloud API credentials | Binaries |
| Global preferences and the telemetry installation identity | Logs and caches |
| Database SQL credentials | Local overlays |
| Filesystem registrations and credentials | Mount locators and companion runtime state |

After installation, verify the new executable and run a read-only command for the resources you use. For example:

```bash
ti --version

# For TiDB Cloud Starter
ti db list-db-clusters --db-cluster-type starter --output text

# For TiDB Cloud Filesystem
ti fs list-file-systems --output text
```

After you verify the migration, you can remove the old `tdc` binaries and local state when you no longer need the rollback copy.

## Resolve a local state conflict

If `~/.tdc/` and `~/.ti/` were created independently, or the migration marker is missing, invalid, or references a different source, `ti` stops without merging or overwriting either directory.

Determine which directory is the intended source of truth, and move the other directory to a backup location. Then run the installer or `ti` command again. Do not combine credential or Filesystem registry directories manually.

## Update environment variables

Update automation to use the following environment variable names:

| `tdc` v0.1.x variable | `ti` variable |
| --- | --- |
| `TDC_PROFILE` | `TI_PROFILE` |
| `TDC_REGION_CODE` | `TI_REGION_CODE` |
| `TDC_PUBLIC_KEY` | `TIDB_CLOUD_PUBLIC_KEY` |
| `TDC_PRIVATE_KEY` | `TIDB_CLOUD_PRIVATE_KEY` |
| `TDC_FS_TOKEN` | `TI_FS_TOKEN` |
| `TDC_FS_FILE_SYSTEM_ID` | `TI_FS_FILE_SYSTEM_ID` |
| `TDC_LOGGING` | `TI_LOGGING` |
| `TDC_TELEMETRY` | `TI_TELEMETRY` |
| `TDC_TELEMETRY_TAG` | `TI_TELEMETRY_TAG` |
| `TDC_TELEMETRY_EXTRA` | `TI_TELEMETRY_EXTRA` |
| `TDC_VAULT_TOKEN` | `TI_VAULT_TOKEN` |
| `TDC_INSTALL_DIR` | `TI_INSTALL_DIR` |

During the v0.2.x transition, `ti` accepts a legacy `TDC_*` environment variable only when the corresponding new variable is not set. If both forms are set to different values, the command fails before changing local or remote state. Support for legacy `TDC_*` variables is removed in v0.3.0.

## What's next

- [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md)
- [Manage TiDB Cloud Filesystem](/ai/ti/guides/manage-filesystems-via-cli.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
