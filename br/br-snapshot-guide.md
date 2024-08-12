---
title: Snapshot Backup and Restore Guide
summary: This document describes how to back up and restore TiDB snapshots using the br command-line tool. It includes instructions for snapshot backup, restoring data of a specified time point, and restoring a database or table. The document also covers the performance and impact of snapshot backup and restore.
---

# Snapshot Backup and Restore Guide

This document describes how to back up and restore TiDB snapshots using the br command-line tool (hereinafter referred to as `br`). Before backing up and restoring data, you need to [install the br command-line tool](/br/br-use-overview.md#deploy-and-use-br) first.

Snapshot backup is an implementation to back up the entire cluster. It is based on [multi-version concurrency control (MVCC)](/tidb-storage.md#mvcc) and backs up all data in the specified snapshot to a target storage. The size of the backup data is approximately the size of the compressed single replica in the cluster. After the backup is completed, you can restore the backup data to an empty cluster or a cluster that does not contain conflict data (with the same schema or same tables), restore the cluster to the time point of the snapshot backup, and restore multiple replicas according to the cluster replica settings.

Besides basic backup and restore, snapshot backup and restore also provides the following features:

* [Backup data of a specified time point](#back-up-cluster-snapshots)
* [Restore data of a specified database or table](#restore-a-database-or-a-table)

## Back up cluster snapshots

> **Note:**
>
> - The following examples assume that Amazon S3 access keys and secret keys are used to authorize permissions. If IAM roles are used to authorize permissions, you need to set `--send-credentials-to-tikv` to `false`.
> - If other storage systems or authorization methods are used to authorize permissions, adjust the parameter settings according to [Backup Storages](/br/backup-and-restore-storages.md).

You can back up a TiDB cluster snapshot by running the `tiup br backup full` command. Run `tiup br backup full --help` to see the help information:

```shell
tiup br backup full --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00 +08:00' \
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
```

In the preceding command:

- `--backupts`: The time point of the snapshot. The format can be [TSO](/glossary.md#tso) or timestamp, such as `400036290571534337` or `2018-05-11 01:42:23 +08:00`. If the data of this snapshot is garbage collected, the `tiup br backup` command returns an error and `br` exits. When backing up using a timestamp, it is recommended to specify the time zone as well. Otherwise, `br` uses the local time zone to construct the timestamp by default, which might lead to an incorrect backup time point. If you leave this parameter unspecified, `br` picks the snapshot corresponding to the backup start time.
- `--storage`: The storage address of the backup data. Snapshot backup supports Amazon S3, Google Cloud Storage, and Azure Blob Storage as backup storage. The preceding command uses Amazon S3 as an example. For more details, see [URI Formats of External Storage Services](/external-storage-uri.md).
- `--ratelimit`: The maximum speed **per TiKV** performing backup tasks. The unit is in MiB/s.

During backup, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the backup task is completed and statistics such as total backup time, average backup speed, and backup data size are displayed.

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] *** [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
```

## Get the backup time point of a snapshot backup

To manage a lot of backups, if you need to get the physical time of a snapshot backup, you can run the following command:

```shell
tiup br validate decode --field="end-version" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" | tail -n1
```

The output is as follows, corresponding to the physical time `2022-09-08 13:30:00 +0800 CST`:

```
435844546560000000
```

## Restore cluster snapshots

> **Note:**
>
> - For BR v7.5.0 and earlier versions, the snapshot restore speed per TiKV node is approximately 100 MiB/s.
> - Starting from BR v7.6.0, to address potential restore bottlenecks in scenarios with large-scale Regions, BR supports accelerating restore through the coarse-grained Region scattering algorithm (experimental). You can enable this feature by specifying the command-line parameter `--granularity="coarse-grained"`.
> - Starting from BR v8.0.0, the snapshot restore through the coarse-grained Region scattering algorithm is generally available (GA) and enabled by default. BR improves the snapshot restore speed significantly by implementing various optimizations such as adopting the coarse-grained Region scattering algorithm, creating databases and tables in batches, reducing the mutual impact between SST file downloads and ingest operations, and accelerating the restore of table statistics. According to test results from real-world cases, the SST file download speed for snapshot restore is improved by approximately up to 10 times, the data restore speed per TiKV node stabilizes at 1.2 GiB/s, the end-to-end restore speed is improved by approximately 1.5 to 3 times, and 100 TiB of data can be restored within one hour.
> - Starting from BR v8.2.0, the command line parameter `--granularity` is deprecated, and the coarse-grained Region scattering algorithm is enabled by default.
> - Starting from BR v8.3.0, the snapshot restore task introduces available disk space checks for TiKV and TiFlash: at the beginning of the task, BR verifies whether TiKV and TiFlash have sufficient disk space based on the size of SST files to be restored; for TiKV v8.3.0 or later version, TiKV verifies whether it has sufficient disk space before downloading each SST file. If the space is insufficient according to any of these checks, the restore task fails with an error. You can skip the check at the beginning of the restore task by setting `--check-requirements=false`, but the disk space check before TiKV downloads each SST file cannot be skipped.

You can restore a snapshot backup by running the `tiup br restore full` command. Run `tiup br restore full --help` to see the help information:

The following example restores the [preceding backup snapshot](#back-up-cluster-snapshots) to a target cluster:

```shell
tiup br restore full --pd "${PD_IP}:2379" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

During restore, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the restore task is completed and statistics such as total restore time, average restore speed, and total data size are displayed.

```shell
Full Restore <------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] *** [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

### Restore a database or a table

BR supports restoring partial data of a specified database or table from backup data. This feature allows you to filter out unwanted data and back up only a specific database or table.

**Restore a database**

To restore a database to a cluster, run the `tiup br restore db` command. The following example restores the `test` database from the backup data to the target cluster:

```shell
tiup br restore db \
--pd "${PD_IP}:2379" \
--db "test" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

In the preceding command, `--db` specifies the name of the database to be restored.

**Restore a table**

To restore a single table to a cluster, run the `tiup br restore table` command. The following example restores the `test.usertable` table from the backup data to the target cluster:

```shell
tiup br restore table --pd "${PD_IP}:2379" \
--db "test" \
--table "usertable" \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

In the preceding command, `--db` specifies the name of the database to be restored, and `--table` specifies the name of the table to be restored.

**Restore multiple tables with table filter**

To restore multiple tables with more complex filter rules, run the `tiup br restore full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`. The following example restores tables that match the `db*.tbl*` filter rule from the backup data to the target cluster:

```shell
tiup br restore full \
--pd "${PD_IP}:2379" \
--filter 'db*.tbl*' \
--storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}"
```

### Restore tables in the `mysql` schema

- Starting from BR v5.1.0, when you back up snapshots, BR automatically backs up the **system tables** in the `mysql` schema, but does not restore these system tables by default. 
- Starting from v6.2.0, BR lets you specify `--with-sys-table` to restore **data in some system tables**. 
- Starting from v7.6.0, BR enables `--with-sys-table` by default, which means that BR restores **data in some system tables** by default.

**BR can restore data in the following system tables:**

```
+----------------------------------+
| mysql.columns_priv               |
| mysql.db                         |
| mysql.default_roles              |
| mysql.global_grants              |
| mysql.global_priv                |
| mysql.role_edges                 |
| mysql.tables_priv                |
| mysql.user                       |
| mysql.bind_info                  |
+----------------------------------+
```

**BR does not restore the following system tables:**

- Statistics tables (`mysql.stat_*`). But statistics can be restored. See [Back up statistics](/br/br-snapshot-manual.md#back-up-statistics).
- System variable tables (`mysql.tidb` and `mysql.global_variables`)
- [Other system tables](https://github.com/pingcap/tidb/blob/master/br/pkg/restore/snap_client/systable_restore.go#L31)

```
+-----------------------------------------------------+
| capture_plan_baselines_blacklist                    |
| column_stats_usage                                  |
| gc_delete_range                                     |
| gc_delete_range_done                                |
| global_variables                                    |
| schema_index_usage                                  |
| stats_buckets                                       |
| stats_extended                                      |
| stats_feedback                                      |
| stats_fm_sketch                                     |
| stats_histograms                                    |
| stats_history                                       |
| stats_meta                                          |
| stats_meta_history                                  |
| stats_table_locked                                  |
| stats_top_n                                         |
| tidb                                                |
+-----------------------------------------------------+
```

When you restore data related to system privilege, note that before restoring data, BR checks whether the system tables in the target cluster are compatible with those in the backup data. "Compatible" means that all the following conditions are met:

- The target cluster has the same system tables as the backup data.
- The **number of columns** in the system privilege table of the target cluster is the same as that in the backup data. The column order is not important.
- The columns in the system privilege table of the target cluster are compatible with that in the backup data. If the data type of the column is a type with a length (such as integer and string), the length in the target cluster must be >= the length in the backup data. If the data type of the column is an `ENUM` type, the number of `ENUM` values in the target cluster must be a superset of that in the backup data.

## Performance and impact

### Performance and impact of snapshot backup

The backup feature has some impact on cluster performance (transaction latency and QPS). However, you can mitigate the impact by adjusting the number of backup threads [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) or by adding more clusters.

To illustrate the impact of backup, this document lists the test conclusions of several snapshot backup tests:

- (5.3.0 and earlier) When the backup threads of BR on a TiKV node take up 75% of the total CPU of the node, the QPS is reduced by 35% of the original QPS.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 80%, the impact of BR tasks on the cluster (write and read) is 20% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 75%, the impact of BR tasks on the cluster (write and read) is 10% at most.
- (5.4.0 and later) When there are no more than `8` threads of BR on a TiKV node and the cluster's total CPU utilization does not exceed 60%, BR tasks have little impact on the cluster (write and read).

You can use the following methods to manually control the impact of backup tasks on cluster performance. However, these two methods also reduce the speed of backup tasks while reducing the impact of backup tasks on the cluster.

- Use the `--ratelimit` parameter to limit the speed of backup tasks. Note that this parameter limits the speed of **saving backup files to external storage**. When calculating the total size of backup files, use the `backup data size(after compressed)` as a benchmark. When `--ratelimit` is set, to avoid too many tasks causing the speed limit to fail, the `concurrency` parameter of br is automatically adjusted to `1`.
- Adjust the TiKV configuration item [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1) to limit the number of threads used by backup tasks. According to internal tests, when BR uses no more than `8` threads for backup tasks, and the total CPU utilization of the cluster does not exceed 60%, the backup tasks have little impact on the cluster, regardless of the read and write workload.

The impact of backup on cluster performance can be reduced by limiting the backup threads number, but this affects the backup performance. The preceding tests show that the backup speed is proportional to the number of backup threads. When the number of threads is small, the backup speed is about 20 MiB/thread. For example, 5 backup threads on a single TiKV node can reach a backup speed of 100 MiB/s.

### Performance and impact of snapshot restore

- During data restore, TiDB tries to fully utilize the TiKV CPU, disk IO, and network bandwidth resources. Therefore, it is recommended to restore the backup data on an empty cluster to avoid affecting the running applications.
- The speed of restoring backup data is much related with the cluster configuration, deployment, and running applications. In internal tests, the restore speed of a single TiKV node can reach 100 MiB/s. The performance and impact of snapshot restore are varied in different user scenarios and should be tested in actual environments.
- BR provides a coarse-grained Region scattering algorithm to accelerate Region restore in large-scale Region scenarios. This algorithm ensures that each TiKV node receives stable and evenly distributed download tasks, thus fully utilizing the resources of each TiKV node and achieving a rapid parallel recovery. In several real-world cases, the snapshot restore speed of the cluster is improved by about 3 times in large-scale Region scenarios.
- Starting from v8.0.0, the `br` command-line tool introduces the `--tikv-max-restore-concurrency` parameter to control the maximum number of files that BR downloads and ingests per TiKV node. By configuring this parameter, you can also control the maximum length of the job queue (the maximum length of the job queue = 32 \* the number of TiKV nodes \* `--tikv-max-restore-concurrency`), thereby controlling the memory consumption of the BR node.

    In normal cases, `--tikv-max-restore-concurrency` is automatically adjusted based on the cluster configuration, so manual configuration is unnecessary. If the **TiKV-Details** > **Backup & Import** > **Import RPC count** monitoring metric in Grafana shows that the number of files BR downloads remains close to 0 for a long time while the number of files that BR ingests consistently reaches the upper limit, it indicates that ingesting file tasks pile up and the job queue has reached its maximum length. In this case, you can take the following measures to alleviate the task pilling-up issue:

    - Set the `--ratelimit` parameter to limit the download speed, ensuring sufficient resources for ingesting file tasks. For example, if the disk throughput of any TiKV node is `x MiB/s` and the network bandwidth for downloading backup files exceeds `x/2 MiB/s`, you can set the parameter as `--ratelimit x/2`. If the disk throughput of any TiKV node is `x MiB/s` and the network bandwidth for downloading backup files is less than or equal to `x/2 MiB/s`, you can leave the parameter `--ratelimit` unset.
    - Increase the `--tikv-max-restore-concurrency` to increase the maximum length of the job queue.

## See also

* [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)
* [br Command-line Manual](/br/use-br-command-line-tool.md)
* [TiDB Snapshot Backup and Restore Architecture](/br/br-snapshot-architecture.md)
