---
title: br Command-line Manual
summary: The `br` command-line tool is used for snapshot backup, log backup, and point-in-time recovery (PITR) in TiDB clusters. It consists of sub-commands, options, and parameters, with common options like `--pd` for PD service address and `-s` for storage path. Sub-commands include `tiup br backup`, `tiup br log`, and `tiup br restore`, each with specific functionalities. Backup commands include `full`, `db`, and `table` options, while log backup and restore commands have various tasks for managing backup operations.
---

# br Command-line Manual

This document describes the definition, components, and common options of `br` commands, and how to perform snapshot backup and restore, and log backup and point-in-time recovery (PITR) using `br` commands.

## `br` command-line description

A `br` command consists of sub-commands, options, and parameters. A sub-command is the characters without `-` or `--`. An option is the characters that start with `-` or `--`. A parameter is the characters that immediately follow behind and are passed to the sub-command or the option.

The following is a complete `br` command:

```shell
tiup br backup full --pd "${PD_IP}:2379" \
--storage "s3://backup-data/snapshot-202209081330/"
```

Explanations for the preceding command are as follows:

* `backup`: the sub-command of `tiup br`.
* `full`: the sub-command of `tiup br backup`.
* `-s` (or `--storage`): the option that specifies the path where the backup files are stored. `"s3://backup-data/snapshot-202209081330/"` is the parameter of `-s`.
* `--pd`: the option that specifies the PD service address. `"${PD_IP}:2379"` is the parameter of `--pd`.

### Commands and sub-commands

A `tiup br` command consists of multiple layers of sub-commands. Currently, br command-line tool has the following sub-commands:

* `tiup br backup`: used to back up the data of the TiDB cluster.
* `tiup br log`: used to start and manage log backup tasks.
* `tiup br restore`: used to restore backup data of the TiDB cluster.
* `tiup br debug`: used to parse backup metadata, check backup data, and so on.

`tiup br backup` and `tiup br restore` include the following sub-commands:

* `full`: used to back up or restore all the cluster data.
* `db`: used to back up or restore a specified database of the cluster.
* `table`: used to back up or restore a single table in the specified database of the cluster.

`tiup br debug` includes the following sub-commands:

* `checksum`: (hidden parameter) used to offline check the integrity of backup data to ensure that all backup files match the CRC64 checksum results calculated by [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md).
* `backupmeta`: used to check whether an intersection exists among backup data files. In normal cases, backup data files do not intersect.
* `decode`: used to parse the `backupmeta` metadata file of a full backup into JSON format. In addition, you can parse specific fields using the `--field` parameter.
* `encode`: used to encode the `backupmeta.json` metadata file of a full backup into the protobuf format that is used during data restore.
* `reset-pd-config-as-default`: (deprecated) used to restore the PD configurations that were changed during the data recovery process to default configurations.
* `search-log-backup`: used to search for specific key information in log backup data.

### Common options

* `--pd`: specifies the PD service address. For example, `"${PD_IP}:2379"`.
* `-s` (or `--storage`): specifies the path where the backup files are stored. Amazon S3, Google Cloud Storage (GCS), Azure Blob Storage, and NFS are supported to store backup data. For more details, refer to [URI Formats of External Storage Services](/external-storage-uri.md).
* `--ca`: specifies the path to the trusted CA certificate in the PEM format.
* `--cert`: specifies the path to the SSL certificate in the PEM format.
* `--key`: specifies the path to the SSL certificate key in the PEM format.
* `--status-addr`: specifies the listening address through which `br` provides statistics to Prometheus.
* `--concurrency`: controls how backup tasks are split into multiple requests and sent concurrently to the same TiKV node. This parameter primarily affects the granularity of request splitting from BR to TiKV, and no longer directly determines overall backup throughput. In most cases, you do not need to change this value. To improve backup performance, you should tune [`tikv.backup.num-threads`](/tikv-configuration-file.md#num-threads-1) instead.
* `--pitr-concurrency`: the number of concurrent tasks during log restore.
* `--tikv-max-restore-concurrency`: the maximum number of concurrent tasks per TiKV node during snapshot restore.
* `--compression`: determines the compression algorithm used for generating backup files. It supports `lz4`, `snappy`, and `zstd`, with the default being `zstd` (usually no need to modify). For guidance on choosing different compression algorithms, refer to [this document](https://github.com/EighteenZi/rocksdb_wiki/blob/master/Compression.md).
* `--compression-level`: sets the compression level corresponding to the chosen compression algorithm for backup. The default compression level for `zstd` is 3. In most cases there is no need to set this option.

## Commands of full backup

To back up cluster data, run the `tiup br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster (`full`) or a single table (`table`).

- [Back up TiDB cluster snapshots](/br/br-snapshot-manual.md#back-up-cluster-snapshots)
- [Back up a database](/br/br-snapshot-manual.md#back-up-a-database)
- [Back up a table](/br/br-snapshot-manual.md#back-up-a-table)
- [Back up multiple tables with table filter](/br/br-snapshot-manual.md#back-up-multiple-tables-with-table-filter)
- [Encrypt snapshots](/br/backup-and-restore-storages.md#server-side-encryption)

## Commands of log backup

To start log backup and manage log backup tasks, run the `tiup br log` command.

- [Start a log backup task](/br/br-pitr-manual.md#start-a-log-backup-task)
- [Query the log backup status](/br/br-pitr-manual.md#query-the-log-backup-status)
- [Pause and resume a log backup task](/br/br-pitr-manual.md#pause-and-resume-a-log-backup-task)
- [Stop and restart a log backup task](/br/br-pitr-manual.md#stop-and-restart-a-log-backup-task)
- [Clean up the backup data](/br/br-pitr-manual.md#clean-up-log-backup-data)
- [View the backup metadata](/br/br-pitr-manual.md#view-the-log-backup-metadata)

## Commands of restoring backup data

To restore cluster data, run the `tiup br restore` command. You can add the `full`, `db`, or `table` sub-command to specify the scope of your restore: the whole cluster (`full`), a single database (`db`), or a single table (`table`).

- [Point-in-time recovery](/br/br-pitr-manual.md#restore-to-a-specified-point-in-time-pitr)
- [Restore cluster snapshots](/br/br-snapshot-manual.md#restore-cluster-snapshots)
- [Restore a database](/br/br-snapshot-manual.md#restore-a-database)
- [Restore a table](/br/br-snapshot-manual.md#restore-a-table)
- [Restore multiple tables with table filter](/br/br-snapshot-manual.md#restore-multiple-tables-with-table-filter)
- [Restore encrypted snapshots](/br/br-snapshot-manual.md#restore-encrypted-snapshots)
