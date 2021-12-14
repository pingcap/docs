---
title: Import and Merge Large MySQL Sharding Schemas and Sharding Tables to TiDB (Greater Than 1 TiB)
summary: Use Dumpling and TiDB Lightning to merge and import MySQL sharding schemas and sharding tables into TiDB. The method described in this article is suitable for scenarios where the total amount of imported data is greater than 1 TiB.
---

# Import and Merge Large MySQL Sharding Schemas and Sharding Tables to TiDB (Greater Than 1 TiB)

If the total size of the sharding tables is large (for example, greater than 1 TiB) and allows the TiDB cluster to suspend business writes during the migration, then you can use TiDB Lightning to quickly merge and import the sharding table data. After import, you can also use TiDB DM for incremental data replication according to your business needs.

This document walks you through the procedure of how to import large sharding schemas and sharding tables into TiDB.

If the data size of the sharding tables is less than 1 TiB, you can follow the procedure described in [Migrate sharding Schemas and Tables to TiDB]( https://docs.pingcap.com/tidb-data-migration/stable/usage-scenario-shard-merge), which supports both full and incremental import.

The following diagram shows how to import sharding schemas and sharding tables into TiDB using Dumpling and TiDB Lightning.

![Use Dumpling and TiDB Lightning to merge and import sharding schemas and sharding tables into TiDB](/media/shard-merge-using-lightning-en.png)

This example assumes that you have two databases, `my_db1` and `my_db2`. You use Dumpling to export two tables `table1` and `table2` from `my_db1`, and two tables `table3` and `table4` from `my_db2`, respectively. After that, you use TiDB Lighting to merge and import the four exported tables into the same `table5` in the downstream TiDB.

Note that although Dumpling can export all databases from a MySQL instance, this document only exports some of the data as an example.

In this document, you can import data following this procedure:

1. Use Dumpling to export full data. In this example, you export 2 tables respectively from 2 upstream databases:

   - Export table1 and table 2 from my_db1
   - Export table3 and table 4 from my_db2

2. Start TiDB Lightning to import data to mydb.table5 in TiDB.

3. (Optional) Use TiDB DM to perform incremental import.

## Prerequisites

Before getting started, see the following documents to prepare for the import task.

- [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [Use TiUP to Deploy Dumpling and Lightning](/migration-tools.md)
- [Privileges required by DM-worker](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro#privileges-required-by-dm-worker)
- [Upstream Permissions for Lightning](/tidb-lightning/tidb-lightning-faq#what-is-the-privilege-requirements-for-the-target-database)
- [Downstream Permissions for Dumpling](/dumpling-overview.md##export-data-from-tidbmysql)

### Hardware requirements of TiDB Lightning

**Operating System**: The example in this document uses a few fresh CentOS 7 instances. You can deploy a small virtual machine either locally virtualized or on cloud. Because TiDB Lightning consumes 100% CPU by default, it is recommended that you deploy it on a dedicated server. If this is not possible due to a tight budget, you can deploy it on a single server together with other TiDB components (e.g. `tikv-server`) and then configure `region-concurrency` to limit the CPU usage. Usually you can configure the size to 75% of the logical CPU.

**Memory and CPU**: Since TiDB Lightning is resource-intensive, it is recommended to allocate more than 64 GiB of memory and more than 32 CPU cores. Meanwhile, to achieve optimal performance, make sure the CPU core to memory (GiB) ratio is greater than 1:2.

**Disk Space**:

- Dumpling requires a hard drive sufficient to store the entire data source. It is recommended to use SSD. The faster the read speed, the better.
- Lightning requires sufficient temporary storage space to store sorted key-value pairs during import. You need to prepare at least as much space as the largest single table of the data source.

**Note**: It is difficult to calculate the exact size of the data exported by Dumpling from MySQL. But you can estimate the amount of data using the `data_length` field with the following SQL statement.

{{< copyable "sql" >}}

```sql
# Calculate all schema sizes in MiB. You need to change ${schema_name} to your actual schema name.
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables group by table_schema;

# Calculate the maximum single table in MiB. You need to change ${schema_name} to your actual schema name.

select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;
```

### Disk space requirements for the target TiKV cluster

The target TiKV cluster must have enough space to store the upcoming imported data. In addition to the [standard hardware configuration](https://docs.pingcap.com/tidb/stable/hardware-and-software-requirements), the total storage space of the target TiKV cluster must be larger than **data source size × [number of replicas](https://docs.pingcap.com/tidb/stable/deploy-and-maintain-faq#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it.) × 2**. For example, if the cluster uses 3 copies by default, then the total storage space needs to be more than 6 times the size of the data source.

At first glance, it may look confusing why there is a “x2” in the formula. In fact, it is based on the following estimated space:

* Indexes can consume extra space.
* There is a space amplification effect of RocksDB.

### Conflict check for sharding tables

If the migration involves sharding schemas and tables, data from multiple sharding tables may cause conflicts for primary keys or unique indexes. Therefore, before migration, you need to check the business characteristics of each sharding table. For more details, see [Cross-Sub-table Data in Primary Key or Unique Index Conflict Handling](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables). The following is a brief description.

Assume that tables1~4 have the same table structure as follows.

```sql
CREATE TABLE `table1` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

Where the `id` column contains the primary key. It is auto-incremental, and duplicate ranges of multiple sharding tables will cause data conflicts. The `sid` column contains the sharding key, which ensures that the index is unique globally. So you can remove the unique key attribute of the `id` column in the downstream `table5`.

```sql
CREATE TABLE `table5` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

The following sections introduce the complete import procedure.

## Step1. Use Dumpling to export full data

If you need to export multiple sharding tables belonging to the same upstream MySQL instance, you can directly use the `-f` parameter of Dumpling to export them in a single operation.

If the sharding tables are stored across different MySQL instances, you can use Dumpling to export them respectively and place the results of both exports in the same parent directory.

In the following example, both methods are used, and then the exported data is stored in the same parent directory.

First, run the following command to use Dumpling to export table1 and table2 from my_db:

```
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-path}/my_db1
```

In the command above:

- `-u` or `--user` specifies the user name to be used. If a password is required for authentication, you can use `-p $YOUR_SECRET_PASSWORD` to pass the password to Dumpling.
- `-p` or `--password` specifies the password to be used.
- `-p` or `--port` specifies the port to be used.
- `-h` or `--host` specifies the IP address of the data source.
- `-t` or `--thread` specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and increases the database's memory consumption. Therefore, it is not recommended to set the number too large.
- `-o` or `--output` specifies the export directory of the storage, which supports a local file path or a [URL of an external storage](/br/backup-and-restore-storages.md).
- `-r` or `--row` specifies the maximum number of rows in a single file. If you use this parameter, Dumpling enables the in-table concurrency to speed up the export and reduce the memory usage.
- `-F` specifies the maximum size of a single file. The unit is `MiB`. Inputs such as `5GiB` or `8KB` are also acceptable. It is recommended to keep the value to 256 MiB or less, if you use TiDB Lightning to load this file into a TiDB instance.
- `-B` or `--database` specifies databases to be exported.
- `-f` or `--filter` export tables that match the filter pattern. For the filter syntax, see [table-filter](/table-filter.md).

> **Note:**
>
> If the size of a single exported table exceeds 10 GB, it is strongly recommended to use the `-r` and `-F` options.
Then, run the following command to use Dumpling to export table3 and table4 from my_db2:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db1.table[32]' -o ${data-path}/my_db2
```

The reason for storing all source data tables in one directory is to facilitate subsequent import by TiDB Lightning.

The starting point information needed for Step 3 Incremental Replication is in the `${data-path}` directory, and in the `metadata` files of `my_db1` and `my_db2`. They are meta-information files automatically generated by Dumpling. To perform incremental replication, you need to note down the binlog location information.

Congratulations! Now you have exported all the required full data.

## Step 2. Start TiDB Lightning to import data

Before starting TiDB Lightning for import, it is recommended that you understand how to handle checkpoints, and then choose the appropriate way to proceed according to your needs.

### Checkpoints

Importing a large volume of data usually takes hours or even days. If such a long running processes unfortunately crashes, it can be very frustrating to redo everything from scratch.

Fortunately, TiDB Lightning provides a `checkpoints` feature to let you store the import progress, so that import task can resume from the breakpoint upon restart.

If the TiDB Lightning task crashes due to unrecoverable errors (for example, data corruption), it will not pick up from the breakpoint, but will report an error and quit the task. You need to solve the problem first by using the tidb-lightning-ctl program. The options include:

* --checkpoint-error-destroy: This option allows you to restart importing from scratch.
* --checkpoint-error-ignore: If import has failed, this option clears the error status as if no errors ever happened.
* --checkpoint-remove: This option simply clears all checkpoints, regardless of errors.

For more information, see [TiDB Lightning Checkpoints](https://docs.pingcap.com/tidb/stable/tidb-lightning-checkpoints).

### Create the target schema

After you make changes in the aforementioned `Conflict check for sharding tables`, you can now manually create the `my_db` schema and `table5` in downstream TiDB. After that, you need to configure `tidb-lightning.toml`.

```toml
[mydumper]
no-schema = true # If the schema and tables are already created downstream, `true` means not to create the schema.
```

### Start the import task

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
    # "local": The default mode. It is used for large data volumes greater than 1 TiB. But during import, downstream TiDB is not available to provide service.
    # "tidb": Can also be used for data volumes less than 1 TiB. During import, downstream TiDB can provide service normally. For more information, see https://docs.pingcap.com/tidb/stable/tidb-lightning-backends
    backend = "local"
    # Set the temporary directory for the sorted key value pairs. It must be empty. The free space must be greater than the largest single table of the data source. It is recommended that you have a different disk directory from `data-source-dir` to get better import performance with exclusive IO.
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
    data-source-dir = "${data-path}"
    # Because table1~4 are merged into table5, you do not need to create a schema. This parameter can prevent creating table1~4 downstream based on Dumpling's exported files.
    no-schema = true
    # Configure the wildcard rules. By default, all tables in the following will be filtered: mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, INSPECTION_SCHEMA
    # If not configured, an error “schema not found” will occur when importing system tables.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # Information of the target TiDB cluster. Values here are only for illustration purpose. Replace them with your own values.
    host = ${host}           # For example: "172.16.31.2"
    port = ${port}           # For example: 4000
    user = "${user_name}"    # For example: "root"
    password = "${password}" # For example: "rootroot"
    # The table information is read from the status port.
    status-port = ${status-port} # For example: 10080
    # the IP address of the cluster PD. Values here are only for illustration purpose. Replace them with your own values.
    pd-addr = "${ip}:${port}"    # For example: "172.16.31.3:2379". When backend = "local", make sure that the values of status-port and pd-addr are correct. Otherwise an error will occur.
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

After the import is finished, TiDB Lightning will quit automatically. To make sure the data is imported successfully, you need to check that the log shows `the whole procedure completed` among the last 5 lines.

> **Note:**
>
> Whether the import is successful or not, the last line will always show `tidb lightning exit`. It just means that TiDB Lightning quits normally, and does not guarantee that the task is completed successfully.

If you encounter any problems during import, see [TiDB Lightning FAQ](https://docs.pingcap.com/tidb/stable/tidb-lightning-faq).

## Step 3. (Optional) Use DM to perform incremental import to TiDB

To import the source database to TiDB based on the Binlog from a specified position, you can use TiDB DM to perform incremental import.

### Add the data source

Create a new `source1.yaml` file, and add the following content:

{{< copyable "" >}}

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.

# Specify whether DM-worker pulls binlogs with GTID (Global Transaction Identifier). The prerequisite is that you have already enabled GTID in the upstream MySQL. If the automatic switch of primary and standby exists in the upstream database, you need to use the GTID mode.
enable-gtid: false

from:
  host: "${host}"           # For example: 172.16.10.81
  user: "root"
  password: "${password}"   # Plaintext passwords is supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
  port: ${port}   # For example: 3306
```

Run the following command in a terminal. Use `tiup dmctl` to load the data source configuration into the DM cluster:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr 172.16.10.71:8261 operate-source create source1.yaml
```

The parameters are described as follows.

|Parameter      | Description |
|-              |-            |
|--master-addr         | {advertise-addr} of any DM-master node in the cluster that dmctl connects to.|
| operate-source create | Load data sources to DM clusters. |

Repeat the above steps until all MySQL instances are added to the DM.

### Create a replication task

Create task configuration `task.yaml` to configure incremental replication mode and replication starting point for each data source. The complete task configuration example is as follows:

{{< copyable "" >}}

```yaml
name: task-test               # The name of the task. Should be globally unique.
task-mode: incremental        # The mode of the task. "incremental" means only incremental data is migrated.
# Required for the sharding schemas and tables. By default, the "pessimistic" mode is used.
# If you have a deeper understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/zh/tidb-data-migration/stable/feature-shard-merge).

shard-mode: "pessimistic"
## Configure the access information of TiDB database instance:
target-database:              # Downstream database instance configuration.
  host: "${host}"             # For example: 127.0.0.1
  port: 4000
  user: "root"
  password: "${password}"     # If password is not empty, it is recommended to use dmctl encrypted password.
## Use block-allow-list to configure tables that require sync:
block-allow-list:             # The filter rule set of the matched table of the data source database instance. Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule-1:                  # # The ID of the block and allow list rule.
    do-dbs: ["my_db1"]        # The databases to be migrated. Here, my_db1 of instance 1 and my_db2 of instance 2 are configured as two separate rules to demonstrate how to avoid my_db2 of instance 1 from being replicated.
  bw-rule-2:
    do-dbs: ["my_db2"]
routes:                               # Table routing rules between upstream and downstream tables
  route-rule-1:                       # Rule name. Merge and import table1 and table2 from my_db1 to the downstream my_db.table5
    schema-pattern: "my_db1"          # Routing rule for the schema. It supports the wildcards "*" and "?".
    table-pattern: "table[1-2]"       # Routing rule for the table. It supports the wildcards "*" and "?".
    target-schema: "my_db"            # Name of the target schema.
    target-table: "table5"            # Name of the target table.
  route-rule-2:                       # Rule name. Merge and import table3 and table4 from my_db2 to the downstream my_db.table5
    schema-pattern: "my_db2"
    table-pattern: "table[3-4]"
    target-schema: "my_db"
    target-table: "table5"
## Configure data sources, using two data sources as examples
mysql-instances:
  - source-id: "mysql-01"             # Data source ID. It is the source-id in source1.yaml
    block-allow-list: "bw-rule-1"     # Use the block and allow list configuration above. Replicate my_db1 in instance 1.
    route-rules: ["route-rule-1"]     # Use the configured routing rule above.
#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The task-mode is incremental and there is no binlog starting point in the checkpoint in the downstream database. If the checkpoint exists, then use the checkpoint.
      binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db1/metadata in Step 1. It must use gtid when there is a primary-standby switch upstream.
      binlog-pos: ${binlog-position}
      # binlog-gtid:                  " For example: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
  - source-id: "mysql-02"             # Data source ID. It is the source-id in source1.yaml.
    block-allow-list: "bw-rule-2"     # Use the block and allow list configuration. my_db2 in the instance2.
    route-rules: ["route-rule-2"]     # Use the configured routing rule above.
#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The task-mode is incremental and there is no binlog starting point in the checkpoint in the downstream database. If the checkpoint exists, then use the checkpoint.
      binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db2/metadata in Step 1. It must use gtid when there is a primary-standby switch upstream.
      binlog-pos: ${binlog-position}
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
## (Optional) If you need to migrate full data that has already been migrated during a full-data migration, you need to enable the safe mode to data migration errors during incremental replication.
## This scenario is mostly seen when the fully migrated data is not part of a consistent snapshot of the data source, and then the incremental data is replicated from a location earlier than the fully migrated data.
# syncers:           # The running parameters of the sync processing unit.
#  global:           # Configuration name.
#    safe-mode: true # If set to true, it changes INSERT from the data source to REPLACE, and UPDATE from the data source to DELETE and REPLACE. Thus, it can import DML repeatedly during migration when primary keys or unique indexes exist in the table structure. TiDB DM automatically starts safe mode within 1 minute before starting or resuming an incremental replication task.
```

For more configurations, see [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full/)

Before you start the data migration task, it is recommended to use the `check-task` command to check if the configuration meets the DM configuration requirements.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Use tiup dmctl to run the following command to start the data migration task.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters in this command are described as follows.

| Parameter | Description|
|-|-|
|--master-addr| {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261 |
|start-task   | Starts the data migration task. |

If the task fails to start, first make configuration changes according to the returned result, and then run the start-task task.yaml command to restart the task. If you encounter problems, refer to [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling) and [TiDB Data Migration FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq)

### Check the import result

You can check if there are running migration tasks in the DM cluster and their status. Use `tiup dmctl` to run the `query-status` command to query.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For more information, see [Query Status](https://docs.pingcap.com/zh/tidb-data-migration/stable/query-status)

### Monitor tasks and view logs

To view the history status of the migration task and more internal operational metrics, you can refer to the following methods.

If Prometheus, Alertmanager and Grafana are correctly deployed when you deploy the DM cluster using TiUP, you can view DM monitoring metrics in Grafana.

When DM is running, DM-worker, DM-master and dmctl output logs. The log directory of each component is as follows.

- DM-master log directory: It is specified by the --log-file DM-master process parameter. If DM is deployed using TiUP, the log directory is {log_dir} in the DM-master node.
- DM-worker log directory: It is specified by the --log-file DM-worker process parameter. If DM is deployed using TiUP, the log directory is {log_dir} in the DM-worker node.

## See also

- [Dumpling](/dumpling-overview.md)
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
- [Pessimistic mode and optimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
- [Pause a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/pause-task)
- [Resume a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/resume-task)
- [Stop a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/stop-task)
- [Export and Import Data Sources and Task Configuration of Clusters](https://docs.pingcap.com/tidb-data-migration/stable/export-import-config)
- [Handle Failed DDL Statements](https://docs.pingcap.com/tidb-data-migration/stable/handle-failed-ddl-statements)