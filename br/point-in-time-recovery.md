---
title: Point-in-Time Recovery
summary: Learn the design, capabilities, and architecture of Point-in-Time Recovery (PiTR).
---

# Point-in-Time Recovery

Point-in-Time Recovery (PiTR) allows you to restore a snapshot of a TiDB cluster to a new cluster from any given time in the past. TiDB v6.2.0 introduces PiTR in [Backup and Restore](/br/backup-and-restore-overview.md) (BR).

You can use PiTR to meet the following business requirements:

- Reduce the RPO of disaster recovery to less than 20 minutes.
- Handle the cases of incorrect writes from applications by, for example, rolling back data to before the error event.
- Perform history data auditing to meet the requirements of laws and regulations.

This document introduces the design, capabilities, and architecture of PiTR. If you need to learn how to use PiTR, refer to [PiTR Usage Scenarios](/br/pitr-usage.md).

## Use PiTR in your business

[BR](/br/backup-and-restore-overview.md) is the tool for using the PiTR feature. With BR, you can perform all operations of PiTR, including data backup (snapshot backup and log backup), one-click restoration to a specified time point, and backup data management.

The following are the procedures of using PiTR in your business:

![Point-in-Time Recovery](/media/br/pitr-usage.png)

### Back up data

To achieve PiTR, you need to perform the following backup tasks:

- Start a log backup task. You can run the `br log start` command to start a log backup task. This task runs in the background of your TiDB cluster and automatically backs up the change log of KV storage to the backup storage.
- Perform [snapshot (full) backup](/br/br-usage-backup.md#back-up-tidb-cluster-snapshots) regularly. You can run the `br backup full` command to back up the cluster snapshot to the backup storage at, for example, 00:00 every day.

### Restore data with one click

To restore data using PiTR, you need to run the `br restore point` command to execute the restoration program. The program reads data from snapshot backup and log backup and restores the data of the specified time point to the new cluster.

When you run the `br restore point` command, you need to specify the latest snapshot backup data before the time point you want to restore and log backup data. BR first restores the snapshot data, and then reads the log backup data from the snapshot time point to the specified restoration time point.

### Manage backup data

To manage backup data for PiTR, you need to design a backup directory structure to store your backup data and regularly delete outdated or no longer needed backup data.

- Organize the backup data in the following structure:

    - Store the snapshot backup and log backup in the same directory for unified management. For example, `backup-${cluster-id}`.
    - Store each snapshot backup in a directory whose name includes the backup date. For example, `backup-${cluster-id}/snapshot-20220512000130`.
    - Store the log backup in a fixed directory. For example, `backup-${cluster-id}/log-backup`.

- Delete the outdated or no longer needed backup data:

    - When you delete the snapshot backup, you can delete the directory of snapshot backup.
    - To delete the log backup before a specified time point, run the `br log truncate` command.

## Capabilities

- PiTR log backup has a 5% impact on the cluster.
- When you run log backup and snapshot backup at the same time, it has a less than 20% impact on the cluster.
- On each TiKV node, PiTR can restore snapshot data at 280 GB/h and log data at 30 GB/h.
- With PiTR, the RPO of disaster recovery is less than 20 minutes.Depending on the data size to be restored, the RTO varies from several minutes to several hours.
- BR deletes outdated log backup data at a speed of 600 GB/h.

<Note>
- The preceding data is based on test results from the following two testing scenarios. The actual data may be different.
- Snapshot data restoration speed = Snapshot data size / (duration * the number of TiKV nodes)
- Log data restoration speed = Restored log data size / (duration * the number of TiKV nodes)
</Note>

Testing scenario 1 (on [TiDB Cloud](https://tidbcloud.com)):

- The number of TiKV nodes (8 core, 16 GB memory): 21
- The number of Regions: 183,000
- New log created in the cluster: 10 GB/h
- Write (insert/update/delete) QPS: 10,000

Testing scenario 2 (on-premises):

- The number of TiKV nodes (8 core, 64 GB memory): 6
- The number of Regions: 50,000
- New log created in the cluster: 10 GB/h
- Write (insert/update/delete) QPS: 10,000

## Limitations

- A single cluster can only start one log backup task.
- You can only restore data to an empty cluster. To avoid impact on the services and data of the cluster, you cannot perform PiTR in-place or on a non-empty cluster.
- You can use Amazon S3 or a shared filesystem (such as NFS) to store the backup data. Currently, GCS and Azure Blob Storage are not supported.
- You can only perform PiTR on cluster level. Database-level and table-level PiTR are not supported.
- You cannot restore data in the user tables or the privilege tables.
- You cannot restore data to the TiFlash storage engine. If the backup cluster has TiFlash replicas, after you perform PiTR, the restoration cluster does not have any TiFlash replica. If the restoration cluster has TiFlash replicas, you need to [manually configure the replica in the schema or the table](/br/pitr-troubleshoot.md#在使用-br-restore-point-命令恢复下游集群后无法从-tiflash-引擎中查询到数据该如何处理). //TODO
- If the upstream database uses TiDB Lightning's physical import mode to import data, the data cannot be backed up in log backup. For details, refer to [上游数据库使用 TiDB Lightning Physical 方式导入数据，导致无法使用日志备份功能](/br/pitr-known-issues.md#上游数据库使用-tidb-lightning-physical-方式导入数据导致无法使用日志备份功能). //TODO
- During the backup process, you cannot exchange partition. For details, refer to [日志备份过程中执行分区交换](/br/pitr-troubleshoot.md#日志备份过程中执行分区交换-exchange-partition-ddl在-pitr-恢复时会报错该如何处理). //TODO
- You cannot restore the log backup data of a certain time period repeatedly. If you restore the log backup data of a range `[t1=10, t2=20)` repeatedly, the restored data might be inconsistent.
- For other known limitations, refer to [PiTR Known Issues](/br/pitr-known-issues.md).
