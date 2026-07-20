---
title: tdc Concepts and Architecture
summary: Understand tdc profiles, regions, credentials, SQL roles, Filesystem resources, local state, and the bundled Drive9 companion.
---

# tdc Concepts and Architecture

This document explains the concepts needed to use tdc with TiDB Cloud Starter and TiDB Cloud Filesystem.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Command model

tdc uses service nouns and explicit operation names:

```text
tdc db create-db-cluster
tdc fs copy-file
tdc fs-git clone-git-workspace
```

The command tree is at most two levels. Long, descriptive command and flag names make intent explicit in logs and agent-generated commands. Commands are non-interactive except for `tdc configure`.

Structured commands return JSON by default. Use `--output text` for a terminal-oriented representation and `--query` for a JMESPath projection.

## Profiles and regions

A profile is a named local namespace containing TiDB Cloud placement, a default virtual project, and credentials. The default profile is named `default`; select another with `--profile`.

tdc represents placement with one canonical region code:

```text
aws-us-east-1
aws-ap-southeast-1
ali-ap-southeast-1
```

The prefix identifies the cloud provider. A global `--region` value overrides `TDC_REGION_CODE` and the profile region for one command without changing saved configuration.

During `tdc configure`, tdc calls the organization API and requires one accessible project with `type = "tidbx_virtual"`. It stores that project ID as the default for Starter cluster creation.

## Credential boundaries

tdc uses separate credentials for separate security boundaries:

| Credential | Purpose | Storage |
| --- | --- | --- |
| TiDB Cloud API public/private key | Organization, Starter control plane, Filesystem provisioning and deletion | `~/.tdc/credentials` |
| DB SQL username/password | SQL access to one Starter cluster | `~/.tdc/db_users/<cluster-id>/credentials` |
| Filesystem owner token | Filesystem data plane, mounts, Git, journal, and owner vault operations | Per-resource credentials under `~/.tdc/fs_resources/` or `TDC_FS_TOKEN` |
| Delegated vault token | Limited access to selected secret fields | `TDC_VAULT_TOKEN` or an explicit command input |

TiDB Cloud API keys are never reused as SQL passwords or Filesystem tokens.

## SQL roles

`tdc db create-db-sql-users` creates or repairs three stable users for a cluster:

- `read_only` for queries that must not modify data;
- `read_write` for normal application and agent work;
- `admin` for DDL and privilege administration.

Role selection is explicit with `--read-only`, `--read-write`, or `--admin`. Read-write is the default when no role flag is supplied.

## One profile, multiple Filesystems

One profile can register multiple Filesystem resources. Each resource has an isolated config file and credential file. Select a resource in this order:

1. `--file-system-name`;
2. `TDC_FS_FILE_SYSTEM_NAME`;
3. the profile's default Filesystem;
4. the only registered Filesystem, when exactly one exists.

If multiple resources exist and none is selected, tdc fails instead of guessing. Use `tdc fs set-default-file-system` to choose a default.

## Config-free sandbox access

A clean agent sandbox does not need `tdc configure` or TiDB Cloud API keys to use an existing Filesystem. Supply:

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
```

tdc resolves these values into an in-memory profile namespace. It does not write an `[env]` profile or persist the token.

## Local state

All tdc-owned state is under `~/.tdc/`:

| Path | Contents |
| --- | --- |
| `config` | Non-sensitive profile, default project, and logging settings |
| `credentials` | TiDB Cloud API keys |
| `fs_resources/` | Per-profile, per-Filesystem metadata and owner credentials |
| `db_users/` | Cluster-scoped SQL credentials |
| `mounts/` | Non-secret locators for active background mounts |
| `logs/tdc.jsonl` | Redacted local operation log |
| `bin/` | Installed `tdc` and `tdc-drive9` binaries |

Operation logging is local and is not telemetry. Set `TDC_LOGGING=off` to disable it for one process.

## tdc and the Drive9 companion

tdc installs [Drive9](https://github.com/mem9-ai/drive9) as the private companion name `tdc-drive9`.

tdc owns:

- profile, credential, region, and Filesystem selection;
- TiDB Cloud control-plane calls;
- JSON/text output, queries, errors, and local logging;
- translation from the tdc command surface to the companion.

The companion owns:

- Filesystem reads, writes, metadata, links, search, and layers;
- FUSE and WebDAV mount processes, caches, drain, and unmount;
- pack/unpack, Git workspace, journal, and vault semantics.

A background mount leaves a long-running `tdc-drive9 mount --foreground` process. `tdc fs unmount-file-system` gracefully flushes pending FUSE work and stops that process. `tdc fs drain-file-system` provides an explicit, reportable durability barrier while leaving a FUSE mount active so it can accept later writes. Do not abruptly terminate a machine with unflushed writes or local-only overlay data that you need to keep.

## What's next

- [Install, Configure, and Update tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
