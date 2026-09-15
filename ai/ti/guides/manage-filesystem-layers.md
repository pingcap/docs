---
title: Manage TiDB Cloud Filesystem Layers and Checkpoints
summary: Learn how to safely create, inspect, fork, checkpoint, roll back, commit, pack, and restore TiDB Cloud Filesystem layers.
---

# Manage TiDB Cloud Filesystem Layers and Checkpoints

Use layers to record isolated changes over a Filesystem base path before you commit or discard them.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Select a Filesystem by passing `--file-system-id`, setting `TI_FS_FILE_SYSTEM_ID`, or supplying an FS token that identifies the Filesystem.
- Provide an FS token with the required read or write permission by using `--fs-token`, `TI_FS_TOKEN`, or the local credential stored for the selected Filesystem.
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

> **Note:**
>
> `copy-file` with `--layer-id` does not support recursive copy. To seed a directory tree into a layer, mount the layer as a writable FUSE mount and copy files through the mount path.

Do not mount the same writable layer at multiple local paths concurrently. Reuse its existing mount, or unmount it before mounting the layer elsewhere.

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

Use `list-layer-chain` to inspect the pinned ancestry of the fork:

```shell
ti fs list-layer-chain --layer-ref experiment
```

A checkpoint mount is read-only. To continue working from a checkpoint, fork a new writable layer from it.

## Finish work in a layer

> **Warning:**
>
> Before you create a checkpoint for a layer with a writable FUSE mount, run [`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount). A checkpoint includes only changes that have reached the service. Before you roll back or commit the layer, drain and then [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount). The CLI does not perform these steps automatically.

Choose one outcome for a layer:

- Roll back the layer to discard its changes:

    ```shell
    ti fs rollback-layer --layer-id "<layer-id>"
    ```

- Commit the layer to apply its changes to the base path:

    ```shell
    ti fs commit-layer --layer-id "<layer-id>"
    ```

> **Note:**
>
> Do not run both `rollback-layer` and `commit-layer` in sequence for the same layer.

## Move local state to another machine

When a FUSE mount uses write-back cache, some data can remain in its local overlay directory. To move this local state to another machine, pack it to an explicit remote archive path:

```shell
ti fs pack-file-system \
  --mount-path /path/to/workspace \
  --archive-path /workspace-overlay.tar.gz
```

On the destination machine, restore the archive into a local overlay root:

```shell
ti fs unpack-file-system \
  --local-root /path/to/local-overlay \
  --remote-root /workspace \
  --mount-profile portable \
  --archive-path /workspace-overlay.tar.gz
```

Use the same local overlay root when you mount the Filesystem on the destination machine. For all pack and unpack options, see the [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) and [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) references.

## What's next

- [Mount a TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
