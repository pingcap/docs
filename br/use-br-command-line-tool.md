---
title: Use BR Command-line for Backup and Restoration
summary: Learn how to use the BR command line to backup and restore cluster data.
---

# Use BR Command-line for Backup and Restoration

This document describes how to back up and restore TiDB cluster data using the BR command line.

Make sure you have read [BR Tool Overview](/br/backup-and-restore-tool.md), especially [Usage Restrictions](/br/backup-and-restore-tool.md#usage-restrictions) and [Best Practices](/br/backup-and-restore-tool.md#best-practices).

## BR command-line description

A `br` command consists of sub-commands, options, and parameters.

* Sub-command: the characters without `-` or `--`.
* Option: the characters that start with `-` or `--`.
* Parameter: the characters that immediately follow behind and are passed to the sub-command or the option.

This is a complete `br` command:

{{< copyable "shell-regular" >}}

```shell
br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"
```

Explanations for the above command are as follows:

* `backup`: the sub-command of `br`.
* `full`: the sub-command of `backup`.
* `-s` (or `--storage`): the option that specifies the path where the backup files are stored.
* `"local:///tmp/backup"`: the parameter of `-s`. `/tmp/backup` is the path in the local disk where the backed up files of each TiKV node are stored.
* `--pd`: the option that specifies the Placement Driver (PD) service address.
* `"${PDIP}:2379"`: the parameter of `--pd`.

> **Note:**
>
> - When the `local` storage is used, the backup data are scattered in the local file system of each node.
>
> - It is **not recommended** to back up to a local disk in the production environment because you **have to** manually aggregate these data to complete the data restoration. For more information, see [Restore Cluster Data](#use-br-command-line-to-restore-cluster-data).
>
> - Aggregating these backup data might cause redundancy and bring troubles to operation and maintenance. Even worse, if restoring data without aggregating these data, you can receive a rather confusing error message `SST file not found`.
>
> - It is recommended to mount the NFS disk on each node, or back up to the `S3` object storage.

### Sub-commands

A `br` command consists of multiple layers of sub-commands. Currently, BR has the following three sub-commands:

* `br backup`: used to back up the data of the TiDB cluster.
* `br restore`: used to restore the data of the TiDB cluster.

Each of the above three sub-commands might still include the following three sub-commands to specify the scope of an operation:

* `full`: used to back up or restore all the cluster data.
* `db`: used to back up or restore the specified database of the cluster.
* `table`: used to back up or restore a single table in the specified database of the cluster.

### Common options

* `--pd`: used for connection, specifying the PD server address. For example, `"${PDIP}:2379"`.
* `-h` (or `--help`): used to get help on all sub-commands. For example, `br backup --help`.
* `-V` (or `--version`): used to check the version of BR.
* `--ca`: specifies the path to the trusted CA certificate in the PEM format.
* `--cert`: specifies the path to the SSL certificate in the PEM format.
* `--key`: specifies the path to the SSL certificate key in the PEM format.
* `--status-addr`: specifies the listening address through which BR provides statistics to Prometheus.

## Use BR command-line to back up cluster data

To back up the cluster data, use the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster or a single table.

### Back up all the cluster data

To back up all the cluster data, execute the `br backup full` command. To get help on this command, execute `br backup full -h` or `br backup full --help`.

**Usage example:**

Back up all the cluster data to the `/tmp/backup` path of each TiKV node and write the `backupmeta` file to this path.

> **Note:**
>
> + If the backup disk and the service disk are different, it has been tested that online backup reduces QPS of the read-only online service by about 15%-25% in case of full-speed backup. If you want to reduce the impact on QPS, use `--ratelimit` to limit the rate.
>
> + If the backup disk and the service disk are the same, the backup competes with the service for I/O resources. This might decrease the QPS of the read-only online service by more than half. Therefore, it is **highly not recommended** to back up the online service data to the TiKV data disk.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

Explanations for some options in the above command are as follows:

* `--ratelimit`: specifies the maximum speed at which a backup operation is performed (MiB/s) on each TiKV node.
* `--log-file`: specifies writing the BR log to the `backupfull.log` file.

A progress bar is displayed in the terminal during the backup. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data safety. The progress bar is displayed as follows:

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### Back up a database

To back up a database in the cluster, execute the `br backup db` command. To get help on this command, execute `br backup db -h` or `br backup db --help`.

**Usage example:**

Back up the data of the `test` database to the `/tmp/backup` path on each TiKV node and write the `backupmeta` file to this path.

{{< copyable "shell-regular" >}}

```shell
br backup db \
    --pd "${PDIP}:2379" \
    --db test \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backuptable.log
```

In the above command, `--db` specifies the name of the database to be backed up. For descriptions of other options, see [Back up all the cluster data](#use-br-command-line-to-back-up-cluster-data).

A progress bar is displayed in the terminal during the backup. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data safety.

### Back up a table

To back up the data of a single table in the cluster, execute the `br backup table` command. To get help on this command, execute `br backup table -h` or `br backup table --help`.

**Usage example:**

Back up the data of the `test.usertable` table to the `/tmp/backup` path on each TiKV node and write the `backupmeta` file to this path.

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backuptable.log
```

The `table` sub-command has two options:

* `--db`: specifies the database name
* `--table`: specifies the table name.

For descriptions of other options, see [Back up all cluster data](#use-br-command-line-to-back-up-cluster-data).

A progress bar is displayed in the terminal during the backup operation. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data safety.

### Back up with table filter

To back up multiple tables with more complex criteria, execute the `br backup full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

**Usage example:**

The following command backs up the data of all tables in the form `db*.tbl*` to the `/tmp/backup` path on each TiKV node and writes the `backupmeta` file to this path.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file backupfull.log
```

### Back up data to Amazon S3 backend

If you back up the data to the Amazon S3 backend, instead of `local` storage, you need to specify the S3 storage path in the `storage` sub-command, and allow the BR node and the TiKV node to access Amazon S3.

You can refer to the [AWS Official Document](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) to create an S3 `Bucket` in the specified `Region`. You can also refer to another [AWS Official Document](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html) to create a `Folder` in the `Bucket`.

> **Note:**
>
> To complete one backup, TiKV and BR usually require the minimum privileges of `s3:ListBucket`, `s3:PutObject`, and `s3:AbortMultipartUpload`.

Pass `SecretKey` and `AccessKey` of the account that has privilege to access the S3 backend to the BR node. Here `SecretKey` and `AccessKey` are passed as environment variables. Then pass the privilege to the TiKV node through BR.

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

When backing up using BR, explicitly specify the parameters `--s3.region` and `--send-credentials-to-tikv`. `--s3.region` indicates the region where S3 is located, and `--send-credentials-to-tikv` means passing the privilege to access S3 to the TiKV node.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --send-credentials-to-tikv=true \
    --ratelimit 128 \
    --log-file backuptable.log
```

### Back up incremental data

If you want to back up incrementally, you only need to specify the **last backup timestamp** `--lastbackupts`.

The incremental backup has two limitations:

- The incremental backup needs to be under a different path from the previous full backup.
- GC (Garbage Collection) safepoint must be before the `lastbackupts`.

To back up the incremental data between `(LAST_BACKUP_TS, current PD timestamp]`, execute the following command:

{{< copyable "shell-regular" >}}

```shell
br backup full\
    --pd ${PDIP}:2379 \
    --ratelimit 128 \
    -s local:///home/tidb/backupdata/incr \
    --lastbackupts ${LAST_BACKUP_TS}
```

To get the timestamp of the last backup, execute the `validate` command. For example:

{{< copyable "shell-regular" >}}

```shell
LAST_BACKUP_TS=`br validate decode --field="end-version" -s local:///home/tidb/backupdata | tail -n1`
```

In the above example, for the incremental backup data, BR records the data changes and the DDL operations during `(LAST_BACKUP_TS, current PD timestamp]`. When restoring data, BR first restores DDL operations and then the data.

### Point-in-time recovery (experimental feature)

Point-in-time recovery (PITR) allows you to restore data to a point in time of your choice.

An example scenario would be to take a full backup every day and take incremental backups every 6 hours and then use TiCDC for PITR. Assume that on one day, the full backup was performed at 00:00 and the first incremental backup was performed at 06:00. If you want to restore the database to the state of 07:16, you can first restore the full backup (taken at 00:00) and the incremental backup (taken at 06:00), and then restore TiCDC logs that fill in the gap between 06:00 and 07:16.

To peform the PITR, you can take the following steps:

1. Restore a full backup using `br restore full`.
2. (optional) Restore incremental backup(s).
3. Use `br restore cdclog` to restore the transactions that happened after the last incremental backup. The complete command to execute is as follows:

    ```shell
    br restore cdclog --storage local:///data/cdclog --start-ts $START_TS --end-ts $END_TS
    ```

    In the command above:

    - `local:///data/cdclog` is the location of the TiCDC logs. This might be on the local filesystem or on the external storage like S3.
    - `$START_TS` is the end position of the restore from the last restored backup (either a full backup or an incremental backup).
    - `$END_TS` is the point to which you want to restore your data.

### Back up Raw KV (experimental feature)

> **Warning:**
>
> This feature is experimental and not thoroughly tested. It is highly **not recommended** to use this feature in the production environment.

In some scenarios, TiKV might run independently of TiDB. Given that, BR also supports bypassing the TiDB layer and backing up data in TiKV.

For example, you can execute the following command to back up all keys between `[0x31, 0x3130303030303030)` in the default CF to `$BACKUP_DIR`:

{{< copyable "shell-regular" >}}

```shell
br backup raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --ratelimit 128 \
    --end 3130303030303030 \
    --format hex \
    --cf default
```

Here, the parameters of `--start`  and `--end` are decoded using the method specified by `--format` before being sent to TiKV. Currently, the following methods are available:

- "raw": The input string is directly encoded as a key in binary format.
- "hex": The default encoding method. The input string is treated as a hexadecimal number.
- "escape": First escape the input string, and then encode it into binary format.

## Use BR command-line to restore cluster data

To restore the cluster data, use the `br restore` command. You can add the `full`, `db` or `table` sub-command to specify the scope of your restoration: the whole cluster, a database or a single table.

> **Note:**
>
> If you use the local storage, you **must** copy all back up SST files to every TiKV node in the path specified by `--storage`.
>
> Even if each TiKV node eventually only need to read a part of the all SST files, they all need full access to the complete archive because:
>
> - Data are replicated into multiple peers. When ingesting SSTs, these files have to be present on *all* peers. This is unlike back up where reading from a single node is enough.
> - Where each peer is scattered to during restore is random. We don't know in advance which node will read which file.
>
> These can be avoided using shared storage, for example mounting an NFS on the local path, or using S3. With network storage, every node can automatically read every SST file, so these caveats no longer apply.

### Restore all the backup data

To restore all the backup data to the cluster, execute the `br restore full` command. To get help on this command, execute `br restore full -h` or `br restore full --help`.

**Usage example:**

Restore all the backup data in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
```

Explanations for some options in the above command are as follows:

* `--ratelimit`: specifies the maximum speed at which a restoration operation is performed (MiB/s) on each TiKV node.
* `--log-file`: specifies writing the BR log to the `restorefull.log` file.

A progress bar is displayed in the terminal during the restoration. When the progress bar advances to 100%, the restoration is complete. Then the BR also checks the backup data to ensure data safety.

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 128 \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### Restore a database

To restore a database to the cluster, execute the `br restore db` command. To get help on this command, execute `br restore db -h` or `br restore db --help`.

**Usage example:**

Restore a database backed up in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--db` specifies the name of the database to be restored. For descriptions of other options, see [Restore all backup data](#restore-all-the-backup-data)).

> **Note:**
>
> When you restore the backup data, the name of the database specified by `--db` must be the same as the one specified by `-- db` in the backup command. Otherwise, the restore fails. This is because the metafile of the backup data ( `backupmeta` file) records the database name, you can only restore data to the database with the same name. The recommended method is to restore the backup data to the database with the same name in another cluster.

### Restore a table

To restore a single table to the cluster, execute the `br restore table` command. To get help on this command, execute `br restore table -h` or `br restore table --help`.

**Usage example:**

Restore a table backed up in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--table` specifies the name of the table to be restored. For descriptions of other options, see [Restore all backup data](#restore-all-the-backup-data) and [Restore a database](#restore-a-database).

### Restore with table filter

To restore multiple tables with more complex criteria, execute the `br restore full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

**Usage example:**

The following command restores a subset of tables backed up in the `/tmp/backup` path to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --filter 'db*.tbl*' \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

### Restore data from Amazon S3 backend

If you restore data from the Amazon S3 backend, instead of `local` storage, you need to specify the S3 storage path in the `storage` sub-command, and allow the BR node and the TiKV node to access Amazon S3.

> **Note:**
>
> To complete one restore, TiKV and BR usually require the minimum privileges of `s3:ListBucket` and `s3:GetObject`.

Pass `SecretKey` and `AccessKey` of the account that has privilege to access the S3 backend to the BR node. Here `SecretKey` and `AccessKey` are passed as environment variables. Then pass the privilege to the TiKV node through BR.

{{< copyable "shell-regular" >}}

```shell
export AWS_ACCESS_KEY_ID=${AccessKey}
export AWS_SECRET_ACCESS_KEY=${SecretKey}
```

When restoring data using BR, explicitly specify the parameters `--s3.region` and `--send-credentials-to-tikv`. `--s3.region` indicates the region where S3 is located, and `--send-credentials-to-tikv` means passing the privilege to access S3 to the TiKV node.

`Bucket` and `Folder` in the `--storage` parameter represent the S3 bucket and the folder where the data to be restored is located.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "s3://${Bucket}/${Folder}" \
    --s3.region "${region}" \
    --ratelimit 128 \
    --send-credentials-to-tikv=true \
    --log-file restorefull.log
```

In the above command, `--table` specifies the name of the table to be restored. For descriptions of other options, see [Restore a database](#restore-a-database).

### Restore incremental data

Restoring incremental data is similar to [restoring full data using BR](#restore-all-the-backup-data). Note that when restoring incremental data, make sure that all the data backed up before `last backup ts` has been restored to the target cluster.

### Restore tables created in the `mysql` schema (experimental feature)

BR backs up tables created in the `mysql` schema by default.

When you restore data using BR, the tables created in the `mysql` schema are not restored by default. If you need to restore these tables, you can explicitly include them using the [table filter](/table-filter.md#syntax). The following example restores `mysql.usertable` created in `mysql` schema. The command restores `mysql.usertable` along with other data.

{{< copyable "shell-regular" >}}

```shell
br restore full -f '*.*' -f '!mysql.*' -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

In the above command, `-f '*.*'` is used to override the default rules and `-f '!mysql.*'` instructs BR not to restore tables in `mysql` unless otherwise stated. `-f 'mysql.usertable'` indicates that `mysql.usertable` is required for restore. For detailed implementation, refer to the [table filter document](/table-filter.md#syntax).

If you only need to restore `mysql.usertable`, use the following command:

{{< copyable "shell-regular" >}}

```shell
br restore full -f 'mysql.usertable' -s $external_storage_url --ratelimit 128
```

> **Warning:**
>
> Although you can back up system tables (such as `mysql.tidb`) using the BR tool, BR ignores the following system tables even if you use the `--filter` setting to perform the restoration:
>
> - Statistical information tables (`mysql.stat_*`)
> - System variable tables (`mysql.tidb`，`mysql.global_variables`)
> - User information tables (such as `mysql.user` and `mysql.columns_priv`)
> - GC data
>
> Restoring system tables might cause more compatibility issues. To avoid unexpected issues, **DO NOT** restore system tables in the production environment.

### Restore Raw KV (experimental feature)

> **Warning:**
>
> This feature is in the experiment, without being thoroughly tested. It is highly **not recommended** to use this feature in the production environment.

Similar to [backing up Raw KV](#back-up-raw-kv-experimental-feature), you can execute the following command to restore Raw KV:

{{< copyable "shell-regular" >}}

```shell
br restore raw --pd $PD_ADDR \
    -s "local://$BACKUP_DIR" \
    --start 31 \
    --end 3130303030303030 \
    --ratelimit 128 \
    --format hex \
    --cf default
```

In the above example, all the backed up keys in the range `[0x31, 0x3130303030303030)` are restored to the TiKV cluster. The coding methods of these keys are identical to that of [keys during the backup process](#back-up-raw-kv-experimental-feature)

### Online restore (experimental feature)

> **Warning:**
>
> This feature is in the experiment, without being thoroughly tested. It also relies on the unstable `Placement Rules` feature of PD. It is highly **not recommended** to use this feature in the production environment.

During data restoration, writing too much data affects the performance of the online cluster. To avoid this effect as much as possible, BR supports [Placement rules](/configure-placement-rules.md) to isolate resources. In this case, downloading and importing SST are only performed on a few specified nodes (or "restore nodes" for short). To complete the online restore, take the following steps.

1. Configure PD, and start Placement rules:

    {{< copyable "shell-regular" >}}

    ```shell
    echo "config set enable-placement-rules true" | pd-ctl
    ```

2. Edit the configuration file of the "restore node" in TiKV, and specify "restore" to the `server` configuration item:

    {{< copyable "" >}}

    ```
    [server]
    labels = { exclusive = "restore" }
    ```

3. Start TiKV of the "restore node" and restore the backed up files using BR. Compared with the offline restore, you only need to add the `--online` flag:

    {{< copyable "shell-regular" >}}

    ```
    br restore full \
        -s "local://$BACKUP_DIR" \
        --ratelimit 128 \
        --pd $PD_ADDR \
        --online
    ```
