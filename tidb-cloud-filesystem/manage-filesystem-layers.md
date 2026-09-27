---
title: Manage File System Layers and Checkpoints
summary: Learn how to create file system layers, checkpoint and fork changes, verify isolation, and commit or discard your work.
aliases: ['/ai/manage-filesystem-layers']
---

# Manage File System Layers and Checkpoints

A layer isolates file changes from the base file system until you commit them. Use checkpoints to preserve intermediate states and forks to explore changes independently. For the underlying concepts, see [Layers and Checkpoints](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have an owner token or a scoped token with `read,list,write,delete` permissions on an existing directory. The example creates and deletes a child directory there.
- Select the file system and make its token available to `ti`. For available access options, see [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).
- Use Bash or Zsh and keep the same shell open throughout the examples.

## Create a layer

Choose an existing directory within your token's scope. Use `/` with an owner token, or replace it with the directory allowed by your scoped token, such as `/workspace`. Create a unique child directory for the example:

```shell
parent_path="/"
base_path="${parent_path%/}/layer-example-$(date +%s)-$$"
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

Save the returned `layer_id` for the remaining commands:

```shell
layer_id="<returned-layer-id>"
```

Use the ID rather than the layer name, which might not be unique.

## Work with and inspect layer changes

Write a sample file to the layer using the returned layer ID:

```shell
printf 'Layer review proposal\n' | ti fs copy-file \
  --from-stdin \
  --to-remote "$base_path/proposal.md" \
  --layer-id "$layer_id"
```

Inspect the layer and its changes:

```shell
ti fs describe-layer --layer-id "$layer_id"
ti fs diff-layer --layer-id "$layer_id"
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
  --layer-ref "$layer_id" \
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
  --layer-id "$layer_id" \
  --checkpoint-id seed \
  --label "before review"
```

To verify the checkpoint's file contents, mount it at a separate local path:

```shell
checkpoint_mount="$(mktemp -d "$HOME/ti-fs-checkpoint.XXXXXX")"
ti fs mount-file-system \
  --mount-path "$checkpoint_mount" \
  --remote-path "$base_path" \
  --layer-ref "$layer_id" \
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
  --parent-layer-ref "$layer_id" \
  --layer-name experiment \
  --checkpoint-id seed
```

Save the fork's returned `layer_id` separately:

```shell
forked_layer_id="<returned-forked-layer-id>"
```

To inspect the fork's pinned ancestry:

```shell
ti fs list-layer-chain --layer-ref "$forked_layer_id"
```

After a fork is created, changes made to the parent and child layers are independent.

## Commit or discard layer changes

If the layer has a writable FUSE mount, stop writers, close open files, and unmount it before choosing an outcome:

```shell
ti fs unmount-file-system \
  --mount-path "$layer_mount"
```

Normal unmount drains pending writes. If unmount fails or the mount log reports a forced exit, keep the local state and verify the layer's contents before continuing; see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

Choose one outcome: **commit** applies the changes to the base file system; **rollback** discards them. To commit:

```shell
ti fs commit-layer --layer-id "$layer_id"
```

After a successful commit, verify the content through the base file system:

```shell
ti fs read-file --path "$base_path/proposal.md"
```

Expected output: `Layer review proposal`.

A commit applies the layer's effective changes to the base file system. If the layer was created by forking another layer, committing it does not merge the changes back into its parent layer.

If the base file system contains conflicting changes, the commit can fail instead of automatically merging them. Keep the layer and inspect its changes and the base file system before deciding how to proceed.

If you chose to discard the changes, run this command instead of committing:

```shell
ti fs rollback-layer --layer-id "$layer_id"
```

Rollback discards the current layer changes. It does not reset the layer to an earlier checkpoint. To continue from a checkpoint, fork a new layer from that checkpoint.

## Delete a layer

If you created a fork, delete it before its parent:

```shell
ti fs delete-layer --layer-ref "$forked_layer_id"
```

Then delete the parent layer:

```shell
ti fs delete-layer --layer-ref "$layer_id"
```

Deleting a layer abandons it without immediately erasing all of its history. If the layer has live descendants, the command fails by default.

Alternatively, to abandon a layer and all of its live descendants together, use `--cascade`:

```shell
ti fs delete-layer \
  --layer-ref "$layer_id" \
  --cascade
```

Use `--cascade` only when you intend to abandon the descendant layers as well.

After unmounting the example mounts and deleting the example layers, remove the base directory:

```shell
ti fs delete-file --path "${base_path:?Set the example directory first}" --recursive
ti fs describe-file --path "$base_path"
```

Expect a not-found error from `describe-file`. After successful unmount, remove the local directories you created with `rmdir "$layer_mount"` and `rmdir "$checkpoint_mount"`. Deleting the example files does not erase the abandoned layers' history immediately.

## What's next

- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
