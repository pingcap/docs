---
title: TiDB Cloud CLI Release Notes
summary: Learn about TiDB Cloud CLI releases, including new features, improvements, bug fixes, and compatibility changes.
---

# TiDB Cloud CLI Release Notes

This page lists the release notes of [TiDB Cloud CLI](/ai/ti/ti-overview.md) in reverse chronological order. Dates are the GitHub release publication dates in UTC.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

Versions before v0.2.0 used the executable name `tdc`. These versions belong to the same product's release history; their entries retain the command names and environment variables used at the time. For current command syntax, see [TiDB Cloud CLI Command Reference](/ai/ti/reference/ti-cli-reference.md).

## Upgrade TiDB Cloud CLI

For an existing installer-managed `ti` installation, check for updates with `ti update --check`, then run `ti update`. Unmount active Filesystem and Vault mounts before updating the CLI and its bundled mount runtime. For installation and update instructions, see [Install, Configure, and Update TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).

If you use `tdc` v0.1.x, install `ti` directly instead of using `tdc update`. Read [Migrate from tdc to TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md) before upgrading.

## September 9, 2026

### v0.2.4

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.2.4)

**New features**

- Add `ti fs fork-layer`, `ti fs list-layer-chain`, and `ti fs delete-layer` to create independent copy-on-write workspaces, inspect their ancestry, and abandon unwanted layers.
- Add `--layer-ref` and `--checkpoint-id` to `ti fs mount-file-system`. You can mount a writable layer or a read-only historical checkpoint to compare workspace versions. These mounts require FUSE; WebDAV does not support them. For more information, see [Manage Filesystem Layers and Checkpoints](/ai/ti/guides/manage-filesystem-layers.md).
- Add commands to inspect and configure optional Filesystem image, audio, video, and embedding providers. Provider secrets are accepted only through `TI_FS_AI_PROVIDER_API_KEY` and are not persisted or printed by the CLI. Filesystem inventory also includes media quota fields returned by the service. For more information, see [Configure Filesystem AI Providers](/ai/ti/guides/configure-filesystem-ai-providers.md).

**Improvements**

- When Filesystem creation fails with a supported free-plan quota error, show guidance to add a payment method in TiDB Cloud, including a link to the billing page.
- When TiDB Cloud API keys are missing, include the API key creation link alongside the existing configuration and environment-variable instructions.
- Clarify that Filesystem deletion and token generation, inventory, enable, disable, and delete operations require TiDB Cloud API keys. An FS token alone does not authorize these administrative operations. Scoped-token generation and token refresh continue to use FS tokens.

**Compatibility changes**

- Remove the public `--foreground` flag from `ti fs mount-file-system`, its `mount` alias, and `ti fs-vault mount-vault`. Mount commands wait for readiness and return while the mount runtime continues in the background. Remove the flag from existing scripts and use the corresponding unmount command when finished.

## August 17, 2026

### v0.2.3

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.2.3)

**New features**

- Use the TiDB Cloud Filesystem tenant API for Filesystem creation, listing, inspection, and deletion. Creation accepts an optional display name and labels. Listing supports display-name and exact-label filters, and inventory includes status, labels, quota usage, and local-token availability without exposing token plaintext. Resource selection continues to use the immutable Filesystem ID. For more information, see [Manage Filesystem Resources](/ai/ti/guides/manage-filesystem-resources.md).

**Improvements**

- Include endpoint mappings for `aws-us-east-1`, `aws-ap-southeast-1`, `aws-us-west-2`, and `alicloud-ap-southeast-1` in the CLI. Runtime commands and installers no longer download a separate Filesystem region manifest. For more information, see [Supported regions](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).
- Use `alicloud-ap-southeast-1` as the canonical Alibaba Cloud region code while retaining compatibility with local credentials using `ali-ap-southeast-1`.
- Simplify successful background mount output by removing raw mount-runtime startup messages and misleading unmount guidance. Failed mounts retain their diagnostic log path.
- Shorten installer output and correct wording and spacing errors in command help.

## August 14, 2026

### v0.2.2

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.2.2)

**New features**

- Add Filesystem token generation, metadata listing, enable, disable, delete, and refresh commands. A Filesystem can have multiple tokens for separate machines, CI jobs, and agent sandboxes. Token plaintext is returned only on generation or refresh, not by listing.
- Add scoped-token generation from an owner token. Scoped tokens restrict access to selected paths and operations. Both owner and scoped tokens work with `TI_FS_TOKEN` and `--fs-token`; scoped tokens can refresh themselves but cannot generate child tokens or administer token inventory.
- Add explicit local token selection with `--store-locally` and checks that prevent invalidating tokens used by known active local mounts. Token authorization changes can take several seconds to propagate. For more information, see [Manage Filesystem Tokens](/ai/ti/guides/manage-filesystem-tokens.md).

**Bug fixes**

- Fix structured commands, including `ti fs list-file-systems`, returning JSON when `--output text` is requested. Structured text output uses tables or key-value fields, and queried scalar lists render one value per line.

## August 11, 2026

### v0.2.1

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.2.1)

**New features**

- Read Filesystem inventory from the service using TiDB Cloud API keys instead of listing only locally registered resources. Local credentials are indexed by the server-assigned Filesystem ID.
- Add `ti fs import-file-system-token` to import an existing owner token on another machine. Data-access and mount commands can also infer the Filesystem ID from a supplied token, so a clean sandbox needs only `TI_FS_TOKEN` and `TI_REGION_CODE`. For more information, see [Use TiDB Cloud Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md).

**Compatibility changes**

- Replace client-defined Filesystem names with server-assigned IDs. Update explicit resource selection to `--file-system-id` or `TI_FS_FILE_SYSTEM_ID`. Complete legacy name-keyed credentials migrate to the ID-keyed store without deleting their source records.
- Remove `--project-id`, saved default-project selection, and `ti organization list-projects`. TiDB Cloud chooses the default project; project metadata returned by the API remains unchanged in command output. Existing profile `project_id` values are ignored and removed when that profile is configured again.
- Make `ti configure` validate and save local input without calling TiDB Cloud or discovering a project. API authentication and authorization errors are reported when a subsequent command accesses the service.

## August 10, 2026

### v0.2.0

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.2.0)

**Compatibility changes**

- Rename the executable from `tdc` to `ti`, move the repository to `tidbcloud/ti-cli`, and use `~/.ti` for local state. There is no `tdc` command alias, and `tdc update` cannot perform this upgrade.
- Use `TI_*` environment variables and `TIDB_CLOUD_PUBLIC_KEY` / `TIDB_CLOUD_PRIVATE_KEY`. Legacy variables are temporarily accepted when their replacements are absent; conflicting old and new values cause an error.
- Migrate durable local state from `~/.tdc` to `~/.ti`, including profiles, credentials, preferences, and anonymous telemetry identity. The source directory is preserved. Independent state in both locations causes an explicit migration conflict instead of an automatic merge or overwrite. For instructions, see [Migrate from tdc to TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md).
- Require `--db-cluster-type starter` for DB commands that do not require an existing instance ID, including creation and listing. ID-based commands discover the instance's service plan and reject unsupported products before performing the requested operation. This removes the default type introduced in v0.1.5.

**Improvements**

- Restrict `ti db list-db-clusters --db-cluster-type starter` to verified Starter instances in the effective provider and region. Filtered pagination fills the requested page incrementally without loading the entire account inventory. For more information, see [Manage TiDB Cloud Starter Instances](/ai/ti/guides/manage-starter-instances.md).

## August 6, 2026

### v0.1.7

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.7)

**New features**

- Add optional `TDC_TELEMETRY_TAG` and `TDC_TELEMETRY_EXTRA` environment variables for segmenting anonymous usage by integration. The CLI bounds the tag length and JSON payload size and does not persist these values locally. Do not include secrets or personal data. For their current `TI_*` equivalents, see [Anonymous telemetry](/ai/ti/reference/ti-configuration-and-credentials.md#anonymous-telemetry).

## July 29, 2026

### v0.1.6

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.6)

**New features**

- Add best-effort anonymous command-completion telemetry to release builds. Events contain command and flag names without values, exit and error codes, duration, region, version, OS, and architecture. Telemetry does not collect credentials, SQL text, file contents, paths, or command output, and cannot change a command's output or exit status.
- Support opting out with `TDC_TELEMETRY=off` or `[telemetry] enabled = false` in `~/.tdc/.preferences`. Help, version, commandless usage, and update commands do not send events. Telemetry is disabled by default in development and CI environments.

## July 22, 2026

### v0.1.5

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.5)

**Improvements**

- Default `tdc db create-db-cluster` to the Starter type while continuing to reject unsupported explicit types. This historical default is removed in v0.2.0, which requires `--db-cluster-type starter`.
- Refine command help descriptions and preview labels across Filesystem commands.

## July 21, 2026

### v0.1.4

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.4)

**Improvements**

- Show a compact two-level usage synopsis when `tdc` is run without a command. In help output, list required flags first, mark them with `(required)`, and enclose value types in angle brackets.
- Remove the repeated Filesystem-name confirmation flag from Filesystem deletion.
- Clarify the configured region as the default region and separate human-readable errors from preceding terminal output with a blank line.

## July 18, 2026

### v0.1.3

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.3)

**New features**

- Add a consistent `--wait` flag to Starter instance creation, branch creation, instance deletion, and Filesystem creation. Creation waits for an `ACTIVE` instance or branch, or for a readable Filesystem root. Instance deletion waits for `DELETED` or confirmed inaccessibility. Timeouts and interruptions do not delete or recreate an accepted resource.

**Bug fixes**

- Report accepted Filesystem deletion as `deleting`, not `deleted`. Filesystem deletion remains asynchronous and does not support `--wait`.

## July 17, 2026

### v0.1.2

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.2)

**Maintenance**

- Remove macOS metadata files from the release source tree. This release does not introduce new commands or change the user-owned update workflow.

### v0.1.1

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.1)

**New features**

- Add configuration-free Filesystem access for ephemeral environments. At this version, data-access workflows use `TDC_FS_TOKEN`, `TDC_REGION_CODE`, and `TDC_FS_FILE_SYSTEM_NAME` without running `tdc configure` or supplying TiDB Cloud API keys. The Filesystem-name requirement is later removed in v0.2.1.

**Improvements**

- Install the CLI and its Filesystem companion under the user-owned `~/.tdc/bin` directory on macOS and Linux, or `%USERPROFILE%\.tdc\bin` on Windows. Installation does not require `sudo` or system-directory symlinks; users add the directory to `PATH` themselves.
- Update both binaries with `tdc update` without requiring `--yes` or elevated privileges.

### v0.1.0

[GitHub release](https://github.com/tidbcloud/ti-cli/releases/tag/v0.1.0)

**New features**

- Introduce the initial preview of TiDB Cloud CLI, then named `tdc`, for users, scripts, and AI agents.
- Support local profiles, Starter instance and branch lifecycle management, SQL access roles, connection strings, and SQL execution.
- Support Filesystem resource management, file operations, local mounts, Git workspaces, journals, and vault workflows.
- Provide JSON and text output, JMESPath `--query`, and `--dry-run` on supported mutating control-plane commands.
