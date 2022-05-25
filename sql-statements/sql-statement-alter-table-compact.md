---
title: ALTER TABLE ... COMPACT
summary: An overview of the usage of ALTER TABLE ... COMPACT for the TiDB database.
---

# ALTER TABLE ... COMPACT

> **Warning:**
>
> This statement is still an experimental feature. It is NOT recommended that you use it in the production environment.

After a write occurs, TiDB automatically performs data compaction at the backend. Specifically, TiDB rewrites the physical data in a table, including cleaning up deleted data and merging multiple versions of data. After data compaction, you can get higher access performance with less disk usage. The `ALTER TABLE ... COMPACT` statement allows you to compact data of specific tables immediately without waiting for the backend to trigger a compaction.

The execution of this statement does not block the existing SQL statements, affect such TiDB functions as transactions, DDL, and GC, or change data obtained by executing SQL statements. However, executing this statement may take up some IO and CPU resources, which might result in business latency.

The execution finishes with execution result returned only when all replicas of a table are compacted. During the execution process, you can safely interrupt the compaction for the current table by executing the [`KILL`](/sql-statements/sql-statement-kill.md) statement. Interrupting a compaction does not break data consistency or lead to data loss, nor does it affect subsequent manual or automatic compactions.

Data compaction is currently supported only for TiFlash, not for TiKV.

## Synopsis

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' 'TIFLASH' 'REPLICA'
```

## Examples

### Compact TiFlash replicas in a table

Assume that an `employees` table has 4 partitions and 2 TiFlash replicas.

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
ALTER TABLE employees SET TIFLASH REPLICA 2;
```

You can execute the following statement to immediately compact data of 2 TiFlash replicas for all partitions in the `employees` table.

{{< copyable "sql" >}}

```sql
ALTER TABLE employee COMPACT TIFLASH REPLICA;
```

## Concurrency

The `ALTER TABLE ... COMPACT` statement compacts data of all replicas in a table at the same time.

To avoid significant impact on online business, each TiFlash instance only processes compaction for one table at a time by default (automatic compaction in the backend is not affected). This means that if you execute the `ALTER TABLE ... COMPACT` statement on multiple tables at the same time, they will be queued for execution on the same TiFlash instance, rather than being executed simultaneously.

You can change the TiFlash configuration file parameter [`manual_compact_pool_size`](/tiflash/tiflash-configuration.md) to obtain greater table-level concurrency with higher resource usage. For example, if `manual_compact_pool_size` is set to 2, you can compact data of 2 tables simultaneously.

## MySQL compatibility

The `ALTER TABLE ... COMPACT` syntax is an extension to the standard SQL syntax introduced by TiDB. Although there is no equivalent MySQL syntax, you can still execute this statement on MySQL clients of versions ranging from 5.7 to 8.0, or on various database drivers that follow the MySQL protocol.

## TiDB Binlog and TiCDC compatibility

The `ALTER TABLE ... COMPACT` statement does not result in logical data changes and are therefore not replicated downstream by TiDB Binlog or TiCDC.

## See also

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL TIDB](/sql-statements/sql-statement-kill.md)