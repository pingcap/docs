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

- `schema-pattern`/`table-pattern`: Filters matching schemas or tables
- `events`: Filters binlog events. Supported events are listed in the table below:

  | Event           | Category | Description                       |
  | --------------- | ---- | --------------------------|
  | all             |      | Includes all events            |
  | all dml         |      | Includes all DML events        |
  | all ddl         |      | Includes all DDL events        |
  | none            |      | Includes no event          |
  | none ddl        |      | Excludes all DDL events      |
  | none dml        |      | Excludes all DML events      |
  | insert          | DML  | Insert DML event      |
  | update          | DML  | Update DML event      |
  | delete          | DML  | Delete DML event      |
  | create database | DDL  | Create database event |
  | drop database   | DDL  | Drop database event   |
  | create table    | DDL  | Create table event    |
  | create index    | DDL  | Create index event    |
  | drop table      | DDL  | Drop table event      |
  | truncate table  | DDL  | Truncate table event  |
  | rename table    | DDL  | Rename table event    |
  | drop index      | DDL  | Drop index event      |
  | alter table     | DDL  | Alter table event     |

- `sql-pattern`: Filters specified DDL SQL statements. The matching rule supports using a regular expression.
- `action`: `Do` or `Ignore`

    - `Do`: the allow list. A binlog event is replicated if meeting either of the following two conditions:

        - The event matches the rule setting.
        - sql-pattern has been specified and the SQL statement of the event matches any of the sql-pattern options.

    - `Ignore`: the block list. A binlog event is filtered out if meeting either of the following two conditions:

        - The event matches the rule setting.
        - sql-pattern has been specified and the SQL statement of the event matches any of the sql-pattern options.

    If both `Do` and `Ignore` are configured, `Ignore` has higher priority over `Do`. That is, an event satisfying both `Ignore` and `Do` conditions will be filtered out.

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
