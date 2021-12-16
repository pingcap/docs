---
title: Migrate and Merge MySQL Shards of Less Than 1 TiB to TiDB
summary: Introduces how to consolidate MySQL sharded shcemas and tables into TiDB (Less Than 1 TiB).
---

# Migrate and Merge MySQL Shards of Less Than 1 TiB to TiDB

If you want to migrate and merge multiple MySQL database instances upstream to one TiDB database downstream, and the amount of data is not too large (for example, the sum of all MySQL shards is less than 1 TiB), you can use DM to migrate MySQL shards. Through examples in this article, you can learn the operation steps, precautions, and troubleshooting of the migration.

This document applies to migrating MySQL shards less than 1 TiB in total.

If you want to migrate MySQL shards with a total of more than 1 TiB of data, it will take a long time by using DM. It is recommended that you follow the operation introduced in [Migrate and Merge MySQL Shards of More Than 1 TiB to TiDB](/migrate-sharding-mysql-tidb-above-tb.md) to migrate data greater than 1 TiB.

This document takes a simple example to illustrate the migration procedure. The MySQL shards of the two data source MySQL instances in the example are migrated to the downstream TiDB cluster. The diagram is shown as follows.

![Use DM to Migrate Sharded Tables](/media/migrate-shard-tables-within-1tb-en.png)

Assume that data source MySQL Instance 1 and MySQL Instance 2 use the same table structure as follows:

  | Schema | Tables |
  |:------|:------|
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

Target schemas and tables：

| Schema | Tables |
|:------|:------|
| store | sale |

## Prerequisites

Before starting the migration, make sure you have completed the following tasks:

- [Use TiUP to Deploy a DM cluster](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [Get upstream and downstream database permissions](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro)

### Check conflicts in the sharded tables

Because the sharded tables are involved in the migration, data from multiple sharded tables may cause data conflicts in the primary key or unique index. Therefore, before the migration, you need to check the sharded table. For details, see [Cross table data conflict handling in primary key or unique index](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables).

In this example, the user.information table structure is as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE `sale_01` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

The `id` column is the primary key, and the `sid` column is the sharding key. The `id` column is auto-incremental, and duplicated multiple sharded table ranges will cause data conflicts. The `sid` can ensure that the index is globally unique, so you can follow the steps in [Remove the primary key attribute of the self-incrementing primary key](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column) to bypasses the `id` column.

{{< copyable "sql" >}}

```sql
CREATE TABLE `sale` (
  `id` bigint(20) NOT NULL,
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `sid` (`sid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

## Step 1: Load the data sources

Create a new file named `source1.yaml`. The configuration file is as follows:

{{< copyable "shell-regular" >}}

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.

# Specify whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
# The prerequisite is that you have already enabled GTID in the upstream MySQL.
# If the automatic switch of primary and standby exists in the upstream database, you need to use the GTID mode.
enable-gtid: false
from:
  host: "${host}" # For example: 172.16.10.81
  user: "root"
  password: "${password}" # Plaintext passwords is supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
  port: 3306
```

Run the following command in a terminal. Use `tiup dmctl` to load the data source configuration into the DM cluster:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

The parameters are described as follows.

|Parameter      | Description |
|-              |-            |
|--master-addr         | {advertise-addr} of any DM-master node in the cluster that dmctl connects to.|
|operate-source create | Load data sources to DM clusters. |

Repeat the above steps until all MySQL instances are added to the DM.

## Step 2: Configure the task

Create a new file named `task1.yaml`. The migration task is as follows.

{{< copyable "shell-regular" >}}

```yaml
name: "shard_merge"
# Task mode. You can set it to the following:
# - full: Performs full data migration
# - incremental: Performs binlog real-time replication
# - all: Performs both full data and binlog replication
task-mode: all
# Required for the MySQL shards. By default, the "pessimistic" mode is used.
# If you have a deeper understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
shard-mode: "pessimistic"
meta-schema: "dm_meta"                        # A schema will be created in the downstream database to store the metadata
ignore-checking-items: ["auto_increment_ID"]  # In this example, there are auto-incremental primary keys upstream, so you do not need to check this item.

target-database:
  host: "${host}"                             # For example: 192.168.0.1
  port: 4000
  user: "root"
  password: "${password}"                     # Plaintext passwords is supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.

mysql-instances:
  -
    source-id: "mysql-01"                                    # ID of the data source. It can be obtained from the data source configurations.
    route-rules: ["sale-route-rule"]                         # The table route rules applied to the data source
    filter-rules: ["store-filter-rule", "sale-filter-rule"]  # Binlog event filter rules applied to the data source
    block-allow-list:  "log-bak-ignored"                     # Block & Allow Lists rules applied to the data source
  -
    source-id: "mysql-02"
    route-rules: ["sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# Configurations for merging MySQL shards
routes:
  sale-route-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"

# Filters some DDL events.
filters:
  sale-filter-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore

# Block and allow list
block-allow-list:
  log-bak-ignored:
    do-dbs: ["store_*"]
```

The above example is the minimum task configuration to perform the migration. For more information, see [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full/).

For more information on `routes`, `filters` and other configurations in the task file, see the following documents:

- [Table routing](https://docs.pingcap.com/tidb-data-migration/stable/key-features#table-routing)
- [Block & Allow Table Lists](https://docs.pingcap.com/tidb-data-migration/stable/key-features#block--allow-table-lists)
- [Binlog event filter](https://docs.pingcap.com/tidb-data-migration/stable/key-features#binlog-event-filter)
- [Binlog expression filter](https://docs.pingcap.com/tidb-data-migration/stable/feature-expression-filter)

## Step 3: Start the task

In order to spot configuration errors in the data migration task in advance, DM provides the [Pre-check](https://docs.pingcap.com/tidb-data-migration/stable/precheck) function. When data migration starts, DM will automatically check related permissions and configurations.

You can also use the `check-task` command to manually check whether the configurations of the upstream MySQL instance meet the requirements.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Use the `dmctl` command to start the migration task:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

| Parameter | Description|
|-|-|
|--master-addr| {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261 |
|start-task   | Starts the data migration task. |

If the migration task fails to start, modify the configuration information according to the error information, and then run `start-task task.yaml` again to start the migration task. If you encounter problems, see [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling), and [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq).

## Step 4: Check the task

After starting the migration task, you can use `dmtcl tiup` to run `query-status` to view the status of the task.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

If you encounter errors, you can use `query-status <taskName of the error task>` to view more detailed information. For details about the query results, task status and sub task status of the `query-status` command, see [TiDB Data Migration Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

## Step 5: Monitor tasks and check logs (optional)

If Prometheus and Grafana are correctly deployed when using TiUP to deploy the DM cluster. For example, assume that the address of Grafana is 172.16.10.71, you can [open the page to enter Grafana](http://172.16.10.71:3000) in the browser and select the Dashboard of DM, and then you can view related monitoring items. For specific monitoring indicators, see [Monitor and Alarm Settings](https://docs.pingcap.com/tidb-data-migration/stable/monitor-a-dm-cluster).

You can also check the DM running status and related errors through the log file.

- DM-master log directory: set by the DM-master process parameter `--log-file`. If you use TiUP to deploy DM, the log directory is located at `/dm-deploy/dm-master-8261/log/`.
- DM-worker log directory: set by the DM-worker process parameter `--log-file`. If you use TiUP to deploy DM, the log directory is located at `/dm-deploy/dm-worker-8262/log/`.

## See also

- [Migrate and Merge MySQL Shards of More Than 1 TiB to TiDB](/migrate-sharding-mysql-tidb-above-tb.md)。
- [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
- [Best Practices of Data Migration in the Shard Merge Scenario](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices)
- [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling)
- [Handle Performance Issues](https://docs.pingcap.com/zh/tidb-data-migration/stable/handle-performance-issues)
- [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq)