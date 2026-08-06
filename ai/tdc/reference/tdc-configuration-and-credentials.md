---
title: TiDB Cloud CLI Configuration and Credentials
summary: Reference TiDB Cloud CLI profiles, precedence rules, local state paths, Filesystem credentials, SQL credentials, mount locators, and operation logs.
---

# TiDB Cloud CLI Configuration and Credentials

`tdc` stores all product-owned local state under `~/.tdc/` and separates non-sensitive configuration from credentials.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `tdc` — is currently in preview. Its features and command-line interface might change without prior notice.

## Main files

```toml
# ~/.tdc/config
[default]
region_code = "aws-us-east-1"
project_id = "..."
```

```toml
# ~/.tdc/credentials
[default]
tdc_public_key = "..."
tdc_private_key = "..."
```

The credentials file uses owner-only permissions where the platform supports POSIX modes.

Global preferences are separate from profiles and credentials:

```toml
# ~/.tdc/.preferences
schema_version = 1

[logging]
enabled = true
max_file_mb = 10
max_files = 5

[telemetry]
enabled = false
```

The dot-prefixed preferences file is optional, hidden from ordinary directory listings, and applies to every profile. Fresh installs and `tdc configure` do not create it. Reading a user-created file does not rewrite its permissions, comments, or formatting.

## Profile selection

The profile namespace is selected in this order:

1. explicit `--profile`;
2. `TDC_PROFILE`;
3. `default`.

An explicit empty profile is invalid.

## TiDB Cloud API credentials

Credential selection is:

1. `TDC_PUBLIC_KEY` and `TDC_PRIVATE_KEY`, when either is set;
2. the selected section of `~/.tdc/credentials`.

Both environment values are required together. `tdc` never mixes one environment half with one file half.

Placement selection is:

1. explicit global `--region`;
2. `TDC_REGION_CODE`;
3. profile `region_code`.

Command flags, environment inputs, saved configuration, and command defaults are resolved per field. Values can therefore come from different levels when they do not form an atomic pair such as the API key pair.

## Default Starter project

Starter create selects a project in this order:

1. explicit non-empty `--project-id`;
2. profile `project_id` discovered by `tdc configure`;
3. omit the project label and let TiDB Cloud select the account's default project.

An explicitly empty `--project-id` is invalid. When no project ID is available, `tdc` omits the project label entirely rather than sending an empty value.

Other DB commands identify resources by cluster or branch ID and do not use `project_id`. Filesystem commands do not consume the DB project default.

## Filesystem credentials and remote inventory

One profile can access multiple Filesystems. Drive9's remote inventory is authoritative for resource existence and status. Local state stores only credentials and their routing hint:

```text
~/.tdc/fs_credentials/<profile-key>/<file-system-id-key>/credentials
```

The credential contains the server-assigned file system ID, canonical region code, and owner `api_key`, and uses owner-only permissions. `tdc fs list-file-systems` reads remote resources and joins only the non-secret `has_local_token` hint.

Resource selection is:

1. explicit `--file-system-id`;
2. `TDC_FS_FILE_SYSTEM_ID`;
3. derive the ID from an explicitly supplied FS token;
4. otherwise fail with `fs.missing_file_system_id`.

`tdc` never infers a Filesystem from a saved default or from the number of local credentials. Use `--file-system-id` for one command or `TDC_FS_FILE_SYSTEM_ID` for a shell, sandbox, or automation environment.

FS owner credential selection for remote `fs`, `fs-git`, `fs-journal`, and owner `fs-vault` operations is:

1. explicit `--fs-token`;
2. `TDC_FS_TOKEN`;
3. selected resource credential.

Prefer `TDC_FS_TOKEN` over a flag because flags can remain in shell history or process listings.

## Config-free Filesystem inputs

A clean sandbox needs only:

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
```

These values form an in-memory namespace only. `tdc` derives the ID from the token and does not write either value to `~/.tdc/`. `TDC_FS_FILE_SYSTEM_ID` is optional and, when present, must match the token. Remote list, describe, provisioning, and deletion require TiDB Cloud API credentials; deletion does not require a local FS token.

## DB SQL credentials

Generated SQL credentials are cluster-scoped:

```text
~/.tdc/db_users/<cluster-id>/credentials
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

`tdc db create-db-sql-users` creates or repairs these stable users. They are not stored in the main credentials file.

## Companion state and mount locators

Each registered Filesystem has an isolated companion home:

```text
~/.tdc/drive9-home/<profile-key>/<resource-key>/
```

Do not edit this state or a standalone `~/.drive9` configuration for `tdc` workflows.

A successful background FS or vault mount writes a non-secret locator:

```text
~/.tdc/mounts/<mount-hash>.locator.json
```

The locator records the placement and companion-home information required for drain and unmount from the same `HOME`. It does not contain the FS token. Successful unmount removes it.

## Operation logs

`tdc` writes redacted local JSON Lines events to:

```text
~/.tdc/logs/tdc.jsonl
```

This log is local audit/debug data, not telemetry. It can include command names, flag names, profile and region, duration, exit and stable error codes, HTTP method/status, operation, and request ID. It excludes flag values, SQL, file paths and contents, payloads, connection strings, and credentials.

Disable it for one process:

```bash
TDC_LOGGING=off tdc db list-db-clusters
```

Or create or edit `~/.tdc/.preferences`:

```toml
schema_version = 1

[logging]
enabled = false
```

Environment values `off`, `false`, `0`, and `no` disable logging; `on`, `true`, `1`, and `yes` enable it. Environment takes precedence over settings. Invalid settings disable operation logging without failing the requested command.

Existing installations that stored `[logging]` in `~/.tdc/config` migrate those values to `~/.tdc/.preferences` automatically. The migration preserves profiles and credentials. `tdc update` does not read or write settings, profiles, credentials, operation logs, or other state under `~/.tdc/`.

## Anonymous telemetry

Release builds send one best-effort completion event for eligible commands to the TiDB Cloud CLI telemetry service. The event contains the canonical command and explicitly supplied flag names, stable exit and error codes, duration, region, CLI version, OS, architecture, install source, and a random pseudonymous installation ID. It does not contain flag values, credentials, tokens, SQL text, file paths or contents, command output, API payloads, profile names, or cloud resource IDs.

Development builds and recognized CI environments default to disabled. Help, version, commandless usage, and every `tdc update` mode are always excluded. Disable telemetry persistently by adding the following global preference:

```toml
[telemetry]
enabled = false
```

Disable it for one process without changing the file:

```bash
TDC_TELEMETRY=off tdc db list-db-clusters
```

The TiDB Cloud CLI creates `~/.tdc/.telemetry-installation-id` lazily for the first eligible event and restricts it to the current user where POSIX permissions are available. Delete this file to reset the pseudonymous identity. Telemetry delivery is lossy and never changes command output, errors, or exit status.

An integration can attach explicit process-scoped metadata without changing a profile or command. `TDC_TELEMETRY_TAG` accepts a UTF-8 string up to 128 bytes. `TDC_TELEMETRY_EXTRA` accepts one complete JSON value up to 2 KiB after compaction. Invalid, prohibited, deeply nested, or oversized metadata is omitted without affecting the command. Do not include credentials, tokens, SQL, paths, personal data, profile names, or cloud resource IDs in either value:

```bash
TDC_TELEMETRY_TAG="e2b-preview" \
TDC_TELEMETRY_EXTRA='{"campaign":"launch","runtime":"e2b"}' \
tdc fs list-files --file-system-id <file-system-id> --path /
```

## Sensitive values

Treat these as secrets:

- TiDB Cloud API private key and public-key pair;
- FS owner token;
- DB SQL usernames, passwords, and connection strings;
- delegated vault tokens and secret values.

Do not put them in source control, tickets, logs, command examples, or unprotected shell history.

## Related documentation

- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
- [Troubleshoot TiDB Cloud CLI](/ai/tdc/reference/tdc-troubleshooting.md)
