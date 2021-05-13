---
title: Set Operations
summary: Learn the supported set operations in TiDB.
---

# Set Operations

TiDB supports three set operations using the UNION, EXCEPT, and INTERSECT operators. The smallest unit of a set is a [`SELECT` statement](/sql-statements/sql-statement-select.md).

## UNION operator

In mathematics, the union of two sets A and B consists of all elements that are in A or in B. For example:

```sql
select 1 union select 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB supports both `UNION DISTINCT` and `UNION ALL` operators. `UNION DISTINCT` removes duplicate records from the result set, while `UNION ALL` keeps all records including duplicates. `UNION DISTINCT` is used by default in TiDB.

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);
INSERT INTO t1 values (1),(2);
INSERT INTO t2 values (1),(3);
```

Examples for `UNION DISTINCT` and `UNION ALL` queries are respectively as follows:

```sql
SELECT * FROM t1 union distinct SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)
SELECT * FROM t1 union all SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 1 |
| 3 |
+---+
4 rows in set (0.00 sec)
```

## EXCEPT operator

If A and B are two sets, EXCEPT returns the difference set of A and B which consists of elements that are in A but not in B.

```sql
SELECT * FROM t1 except SELECT * FROM t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

`EXCEPT ALL` operator is not yet supported.

## INTERSECT operator

In mathematics, the intersection of two sets A and B consists of all elements that are both in A and B, and no other elements.

```sql
SELECT * FROM t1 intersect SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL` operator is not yet supported. INTERSECT operator has higher precedence over EXCEPT and UNION operators.

```sql
SELECT * FROM t1 union all SELECT * FROM t1 intersect SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 1 |
| 2 |
+---+
3 rows in set (0.00 sec)
```

## Parentheses

TiDB supports using parentheses to specify the precedence of set operations. Expressions in parentheses are processed first.

```sql
(SELECT * FROM t1 union all SELECT * FROM t1) intersect SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## Use `Order By` and `Limit`

TiDB supports using [`ORDER BY`](/media/sqlgram/OrderByOptional.png) or [`LIMIT`](/media/sqlgram/LimitClause.png) clause in set operations. These two clauses must be at the end of the entire statement.

```sql
(SELECT * FROM t1 union all SELECT * FROM t1 intersect SELECT * FROM t2) order by a limit 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```
