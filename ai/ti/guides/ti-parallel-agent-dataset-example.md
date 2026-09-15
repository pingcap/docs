---
title: Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem
summary: Upload one unstructured dataset and expose the same read-only mounted namespace to multiple agent workers.
---

# Share a Read-Only Dataset Across Parallel Agents with TiDB Cloud Filesystem

This workflow gives multiple short-lived workers one shared corpus without downloading a separate copy into every sandbox. Use it when parallel document-processing or evaluation agents need consistent access to the same PDFs, images, logs, or model artifacts.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

An owner uploads the corpus once and creates a scoped, read-only Filesystem token for each worker. Every worker selects the same Filesystem and mounts the corpus read-only, so ordinary tools can traverse one common namespace without a storage SDK. This reduces startup time and avoids independent point-in-time copies. If workers produce results, they write them to separate paths in a different, writable output Filesystem, not to the dataset Filesystem.

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

# Create one short-lived, read-only scoped token per worker.
ti fs generate-file-system-scoped-token \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID" \
  --subject worker-1 \
  --ttl 24h \
  --allow /datasets/corpus:read,list > ./worker-1-token.json
```

Transfer the `fs_token` from `worker-1-token.json` and the Filesystem region code through a secret manager. Repeat the token-generation command with a unique subject for each worker. Keep the owner token only on the trusted machine, and delete the JSON files after storing the tokens securely.

## Step 2. Mount in each worker

> **Warning:**
>
> Give each worker a scoped token that permits only `read` and `list` under the corpus path. The `--read-only` mount option prevents accidental writes through the mount, but it does not change a token's permissions.

Inject the worker's scoped token as `TI_FS_TOKEN` and set `TI_REGION_CODE` to the Filesystem region, then run:

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
rm -f ./filesystem.json ./worker-*-token.json
ti fs delete-file-system --file-system-id "$TI_FS_FILE_SYSTEM_ID"
```

## Security and operational notes

- Do not distribute the owner token to workers. Generate a separate, short-lived scoped token for each worker so that read-only access is enforced by the credential.
- Partition result paths by agent or run ID if workers write to the same output Filesystem.
- On platforms where FUSE or WebDAV mounting is unavailable, use `read-file`, `find-files`, and `copy-file --to-local` directly.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [Use a Filesystem in an Agent Sandbox](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)
