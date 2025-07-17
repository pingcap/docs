---
title: 使用 FastScan
summary: 介绍在 OLAP 场景中通过使用 FastScan 来加快查询速度的方法。
---

# 使用 FastScan

本文档描述了如何在在线分析处理（OLAP）场景中使用 FastScan 来加快查询速度。

默认情况下，TiFlash 保证查询结果的精度和数据一致性。通过启用 FastScan 功能，TiFlash 提供了更高效的查询性能，但不保证查询结果的准确性和数据一致性。

一些 OLAP 场景允许对查询结果的准确性有一定的容忍度。在这些情况下，如果你需要更高的查询性能，可以在会话或全局层面启用 FastScan 功能。你可以通过配置变量 [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630) 来选择是否启用 FastScan。

## 限制

当启用 FastScan 功能时，你的查询结果可能包含表的旧数据。这意味着你可能会获得具有相同主键的多个历史版本数据，或者已被删除的数据。

例如：

```sql
CREATE TABLE t1 (a INT PRIMARY KEY, b INT);
ALTER TABLE t1 SET TIFLASH REPLICA 1;
INSERT INTO t1 VALUES(1,2);
INSERT INTO t1 VALUES(10,20);
UPDATE t1 SET b = 4 WHERE a = 1;
DELETE FROM t1 WHERE a = 10;
SET SESSION tidb_isolation_read_engines='tiflash';

SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    4 |
+------+------+

SET SESSION tiflash_fastscan=ON;
SELECT * FROM t1;
+------+------+
| a    | b    |
+------+------+
|    1 |    2 |
|    1 |    4 |
|   10 |   20 |
+------+------+
```

虽然 TiFlash 可以在后台自动启动旧数据的压缩，但旧数据不会在物理上立即清理，直到它经过压缩且其数据版本早于 GC 安全点。物理清理完成后，已清理的旧数据将不再在 FastScan 模式下返回。数据压缩的时机由多种因素自动触发，你也可以通过 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) 语句手动触发数据压缩。

## 启用和禁用 FastScan

默认情况下，变量在会话层和全局层面均为 `tiflash_fastscan=OFF`，即未启用 FastScan 功能。你可以使用以下语句查看变量信息。

```
show variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

```
show global variables like 'tiflash_fastscan';

+------------------+-------+
| Variable_name    | Value |
+------------------+-------+
| tiflash_fastscan | OFF   |
+------------------+-------+
```

你可以在会话层和全局层面配置变量 `tiflash_fastscan`。如果需要在当前会话中启用 FastScan，可以使用以下语句：

```
set session tiflash_fastscan=ON;
```

你也可以在全局层面设置 `tiflash_fastscan`。新的设置将在新会话中生效，但不会影响当前和之前的会话。此外，在新会话中，会话层和全局层的 `tiflash_fastscan` 都会采用新值。

```
set global tiflash_fastscan=ON;
```

你可以使用以下语句禁用 FastScan：

```
set session tiflash_fastscan=OFF;
set global tiflash_fastscan=OFF;
```

## FastScan 的机制

TiFlash 存储层中的数据分为两个层次：Delta 层和 Stable 层。

默认情况下，未启用 FastScan，TableScan 操作符处理数据的步骤如下：

1. 读取数据：在 Delta 层和 Stable 层中创建独立的数据流以读取各自的数据。
2. 排序合并：合并步骤 1 中创建的数据流，然后按照（主键列，时间戳列）的顺序返回排序后的数据。
3. 范围过滤：根据数据范围，过滤步骤 2 生成的数据，然后返回过滤后的数据。
4. MVCC + 列过滤：通过 MVCC（即根据主键列和时间戳列过滤数据版本）以及列（即过滤掉不需要的列）对步骤 3 生成的数据进行过滤，然后返回。

FastScan 通过牺牲部分数据一致性来实现更快的查询速度。在 FastScan 中，省略了正常扫描流程中的步骤 2 和步骤 4 中的 MVCC 部分，从而提升查询性能。