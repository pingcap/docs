---
title: TiDB Cloud Filesystem Layers and Checkpoints
summary: Understand how Filesystem layers isolate changes, how forks and checkpoints preserve layer history, and when changes become visible in the base Filesystem.
---

# TiDB Cloud Filesystem Layers and Checkpoints

A Filesystem layer gives you a writable view over a base path without immediately changing the shared files. Use layers to prepare independent drafts, inspect changes, and publish a selected result after review. The CLI calls these objects **layers**, not Git branches; no Git repository is required.

For commands to create, fork, checkpoint, commit, or roll back a layer, see [Manage TiDB Cloud Filesystem Layers and Checkpoints](/tidb-cloud-filesystem/manage-filesystem-layers.md).

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Understand the model

- **Base Filesystem:** the live shared files read by ordinary file commands and mounts without a layer selector.
- **Layer:** a set of changes over a base path. Its writes remain separate from the base until committed.
- **Fork:** a child layer that pins the parent's layer history at its current tip or a specified checkpoint. Later writes to either layer are independent of the other layer's later changes.
- **Checkpoint:** a named point in one layer's durable history. It does not publish changes to the base or flush another client's pending writes.
- **Commit:** apply all of the layer's effective changes to the base Filesystem. This is not a Git commit or a selective per-file publish operation.

Use immutable layer IDs in automation because layer names are not guaranteed to be unique. A checkpoint mount is read-only; to continue writing from a checkpoint, fork a new writable layer. Rolling back a layer discards its changes rather than resetting it to a selected checkpoint.

## Understand visibility and boundaries

Plain `ti fs read-file` and `ti fs list-files` commands read the base, not an uncommitted layer. Use a layer mount to inspect files in that layer. A fork or checkpoint pins layer history, not the entire base Filesystem: paths resolved from the live base can still reflect later base changes.

Before checkpointing a layer with a writable FUSE mount, [drain the mount](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely) so its writes reach the service. Before committing or rolling back the layer, drain and unmount it. Do not mount the same writable layer at multiple local paths concurrently.

Layers are not full Filesystem snapshots, backups, or authorization boundaries. Use [scoped tokens](/tidb-cloud-filesystem/filesystem-authorization.md#scoped-fs-tokens) to limit access. A layer commit can fail if the base has conflicting changes; retain the layer and inspect the conflict rather than assuming an automatic merge.

## Limitations

### Unsupported operations

- The CLI does not provide Git-style merge, rebase, or an in-place reset to a checkpoint.
- A layer commit does not merge changes into its parent layer.

### Other boundaries

- Deleting a layer logically abandons it but does not guarantee immediate physical removal of history pinned by descendants.
- Repeated changes to layer-created files and inherited metadata can have preview limitations. Test complex edit histories before relying on them.

For command flags and output fields, see the [`ti fs` command reference](/ai/ti/reference/ti-filesystem.md).
