---
title: Known Issues in Log Backup
summary: Learn known issues in log backup.
---

# Known Issues in Log Backup

This document lists the known issues and corresponding workarounds when you use the log backup feature.

## BR encounters the OOM problem when you execute PiTR recovery or the `br log truncate` command

Issue: [#36648](https://github.com/pingcap/tidb/issues/36648)

Consider the following possible causes.

- PiTR recovery experiences OOM because the log interval to be recovered is too large.
    It is recommended that the recovery log interval range from two days to one week. That is, perform a full backup operation at least once in two days or once in up to one week during the backup process.
- OOM occurs when you delete a log because the interval of the deleted log is too large.
    To resolve this issue, you can reduce the interval for the log to be deleted. You can delete small interval logs several times instead of deleting the large interval logs directly.
- The memory allocation of the node where the BR process is located is too low.
    It is recommended to scale up the node memory configuration to at least 16 GB to ensure that PiTR has sufficient memory resources for recovery.

## The upstream database uses TiDB Lightning Physical Mode to import data, which makes it impossible to use the log backup feature

Currently the log backup feature is not fully adapted to TiDB Lightning, so the data imported by TiDB Lightning Physical Mode cannot be backed up to the log.

In upstream clusters where you create log backup tasks, avoid using the TiDB Lightning Physical Mode to import data. Instead, you can use TiDB Lightning Logical Mode. If you do need to use the Physical Mode, you can do a full backup operation after the import is complete, so that PiTR can be restored to the time point after the full backup.

## When you use the self-built Minio system as the storage for log backups, running `br restore point` or `br log truncate` returns a `RequestCanceled` error

Issue: [#36515](https://github.com/pingcap/tidb/issues/36515)

```shell
[error="RequestCanceled: request context canceled\ncaused by: context canceled"]
```

This error occurs because the current log backup generates a large number of small files. The capacity of the self-built Minio storage system cannot support the current log backup feature.

To resolve this issue, you need to upgrade your Minio system to a large distributed cluster, or use the Amazon S3 storage system directly as the storage for log backups.

## If the cluster load is too high, there are too many Regions, and the storage has reached a performance bottleneck (for example, use a self-built Minio system as storage for log backups), the backup progress checkpoint delay may exceed 10 minutes

Issue: [#13030](https://github.com/tikv/tikv/issues/13030)

Because the current log backup generates a large number of small files, the self-built Minio system is not able to support the writing requirements, which results in slow backup progress.

To resolve this issue, you need to upgrade your Minio system to a large distributed cluster, or use the Amazon S3 storage system directly as the storage for log backups.

## The cluster has recovered from the network partition failure, the checkpoint of the log backup task progress still does not resume

Issue: [#13126](https://github.com/tikv/tikv/issues/13126)

After a network partition failure in the cluster, the backup task cannot continue backing up the logs. After a certain retry time, the task will be set to `ERROR` state. At this point, the backup task has stopped.

To resolve this issue, you need to manually execute the `br log resume` command to resume the log backup task.
