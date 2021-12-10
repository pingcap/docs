---
title: Migrate Data above Terabytes from MySQL to TiDB
summary: Learn how to migrate data above Terabytes from MySQL to TiDB.
---

# Migrate Data above Terabytes from MySQL to TiDB

When the data volume to be migrated is small, you can easily use DM to migrate data, both for full migration and incremental replication. However, because DM imports data at a slow speed (30~50 GiB/h), when the data volume is large, the migration might take a long time.

This document describes how to migrate large volumes of data from MySQL to TiDB using Dumpling and TiDB Lightning. The local backend mode imports data at 500 GiB/h. After the full migration, you can use DM to replicate the incremental data.

## Prerequisites

- [Install DM](https://docs.pingcap.com/zh/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup).
- [Install Dumpling and TiDB Lightning](/migration-tools.md).
- [Get the source database and target database privileges required for DM](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).
- [Get the source database privileges required for Dumpling](/dumpling-overview.md#export-data-from-tidbmysql).

## Resources required

**OS**: Examples in this document use new, clean CentOS 7 instances. You can virtualize a host locally or deploy a cloud virtual machine on a vendor-provided platform. TiDB Lightning runs on a full CPU by default, so it is recommended to deploy TiDB Lightning on a dedicated machine. If you cannot deploy a dedicated machine, you may deploy TiDB Lightning on a shared machine with other components (such as `tikv-server`) and limit its CPU usage by configuring `region-concurrency`. In the case of hybrid deployment, you can limit the CPU usage of TiDB Lightning to 75% of the number of logical CPUs.

**Memory and CPU**: TiDB Lightning consumes high resources, so it is recommended to allocate more than 64 GB of memory and 32-cores CPU for TiDB Lightning. To get the best performance, make sure the CPU core to memory (GB) ratio is more than 1:2.

**Disk space**:

- Dumpling requires disk space to store the whole data source. SSD is recommended.
- TiDB Lightning requires disk space to temporarily store the sorted key-value pairs. The disk space should be enough to hold the largest single table from the data source.

**Note**: It is not supported to calculate the exact data volume exported by Dumpling from MySQL. You can estimate the data volume by using the following SQL statement to summarize the `data-length` field in the `information_schema.tables` table:

{{< copyable "sql" >}}

```sql
# Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name.
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_schema;

# Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name.
select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
```

### Disk space for the target TiKV cluster

The target TiKV cluster must have enough disk space to store the imported data. In addition to [the standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x [the number of replicas](/faq/deploy-and-maintain-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space 6 times the size of the data source. The formula has a **x 2** because:

- Index might take extra space.
- RocksDB has a space amplification issue.

## Step 1. Export data from MySQL using Dumpling

Export data from MySQL by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-dir}
```

Dumpling exports data in SQL files by default. You can specify the file format by adding the `--filetype [sql|csv]` option.

The options used above are as follows:

|Options                |Description|
|-                      |-|
|`-u` or `--user`       |MySQL user|
|`-p` or `--password`   |MySQL user password|
|`-P` or `--port`       |MySQL port|
|`-h` or `--host`       |MySQL IP address|
|`-t` or `--thread`     |The number of threads used for export|
|`-o` or `--output`     |The directory that stores the exported file. Supports local path or [external storage URL](/br/backup-and-restore-storages.md)|
|`-r` or `--row`        |The maximum number of rows in a single file|
|`-F`                   |The maximum size of a single file, in MiB|
|-`B` or `--database`   |Specifies a database to be exported|
|`-f` or `--filter`     |Exports table that matches the pattern. The syntax is the same as [table-filter](/table-filter.md). `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` exports all tables except the system schema. |

Make sure `${data-path}` has enough space to store the exported data. To avoid the import being interrupted, it is strongly recommended to use the `-F` option to limit the size of a single file.

Next, view the `metadata` file in the `${data-path}` directory. This is a Dumpling-generated metadata file. Record the binlog position information, which is required for the incremental replication in Step 3.

```
SHOW MASTER STATUS:
 Log: mysql-bin.000004
 Pos: 109227
 GTID:
```

## Step 2. Import full data to TiDB using TiDB Lightning

1. Create the `tidb-lightning.toml` configuration file:

    {{< copyable "" >}}

    ```toml
    [lightning]
    # log.
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default. The local backend is used to import large volumes of data (1 TB or above). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is used to import small volumes of data (below 1 TB). During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # Directory of the data source. The same directory that Dumpling exports the data to in Step 1.
    data-source-dir = "${data-path}"

    # Configure the wildcard rule. The default rule filters out all tables in these system databases: mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, INSPECTION_SCHEMA.
    # If you do not configure this item, TiDB Lightning reports a `cannot find schema` error when it imports system tables.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # The target TiDB cluster information.
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # Obtain the table schema information from TiDB status port, e.g.: 10080
    pd-addr = "${ip}:${port}"     # The cluster PD address, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    For more information on TiDB Lightning configuration, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

2. Start the import by running `tidb-lightning`. If you launch the program directly in command line, the program might exit because of the `SIGHUP` signal. In this case, it is recommended to run the program with a `nohup` or `screen` tool. For example:

    {{< copyable "shell-regular" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

3. After TiDB Lightning completes the import, it exits automatically. If the import is successful, the last line of `tidb-lightning.log` prints `tidb lightning exit`.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Step 3. Replicate incremental data to TiDB using DM

### Add the data source

1. Create a `source1.yaml` file as follows:

    {{< copyable "" >}}

    ```yaml
    # Configuration.
    source-id: "mysql-01" # Must be unique.

    # Configure whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL has automatic source-replica switching, then GTID mode is required.
    enable-gtid: false
    from:
      host: "${host}"           # e.g.: 172.16.10.81
      user: "root"
      password: "${password}"   # Supports but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2. Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    The options used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The {advertise-addr} of any DM-master in the cluster that `dmctl` is connecting to, e.g.: 172.16.10.71:8261|
    |`operate-source create`|Load the data source to the DM cluster.|

### Add a replication task

Edit the `task.yaml` file to configure the incremental replication mode and the starting point of each data source:

{{< copyable "shell-regular" >}}

```yaml
   name: task-test                      # Task name. Must be globally unique.
   task-mode: incremental               # Task mode. "incremental" only performs incremental data replication.
   ## Configures the target TiDB database.
   target-database:                     # The target database instance.
     host: "${host}"                    # e.g.: 127.0.0.1
     port: 4000
     user: "root"
     password: "${password}"            # It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

   ##  Use block and allow lists to specify the tables to be replicated.
   block-allow-list:                    # The collection of filtering rules that matches the tables in the source database instance. If DM version is v2.0.0-beta.2 or earlier, use black-white-list instead.
     bw-rule-1:                         # The block-allow-list configuration item ID.
       do-dbs: ["${db-name}"]           # Name of databases to be replicated.

   ## Configure the data source.
   mysql-instances:
     - source-id: "mysql-01"            # Data source ID，i.e., source-id in source1.yaml
       block-allow-list: "bw-rule-1"    # Reference the block-allow-list configuration above.
#       syncer-config-name: "global"    # Reference the syncers incremental data configuration below.
       meta:                            # When task-mode is "incremental" and the downstream database does not have a checkpoint, the binlog position is used as the starting point. If the downstream database has a checkpoint, use the checkpoint as the starting point.
         binlog-name: "mysql-bin.000004"  # 第 1 步中记录的日志位置，当上游存在主从切换时，必须使用 gtid。The binlog position recorded in "Step 1." When the upstream database has source-replica switching, GTID mode is required.
         binlog-pos: 109227
         # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

   ## (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable safe mode to avoid the incremental data replication error.
   ## This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
   # syncers:           # The running configurations of the sync processing unit.
   #  global:           # Configuration name.
   #    safe-mode: true # If this field is set to true, DM will change INSERT to REPLACE, UPDATE to DELETE and REPLACE. This is to ensure that when the table schema contains primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables safe mode.
```

The YAML above is the minimum configuration required for the migration task. For more configuration items, refer to [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full).

Before you start the migration task, to reduce the probability of errors, it is recommended to check whether the configuration meets the requirements of DM by running the `check-task` command:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Start the migration task by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The options used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The {advertise-addr} of any DM-master in the cluster that `dmctl` is connecting to, e.g.: 172.16.10.71:8261|
|`start-task`           |Start the migration task.|

If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

If you encounter any problem, refer to [DM error handling](https://docs.pingcap.com/tidb-data-migration/stable/error-handling) and [DM FAQ](https://docs.pingcap.com/zh/tidb-data-migration/stable/faq).

### Check the migration task status

To learn whether the DM cluster has an ongoing migration task and the task status, run the `query-status` command using `tiup dmctl`:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

### Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl output the related information in logs. The log directory of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](https://docs.pingcap.com/tidb-data-migration/stable/pause-task).
- [Resume the migration task](https://docs.pingcap.com/tidb-data-migration/stable/resume-task).
- [Stop the migration task](https://docs.pingcap.com/tidb-data-migration/stable/stop-task).
- [Export and import the cluster data source and task configuration](https://docs.pingcap.com/tidb-data-migration/stable/export-import-config).
- [Handle failed DDL statements](https://docs.pingcap.com/tidb-data-migration/stable/handle-failed-ddl-statements).
