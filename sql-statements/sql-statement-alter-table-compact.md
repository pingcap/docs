---
title: ALTER TABLE ... COMPACT
summary: 关于 TiDB 数据库中使用 ALTER TABLE ... COMPACT 的概述。
---

# ALTER TABLE ... COMPACT

为了提升读取性能并减少磁盘空间使用，TiDB 会在后台自动调度存储节点进行数据压缩。在压缩过程中，存储节点会重写物理数据，包括清理已删除的行和合并由更新引起的多个版本的数据。`ALTER TABLE ... COMPACT` 语句允许你立即对指定的表启动压缩，而无需等待后台触发的压缩操作。

执行该语句不会阻塞现有的 SQL 语句，也不会影响任何 TiDB 功能，例如事务、DDL 和 GC。通过 SQL 语句可以选择的数据也不会被改变。执行此操作会消耗一定的 IO 和 CPU 资源。请注意选择合适的时机执行，例如资源充足时，以避免对业务造成负面影响。

当一张表的所有副本都完成压缩后，该压缩操作会被视为完成并返回。在执行过程中，你可以安全地通过执行 [`KILL`](/sql-statements/sql-statement-kill.md) 语句中断压缩。中断压缩不会破坏数据一致性，也不会导致数据丢失，也不会影响后续的手动或后台压缩操作。

目前，该数据压缩语句仅支持 TiFlash 副本，不支持 TiKV 副本。

## 语法简介

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

自 v6.2.0 版本起，可以省略 `TIFLASH REPLICA` 部分。当省略时，语句的语义保持不变，只对 TiFlash 生效。

## 示例

### 压缩表中的 TiFlash 副本

以下以 `employees` 表为例，该表有 4 个分区，且每个分区有 2 个 TiFlash 副本：

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

你可以执行以下语句，立即对 `employees` 表中所有分区的 2 个 TiFlash 副本进行压缩：

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

### 压缩表中指定分区的 TiFlash 副本

以下以 `employees` 表为例，该表有 4 个分区，且每个分区有 2 个 TiFlash 副本：

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

你可以执行以下语句，立即对 `employees` 表中 `pNorth` 和 `pEast` 分区的 2 个 TiFlash 副本进行压缩：

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## 并发性

`ALTER TABLE ... COMPACT` 语句会同时压缩一张表的所有副本。

为了避免对线上业务造成较大影响，每个 TiFlash 实例默认一次只压缩一个表的数据（除了后台触发的压缩操作）。这意味着，如果你同时对多个表执行 `ALTER TABLE ... COMPACT`，它们的执行会排队在同一台 TiFlash 实例上，而不是同时进行。

<CustomContent platform="tidb">

如果希望获得更高的表级并发度和更高的资源使用，可以修改 TiFlash 的配置 [`manual_compact_pool_size`](/tiflash/tiflash-configuration.md)。例如，将 `manual_compact_pool_size` 设置为 2 时，可以同时处理 2 个表的压缩。

</CustomContent>

## 观察数据压缩进度

你可以通过检查 `INFORMATION_SCHEMA.TIFLASH_TABLES` 表中的 `TOTAL_DELTA_ROWS` 列，观察数据压缩的进度或判断是否需要对表进行压缩。`TOTAL_DELTA_ROWS` 的值越大，表示可以压缩的数据越多。如果 `TOTAL_DELTA_ROWS` 为 `0`，说明表中的所有数据都处于最佳状态，无需压缩。

<details>
  <summary>示例：检查非分区表的压缩状态</summary>

```sql
USE test;

CREATE TABLE foo(id INT);

ALTER TABLE foo SET TIFLASH REPLICA 1;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 0 |
+------------------+-------------------+

INSERT INTO foo VALUES (1), (3), (7);

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                3 |                 0 |
+------------------+-------------------+
-- 新写入的数据可以被压缩

ALTER TABLE foo COMPACT TIFLASH REPLICA;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 3 |
+------------------+-------------------+
-- 所有数据都处于最佳状态，无需压缩
```

</details>

<details>
  <summary>示例：检查分区表的压缩状态</summary>

```sql
USE test;

CREATE TABLE employees
    (id INT NOT NULL, store_id INT)
    PARTITION BY LIST (store_id) (
        PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
        PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
        PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
        PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
    );

ALTER TABLE employees SET TIFLASH REPLICA 1;

INSERT INTO employees VALUES (1, 1), (6, 6), (10, 10);

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                1 |                 0 |
| pEast          |                2 |                 0 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- 部分分区可以被压缩

ALTER TABLE employees COMPACT TIFLASH REPLICA;

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                0 |                 1 |
| pEast          |                0 |                 2 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- 所有分区中的数据都处于最佳状态，无需压缩
```

</details>

> **注意：**
>
> - 如果在压缩过程中数据被更新，`TOTAL_DELTA_ROWS` 可能在压缩完成后仍为非零值。这是正常现象，表示这些更新尚未被压缩。若要压缩这些更新，可以再次执行 `ALTER TABLE ... COMPACT` 语句。
>
> - `TOTAL_DELTA_ROWS` 表示数据版本，而非行数。例如，插入一行后又删除该行，`TOTAL_DELTA_ROWS` 会增加 2。

## 兼容性

### MySQL 兼容性

`ALTER TABLE ... COMPACT` 语法是 TiDB 特有的，是对标准 SQL 语法的扩展。虽然没有对应的 MySQL 语法，但你仍可以通过使用支持 MySQL 协议的客户端或各种数据库驱动程序执行此语句。

### TiCDC 兼容性

`ALTER TABLE ... COMPACT` 语句不会引起逻辑数据变更，因此不会被 TiCDC 复制到下游。

## 相关链接

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL TIDB](/sql-statements/sql-statement-kill.md)