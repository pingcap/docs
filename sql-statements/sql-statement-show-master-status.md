---
title: SHOW MASTER STATUS
summary: An overview of the usage of SHOW MASTER STATUS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-master-status/']
---

# SHOW MASTER STATUS

The `SHOW MASTER STATUS` statement displays the latest TSO in the cluster.

## Examples

{{< copyable "sql" >}}

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

## MySQL compatibility

The output of `SHOW MASTER STATUS` is designed to match MySQL. However, the execution results are different in that the MySQL result is the binlog location information and the TiDB result is the latest TSO information.

The `SHOW BINARY LOG STATUS` statement was added in TiDB as an alias for `SHOW MASTER STATUS`, which has been deprecated in MySQL 8.2.0 and newer versions.
