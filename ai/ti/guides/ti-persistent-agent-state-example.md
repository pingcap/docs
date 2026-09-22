---
title: Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem
summary: Preserve plans, checkpoints, outputs, and workflow history in a TiDB Cloud Filesystem while replacing agent sandboxes.
---

# Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem

This workflow keeps plans, intermediate results, diagnostic files, and workflow history in TiDB Cloud Filesystem while the agent's compute environment remains disposable. A replacement sandbox can resume the task without keeping the previous sandbox alive only to preserve its local disk.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

A trusted machine provisions one Filesystem. Each sandbox receives only the Filesystem token and region code. The token identifies the Filesystem, so the agent can write durable task state to the remote namespace and record workflow transitions in a journal without receiving TiDB Cloud control-plane keys.

## Prerequisites

- Install and configure the TiDB Cloud CLI on a trusted machine.
- Install the TiDB Cloud CLI in each sandbox.
- Install `jq` on the trusted machine.
- Use a secure secret manager or encrypted sandbox input for token transfer.

## Step 1. Provision the state Filesystem

On a trusted machine:

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

Store `TI_FS_TOKEN` in a secret manager, record `FILE_SYSTEM_ID` for cleanup, and record the configured region code. Delete `filesystem.json` after storing these values securely.

## Step 2. Start the first sandbox

Inject the following environment variables:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

Write a plan and create a workflow journal:

```bash
printf '%s\n' '# Plan' '1. inspect' '2. change' '3. verify' \
  | ti fs copy-file --from-stdin --to-remote /tasks/task-42/plan.md

ti fs-journal create-journal \
  --journal-id task-42 \
  --journal-kind agent \
  --title "task 42" \
  --actor agent:worker-1

ti fs-journal append-journal-entries \
  --journal-id task-42 \
  --entry-json '{"type":"task.checkpoint","step":"inspection-complete"}'
```

The `agent` journal kind classifies this journal as an agent workflow and is the default when `--journal-kind` is omitted. The option accepts a custom string when you need a different workflow classification.

## Step 3. Resume in a replacement sandbox

Inject the same two FS variables into the new sandbox, then restore the durable state:

```bash
ti fs read-file --path /tasks/task-42/plan.md
ti fs-journal read-journal-entries --journal-id task-42 --after-seq 0
```

Continue writing results under the same task path. Use a unique task ID so parallel agents do not overwrite each other's files.

## Cleanup

After the sandboxes stop using the Filesystem, delete it from the trusted machine:

```bash
rm -f ./filesystem.json
ti fs delete-file-system --file-system-id "$FILE_SYSTEM_ID"
```

Deleting the Filesystem also deletes its task files and journals.

## Security and operational notes

- The Filesystem token is an owner credential. Keep it in a runtime secret store and do not include it in images or task prompts.
- A completed direct data-plane write is remotely visible. For mounted FUSE writes, unmount gracefully before deleting the sandbox.
- Journals preserve ordered workflow evidence; task files preserve mutable working state. Use both when you need state and history.

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
