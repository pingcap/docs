---
title: Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem
summary: Preserve plans, checkpoints, outputs, and workflow history in a TiDB Cloud Filesystem while replacing agent sandboxes.
---

# Persist Agent State Across Disposable Sandboxes with TiDB Cloud Filesystem

This scenario keeps an agent's durable state in TiDB Cloud Filesystem while its compute environment remains disposable.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## The problem

An agent sandbox can disappear after a timeout, failure, or deployment. Plans, intermediate results, and diagnostic files stored only on its local disk disappear with it. Keeping the sandbox alive only to preserve state ties storage durability to compute lifecycle and wastes resources.

## How TiDB Cloud CLI changes the workflow

A trusted machine provisions one Filesystem. Each sandbox receives only the Filesystem token, region code, and name. The agent writes durable task state to the remote namespace and records workflow transitions in a journal. A replacement sandbox can read both without receiving TiDB Cloud control-plane keys.

## Step 1. Provision the state Filesystem

On a trusted machine:

```bash
export TI_FS_TOKEN="$(ti fs create-file-system \
  --file-system-name agent-state \
  --wait \
  --query fs_token \
  --output text)"
```

Store `TI_FS_TOKEN` in a secret manager. Also record the configured canonical region code and the Filesystem name.

## Step 2. Start the first sandbox

Inject the following environment variables:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
export TI_FS_FILE_SYSTEM_NAME="agent-state"
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

## Step 3. Resume in a replacement sandbox

Inject the same three FS variables into the new sandbox, then restore the durable state:

```bash
ti fs read-file --path /tasks/task-42/plan.md
ti fs-journal read-journal-entries --journal-id task-42 --after-seq 0
```

Continue writing results under the same task path. Use a unique task ID so parallel agents do not overwrite each other's files.

## Operational notes

- The FS token is an owner credential. Keep it in a runtime secret store and do not include it in images or task prompts.
- A completed direct data-plane write is remotely visible. For mounted FUSE writes, unmount gracefully before deleting the sandbox.
- Journals preserve ordered workflow evidence; task files preserve mutable working state. Use both when you need state and history.

## Related reference

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
