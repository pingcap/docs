---
title: TiDB Log Backup and PITR Guide
summary: TiDB Log Backup and PITR Guide explains how to back up and restore data using the br command-line tool. It includes instructions for starting log backup, running full backup regularly, and cleaning up outdated data. The guide also provides information on running PITR and the performance capabilities of PITR.
---

# TiDB Log Backup and PITR Guide

A full backup (snapshot backup) contains the full cluster data at a certain point, while TiDB log backup can back up data written by applications to a specified storage in a timely manner. If you want to choose the restore point as required, that is, to perform point-in-time recovery (PITR), you can [start log backup](#start-log-backup) and [run full backup regularly](#run-full-backup-regularly).

Before you back up or restore data using the br command-line tool (hereinafter referred to as `br`), you need to [install `br`](/br/br-use-overview.md#deploy-and-use-br) first.

## Back up TiDB cluster

### Start log backup

> **Note:**
>
> - The following examples assume that Amazon S3 access keys and secret keys are used to authorize permissions. If IAM roles are used to authorize permissions, you need to set `--send-credentials-to-tikv` to `false`.
> - If other storage systems or authorization methods are used to authorize permissions, adjust the parameter settings according to [Backup Storages](/br/backup-and-restore-storages.md).

To start a log backup, run `tiup br log start`. A cluster can only run one log backup task each time.

```shell
tiup br log start --task-name=pitr --pd "${PD_IP}:2379" \
--storage 's3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

### Query the status of the log backup

After the log backup task starts, it runs in the background of the TiDB cluster until you stop it manually. During this process, the TiDB change logs are regularly backed up to the specified storage in small batches. To query the status of the log backup task, run the following command:

```shell
tiup br log status --task-name=pitr --pd "${PD_IP}:2379"
```

Expected output:

```
● Total 1 Tasks.
> #1 <
           name: pitr
         status: ● NORMAL
          start: 2022-05-13 11:09:40.7 +0800
            end: 2035-01-01 00:00:00 +0800
        storage: s3://backup-101/log-backup
    speed(est.): 0.00 ops/s
checkpoint[global]: 2022-05-13 11:31:47.2 +0800; gap=4m53s
```

The fields are explained as follows:

- `name`: the name of the log backup task.
- `status`: the status of the log backup task, including `NORMAL`, `PAUSED`, and `ERROR`.
- `start`: the start timestamp of the log backup task.
- `end`: the end timestamp of the log backup task. Currently, this field does not take effect.
- `storage`: the URI of the external storage for the log backup.
- `speed(est.)`: the current data transfer rate of the log backup. This value is estimated based on traffic samples taken in the past few seconds. For more accurate traffic statistics, you can check the `Log Backup` row in the **[TiKV-Details](/grafana-tikv-dashboard.md#tikv-details-dashboard)** dashboard at Grafana.
- `checkpoint[global]`: the current progress of the log backup. You can use PITR to restore to a point in time before this timestamp.

If the log backup task is paused, the `log status` command outputs additional fields to display the details of the pause. They are:

- `pause-time`: the time when the pause operation is executed.
- `pause-operator`: the hostname of the machine that executes the pause operation.
- `pause-operator-pid`: the PID of the process that executes the pause operation.
- `pause-payload`: additional information attached when the task is paused.

If the pause is due to an error in TiKV, you might also see additional error reports from TiKV:

- `error[store=*]`: the error code on TiKV.
- `error-happen-at[store=*]`: the time when the error occurs on TiKV.
- `error-message[store=*]`: the error message on TiKV.

### Run full backup regularly

The snapshot backup can be used as a method of full backup. You can run `tiup br backup full` to back up the cluster snapshot to the backup storage according to a fixed schedule (for example, every 2 days).

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage 's3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

## Run PITR

To restore the cluster to any point in time within the backup retention period, you can use `tiup br restore point`. When you run this command, you need to specify the **time point you want to restore**, **the latest snapshot backup data before the time point**, and the **log backup data**. BR will automatically determine and read data needed for the restore, and then restore these data to the specified cluster in order.

```shell
tiup br restore point --pd "${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--full-backup-storage='s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}' \
--restored-ts '2022-05-15 18:00:00+0800'
```

During data restore, you can view the progress through the progress bar in the terminal. The restore is divided into two phases, full restore and log restore (restore meta files and restore KV files). After each phase is completed, `br` outputs information such as restore time and data size.

```shell
Split&Scatter Region <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Download&Ingest SST <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore Pipeline <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["Full Restore success summary"] ****** [total-take=xxx.xxxs] [restore-data-size(after-compressed)=xxx.xxx] [Size=xxxx] [BackupTS={TS}] [total-kv=xxx] [total-kv-size=xxx] [average-speed=xxx]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ["restore log success summary"] [total-take=xxx.xx] [restore-from={TS}] [restore-to={TS}] [total-kv-count=xxx] [total-size=xxx]
```

During data restore, the table mode of the target table is automatically set to `restore`. Tables in `restore` mode do not allow any read or write operations. After data restore is complete, the table mode automatically switches back to `normal`, and you can read and write the table normally. This mechanism ensures task stability and data consistency throughout the restore process.

## Clean up outdated data

As described in the [Usage Overview of TiDB Backup and Restore](/br/br-use-overview.md):

To perform PITR, you need to restore the full backup before the restore point, and the log backup between the full backup point and the restore point. Therefore, for log backups that exceed the backup retention period, you can use `tiup br log truncate` to delete the backup before the specified time point. **It is recommended to only delete the log backup before the full snapshot**.

The following steps describe how to clean up backup data that exceeds the backup retention period:

1. Get the **last full backup** outside the backup retention period.
2. Use the `validate` command to get the time point corresponding to the backup. Assume that the backup data before 2022/09/01 needs to be cleaned, you should look for the last full backup before this time point and ensure that it will not be cleaned.

    ```shell
    FULL_BACKUP_TS=`tiup br validate decode --field="end-version" --storage "s3://backup-101/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}"| tail -n1`
    ```

3. Delete log backup data earlier than the snapshot backup `FULL_BACKUP_TS`:

    ```shell
    tiup br log truncate --until=${FULL_BACKUP_TS} --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
    ```

4. Delete snapshot data earlier than the snapshot backup `FULL_BACKUP_TS`:

    ```shell
    aws s3 rm --recursive s3://backup-101/snapshot-${date}
    ```

## Performance capabilities of PITR

- On each TiKV node, PITR can restore snapshot data (full restore) at a speed of 2 TiB/h and log data (including meta files and KV files) at a speed of 30 GiB/h.
- BR deletes outdated log backup data (`tiup br log truncate`) at a speed of 600 GB/h.

> **Note:**
>
> The preceding specifications are based on test results from the following two testing scenarios. The actual data might be different.
>
> - Snapshot data restore speed = Total size of restored snapshot data on all TiKV nodes in the cluster / (duration * the number of TiKV nodes)
> - Log data restore speed = Total size of restored log data on all TiKV nodes in the cluster / (duration * the number of TiKV nodes)
>
> External storage only contains KV data of a single replica. Therefore, the data size in external storage does not represent the actual data size restored in the cluster. BR restores all replicas according to the number of replicas configured for the cluster. The more replicas there are, the more data can be actually restored.
> The default replica number for all clusters in the test is 3.
> To improve the overall restore performance, you can modify the [`import.num-threads`](/tikv-configuration-file.md#import) item in the TiKV configuration file and the [`pitr-concurrency`](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr) option in the BR command.
> When the upstream cluster has **many Regions** and a **short flush interval**, PITR generates a large number of small files. This increases batching and dispatching overhead during restore. To raise the number of files processed per batch, you can **moderately** increase the values of the following parameters:
>
> - `pitr-batch-size`: cumulative **bytes per batch** (default **16 MiB**).
> - `pitr-batch-count`: **number of files per batch** (default **8**).
>
> When determining whether to start the next batch, these two thresholds are evaluated independently: whichever threshold is reached first closes the current batch and starts the next, while the other threshold is ignored for that batch.

Testing scenario 1 (on [TiDB Cloud](https://tidbcloud.com)) is as follows:

- The number of TiKV nodes (8 core, 16 GB memory): 21
- TiKV configuration item `import.num-threads`: 8
- BR command option `pitr-concurrency`: 128
- The number of Regions: 183,000
- New log data created in the cluster: 10 GB/h
- Write (INSERT/UPDATE/DELETE) QPS: 10,000

Testing scenario 2 (on TiDB Self-Managed) is as follows:

- The number of TiKV nodes (8 core, 64 GB memory): 6
- TiKV configuration item `import.num-threads`: 8
- BR command option `pitr-concurrency`: 128
- The number of Regions: 50,000
- New log data created in the cluster: 10 GB/h
- Write (INSERT/UPDATE/DELETE) QPS: 10,000

## Monitoring and alert

After log backup tasks are distributed, each TiKV node continuously writes data to external storage. You can view the monitoring data for this process in the **TiKV-Details > Backup Log** dashboard.

To receive notifications metrics deviate from normal ranges, see [Log backup alerts](/br/br-monitoring-and-alert.md#log-backup-alerts) to configure alert rules.

## See also

* [TiDB Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)
* [br Command-line Manual](/br/use-br-command-line-tool.md)
* [Log Backup and PITR Architecture](/br/br-log-architecture.md)
* [Monitoring and Alert for Backup and Restore](/br/br-monitoring-and-alert.md)
