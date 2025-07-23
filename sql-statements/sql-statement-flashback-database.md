---
title: FLASHBACK DATABASE
summary: 了解 TiDB 数据库中 FLASHBACK DATABASE 的用法。
---

# FLASHBACK DATABASE

TiDB v6.4.0 引入了 `FLASHBACK DATABASE` 语法。你可以使用 `FLASHBACK DATABASE` 来还原被 `DROP` 语句删除的数据库及其数据，前提是在垃圾回收（GC）生命周期内。

你可以通过配置 [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) 系统变量，设置历史数据的保留时间。默认值为 `10m0s`。你可以使用以下 SQL 语句查询当前的 `safePoint`，即 GC 已经执行到的时间点：

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

只要在 `tikv_gc_safe_point` 时间之后删除的数据库，你都可以使用 `FLASHBACK DATABASE` 来还原。

## 语法

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### 语法结构

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName
FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注意事项

* 如果数据库在 `tikv_gc_safe_point` 时间之前被删除，你将无法使用 `FLASHBACK DATABASE` 语句还原数据。`FLASHBACK DATABASE` 语句会返回类似于 `ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST` 的错误。

* 你不能多次使用 `FLASHBACK DATABASE` 语句还原同一个数据库。因为通过 `FLASHBACK DATABASE` 还原的数据库具有与原数据库相同的 schema ID，重复还原会导致 schema ID 重复。在 TiDB 中，数据库 schema ID 必须是全局唯一的。

## 示例

- 还原被 `DROP` 删除的 `test` 数据库：

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test;
    ```

- 还原被 `DROP` 删除的 `test` 数据库，并将其重命名为 `test1`：

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test TO test1;
    ```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。