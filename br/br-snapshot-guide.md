---
title: Snapshot Backup and Restore Guide
summary: This document describes how to back up and restore TiDB snapshots using the br command-line tool. It includes instructions for snapshot backup, restoring data of a specified time point, and restoring a database or table. The document also covers the performance and impact of snapshot backup and restore.
aliases: ['/tidb/dev/br-usage-backup/','/tidb/dev/br-usage-restore/','/tidb/dev/br-usage-restore-for-maintain/', '/tidb/dev/br-usage-backup-for-maintain/']
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
    --storage "s3://backup-101/snapshot-202209081330?access-key=${access-key}&secret-access-key=${secret-access-key}" 
```

In the preceding command:

- `--backupts`: The time point of the snapshot. The format can be [TSO](/tso.md) or timestamp, such as `400036290571534337` or `2018-05-11 01:42:23 +08:00`. If the data of this snapshot is garbage collected, the `tiup br backup` command returns an error and `br` exits. When backing up using a timestamp, it is recommended to specify the time zone as well. Otherwise, `br` uses the local time zone to construct the timestamp by default, which might lead to an incorrect backup time point. If you leave this parameter unspecified, `br` picks the snapshot corresponding to the backup start time.
- `--storage`: The storage address of the backup data. Snapshot backup supports Amazon S3, Google Cloud Storage, and Azure Blob Storage as backup storage. The preceding command uses Amazon S3 as an example. For more details, see [URI Formats of External Storage Services](/external-storage-uri.md).

During backup, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the backup task is completed and statistics such as total backup time, average backup speed, and backup data size are displayed.

- `total-ranges`: indicates the total number of files to be backed up.
- `ranges-succeed`: indicates the number of files that are successfully backed up.
- `ranges-failed`: indicates the number of files that failed to be backed up.
- `backup-total-ranges`: indicates the number of tables (including partitions) and indexes that are to be backed up.
- `write-CF-files`: indicates the number of backup SST files that contain `write CF` data.
- `default-CF-files`: indicates the number of backup SST files that contain `default CF` data.

```shell
Full Backup <-------------------------------------------------------------------------------> 100.00%
Checksum <----------------------------------------------------------------------------------> 100.00%
*** ["Full Backup success summary"] *** [total-ranges=20] [ranges-succeed=20] [ranges-failed=0] [backup-checksum=3.597416ms] [backup-fast-checksum=2.36975ms] [backup-total-ranges=11] [backup-total-regions=10] [write-CF-files=14] [default-CF-files=6] [total-take=4.715509333s] [BackupTS=435844546560000000] [total-kv=1131] [total-kv-size=250kB] [average-speed=53.02kB/s] [backup-data-size(after-compressed)=71.33kB] [Size=71330]
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

- `total-ranges`: indicates the total number of files that are to be restored.
- `ranges-succeed`: indicates the number of files that are successfully restored.
- `ranges-failed`: indicates the number of files that failed to be restored.
- `merge-ranges`: indicates the time taken to merge the data range.
- `split-region`: indicates the time taken to split and scatter Regions.
- `restore-files`: indicates the time TiKV takes to download and ingest SST files.
- `write-CF-files`: indicates the number of restored SST files that contain `write CF` data.
- `default-CF-files`: indicates the number of restored SST files that contain `default CF` data.
- `split-keys`: indicates the number of keys generated for splitting Regions.

```shell
Split&Scatter Region <--------------------------------------------------------------------> 100.00%
Download&Ingest SST <---------------------------------------------------------------------> 100.00%
Restore Pipeline <------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] [total-ranges=20] [ranges-succeed=20] [ranges-failed=0] [merge-ranges=7.546971ms] [split-region=343.594072ms] [restore-files=1.57662s] [default-CF-files=6] [write-CF-files=14] [split-keys=9] [total-take=4.344617542s] [total-kv=5] [total-kv-size=327B] [average-speed=75.27B/s] [restore-data-size(after-compressed)=4.813kB] [Size=4813] [BackupTS=435844901803917314]
```

During data restore, the table mode of the target table is automatically set to `restore`. Tables in `restore` mode do not allow any read or write operations. After data restore is complete, the table mode automatically switches back to `normal`, and you can read and write the table normally. This mechanism ensures task stability and data consistency throughout the restore process.

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

When you perform a snapshot backup, BR backs up system tables as tables with the `__TiDB_BR_Temporary_` prefix added to the database name. For example, BR backs up the `mysql.user` table as `__TiDB_BR_Temporary_mysql.user`. During the snapshot restore, BR first restores these tables with the `__TiDB_BR_Temporary_` prefix to avoid conflicts with existing system table data in the target cluster. While restoring system tables, BR writes the data from the tables with the `__TiDB_BR_Temporary_` prefix into the corresponding system tables using the `REPLACE INTO` statement.

- Starting from BR v5.1.0, when you back up snapshots, BR automatically backs up the **system tables** in the `mysql` schema, but does not restore these system tables by default.
- Starting from v6.2.0, BR lets you specify `--with-sys-table` to restore **data in some system tables**.
- Starting from v7.6.0, BR enables `--with-sys-table` by default, which means that BR restores **data in some system tables** by default.
- Starting from v8.5.5 and v9.0.0, BR lets you specify `--fast-load-sys-tables` to restore system tables physically. This approach uses the `RENAME TABLE` DDL statement to atomically swap the system tables in the `__TiDB_BR_Temporary_mysql` database with the system tables in the `mysql` database. Unlike the logical restoration of system tables using the `REPLACE INTO` SQL statement, physical restoration completely overwrites the existing data in the system tables.

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
- Other system tables

```
+-----------------------------------------------------+
| advisory_locks                                      |
| analyze_jobs                                        |
| analyze_options                                     |
| capture_plan_baselines_blacklist                    |
| column_stats_usage                                  |
| dist_framework_meta                                 |
| gc_delete_range                                     |
| gc_delete_range_done                                |
| global_variables                                    |
| help_topic                                          |
| index_advisor_results                               |
| plan_replayer_status                                |
| plan_replayer_task                                  |
| request_unit_by_group                               |
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
| table_cache_meta                                    |
| tidb                                                |
| tidb_background_subtask                             |
| tidb_background_subtask_history                     |
| tidb_ddl_history                                    |
| tidb_ddl_job                                        |
| tidb_ddl_notifier                                   |
| tidb_ddl_reorg                                      |
| tidb_global_task                                    |
| tidb_global_task_history                            |
| tidb_import_jobs                                    |
| tidb_mdl_info                                       |
| tidb_mdl_view                                       |
| tidb_pitr_id_map                                    |
| tidb_runaway_queries                                |
| tidb_runaway_watch                                  |
| tidb_runaway_watch_done                             |
| tidb_timers                                         |
| tidb_ttl_job_history                                |
| tidb_ttl_table_status                               |
| tidb_ttl_task                                       |
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

- Recommended method: Adjust the TiKV configuration parameter [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1), which controls the number of worker threads used by backup tasks. Because backup is a CPU-intensive operation, tuning this parameter allows for more precise control over TiKV’s CPU usage, enabling better resource isolation and predictability. In most scenarios, simply adjusting `num-threads` is sufficient to limit the impact of backup on the cluster. Internal testing shows that when the number of threads is set to `8` or fewer, and overall cluster CPU usage remains below 60%, the impact of backup on foreground workloads is negligible.

- Alternative method: If you have already set `backup.num-threads` to a small value (for example, `1`), but still want to further reduce the impact of backup on the cluster, consider using the `--ratelimit` parameter. This option limits the bandwidth used to write backup files to external storage, specified in MiB/s. Note that the actual rate limiting effect depends on the size of the compressed data. You can refer to the `backup data size (after compressed)` field in the logs for more insight. When `--ratelimit` is enabled, BR automatically sets `--concurrency` to `1` to reduce the number of concurrent requests.

> **Note:** 
>
> Enabling `--ratelimit` will further reduce backup throughput. In most cases, if you are already performing backups during off-peak hours and have reduced `backup.num-threads` to 1 but still observe backup impact on foreground workloads, it typically indicates that the cluster is approaching its resource limits.
>
> In such situations, consider the following alternatives:
>
> - [Scale out a cluster](/tiup/tiup-cluster.md#scale-out-a-cluster) to increase available resources.
> - Enable [`Log Backup`](/br/br-log-architecture.md) to offload backup pressure and minimize disruption to online workloads.

The impact of backup on cluster performance can be reduced by limiting the backup threads number, but this affects the backup performance. The preceding tests show that the backup speed is proportional to the number of backup threads. When the number of threads is small, the backup speed is about 20 MiB/thread. For example, 5 backup threads on a single TiKV node can reach a backup speed of 100 MiB/s.

### Performance and impact of snapshot restore

- During data restore, TiDB tries to fully utilize the TiKV CPU, disk IO, and network bandwidth resources. Therefore, it is recommended to restore the backup data on an empty cluster to avoid affecting the running applications.
- The speed of restoring backup data is much related with the cluster configuration, deployment, and running applications. The performance and impact of snapshot restore are varied in different user scenarios and should be tested in actual environments.
- BR provides a coarse-grained Region scattering algorithm to accelerate Region restore in large-scale Region scenarios. This algorithm ensures that each TiKV node receives stable and evenly distributed download tasks, thus fully utilizing the resources of each TiKV node and achieving a rapid parallel recovery. In several real-world cases, the snapshot restore speed of the cluster is improved by about 3 times in large-scale Region scenarios.
- Starting from v8.0.0, the `br` command-line tool introduces the `--tikv-max-restore-concurrency` parameter to control the maximum number of files that BR downloads and ingests per TiKV node. By configuring this parameter, you can also control the maximum length of the job queue (the maximum length of the job queue = 32 \* the number of TiKV nodes \* `--tikv-max-restore-concurrency`), thereby controlling the memory consumption of the BR node.

    In normal cases, `--tikv-max-restore-concurrency` is automatically adjusted based on the cluster configuration, so manual configuration is unnecessary. If the **TiKV-Details** > **Backup & Import** > **Import RPC count** monitoring metric in Grafana shows that the number of files BR downloads remains close to 0 for a long time while the number of files that BR ingests consistently reaches the upper limit, it indicates that ingesting file tasks pile up and the job queue has reached its maximum length. In this case, you can take the following measures to alleviate the task pilling-up issue:

    - Set the `--ratelimit` parameter to limit the download speed, ensuring sufficient resources for ingesting file tasks. For example, if the disk throughput of any TiKV node is `x MiB/s` and the network bandwidth for downloading backup files exceeds `x/2 MiB/s`, you can set the parameter as `--ratelimit x/2`. If the disk throughput of any TiKV node is `x MiB/s` and the network bandwidth for downloading backup files is less than or equal to `x/2 MiB/s`, you can leave the parameter `--ratelimit` unset.
    - Increase the `--tikv-max-restore-concurrency` to increase the maximum length of the job queue.

## See also

* [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)
* [br Command-line Manual](/br/use-br-command-line-tool.md)
* [TiDB Snapshot Backup and Restore Architecture](/br/br-snapshot-architecture.md)
