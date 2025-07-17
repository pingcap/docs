---
title: Set Operations
summary: 了解 TiDB 支持的集合操作。
---

# Set Operations

TiDB 支持使用 UNION、EXCEPT 和 INTERSECT 操作符的三种集合操作。集合的最小单位是一个 [`SELECT` statement](/sql-statements/sql-statement-select.md)。

## UNION operator

在数学中，两个集合 A 和 B 的并集由所有在 A 或 B 中的元素组成。例如：

```sql
SELECT 1 UNION SELECT 2;
+---+
| 1 |
+---+
| 2 |
| 1 |
+---+
2 rows in set (0.00 sec)
```

TiDB 支持 `UNION DISTINCT` 和 `UNION ALL` 两种操作符。`UNION DISTINCT` 会从结果集中移除重复的记录，而 `UNION ALL` 会保留所有记录，包括重复项。TiDB 默认使用 `UNION DISTINCT`。

```sql
CREATE TABLE t1 (a int);
CREATE TABLE t2 (a int);
INSERT INTO t1 VALUES (1),(2);
INSERT INTO t2 VALUES (1),(3);
```

`UNION DISTINCT` 和 `UNION ALL` 查询的示例如下：

```sql
SELECT * FROM t1 UNION DISTINCT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
+---+
3 rows in set (0.00 sec)

SELECT * FROM t1 UNION ALL SELECT * FROM t2;
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

如果 A 和 B 是两个集合，EXCEPT 返回 A 和 B 的差集，即在 A 中但不在 B 中的元素。

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2;
+---+
| a |
+---+
| 2 |
+---+
1 rows in set (0.00 sec)
```

`EXCEPT ALL` 操作符尚不支持。

## INTERSECT operator

在数学中，两个集合 A 和 B 的交集由同时在 A 和 B 中的所有元素组成，且不包含其他元素。

```sql
SELECT * FROM t1 INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

`INTERSECT ALL` 操作符尚不支持。INTERSECT 操作符的优先级高于 EXCEPT 和 UNION 操作符。

```sql
SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2;
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

TiDB 支持使用括号来指定集合操作的优先级。括号中的表达式会优先处理。

```sql
(SELECT * FROM t1 UNION ALL SELECT * FROM t1) INTERSECT SELECT * FROM t2;
+---+
| a |
+---+
| 1 |
+---+
1 rows in set (0.00 sec)
```

## Use `ORDER BY` and `LIMIT`

TiDB 支持在整个集合操作的结果上使用 `ORDER BY` 或 `LIMIT` 子句。这两个子句必须放在整个语句的最后。

```sql
(SELECT * FROM t1 UNION ALL SELECT * FROM t1 INTERSECT SELECT * FROM t2) ORDER BY a LIMIT 2;
+---+
| a |
+---+
| 1 |
| 1 |
+---+
2 rows in set (0.00 sec)
```