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
- Use Bash or Zsh and keep the same shell open throughout the examples.

## Create a layer

Create a unique base directory for the example:

```shell
base_path="/layer-example-$(date +%s)-$$"
ti fs create-directory --path "$base_path"
```

Then create a layer:

```shell
ti fs create-layer \
  --base-root-path "$base_path" \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

`--base-root-path` determines which part of the base file system the layer overlays.

`restore-safe` is the only `--durability-mode` value accepted by the current CLI. For all available options, see the [`create-layer` command reference](/ai/ti/reference/ti-fs-create-layer.md).

The command returns a layer ID. Use the layer ID for subsequent operations, especially in automation, because layer names are not guaranteed to be unique.

## Work with and inspect layer changes

Write a sample file to the layer using the returned layer ID:

```shell
printf 'Layer review proposal\n' | ti fs copy-file \
  --from-stdin \
  --to-remote "$base_path/proposal.md" \
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

### Mount a writable layer

To use local tools, complete the [FUSE prerequisites](/tidb-cloud-filesystem/filesystem-mount.md#choose-a-mount-method) and mount the layer. WebDAV does not support layers or checkpoints.

```shell
layer_mount="$(mktemp -d "$HOME/ti-fs-layer.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$layer_mount" \
  --remote-path "$base_path" \
  --layer-ref "<layer-id>" \
  --driver fuse
cat "$layer_mount/proposal.md"
```

Expected output: `Layer review proposal`. To verify isolation, read from the base file system without selecting a layer:

```shell
ti fs read-file --path "$base_path/proposal.md"
```

Expect a not-found error because the layer has not been committed. If the file is visible in the base, stop and inspect the layer selection before proceeding.

## Create a checkpoint

A checkpoint preserves a point in the layer's durable history.

If the layer has a writable FUSE mount, stop writes, close open files, and drain the mount before creating the checkpoint:

```shell
ti fs drain-file-system \
  --mount-path "$layer_mount"
```

Then create the checkpoint:

```shell
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"
```

To verify the checkpoint's file contents, mount it at a separate local path:

```shell
checkpoint_mount="$(mktemp -d "$HOME/ti-fs-checkpoint.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$checkpoint_mount" \
  --remote-path "$base_path" \
  --layer-ref "<layer-id>" \
  --checkpoint-id seed \
  --driver fuse
cat "$checkpoint_mount/proposal.md"
ti fs unmount-file-system --mount-path "$checkpoint_mount"
```

Expected output: `Layer review proposal`. Checkpoint mounts are read-only. If a read hangs, follow [mount troubleshooting](/tidb-cloud-filesystem/filesystem-troubleshooting.md#mount-succeeds-but-file-access-hangs).

## Fork a layer

If you want to continue working independently from the checkpoint, fork a new writable layer. Otherwise, skip to [Commit or discard layer changes](#commit-or-discard-layer-changes).

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
  --mount-path "$layer_mount"

ti fs unmount-file-system \
  --mount-path "$layer_mount"
```

For more information about safely finishing mount activity, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

To apply the layer's changes to the base file system:

```shell
ti fs commit-layer --layer-id "<layer-id>"
```

After a successful commit, verify the content through the base file system:

```shell
ti fs read-file --path "$base_path/proposal.md"
```

Expected output: `Layer review proposal`.

A commit applies the layer's effective changes to the base file system. If the layer was created by forking another layer, committing it does not merge the changes back into its parent layer.

If the base file system contains conflicting changes, the commit can fail instead of automatically merging them. Keep the layer and inspect its changes and the base file system before deciding how to proceed.

To discard the layer's uncommitted changes instead:

```shell
ti fs rollback-layer --layer-id "<layer-id>"
```

Rollback discards the current layer changes. It does not reset the layer to an earlier checkpoint. To continue from a checkpoint, fork a new layer from that checkpoint.

## Delete a layer

If you created a fork, delete it before its parent:

```shell
ti fs delete-layer --layer-ref "<forked-layer-id>"
```

Then delete the parent layer:

```shell
ti fs delete-layer --layer-ref "<layer-id>"
```

Deleting a layer abandons it without immediately erasing all of its history. If the layer has live descendants, the command fails by default.

Alternatively, to abandon a layer and all of its live descendants together, use `--cascade`:

```shell
ti fs delete-layer \
  --layer-ref "<layer-id>" \
  --cascade
```

Use `--cascade` only when you intend to abandon the descendant layers as well.

After unmounting the example mounts and deleting the example layers, remove the base directory:

```shell
ti fs delete-file --path "${base_path:?Set the example directory first}" --recursive
ti fs describe-file --path "$base_path"
```

Expect a not-found error from `describe-file`. If you created local mount directories, remove them with `rmdir` after successful unmount. Deleting the example files does not erase the abandoned layers' history immediately.

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
