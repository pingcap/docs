---
title: Migrate and Merge MySQL Shards of Less Than 1 TiB to TiDB
summary: Learn how to consolidate MySQL shards of less than 1 TiB to TiDB.
---

# Migrate and Merge MySQL Shards of Less Than 1 TiB to TiDB

If you want to migrate and merge multiple MySQL database instances upstream to one TiDB database downstream, and the amount of data is not too large (for example, the sum of all MySQL shards is less than 1 TiB), you can use DM to migrate MySQL shards. Through examples in this document, you can learn the operation steps, precautions, and troubleshooting of the migration.

This document applies to migrating MySQL shards less than 1 TiB in total. If you want to migrate MySQL shards with a total of more than 1 TiB of data, it will take a long time by using DM. In this case, it is recommended that you follow the operation introduced in [Migrate and Merge MySQL Shards of More Than 1 TB to TiDB](/migrate-sharding-mysql-tidb-above-tb.md) to perform migration.

This document takes a simple example to illustrate the migration procedure. The MySQL shards of the two data source MySQL instances in the example are migrated to the downstream TiDB cluster. The diagram is shown as follows.

![Use DM to Migrate Sharded Tables](/media/migrate-shard-tables-within-1tb-en.png)

Assume that data sources MySQL Instance 1 and MySQL Instance 2 use the same table structure as follows:

  | Schema | Table |
  |:------|:------|
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

Target schemas and tables：

| Schema | Table |
|:------|:------|
| store | sale |

## Prerequisites

Before starting the migration, make sure you have completed the following tasks:

- [Deploy a DM Cluster Using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup)
- [Privileges required by DM-worker](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro#privileges-required-by-dm-worker)

### Check conflicts for the sharded tables

If the migration involves sharded tables, data from multiple sharded tables may cause conflicts for primary keys or unique indexes. Therefore, before migration, you need to check the business characteristics of each sharded table. For more details, see [Handle conflicts between primary keys or unique indexes across multiple sharded tables](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables).

In this example, `sale_01` and `sale_02` have the same table structure as follows

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

The `id` column is the primary key, and the `sid` column is the sharding key. The `id` column is auto-incremental, and duplicated multiple sharded table ranges will cause data conflicts. The `sid` can ensure that the index is globally unique, so you can follow the steps in [Remove the primary key attribute of the auto-incremental primary key](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column) to bypasses the `id` column.

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

## Step 1: Load data sources

Create a file named `source1.yaml`. The configuration file is as follows:

{{< copyable "shell-regular" >}}

```yaml
# Configuration.
source-id: "mysql-01" # Must be unique.

# Specifies whether DM-worker pulls binlogs with GTID (Global Transaction Identifier).
# The prerequisite is that you have already enabled GTID in the upstream MySQL.
# If the upstream database has enabled automatic switch of primary and standby, you must use the GTID mode.
enable-gtid: false
from:
  host: "${host}" # For example: 172.16.10.81
  user: "root"
  password: "${password}" # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.
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
|--master-addr         | {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261|
|operate-source create | Load data sources to the DM cluster. |

Repeat the above steps until all data sources are added to the DM cluster.

## Step 2: Configure the migration task

Create a file named `task1.yaml` and writes the following content to it:

{{< copyable "shell-regular" >}}

```yaml
name: "shard_merge"
# Task mode. You can set it to the following:
# - full: Performs full data migration
# - incremental: Performs binlog real-time replication
# - all: Performs both full data and binlog replication
task-mode: all
# Required for the MySQL shards. By default, the "pessimistic" mode is used.
# If you have a deep understanding of the principles and usage limitations of the optimistic mode, you can also use the "optimistic" mode.
# For more information, see [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
shard-mode: "pessimistic"
meta-schema: "dm_meta"                        # A schema will be created in the downstream database to store the metadata
ignore-checking-items: ["auto_increment_ID"]  # In this example, there are auto-incremental primary keys upstream, so you do not need to check this item.

target-database:
  host: "${host}"                             # For example: 192.168.0.1
  port: 4000
  user: "root"
  password: "${password}"                     # Plaintext passwords are supported but not recommended. It is recommended that you use dmctl encrypt to encrypt plaintext passwords.

mysql-instances:
  -
    source-id: "mysql-01"                                    # ID of the data source, which is source-id in source1.yaml
    route-rules: ["sale-route-rule"]                         # Table route rules applied to the data source
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

# Filters out some DDL events.
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

The above example is the minimum configuration to perform the migration task. For more information, see [DM Advanced Task Configuration File](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-file-full).

For more information on `routes`, `filters` and other configurations in the task file, see the following documents:

- [Table routing](https://docs.pingcap.com/tidb-data-migration/stable/key-features#table-routing)
- [Block & Allow Table Lists](https://docs.pingcap.com/tidb-data-migration/stable/key-features#block-and-allow-table-lists)
- [Binlog event filter](https://docs.pingcap.com/tidb-data-migration/stable/key-features#binlog-event-filter)
- [Filter Certain Row Changes Using SQL Expressions](https://docs.pingcap.com/tidb-data-migration/stable/feature-expression-filter)

## Step 3: Start the task

Before starting a migration task, run the `check-task` command to check whether the configuration meets the requirements of DM so as to avoid possible errors.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Run the following command in `tiup dmctl` to start a migration task:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

| Parameter | Description|
|-|-|
|--master-addr| {advertise-addr} of any DM-master node in the cluster that dmctl connects to. For example: 172.16.10.71:8261 |
|start-task   | Starts the data migration task. |

If the migration task fails to start, modify the configuration information according to the error information, and then run `start-task task.yaml` again to start the migration task. If you encounter problems, see [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling) and [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq).

## Step 4: Check the task

After starting the migration task, you can use `dmtcl tiup` to run `query-status` to view the status of the task.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

If you encounter errors, use `query-status <name of the error task>` to view more detailed information. For details about the query results, task status and sub task status of the `query-status` command, see [TiDB Data Migration Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

## Step 5: Monitor tasks and check logs (optional)

You can view the history of a migration task and internal operational metrics through Grafana or logs.

- Via Grafana
    If Prometheus, Alertmanager, and Grafana are correctly deployed when you deploy the DM cluster using TiUP, you can view DM monitoring metrics in Grafana. Specifically, enter the IP address and port specified during deployment in Grafana and select the DM dashboard.

- Via logs

    When DM is running, DM-master, DM-worker, and dmctl output logs, which includes information about migration tasks. The log directory of each component is as follows.

    - DM-master log directory: It is specified by the DM-master process parameter `--log-file`. If DM is deployed using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/`.
    - DM-worker log directory: It is specified by the DM-worker process parameter `--log-file`. If DM is deployed using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/`.

## See also

- [Migrate and Merge MySQL Shards of More Than 1 TiB to TiDB](/migrate-sharding-mysql-tidb-above-tb.md)。
- [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
- [Best Practices of Data Migration in the Shard Merge Scenario](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices)
- [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling)
- [Handle Performance Issues](https://docs.pingcap.com/zh/tidb-data-migration/stable/handle-performance-issues)
- [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq)