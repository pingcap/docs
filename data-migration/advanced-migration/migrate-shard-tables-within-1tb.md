---
title: Use DM to Migrate Sharded Tables (within 1 TB)
summary: Introduces how to use DM to migrate sharded tables (within 1 TB).
---

# Use DM to Migrate Sharded Tables (within 1 TB)

If you want to merge and migrate multiple MySQL database instances upstream to one TiDB database downstream, and the amount of data is not too large (for example, the sum of all sharded tables is less than 1 TB), you can use DM to migrate sharded tables. Through examples in this article, you can learn the operation steps, precautions, and troubleshooting of the migration.

This document applies to migration of sharded tables within 1 TB in total.

If you want to migrate sharded tables with a total of more than 1 TB of data, it will take a long time by using DM. It is recommended that you follow the operation introduced in [Using Dumpling and TiDB Lightning to migrate sharded table data](/migrate-from-mysql-shard-merge-using-lightning.md) to migrate data larger than 1 TB.

## Migration Scenarios

This article takes a simple scenario as an example. The sharded tables of the two data source MySQL instances in the example are migrated to the downstream TiDB cluster. The diagram is shown as follows.

![Use DM to Migrate Sharded Tables](/media/migrate-shard-tables-within-1tb-en.png)

Assume that the schema and table structures of the two data source instances are as follows:

Data source MySQL Instance 1:

  | Schema | Tables |
  |:------|:------|
  | user  | information, log_bak |
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

Data source MySQL Instance 2:

  | Schema | Tables |
  |:------|:------|
  | user  | information, log_bak |
  | store_01 | sale_01, sale_02 |
  | store_02 | sale_01, sale_02 |

Target schemas and tables：

| Schema | Tables |
|:------|:------|
| user | information |
| store | sale |

## Prerequisites

Before starting the migration, complete the following tasks:

- Deploy a DM cluster
- Get upstream and downstream database permissions
- Check conflicts in the sharded tables
- Understand the basic functions of DM

### Deploy a DM cluster

You can deploy a DM cluster in a variety of ways. Currently, it is recommended to use TiUP to deploy DM clusters. For the deployment method, see [Deploy DM cluster using TiUP](https://docs.pingcap.com/tidb-data-migration/stable/deploy-a-dm-cluster-using-tiup).

### Get upstream and downstream database permissions

You must have corresponding read and write permissions of upstream and downstream databases. For details on permission requirements, see [DM-worker required permissions](https://docs.pingcap.com/tidb-data-migration/stable/dm-worker-intro#privileges-required-by-dm-worker).

### Check conflicts in the sharded tables

If sharded tables are involved in the migration, data from multiple sharded tables may cause data conflicts in the primary key or unique index. Therefore, before the migration, you need to check the business characteristics of each sharded table. For details, see [Cross table data conflict handling in primary key or unique index](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#handle-conflicts-between-primary-keys-or-unique-indexes-across-multiple-sharded-tables)

In this example, the user.information table structure is as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE `information` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `uid` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

The id column is the primary key, and the uid column is the unique index. The id column has an auto-increment attribute, and duplicate of multiple sharded table ranges will cause data conflicts. The uid can ensure that the index is globally unique, so you can follow the article [Remove the primary key attribute of the self-incrementing primary key](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column) to bypasses the id column. The table structure of `store_{01|02}.sale_{01|02}` is as follows:

{{< copyable "sql" >}}

```sql
CREATE TABLE `sale_01` (
  `sid` bigint(20) NOT NULL,
  `pid` bigint(20) NOT NULL,
  `comment` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sid`),
  KEY `pid` (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

In this example, sid is the sharding key, which can guarantee that the same sid can only be divided into one sharded table. So no data conflict will be caused, and no additional operations are required.

### Understand the basic functions of DM

DM provides [Table routing](https://docs.pingcap.com/tidb-data-migration/stable/key-features#table-routing), [Block & Allow Table Lists](https://docs.pingcap.com/tidb-data-migration/stable/key-features#block--allow-table-lists), [Binlog event filter](https://docs.pingcap.com/tidb-data-migration/stable/key-features#binlog-event-filter) and other basic functions, suitable for different migration scenarios. Before migrating, it is recommended to understand these basic functions and select them according to your own requirements.

#### Table routing

Table routing can migrate tables of upstream MySQL/MariaDB instances to downstream designated tables. It is also a core function required for migration of sharded tables. In a migration scenario of sharded tables, if the tables `store_{01|02}.sale_{01|02}` of the upstream two MySQL instances need to be merged into the `store.sale` table in the downstream TiDB, the following table routing rules can be used:

```
routes:
  ...
  store-route-rule: # Migrate store_{01|02} in upstream to store in downstream.
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule: # Migrate store_{01|02}.sale_{01|02} in upstream to store.sale in downstream.
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"
```

For more information, see [Table routing](https://docs.pingcap.com/tidb-data-migration/stable/key-features#table-routing).

#### Block & Allow Table Lists

The block & allow list filtering rules of the table in the upstream database instance can be used to filter to only migrate all operations of certain databases or tables. For more information, see [Block & Allow Table Lists](https://docs.pingcap.com/zh/tidb-data-migration/stable/key-features#block--allow-table-lists).

#### Binlog event filter

Binlog event filter provides more fine-grained filtering rules than the block & allow table lists of the migration table. You can specify that only certain types of binlogs of the schema or table are migrated or filtered, such as INSERT and TRUNCATE TABLE. For more information, see [Binlog event filter](https://docs.pingcap.com/tidb-data-migration/stable/key-features#binlog-event-filter).

## Migration Solutions

You can choose different migration solutions according to your needs. The following examples introduce several common migration requirements and applicable solutions.

### Scenario 1: Migrate databases with the same name in upstream and downstream

Assume that you need to merge `user.information` in the upstream database into the `user.information` table in the downstream TiDB. To meet this migration requirement, there is no need to configure table routing rules. In accordance with the requirement to [remove the primary key attribute of the self-incrementing primary key](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices#remove-the-primary-key-attribute-from-the-column), you can manually create a table in the downstream database.

```sql
CREATE TABLE `information` (
  `id` bigint(20) NOT NULL,
  `uid` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `data` varchar(255) DEFAULT NULL,
  INDEX (`id`),
  UNIQUE KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
```

And skip the pre-check in the configuration file.

```
ignore-checking-items: ["auto_increment_ID"]
```

### Scenario 2: Use Table routing to migrate sharded tables

Assume that you want to merge the `store_{01|02}.sale_{01|02}` tables in the example into the `store.sale` table in the downstream TiDB. To meet the migration requirement, you need to configure the table routing rules as follows:

```
routes:
  store-route-rule: # Migrate store_{01|02} tables in upstream to store in downstream.
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule: # Migrate store_{01|02}.sale_{01|02} tables in upstream to store.sale in downstream.
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"
```

### Scenario 3: Migrate with Block & Allow Lists

Assume that you want to merge `user` and `store_{01|02}` databases, but exclude the `user.log_bak` table in two instances. To meet the migration requirement, you need to configure Block & Allow Lists as follows:

```
block-allow-list:
  log-bak-ignored:
    do-dbs: ["user", "store_*"]
    ignore-tables:
    - db-name: "user"
      tbl-name: "log_bak"
```

### Scenario 4: Migrate with Binlog event filter

Filter out all the delete operations of the `store_{01|02}.sale_{01|02}` tables in the two instances, and filter the `drop database` operations of the library. To meet the migration requirement, you need to configure the Binlog event filter rules as follows:

```
filters:
  sale-filter-rule:     # Filter out delete operations of any table in the store_*
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  store-filter-rule:   # Filter out delete operations of store_*
    schema-pattern: "store_*"
    events: ["drop database"]
    action: Ignore
```

### Scenario 5: Use SQL expressions to filter row changes

Starting from v2.0.5, DM supports the use of SQL expressions to filter certain row changes. In the ROW format binlog supported by DM, binlog event carries the values of all columns. You can configure SQL expressions based on these values. If the calculation result of the expression for a row change is TRUE, DM will not migrate the row change downstream. For more details, see [Use SQL expressions to filter certain row changes](https://docs.pingcap.com/tidb-data-migration/stable/feature-expression-filter).

After deciding the migration plan, you can follow the steps below to migrate your data.

## Step 1: Load the data sources

Before running the data migration task, you need to load the data source configurations to DM, including encrypting access password, preparing data source configuration files, and loading data source configurations.

### Encrypt access password of data sources

For security concerns, it is recommended to use an encrypted MySQL access password. With DM v2.0, you can use the plaintext password to configure the access password information of the data sources. If you have not set the password for the data source, you can skip this step.

Take the password "123456" as an example:

```
tiup dmctl --encrypt "123456"
```

```
fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg=
```

Record the encrypted password and use it to create a new MySQL data source below.

### Prepare the configuration files of the data sources 

Write the content of the MySQL1 configuration file to mysql-source1-conf.yaml. The configuration file is as follows:

```
# MySQL Configuration.
source-id: "mysql1"
from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

Write the content of the MySQL2 configuration file to mysql-source2-conf.yaml. The configuration file is as follows:

```
# MySQL Configuration.
source-id: "mysql2"
from:
  host: "127.0.0.1"
  user: "root"
  password: "fCxfQ9XKCezSzuCD0Wf5dUD+LsKegSg="
  port: 3306
```

### Load data source configurations

Run the following command in the terminal and use `dmctl` to first load the data source configurations of MySQL1 into the DM cluster:

```shell
tiup dmctl --master-addr=127.0.0.1:8261 operate-source create mysql-source1-conf.yaml
```

The output result is as follows:

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql1",
            "worker": "worker1"
        }
    ]
}
```

In this way, MySQL1 is successfully added to the DM cluster.

Follow the above instructions to add MySQL2 to the DM cluster.

## Step 2: Configure the task

The complete configuration task.yaml of the migration task is as follows. For more details, see [Data Migration Task Configuration Guide](https://docs.pingcap.com/tidb-data-migration/stable/task-configuration-guide). This configuration includes the configuration of multiple scenarios in the above migration scheme.

```
name: "shard_merge"
task-mode: all                                   # Perform full data migration + incremental migration
meta-schema: "dm_meta"
ignore-checking-items: ["auto_increment_ID"]
target-database:
  host: "192.168.0.1"
  port: 4000
  user: "root"
  password: ""
mysql-instances:
  -
    source-id: "mysql1"        # ID of the data source. It can be obtained from the data source onfigurations. 
    route-rules: ["store-route-rule", "sale-route-rule"] # The table route rules applied to the data source
    filter-rules: ["store-filter-rule", "sale-filter-rule"] # Binlog event filter rules applied to the data source
    block-allow-list:  "log-bak-ignored" # Block & Allow Lists rules applied to the data source
  -
    source-id: "mysql2"
    route-rules: ["store-route-rule", "sale-route-rule"]
    filter-rules: ["store-filter-rule", "sale-filter-rule"]
    block-allow-list:  "log-bak-ignored"

# Other common configurations shared by all instances

routes:
  store-route-rule:
    schema-pattern: "store_*"
    target-schema: "store"
  sale-route-rule:
    schema-pattern: "store_*"
    table-pattern: "sale_*"
    target-schema: "store"
    target-table:  "sale"

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

block-allow-list:
  log-bak-ignored:
    do-dbs: ["user", "store_*"]
    ignore-tables:
    - db-name: "user"
      tbl-name: "log_bak"
```

## Step 3: Start the task

为了提前发现数据迁移任务的一些配置错误，DM 中增加了[前置检查](https://docs.pingcap.com/zh/tidb-data-migration/stable/precheck)功能，在开始数据迁移的时候，DM 会自动检查相关权限和配置。你也可以使用 `check-task` 命令手动检查上游 MySQL 实例的配置是否满足要求。

In order to spot configuration errors in the data migration task in advance, DM provides the [Pre-check](https://docs.pingcap.com/tidb-data-migration/stable/precheck) function. When data migration starts, DM will automatically check related permissions and configurations. You can also use the `check-task` command to manually check whether the configurations of the upstream MySQL instance meet the requirements.

Use the `dmctl` command to start the migration task: 

```shell
tiup dmctl --master-addr 127.0.0.1:8261 start-task task.yaml
```

After the migration task is successfully started, a message similar to the following will be displayed:

```
{
    "result": true,
    "msg": "",
    "workers": [
        {
            "result": true,
            "worker": "127.0.0.1:8261",
            "msg": ""
        },
        {
            "result": true,
            "worker": "127.0.0.2:8262",
            "msg": ""
        }
    ]
}
```

If the migration task fails to start, modify the configuration information according to the error information, and then run `start-task task.yaml` again to start the migration task. If you encounter problems, see [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling), and [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq).

## Step 4: Check the task.

After starting the migration task, you can use `dmtcl query-status` to view the status of the task.

```shell
tiup dmctl --master-addr 127.0.0.1:8261 query-status
```

If you encounter errors, you can use `query-status <taskName of the error task>` to view more detailed information. For details about the query results, task status and sub task status of the `query-status` command, see [TiDB Data Migration Query Status](https://docs.pingcap.com/tidb-data-migration/stable/query-status).

## Step 5: Monitor tasks and check logs

If Prometheus and Grafana are correctly deployed when using TiUP to deploy the DM cluster, for example, assume that the address of Grafana is 172.16.10.71, you can [open the page to enter Grafana](http://172.16.10.71:3000) in the browser and select the Dashboard of DM, and then you can view related monitoring items. For specific monitoring indicators, see [Monitor and Alarm Settings](https://docs.pingcap.com/tidb-data-migration/stable/monitor-a-dm-cluster).

You can also check the DM running status and related errors through the log file.

- DM-master log directory: set by the DM-master process parameter `--log-file`. If you use TiUP to deploy DM, the log directory is located at /dm-deploy/dm-master-8261/log/.
- DM-worker log directory: set by the DM-worker process parameter `--log-file`. If you use TiUP to deploy DM, the log directory is located at /dm-deploy/dm-worker-8262/log/.

## See also

- [Use Dumpling and TiDB Lightning to Migrate Sharded Tables (Larger than 1 TB)](/migrate-from-mysql-shard-merge-using-lightning.md)。
- [Merge and Migrate Data from Sharded Tables](https://docs.pingcap.com/tidb-data-migration/stable/feature-shard-merge)
- [Best Practices of Data Migration in the Shard Merge Scenario](https://docs.pingcap.com/tidb-data-migration/stable/shard-merge-best-practices)
- [Handle Errors](https://docs.pingcap.com/tidb-data-migration/stable/error-handling)
- [FAQ](https://docs.pingcap.com/tidb-data-migration/stable/faq)