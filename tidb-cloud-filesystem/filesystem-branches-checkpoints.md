---
title: TiDB Cloud Filesystem Branches and Checkpoints
summary: Use Filesystem layers to compare parallel agent drafts, checkpoint progress, inspect history, and publish a selected result.
---

# TiDB Cloud Filesystem Branches and Checkpoints

When two agents explore different answers, they should not overwrite each other's drafts. A Filesystem layer gives each agent a writable view over a base directory. Fork layers to work in parallel, record checkpoints for review, and commit a selected result to the shared base.

The CLI calls these objects **layers**, not Git branches. All commands in this guide use `ti fs`; no Git repository is required.

This page explains the model through a parallel review scenario. For individual commands to create, inspect, commit, or roll back layers, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Understand the model

- **Base Filesystem:** the live shared files read by ordinary file commands and mounts without a layer selector.
- **Layer:** a set of changes over a base path. Its writes do not change the base until committed.
- **Fork:** a child layer that pins the parent's layer history at its current tip or a specified checkpoint. The child's later writes are independent of the parent's later layer changes.
- **Checkpoint:** a named point in one layer's durable history. It does not flush another client's pending writes or publish changes to the base.
- **Commit:** apply the layer's effective changes to the base Filesystem. This is not the same as a Git commit.

> **Warning:**
>
> A fork or checkpoint pins layer history, not the entire base Filesystem. Paths resolved from the live base can still reflect later base changes. Layers are neither full Filesystem snapshots nor authorization boundaries. Do not use them as a substitute for backups or scoped tokens.

## Prepare a parallel review

This example has two agents write alternative reports, then publishes one result. It uses new filenames for successive drafts and avoids modifying the same file across checkpoints.

Before running it:

- Install `ti` v0.2.4 or later and select a Filesystem with an owner token as described in [Mounting Locally](/tidb-cloud-filesystem/filesystem-mount.md#select-a-filesystem).
- Use Linux with FUSE3 or macOS with macFUSE. WebDAV cannot mount layers or checkpoints.
- Use the same terminal for the shell variables below. Do not run other writers against this example's base path.

```bash
# Isolate this run from existing work and earlier examples.
RUN_ID="$(date +%s)"
REMOTE_ROOT="/layer-demo-$RUN_ID"
LOCAL_ROOT="$HOME/layer-demo-$RUN_ID"
ti fs create-directory --path "$REMOTE_ROOT"
ti fs create-directory --path "$REMOTE_ROOT/reports"
mkdir -p "$LOCAL_ROOT/brief" "$LOCAL_ROOT/analyst" "$LOCAL_ROOT/review"
```

## Create a seed and fork two drafts

```bash
# Create the seed layer and retain its immutable ID.
BASE_LAYER_ID="$(ti fs create-layer \
  --base-root-path "$REMOTE_ROOT" \
  --layer-name "seed-$RUN_ID" \
  --query layer_id --output text)"

# Direct layer upload avoids a pending local mount write.
printf 'Compare two approaches to the same research question.\n' | ti fs copy-file \
  --from-stdin --to-remote "$REMOTE_ROOT/input.txt" \
  --layer-id "$BASE_LAYER_ID"

SEED_ID="$(ti fs create-layer-checkpoint \
  --layer-id "$BASE_LAYER_ID" \
  --checkpoint-id "seed-$RUN_ID" \
  --label workspace-seed --query checkpoint_id --output text)"
```

Fork both drafts before committing the seed:

```bash
# Both children start from the same parent checkpoint.
BRIEF_ID="$(ti fs fork-layer \
  --parent-layer-ref "$BASE_LAYER_ID" \
  --layer-name "brief-$RUN_ID" --checkpoint-id "$SEED_ID" \
  --query layer_id --output text)"
ANALYST_ID="$(ti fs fork-layer \
  --parent-layer-ref "$BASE_LAYER_ID" \
  --layer-name "analyst-$RUN_ID" --checkpoint-id "$SEED_ID" \
  --query layer_id --output text)"
ti fs list-layer-chain --layer-ref "$ANALYST_ID"

# Publish the shared input before the children start writing new reports.
ti fs commit-layer --layer-id "$BASE_LAYER_ID"
```

The children retain their pinned parent history. Creating the shared directories in the base and committing the seed first also avoids having each child publish inherited directory creation as part of its own report.

## Write the alternatives

```bash
# Give each agent its own writable FUSE mount.
ti fs mount-file-system --driver fuse --remote-path "$REMOTE_ROOT" \
  --mount-path "$LOCAL_ROOT/brief" --layer-ref "$BRIEF_ID"
ti fs mount-file-system --driver fuse --remote-path "$REMOTE_ROOT" \
  --mount-path "$LOCAL_ROOT/analyst" --layer-ref "$ANALYST_ID"

printf 'A concise recommendation.\n' > "$LOCAL_ROOT/brief/reports/brief.txt"
printf 'An evidence-led first draft.\n' > "$LOCAL_ROOT/analyst/reports/analyst-v1.txt"

# Make the first analyst draft durable before checkpointing it.
ti fs drain-file-system --mount-path "$LOCAL_ROOT/analyst" --timeout 30s
V1_ID="$(ti fs create-layer-checkpoint \
  --layer-id "$ANALYST_ID" --checkpoint-id "v1-$RUN_ID" \
  --label first-draft --query checkpoint_id --output text)"
```

The two mounts contain different reports. Neither report is published in the base yet. Do not mount the same writable layer at multiple paths concurrently.

## Review a historical checkpoint

```bash
# Keep revisions in different files for this preview workflow.
printf 'A second draft with additional evidence.\n' > "$LOCAL_ROOT/analyst/reports/analyst-v2.txt"
ti fs drain-file-system --mount-path "$LOCAL_ROOT/analyst" --timeout 30s
ti fs create-layer-checkpoint --layer-id "$ANALYST_ID" \
  --checkpoint-id "v2-$RUN_ID" --label second-draft

# Mount the earlier checkpoint read-only alongside the current writable tip.
ti fs mount-file-system --driver fuse --remote-path "$REMOTE_ROOT" \
  --mount-path "$LOCAL_ROOT/review" \
  --layer-ref "$ANALYST_ID" --checkpoint-id "$V1_ID"
ls "$LOCAL_ROOT/review/reports"
ls "$LOCAL_ROOT/analyst/reports"
ti fs diff-layer --layer-id "$ANALYST_ID"
```

The historical view includes `analyst-v1.txt` but not the later `analyst-v2.txt`. The writable tip includes both. `diff-layer` reports layer changes; it is not a Git-style line-by-line patch.

To continue writing from a checkpoint, create a new child with `ti fs fork-layer --parent-layer-ref <layer-id> --checkpoint-id <checkpoint-id> --layer-name <new-name>` while the parent remains forkable. A checkpoint mount itself is read-only. `rollback-layer` discards a layer; it does not reset that layer to a selected checkpoint.

## Publish the selected result

Stop all writers and unmount the example mounts before changing layer lifecycle state:

```bash
# Flush writes and release both writable and historical mounts.
ti fs unmount-file-system --mount-path "$LOCAL_ROOT/review"
ti fs drain-file-system --mount-path "$LOCAL_ROOT/brief" --timeout 30s
ti fs unmount-file-system --mount-path "$LOCAL_ROOT/brief"
ti fs drain-file-system --mount-path "$LOCAL_ROOT/analyst" --timeout 30s
ti fs unmount-file-system --mount-path "$LOCAL_ROOT/analyst"

# Abandon the rejected draft and publish the selected layer to the base.
ti fs delete-layer --layer-ref "$BRIEF_ID"
ti fs commit-layer --layer-id "$ANALYST_ID"
ti fs read-file --path "$REMOTE_ROOT/reports/analyst-v2.txt"
```

Committing publishes all effective changes in the selected layer, including both analyst draft files in this example. It does not select a single file automatically. Deleting a layer logically abandons it; it does not guarantee immediate physical removal of history still pinned by descendants.

## Preview boundaries

- Use immutable layer IDs in automation. Names are not guaranteed to be unique.
- Run a successful FUSE drain before a checkpoint of mounted writes. A checkpoint cannot capture data still buffered only on another machine.
- Recursive `ti fs copy-file --recursive` cannot be combined with `--layer-id`. To populate a layer with a directory tree, copy through its writable FUSE mount.
- Plain `ti fs read-file` and `ti fs list-files` read the base, not an uncommitted layer. Use a layer mount to inspect its files.
- Commit can fail on conflicting base changes. Retain the layer and inspect the conflict; do not automatically delete and recreate it or assume a transactional multi-file merge.
- Repeated changes to layer-created files and inherited metadata can have preview limitations. This example deliberately uses separate revision files and publishes the seed before child work. Test your own workflow before relying on more complex edit histories.
- Layer commit is not a merge into its parent, and the CLI does not provide Git-style merge, rebase, or an in-place reset to a checkpoint.

## What's next

- [Control which participants can read and write](/tidb-cloud-filesystem/filesystem-authorization.md).
- [Review the layer command reference](/ai/ti/reference/ti-filesystem.md).
