---
title: SHOW [FULL] PROCESSLIST | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 SHOW [FULL] PROCESSLIST 的概述。
---

# SHOW [FULL] PROCESSLIST

该语句列出当前连接到同一 TiDB 服务器的会话。`Info` 列包含查询文本，除非指定可选关键字 `FULL`，否则会被截断。

## 概述

```ebnf+diagram
ShowProcesslistStmt ::=
    "SHOW" "FULL"? "PROCESSLIST"
```

## 示例

```sql
mysql> SHOW PROCESSLIST;
+------+------+-----------------+------+---------+------+------------+------------------+
| Id   | User | Host            | db   | Command | Time | State      | Info             |
+------+------+-----------------+------+---------+------+------------+------------------+
|    5 | root | 127.0.0.1:45970 | test | Query   |    0 | autocommit | SHOW PROCESSLIST |
+------+------+-----------------+------+---------+------+------------+------------------+
1 rows in set (0.00 sec)
```

## MySQL 兼容性

* TiDB 中的 `State` 列不具有描述性。在 TiDB 中用单一值表示状态更为复杂，因为查询是并行执行的，每个 goroutine 在任何时间点可能具有不同的状态。

## 相关链接

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
* [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)