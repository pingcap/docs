---
<<<<<<< HEAD
title: Use BR to Back up and Restore Data
summary: Learn how to back up and restore data of the TiDB cluster using BR.
aliases: ['/docs/v3.1/br/backup-and-restore-tool/','/docs/v3.1/reference/tools/br/br/','/docs/v3.1/how-to/maintain/backup-and-restore/br/']
=======
title: BR Tool Overview
summary: Learn what is BR and how to use the tool.
aliases: ['/docs/dev/br/backup-and-restore-tool/','/docs/dev/reference/tools/br/br/','/docs/dev/how-to/maintain/backup-and-restore/br/']
>>>>>>> 7956a695... BR: reorganize content about BR tool (#4810)
---

# BR Tool Overview

<<<<<<< HEAD
[Backup & Restore](http://github.com/pingcap/br) (BR) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with [`dumpling`](/export-or-backup-using-dumpling.md) and [`mydumper`/`loader`](/backup-and-restore-using-mydumper-lightning.md), BR is more suitable for scenarios of huge data volume. This document describes the BR command line, detailed use examples, best practices, restrictions, and introduces the implementation principles of BR.
=======
[BR](http://github.com/pingcap/br) (Backup & Restore) is a command-line tool for distributed backup and restoration of the TiDB cluster data. It is supported to use BR only in TiDB v3.1 and later versions.
>>>>>>> 7956a695... BR: reorganize content about BR tool (#4810)

Compared with [`dumpling`](/backup-and-restore-using-dumpling-lightning.md), BR is more suitable for scenarios of huge data volume.

<<<<<<< HEAD
- BR only supports TiDB v3.1 and later versions.
- Currently, you can perform restoration only on new clusters.
- It is recommended that you execute multiple backup operations serially. Otherwise, different backup operations might interfere with each other.
- When BR restores data to the upstream cluster of Drainer, Drainer cannot replicate the restored data to the downstream.

## Recommended deployment configuration

- It is recommended that you deploy BR on the PD node.
- It is recommended that you mount a high-performance SSD to BR nodes and all TiKV nodes. A 10-gigabit network card is recommended. Otherwise, bandwidth is likely to be the performance bottleneck during the backup and restore process.

## Download Binary

Refer to the [download page](/download-ecosystem-tools.md#br-backup-and-restore) for more information.
=======
This document describes BR's implementation principles, recommended deployment configuration, usage restrictions, several methods to use BR, etc.
>>>>>>> 7956a695... BR: reorganize content about BR tool (#4810)

## Implementation principles

BR sends the backup or restoration commands to each TiKV node. After receiving these commands, TiKV performs the corresponding backup or restoration operations.

Each TiKV node has a path in which the backup files generated in the backup operation are stored and from which the stored backup files are read during the restoration.

![br-arch](/media/br-arch.png)

<details>

<summary>Backup principle</summary>

When BR performs a backup operation, it first obtains the following information from PD:

- The current TS (timestamp) as the time of the backup snapshot
- The TiKV node information of the current cluster

According to these information, BR starts a TiDB instance internally to obtain the database or table information corresponding to the TS, and filters out the system databases (`information_schema`, `performance_schema`, `mysql`) at the same time.

According to the backup sub-command, BR adopts the following two types of backup logic:

- Full backup: BR traverses all the tables and constructs the KV range to be backed up according to each table.
- Single table backup: BR constructs the KV range to be backed up according a single table.

Finally, BR collects the KV range to be backed up and sends the complete backup request to the TiKV node of the cluster.

The structure of the request:

```
BackupRequest{
    ClusterId,      // The cluster ID.
    StartKey,       // The starting key of the backup (backed up).
    EndKey,         // The ending key of the backup (not backed up).
    StartVersion,   // The version of the last backup snapshot, used for the incremental backup.
    EndVersion,     // The backup snapshot time.
    StorageBackend, // The path where backup files are stored.
    RateLimit,      // Backup speed (MB/s).
}
```

After receiving the backup request, the TiKV node traverses all Region leaders on the node to find the Regions that overlap with the KV ranges in this request. The TiKV node backs up some or all of the data within the range, and generates the corresponding SST file.

After finishing backing up the data of the corresponding Region, the TiKV node returns the metadata to BR. BR collects the metadata and stores it in the `backupmeta` file which is used for restoration.

If `StartVersion` is not `0`, the backup is seen as an incremental backup. In addition to KVs, BR also collects DDLs between `[StartVersion, EndVersion)`. During data restoration, these DDLs are restored first.

If checksum is enabled when you execute the backup command, BR calculates the checksum of each backed up table for data check.

### Types of backup files

Two types of backup files are generated in the path where backup files are stored:

- **The SST file**: stores the data that the TiKV node backed up.
- **The `backupmeta` file**: stores the metadata of this backup operation, including the number, the key range, the size, and the Hash (sha256) value of the backup files.

### The format of the SST file name

The SST file is named in the format of `storeID_regionID_regionEpoch_keyHash_cf`, where

- `storeID` is the TiKV node ID;
- `regionID` is the Region ID;
- `regionEpoch` is the version number of the Region;
- `keyHash` is the Hash (sha256) value of the startKey of a range, which ensures the uniqueness of a key;
- `cf` indicates the [Column Family](/tune-tikv-performance.md#tune-tikv-performance) of RocksDB (`default` or `write` by default).

</details>

<details>

<summary>Restoration principle</summary>

During the data restoration process, BR performs the following tasks in order:

1. It parses the `backupmeta` file in the backup path, and then starts a TiDB instance internally to create the corresponding databases and tables based on the parsed information.

2. It aggregates the parsed SST files according to the tables.

3. It pre-splits Regions according to the key range of the SST file so that every Region corresponds to at least one SST file.

4. It traverses each table to be restored and the SST file corresponding to each tables.

5. It finds the Region corresponding to the SST file and sends a request to the corresponding TiKV node for downloading the file. Then it sends a request for loading the file after the file is successfully downloaded.

After TiKV receives the request to load the SST file, TiKV uses the Raft mechanism to ensure the strong consistency of the SST data. After the downloaded SST file is loaded successfully, the file is deleted asynchronously.

After the restoration operation is completed, BR performs a checksum calculation on the restored data to compare the stored data with the backed up data.

</details>

<<<<<<< HEAD
## Command-line description

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
> - It is **not recommended** to back up to a local disk in the production environment because you **have to** manually aggregate these data to complete the data restoration. For more information, see [Restore Cluster Data](#restore-cluster-data).
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

## Back up cluster data

To back up the cluster data, use the `br backup` command. You can add the `full` or `table` sub-command to specify the scope of your backup operation: the whole cluster or a single table.

If the backup time might exceed the [`tikv_gc_life_time`](/garbage-collection-configuration.md#tikv_gc_life_time) configuration which is `10m0s` by default (`10m0s` means 10 minutes), increase the value of this configuration.

For example, set `tikv_gc_life_time` to `720h`:

{{< copyable "sql" >}}

```sql
mysql -h${TiDBIP} -P4000 -u${TIDB_USER} ${password_str} -Nse \
    "update mysql.tidb set variable_value='720h' where variable_name='tikv_gc_life_time'";
```

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
    --ratelimit 120 \
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
    --ratelimit 120 \
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
    --ratelimit 120 \
    --log-file backuptable.log
```

In the above command, `--db` specifies the name of the database to be backed up. For descriptions of other options, see [Back up all the cluster data](/br/backup-and-restore-tool.md#back-up-all-the-cluster-data).

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
    --ratelimit 120 \
    --log-file backuptable.log
```

The `table` sub-command has two options:

* `--db`: specifies the database name
* `--table`: specifies the table name.

For descriptions of other options, see [Back up all cluster data](#back-up-all-the-cluster-data).

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
    --ratelimit 120 \
    --log-file backupfull.log
```

### Back up data to Amazon S3 backend

If you back up the data to the Amazon S3 backend, instead of `local` storage, you need to specify the S3 storage path in the `storage` sub-command, and allow the BR node and the TiKV node to access Amazon S3.

You can refer to the [AWS Official Document](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html) to create an S3 `Bucket` in the specified `Region`. You can also refer to another [AWS Official Document](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html) to create a `Folder` in the `Bucket`.

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
    --log-file backuptable.log
```

### Back up incremental data
=======
## Deploy and use BR
>>>>>>> 7956a695... BR: reorganize content about BR tool (#4810)

## Recommended deployment configuration

- It is recommended that you deploy BR on the PD node.
- It is recommended that you mount a high-performance SSD to BR nodes and all TiKV nodes. A 10-gigabit network card is recommended. Otherwise, bandwidth is likely to be the performance bottleneck during the backup and restore process.

> **Note:**
>
> - If you do not mount a network disk or use other shared storage, the data backed up by BR will be generated on each TiKV node. Because BR only backs up leader replicas, you should estimate the space reserved for each node based on the leader size.
>
> - Meanwhile, because TiDB v4.0 uses leader count for load balancing by default, leaders are greatly different in size, resulting in uneven distribution of backup data on each node.

### Usage restrictions

The following are the limitations of using BR for backup and restoration:

- It is supported to use BR only in TiDB v3.1 and later versions.
- When BR restores data to the upstream cluster of TiCDC/Drainer, TiCDC/Drainer cannot replicate the restored data to the downstream.
- BR supports operations only between clusters with the same [`new_collations_enabled_on_first_bootstrap`](/character-set-and-collation.md#collation-support-framework) value because BR only backs up KV data. If the cluster to be backed up and the cluster to be restored use different collations, the data validation fails. Therefore, before restoring a cluster, make sure that the switch value from the query result of the `select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME='new_collation_enabled';` statement is consistent with that during the backup process.

    - For v3.1 clusters, the new collation framework is not supported, so you can see it as disabled.
    - For v4.0 clusters, check whether the new collation is enabled by executing `SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';`.

    For example, assume that data is backed up from a v3.1 cluster and will be restored to a v4.0 cluster. The `new_collation_enabled` value of the v4.0 cluster is `true`, which means that the new collation is enabled in the cluster to be restored when this cluster is created. If you perform the restore in this situation, an error might occur.

### Best practices

The following are some recommended operations for using BR for backup and restoration:

- It is recommended that you perform the backup operation during off-peak hours to minimize the impact on applications.
- BR supports restore on clusters of different topologies. However, the online applications will be greatly impacted during the restore operation. It is recommended that you perform restore during the off-peak hours or use `rate-limit` to limit the rate.
- It is recommended that you execute multiple backup operations serially. Running different backup operations in parallel reduces backup performance and also affects the online application.
- It is recommended that you execute multiple restore operations serially. Running different restore operations in parallel increases Region conflicts and also reduces restore performance.
- It is recommended that you mount a shared storage (for example, NFS) on the backup path specified by `-s`, to make it easier to collect and manage backup files.
- It is recommended that you use a storage hardware with high throughput, because the throughput of a storage hardware limits the backup and restoration speed.

### How to use BR

Currently, the following methods are supported to run the BR tool:

- Use SQL statements
- Use the command-line tool
- Use BR In the Kubernetes environment

#### Use SQL statements

In TiDB v4.0.2 and later versions, you can run the BR tool using SQL statements.

For detailed operations, see the following documents:

- [Backup syntax](/sql-statements/sql-statement-backup.md#backup)
- [Restore syntax](/sql-statements/sql-statement-restore.md#restore)

#### Use the command-line tool

In TiDB versions above v3.1, you can run the BR tool using the command-line tool.

First, you need to download the binary file of the BR tool. See [download link](/download-ecosystem-tools.md#br-backup-and-restore).

For how to use the command-line tool to perform backup and restore operations, see [Use the BR command-line tool](/br/use-br-command-line-tool.md).

#### In the Kubernetes environment

In the Kubernetes environment, you can use the BR tool to back up TiDB cluster data to S3-compatible storage, Google Cloud Storage (GCS) and persistent volumes (PV), and restore them:

> **Note:**
>
> For Amazon S3 and Google Cloud Storage parameter descriptions, see the [BR Storages](/br/backup-and-restore-storages.md) document.

- [Back up Data to S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)
- [Restore Data from S3-Compatible Storage Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)
- [Back up Data to GCS Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-gcs-using-br)
- [Restore Data from GCS Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-gcs-using-br)
- [Back up Data to PV Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-pv-using-br)
- [Restore Data from PV Using BR](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-pv-using-br)

## Other documents about BR

- [Use BR Command-line](/br/use-br-command-line-tool.md)
- [BR Use Cases](/br/backup-and-restore-use-cases.md)
- [BR FAQ](/br/backup-and-restore-faq.md)
- [BR Storages](/br/backup-and-restore-storages.md)
