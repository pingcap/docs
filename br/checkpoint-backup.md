---
title: Checkpoint Backup
summary: Learn about the checkpoint backup feature, including its application scenarios, usage, and implementation details.
---

# Checkpoint Backup <span class="version-mark">New in v6.5.0</span>

Snapshot backup may end in advance due to recoverable errors, such as disk exhaustion and node down. Before TiDB v6.5.0, data that is backed up before the interruption would be invalidated after addressing the error, and you need to start the backup again. For large clusters, this results in noticeable extra cost.

Since TiDB v6.5.0, Backup & Restore (BR) introduces checkpoint backup feature to allow continuing an interrupted backup. This feature is enabled by default. After this feature is enabled, most data of the interrupted backup is retained after an unexpected exit.

## Application scenarios

If your TiDB cluster is large and cannot tolerate backup again after a failure, you can enable the checkpoint backup feature. After this feature is enabled, br command-line tool (hereinafter referred to as `br`) periodically records the shards that have been backed up. In this way, the next backup retry can use the backup progress close to the abnormal exit.

## Usage limitations

During the backup, `br` periodically updates the `gc-safe-point` of the backup snapshot in PD to avoid data being garbage collected. When `br` exits, the `gc-safe-point` cannot be updated in time. As a result, before the next retry backup, the data might have been garbage collected.

To avoid this situation, `br` keeps the `gc-safe-point` for about one hour by default when `gcttl` is not specified. If you need to extend this time, you can set the `gcttl` parameter.

The following example sets `gcttl` to 15 hours to extend the retention period of `gc-safe-point`:

```shell
br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" \
--gcttl 54000
```

> **Note:**
>
> `gc-safe-point` created before backup is deleted after the snapshot backup is completed and you do not need to delete it manually.

## Implementation details

During snapshot backup, `br` encodes the tables into the corresponding key space, and generates backup RPC requests before sending them to TiKV nodes. After receiving the backup request, TiKV nodes back up the data within the requested range. Every time a TiKV node finishes backing up data of a Region, it returns the backup information of this range to `br`.

By recording the information returned by TiKV nodes, `br` gets informed of the key ranges that have been backed up. The checkpoint backup feature periodically uploads the new backup information to external storage so that the key ranges that have been backed up can be persisted.

When `br` retries the backup, it reads the key ranges that have been backed up from external storage, and compares them with the key ranges of the backup task. The differential data helps `br` to determine the data that still needs to be backed up in checkpoint backup.
