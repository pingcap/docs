---
title: Import Large Sharded Schemas and Sharded Tables to TiDB (>1 TiB)
summary: Use Dumpling and TiDB Lightning to merge and import sharded schemas and sharded tables into TiDB. The method described in this article is suitable for scenarios where the total amount of imported data is greater than 1 TiB.
---

# Import Large Sharded Schemas and Sharded Tables to TiDB (>1 TiB)

If the total size of the sharded tables is large (for example, greater than 1 TiB) and allows the TiDB cluster to suspend other business writes during the migration, then you can use TiDB Lightning to quickly merge and import the sharded table data. After import, you can also choose whether to use TiDB DM for incremental data synchronization based on your business needs. 

This document walks you through the procedure of how to import large sharded schemas and sharded tables into TiDB.

If the data size of the sharded tables is under 1 TiB, you can follow the procedure described in [Migrate Sharded Schemas and Tables to TiDB]( https://docs.pingcap.com/tidb-data-migration/stable/usage-scenario-shard-merge), which supports both full and incremental import.

The following diagram shows how to import sharded schemas and sharded tables into TiDB using Dumpling and TiDB Lightning.

![Use Dumpling and TiDB Lightning to merge and import sharded schemas and sharded tables into TiDB](/media/shard-merge-using-lightning.png)

This example assumes that you have two databases, `my_db1` and `my_db2`. You use Dumpling to export two tables `table1` and `table2` from `my_db1`, and two tables `table3` and `table4` from `my_db2`, respectively. After that, you use TiDB Lighting to merge and import the four exported tables into the same `table5` in the downstream TiDB.

Note that although Dumpling can export all databases from a MySQL instance, this article only exports some of the data as an example.

For more information about Dumpling and TiDB Lightning, see the following articles:

* [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview)
* [TiDB Lightning](https://docs.pingcap.com/tidb/stable/tidb-lightning-overview)

**Note**: It is difficult to calculate the exact size of the data exported by Dumpling from MySQL. But you can estimate the amount of data using the `data_length` field with the following SQL statement.

{{< copyable "sql" >}}

```sql
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables group by table_schema;
```

## Prerequisites

### Hardware requirements of TiDB Lightning 

**Operating System**: The example in this document uses a few fresh CentOS 7 instances. You can deploy a small virtual machine either locally virtualized or on cloud. Because TiDB Lightning consumes 100% CPU by default, it is recommended that you deploy it on a dedicated server. If this is not possible due to a tight budget, you can deploy it on a single server together with other TiDB components (e.g. `tikv-server`) and then configure `region-concurrency` to limit the CPU usage. Usually you can configure the size to 75% of the logical CPU.

**Memory and CPU**: Since TiDB Lightning is resource-intensive, it is recommended to allocate more than 64 GB of memory and more than 32 CPU cores. Meanwhile, to achieve optimal performance, make sure the CPU core to memory (GB) ratio is greater than 1:2.

**Disk Space**: You need to prepare an SSD hard drive sufficient to store the entire data source. The faster the read speed, the better.

### Disk space requirements for the target TiKV cluster

**Disk Space**: The target TiKV cluster must have enough space to store the upcoming imported data. In addition to the [standard hardware configuration](https://docs.pingcap.com/tidb/stable/hardware-and-software-requirements), the total storage space of the target TiKV cluster must be larger than **data source size × [number of replicas](/faq/deploy-and-maintain-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it.) × 2**. For example, if the cluster uses 3 copies by default, then the total storage space needs to be more than 6 times the size of the data source. 

At first glance, it may look confusing why there is a “x2” in the formula. In fact, it is based on the following estimated space:

* Indexes can consume extra space.
* There is a space amplification effect of RocksDB.

### Upstream MySQL permissions

To export data from upstream MySQL using Dumpling, make sure that you have the following permissions:

* SELECT
* RELOAD
* LOCK TABLES
* REPLICATION CLIENT
* PROCESS

### Downstream TiDB permissions

Because the backend mode Local-backend is used in this example, TiDB Lightning requires the following permissions for downstream TiDB.

* SELECT
* UPDATE
* ALTER
* CREATE
* DROP

In general, the configuration item `checksum = true` is recommended, so TiDB Lightning also requires downstream TiDB admin permissions.

For more information about permissions, see [What is the privilege requirements for the target database]( https://docs.pingcap.com/tidb/stable/tidb-lightning-faq#what-is-the-privilege-requirements-for-the-target-database).

<!-- A new feature that will be released soon.
### Deploy Dumpling and TiDB Lightning using TiUP

* [Use TiUP to Deploy TiDB Lighting](https://github.com/pingcap/docs/pull/6144/files#diff-53a937b1281c0fcb1ca972172e4c1b31a97af54bc5414e3186a648ea9eef6e23)
* [Use TiUP to deploy Dumping](https://github.com/pingcap/docs/pull/6144/files#diff-53a937b1281c0fcb1ca972172e4c1b31a97af54bc5414e3186a648ea9eef6e23)
-->

## Procedure of data import

You import data following this procedure:

1. Use Dumpling to export full data. In this example, you export 2 tables respectively from 2 upstream databases: 

   - Export table1 and table 2 from my_db1
   - Export table3 and table 4 from my_db2

2. Start TiDB Lightning to import data.

3. Check the import result.

4. (Optional) Use TiDB DM to perform incremental import. 

The following sections introduce the complete import procedure. 

### Step1. Use Dumpling to export full data

If you need to export multiple sharded tables belonging to the same upstream MySQL instance, you can directly use the `-f` parameter of Dumpling to export them in a single operation. 

If the sharded tables are stored across different MySQL instances, you can use Dumpling to export them respectively and place the results of both exports in the same parent directory. 

In the following example, both methods are used, and then the exported data is stored in the same parent directory.

First, run the following command to use Dumpling to export table1 and table2 from my_db:

```
tiup dumpling -h <ip> -P <port> -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o /data/my_database/
```

In the command above:

- `-h` specifies the IP address of the data source.
- `-p` specifies the port to be used.
- `-u` specifies the user name to be used. If a password is required for authentication, you can use `-p $YOUR_SECRET_PASSWORD` to pass the password to Dumpling.
- `-o` specifies the export directory of the storage, which supports a local file path or a [URL of an external storage](/br/backup-and-restore-storages.md).
- `t` specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and increases the database's memory consumption. Therefore, it is not recommended to set the number too large.
- `-r` specifies the maximum number of rows in a single file. If you use this parameter, Dumpling enables the in-table concurrency to speed up the export and reduce the memory usage.
- `-F` specifies the maximum size of a single file. The unit is `MiB`. Inputs such as `5GiB` or `8KB` are also acceptable. It is recommended to keep the value to 256 MiB or less, if you use TiDB Lightning to load this file into a TiDB instance.

> **Note:**
>
> If the size of a single exported table exceeds 10 GB, it is strongly recommended to use the `-r` and `-F` options.

Then, run the following command to use Dumpling to export table3 and table4 from my_db2:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h <ip> -P <port> -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o /data/my_database/
```

The reason for storing all source data tables in one directory is to facilitate subsequent import by TiDB Lightning.

Congratulations! Now you have exported all the required full data.

### Step 2. Start TiDB Lightning to import data

Before starting TiDB Lightning for import, it is recommended that you understand how to select the backend mode, how to handle breakpoints, and then choose the appropriate way to proceed according to your needs.

#### Backends

When starting TiDB Lightning, choose an appropriate backend according to your needs.

* If the target TiDB cluster is v4.0 or later versions, it is recommended to use the **Local-backend** mode. It is easier to use and has better performance.
* If the target TiDB cluster is v3.x or earlier versions, it is recommended to use the **Importer-backend** mode.
* If the target TiDB cluster is already in the production environment, or the target table already has data populated, it is recommended to use the **TiDB-backend** mode.

By default, the Local-backend mode is used. In this example, the Local-backend mode is used. For more information, see [TiDB Lightning Backends]( https://docs.pingcap.com/tidb/stable/tidb-lightning-backends).

The following table shows cons and pros of each backend.

| Backend | Local-backend | Importer-backend | TiDB-backend |
|:---|:---|:---|:---|
| Speed | Fast (~500 GB/hr) | Fast (~300 GB/hr) | Slow (~50 GB/hr) |
| Resource usage | High | High | Low |
| Network bandwidth usage| High | Medium | Low |
| ACID respected while importing | No | No | Yes |
| Target tables | Must be empty | Must be empty | Can be populated |
| Additional component required | No | `tikv-importer` | No |
| TiDB versions supported | >= v4.0.0 | All | All |
| TiDB services impacted | Yes | Yes | No |

#### Checkpoints

Importing a large volume of data usually takes hours or even days. If such a long running processes unfortunately crashes, it can be very frustrating to redo everything from scratch. 

Fortunately, TiDB Lightning provides a `checkpoints` feature to let you store the import progress, so that import task can resume from the breakpoint upon restart.

If the TiDB Lightning task crashes due to unrecoverable errors (for example, data corruption), it will not pick up from the breakpoint, but will report an error and quit the task. You need to solve the problem first by using the tidb-lightning-ctl program. The options include:

* --checkpoint-error-destroy: This option allows you to restart importing from scratch. 
* --checkpoint-error-ignore: If import has failed, this option clears the error status as if no errors ever happened. 
* --checkpoint-remove: This option simply clears all checkpoints, regardless of errors.

For more information, see [TiDB Lightning Checkpoints](https://docs.pingcap.com/tidb/stable/tidb-lightning-checkpoints).

#### Start the import task

Follow these steps to start `tidb-lightning`:

1. Upload the data sources to the server with TiDB Lightning deployed.
2. Edit the toml file. `tidb-lightning.toml` is used in the following example:

    ```toml
    [lightning]
    # Logs
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Choose a local backend.
    backend = "local"

    # Set the temporary directory for the sorted key value pairs. It must be empty.
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    # Set routes. Import table1 and table2 in my_db1, and table3 and table4 in my_db2, to the target table5 in downstream my_db.
    [[routes]]
    schema-pattern = "my_db1"
    table-pattern = "table[1-2]"
    target-schema = "my_db"
    target-table = "table5"

    [[routes]]
    schema-pattern = "my_db2"
    table-pattern = "table[3-4]"
    target-schema = "my_db"
    target-table = "table5"

    [mydumper]
    # The source data directory. Set this to the path of the Dumpling exported data. If Dumpling is executed multiple times and in different directories, you need to place all the exported data in the same parent directory. You can specify this parent directory here.
    data-source-dir = "/data/my_database/"
    # Configure the wildcard rules. By default, all tables in the following will be filtered: mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, INSPECTION_SCHEMA
    # If not configured, an error “schema not found” will occur when importing system tables. 
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # Information of the target TiDB cluster. Values here are only for illustration purpose. Replace them with your own values.
    host = "172.16.31.2"
    port = 4000
    user = "root"
    password = "rootroot"
    # The table information is read from the status port. 
    status-port = 10080
    # the IP address of the cluster PD. Values here are only for illustration purpose. Replace them with your own values.
    pd-addr = "172.16.31.3:2379"
    ```

3. Configure appropriate parameters to run `tidb-lightning`. If you start the program directly on the command line with `nohup`, it may quit due to the SIGHUP signal. So it is recommended to put `nohup` inside the script. For example:

   {{< copyable "shell-regular" >}}

   ```shell
   tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
   ```
   
4. After the import task gets started, you can check the progress by using either of the following:

   - View progress via keyword `progress` in the `grep` log. By default, the data refreshes every 5 minutes.
   - View progress via the monitoring dashboard. For more information, see [TiDB Lightning Monitoring]( /tidb-lightning/monitor-tidb-lightning.md)

Now, you only need to wait for the import task to finish. 

### Step 3. Check the import result

After the import is finished, TiDB Lightning will quit automatically. To make sure the data is imported successfully, you need to check that the log shows `the whole procedure completed` among the last 5 lines.

> **Note:**
>
> Whether the import is successful or not, the last line will always show `tidb lightning exit`. It just means that TiDB Lightning quits normally, and does not guarantee that the task is completed successfully.

If you encounter any problems during import, see [TiDB Lightning FAQ](https://docs.pingcap.com/tidb/stable/tidb-lightning-faq).

### Step 4. (Optional) Incremental import 

To import the source database to TiDB based on the Binlog from a specified position, you can use TiDB DM to perform incremental import. For more information, see [Incremental Data Migration Scenario](https://docs.pingcap.com/tidb-data-migration/stable/usage-scenario-incremental-migration).

Congratulations! You have imported large sharded schemas and sharded tables to TiDB successfully! 
