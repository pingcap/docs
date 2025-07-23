---
title: FLASHBACK TABLE
summary: 学习如何使用 `FLASHBACK TABLE` 语句恢复表。
---

# FLASHBACK TABLE

`FLASHBACK TABLE` 语法自 TiDB 4.0 版本引入。你可以使用 `FLASHBACK TABLE` 语句在垃圾回收（GC）生命周期内恢复被 `DROP` 或 `TRUNCATE` 操作删除的表及其数据。

系统变量 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)（默认值：`10m0s`）定义了行的早期版本的保留时间。可以通过以下查询获取当前已执行垃圾回收的 `safePoint`：

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

只要在 `tikv_gc_safe_point` 时间之后通过 `DROP` 或 `TRUNCATE` 语句删除的表，你都可以使用 `FLASHBACK TABLE` 语句进行恢复。

## 语法

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## 概要

```ebnf+diagram
FlashbackTableStmt ::=
    'FLASHBACK' 'TABLE' TableName FlashbackToNewName

TableName ::=
    Identifier ( '.' Identifier )?

FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注意事项

如果一个表被删除且已超过 GC 生命周期，你将无法再使用 `FLASHBACK TABLE` 语句恢复被删除的数据。否则，会返回类似 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST` 的错误。

## 示例

- 恢复被 `DROP` 操作删除的表数据：

    
    ```sql
    DROP TABLE t;
    ```

    
    ```sql
    FLASHBACK TABLE t;
    ```

- 恢复被 `TRUNCATE` 操作删除的表数据。由于截断的表 `t` 仍然存在，你需要将表 `t` 重命名为要恢复的表，否则会因为表 `t` 已存在而返回错误。

    
    ```sql
    TRUNCATE TABLE t;
    ```

    
    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 实现原理

在删除表时，TiDB 只会删除表的元数据，并将待删除的表数据（行数据和索引数据）写入 `mysql.gc_delete_range` 表。TiDB 后台的 GC Worker 会定期从 `mysql.gc_delete_range` 表中删除超出 GC 生命周期的键。

因此，要恢复一张表，只需恢复表的元数据，并在 GC Worker 删除表数据之前删除 `mysql.gc_delete_range` 表中的对应行记录。你可以使用 TiDB 的快照读来恢复表的元数据。关于快照读的详细内容，参考 [Read Historical Data](/read-historical-data.md)。

以下是 `FLASHBACK TABLE t TO t1` 的工作流程：

1. TiDB 搜索最近的 DDL 历史任务，定位到在表 `t` 上的第一个 `DROP TABLE` 或 `truncate table` 类型的 DDL 操作。如果未能找到，返回错误。
2. TiDB 检查该 DDL 任务的起始时间是否早于 `tikv_gc_safe_point`。如果早于，意味着被 `DROP` 或 `TRUNCATE` 操作删除的表已被 GC 清理，返回错误。
3. TiDB 以该 DDL 任务的起始时间作为快照，读取历史数据并获取表的元数据。
4. TiDB 删除 `mysql.gc_delete_range` 中与表 `t` 相关的 GC 任务。
5. TiDB 将表的 `name` 元数据改为 `t1`，并用此元数据创建一个新表。注意，只是表名被更改，表 ID 不变。该表 ID 与之前删除的表 `t` 相同。

从上述流程可以看出，TiDB 始终操作表的元数据，用户数据从未被修改。恢复后的表 `t1` 拥有与之前删除的表 `t` 相同的 ID，因此 `t1` 可以读取 `t` 的用户数据。

> **Note:**
>
> 你不能多次使用 `FLASHBACK` 语句恢复同一已删除的表，因为恢复的表的 ID 与被删除的表相同，而 TiDB 要求所有现存的表都必须具有全局唯一的表 ID。

`FLASHBACK TABLE` 操作通过 TiDB 获取表的元数据（采用快照读），然后执行类似 `CREATE TABLE` 的表创建流程。因此，`FLASHBACK TABLE` 本质上是一种 DDL 操作。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。