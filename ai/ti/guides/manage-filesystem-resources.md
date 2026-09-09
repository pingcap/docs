---
title: Manage TiDB Cloud Filesystem Resources
summary: Learn how to safely create, inspect, check, select, and delete TiDB Cloud Filesystem resources by using TiDB Cloud CLI.
---

# Manage TiDB Cloud Filesystem Resources

Use `ti fs` to provision TiDB Cloud Filesystem resources and inspect their remote metadata and access status.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Configure a profile with TiDB Cloud API credentials.
- Install `jq`, or use another JSON processor to capture command output safely.

## Create a Filesystem

Create a Filesystem, wait until data-plane access is ready, and save the returned ID and one-time owner token in a file that is not world-readable:

```shell
umask 077
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait > ./filesystem.json

export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

The JSON response includes `fs_token` only once. Store it in a secret manager, and then delete `filesystem.json`. Do not put credentials, connection strings, private paths, or personal data in Filesystem labels.

## List and inspect Filesystems

List the Filesystems available in the effective region:

```shell
ti fs list-file-systems --output text
```

Read authoritative metadata for one Filesystem:

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

When you can access more than one Filesystem, pass `--file-system-id` explicitly or set `TI_FS_FILE_SYSTEM_ID`. The CLI does not infer a Filesystem from the number of locally stored credentials.

## Check access

Verify resource selection, endpoint resolution, credentials, and companion access:

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

## Delete a Filesystem

Delete a Filesystem by explicit ID:

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Filesystem deletion is asynchronous. The CLI removes a matching local credential after the service accepts the request.

## What's next

- [Manage TiDB Cloud Filesystem Tokens](/ai/ti/guides/manage-filesystem-tokens.md)
- [Work with TiDB Cloud Filesystem Data](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
