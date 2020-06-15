---
title: SHOW CONFIG
summary: Overview of the use of SHOW CONFIG in the TiDB database
category: reference
---

# SHOW CONFIG

> **Warning:**
>
> This feature is currently an experimental feature and is not recommended for use in a production environment.

The `SHOW CONFIG` statement is used to show the current configuration of various components of TiDB. Please note that the configuration and system variables act on different dimensions. Please do not confuse them. If you want to obtain system variable information, please use [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md) syntax.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## Examples

Show all configurations:

{{< copyable "sql" >}}

```sql
SHOW CONFIG;
```

```
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| Type | Instance       | Name                                            | Value                                                               |
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
| tidb | 127.0.0.1:4000 | alter-primary-key                               | false                                                               |
| tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
| tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
...
120 rows in set (0.01 sec)
```

Show the `type` of the configuration of `tidb`:

{{< copyable "sql" >}}

```sql
SHOW CONFIG WHERE type = 'tidb' AND name = 'advertise-address';
```

```
+------+----------------+-------------------+-----------+
| Type | Instance       | Name              | Value     |
+------+----------------+-------------------+-----------+
| tidb | 127.0.0.1:4000 | advertise-address | 127.0.0.1 |
+------+----------------+-------------------+-----------+
1 row in set (0.05 sec)
```

You can also use the `LIKE` clause to show the `type` of the configuration of `tidb`:

{{< copyable "sql" >}}

```sql
SHOW CONFIG LIKE 'tidb';
```

```
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| Type | Instance       | Name                                            | Value                                                               |
+------+----------------+-------------------------------------------------+---------------------------------------------------------------------+
| tidb | 127.0.0.1:4000 | advertise-address                               | 127.0.0.1                                                           |
| tidb | 127.0.0.1:4000 | alter-primary-key                               | false                                                               |
| tidb | 127.0.0.1:4000 | binlog.binlog-socket                            |                                                                     |
| tidb | 127.0.0.1:4000 | binlog.enable                                   | false                                                               |
...
40 rows in set (0.01 sec)
```

## MySQL compatibility

`SHOW CONFIG` is the extended syntax of TiDB, MySQL has no corresponding syntax.

## See also

* [SHOW VARIABLES](/sql-statements/sql-statement-show-variables.md)
