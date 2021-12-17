---
title: Migrate MySQL Data of More than 1 TiB to TiDB
summary: Learn how to migrate data above Terabytes from MySQL to TiDB.
---

# Migrate MySQL Data of More than 1 TiB to TiDB

When the data volume to be migrated is small, you can easily [use DM to migrate data](/data-migration/migrate-mysql-tidb-less-tb.md), both for full migration and incremental replication. However, because DM imports data at a slow speed (30~50 GiB/h), when the data volume is large, the migration might take a long time.

This document describes how to migrate large volumes of data from MySQL to TiDB using Dumpling and TiDB Lightning. TiDB Lightning's local backend mode imports data at 500 GiB/h. After the full migration is completed, you can replicate the incremental data using DM.

## Prerequisites

- [Install DM](https://docs.pingcap.com/zh/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup).
- [Install Dumpling and TiDB Lightning](/migration-tools.md).
- [Get the source database and target database privileges required for DM](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).
- [Get the source database privileges required for Dumpling](/dumpling-overview.md#export-data-from-tidbmysql).

## Resource requirements

**OS**: Examples in this document use new, clean CentOS 7 instances. You can virtualize a host locally or deploy a cloud virtual machine on a vendor-provided platform. TiDB Lightning runs on a full CPU by default, so it is recommended to deploy TiDB Lightning on a dedicated machine. If you cannot use a dedicated machine, you may deploy TiDB Lightning on a shared machine with other components (such as `tikv-server`) and limit TiDB Lightning's CPU usage by configuring `region-concurrency`. In the case of hybrid deployment, you can limit the CPU usage of TiDB Lightning to 75% of the number of logical CPUs.

**Memory and CPU**: TiDB Lightning consumes high resources, so it is recommended to allocate more than 64 GB of memory and 32-core CPU for TiDB Lightning. To get the best performance, make sure the CPU core to memory (GB) ratio is more than 1:2.

**Disk space**:

- Dumpling requires enough disk space to store the whole data source. SSD is recommended.
- TiDB Lightning needs space to temporarily store the sorted key-value pairs. The disk space should be enough to hold the largest single table from the data source.

**Note**: You cannot calculate the exact data volume exported by Dumpling from MySQL, but you can estimate the data volume by using the following SQL statement to summarize the `data-length` field in the `information_schema.tables` table:

{{< copyable "sql" >}}

```sql
/* Calculate the size of all schemas, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM FROM information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_schema;

/* Calculate the size of the largest table, in MiB. Replace ${schema_name} with your schema name. */
SELECT table_name,table_schema,SUM(data_length)/1024/1024 AS data_length,SUM(index_length)/1024/1024 AS index_length,SUM(data_length+index_length)/1024/1024 AS SUM from information_schema.tables WHERE table_schema = "${schema_name}" GROUP BY table_name,table_schema ORDER BY SUM DESC LIMIT 5;
```

### Disk space for the target TiKV cluster

The target TiKV cluster must have enough disk space to store the imported data. In addition to [the standard hardware requirements](/hardware-and-software-requirements.md), the storage space of the target TiKV cluster must be larger than **the size of the data source x [the number of replicas](/faq/deploy-and-maintain-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) x 2**. For example, if the cluster uses 3 replicas by default, the target TiKV cluster must have a storage space 6 times the size of the data source. The formula has `x 2` because:

- Index might take extra space.
- RocksDB has a space amplification effect.

## Step 1. Export all data from MySQL

1. Export all data from MySQL by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-dir}
    ```

    Dumpling exports data in SQL files by default. You can specify the file format by adding the `--filetype` option.

    The parameters used above are as follows. For more Dumpling parameters, refer to [Dumpling Overview](/dumpling-overview.md).

    |parameters             |Description|
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
    |`-f` or `--filter`     |Exports tables that match the pattern. The syntax is the same as [table-filter](/table-filter.md). `[\*.\*,!/^(mysql&#124;sys&#124;INFORMATION_SCHEMA&#124;PERFORMANCE_SCHEMA&#124;METRICS_SCHEMA&#124;INSPECTION_SCHEMA)$/.\*]` exports all tables except the system schema. |

    Make sure `${data-path}` has enough space to store the exported data. To prevent the import from being interrupted by a large table, it is strongly recommended to use the `-F` option to limit the size of a single file.

2. View the `metadata` file in the `${data-path}` directory. This is a Dumpling-generated metadata file. Record the binlog position information, which is required for the incremental replication in Step 3.

    ```
    SHOW MASTER STATUS:
    Log: mysql-bin.000004
    Pos: 109227
    GTID:
    ```

## Step 2. Import full data to TiDB

1. Create the `tidb-lightning.toml` configuration file:

    {{< copyable "" >}}

    ```toml
    [lightning]
    # log.
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # "local": Default backend. The local backend is used to import large volumes of data (1 TiB or more). During the import, the target TiDB cluster cannot provide any service.
    # "tidb": The "tidb" backend is used to import data less than 1 TiB. During the import, the target TiDB cluster can provide service normally. For more information on the backends, refer to https://docs.pingcap.com/tidb/stable/tidb-lightning-backends.
    backend = "local"
    # For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.
    sorted-kv-dir = "${sorted-kv-dir}"

    [mydumper]
    # The data source directory. The same directory where Dumpling exports data in Step 1.
    data-source-dir = "${data-path}"

    # Configures the wildcard rule. The default rule filters out all tables in these system databases: mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, INSPECTION_SCHEMA.
    # If you do not configure this item, TiDB Lightning reports a `cannot find schema` exception when it imports system tables.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # The target TiDB cluster information.
    host = ${host}                # e.g.: 172.16.32.1
    port = ${port}                # e.g.: 4000
    user = "${user_name}"         # e.g.: "root"
    password = "${password}"      # e.g.: "rootroot"
    status-port = ${status-port}  # Obtains the table schema information from TiDB status port, e.g.: 10080
    pd-addr = "${ip}:${port}"     # The cluster PD address, e.g.: 172.16.31.3:2379. TiDB Lightning obtains some information from PD. When backend = "local", you must specify status-port and pd-addr correctly. Otherwise, the import will be abnormal.
    ```

    For more information on TiDB Lightning configuration, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

2. Start the import by running `tidb-lightning`. If you launch the program directly in the command line, the program might exit because of the `SIGHUP` signal. In this case, it is recommended to run the program using a `nohup` or `screen` tool. For example:

    {{< copyable "shell-regular" >}}

    ```shell
    nohup tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

3. After TiDB Lightning completes the import, it exits automatically. If the import is successful, the last line of `tidb-lightning.log` prints `tidb lightning exit`.

If the import fails, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Step 3. Replicate incremental data to TiDB

### Add the data source

1. Create a `source1.yaml` file as follows:

    {{< copyable "" >}}

    ```yaml
    # Configuration.
    source-id: "mysql-01" # Must be unique.

    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL has automatic source-replica switching, GTID mode is required.
    enable-gtid: false

    from:
      host: "${host}"           # e.g.: 172.16.10.81
      user: "root"
      password: "${password}"   # Supported but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2. Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`operate-source create`|Loads the data source to the DM cluster.|

### Add a replication task

1. Edit the `task.yaml` file. Configure the incremental replication mode and the starting point of each data source:

    {{< copyable "shell-regular" >}}

    ```yaml
    name: task-test                      # Task name. Must be globally unique.
    task-mode: incremental               # Task mode. The "incremental" mode only performs incremental data replication.

    # Configures the target TiDB database.
    target-database:                     # The target database instance.
      host: "${host}"                    # e.g.: 127.0.0.1
      port: 4000
      user: "root"
      password: "${password}"            # It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

    # Use block and allow lists to specify the tables to be replicated.
    block-allow-list:                    # The collection of filtering rules that matches the tables in the source database instance. If the DM version is v2.0.0-beta.2 or earlier, use black-white-list instead.
      bw-rule-1:                         # The block-allow-list configuration item ID.
        do-dbs: ["${db-name}"]           # Name of databases to be replicated.

    # Configures the data source.
    mysql-instances:
      - source-id: "mysql-01"            # Data source ID，i.e., source-id in source1.yaml
        block-allow-list: "bw-rule-1"    # References the block-allow-list configuration above.
        # syncer-config-name: "global"    # References the syncers incremental data configuration below.
        meta:                            # When task-mode is "incremental" and the downstream database does not have a checkpoint, DM uses the binlog position as the starting point. If the downstream database has a checkpoint, DM uses the checkpoint as the starting point.
          binlog-name: "mysql-bin.000004"  # The binlog position recorded in Step 1. When the upstream database has source-replica switching, GTID mode is required.
          binlog-pos: 109227
          # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

    # (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
    # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
    # syncers:            # The running configurations of the sync processing unit.
    #   global:           # Configuration name.
    #     safe-mode: true # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
    ```

    The YAML above is the minimum configuration required for the migration task. For more configuration items, refer to [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full).

    Before you start the migration task, to reduce the probability of errors, it is recommended to confirm that the configuration meets the requirements of DM by running the `check-task` command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
    ```

2. Start the migration task by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`start-task`           |Starts the migration task.|

    If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

    If you encounter any problem, refer to [DM error handling](https://docs.pingcap.com/tidb-data-migration/stable/error-handling) and [DM FAQ](https://docs.pingcap.com/zh/tidb-data-migration/stable/faq).

### Check the migration task status

To learn whether the DM cluster has an ongoing migration task and view the task status, run the `query-status` command using `tiup dmctl`:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

### Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl print the related information in logs. The log directories of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](https://docs.pingcap.com/tidb-data-migration/stable/pause-task).
- [Resume the migration task](https://docs.pingcap.com/tidb-data-migration/stable/resume-task).
- [Stop the migration task](https://docs.pingcap.com/tidb-data-migration/stable/stop-task).
- [Export and import the cluster data source and task configuration](https://docs.pingcap.com/tidb-data-migration/stable/export-import-config).
- [Handle failed DDL statements](https://docs.pingcap.com/tidb-data-migration/stable/handle-failed-ddl-statements).
