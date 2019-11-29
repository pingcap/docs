---
title: Use BR to Backup and Restore Cluster Data
summary: Learn how to backup and restore the data of the TiDB cluster using BR.
category: how-to
---

# Use BR to Backup and Restore Cluster Data

Backup & Restore (BR) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with [Mydumper/Loader](/dev/how-to/maintain/backup-and-restore/mydumper-loader.md), BR is more suitable for scenarios of huge data volume. This document introduces the working principle of BR, describes the command line, and offers detailed use cases of this tool.

## Working principle

BR sends the backup and restoration commands to each TiKV node. After receiving these commands, TiKV performs the corresponding backup and restoration operations. Each TiKV node has a directory in which the backup files generated in the backup operation are stored and from which the stored backup files are read in the restoration.

![br-arch](/media/br-arch.png)

## Command-line description

A `br` command consists of sub-commands, options and parameters. The sub-command is the characters without `-` or `--`. The option is the characters that start with `-` or `--`. The parameter is the characters that immediately follow and pass to the sub-command or the option.

This is a complete `br` command:

`br backup full --pd "${PDIP}:2379" -s "local:///tmp/backup"`

In this command,

* `backup` is the sub-command of `br`.
* `full` is the sub-command of `backup`.
* `-s` or `--storage` specifies the directory in which the backup files are stored.
* `"local:///tmp/backup"` is the parameter of `-s`. `/tmp/backup` is the directory in the local disk for storing backup files.
* `--pd` is the PD service address.
* `"${PDIP}:2379"` is the parameter of `--pd`.

### Sub-commands

A `br` command consists of multiple layers of sub-command. Currently, BR has the following three sub-commands:

* `br backup` is used to backup the data of the TiDB cluster.
* `br restore` is used to restore the data of the TiDB cluster.
* `br version` is used to check the version of BR.

Each of the above three sub-commands might include the following three sub-commands:

* `full` is used to backup or restore all the cluster data.
* `db` is used to restore the specified database of the cluster.
* `table` is used to backup or restore a single table in the specified database of the cluster.

### Common options

* `--pd` is for connection, specifying the PD server address. For example, `"${PDIP}:2379"`.
* `-h`/`--help` is used to get help on all sub-commands. For example, `br backup --help`.
* `--ca` specifies the path to the trusted CA certificate in the PEM format.
* `--cert` specifies the path to the SSL certificate in the PEM format.
* `--key` specifies the path to the SSL certificate key in the PEM format.
* `--status-addr` specifies the listening address through which BR provides statistics to Prometheus.

## Backup cluster data

To backup the cluster data, use the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster or a single table.

### Backup all cluster data

To backup all the cluster data, execute the `br backup full` command. To get help on this command, execute `br backup full -h` or `br backup full --help`.

Use case: Backup all the cluster data to the `/tmp/backup` directory of each TiKV node and write the `backupmeta` file to this directory.

{{< copyable "shell-regular" >}}

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
```

In the above `br` command, the `--ratelimit` and `--concurrency` options set upper limits on the speed at which a backup operation is performed (MiB/s) and the number of concurrent executions for each TiKV node, and the BR log is written to the `backupfull.log` file.

A progress bar is displayed in the terminal during the backup. When the progress bar advances to 100%, the backup is complete. Then the BR also checks the backup data to ensure data security. The progress bar is displayed as follows:

```shell
br backup full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backupfull.log
Full Backup <---------/................................................> 17.12%.
```

### Backup single table

To backup the data of a single table in the cluster, execute the `br backup table` command. To get help on this command, execute `br backup table -h` or `br backup table --help`.

Use case: Backup the data of the `test.usertable` table to the `/tmp/backup` directory in each TiKV node and write the `backupmeta` file to this directory.

{{< copyable "shell-regular" >}}

```shell
br backup table \
    --pd "${PDIP}:2379" \
    --db test \
    --table usertable \
    --storage "local:///tmp/backup" \
    --ratelimit 120 \
    --concurrency 4 \
    --log-file backuptable.log
```

The `table` sub-command has two options: `--db` and `--table`. `--db` specifies the database name and `--table` specifies the table name. The other options have the same meanings as those in [Backup whole cluster](#backup-whole-cluster).

A progress bar is displayed in the terminal during the backup operation. When the progress bar advances to 100%, the backup is complete. Then, the BR also checks the backup data to ensure data security.

## Restore cluster data

To restore the cluster data, use the `br restore` command. You can add the `full`, `db` or `table` sub-command to specify the scope of your restoration: the whole cluster, a database or a single table.

### Restore all backup data

To restore all the backup data to the cluster, execute the `br restore full` command. To get help on this command, execute `br restore full -h` or `br restore full --help`.

Usage: Restore all the backup data in the `/tmp/backup` directory to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --concurrency 128 \
    --log-file restorefull.log
```

`--concurrency` specifies how many sub-tasks can be performed concurrently in a restoration operation, and the BR log is written to the `restorefull.log` file.

A progress bar is displayed in the terminal during the restoration. When the progress bar advances to 100%, the restoration is complete. Then, the BR also checks the backup data to ensure data security.

```shell
br restore full \
    --pd "${PDIP}:2379" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
Full Restore <---------/...............................................> 17.12%.
```

### Restore a database

To restore a database to the cluster, execute the `br restore db` command. To get help on this command, execute `br restore db -h` or `br restore db --help`.

Usage: Restore a database in the backup data in the `/tmp/backup` directory to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore db \
    --pd "${PDIP}:2379" \
    --db "test" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--db` specifies the name of the database to be restored. The other options have the same meaning as those in [Restore all backup data](#restore-all-backup-data).

### Restore a table

To restore a single table to the cluster, execute the `br restore table` command. To get help on this command, execute `br restore table -h` or `br restore table --help`.

Usage: Restore a database table in the backup data in the `/tmp/backup` directory to the cluster.

{{< copyable "shell-regular" >}}

```shell
br restore table \
    --pd "${PDIP}:2379" \
    --db "test" \
    --table "usertable" \
    --storage "local:///tmp/backup" \
    --log-file restorefull.log
```

In the above command, `--table` specifies the name of the table to be restored. The other options have the same meaning as those in [Restore a database](#restore-a-database).

## Best practices

- It is recommended that you mount a shared storage (for example, NFS) on the backup directory specified by `-s`. This makes it easier to collect and manage backup files.
- It is recommended that you use a storage hardware with high throughput, because the throughput of a storage hardware limits the backup and restoration speed.
- It is recommended that you perform the backup operation in a low-peak application time to minimize the impact on the application.

## Note

- BR only supports TiDB v3.1 or later versions.
- If the backed up cluster does not have a network storage, before the restoration, copy the backup SST files to the directory specified by `--storage` on each TikV node.
- Do not perform the backup operation when executing DDL statements on TiDB.
- Perform the restoration only on new clusters.
- If the backup time might exceed the [`tikv_gc_life_time`](/dev/reference/garbage-collection/configuration.md#tikv_gc_life_time) configuration which is `"10m0s"` by default, increase the value of this configuration.

    For example, set `tikv_gc_life_time` to `720h`:

    {{< copyable "sql" >}}

    ```
    mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
        "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
    ```

- To speed up the restoration, use pd-ctl to remove the schedulers related to scheduling before the restoration and add back these removed schedulers after the restoration.

    Remove schedulers:

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler remove balance-region-scheduler
    ```

    Add schedulers:

    {{< copyable "shell-regular" >}}

    ```shell
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-hot-region-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-leader-scheduler
    ./pd-ctl -u ${PDIP}:2379 scheduler add balance-region-scheduler
    ```
