---
title: Share a TiDB Cloud Filesystem Across Machines
summary: Create one Filesystem, securely access it from a second machine, and verify data-plane and mount visibility.
---

# Share a TiDB Cloud Filesystem Across Machines

This workflow gives users, automation, or agents on two machines one shared workspace. Use it when changes must remain visible from both machines without exchanging point-in-time copies through `scp` or archive uploads.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

Machine A creates the Filesystem and generates a separate owner token for machine B. Both machines then access the same remote namespace through data-plane commands or a mounted directory, so writes become visible through either interface after they are flushed. This provides shared-directory behavior without manual snapshot synchronization or object-storage-specific transfer logic.

| Participant | Credentials | Role in the workflow |
| --- | --- | --- |
| Machine A | Configured `ti` profile and its FS owner token | Creates and manages the Filesystem, writes initial data, and generates the token for machine B |
| Machine B | Its own FS owner token and the Filesystem region code | Accesses the Filesystem without TiDB Cloud API keys or a copied profile |
| TiDB Cloud Filesystem | Not applicable | Provides the shared remote namespace used by both machines |

Using a separate token for each machine lets you revoke machine B without interrupting machine A. Because both tokens grant owner access, transfer and store them as secrets.

## Prerequisites

- Machine A has configured `ti`.
- Both machines have `ti` installed.
- Machine A has `jq` installed.
- You have a secure secret-transfer channel.

## Step 1. Create the Filesystem on machine A

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs generate-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-name machine-b \
  --ttl 720h > ./machine-b-token.json

printf 'from machine A\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /shared/origin.txt
```

Transfer the `fs_token` from `machine-b-token.json` through a secret manager and communicate the canonical region code. Keep `FILE_SYSTEM_ID` on machine A for control-plane operations, then delete both JSON files after storing their tokens securely.

## Step 2. Configure machine B in memory

```bash
export TI_FS_TOKEN="<owner-token-from-secret-manager>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Set `TI_REGION_CODE` to the region where the Filesystem was created. No `ti configure` is required.

## Step 3. Verify direct visibility on machine B

```bash
ti fs read-file --path /shared/origin.txt
printf 'from machine B\n' | ti fs copy-file --from-stdin --to-remote /shared/second.txt
```

## Step 4. Verify mount and data-plane visibility

```bash
mkdir -p /path/to/shared-workspace
ti fs mount-file-system \
  --mount-path /path/to/shared-workspace

cat /path/to/shared-workspace/shared/origin.txt
printf 'written through mount\n' > /path/to/shared-workspace/shared/mounted.txt

# Graceful unmount flushes pending writes before the data-plane read.
ti fs unmount-file-system --mount-path /path/to/shared-workspace
ti fs read-file --path /shared/mounted.txt
```

The first read proves data-plane writes are visible through the mount. The final read proves mount writes are visible through the data plane after they are flushed.

## Cleanup

### On machine B

After the graceful unmount in Step 4, remove the credentials from the current shell:

```bash
unset TI_FS_TOKEN TI_REGION_CODE
```

### On machine A

```bash
rm -f ./filesystem.json ./machine-b-token.json

ti fs list-file-system-tokens --file-system-id "$FILE_SYSTEM_ID" --output text
ti fs delete-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --token-id "<machine-b-token-id>"
ti fs delete-file-system \
  --file-system-id "$FILE_SYSTEM_ID"
```

## Security notes

- Each FS token grants owner access. Transfer it as a secret, not in chat or command history, and use a separate token for each machine.
- Concurrent writers can overwrite the same paths; coordinate ownership at the workflow level.
- Do not terminate a machine before graceful unmount completes. Use an explicit drain only when you need remote durability while keeping the FUSE mount online.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md)
