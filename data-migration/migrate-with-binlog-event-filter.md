---
title: Migrate with Binlog Event Filter
summary: Learn how to filter binlog events when migrating data
---

# Filter Binlog Events

This document describes how to filter binlog events when you use DM to perform continuous incremental data replication. For the detailed replication instruction, refer to the following documents:

- [Migrate MySQL data of less than 1 TB to TiDB](/data-migration/migrate-mysql-tidb-less-tb.md)
- [Migrate MySQL data of more than 1 TB to TiDB](/data-migration/migrate-mysql-tidb-above-tb.md)
- [Merge and migrate MySQL shards of less than 1 TB to TiDB](/data-migration/migrate-shared-mysql-tidb-less-tb.md)
- [Merge and migrate MySQL shards of more than 1 TB to TiDB](/data-migration/migrate-shared-mysql-tidb-above-tb.md)

## Configuration

To use binlog event filter, add a `filter` when configuring the YAML file of DM, as shown below:

```yaml
filters:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    events: ["truncate table", "drop table"]
    sql-pattern: ["^DROP\\s+PROCEDURE", "^CREATE\\s+PROCEDURE"]
    action: Ignore
```

- `schema-pattern`/`table-pattern`: Filter matching schemas or tables
- `events`: Filter binlog events. Supported events are listed in the table below:

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

- `sql-pattern`：Filter specified DDL SQL statements. The matching rule supports using a regular expression.
- `action`: `Do` or `Ignore`

    - `Do`: the allow list. A binlog event is filtered if meeting either of the following two conditions:

        - The event is not in the event list of the rule.
        - sql-pattern has been specified but the SQL statement of the event does not match sql-pattern.

    - `Ignore`: the block list. A binlog event is filtered out if meeting either of the following two conditions:

        - The event is in the event list of the rule.
        - sql-pattern has been specified and the SQL statement of the event matches sql-pattern.

## Application scenarios

This section describes the application scenarios of binlog event filter.

### Drop all sharding deletion operations

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

### Migrate sharding DML statements only

To filter only DML statements, configure two `Binlog event filter rule`, as shown below:

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

### Drop SQL statements not supported by TiDB

To filter out SQL statements not supported by TiDB, configure a `filter-procedure-rule`, as shown below:

```
filters:
  filter-procedure-rule:
    schema-pattern: "*"
    sql-pattern: [".*\\s+DROP\\s+PROCEDURE", ".*\\s+CREATE\\s+PROCEDURE", "ALTER\\s+TABLE[\\s\\S]*ADD\\s+PARTITION", "ALTER\\s+TABLE[\\s\\S]*DROP\\s+PARTITION"]
    action: Ignore
```

> **Warning:**
>
> To avoid filtering out data that needs to be migrated, configure the global filtering rule as strictly as possible.

## See also

[Filter Binlog Events Using SQL Expressions](/data-migration/migrate-with-binlog-sql-expression-filter.md)