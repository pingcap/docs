---
title: Changefeed Log Filters
summary: Learn how to use the table filter and event filter of TiCDC.
---

# Changefeed Log Filters

TiCDC supports filtering data by tables and events. This document introduces how to use the two types of filters.

## Table filter

Table filter is a feature that allows you to keep or filter out specific databases and tables by specifying the following configurations:

```toml
[filter]
# Filter rules
rules = ['*.*', '!test.*']
```

Common filter rules:

- `rules = ['*.*']`
    - Replicate all tables (not including system tables)
- `rules = ['test1.*']`
    - Replicate all tables in the `test1` database
- `rules = ['*.*', '!scm1.tbl2']`
    - Replicate all tables except for the `scm1.tbl2` table
- `rules = ['scm1.tbl2', 'scm1.tbl3']`
    - Only replicate tables `scm1.tbl2` and `scm1.tbl3`
- `rules = ['scm1.tidb_*']`
    - Replicate all tables in the `scm1` database whose names start with `tidb_`

For more information, see [Table filter syntax](/table-filter.md#syntax).

## Event filter rules

Starting in v6.2.0, TiCDC supports event filter. You can configure event filter rules to filter out the DML and DDL events that meet the specified conditions.

The following is an example of event filter rules:

```toml
[filter]
# The event filter rules must be under the `[filter]` configuration. You can configure multiple event filters at the same time.

[[filter.event-filters]]
matcher = ["test.worker"] # matcher is an allow list, which means this rule only applies to the worker table in the test database.
ignore-event = ["insert"] # Ignore insert events.
ignore-sql = ["^drop", "add column"] # Ignore DDLs that start with "drop" or contain "add column".
ignore-delete-value-expr = "name = 'john'" # Ignore delete DMLs that contain the condition "name = 'john'".
ignore-insert-value-expr = "id >= 100" # Ignore insert DMLs that contain the condition "id >= 100".
ignore-update-old-value-expr = "age < 18 or name = 'lili'" # Ignore update DMLs whose old value contains "age < 18" or "name = 'lili'".
ignore-update-new-value-expr = "gender = 'male' and age > 18" # Ignore update DMLs whose new value contains "gender = 'male'" and "age > 18".
```

Description of configuration parameters:

- `matcher`: the database and table that this event filter rule applies to. The syntax is the same as [table filter](/table-filter.md).

    > **Note:**
    >
    > `matcher` matches the database name, so you need to pay extra attention when configuring it. For example, when the `event-filters` configuration is as follows:
    >
    > ```toml
    > [filter]
    > [[filter.event-filters]]
    > matcher = ["test.t1"]
    > ignore-sql = ["^drop"]
    > ```
    >
    > `ignore-sql = ["^drop"]` not only filters out `DROP TABLE test.t1` but also filters out `DROP DATABASE test`, because `matcher` contains the database name `test`.
    >
    > If you only want to filter out the specified table instead of the entire database, modify the `ignore-sql` value to `["drop table"]`.

- `ignore-event`: the event type to be ignored. This parameter accepts an array of strings. You can configure multiple event types. Currently, the following event types are supported:

    | Event           | Type | Alias | Description         |
    | --------------- | ---- | -|--------------------------|
    | all dml         |      | |Matches all DML events       |
    | all ddl         |      | |Matches all DDL events         |
    | insert          | DML  | |Matches `insert` DML event      |
    | update          | DML  | |Matches `update` DML event      |
    | delete          | DML  | |Matches `delete` DML event      |
    | create schema   | DDL  | create database |Matches `create database` event |
    | drop schema     | DDL  | drop database  |Matches `drop database` event |
    | create table    | DDL  | |Matches `create table` event    |
    | drop table      | DDL  | |Matches `drop table` event      |
    | rename table    | DDL  | |Matches `rename table` event    |
    | truncate table  | DDL  | |Matches `truncate table` event  |
    | alter table     | DDL  | |Matches `alter table` event, including all clauses of `alter table`, `create index` and `drop index`   |
    | add table partition    | DDL  | |Matches `add table partition` event     |
    | drop table partition    | DDL  | |Matches `drop table partition` event     |
    | truncate table partition    | DDL  | |Matches `truncate table partition` event     |
    | create view     | DDL  | |Matches `create view`event     |
    | drop view     | DDL  | |Matches `drop view` event     |
    | modify schema charset and collate | DDL  | |Matches `modify schema charset and collate` event     |
    | recover table   | DDL  | |Matches `recover table` event    |
    | rebase auto id    | DDL  | |Matches `rebase auto id` event    |
    | modify table comment | DDL  | |Matches `modify table comment` event    |
    | modify table charset and collate | DDL  | |Matches `modify table charset and collate` event    |
    | exchange table partition | DDL  | |Matches `exchange table partition` event    |
    | reorganize table partition | DDL  | |Matches `reorganize table partition` event    |
    | alter table partitioning | DDL  | |Matches `alter table partitioning` event    |
    | remove table partitioning | DDL  | |Matches `remove table partitioning` event    |
    | add column | DDL  | |Matches `add column` event    |
    | drop column | DDL  | |Matches `drop column` event    |
    | modify column | DDL  | |Matches `modify column` event    |
    | set default value | DDL  | |Matches `set default value` event    |
    | add primary key | DDL  | |Matches `add primary key` event    |
    | drop primary key | DDL  | |Matches `drop primary key` event    |
    | rename index | DDL  | |Matches `rename index` event    |
    | alter index visibility | DDL  | |Matches `alter index visibility` event    |
    | alter ttl info | DDL  | |Matches `alter ttl info` event    |
    | alter ttl remove| DDL  | |Matches DDL events that remove all TTL attributes of a table |
    | multi schema change | DDL  | |Matches DDL events that change multiple attributes of a table within the same DDL statement |

    > **Note:**
    >
    > TiDB's DDL statements support changing multiple attributes of a single table at the same time, such as `ALTER TABLE t MODIFY COLUMN a INT, ADD COLUMN b INT, DROP COLUMN c;`. This operation is defined as MultiSchemaChange. If you want to filter out this type of DDL, you need to configure `"multi schema change"` in `ignore-event`.

- `ignore-sql`: the regular expressions of the DDL statements to be filtered out. This parameter accepts an array of strings, in which you can configure multiple regular expressions. This configuration only applies to DDL events.
- `ignore-delete-value-expr`: this parameter accepts a SQL expression that follows the default SQL mode, used to filter out the `DELETE` type of DML events with a specified value.
- `ignore-insert-value-expr`: this parameter accepts a SQL expression that follows the default SQL mode, used to filter out the `INSERT` type of DML events with a specified value.
- `ignore-update-old-value-expr`: this parameter accepts a SQL expression that follows the default SQL mode, used to filter out the `UPDATE` type of DML events with a specified old value.
- `ignore-update-new-value-expr`: this parameter accepts a SQL expression that follows the default SQL mode, used to filter out the `UPDATE` DML events with a specified new value.

> **Note:**
>
> - When TiDB updates a value in the column of the clustered index, TiDB splits an `UPDATE` event into a `DELETE` event and an `INSERT` event. TiCDC does not identify such events as an `UPDATE` event and thus cannot correctly filter out such events.
> - When you configure a SQL expression, make sure all tables that matches `matcher` contain all the columns specified in the SQL expression. Otherwise, the replication task cannot be created. In addition, if the table schema changes during the replication, which results in a table no longer containing a required column, the replication task fails and cannot be resumed automatically. In such a situation, you must manually modify the configuration and resume the task.
