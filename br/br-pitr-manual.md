---
title: TiDB Log Backup and PITR Command Manual
summary: Introduce the commands used in TiDB log backup and point-in-time recovery (PITR).
aliases: ['/tidb/dev/br-log-command-line/']
---

# TiDB Log Backup and PITR Command Manual

This document describes the commands used in TiDB log backup and point-in-time recovery (PITR).

For more information about log backup and PITR, refer to:

- [Log Backup and PITR Guide](/br/br-pitr-guide.md)
- [Back up and Restore Use Cases](/br/backup-and-restore-use-cases.md)

## Perform log backup

You can start and manage log backup using the `tiup br log` command.

```shell
tiup br log --help

backup stream log from TiDB/TiKV cluster

Usage:
  br log [command]

Available Commands:
  metadata   get the metadata of log dir
  pause      pause a log backup task
  resume     resume a log backup task
  start      start a log backup task
  status     get status for the log backup task
  stop       stop a log backup task
  truncate   truncate the log data until sometime
```

Each subcommand is described as follows:

- `tiup br log start`: start a log backup task.
- `tiup br log status`: query the status of the log backup task.
- `tiup br log pause`: pause a log backup task.
- `tiup br log resume`: resume a paused log backup task.
- `tiup br log stop`: stop a log backup task and delete the task metadata.
- `tiup br log truncate`: clean up the log backup data from the backup storage.
- `tiup br log metadata`: query the metadata of the log backup data.

### Start a log backup task

You can run the `tiup br log start` command to start a log backup task. This task runs in the background of your TiDB cluster and automatically backs up the change log of KV storage to the backup storage.

Run `tiup br log start --help` to see the help information:

```shell
tiup br log start --help
start a log backup task

Usage:
  br log start [flags]

Flags:
  -h, --help               help for start
  --start-ts string        usually equals last full backupTS, used for backup log. Default value is current ts. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.
  --task-name string       The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"

```

The example output only shows the common parameters. These parameters are described as follows:

- `--start-ts`: specifies the start timestamp for the log backup. If this parameter is not specified, the backup program uses the current time as `start-ts`.
- `task-name`: specifies the task name for the log backup. This name is also used to query, pause, and resume the backup task.
- `--ca`, `--cert`, `--key`: specifies the mTLS encryption method to communicate with TiKV and PD.
- `--pd`: specifies the PD address for the backup cluster. BR needs to access PD to start the log backup task.
- `--storage`: specifies the backup storage address. Currently, BR supports Amazon S3, Google Cloud Storage (GCS), or Azure Blob Storage as the storage for log backup. The preceding command uses Amazon S3 as an example. For details, see [URI Formats of External Storage Services](/external-storage-uri.md).

Usage example:

```shell
tiup br log start \
  --task-name=pitr \
  --pd="${PD_IP}:2379" \
  --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

### Encrypt the log backup data

BR enables you to encrypt log backup data before uploading it to your backup storage.

Starting from TiDB v8.4.0, you can encrypt log backup data by passing the following parameters in the log backup command, which is similar to [snapshot backup encryption](/br/br-snapshot-manual.md#encrypt-the-backup-data):

- `--log.crypter.method`: Encryption algorithm, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted.
- `--log.crypter.key`: Encryption key in hexadecimal string format. It is a 128-bit (16 bytes) key for the algorithm `aes128-ctr`, a 24-byte key for the algorithm `aes192-ctr`, and a 32-byte key for the algorithm `aes256-ctr`.
- `--log.crypter.key-file`: The key file. You can directly pass in the file path where the key is stored as a parameter without passing in the `crypter.key`.

The following is an example:

```shell
tiup br log start \
    --task-name=pitr-with-encryption
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --log.crypter.method aes128-ctr \
    --log.crypter.key 0123456789abcdef0123456789abcdef
```

However, in scenarios with higher security requirements, you might not want to pass a fixed encryption key directly in the command line. To further enhance security, you can use a master key based encryption system to manage encryption keys. This system generates different data keys to encrypt different log backup files and supports master key rotation. You can configure it using the following parameters:

- `--master-key-crypter-method`: Encryption algorithm based on the master key, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted.
- `--master-key`: Master key configuration. It can be a master key stored on a local disk or a master key managed by a cloud Key Management Service (KMS).

Encrypt using a master key stored on a local disk:

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "local:///path/to/master.key"
```

Encrypt using a master key managed by AWS KMS:

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "aws-kms:///${AWS_KMS_KEY_ID}?AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY}&AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}&REGION=${AWS_REGION}"
```

Encrypt using a master key managed by Google Cloud KMS:

```shell
tiup br log start \
    --task-name=pitr-with-encryption \
    --pd ${PD_IP}:2379 \
    --storage "s3://${BACKUP_COLLECTION_ADDR}/snapshot-${DATE}?access-key=${AWS_ACCESS_KEY}&secret-access-key=${AWS_SECRET_ACCESS_KEY}" \
    --master-key-crypter-method aes128-ctr \
    --master-key "gcp-kms:///projects/$GCP_PROJECT_ID/locations/$GCP_LOCATION/keyRings/$GCP_KEY_RING/cryptoKeys/$GCP_KEY_NAME?AUTH=specified&CREDENTIALS=$GCP_CREDENTIALS_PATH"
```

> **Note:**
>
> - If the key is lost, the log backup data cannot be restored to the cluster.
> - The encryption feature needs to be used on `br` and TiDB clusters v8.4.0 or later versions. The encrypted log backup data cannot be restored on clusters earlier than v8.4.0.

### Query the log backup status

You can run the `tiup br log status` command to query the log backup status.

Run `tiup br log status --help` to see the help information:

```shell
tiup br log status --help
get status for the log backup task

Usage:
  br log status [flags]

Flags:
  -h, --help           help for status
  --json               Print JSON as the output.
  --task-name string   The task name for backup stream log. If default, get status of all of tasks (default "*")

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])

```

In the example output, `task-name` is used to specify the name of the backup task. The default value is `*`, which means querying the status of all tasks.

Usage example:

```shell
tiup br log status --task-name=pitr --pd="${PD_IP}:2379"
```

Expected output:

```shell
● Total 1 Tasks.
> #1 <
              name: pitr
            status: ● NORMAL
             start: 2022-07-14 20:08:03.268 +0800
               end: 2090-11-18 22:07:45.624 +0800
           storage: s3://backup-101/logbackup
       speed(est.): 0.82 ops/s
checkpoint[global]: 2022-07-25 22:52:15.518 +0800; gap=2m52s
```

The output fields are described as follows:

- `status`: the status of the backup task, which can be `NORMAL`, `ERROR`, or `PAUSE`.
- `start`: the start time of the backup task. It is the `start-ts` value specified when the backup task is started.
- `storage`: the backup storage address.
- `speed`: the total QPS of the backup task. QPS means the number of logs backed per second.
- `checkpoint [global]`: all data before this checkpoint is backed up to the backup storage. This is the latest timestamp available for restoring the backup data.
- `error [store]`: the error the log backup program encounters on the storage node.

### Pause and resume a log backup task

You can run the `tiup br log pause` command to pause a running log backup task.

Run `tiup br log pause --help` to see the help information:

```shell
tiup br log pause --help
pause a log backup task

Usage:
  br log pause [flags]

Flags:
  --gc-ttl int         the TTL (in seconds) that PD holds for BR's GC safepoint (default 86400)
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **Note:**
>
> - After the log backup task is paused, to prevent the MVCC data that generates the change log from being deleted, the backup program automatically sets the current backup checkpoint as the service safepoint, which retains MVCC data within the latest 24 hours. If the backup task is paused for more than 24 hours, the corresponding data is garbage collected and is not backed up.
> - Retaining too much MVCC data has a negative impact on the storage capacity and performance of the TiDB cluster. Therefore, it is recommended to resume the backup task in time.

Usage example:

```shell
tiup br log pause --task-name=pitr --pd="${PD_IP}:2379"
```

You can run the `tiup br log resume` command to resume a paused backup task.

Run `tiup br log resume --help` to see the help information:

```shell
tiup br log resume --help
resume a log backup task

Usage:
  br log resume [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for backup stream log.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

After the backup task is paused for more than 24 hours, running `tiup br log resume` reports an error, and BR prompts that backup data is lost. To handle this error, refer to [Backup & Restore FAQs](/faq/backup-and-restore-faq.md#what-should-i-do-if-the-error-message-errbackupgcsafepointexceeded-is-returned-when-using-the-br-log-resume-command-to-resume-a-suspended-task).

Usage example:

```shell
tiup br log resume --task-name=pitr --pd="${PD_IP}:2379"
```

### Stop and restart a log backup task

You can stop a log backup task by running the `tiup br log stop` command and restart a log backup task that is stopped by using the original `--storage` directory.

### Stop a log backup task

You can run the `tiup br log stop` command to stop a log backup task. This command cleans up the task metadata in the backup cluster.

Run `tiup br log stop --help` to see the help information:

```shell
tiup br log stop --help
stop a log backup task

Usage:
  br log stop [flags]

Flags:
  -h, --help           help for status
  --task-name string   The task name for the backup log task.

Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
```

> **Note:**
>
> Use this command with caution. If you need to pause a log backup task, use `tiup br log pause` and `tiup br log resume` instead.

Usage example:

```shell
tiup br log stop --task-name=pitr --pd="${PD_IP}:2379"
```

#### Restart a log backup task

After running the `tiup br log stop` command to stop a log backup task, you can create a new log backup task in another `--storage` directory or restart the log backup task in the original `--storage` directory by running the `tiup br log start` command. If you restart the task in the original `--storage` directory, pay attention to the following points:

- Parameters of the `--storage` directory for restarting a task must be the same as the task that is stopped.
- The `--start-ts` does not need to be specified. BR automatically starts the backup from the last backup checkpoint.
- If the task is stopped for a long time and multiple versions of the data have been garbage collected, the error `BR:Backup:ErrBackupGCSafepointExceeded` is reported when you attempt to restart the task. In this case, you have to create a new log backup task in another `--storage` directory.

### Clean up log backup data

You can run the `tiup br log truncate` command to clean up the outdated or no longer needed log backup data.

Run `tiup br log truncate --help` to see the help information:

```shell
tiup br log truncate --help
truncate the incremental log until sometime.

Usage:
  br log truncate [flags]

Flags:
  --dry-run        Run the command but don't really delete the files.
  -h, --help       help for truncate
  --until string   Remove all backup data until this TS.(support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'.)
  -y, --yes        Skip all prompts and always execute the command.


Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

This command only accesses the backup storage and does not access the TiDB cluster. Some parameters are described as follows:

- `--dry-run`: run the command but do not really delete the files.
- `--until`: delete all log backup data before the specified timestamp.
- `--storage`: the backup storage address. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI Formats of External Storage Services](/external-storage-uri.md).

Usage example:

```shell
tiup br log truncate --until='2022-07-26 21:20:00+0800' \
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

Expected output:

```shell
Reading Metadata... DONE; take = 277.911599ms
We are going to remove 9 files, until 2022-07-26 21:20:00.0000.
Sure? (y/N) y
Clearing data files... DONE; take = 43.504161ms, kv-count = 53, kv-size = 4573(4.573kB)
Removing metadata... DONE; take = 24.038962ms
```

### View the log backup metadata

You can run the `tiup br log metadata` command to view the log backup metadata in the storage system, such as the earliest and latest timestamp that can be restored.

Run `tiup br log metadata --help` to see the help information:

```shell
tiup br log metadata --help
get the metadata of log backup storage

Usage:
  br log metadata [flags]

Flags:
  -h, --help       help for metadata

Global Flags:
  -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

This command only accesses the backup storage and does not access the TiDB cluster.

The `--storage` parameter is used to specify the backup storage address. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI Formats of External Storage Services](/external-storage-uri.md).

Usage example:

```shell
tiup br log metadata --storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
```

Expected output:

```shell
[2022/07/25 23:02:57.236 +08:00] [INFO] [collector.go:69] ["log metadata"] [log-min-ts=434582449885806593] [log-min-date="2022-07-14 20:08:03.268 +0800"] [log-max-ts=434834300106964993] [log-max-date="2022-07-25 23:00:15.618 +0800"]
```

## Restore to a specified point in time (PITR)

> **Note:**
>
> - If you specify `--full-backup-storage` as the incremental backup address for `restore point`, for restores of this backup and any previous incremental backups, you need to set the parameter `--allow-pitr-from-incremental` to `true` to make the incremental backups compatible with the subsequent log backups.
> - For information about checksum configuration, see [Checksum](/br/br-snapshot-manual.md#checksum).

You can run the `tiup br restore point` command to perform a PITR on a new cluster or just restore the log backup data.

Run `tiup br restore point --help` to see the help information:

```shell
tiup br restore point --help
restore data from log until specify commit timestamp

Usage:
  br restore point [flags]

Flags:
  --full-backup-storage string specify the backup full storage. fill it if want restore full backup before restore log.
  -h, --help                   help for point
  --pitr-batch-count uint32    specify the batch count to restore log. (default 8)
  --pitr-batch-size uint32     specify the batch size to restore log. (default 16777216)
  --pitr-concurrency uint32    specify the concurrency to restore log. (default 16)
  --restored-ts string         the point of restore, used for log restore. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'
  --start-ts string            the start timestamp which log restore from. support TSO or datetime, e.g. '400036290571534337' or '2018-05-11 01:42:23+0800'


Global Flags:
 --ca string                  CA certificate path for TLS connection
 --cert string                Certificate path for TLS connection
 --key string                 Private key path for TLS connection
 -u, --pd strings             PD address (default [127.0.0.1:2379])
 -s, --storage string         specify the url where backup storage, eg, "s3://bucket/path/prefix"
```

The example output only shows the common parameters. These parameters are described as follows:

- `--full-backup-storage`: the storage address for the snapshot (full) backup. To use PITR, specify this parameter and choose the latest snapshot backup before the restore timestamp. To restore only log backup data, you can omit this parameter. Note that when initializing the recovery cluster for the first time, you must specify a snapshot backup. Currently, BR supports Amazon S3, GCS, and Azure Blob Storage as the storage for log backup. For details, see [URI Formats of External Storage Services](/external-storage-uri.md).
- `--pitr-batch-count`: the maximum number of files in a single batch when restoring log data. Once this threshold is reached, the current batch ends immediately and the next batch starts.
- `--pitr-batch-size`: the maximum data size (in bytes) in a single batch when restoring log data. Once this threshold is reached, the current batch ends immediately and the next batch starts.
- `--pitr-concurrency`: the number of concurrent tasks during log restore. Each concurrent task restores one batch of log data at a time.
- `--restored-ts`: the timestamp that you want to restore data to. If this parameter is not specified, BR restores data to the latest timestamp available in the log backup, that is, the checkpoint of the backup data.
- `--start-ts`: the start timestamp that you want to restore log backup data from. If you only need to restore log backup data, you must specify this parameter.
- `--pd`: the PD address of the restore cluster.
- `--ca`, `--cert`, `--key`: specify the mTLS encryption method to communicate with TiKV and PD.
- `--storage`: the storage address for the log backup. Currently, BR supports Amazon S3, GCS, or Azure Blob Storage as the storage for log backup. For details, see [URI Formats of External Storage Services](/external-storage-uri.md).

Usage example:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${access-key}&secret-access-key=${secret-access-key}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${access-key}&secret-access-key=${secret-access-key}'

Split&Scatter Region <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Download&Ingest SST <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore Pipeline <--------------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
*** ***["Full Restore success summary"] ****** [total-take=3.112928252s] [restore-data-size(after-compressed)=5.056kB] [Size=5056] [BackupTS=434693927394607136] [total-kv=4] [total-kv-size=290B] [average-speed=93.16B/s]
Restore Meta Files <--------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
Restore KV Files <----------------------------------------------------------------------------------------------------------------------------------------------------> 100.00%
"restore log success summary"] [total-take=192.955533ms] [restore-from=434693681289625602] [restore-to=434693753549881345] [total-kv-count=33] [total-size=21551]
```

> **Note:**
>
> - When you restore the cluster for the first time, you must specify the full snapshot data. Otherwise, some data in the newly created table might be incorrect due to rewriting Table ID rules. For more information, see GitHub issue [#54418](https://github.com/pingcap/tidb/issues/54418).
> - You cannot restore the log backup data of a certain time period repeatedly. If you restore the log backup data of a range `[t1=10, t2=20)` repeatedly, the restored data might be inconsistent.
> - When you restore log data of different time periods in multiple batches, ensure that the log data is restored in consecutive order. If you restore the log backup data of `[t1, t2)`, `[t2, t3)`, and `[t3, t4)` in consecutive order, the restored data is consistent. However, if you restore `[t1, t2)` and then skip `[t2, t3)` to restore `[t3, t4)`, the restored data might be inconsistent.

### Restore encrypted log backup data

To restore encrypted log backup data, you need to pass the corresponding decryption parameters in the restore command. Make sure that the decryption parameters are the same as those used for encryption. If the decryption algorithm or key is incorrect, the data cannot be restored.

The following is an example:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--log.crypter.method aes128-ctr
--log.crypter.key 0123456789abcdef0123456789abcdef
```

If a log backup is encrypted using a master key, you can decrypt and restore the backup data using the following command:

```shell
tiup br restore point --pd="${PD_IP}:2379"
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--full-backup-storage='s3://backup-101/snapshot-202205120000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'
--crypter.method aes128-ctr
--crypter.key 0123456789abcdef0123456789abcdef
--master-key-crypter-method aes128-ctr
--master-key "local:///path/to/master.key"
```

### Restore data using filters

Starting from TiDB v8.5.5 and v9.0.0, you can use filters during PITR to restore specific databases or tables, enabling more fine-grained control over the data to be restored.

The filter patterns follow the same [table filtering syntax](/table-filter.md) as other BR operations:

- `'*.*'`: matches all databases and tables.
- `'db1.*'`: matches all tables in the database `db1`.
- `'db1.table1'`: matches the specific table `table1` in the database `db1`.
- `'db*.tbl*'`: matches databases starting with `db` and tables starting with `tbl`.
- `'!mysql.*'`: excludes all tables in the `mysql` database.

Usage examples:

```shell
# restore specific databases
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.*' --filter 'db2.*'

# restore specific tables
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.users' --filter 'db1.orders'

# restore using pattern matching
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db*.tbl*'
```

> **Note:**
>
> - Before restoring data using filters, ensure that the target cluster does not contain any databases or tables that match the filter. Otherwise, the restore will fail with an error.
> - The filter options apply during the restore phase for both snapshot and log backups.
> - You can specify multiple `--filter` options to include or exclude different patterns.
> - PITR filtering does not support system tables yet. If you need to restore specific system tables, use the `br restore full` command with filters instead. Note that this command restores only the snapshot backup data (not log backup data).
> - The regular expression in the restore task matches the table name at the `restored-ts` time point, with the following three possible cases:
>     - Table A (table id = 1): the table name always matches the `--filter` regular expression at and before the `restored-ts` time point. In this case, PITR restores the table.
>     - Table B (table id = 2): the table name does not match the `--filter` regular expression at some point before `restored-ts`, but matches at the `restored-ts` time point. In this case, PITR restores the table.
>     - Table C (table id = 3): the table name matches the `--filter` regular expression at some point before `restored-ts`, but does **not** match at the `restored-ts` time point. In this case, PITR does **not** restore the table.
> - You can use the database and table filtering feature to restore part of the data online. During the online restore process, do **not** create databases or tables with the same names as the restored objects, otherwise the restore task fails due to conflicts. To avoid data inconsistency, the tables created by PITR during this restore process are not readable or writable until the restore task is complete.

### Concurrent restore operations

Starting from TiDB v8.5.5 and v9.0.0, you can run multiple PITR restore tasks concurrently. This feature allows you to restore different datasets in parallel, improving efficiency for large-scale restore scenarios.

Usage example for concurrent restores:

```shell
# terminal 1 - restore database db1
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db1.*'

# terminal 2 - restore database db2 (can run simultaneously)
tiup br restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--start-ts "2025-06-02 00:00:00+0800" \
--restored-ts "2025-06-03 18:00:00+0800" \
--filter 'db2.*'
```

> **Note:**
>
> - Each concurrent restore operation must target a different database or a non-overlapping set of tables. Attempting to restore overlapping datasets concurrently will result in an error.
> - Multiple restore tasks consume a lot of system resources. It is recommended to run concurrent restore tasks only when CPU and I/O resources are sufficient.

### Compatibility between ongoing log backup and snapshot restore

Starting from v8.5.5 and v9.0.0, when a log backup task is running, if all of the following conditions are met, you can still perform snapshot restore (`br restore [full|database|table]`) and allow the restored data to be properly recorded by the ongoing log backup (hereinafter referred to as "log backup"):

- The node performing backup and restore operations has the following necessary permissions: 
    - Read access to the external storage containing the backup source, for snapshot restore
    - Write access to the target external storage used by the log backup
- The target external storage for the log backup is Amazon S3 (`s3://`), Google Cloud Storage (`gcs://`), or Azure Blob Storage (`azblob://`).
- The data to be restored uses the same type of external storage as the target storage for the log backup.
- Neither the data to be restored nor the log backup has enabled local encryption. For details, see [log backup encryption](#encrypt-the-log-backup-data) and [snapshot backup encryption](/br/br-snapshot-manual.md#encrypt-the-backup-data).

If any of the above conditions are not met, you can restore the data by following these steps:

1. [Stop the log backup task](#stop-a-log-backup-task).
2. Perform the data restore.
3. After the restore is complete, perform a new snapshot backup.
4. [Restart the log backup task](#restart-a-log-backup-task).

> **Note:**
>
> When restoring a log backup that contains records of snapshot (full) restore data, you must use BR v8.5.5 or later. Otherwise, restoring the recorded full restore data might fail.

### Compatibility between ongoing log backup and PITR operations

Starting from TiDB v8.5.5 and v9.0.0, you can perform PITR operations while a log backup task is running by default. The system automatically handles compatibility between these operations.

#### Important limitation for PITR with ongoing log backup

When you perform the PITR operations while a log backup is running, the restored data will also be recorded in the ongoing log backup. However, due to the nature of log restore operations, data inconsistencies might occur within the restore window. The system writes metadata to external storage to mark both the time range and data range where consistency cannot be guaranteed.

If such inconsistency occurs during the time range `[t1, t2)`, you cannot directly restore data from this period. Instead, choose one of the following alternatives:

- Restore data up to `t1` (to retrieve data before the inconsistent period).
- Perform a new snapshot backup after `t2`, and use it as the base for future PITR operations.

### Abort restore operations

If a restore operation fails, you can use the `tiup br abort` command to clean up registry entries and checkpoint data. This command automatically locates and removes relevant metadata based on the original restore parameters, including entries in the `mysql.tidb_restore_registry` table and checkpoint data (regardless of whether it is stored in a local database or external storage).

> **Note:**
>
> The `abort` command only cleans up metadata. You need to manually delete any actual restored data from the cluster.

The examples of aborting restore operations using the same parameters as the original restore command are as follows:

```shell
# Abort a PITR operation
tiup br abort restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'

# Abort a PITR operation with filters
tiup br abort restore point --pd="${PD_IP}:2379" \
--storage='s3://backup-101/logbackup?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--full-backup-storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--filter 'db1.*'

# Abort a full restore
tiup br abort restore full --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}'

# Abort a database restore
tiup br abort restore db --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--db database_name

# Abort a table restore
tiup br abort restore table --pd="${PD_IP}:2379" \
--storage='s3://backup-101/snapshot-20250602000000?access-key=${ACCESS-KEY}&secret-access-key=${SECRET-ACCESS-KEY}' \
--db database_name --table table_name
```
