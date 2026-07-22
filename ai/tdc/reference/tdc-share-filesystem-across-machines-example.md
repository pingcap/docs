---
title: Share a TiDB Cloud Filesystem Across Machines
summary: Create one Filesystem, securely access it from a second machine, and verify data-plane and mount visibility.
---

# Share a TiDB Cloud Filesystem Across Machines

This example gives agents or users on two machines one shared workspace without copying files between machine-local disks.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The agent problem

An agent can prepare source files or artifacts on machine A and continue the task on machine B, but each machine normally sees only its own disk. Copying a snapshot before every handoff adds latency, and changes made after the copy are invisible to the other machine. Concurrent handoffs can also create conflicting copies with no clear source of truth.

## Why native local disks and manual synchronization are not enough

Local disks do not provide a shared namespace. Commands such as `scp` and archive upload transfer point-in-time copies rather than live state, while object storage does not by itself behave like the mounted directory expected by editors, build tools, and agents.

## How tdc changes the workflow

Both machines select the same TiDB Cloud Filesystem. Data-plane commands and the mounted path address one remote namespace, so a write from either interface becomes visible through the other after it is flushed. Machine B needs only the Filesystem token, region code, and name; it does not need TiDB Cloud API keys or a copied profile.

## Prerequisites

- Machine A has configured tdc.
- Both machines have tdc installed.
- You have a secure secret-transfer channel.

## Step 1. Create the Filesystem on machine A

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name shared-workspace \
  --wait \
  --query fs_token \
  --output text)"

printf 'from machine A\n' | tdc fs copy-file \
  --file-system-name shared-workspace \
  --from-stdin \
  --to-remote /shared/origin.txt
```

Transfer the token through a secret manager. Also communicate the canonical region code and Filesystem name.

## Step 2. Configure machine B in memory

```bash
export TDC_FS_TOKEN="<owner-token-from-secret-manager>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="shared-workspace"
```

No `tdc configure` is required.

## Step 3. Verify direct visibility on machine B

```bash
tdc fs read-file --path /shared/origin.txt
printf 'from machine B\n' | tdc fs copy-file --from-stdin --to-remote /shared/second.txt
```

## Step 4. Verify mount and data-plane visibility

```bash
mkdir -p /path/to/shared-workspace
tdc fs mount-file-system \
  --file-system-name shared-workspace \
  --mount-path /path/to/shared-workspace

cat /path/to/shared-workspace/shared/origin.txt
printf 'written through mount\n' > /path/to/shared-workspace/shared/mounted.txt
tdc fs read-file --path /shared/mounted.txt
```

The first read proves data-plane writes are visible through the mount. The final read proves mount writes are visible through the data plane after they are flushed.

## Cleanup

Stop writers and unmount either driver. A graceful FUSE unmount automatically drains pending work:

```bash
tdc fs unmount-file-system --mount-path /path/to/shared-workspace
unset TDC_FS_TOKEN TDC_REGION_CODE TDC_FS_FILE_SYSTEM_NAME
```

On machine A:

```bash
tdc fs delete-file-system \
  --file-system-name shared-workspace
```

## Security notes

- The FS token grants owner access. Transfer it as a secret, not in chat or command history.
- Concurrent writers can overwrite the same paths; coordinate ownership at the workflow level.
- Do not terminate a machine before graceful unmount completes. Use an explicit drain only when you need remote durability while keeping the FUSE mount online.

## What's next

- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/tdc/reference/tdc-agent-sandbox-example.md)
