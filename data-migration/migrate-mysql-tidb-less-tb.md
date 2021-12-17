---
title: Migrate MySQL Data of Less Than 1 TiB to TiDB
summary: Learn how to migrate data less than 1 TiB from MySQL to TiDB.
---

# Migrate MySQL Data of Less Than 1 TiB to TiDB

This document describes how to use TiDB DM (hereinafter referred to as DM) to migrate data that is less than 1 TiB to TiDB in the full migration mode and incremental replication mode. Generally speaking, affected by the information such as the number of table structure indexes, hardwares, and network environment, the migration rate varies from 30 to 50 GB/h. The migration process using TiDB DM is shown in the figure below.

![dm](/media/dm/migrate-with-dm.png)

## Prerequisites

- [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [Get the source database and target database privileges required for DM](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro)

## Step 1. Create the data source

First, create the `source1.yaml` file as follows:

{{< copyable "" >}}

```yaml
# Configuration.
source-id: "mysql-01"     # Must be unique.

# Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must have enabled GTID. If the upstream MySQL has automatic source-replica switching, GTID mode is required.
enable-gtid: false

from:
  host: "${host}"         # For example: 172.16.10.81
  user: "root"
  password: "${password}" # Supported but not recommended to use plaintext password. It is recommended to use dmctl encrypt to encrypt the plaintext password before using it.
  port: 3306
```

Then, load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

The parameters used in the command above are described as follows:

|Parameter           |Description|
|-              |-|
|`--master-addr`  |The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected. For example: 172.16.10.71:8261.
|`operate-source create`|Load the data source to the DM cluster.|

## Step 2. Create the migration task

Create the `task1.yaml` file as follows:

{{< copyable "" >}}

```yaml
# Task name. Multiple tasks that are running at the same time must each have a unique name.
name: "test"
# Task mode. Options are:
# full: only performs full data migration.
# incremental: only performs binlog real-time replication.
# all: full data migration + binlog real-time replication.
task-mode: "all"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # For example: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Supported but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

# The configuration of all MySQL instances of source database required for the current migration task.
mysql-instances:
-
  # The ID of an upstream instance or a replication group
  source-id: "mysql-01"
  # The names of the block and allowlist configuration of the schema name or table name that is to be migrated. These names are used reference the global configuration of the block and allowlist. For the global configuration, refer to the `block-allow-list` configuration below.
  block-allow-list: "listA"          # If the DM version is v2.0.0-beta.2 or earlier, use black-white-list instead.

# The global configuration of block and allow list. Each instance is referenced by a configuration item name.
block-allow-list:                     # If the DM version is v2.0.0-beta.2 or earlier, use black-white-list instead.
  listA:                              # name
    do-tables:                        # The allowlist of upstream tables that need to be migrated.
    - db-name: "test_db"              # The schema name of the table to be migrated.
      tbl-name: "test_table"          # The name of the table to be migrated.

```

The above is the minimum task configuration to perform the migration. For more configuration items regarding the task, refer to [DM task complete configuration file introduction](https://docs.pingcap.com/zh/tidb-data-migration/stable/task-configuration-file-full/).

## Step 3. Run the migration task

To reduce the probability of subsequent errors, before starting the migration task, it is recommended to use the `check-task` command to check whether the configuration meets the requirements of DM configuration.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Start the migration task by running the following command with `tiup dmctl`.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters used in the command above are described as follows:

|Parameter|Description|
|-|-|
|`--master-addr`|The {advertise-addr} of any DM-master in the cluster where `dmctl` is to be connected. For example: 172.16.10.71:8261.
|`start-task`|Start the migration task|

If the task fails to start, after changing the configuration according to the returned result, you can run the `start-task task.yaml` command to restart the task. If you encounter problems, refer to [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling/) and [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq).

## Step 4: Check the migration task status

To learn whether the DM cluster has an ongoing migration task, the task status and some other information, run the `query-status` command using `tiup dmctl`:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

## Step 5. Monitor the task and view logs （optional)

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

- The log directory of DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- The log directory of DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](https://docs.pingcap.com/tidb-data-migration/stable/pause-task)
- [Resume the migration task](https://docs.pingcap.com/tidb-data-migration/stable/resume-task)
- [Stop the migration task](https://docs.pingcap.com/tidb-data-migration/stable/stop-task)
- [Export and import the cluster data source and task configuration](https://docs.pingcap.com/tidb-data-migration/stable/export-import-config)
- [Handle failed DDL statements](https://docs.pingcap.com/tidb-data-migration/stable/handle-failed-ddl-statements)
