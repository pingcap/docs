---
title: Share a TiDB Cloud Filesystem Across Machines
summary: Create one Filesystem, securely access it from a second machine, and verify data-plane and mount visibility.
---

# Share a TiDB Cloud Filesystem Across Machines

This example gives agents or users on two machines one shared workspace without copying files between machine-local disks.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## The agent problem

An agent can prepare source files or artifacts on machine A and continue the task on machine B, but each machine normally sees only its own disk. Copying a snapshot before every handoff adds latency, and changes made after the copy are invisible to the other machine. Concurrent handoffs can also create conflicting copies with no clear source of truth.

## Limitations of native local disks and manual synchronization

Local disks do not provide a shared namespace. Commands such as `scp` and archive upload transfer point-in-time copies rather than live state, while object storage does not by itself behave like the mounted directory expected by editors, build tools, and agents.

## How TiDB Cloud CLI changes the workflow

Both machines select the same TiDB Cloud Filesystem with separate owner tokens. Data-plane commands and the mounted path address one remote namespace, so a write from either interface becomes visible through the other after it is flushed. Machine B needs only its Filesystem token and region code; the token identifies the Filesystem, so it does not need TiDB Cloud API keys or a copied profile. Separate tokens let you revoke machine B without interrupting machine A.

## Prerequisites

- Machine A has configured `ti`.
- Both machines have `ti` installed.
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
export TI_REGION_CODE="aws-us-east-1"
```

No `ti configure` is required.

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
ti fs read-file --path /shared/mounted.txt
```

The first read proves data-plane writes are visible through the mount. The final read proves mount writes are visible through the data plane after they are flushed.

## Cleanup

Stop writers and unmount either driver. A graceful FUSE unmount automatically drains pending work:

```bash
ti fs unmount-file-system --mount-path /path/to/shared-workspace
unset TI_FS_TOKEN TI_REGION_CODE
```

On machine A:

```bash
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
- [Use a Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
