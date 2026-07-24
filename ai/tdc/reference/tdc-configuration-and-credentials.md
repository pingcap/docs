---
title: tdc Configuration and Credentials
summary: Reference tdc profiles, environment and flag precedence, local state paths, Filesystem registry, SQL credentials, mount locators, and operation logs.
---

# tdc Configuration and Credentials

tdc stores all product-owned local state under `~/.tdc/` and separates non-sensitive configuration from credentials.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Main files

```toml
# ~/.tdc/config
[default]
region_code = "aws-us-east-1"
project_id = "..."
fs_default_file_system_name = "workspace"

[logging]
enabled = true
max_file_mb = 10
max_files = 5
```

```toml
# ~/.tdc/credentials
[default]
tdc_public_key = "..."
tdc_private_key = "..."
```

The credentials file uses owner-only permissions where the platform supports POSIX modes.

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

Both environment values are required together. tdc never mixes one environment half with one file half.

Placement selection is:

1. explicit global `--region`;
2. `TDC_REGION_CODE`;
3. profile `region_code`.

Command flags, environment inputs, saved configuration, and command defaults are resolved per field. Values can therefore come from different levels when they do not form an atomic pair such as the API key pair.

## Default Starter project

Starter create selects a project in this order:

1. explicit non-empty `--project-id`;
2. profile `project_id` discovered by `tdc configure`;
3. fail before sending the create request.

Other DB commands identify resources by cluster or branch ID and do not use `project_id`. Filesystem commands do not consume the DB project default.

## Filesystem resource registry

One profile can register multiple Filesystems. The main config stores only the optional default name. Resource state is isolated:

```text
~/.tdc/fs_resources/<profile-key>/<resource-key>/config
~/.tdc/fs_resources/<profile-key>/<resource-key>/credentials
```

The resource config contains the stored Filesystem name, tenant ID, cloud provider, region code, and creation time. The credentials file contains only the owner `api_key` and uses owner-only permissions.

Resource selection is:

1. explicit `--file-system-name`;
2. `TDC_FS_FILE_SYSTEM_NAME`;
3. profile `fs_default_file_system_name`;
4. the only registered resource;
5. fail as missing or ambiguous.

FS owner credential selection for remote `fs`, `fs-git`, `fs-journal`, and owner `fs-vault` operations is:

1. explicit `--fs-token`;
2. `TDC_FS_TOKEN`;
3. selected resource credential.

Prefer `TDC_FS_TOKEN` over a flag because flags can remain in shell history or process listings.

## Config-free Filesystem inputs

A clean sandbox can use:

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
```

These values form an in-memory namespace only. tdc does not write them to `~/.tdc/`. Provisioning and deletion still require TiDB Cloud API credentials; deletion also requires the local resource registration.

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

Do not edit this state or a standalone `~/.drive9` configuration for tdc workflows.

A successful background FS or vault mount writes a non-secret locator:

```text
~/.tdc/mounts/<mount-hash>.locator.json
```

The locator records enough placement and companion-home information for drain and unmount from the same `HOME`. It does not contain the FS token. Successful unmount removes it.

## Operation logs

tdc writes redacted local JSON Lines events to:

```text
~/.tdc/logs/tdc.jsonl
```

This log is local audit/debug data, not telemetry. It can include command names, flag names, profile and region, duration, exit and stable error codes, HTTP method/status, operation, and request ID. It excludes flag values, SQL, file paths and contents, payloads, connection strings, and credentials.

Disable it for one process:

```bash
TDC_LOGGING=off tdc db list-db-clusters
```

Or configure:

```toml
[logging]
enabled = false
```

Environment values `off`, `false`, `0`, and `no` disable logging; `on`, `true`, `1`, and `yes` enable it. Environment takes precedence over config.

## Sensitive values

Treat these as secrets:

- TiDB Cloud API private key and public-key pair;
- FS owner token;
- DB SQL usernames, passwords, and connection strings;
- delegated vault tokens and secret values.

Do not put them in source control, tickets, logs, command examples, or unprotected shell history.

## Related documentation

- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)
