---
title: Migrate Data from Amazon Aurora to TiDB
summary: Learn how to migrate data from Amazon Aurora to TiDB using DB snapshot.
aliases: ['/tidb/dev/migrate-from-aurora-using-lightning','/docs/dev/migrate-from-aurora-mysql-database/','/docs/dev/how-to/migrate/from-mysql-aurora/','/docs/dev/how-to/migrate/from-aurora/', '/tidb/dev/migrate-from-aurora-mysql-database/', '/tidb/dev/migrate-from-mysql-aurora/','/tidb/stable/migrate-from-aurora-using-lightning/']
---

# Migrate Data from Amazon Aurora to TiDB

This document describes how to migrate data from Amazon Aurora to TiDB. The migration process uses [DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html), which saves a lot of space and time.

The whole migration has two processes:

- Import full data to TiDB using TiDB Lightning
- Replicate incremental data to TiDB using DM (optional)

## Prerequisites

- [Install Dumpling and TiDB Lightning](/migration-tools.md). If you want to create the corresponding tables manually on the target side, do not install Dumpling.
- [Get the upstream database privileges required by Dumpling](/dumpling-overview.md#required-privileges).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).
- If you want to replicate incremental data with DM, before creating the migration snapshot, enable binary logging on the Aurora cluster and set `binlog_format=ROW` and `binlog_row_image=FULL`. For Aurora MySQL version 3, also set `binlog_transaction_compression=OFF`. Retain the required binlogs until DM catches up with the source. For details, see [Setting up binary log replication for Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.SettingUp.html) and [DM precheck](/dm/dm-precheck.md).

## Import full data to TiDB

### Step 1. Export and import the schema file

This section describes how to export the schema file from Amazon Aurora and import it to TiDB. If you have manually created the table in the target database, you can skip this step.

Before exporting the schema, create or select the snapshot you will use in [Step 2.1](#21-export-an-amazon-aurora-snapshot-to-amazon-s3), completing the binlog setup in that section first if you plan to use DM. The schema must match that snapshot. If the live source schema has changed since the snapshot was created, restore the snapshot to a temporary cluster as described in Step 2.1, then use that cluster as the Dumpling source (`${host}`) below. Keep the restored schema unchanged until the export completes. If you create tables manually in TiDB, ensure their definitions match the selected snapshot.

#### 1.1 Export the schema file from Amazon Aurora

Because the snapshot file from Amazon Aurora does not contain the DDL statements, you need to export the schema using Dumpling and create the schema in the target database using TiDB Lightning.

Export the schema using Dumpling by running the following command. The command includes the `--filter` parameter to only export the desired table schema. For more information about the parameters, see the [Option list of Dumpling](/dumpling-overview.md#option-list-of-dumpling).

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12],mydb.*' --consistency none --no-data --output 's3://my-bucket/schema-backup'
```

Record the URI of the schema exported in the above command, such as 's3://my-bucket/schema-backup', which will be used when importing the schema file later.

To get access to Amazon S3, you can pass the secret access key and access key of the account that has access to this Amazon S3 storage path into the Dumpling or TiDB Lightning node as environment variables. Dumpling and TiDB Lightning also support reading credential files from `~/.aws/credentials`. This method eliminates the need to provide the secret access key and access key again for all tasks on that Dumpling or TiDB Lightning node.

#### 1.2 Create the TiDB Lightning configuration file for the schema file

Create a new `tidb-lightning-schema.toml` file, copy the following content into the file, and replace the corresponding content.

```toml
[tidb]

# The target TiDB cluster information.
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"       # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the schema file exported from Amazon Aurora
data-source-dir = "s3://my-bucket/schema-backup"
```

If you need to enable TLS in the TiDB cluster, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

#### 1.3 Import the schema file to TiDB

Use TiDB Lightning to import the schema file to the downstream TiDB.

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning-schema.toml > nohup.out 2>&1 &
```

### Step 2. Export and import an Amazon Aurora snapshot to Amazon S3

This section describes how to export an Amazon Aurora snapshot to Amazon S3 and import it into TiDB by TiDB Lightning.

#### 2.1 Export an Amazon Aurora snapshot to Amazon S3

1. If you plan to use DM for incremental replication, configure the binlog settings in [Prerequisites](#prerequisites) before creating the snapshot. Use a custom DB cluster parameter group and reboot the writer instance as required for the changes to take effect. For details, see [Configuring Aurora MySQL binary logging](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_LogAccess.MySQL.BinaryFormat.html).

    If you plan to set `enable-gtid: true` in DM, also enable GTID mode on the original source before creating the snapshot. For setup instructions, see [Enabling GTID-based replication for an Aurora MySQL cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.configuring-aurora.html).

    Set a binlog retention period that covers the time from snapshot creation until DM catches up, including snapshot export, TiDB Lightning import, and a margin for delays. The following example sets retention to 144 hours (6 days) and displays the configuration for verification. Adjust the value to your migration duration and the limit supported by your Aurora version.

    ```sql
    CALL mysql.rds_set_configuration('binlog retention hours', 144);
    CALL mysql.rds_show_configuration;
    ```

    Skip this step if you only need full data migration.

2. Create or select the Aurora DB cluster snapshot to export. If you plan to use DM, obtain the binlog file name and position corresponding to this snapshot: restore the snapshot to a temporary Aurora cluster using the same parameter groups as the source, then find the `Binlog position from crash recovery is <binlog-file-name> <binlog-position>` message in the restored writer instance's **Recent Events**. For detailed instructions, see [Setting up binary log replication for Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.SettingUp.html). Record these values for the DM task, which must connect to the original source cluster. Delete the temporary cluster only after recording the position and exporting any schema needed in Step 1.

    For incremental replication, the required binlog settings must have been in effect when the snapshot was created. On the original source, use `SHOW BINARY LOGS;` to confirm that the required binlog file is still available, and retain all binlogs from that position until DM has processed them. If an existing snapshot does not meet these conditions, create a new snapshot after completing the binlog setup in step 1 of this section. Whenever you select a different snapshot, verify that the schema prepared in [Step 1](#step-1-export-and-import-the-schema-file) matches it. If it differs, export the schema from a temporary cluster restored from the new snapshot and update the target table definitions before importing the snapshot data. Do not use the current position from `SHOW MASTER STATUS` as a substitute for the snapshot position, because changes can be replayed or skipped.

    If enhanced binlog (`aurora_enhanced_binlog=1`) is enabled on the source cluster running Aurora MySQL version 3 earlier than 3.14.0, snapshot restoration can report incorrect binlog coordinates when transactions have been rolled back. Before using this procedure, upgrade the source to version 3.14.0 or later and create a new snapshot. For details, see the [Aurora MySQL 3.14.0 release notes](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraMySQLReleaseNotes/AuroraMySQL.Updates.3140.html).

3. Export the snapshot selected in step 2 to Amazon S3. For detailed steps, see [Exporting DB cluster snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-export-snapshot.html). The exported data reflects the snapshot's point in time, regardless of when the export task starts.

#### 2.2 Create the TiDB Lightning configuration file for the data file

Create a new `tidb-lightning-data.toml` configuration file, copy the following content into the file, and replace the corresponding content.

```toml
[tidb]

# The target TiDB cluster information.
host = "${host}"
port = "${port}"
user = "${user_name}"
password = "${password}"
status-port = "${status-port}"  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"       # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the snapshot file exported from Amazon Aurora
data-source-dir = "${s3_path}"  # eg: s3://my-bucket/sql-backup

[[mydumper.files]]
# The expression that parses the Parquet file.
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

If you need to enable TLS in the TiDB cluster, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

#### 2.3 Import full data to TiDB

1. Use TiDB Lightning to import data from an Amazon Aurora snapshot to TiDB.

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning-data.toml > nohup.out 2>&1 &
    ```

2. After the import starts, you can check the progress of the import by either of the following methods:

    - `grep` the keyword `progress` in the log. The progress is updated every 5 minutes by default.
    - Check progress in [the monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).

3. After TiDB Lightning completes the import, it exits automatically. Check whether `tidb-lightning.log` contains `the whole procedure completed` in the last lines. If yes, the import is successful. If no, the import encounters an error. Address the error as instructed in the error message.

> **Note:**
>
> Whether the import is successful or not, the last line of the log shows `tidb lightning exit`. It means that TiDB Lightning exits normally, but does not necessarily mean that the import is successful.

If you encounter any problem during the import, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Replicate incremental data to TiDB (optional)

### Prerequisites

- [Install DM](/dm/deploy-a-dm-cluster-using-tiup.md).
- [Get the source database and target database privileges required for DM](/dm/dm-worker-intro.md).

### Step 1: Create the data source

1. Create the `source1.yaml` file as follows:

    ```yaml
    # Must be unique.
    source-id: "mysql-01"
    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
    enable-gtid: false

    from:
      host: "${host}"         # e.g.: 172.16.10.81
      user: "root"
      password: "${password}" # Supported but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2. Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`operate-source create`|Loads the data source to the DM cluster.|

### Step 2: Create the migration task

Create the `task1.yaml` file as follows. Set `meta.binlog-name` and `meta.binlog-pos` to the snapshot-aligned values recorded in [Step 2.1](#21-export-an-amazon-aurora-snapshot-to-amazon-s3), and configure DM to read from the original source Aurora cluster.

If you set `enable-gtid: true`, also set `meta.binlog-gtid` to the GTID set corresponding to the recorded snapshot position. To obtain this set, use [`mysqlbinlog`](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html) to read the recorded source binlog file from its beginning with `--stop-position=<binlog-position>`. Combine the file's `Previous_gtids` set with the GTIDs of transactions completed before that position. Do not substitute the live source's current `gtid_executed` value, which can include transactions after the snapshot. For the configuration requirement, see [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

Create the task configuration as follows:

```yaml
# Task name. Multiple tasks that are running at the same time must each have a unique name.
name: "test"
# Task mode. Options are:
# - full: only performs full data migration.
# - incremental: only performs binlog real-time replication.
# - all: full data migration + binlog real-time replication.
task-mode: "incremental"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # e.g.: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Supported but not recommended to use a plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

# Global configuration for block and allow lists. Each instance can reference the configuration by name.
block-allow-list:                     # If the DM version is earlier than v2.0.0-beta.2, use black-white-list.
  listA:                              # Name.
    do-tables:                        # Allow list for the upstream tables to be migrated.
    - db-name: "test_db"              # Name of databases to be migrated.
      tbl-name: "test_table"          # Name of tables to be migrated.

# Configures the data source.
mysql-instances:
  - source-id: "mysql-01"               # Data source ID, i.e., source-id in source1.yaml
    block-allow-list: "listA"           # References the block-allow-list configuration above.
#       syncer-config-name: "global"    # Name of the syncer configuration.
    meta:                               # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
      binlog-name: "mysql-bin-changelog.018128" # Example only. Replace with the binlog file name recorded for your selected snapshot. When the upstream database has source-replica switching, GTID mode is required.
      binlog-pos: 52806 # Example only. Replace with the position recorded for your selected snapshot.
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
   # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
   # syncers:            # The running configurations of the sync processing unit.
   #   global:            # Configuration name.
   #     safe-mode: true  # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
```

The YAML file above is the minimum configuration required for the migration task. For more configuration items, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

### Step 3. Run the migration task

Before you start the migration task, to reduce the probability of errors, it is recommended to confirm that the configuration meets the requirements of DM by running the `check-task` command:

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

After that, start the migration task by running `tiup dmctl`:

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
|`start-task`           |Starts the migration task.|

If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

If you encounter any problem, refer to [DM error handling](/dm/dm-error-handling.md) and [DM FAQ](/dm/dm-faq.md).

### Step 4. Check the migration task status

To learn whether the DM cluster has an ongoing migration task and the task status, run the `query-status` command using `tiup dmctl`:

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](/dm/dm-query-status.md).

### Step 5. Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl print the related information in logs. The log directories of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](/dm/dm-pause-task.md).
- [Resume the migration task](/dm/dm-resume-task.md).
- [Stop the migration task](/dm/dm-stop-task.md).
- [Export and import the cluster data source and task configuration](/dm/dm-export-import-config.md).
- [Handle failed DDL statements](/dm/handle-failed-ddl-statements.md).
