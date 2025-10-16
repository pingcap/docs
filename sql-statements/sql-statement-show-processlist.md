---
title: SHOW [FULL] PROCESSLIST | TiDB SQL Statement Reference
summary: TiDB 数据库中 SHOW [FULL] PROCESSLIST 的用法概述。
---

# SHOW [FULL] PROCESSLIST

该语句用于列出当前连接到同一 TiDB 服务器的会话。`Info` 列包含查询文本，如果未指定可选关键字 `FULL`，则该文本会被截断。若要查看整个集群范围内的进程列表，请使用 [`INFORMATION_SCHEMA.CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md#cluster_processlist) 表。

## 语法

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

## 权限

如果当前用户没有 `PROCESS` 权限，`SHOW PROCESSLIST` 只会显示该用户自己会话的请求。

## MySQL 兼容性

* TiDB 中的 `State` 列不具备描述性。在 TiDB 中将状态表示为单一值更加复杂，因为查询是并行执行的，每个 goroutine 在任意时刻都可能处于不同的状态。

## 另请参阅

* [KILL \[TIDB\]](/sql-statements/sql-statement-kill.md)
* [`INFORMATION_SCHEMA.PROCESSLIST`](/information-schema/information-schema-processlist.md)
