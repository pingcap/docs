---
title: Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem
summary: Upload one unstructured dataset and expose the same read-only mounted namespace to multiple agent workers.
---

# Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem

This workflow gives multiple short-lived workers one shared corpus without downloading a separate copy into every sandbox. Use it when parallel document-processing or evaluation agents need consistent access to the same PDFs, images, logs, or model artifacts.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## How it works

An owner uploads the corpus once. Every worker selects the same Filesystem and mounts it read-only, so ordinary tools can traverse one common namespace without a storage SDK. This reduces startup time and avoids independent point-in-time copies. Workers write results to separate task paths or a different output Filesystem.

## Prerequisites

- Install and configure the TiDB Cloud CLI on a trusted machine.
- Install the TiDB Cloud CLI and the required mount dependencies in each worker.
- Install `jq` on the trusted machine.
- Use a secure secret manager or encrypted worker input for token transfer.

## Step 1. Upload the corpus

On a trusted machine:

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs copy-file \
  --from-local ./corpus \
  --to-remote /datasets/corpus \
  --recursive

ti fs find-files \
  --path /datasets/corpus \
  --file-name-pattern "*.pdf" \
  --output text
```

Transfer the FS token and canonical region code through a secret manager. Delete `filesystem.json` after storing the token securely.

## Step 2. Mount in each worker

> **Warning:**
>
> `--read-only` prevents writes only through that mount. The FS owner token remains an owner credential and can authorize writes through direct `ti fs` commands. Do not treat a read-only mount as a read-only security credential.

Inject `TI_FS_TOKEN` and `TI_REGION_CODE` into each worker, then run:

```bash
mkdir -p "$HOME/corpus"
ti fs mount-file-system \
  --mount-path "$HOME/corpus" \
  --remote-path /datasets/corpus \
  --read-only
```

The worker can use standard tools without a storage SDK:

```bash
find "$HOME/corpus" -type f -name '*.pdf' -print
```

## Cleanup

Unmount the Filesystem in every worker before terminating it:

```bash
ti fs unmount-file-system --mount-path "$HOME/corpus"
```

After all workers have unmounted the Filesystem, delete it from the trusted machine if you no longer need the dataset:

```bash
rm -f ./filesystem.json
ti fs delete-file-system --file-system-id "$TI_FS_FILE_SYSTEM_ID"
```

## Security and operational notes

- Do not let workers use direct mutating `ti fs` commands when the workflow requires read-only behavior.
- Partition result paths by agent or run ID if workers write to the same output Filesystem.
- On platforms where FUSE or WebDAV mounting is unavailable, use `read-file`, `find-files`, and `copy-file --to-local` directly.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
