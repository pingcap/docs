---
title: Manage Filesystem Layers and Checkpoints
summary: Learn how to safely create, inspect, fork, checkpoint, roll back, commit, pack, and restore TiDB Cloud Filesystem layers.
---

# Manage Filesystem Layers and Checkpoints

Use layers to record isolated changes over a Filesystem base path before you commit or discard them.

## Prerequisites

- Obtain access to a TiDB Cloud Filesystem.
- Choose the base path whose data the layer overlays.

## Create and inspect a layer

```shell
ti fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

Use the returned layer ID to write and inspect changes:

```shell
ti fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

ti fs describe-layer --layer-id "<layer-id>"
ti fs diff-layer --layer-id "<layer-id>"
```

Recursive copy and `--layer-id` are mutually exclusive. To seed a directory tree, use a writable FUSE layer mount.

## Create a checkpoint and fork a layer

```shell
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"

ti fs fork-layer \
  --parent-layer-ref "<layer-id>" \
  --layer-name experiment \
  --checkpoint-id seed
```

Use `list-layer-chain` to inspect the pinned ancestry of the fork.

## Finish work in a layer

Drain and unmount a writable layer before creating a checkpoint, rolling it back, or committing it. Then choose one outcome:

```shell
ti fs rollback-layer --layer-id "<layer-id>"
```

Or:

```shell
ti fs commit-layer --layer-id "<layer-id>"
```

Do not run both commands in sequence for the same work.

## Move local overlay state

Pack selected local overlay paths before moving work to another machine, and unpack them at the destination:

```shell
ti fs pack-file-system --mount-path /path/to/workspace
ti fs unpack-file-system --mount-path /path/to/workspace
```

## What's next

- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
