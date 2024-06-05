---
title: TiDB Snapshot Backup and Restore Command Manual
summary: TiDB Snapshot Backup and Restore Command Manual describes commands for backing up and restoring cluster snapshots, databases, and tables. It also covers encrypting backup data and restoring encrypted snapshots. The BR tool supports self-adapting to GC and introduces the --ignore-stats parameter for backing up and restoring statistics. It also supports encrypting backup data and restoring partial data of specified databases or tables.
---

# TiDB Snapshot Backup and Restore Command Manual

This document describes the commands of TiDB snapshot backup and restore according to the application scenarios, including:

- [Back up cluster snapshots](#back-up-cluster-snapshots)
- [Back up a database or a table](#back-up-a-database-or-a-table)
    - [Back up a database](#back-up-a-database)
    - [Back up a table](#back-up-a-table)
    - [Back up multiple tables with table filter](#back-up-multiple-tables-with-table-filter)
- [Back up statistics](#back-up-statistics)
- [Encrypt the backup data](#encrypt-the-backup-data)
- [Restore cluster snapshots](#restore-cluster-snapshots)
- [Restore a database or a table](#restore-a-database-or-a-table)
    - [Restore a database](#restore-a-database)
    - [Restore a table](#restore-a-table)
    - [Restore multiple tables with table filter](#restore-multiple-tables-with-table-filter)
    - [Restore execution plan bindings from the `mysql` schema](#restore-execution-plan-bindings-from-the-mysql-schema)
- [Restore encrypted snapshots](#restore-encrypted-snapshots)

For more information about snapshot backup and restore, refer to:

- [Snapshot Backup and Restore Guide](/br/br-snapshot-guide.md)
- [Backup and Restore Use Cases](/br/backup-and-restore-use-cases.md)

## Back up cluster snapshots

You can back up the latest or specified snapshot of the TiDB cluster using the `tiup br backup full` command. For more information about the command, run the `tiup br backup full --help` command.

```shell
tiup br backup full \
    --pd "${PD_IP}:2379" \
    --backupts '2022-09-08 13:30:00' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

In the preceding command:

- `--backupts`: The time point of the snapshot. The format can be [TSO](/glossary.md#tso) or timestamp, such as `400036290571534337` or `2018-05-11 01:42:23`. If the data of this snapshot is garbage collected, the `tiup br backup` command returns an error and 'br' exits. If you leave this parameter unspecified, `br` picks the snapshot corresponding to the backup start time.
- `--ratelimit`: The maximum speed **per TiKV** performing backup tasks. The unit is in MiB/s.
- `--log-file`: The target file where `br` log is written.

> **Note:**
>
> The BR tool already supports self-adapting to GC. It automatically registers `backupTS` (the latest PD timestamp by default) to PD's `safePoint` to ensure that TiDB's GC Safe Point does not move forward during the backup, thus avoiding manually setting GC configurations.

During backup, a progress bar is displayed in the terminal, as shown below. When the progress bar advances to 100%, the backup is complete.

```shell
Full Backup <---------/................................................> 17.12%.
```

## Back up a database or a table

Backup & Restore (BR) supports backing up partial data of a specified database or table from a cluster snapshot or incremental data backup. This feature allows you to filter out unwanted data from snapshot backup and incremental data backup, and back up only business-critical data.

### Back up a database

To back up a database in a cluster, run the `tiup br backup db` command.

The following example backs up the `test` database to Amazon S3:

```shell
tiup br backup db \
    --pd "${PD_IP}:2379" \
    --db test \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

In the preceding command, `--db` specifies the database name, and other parameters are the same as those in [Back up TiDB cluster snapshots](#back-up-cluster-snapshots).

### Back up a table

To back up a table in a cluster, run the `tiup br backup table` command.

The following example backs up the `test.usertable` table to Amazon S3:

```shell
tiup br backup table \
    --pd "${PD_IP}:2379" \
    --db test \
    --table usertable \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backuptable.log
```

In the preceding command, `--db` and `--table` specify the database name and table name respectively, and other parameters are the same as those in [Back up TiDB cluster snapshots](#back-up-cluster-snapshots).

### Back up multiple tables with table filter

To back up multiple tables with more criteria, run the `tiup br backup full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

The following example backs up tables that match the `db*.tbl*` filter rule to Amazon S3:

```shell
tiup br backup full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file backupfull.log
```

## Back up statistics

Starting from TiDB v7.5.0, the `br` command-line tool introduces the `--ignore-stats` parameter. When you set this parameter to `false`, the `br` command-line tool supports backing up statistics of columns, indexes, and tables. In this case, you do not need to manually run the statistics collection task for the TiDB database restored from the backup, or wait for the completion of the automatic collection task. This feature simplifies the database maintenance work and improves the query performance.

If you do not set this parameter to `false`, the `br` command-line tool uses the default setting `--ignore-stats=true`, which means statistics are not backed up during data backup.

The following is an example of backing up cluster snapshot data and backing up table statistics with `--ignore-stats=false`:

```shell
tiup br backup full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log \
--ignore-stats=false
```

After backing up data with the preceding configuration, when you restore data, the `br` command-line tool automatically restores table statistics if table statistics are included in the backup (Starting from v8.0.0, the `br` command-line tool introduces the `--load-stats` parameter, which controls whether to restore backup statistics. The default behavior is to restore backup statistics. There is no need to set it to `false` in most cases):

```shell
tiup br restore full \
--storage local:///br_data/ --pd "${PD_IP}:2379" --log-file restore.log
```

When the backup and restore feature backs up data, it stores statistics in JSON format within the `backupmeta` file. When restoring data, it loads statistics in JSON format into the cluster. For more information, see [LOAD STATS](/sql-statements/sql-statement-load-stats.md).

## Encrypt the backup data

> **Warning:**
>
> This is an experimental feature. It is not recommended that you use it in the production environment.

BR supports encrypting backup data at the backup side and [at the storage side when backing up to Amazon S3](/br/backup-and-restore-storages.md#amazon-s3-server-side-encryption). You can choose either encryption method as required.

Since TiDB v5.3.0, you can encrypt backup data by configuring the following parameters:

- `--crypter.method`: Encryption algorithm, which can be `aes128-ctr`, `aes192-ctr`, or `aes256-ctr`. The default value is `plaintext`, indicating that data is not encrypted.
- `--crypter.key`: Encryption key in hexadecimal string format. It is a 128-bit (16 bytes) key for the algorithm `aes128-ctr`, a 24-byte key for the algorithm `aes192-ctr`, and a 32-byte key for the algorithm `aes256-ctr`.
- `--crypter.key-file`: The key file. You can directly pass in the file path where the key is stored as a parameter without passing in the `crypter.key`.

The following is an example:

```shell
tiup br backup full\
    --pd ${PD_IP}:2379 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```

> **Note:**
>
> - If the key is lost, the backup data cannot be restored to the cluster.
> - The encryption feature needs to be used on `br` and TiDB clusters v5.3.0 or later versions. The encrypted backup data cannot be restored on clusters earlier than v5.3.0.

## Restore cluster snapshots

You can restore a TiDB cluster snapshot by running the `tiup br restore full` command.

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --with-sys-table \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --ratelimit 128 \
    --log-file restorefull.log
```

In the preceding command:

- `--with-sys-table`: BR restores **data in some system tables**, including account permission data and SQL bindings, and statistics (see [Back up statistics](/br/br-snapshot-manual.md#back-up-statistics)). However, it does not restore statistics tables (`mysql.stat_*`) and system variable tables (`mysql.tidb` and `mysql.global_variables`). For more information, see [Restore tables in the `mysql` schema](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema).
- `--ratelimit`: The maximum speed **per TiKV** performing restore tasks. The unit is in MiB/s.
- `--log-file`: The target file where the `br` log is written.

During restore, a progress bar is displayed in the terminal as shown below. When the progress bar advances to 100%, the restore task is completed. Then `br` will verify the restored data to ensure data security.

```shell
Full Restore <---------/...............................................> 17.12%.
```

## Restore a database or a table

You can use `br` to restore partial data of a specified database or table from backup data. This feature allows you to filter out data that you do not need during the restore.

### Restore a database

To restore a database to a cluster, run the `tiup br restore db` command.

The following example restores the `test` database from the backup data to the target cluster:

```shell
tiup br restore db \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_db.log
```

In the preceding command, `--db` specifies the name of the database to be restored and other parameters are the same as those in [Restore TiDB cluster snapshots](#restore-cluster-snapshots).

> **Note:**
>
> When you restore the backup data, the database name specified by `--db` must be the same as the one specified by `-- db` in the backup command. Otherwise, the restore fails. This is because the metafile of the backup data (`backupmeta` file) records the database name, and you can only restore data to the database with the same name. The recommended method is to restore the backup data to the database with the same name in another cluster.

### Restore a table

To restore a single table to a cluster, run the `tiup br restore table` command.

The following example restores the `test.usertable` table from Amazon S3 to the target cluster:

```shell
tiup br restore table \
    --pd "${PD_IP}:2379" \
    --db "test" \
    --table "usertable" \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_table.log
```

In the preceding command, `--table` specifies the name of the table to be restored, and other parameters are the same as those in [Restore a database](#restore-a-database).

### Restore multiple tables with table filter

To restore multiple tables with more complex filter rules, run the `tiup br restore full` command and specify the [table filters](/table-filter.md) with `--filter` or `-f`.

The following example restores tables that match the `db*.tbl*` filter rule from Amazon S3 to the target cluster:

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'db*.tbl*' \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restorefull.log
```

### Restore execution plan bindings from the `mysql` schema

To restore execution plan bindings of a cluster, you can run the `tiup br restore full` command, including the `--with-sys-table` option and also the `--filter` or `-f` option to specify the `mysql` schema to be restored.

The following is an example of restoring the `mysql.bind_info` table:

```shell
tiup br restore full \
    --pd "${PD_IP}:2379" \
    --filter 'mysql.bind_info' \
    --with-sys-table \
    --ratelimit 128 \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --log-file restore_system_table.log
```

After the restore is completed, you can confirm the execution plan binding information with [`SHOW GLOBAL BINDINGS`](/sql-statements/sql-statement-show-bindings.md):

```sql
SHOW GLOBAL BINDINGS;
```

The dynamic loading of execution plan bindings after the restore is still undergoing optimization (related issues are [#46527](https://github.com/pingcap/tidb/issues/46527) and [#46528](https://github.com/pingcap/tidb/issues/46528)). You need to manually reload the execution plan bindings after the restore.

```sql
-- Ensure that the mysql.bind_info table has only one record for builtin_pseudo_sql_for_bind_lock. If there are more records, you need to manually delete them.
SELECT count(*) FROM mysql.bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock';
DELETE FROM bind_info WHERE original_sql = 'builtin_pseudo_sql_for_bind_lock' LIMIT 1;

-- Force to reload the binding information.
ADMIN RELOAD BINDINGS;
```

## Restore encrypted snapshots

> **Warning:**
>
> This is an experimental feature. It is not recommended that you use it in the production environment.

After encrypting the backup data, you need to pass in the corresponding decryption parameters to restore the data. Ensure that the decryption algorithm and key are correct. If the decryption algorithm or key is incorrect, the data cannot be restored. The following is an example:

```shell
tiup br restore full\
    --pd "${PD_IP}:2379" \
    --storage "s3://${backup_collection_addr}/snapshot-${date}?access-key=${access-key}&secret-access-key=${secret-access-key}" \
    --crypter.method aes128-ctr \
    --crypter.key 0123456789abcdef0123456789abcdef
```
