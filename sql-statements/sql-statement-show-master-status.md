---
title: SHOW MASTER STATUS
summary: 关于在 TiDB 数据库中使用 SHOW MASTER STATUS 的概述。
---

# SHOW MASTER STATUS

`SHOW MASTER STATUS` 语句显示集群中的最新 TSO。

## 示例

```sql
SHOW MASTER STATUS;
```

```sql
+-------------+--------------------+--------------+------------------+-------------------+
| File        | Position           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------+--------------------+--------------+------------------+-------------------+
| tidb-binlog | 416916363252072450 |              |                  |                   |
+-------------+--------------------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

`SHOW MASTER STATUS` 的输出旨在与 MySQL 保持一致。然而，执行结果不同，MySQL 的结果是 binlog 位置相关信息，而 TiDB 的结果是最新的 TSO 信息。

在 TiDB 中，`SHOW BINARY LOG STATUS` 语句作为 `SHOW MASTER STATUS` 的别名被添加，已在 MySQL 8.2.0 及更新版本中被废弃。