---
title: Manage TiDB Cloud Filesystem Resources
summary: Learn how to safely create, inspect, check, select, and delete TiDB Cloud Filesystem resources by using TiDB Cloud CLI.
---

# Manage TiDB Cloud Filesystem Resources

TiDB Cloud Filesystem is a serverless distributed file system designed for AI agents and automation workloads. It provides a persistent, shareable file namespace that remains available independently of the local machine, sandbox, or CI runner that accesses it.

You can access files directly through TiDB Cloud CLI commands or mount a Filesystem into a supported environment and work with it like a local file system. This makes it useful for preserving agent state, sharing files across isolated environments, handing off CI artifacts, and maintaining reusable workspaces.

This document describes how to use [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) to create, inspect, select, and delete Filesystem resources.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Configure a profile with TiDB Cloud API credentials.
- Install `jq`, or use another JSON processor to capture command output safely.

## Create a Filesystem

Create a Filesystem and save the returned ID and one-time owner token in a file that is not world-readable. The `--wait` flag tells the CLI to poll until data-plane access is ready before returning:

```shell
umask 077
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait > ./filesystem.json

export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

> **Warning:**
>
> The JSON response includes `fs_token` only once. The CLI also stores this token in its local credential directory automatically. However, if the local storage is lost, you cannot retrieve the token again. Store a backup copy in a secret manager, and then delete `filesystem.json`.

> **Note:**
>
> Do not put credentials, connection strings, private paths, or personal data in Filesystem labels.

## List and inspect Filesystems

List the Filesystems available in the effective region:

```shell
ti fs list-file-systems --output text
```

Read authoritative metadata for one Filesystem:

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

If you have access to more than one Filesystem, pass `--file-system-id` explicitly or set the `TI_FS_FILE_SYSTEM_ID` environment variable. The CLI does not automatically select a Filesystem for you.

## Check access

Verify resource selection, endpoint resolution, credentials, and companion access:

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

## Delete a Filesystem

> **Warning:**
>
> Before deleting a Filesystem, drain and unmount any active local mounts for it. The CLI does not do this automatically.

Delete a Filesystem by explicit ID:

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Filesystem deletion is asynchronous. After the service accepts the request, the CLI reports the Filesystem status as `deleting` and removes the matching local credential. This output does not mean that remote deletion has finished.

## What's next

- [Manage TiDB Cloud Filesystem Tokens](/ai/ti/guides/manage-filesystem-tokens.md)
- [Work with TiDB Cloud Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
