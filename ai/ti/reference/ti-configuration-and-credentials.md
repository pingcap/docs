---
title: TiDB Cloud CLI Configuration and Credentials
summary: Reference TiDB Cloud CLI profiles, precedence rules, local state paths, Filesystem registry, SQL credentials, mount locators, and operation logs.
---

# TiDB Cloud CLI Configuration and Credentials

`ti` stores all product-owned local state under `~/.ti/` and separates non-sensitive configuration from credentials.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Main files

```toml
# ~/.ti/config
[default]
region_code = "aws-us-east-1"
project_id = "..."
```

```toml
# ~/.ti/credentials
[default]
tidb_cloud_public_key = "..."
tidb_cloud_private_key = "..."
```

The credentials file uses owner-only permissions where the platform supports POSIX modes.

Global preferences are separate from profiles and credentials:

```toml
# ~/.ti/.preferences
schema_version = 1

[logging]
enabled = true
max_file_mb = 10
max_files = 5

[telemetry]
enabled = false
```

The dot-prefixed preferences file is optional, hidden from ordinary directory listings, and applies to every profile. Fresh installs and `ti configure` do not create it. Reading a user-created file does not rewrite its permissions, comments, or formatting.

## Profile selection

The profile namespace is selected in this order:

1. explicit `--profile`;
2. `TI_PROFILE`;
3. `default`.

An explicit empty profile is invalid.

## TiDB Cloud API credentials

Credential selection is:

1. `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY`, when either is set;
2. the selected section of `~/.ti/credentials`.

Both environment values are required together. `ti` never mixes one environment half with one file half.

During the v0.2.x transition, the CLI accepts the corresponding legacy `TDC_*` environment variable only when the canonical variable is absent. If both are set to different values, the command fails before changing local or remote state. New configuration writes only the canonical names shown on this page.

Placement selection is:

1. explicit global `--region`;
2. `TI_REGION_CODE`;
3. profile `region_code`.

Command flags, environment inputs, saved configuration, and command defaults are resolved per field. Values can therefore come from different levels when they do not form an atomic pair such as the API key pair.

## Default Starter project

Starter create selects a project in this order:

1. explicit non-empty `--project-id`;
2. profile `project_id` discovered by `ti configure`;
3. omit the project label and let TiDB Cloud select the account's default project.

An explicitly empty `--project-id` is invalid. When no project ID is available, `ti` omits the project label entirely rather than sending an empty value.

Other DB commands identify resources by cluster or branch ID and do not use `project_id`. Filesystem commands do not consume the DB project default.

## Filesystem resource registry

One profile can register multiple Filesystems. Resource state is isolated from the main profile configuration:

```text
~/.ti/fs_resources/<profile-key>/<resource-key>/config
~/.ti/fs_resources/<profile-key>/<resource-key>/credentials
```

The resource config contains the stored Filesystem name, tenant ID, cloud provider, region code, and creation time. The credentials file contains only the owner `api_key` and uses owner-only permissions.

Resource selection is:

1. explicit `--file-system-name`;
2. `TI_FS_FILE_SYSTEM_NAME`;
3. fail with `fs.missing_file_system_name`.

`ti` never infers a Filesystem from a saved default or from the number of registered resources. Use `--file-system-name` for one command or `TI_FS_FILE_SYSTEM_NAME` for a shell, sandbox, or automation environment.

FS owner credential selection for remote `fs`, `fs-git`, `fs-journal`, and owner `fs-vault` operations is:

1. explicit `--fs-token`;
2. `TI_FS_TOKEN`;
3. selected resource credential.

Prefer `TI_FS_TOKEN` over a flag because flags can remain in shell history or process listings.

## Config-free Filesystem inputs

A clean sandbox can use:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
export TI_FS_FILE_SYSTEM_NAME="workspace"
```

These values form an in-memory namespace only. `ti` does not write them to `~/.ti/`. Provisioning and deletion still require TiDB Cloud API credentials; deletion also requires the local resource registration.

## DB SQL credentials

Generated SQL credentials are cluster-scoped:

```text
~/.ti/db_users/<cluster-id>/credentials
```

```toml
[read_only]
username = "..."
password = "..."

[read_write]
username = "..."
password = "..."

[admin]
username = "..."
password = "..."
```

`ti db create-db-sql-users` creates or repairs these stable users. They are not stored in the main credentials file.

## Companion state and mount locators

Each registered Filesystem has an isolated companion home:

```text
~/.ti/drive9-home/<profile-key>/<resource-key>/
```

Do not edit this state or a standalone `~/.drive9` configuration for `ti` workflows.

A successful background FS or vault mount writes a non-secret locator:

```text
~/.ti/mounts/<mount-hash>.locator.json
```

The locator records the placement and companion-home information required for drain and unmount from the same `HOME`. It does not contain the FS token. Successful unmount removes it.

## Operation logs

`ti` writes redacted local JSON Lines events to:

```text
~/.ti/logs/ti.jsonl
```

This log is local audit/debug data, not telemetry. It can include command names, flag names, profile and region, duration, exit and stable error codes, HTTP method/status, operation, and request ID. It excludes flag values, SQL, file paths and contents, payloads, connection strings, and credentials.

Disable it for one process:

```bash
TI_LOGGING=off ti db list-db-clusters --db-cluster-type starter
```

Or create or edit `~/.ti/.preferences`:

```toml
schema_version = 1

[logging]
enabled = false
```

Environment values `off`, `false`, `0`, and `no` disable logging; `on`, `true`, `1`, and `yes` enable it. Environment takes precedence over settings. Invalid settings disable operation logging without failing the requested command.

Existing installations that stored `[logging]` in `~/.ti/config` migrate those values to `~/.ti/.preferences` automatically. The migration preserves profiles and credentials. `ti update` does not read or write settings, profiles, credentials, operation logs, or other state under `~/.ti/`.

## Anonymous telemetry

Release builds send one best-effort completion event for eligible commands to the TiDB Cloud CLI telemetry service. The event contains the canonical command and explicitly supplied flag names, stable exit and error codes, duration, region, CLI version, OS, architecture, install source, and a random pseudonymous installation ID. It does not contain flag values, credentials, tokens, SQL text, file paths or contents, command output, API payloads, profile names, or cloud resource IDs.

Development builds and recognized CI environments default to disabled. Help, version, commandless usage, and every `ti update` mode are always excluded. Disable telemetry persistently by adding the following global preference:

```toml
[telemetry]
enabled = false
```

Disable it for one process without changing the file:

```bash
TI_TELEMETRY=off ti db list-db-clusters --db-cluster-type starter
```

The TiDB Cloud CLI creates `~/.ti/.telemetry-installation-id` lazily for the first eligible event and restricts it to the current user where POSIX permissions are available. Delete this file to reset the pseudonymous identity. Telemetry delivery is lossy and never changes command output, errors, or exit status.

An integration can attach explicit process-scoped metadata without changing a profile or command. `TI_TELEMETRY_TAG` accepts a UTF-8 string up to 128 bytes. `TI_TELEMETRY_EXTRA` accepts one complete JSON value up to 2 KiB after compaction. Invalid, prohibited, deeply nested, or oversized metadata is omitted without affecting the command. Do not include credentials, tokens, SQL, paths, personal data, profile names, or cloud resource IDs in either value:

```bash
TI_TELEMETRY_TAG="e2b-preview" \
TI_TELEMETRY_EXTRA='{"campaign":"launch","runtime":"e2b"}' \
ti fs list-files --file-system-name workspace --path /
```

## Sensitive values

Treat these as secrets:

- TiDB Cloud API private key and public-key pair;
- FS owner token;
- DB SQL usernames, passwords, and connection strings;
- delegated vault tokens and secret values.

Do not put them in source control, tickets, logs, command examples, or unprotected shell history.

## Related documentation

- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)
