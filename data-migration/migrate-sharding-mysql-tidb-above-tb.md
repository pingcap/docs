---
title: Migrate and Merge MySQL Shards of More Than 1 TiB to TiDB
summary: Learn how to migrate and merge MySQL shards of more than 1 TiB to TiDB using Dumpling and TiDB Lightning.
---

# Migrate and Merge MySQL Shards of More Than 1 TiB to TiDB

If you want to migrate a large MySQL dataset (for example, more than 1 TiB) from different partitions into TiDB, and you are able to suspend all the TiDB cluster write operations from your business during the migration, you can use TiDB Lightning to do the migration quickly. After migration, you can also use TiDB DM to perform incremental replication according to your business needs.

This document uses an example to walk through the whole procedure of such kind of migration.

If the data size of the MySQL shards is less than 1 TiB, you can follow the procedure described in [Migrate and Merge MySQL Shards of Less Than 1 TB to TiDB](/data-migration/migrate-sharding-mysql-tidb-less-tb.md), which supports both full and incremental migration and the steps are easier.

The following diagram shows how to migrate MySQL shards to TiDB using Dumpling and TiDB Lightning.

![Use Dumpling and TiDB Lightning to migrate and merge MySQL shards to TiDB](/media/shard-merge-using-lightning-en.png)

This example assumes that you have two databases, `my_db1` and `my_db2`. You use Dumpling to export two tables `table1` and `table2` from `my_db1`, and two tables `table3` and `table4` from `my_db2`, respectively. After that, you use TiDB Lighting to import and merge the four exported tables into the same `table5` from `mydb` in the target TiDB.

Note that although Dumpling can export all databases from a MySQL instance, this document only exports some of the data as an example.

In this document, you can migrate data following this procedure:

1. Use Dumpling to export full data. In this example, you export 2 tables respectively from 2 upstream databases:

   - Export `table1` and `table2` from my_db1
   - Export `table3` and `table4` from my_db2

2. Start TiDB Lightning to migrate data to `mydb.table5` in TiDB.

3. (Optional) Use TiDB DM to perform incremental replication.

## Prerequisites

Before getting started, see the following documents to prepare for the migration task.

- [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [Use TiUP to Deploy Dumpling and Lightning](/migration-tools.md)
- [Privileges required by DM-worker](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro#privileges-required-by-dm-worker)
- [Upstream Permissions for Lightning](/tidb-lightning/tidb-lightning-faq#what-is-the-privilege-requirements-for-the-target-database)
- [Downstream Permissions for Dumpling](/dumpling-overview.md##export-data-from-tidbmysql)

### Hardware requirements of TiDB Lightning

**Operating System**: The example in this document uses fresh CentOS 7 instances. You can deploy a small virtual machine either on your host locally or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, `tikv-server`) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**: Since TiDB Lightning is resource-intensive, it is recommended to allocate more than 64 GiB of memory and more than 32 CPU cores. Meanwhile, to achieve optimal performance, make sure that the CPU core to memory (GiB) ratio is greater than 1:2.

**Disk Space**:

- Dumpling requires a hard drive sufficient to store the entire data source. It is recommended to use SSD. The faster the read speed, the better.
- TiDB Lightning requires sufficient temporary storage space to store sorted key-value pairs during migration. You need to prepare at least as much space as the largest single table of the data source.

**Note**: It is difficult to calculate the exact size of the data exported by Dumpling from MySQL. But you can estimate the amount of data using the `data_length` field with the following SQL statement.

{{< copyable "sql" >}}

```sql
# Calculate the size of all schemas in MiB. You need to change ${schema_name} to the actual schema name.
select table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables group by table_schema;

# Calculate the size of the largest single table in MiB. You need to change ${schema_name} to the actual schema name.

select table_name,table_schema,sum(data_length)/1024/1024 as data_length,sum(index_length)/1024/1024 as index_length,sum(data_length+index_length)/1024/1024 as sum from information_schema.tables where table_schema = "${schema_name}" group by table_name,table_schema order by sum  desc limit 5;

### Disk space requirements for the target TiKV cluster

The target TiKV cluster must have enough space to store upcoming migrated data. In addition to the [Server recommendations](https://docs.pingcap.com/tidb/stable/hardware-and-software-requirements#server-recommendations), the total storage space of the target TiKV cluster must be larger than **(data source size) × ([number of replicas](https://docs.pingcap.com/tidb/stable/deploy-and-maintain-faq#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) × 2**. For example, if the cluster uses 3 replicas by default, the total storage space needs to be more than 6 times the size of the data source.

At first glance, it may look confusing why there is a **“x2”** in the formula. In fact, it is based on the following estimated space:

* Extra space consumed by indexes
* Space amplified by RocksDB

### Check conflicts for Sharded Tables

If the migration involves sharded tables, data from multiple sharded tables may cause conflicts for primary keys or unique indexes. Therefore, before migration, you need to check the business characteristics of each sharded table. For more details, see [Handle conflicts between primary keys or unique indexes across multiple sharded tables](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables). The following is a brief description.

Assume that tables 1~4 have the same table structure as follows.

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

For those four tables, the `id` column is the primary key. It is auto-incremental, which will cause different sharded tables to generate duplicated `id` ranges and cause the primary key conflict on the target table during the migration. On the other hand, the `sid` column is the sharding key, which ensures that the index is unique globally. So you can remove the unique constraint of the `id` column in the target `table5` to avoid the data merge conflicts

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

The following sections introduce the complete migration procedure.

## Step1. Use Dumpling to export full data

If you need to export multiple sharded tables belonging to the same upstream MySQL instance, you can directly use the `-f` parameter of Dumpling to export them in a single operation.

If the sharded tables are stored across different MySQL instances, you can use Dumpling to export them respectively and place the exported results in the same parent directory.

In the following example, both methods are used, and then the exported data is stored in the same parent directory.

First, run the following command to use Dumpling to export `table1` and `table2` from `my_db1`:

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db1 -f 'my_db1.table[12]' -o ${data-path}/my_db1
```

In the command above:
| Parameter       |   Description |
|-                |-              |
| `-u` or `--user`       |   Specifies the user name to be used. If a password is required for authentication, you can use `-p $YOUR_SECRET_PASSWORD` to pass the password to Dumpling. |
| `-p` or `--password`   |   Specifies the password to be used. |
| `-p` or `--port`       |   Specifies the port to be used.|
| `-h` or `--host`       |   Specifies the IP address of the data source.  |
| `-t` or `--thread`     |   Specifies the number of threads for the export. Increasing the number of threads improves the concurrency of Dumpling and the export speed, and increases the database's memory consumption. Therefore, it is not recommended to set the number too large.|
| `-o` or `--output`     |  Specifies the export directory of the storage, which supports a local file path or a [URL of an external storage](/br/backup-and-restore-storages.md).|
| `-r` or `--row`        | Specifies the maximum number of rows in a single file. If you use this parameter, Dumpling enables the in-table concurrency to speed up the export and reduce the memory usage.|
| `-F` |  Specifies the maximum size of a single file. The unit is `MiB`. Inputs such as `5GiB` or `8KB` are also acceptable. It is recommended to keep the value to 256 MiB or less, if you use TiDB Lightning to load this file into a TiDB instance. |
| `-B` or `--database`   | Specifies databases to be exported. |
| `-f` or `--filter`     |  Sexport tables that match the filter pattern. For the filter syntax, see [table-filter](/table-filter.md) |

> **Note:**
>
> If the size of a single exported table exceeds 10 GiB, it is strongly recommended to use the `-r` and `-F` options.

Then, run the following command to use Dumpling to export `table3` and `table4` from `my_db2`. Note that the path is `${data-path}/my_db2` instead of `${data-path}/my_db1`.

{{< copyable "shell-regular" >}}

```shell
tiup dumpling -h ${ip} -P 3306 -u root -t 16 -r 200000 -F 256MB -B my_db2 -f 'my_db2.table[34]' -o ${data-path}/my_db2
```

After the preceding procedures, all source data tables are now exported to the `${data-path}` directory. Putting all the exported data on the same directory makes subsequent import by TiDB Lightning convenient.

The starting position information needed for incremental replication is in the `metadata` files in `my_db1` and `my_db2` sub-directories of `${data-path}` directory respectively. They are meta-information files automatically generated by Dumpling. To perform incremental replication, you need to record the binlog locations information in these files.

## Step 2. Start TiDB Lightning to import full exported data

Before starting TiDB Lightning for migration, it is recommended that you understand how to handle checkpoints, and then choose the appropriate way to proceed according to your needs.

### Checkpoints

Migrating a large volume of data usually takes hours or even days. There is a certain chance that the long-running process is interrupted unexpectedly. It can be very frustrating to redo everything from scratch, even if some part of data has already been imported.

Fortunately, TiDB Lightning provides a `checkpoints` feature to let you store the migration progress, so that an interrupted migration task can resume from the breakpoint upon restart.

If the TiDB Lightning task crashes due to unrecoverable errors (for example, data corruption), it will not pick up from the checkpoint, but will report an error and quit the task. To ensure the safety of the imported data, you must resolve these errors by using the `tidb-lightning-ctl` command before proceeding with other steps. The options include:

* --checkpoint-error-destroy: This option allows you to restart importing data into failed target tables from scratch by destroying all the existing data in those tables first.
* --checkpoint-error-ignore: If migration has failed, this option clears the error status as if no errors ever happened.
* --checkpoint-remove: This option simply clears all checkpoints, regardless of errors.

For more information, see [TiDB Lightning Checkpoints](https://docs.pingcap.com/tidb/stable/tidb-lightning-checkpoints).

### Create the target schema

After you make changes in the aforementioned [Check conflicts for sharded tables](data-migration\migrate-sharding-mysql-tidb-above-tb.md#check-conflicts-for-sharding-tables), you can now manually create the `my_db` schema and `table5` in downstream TiDB. After that, you need to configure `tidb-lightning.toml`.

```toml
[mydumper]
no-schema = true # If you have created the downstream schema and tables, setting `true` tells TiDB Lightning not to create the downstream schema.
```

### Start the migration task

Follow these steps to start `tidb-lightning`:

1. Upload the exported full data to the server where TiDB Lightning is deployed.
2. Edit the toml file. `tidb-lightning.toml` is used in the following example:

    ```toml
    [lightning]
    # Logs
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # Choose a local backend.
    # "local": The default mode. It is used for large data volumes greater than 1 TiB. During migration, downstream TiDB cannot provide services.
    # "tidb": Used for data volumes less than 1 TiB. During migration, downstream TiDB can provide services normally.
    # For more information, see [TiDB Lightning Backends](https://docs.pingcap.com/tidb/stable/tidb-lightning-backends)
    backend = "local"
    # Set the temporary directory for the sorted key value pairs. It must be empty.
    # The free space must be greater than the largest single table of the data source.
    # It is recommended that you use a directory different from `data-source-dir` to get better migration performance by consuming IO resources exclusively.
    sorted-kv-dir = "${sorted-kv-dir}"

    # Set the renaming rules ('routes') from source to target tables, in order to support merging different table shards into a single target table. Here you migrate `table1` and `table2` in `my_db1`, and `table3` and `table4` in `my_db2`, to the target `table5` in downstream `my_db`.
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
    # The source data directory. Set this to the path of the Dumpling exported data.
    # If there are several Dumpling-exported data directories, you need to place all these directories in the same parent directory, and use the parent directory here.
    data-source-dir = "${data-path}"
    # Because table1~table4 from source are merged into another table5 in the target, you should tell TiDB Lightning no need to create schemas, so that table1 ~ table4 won't be created automatically according to the exported schema information
    # This parameter can prevent creating tables1~4 downstream based on files exported by Dumpling.
    no-schema = true
    # Configure the wildcard rules. By default, all the following tables will be filtered: mysql, sys, INFORMATION_SCHEMA, PERFORMANCE_SCHEMA, METRICS_SCHEMA, INSPECTION_SCHEMA
    # If not configured, an error “schema not found” will occur when migrating system tables.
    filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

    [tidb]
    # Information of the target TiDB cluster.
    # Values here are only for illustration purpose. Replace them with your own values.
    host = ${host}           # For example: "172.16.31.1"
    port = ${port}           # For example: 4000
    user = "${user_name}"    # For example: "root"
    password = "${password}" # For example: "rootroot"
    # The table information is read from the status port.
    status-port = ${status-port} # For example: 10080
    # the IP address of the PD cluster. TiDB Lightning gets some information through the PD cluster.
    # For example: "172.16.31.3:2379".
    # When backend = "local", make sure that the values of status-port and pd-addr are correct. Otherwise an error will occur.
    pd-addr = "${ip}:${port}"
    ```

3. Configure appropriate parameters to run `tidb-lightning`. If you start the task directly in a command-line interface, it may quit due to the SIGHUP signal. It is recommended that you introduce such tools as `nohup` and `screen`. For example:

   {{< copyable "shell-regular" >}}

   ```shell
   tiup tidb-lightning -config tidb-lightning.toml > nohup.out &
   ```

4. After starting the migration task, you can check the progress by using either of the following methods:

   - Use `grep` tool to search the keyword `progress` in the log. By default, a message reporting the progress is flushed into the log file every 5 minutes.
   - View progress via the monitoring dashboard. For more information, see [TiDB Lightning Monitoring]( /tidb-lightning/monitor-tidb-lightning.md).

After the importing finishes, TiDB Lightning will exit automatically. To make sure that the data is imported successfully, check for `the whole procedure completed` among the last 5 lines in the log.

> **Note:**
>
> Whether the migration is successful or not, the last line in the log will always be `tidb lightning exit`. It just means that TiDB Lightning quits normally, and does not guarantee that the importing task is completed successfully.

If you encounter any problems during migration, see [TiDB Lightning FAQs](/tidb-lightning/tidb-lightning-faq.md).

## Step 3. (Optional) Use DM to perform incremental replication

To replicate the data changes based on binlog from a specified position in the source database to TiDB, you can use TiDB DM to perform incremental replication.

### Add the data source

Create a new data source file called `source1.yaml`, which configures an upstream data source into DM, and add the following content:

{{< copyable "" >}}

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.

# Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
# The prerequisite is that you have already enabled GTID in the upstream MySQL.
# If the upstream database has enabled automatic switch of primary and standby, you must use the GTID mode.
enable-gtid: true

from:
  host: "${host}"           # For example: 172.16.10.81
  user: "root"
  password: "${password}"   # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
  port: ${port}             # For example: 3306
```

Run the following command in a terminal. Use `tiup dmctl` to load the data source configuration into the DM cluster:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

The parameters are described as follows.

|Parameter      | Description |
|-              |-            |
|--master-addr         | {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261|
| operate-source create | Load data sources to DM clusters. |

Repeat the above steps until all MySQL upstream instances are added to the DM as data sources.

### Create a replication task

Edit a task configuration file called `task.yaml`, to configure the incremental replication mode and replication starting point for each data source.

{{< copyable "" >}}

```yaml
name: task-test               # The name of the task. Should be globally unique.
task-mode: incremental        # The mode of the task. "incremental" means full data migration is skipped and only incremental replication is performed.
# Required for the sharded tables. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/zh/tidb-data-migration/stable/feature-shard-merge).

shard-mode: "pessimistic"

# Configure the access information of the TiDB database instance:
target-database:              # Downstream database instance
  host: "${host}"             # For example: 127.0.0.1
  port: 4000
  user: "root"
  password: "${password}"     # It is recommended to use a dmctl encrypted password.

# Use block-allow-list to configure tables that require sync:
block-allow-list:             # The set of filter rules on matching tables in the data sources, to decide which tables need to migrate and which not. Use the black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule-1:                  # The ID of the block and allow list rule.
    do-dbs: ["my_db1"]        # The databases to be migrated. Here, my_db1 of instance 1 and my_db2 of instance 2 are configured as two separate rules to demonstrate how to prevent my_db2 of instance 1 from being replicated.
  bw-rule-2:
    do-dbs: ["my_db2"]
routes:                               # Table renaming rules ('routes') from upstream to downstream tables, in order to support merging different sharded table into a single target table. 
  route-rule-1:                       # Rule name. Migrate and merge table1 and table2 from my_db1 to the downstream my_db.table5.
    schema-pattern: "my_db1"          # Rule for matching upstream schema names. It supports the wildcards "*" and "?".
    table-pattern: "table[1-2]"       # Rule for matching upstream table names. It supports the wildcards "*" and "?".
    target-schema: "my_db"            # Name of the target schema.
    target-table: "table5"            # Name of the target table.
  route-rule-2:                       # Rule name. Migrate and merge table3 and table4 from my_db2 to the downstream my_db.table5.
    schema-pattern: "my_db2"
    table-pattern: "table[3-4]"
    target-schema: "my_db"
    target-table: "table5"

# Configure data sources. The following uses two data sources as an example.
mysql-instances:
  - source-id: "mysql-01"             # Data source ID. It is the source-id in source1.yaml.
    block-allow-list: "bw-rule-1"     # Use the block and allow list configuration above. Replicate `my_db1` in instance 1.
    route-rules: ["route-rule-1"]     # Use the configured routing rule above to merge upstream tables.
#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The migration starting point of binlog when task-mode is incremental and there is no checkpoint in the downstream database. A checkpoint prevails if any.
      binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db1/metadata in Step 1. You can either specify binlog-name + binlog-pos or binlog-gtid. When the upstream database service is configured to switch master between different nodes automatically, use binlog GTID here. 
      binlog-pos: ${binlog-position}
      # binlog-gtid:                  " For example: 09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
  - source-id: "mysql-02"             # Data source ID. It is the source-id in source1.yaml.
    block-allow-list: "bw-rule-2"     # Use the block and allow list configuration above. Replicate `my_db2` in instance2.
    route-rules: ["route-rule-2"]     # Use the routing rule configured above.
#       syncer-config-name: "global"  # Use the syncers configuration below.
    meta:                             # The migration starting point of binlog when task-mode is incremental and there is no checkpoint in the downstream database. A checkpoint prevails if any.
      # binlog-name: "${binlog-name}"   # The log location recorded in ${data-path}/my_db2/metadata in Step 1. You can either specify binlog-name + binlog-pos or binlog-gtid. When the upstream database service is configured to switch master between different nodes automatically, use binlog GTID here. 
      # binlog-pos: ${binlog-position}
      binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"
# (Optional) If you need to incrementally replicate some data changes that have been covered in the full migration, you need to enable the safe mode to avoid data migration errors during incremental replication.
# This scenario is common when the fully migrated data is not part of a consistent snapshot of the data source, and the incremental data is replicated from a location earlier than the fully migrated data.
# syncers:           # The running parameters of the sync processing unit.
#  global:           # Configuration name.
# If set to true, DM changes INSERT to REPLACE, and changes UPDATE to a pair of DELETE and REPLACE for data source replication operations.
# Thus, it can apply DML repeatedly during replication when primary keys or unique indexes exist in the table structure.
# TiDB DM automatically starts safe mode within 1 minute before starting or resuming an incremental replication task.
#    safe-mode: true
```

For more configurations, see [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full/).

Before you start the data migration task, it is recommended to use the `check-task` subcommand in `tiup dmctl` to check if the configuration meets the DM configuration requirements.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Use `tiup dmctl` to run the following command to start the data migration task.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters in this command are described as follows.

| Parameter | Description|
|-|-|
|--master-addr| {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261 |
|start-task   | Starts the data migration task. |

If the task fails to start, first make configuration changes according to the prompt messages from the returned result, and then run the `start-task task.yaml` subcommand in `tiup dmctl` to restart the task. If you encounter problems, see [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling) and [TiDB Data Migration FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq).

### Check the migration status

You can check if there are running migration tasks in the DM cluster and their status by running the `query-status` command in `tiup dmctl`.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For more information, see [Query Status](https://docs.pingcap.com/zh/tidb-data-migration/stable/query-status).

### Monitor tasks and view logs

You can view the history of a migration task and internal operational metrics through Grafana or logs.

- Via Grafana
    If Prometheus, Alertmanager, and Grafana are correctly deployed when you deploy the DM cluster using TiUP, you can view DM monitoring metrics in Grafana. Specifically, enter the IP address and port specified during deployment in Grafana and select the DM dashboard.

- Via logs

    When DM is running, DM-master, DM-worker, and dmctl output logs, which includes information about migration tasks. The log directory of each component is as follows.

    - DM-master log directory: It is specified by the DM-master command line parameter `--log-file`. If DM is deployed using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/`.
    - DM-worker log directory: It is specified by the DM-worker command line parameter `--log-file`. If DM is deployed using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/`.

## See also

- [Dumpling](/dumpling-overview.md)
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)
- [Pessimistic mode and optimistic mode](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
- [Pause a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/pause-task)
- [Resume a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/resume-task)
- [Stop a Data Migration Task](https://docs.pingcap.com/tidb-data-migration/stable/stop-task)
- [Export and Import Data Sources and Task Configuration of Clusters](https://docs.pingcap.com/tidb-data-migration/stable/export-import-config)
- [Handle Failed DDL Statements](https://docs.pingcap.com/tidb-data-migration/stable/handle-failed-ddl-statements)