---
title: REFRESH STATS
summary: Learn how to reload statistics into memory for specific tables or the whole TiDB cluster.
---

# REFRESH STATS

`REFRESH STATS` reloads persisted optimizer statistics from the TiDB system tables into memory. This statement is primarily intended for scenarios where statistics have been restored externally (for example, by BR) or when you need to reconcile in-memory statistics without rerunning `ANALYZE`.

When you run `REFRESH STATS`, TiDB reuses the statistics initialization routines that are automatically triggered at startup. You can reload statistics for individual tables, every table in selected databases, or the entire cluster, and optionally choose whether to perform lightweight (`LITE`) or full (`FULL`) initialization.

> **Warning:**
>
> This statement is built for BR's internal restore workflow and BR runs it automatically when needed. Do not execute it manually unless you are debugging in-memory statistics, and never run it on production clusters as part of routine operations. Additionally, do not run this statement concurrently for the same tables, as it may lead to unexpected behavior.

## Synopsis

```ebnf+diagram
RefreshStatsStmt ::=
    'REFRESH' 'STATS' RefreshTargetList RefreshMode? ClusterOption?

RefreshTargetList ::=
    RefreshTarget (',' RefreshTarget)*

RefreshTarget ::=
    TableName
  | SchemaWildcard
  | GlobalWildcard

TableName ::=
    Identifier ('.' Identifier)?

SchemaWildcard ::=
    Identifier '.' '*'

GlobalWildcard ::=
    '*' '.' '*'

RefreshMode ::=
    'FULL'
  | 'LITE'

ClusterOption ::=
    'CLUSTER'
```

## Options

- **Targets (`RefreshTargetList`)**
    - `table_name` refreshes a table in the current database.
    - `db_name.table_name` refreshes a fully qualified table.
    - `db_name.*` refreshes every table in the specified database.
    - `*.*` refreshes every table in the cluster.
- **`FULL`** Forces TiDB to load full statistics (histograms, TopN, CMSketches) into memory, equivalent to setting [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710) to `false` for this operation. Use this when you need complete statistics immediately after the refresh.
- **`LITE`** Uses lightweight initialization, equivalent to `lite-init-stats = true`, which skips loading histograms and other heavy structures until they are needed.
- **`CLUSTER`** Broadcasts the refresh request to every TiDB server. Without this keyword, only the TiDB node that receives the statement reloads its in-memory statistics.
- **Default mode** If neither `FULL` nor `LITE` is specified, TiDB uses the current value of [`lite-init-stats`](/tidb-configuration-file.md#lite-init-stats-new-in-v710).

## Examples

- Refresh statistics for a single table on the connected TiDB node:

  ```sql
  REFRESH STATS orders;
  ```

- Refresh all tables in `sales` with lightweight initialization:

  ```sql
  REFRESH STATS sales.* LITE;
  ```

- Force every TiDB node to load full statistics for the entire cluster:

  ```sql
  REFRESH STATS *.* FULL CLUSTER;
  ```

## Privileges

To execute `REFRESH STATS`, you must either have the `RESTORE_ADMIN` privilege or hold `SELECT` on every targeted table. If you do not have sufficient privileges, TiDB returns an error and aborts the statement.

## MySQL compatibility

`REFRESH STATS` is a TiDB-specific extension and is not part of MySQL.

## See also

- [Statistics](/statistics.md)
- [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)
- [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md)
