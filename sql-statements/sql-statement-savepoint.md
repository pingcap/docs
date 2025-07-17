---
title: SAVEPOINT | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SAVEPOINT 的概述。
---

# SAVEPOINT

`SAVEPOINT` 是在 TiDB v6.2.0 中引入的功能。其语法如下：

```sql
SAVEPOINT identifier
ROLLBACK TO [SAVEPOINT] identifier
RELEASE SAVEPOINT identifier
```

> **Warning:**
>
> 当 [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) 被禁用时，你不能在悲观事务中使用 `SAVEPOINT`。

- `SAVEPOINT` 用于在当前事务中设置一个指定名称的保存点。如果同名的保存点已存在，则会被删除，并重新设置一个同名的新保存点。

- `ROLLBACK TO SAVEPOINT` 会将事务回滚到指定名称的保存点，并不会终止事务。在回滚过程中，保存点之后对表数据的更改将被还原，且所有在该保存点之后设置的保存点都会被删除。在悲观事务中，事务持有的锁不会被回滚，而是在事务结束时释放。

    如果 `ROLLBACK TO SAVEPOINT` 语句中指定的保存点不存在，将返回以下错误：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

- `RELEASE SAVEPOINT` 语句会删除指定名称的保存点以及该保存点之后的所有保存点，但不会提交或回滚当前事务。如果指定名称的保存点不存在，将返回以下错误：

    ```
    ERROR 1305 (42000): SAVEPOINT identifier does not exist
    ```

    在事务提交或回滚后，所有在该事务中的保存点都将被删除。

## 概要

```ebnf+diagram
SavepointStmt ::=
    "SAVEPOINT" Identifier

RollbackToStmt ::=
    "ROLLBACK" "TO" "SAVEPOINT"? Identifier

ReleaseSavepointStmt ::=
    "RELEASE" "SAVEPOINT" Identifier
```

## 示例

创建表 `t1`：

```sql
CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

开始当前事务：

```sql
BEGIN;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

向表中插入数据并设置保存点 `sp1`：

```sql
INSERT INTO t1 VALUES (1);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

再次向表中插入数据并设置保存点 `sp2`：

```sql
INSERT INTO t1 VALUES (2);
```

```sql
Query OK, 1 row affected (0.00 sec)
```

```sql
SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

释放保存点 `sp2`：

```sql
RELEASE SAVEPOINT sp2;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

回滚到保存点 `sp1`：

```sql
ROLLBACK TO SAVEPOINT sp1;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

提交事务并查询表，只会返回在 `sp1` 之前插入的数据。

```sql
COMMIT;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
SELECT * FROM t1;
```

```sql
+---+
| a |
+---+
| 1 |
+---+
1 row in set
```

## MySQL 兼容性

当使用 `ROLLBACK TO SAVEPOINT` 将事务回滚到指定的保存点时，MySQL 只会在回滚到该保存点后释放持有的锁，而在 TiDB 的悲观事务中，TiDB 不会立即释放在指定保存点之后持有的锁。相反，TiDB 会在事务提交或回滚时释放所有锁。

TiDB 不支持 MySQL 语法 `ROLLBACK WORK TO SAVEPOINT ...`。

## 相关链接

* [COMMIT](/sql-statements/sql-statement-commit.md)
* [ROLLBACK](/sql-statements/sql-statement-rollback.md)
* [START TRANSACTION](/sql-statements/sql-statement-start-transaction.md)
* [TiDB 乐观事务模式](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)
