---
title: Manage File System Layers and Checkpoints
summary: Learn how to create, inspect, checkpoint, fork, commit, roll back, and delete file system layers.
aliases: ['/ai/manage-filesystem-layers']
---

# Manage File System Layers and Checkpoints

In TiDB Cloud Filesystem, a layer gives you a separate workspace for changing files without immediately affecting the base file system. You can make and review changes in the layer, then decide whether to apply them to the base file system or discard them.

You can also create a checkpoint to preserve a point in the layer's history, or fork a new layer from the current layer or a checkpoint to continue working independently.

For an overview of how layers, checkpoints, forks, and the base file system relate to each other, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing file system in TiDB Cloud Filesystem with a token that provides the required read or write permissions.
- Select the file system and make its token available to `ti`. For available access options, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).
- Choose the base path whose data the layer overlays.

## Create a layer

Choose the base path that you want the layer to overlay, and create a layer:

```shell
ti fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

`--base-root-path` determines which part of the base file system the layer overlays.

`restore-safe` is the only `--durability-mode` value accepted by the current CLI. For all available options, see the [`create-layer` command reference](/ai/ti/reference/ti-fs-create-layer.md).

The command returns a layer ID. Use the layer ID for subsequent operations, especially in automation, because layer names are not guaranteed to be unique.

## Work with and inspect layer changes

Write a file to the layer by specifying its layer ID:

```shell
ti fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"
```

Inspect the layer and its changes:

```shell
ti fs describe-layer --layer-id "<layer-id>"
ti fs diff-layer --layer-id "<layer-id>"
```

List all layers in the selected file system:

```shell
ti fs list-layers --output text
```

Changes that have not been committed remain in the layer. File operations that do not select the layer access the base file system and do not show its uncommitted changes.

> **Note:**
>
> `copy-file` with `--layer-id` does not support recursive copy. To copy a directory tree into a layer, mount the layer as a writable FUSE mount and copy files through the mount path.
>
> Do not mount the same writable layer at multiple local paths concurrently. Reuse its existing mount, or unmount it before mounting the layer elsewhere.

## Create a checkpoint

A checkpoint preserves a point in the layer's durable history.

If the layer has an active writable FUSE mount, drain pending writes before creating the checkpoint so that the checkpoint includes the changes that have reached the service:

```shell
ti fs drain-file-system \
  --mount-path "/path/to/workspace"
```

Then create the checkpoint:

```shell
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"
```

A checkpoint mount is read-only. To continue making changes from a checkpoint, fork a new writable layer.

## Fork a layer

Fork a new writable layer from the current layer or one of its checkpoints:

```shell
ti fs fork-layer \
  --parent-layer-ref "<layer-id>" \
  --layer-name experiment \
  --checkpoint-id seed
```

Use the layer ID returned for the fork when you perform subsequent operations on it.

To inspect the fork's pinned ancestry:

```shell
ti fs list-layer-chain --layer-ref "<forked-layer-id>"
```

After a fork is created, changes made to the parent and child layers are independent.

## Commit or discard layer changes

Before committing or rolling back a layer with an active writable FUSE mount, stop applications that are writing to the mount, drain pending writes, and unmount it:

```shell
ti fs drain-file-system \
  --mount-path "/path/to/workspace"

ti fs unmount-file-system \
  --mount-path "/path/to/workspace"
```

For more information about safely finishing mount activity, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

To apply the layer's changes to the base file system:

```shell
ti fs commit-layer --layer-id "<layer-id>"
```

A commit applies the layer's effective changes to the base file system. If the layer was created by forking another layer, committing it does not merge the changes back into its parent layer.

If the base file system contains conflicting changes, the commit can fail instead of automatically merging them. Keep the layer and inspect its changes and the base file system before deciding how to proceed.

To discard the layer's uncommitted changes instead:

```shell
ti fs rollback-layer --layer-id "<layer-id>"
```

Rollback discards the current layer changes. It does not reset the layer to an earlier checkpoint. To continue from a checkpoint, fork a new layer from that checkpoint.

## Delete a layer

When you no longer need a layer, delete it by its layer ID:

```shell
ti fs delete-layer --layer-ref "<layer-id>"
```

Deleting a layer abandons it without immediately erasing all of its history. If the layer has live descendants, the command fails by default.

To abandon the layer and all of its live descendants, use `--cascade`:

```shell
ti fs delete-layer \
  --layer-ref "<layer-id>" \
  --cascade
```

Use `--cascade` only when you intend to abandon the descendant layers as well.

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
