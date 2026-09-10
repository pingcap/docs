---
title: Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem
summary: Upload one unstructured dataset and expose the same read-only mounted namespace to multiple agent workers.
---

# Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem

This scenario gives multiple short-lived workers one shared corpus without copying it into every sandbox.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## The problem

Parallel document-processing or evaluation agents often need the same PDFs, images, logs, or model artifacts. Downloading the complete corpus into every worker delays startup, duplicates storage, and leaves each worker with a different point-in-time copy.

## How TiDB Cloud CLI changes the workflow

An owner uploads the corpus once. Every worker selects the same Filesystem and mounts it read-only, so ordinary tools can traverse a common namespace. Workers write results to separate task paths or a different output Filesystem.

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

Unmount before terminating the worker:

```bash
ti fs unmount-file-system --mount-path "$HOME/corpus"
```

## Operational notes

- `--read-only` prevents writes through that mount. The underlying FS owner token remains an owner credential and is not a read-only security token.
- Do not let workers use direct mutating `ti fs` commands when the workflow requires read-only behavior.
- Partition result paths by agent or run ID if workers write to the same output Filesystem.
- On platforms where FUSE or WebDAV mounting is unavailable, use `read-file`, `find-files`, and `copy-file --to-local` directly.

## Related reference

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
