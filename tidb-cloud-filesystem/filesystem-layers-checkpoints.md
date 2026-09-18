---
title: TiDB Cloud Filesystem Layers and Checkpoints
summary: TiDB Cloud Filesystem layers isolate changes from the base Filesystem, while forks and checkpoints preserve layer history until changes are committed.
---

# TiDB Cloud Filesystem Layers and Checkpoints

A Filesystem layer records changes over a path in the base Filesystem while keeping those changes separate from the shared base data. Changes in a layer become part of the base Filesystem only when the layer is committed.

Layers can also be checkpointed or forked, which lets you preserve a point in a layer's history or continue work in an independent child layer.

Filesystem layers are independent of Git branches and do not require a Git repository.

For commands to create, inspect, fork, checkpoint, commit, or roll back layers, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Core concepts

- **Base Filesystem:** the shared Filesystem state outside a layer. A layer records changes over a base path without immediately modifying this state.
- **Layer:** a writable set of changes over a base path. Until the layer is committed, its changes remain separate from the base Filesystem.
- **Checkpoint:** a named point in a layer's durable history. Creating a checkpoint preserves that point in the layer history but does not apply the layer's changes to the base Filesystem.
- **Fork:** a new writable child layer created from the current state of another layer or from one of its checkpoints. Changes made after the fork are independent between the parent and child layers.
- **Commit:** applies the effective changes in a layer to the base Filesystem.
- **Rollback:** discards the layer's uncommitted changes without applying them to the base Filesystem. Rollback does not reset a layer to an earlier checkpoint.

## Layers and the base Filesystem

Changes made in a layer are visible through that layer but are not visible in the base Filesystem until the layer is committed.

Operations that do not specify a layer access the base Filesystem. This means that an uncommitted layer does not change what other users or applications see when they access the base directly.

A layer is an overlay on a base path rather than a complete snapshot of the Filesystem. A fork or checkpoint preserves the relevant layer history, but it does not freeze the entire base Filesystem. Data that continues to be resolved from the base can therefore reflect later changes to the base.

## Forks and checkpoints

A checkpoint preserves a point in one layer's durable history. It does not create another writable layer and does not publish changes to the base Filesystem.

A checkpoint can be accessed as a read-only view. To continue making changes from a checkpoint, fork a new writable layer from it.

A fork preserves the parent layer history at the point where the fork is created. After that, new changes in the parent and child layers are independent.

For operational requirements when creating checkpoints or working with mounted layers, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

## Commit and rollback

Committing a layer applies all of its effective changes to the base Filesystem. A commit is not a Git commit and does not selectively publish individual files.

A commit applies changes to the base Filesystem, not to the layer's parent layer. If the base Filesystem contains conflicting changes, the commit can fail rather than automatically merging the changes.

Rolling back a layer discards its uncommitted changes instead of publishing them. It does not reset the layer to an earlier checkpoint.

## Boundaries and limitations

Layers provide change isolation, but they are not full Filesystem snapshots, backups, or authorization boundaries. To restrict access to Filesystem paths or operations, use [scoped tokens](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-tokens).

The current layer model has the following limitations:

- Git-style merge and rebase operations are not supported.
- A layer cannot be reset in place to a checkpoint. To continue from a checkpoint, fork a new layer.
- Committing a child layer does not merge its changes into its parent layer.
- Deleting a layer logically abandons it, but history referenced by descendant layers might remain available while those descendants depend on it.
- Complex histories involving repeated changes to layer-created files or inherited metadata might have limitations during public preview.

For command syntax, flags, and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).
