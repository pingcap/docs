---
title: Share a TiDB Cloud Filesystem Across Machines
summary: Create one Filesystem, securely access it from a second machine, and verify data-plane and mount visibility.
---

# Share a TiDB Cloud Filesystem Across Machines

This example creates a Filesystem on machine A and accesses the same data from machine B without copying a tdc profile.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

- Machine A has configured tdc.
- Both machines have tdc installed.
- You have a secure secret-transfer channel.

## Step 1. Create the Filesystem on machine A

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name shared-workspace \
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

Stop writers. If the mount is FUSE:

```bash
tdc fs drain-file-system --mount-path /path/to/shared-workspace
```

Unmount either driver:

```bash
tdc fs unmount-file-system --mount-path /path/to/shared-workspace
unset TDC_FS_TOKEN TDC_REGION_CODE TDC_FS_FILE_SYSTEM_NAME
```

On machine A:

```bash
tdc fs delete-file-system \
  --file-system-name shared-workspace \
  --confirm-file-system-name shared-workspace
```

## Security notes

- The FS token grants owner access. Transfer it as a secret, not in chat or command history.
- Concurrent writers can overwrite the same paths; coordinate ownership at the workflow level.
- Do not terminate a machine before pending FUSE writes are drained.

## What's next

- [Manage TiDB Cloud Filesystem with tdc](/ai/tdc/guides/tdc-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/tdc/examples/tdc-agent-sandbox-example.md)
