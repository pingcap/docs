---
title: Share a Read-Only Dataset Across Parallel Agents with tdc
summary: Upload one unstructured dataset and expose the same read-only mounted namespace to multiple agent workers.
---

# Share a Read-Only Dataset Across Parallel Agents with tdc

This scenario gives multiple short-lived workers one shared corpus without copying it into every sandbox.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## The problem

Parallel document-processing or evaluation agents often need the same PDFs, images, logs, or model artifacts. Downloading the complete corpus into every worker delays startup, duplicates storage, and leaves each worker with a different point-in-time copy.

## How tdc changes the workflow

An owner uploads the corpus once. Every worker selects the same Filesystem and mounts it read-only, so ordinary tools can traverse a common namespace. Workers write results to separate task paths or a different output Filesystem.

## Step 1. Upload the corpus

On a trusted machine:

```bash
tdc fs create-file-system \
  --file-system-name shared-corpus \
  --set-default \
  --wait

tdc fs copy-file \
  --from-local ./corpus \
  --to-remote /datasets/corpus \
  --recursive

tdc fs find-files \
  --path /datasets/corpus \
  --file-name-pattern "*.pdf" \
  --output text
```

Transfer the returned FS token through a secret manager.

## Step 2. Mount in each worker

Inject the resource token, region, and name into each worker, then run:

```bash
mkdir -p "$HOME/corpus"
tdc fs mount-file-system \
  --file-system-name shared-corpus \
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
tdc fs unmount-file-system --mount-path "$HOME/corpus"
```

## Operational notes

- `--read-only` prevents writes through that mount. The underlying FS owner token remains an owner credential and is not a read-only security token.
- Do not let workers use direct mutating `tdc fs` commands when the workflow requires read-only behavior.
- Partition result paths by agent or run ID if workers write to the same output Filesystem.
- On platforms where FUSE or WebDAV mounting is unavailable, use `read-file`, `find-files`, and `copy-file --to-local` directly.

## Related reference

- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/tdc/reference/tdc-agent-sandbox-example.md)
- [tdc Regions, Security, and Limitations](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
