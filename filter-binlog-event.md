---
title: Filter Binlog Events
summary: Learn how to filter binlog events when migrating data.
---

# Filter Binlog Events

This document describes how to filter binlog events when you use DM to perform continuous incremental data replication. For the detailed replication instructions, refer to the following documents by scenarios:

- [Migrate Small Datasets from MySQL to TiDB](/migrate-small-mysql-to-tidb.md)
- [Migrate Large Datasets from MySQL to TiDB](/migrate-large-mysql-to-tidb.md)
- [Migrate and Merge MySQL Shards of Small Datasets to TiDB](/migrate-small-mysql-shards-to-tidb.md)
- [Migrate and Merge MySQL Shards of Large Datasets to TiDB](/migrate-large-mysql-shards-to-tidb.md)

## Configuration

To use binlog event filters, add the `filters` field to the DM task configuration file, as shown below:

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    action: Ignore
```

After defining a filter rule, reference it in `filter-rules` under the corresponding `mysql-instances` entry. Otherwise, DM does not apply the rule to that source.

```yaml
mysql-instances:
  - source-id: "mysql-replica-01"
    filter-rules: ["rule-1"]
```

For more information, see [Data Migration task configuration guide](/dm/dm-task-configuration-guide.md#configure-binlog-events-to-be-migrated).

- `schema-pattern`/`table-pattern`: filters matching schemas or tables.
- `events`: filters binlog events. Supported events are listed in the following table:

  | Event | Category | Description |
  | --- | --- | --- |
  | `all` |  | Includes all events. |
  | `all dml` |  | Includes all DML events. |
  | `all ddl` |  | Includes all DDL events. |
  | `incompatible ddl changes` |  | Includes all incompatible DDL events that might cause data loss. |
  | `none` |  | Includes no events. |
  | `none ddl` |  | Excludes all DDL events. |
  | `none dml` |  | Excludes all DML events. |
  | `insert` | DML | The `INSERT` DML event. |
  | `update` | DML | The `UPDATE` DML event. |
  | `delete` | DML | The `DELETE` DML event. |
  | `create database` | DDL | The `CREATE DATABASE` DDL event. |
  | `drop database` | incompatible DDL | The `DROP DATABASE` DDL event. |
  | `create table` | DDL | The `CREATE TABLE` DDL event. |
  | `create index` | DDL | The `CREATE INDEX` DDL event. |
  | `drop table` | incompatible DDL | The `DROP TABLE` DDL event. |
  | `truncate table` | incompatible DDL | The `TRUNCATE TABLE` DDL event. |
  | `rename table` | incompatible DDL | The `RENAME TABLE` DDL event. |
  | `drop index` | incompatible DDL | The `DROP INDEX` DDL event. |
  | `alter table` | DDL | The `ALTER TABLE` DDL event. |
  | `value range decrease` | incompatible DDL | Decreases the value range of a column field. |
  | `precision decrease` | incompatible DDL | Decreases the precision of a column field. |
  | `modify column` | incompatible DDL | Changes a column field type. |
  | `rename column` | incompatible DDL | Changes a column name. |
  | `rename index` | incompatible DDL | Changes an index name. |
  | `drop column` | incompatible DDL | Drops a column from a table. |
  | `truncate table partition` | incompatible DDL | Removes all data from a specified partition. |
  | `drop primary key` | incompatible DDL | Drops the primary key. |
  | `drop unique key` | incompatible DDL | Drops a unique key. |
  | `modify default value` | incompatible DDL | Modifies a column default value. |
  | `modify constraint` | incompatible DDL | Modifies a constraint. |
  | `modify columns order` | incompatible DDL | Modifies the order of columns. |
  | `modify charset` | incompatible DDL | Modifies a column character set. |
  | `modify collation` | incompatible DDL | Modifies a column collation. |
  | `remove auto increment` | incompatible DDL | Removes an auto-increment attribute. |
  | `modify storage engine` | incompatible DDL | Modifies the table storage engine. |
  | `reorganize table partition` | incompatible DDL | Reorganizes table partitions. |
  | `rebuild table partition` | incompatible DDL | Rebuilds a table partition. |
  | `exchange table partition` | incompatible DDL | Exchanges a partition between two tables. |
  | `coalesce table partition` | incompatible DDL | Decreases the number of partitions in a table. |

- `sql-pattern`: filters specified DDL SQL statements. The matching rule supports regular expressions.
- `action`: `Do`, `Ignore`, or `Error`.

    - `Do`: the allow list.

        - If you configure only `events`, DM replicates only events whose types match `events`.
        - If you configure only `sql-pattern`, DM replicates only DDL statements whose SQL text matches `sql-pattern`.
        - If you configure both `events` and `sql-pattern` for a DDL statement, DM replicates the statement only when both the event type and the SQL text match the rule.

    - `Ignore`: the block list. DM filters out a binlog event if either of the following conditions is met:

        - The event type matches `events`.
        - `sql-pattern` is configured and the SQL statement matches any item in `sql-pattern`.

    - `Error`: the error list. DM reports an error if either of the following conditions is met:

        - The event type matches `events`.
        - `sql-pattern` is configured and the SQL statement matches any item in `sql-pattern`.

    When multiple rules match the same table, `Ignore` has higher priority than `Error`, and `Error` has higher priority than `Do`.

## Application scenarios

This section describes the application scenarios of binlog event filter.

### Filter out all sharding deletion operations

To filter out all deletion operations, configure a `filter-table-rule` and a `filter-schema-rule`, as shown below:

```
filters:
  filter-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table", "delete"]
    action: Ignore
  filter-schema-rule:
    schema-pattern: "test_*"
    events: ["drop database"]
    action: Ignore
```

### Migrate only DML operations of sharded schemas and tables

To replicate only DML statements, configure two `Binlog event filter rule`, as shown below:

```
filters:
  do-table-rule:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["create table", "all dml"]
    action: Do
  do-schema-rule:
    schema-pattern: "test_*"
    events: ["create database"]
    action: Do
```

### Handle SQL statements that TiDB does not support or that DM cannot parse

You do not need to configure filters for `CREATE PROCEDURE`, `DROP PROCEDURE`, or `ALTER PROCEDURE`. DM skips these statements automatically.

When you add or drop a partition in MySQL, DM normally replicates the change to TiDB. You do not need a filter for partition operations that both DM and TiDB support. To check which operations TiDB supports for your table's partition type, see [Partition management](/partitioned-table.md#partition-management).

If DM reports a parsing error for an `ALTER TABLE` statement that uses `ADD PARTITION` or `DROP PARTITION` and you do not need to replicate the partition change to TiDB, you can use the following rule to skip the statement. A parsing error in DM does not necessarily mean that TiDB does not support the operation.

When DM cannot parse a statement, it cannot apply filters that target a specific schema or table. In this case, you need a global filtering rule with `schema-pattern: "*"` and no `table-pattern`. This rule applies to matching statements for all tables in the migration task.

> **Warning:**
>
> To avoid filtering out data that needs to be migrated, configure the global filtering rule as strictly as possible.
>
> The following patterns match SQL text, including string literals, and might unintentionally filter out other DDL statements. For example, an `ALTER TABLE ... ADD COLUMN` statement containing `ADD PARTITION` in a default value might also be skipped. Before using this rule, make sure the patterns do not match any DDL statements you need to replicate.

```
filters:
  filter-partition-rule:
    schema-pattern: "*"
    sql-pattern: ["ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

## See also

[Filter Binlog Events Using SQL Expressions](/filter-dml-event.md)
