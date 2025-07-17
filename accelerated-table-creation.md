---
title: TiDB Accelerated Table Creation
summary: 了解 TiDB 中创建表的性能优化的概念、原理和实现细节。
---

# TiDB Accelerated Table Creation

TiDB v7.6.0 引入了系统变量 [`tidb_ddl_version`](https://docs.pingcap.com/tidb/v7.6/system-variables#tidb_enable_fast_create_table-new-in-v800) 以支持加速创建表，从而提升批量创建表的效率。从 v8.0.0 版本开始，该系统变量被重命名为 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800)。

当通过 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) 启用加速创建表后，在同一时间提交到同一 TiDB 节点的具有相同 schema 的创建表语句会被合并为批量创建表语句，以提高创建表的性能。因此，为了提升创建表的性能，建议连接到同一 TiDB 节点，且同时并发创建具有相同 schema 的表，并适当增加并发度。

合并的批量创建表语句在同一事务中执行，因此如果其中一条语句失败，所有语句都将失败。

## 与 TiDB 工具的兼容性

- 在 TiDB v8.3.0 之前，[TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview) 不支持复制由 `tidb_enable_fast_create_table` 创建的表。从 v8.3.0 版本开始，TiCDC 可以正确复制这些表。

## 限制

你现在只能在 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句中使用性能优化进行表创建，并且该语句不得包含任何外键约束。

## 使用 `tidb_enable_fast_create_table` 加速表创建

你可以通过设置系统变量 [`tidb_enable_fast_create_table`](/system-variables.md#tidb_enable_fast_create_table-new-in-v800) 的值，来启用或禁用表创建的性能优化。

从 TiDB v8.5.0 版本开始，新创建的集群默认启用加速表创建功能，`tidb_enable_fast_create_table` 设置为 `ON`。对于从 v8.4.0 或更早版本升级的集群，`tidb_enable_fast_create_table` 的默认值保持不变。

要启用表创建的性能优化，将该变量的值设置为 `ON`：

```sql
SET GLOBAL tidb_enable_fast_create_table = ON;
```

要禁用表创建的性能优化，将该变量的值设置为 `OFF`：

```sql
SET GLOBAL tidb_enable_fast_create_table = OFF;
```