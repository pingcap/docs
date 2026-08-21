---
title: TiDB Cloud CLI Configuration and Credentials
summary: Reference TiDB Cloud CLI profiles, precedence rules, local state paths, Filesystem credentials, SQL credentials, mount locators, and operation logs.
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
```

```toml
# ~/.ti/credentials
[default]
ti_public_key = "..."
ti_private_key = "..."
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

1. `TI_PUBLIC_KEY` and `TI_PRIVATE_KEY`, when either is set;
2. the selected section of `~/.ti/credentials`.

Both environment values are required together. `ti` never mixes one environment half with one file half.

Placement selection is:

1. explicit global `--region`;
2. `TI_REGION_CODE`;
3. profile `region_code`.

Command flags, environment inputs, saved configuration, and command defaults are resolved per field. Values can therefore come from different levels when they do not form an atomic pair such as the API key pair.

## Starter project placement

The TiDB Cloud CLI does not accept or store a project selector. Starter cluster creation omits project placement and lets TiDB Cloud select its server-side default project. Project fields and labels returned by TiDB Cloud remain visible as resource metadata and are not reused for later requests.

## Filesystem credentials and remote inventory

One profile can access multiple Filesystems. Drive9's remote inventory is authoritative for resource existence and status. Local state stores only credentials and their routing hint:

```text
~/.ti/fs_credentials/<profile-key>/<file-system-id-key>/credentials
```

The credential contains the server-assigned file system ID, canonical region code, selected `api_key`, and optional authoritative token metadata, and uses owner-only permissions. `ti fs list-file-systems` reads remote resources and joins only the non-secret `has_local_token` hint.

One remote Filesystem can have multiple tokens, but each profile stores at most one selected token per Filesystem. The local store is an operational selection, not a replica of remote token inventory. Credentials created by provisioning or older imports might not contain `token_id`, `scope_kind`, `token_name`, `expires_at`, or `scopes`; they remain valid for data-plane use, and `ti` does not guess missing metadata from token-list rows.

`ti fs generate-file-system-token` does not change the selected credential unless `--store-locally` is set. `--replace` changes only the local selection and leaves the previous remote token active. A refresh sourced from the local credential atomically replaces it. A refresh sourced from a flag or `TI_FS_TOKEN` returns the replacement plaintext without writing local state.

`ti fs generate-file-system-scoped-token` accepts only an owner token and can store its authoritative path scopes locally. The token JWT itself contains the Filesystem ID but not the token kind, token ID, or scopes. Therefore, an explicit or environment token is passed to the service for authorization instead of being classified locally. `TI_FS_TOKEN` can contain either an owner token or a scoped token; available operations depend on its server-side capability.

Owner FS tokens authorize Filesystem data access and token inventory or lifecycle operations. They do not authorize TiDB Cloud Filesystem resource creation, listing, description, or deletion, and they cannot generate another owner token. Those operations require TiDB Cloud API credentials. `ti fs delete-file-system` additionally requires an explicit `--file-system-id`; the ID embedded in `TI_FS_TOKEN` is never used to select a Filesystem for deletion.

Resource selection is:

1. explicit `--file-system-id`;
2. `TI_FS_FILE_SYSTEM_ID`;
3. derive the ID from an explicitly supplied FS token;
4. otherwise fail with `fs.missing_file_system_id`.

`ti` never infers a Filesystem from a saved default or from the number of local credentials. Use `--file-system-id` for one command or `TI_FS_FILE_SYSTEM_ID` for a shell, sandbox, or automation environment.

FS owner credential selection for remote `fs`, `fs-git`, `fs-journal`, and owner `fs-vault` operations is:

1. explicit `--fs-token`;
2. `TI_FS_TOKEN`;
3. selected resource credential.

Prefer `TI_FS_TOKEN` over a flag because flags can remain in shell history or process listings.

## Config-free Filesystem inputs

A clean sandbox needs only:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
```

These values form an in-memory namespace only. `ti` derives the ID from the token and does not write either value to `~/.ti/`. `TI_FS_FILE_SYSTEM_ID` is optional and, when present, must match the token. Remote Filesystem inventory, description, provisioning, and deletion require TiDB Cloud API credentials. An FS token is neither required nor accepted as authorization for Filesystem deletion.

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
ti fs list-files --file-system-id <file-system-id> --path /
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
