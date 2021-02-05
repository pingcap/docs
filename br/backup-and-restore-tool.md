---
title: Use BR to Back up and Restore Data
summary: Learn how to back up and restore data of the TiDB cluster using BR.
aliases: ['/docs/dev/br/backup-and-restore-tool/','/docs/dev/reference/tools/br/br/','/docs/dev/how-to/maintain/backup-and-restore/br/']
---

# Use BR to Back up and Restore Data

[Backup & Restore](http://github.com/pingcap/br) (BR) is a command-line tool for distributed backup and restoration of the TiDB cluster data. Compared with [`dumpling`](/backup-and-restore-using-dumpling-lightning.md), BR is more suitable for scenarios of huge data volume. This document describes the BR command line, detailed use examples, best practices, restrictions, and introduces the implementation principles of BR.

## Usage restrictions

- BR only supports TiDB v3.1 and later versions.
- BR supports restore on clusters of different topologies. However, the online applications will be greatly impacted during the restore operation. It is recommended that you perform restore during the off-peak hours or use `rate-limit` to limit the rate.
- It is recommended that you execute multiple backup operations serially. Running different backup operations in parallel reduces backup performance and also affects the online application.
- It is recommended that you execute multiple restore operations serially. Running different restore operations in parallel increases Region conflicts and also reduces restore performance.
- When BR restores data to the upstream cluster of TiCDC/Drainer, TiCDC/Drainer cannot replicate the restored data to the downstream.
- BR supports operations only between clusters with the same [`new_collations_enabled_on_first_bootstrap`](/character-set-and-collation.md#collation-support-framework) value because BR only backs up KV data. If the cluster to be backed up and the cluster to be restored use different collations, the data validation fails. Therefore, before restoring a cluster, make sure that the switch value from the query result of the `select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME='new_collation_enabled';` statement is consistent with that during the backup process.

    - For v3.1 clusters, the new collation framework is not supported, so you can see it as disabled.
    - For v4.0 clusters, check whether the new collation is enabled by executing `SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';`.

    For example, assume that data is backed up from a v3.1 cluster and will be restored to a v4.0 cluster. The `new_collation_enabled` value of the v4.0 cluster is `true`, which means that the new collation is enabled in the cluster to be restored when this cluster is created. If you perform the restore in this situation, an error might occur.

## Recommended deployment configuration

- It is recommended that you deploy BR on the PD node.
- It is recommended that you mount a high-performance SSD to BR nodes and all TiKV nodes. A 10-gigabit network card is recommended. Otherwise, bandwidth is likely to be the performance bottleneck during the backup and restore process.

> **Note:**
>
> If you do not mount a network disk or use other shared storage, the data backed up by BR will be generated on each TiKV node. Because BR only backs up leader replicas, you should estimate the space reserved for each node based on the leader size.
>
> Meanwhile, because TiDB v4.0 uses leader count for load balancing by default, leaders are greatly different in size, resulting in uneven distribution of backup data on each node.

## Implementation principles

BR sends the backup or restoration commands to each TiKV node. After receiving these commands, TiKV performs the corresponding backup or restoration operations. Each TiKV node has a path in which the backup files generated in the backup operation are stored and from which the stored backup files are read during the restoration.

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
- `cf` indicates the [Column Family](/tune-tikv-memory-performance.md) of RocksDB (`default` or `write` by default).

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

## How to use BR

Currently, you can use SQL statements or the command-line tool to back up and restore data.

### Use SQL statements

TiDB v4.0.2 and later versions support backup and restore operations using SQL statements. For details, see the [Backup syntax](/sql-statements/sql-statement-backup.md#backup) and the [Restore syntax](/sql-statements/sql-statement-restore.md#restore).

### Use the command-line tool

Also, you can use the command-line tool to perform backup and restore. First, you need to download the binary file of the BR tool. For details, see [download link](/download-ecosystem-tools.md#br-backup-and-restore).

The following section takes the command-line tool as an example to introduce how to perform backup and restore operations.

## Best practices

- It is recommended that you mount a shared storage (for example, NFS) on the backup path specified by `-s`, to make it easier to collect and manage backup files.
- It is recommended that you use a storage hardware with high throughput, because the throughput of a storage hardware limits the backup and restoration speed.
- It is recommended that you perform the backup operation during off-peak hours to minimize the impact on applications.

For more recommended practices of using BR, refer to [BR Use Cases](/br/backup-and-restore-use-cases.md).
