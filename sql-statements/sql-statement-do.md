---
title: DO | TiDB SQL Statement Reference
summary: An overview of the usage of DO for the TiDB database.
category: reference
aliases: ['/docs/dev/reference/sql/statements/do/']
---

# DO

`DO` executes the expressions but does not return any results. In most cases, `DO` is equivalent to `SELECT expr, ...` that does not return a result.

> **Note:**
>
> `DO` only executes expressions. It cannot be used in all cases where `SELECT` can be used. For example, `DO id FROM t1` is invalid because it references a table. 

In MySQL, a common use case is to execute stored procedure or trigger. Since TiDB does not provide stored procedure or trigger, this function has a limited use.

## Synopsis

**DoStmt:**

![DoStmt](/media/sqlgram/DoStmt.png)

**ExpressionList:**

![ExpressionList](/media/sqlgram/ExpressionList.png)

**Expression:**

![Expression](/media/sqlgram/Expression.png)

## Examples

This SELECT statement pauses, but also produces a result set.

```sql
mysql> SELECT SLEEP(5);
+----------+
| SLEEP(5) |
+----------+
|        0 |
+----------+
1 row in set (5.00 sec)
```

DO, on the other hand, pauses without producing a result set.

```sql
mysql> DO SLEEP(5);
Query OK, 0 rows affected (5.00 sec)

mysql> DO SLEEP(1), SLEEP(1.5);
Query OK, 0 rows affected (2.50 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.

## See also

* [SELECT](/sql-statements/sql-statement-select.md)
