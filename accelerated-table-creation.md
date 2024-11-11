---
title: TiDB Accelerated Table Creation
summary: Learn the concept, principles, and implementation details of performance optimization for creating tables in TiDB.
aliases: ['/tidb/dev/ddl-v2/']
---

# TiDB Accelerated Table Creation

TiDB v7.6.0 introduces the system variable [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800) to support accelerating table creation, which improves the efficiency of bulk table creation. Starting from v8.0.0, this system variable is renamed to [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

When accelerated table creation is enabled via [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800), table creation statements with the same schema committed to the same TiDB node at the same time are merged into batch table creation statements to improve table creation performance. Therefore, to improve the table creation performance, try to connect to the same TiDB node, create tables with the same schema concurrently, and increase the concurrency appropriately.

The merged batch table creation statements are executed within the same transaction, so if one statement of them fails, all of them will fail.

## Compatibility with TiDB tools

- Before TiDB v8.3.0, [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) does not support replicating the tables that are created by `tidb_enable_fast_create_table`. After TiDB v8.3.0, TiCDC can handle it.

## Limitation

You can now use performance optimization for table creation only in the [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) statement, and this statement must not include any foreign key constraints.

## Use `tidb_enable_fast_create_table` to accelerate table creation

You can enable or disable performance optimization for creating tables by specifying the value of the system variable [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800).

Since TiDB v8.5.0, `tidb_enable_fast_create_table` is enabled by default for new clusters. If the cluster is upgraded from below version, the variable value remain unchanged.

To enable performance optimization for creating tables, set the value of this variable to `ON`:

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

To disable performance optimization for creating tables, set the value of this variable to `OFF`:

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```
