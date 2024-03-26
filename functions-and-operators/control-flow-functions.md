---
title: Control Flow Functions
summary: Learn about the Control Flow functions.
aliases: ['/docs/dev/functions-and-operators/control-flow-functions/','/docs/dev/reference/sql/functions-and-operators/control-flow-functions/']
---

# Control Flow Functions

TiDB supports all of the [control flow functions](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html) available in MySQL 8.0.

| Name                                                                                            | Description                       |
|:--------------------------------------------------------------------------------------------------|:----------------------------------|
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case operator                     |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | If/else construct                 |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | Null if/else construct            |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | Return NULL if expr1 = expr2      |

## CASE

The `CASE` operator allows you to respond on multiple values and conditions.

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, CASE WHEN n MOD 2 THEN "odd" ELSE "even" END FROM d
```

```
+----+----------------------------------------------+
| n  | CASE WHEN n MOD 2 THEN "odd" ELSE "even" END |
+----+----------------------------------------------+
|  1 | odd                                          |
|  2 | even                                         |
|  3 | odd                                          |
|  4 | even                                         |
|  5 | odd                                          |
|  6 | even                                         |
|  7 | odd                                          |
|  8 | even                                         |
|  9 | odd                                          |
| 10 | even                                         |
+----+----------------------------------------------+
10 rows in set (0.00 sec)
```

## IF()

The `IF()` statement allows you to do something based on wheter a value or expression is true or not.

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, IF(n MOD 2, "odd", "even") FROM d;
```

```
+----+----------------------------+
| n  | IF(n MOD 2, "odd", "even") |
+----+----------------------------+
|  1 | odd                        |
|  2 | even                       |
|  3 | odd                        |
|  4 | even                       |
|  5 | odd                        |
|  6 | even                       |
|  7 | odd                        |
|  8 | even                       |
|  9 | odd                        |
| 10 | even                       |
+----+----------------------------+
10 rows in set (0.00 sec)
```

## IFNULL()

The `IFNULL()` functions returns the data of the expression if it is not NULL and if it is NULL it returns the data of the second argument of the function.

```sql
WITH data AS (SELECT NULL AS x UNION ALL SELECT 1 )
SELECT x, IFNULL(x,'x has no value') FROM data;
```

```
+------+----------------------------+
| x    | IFNULL(x,'x has no value') |
+------+----------------------------+
| NULL | x has no value             |
|    1 | 1                          |
+------+----------------------------+
2 rows in set (0.0006 sec)
```

## NULLIF()

The `NULLIF()` function returns null if both arguments are the same. Otherwise it returns the first argument.

```sql
WITH RECURSIVE d AS (SELECT 1 AS n UNION ALL SELECT n+1 FROM d WHERE n<10)
SELECT n, NULLIF(n+n, n+2) FROM d;
```

```
+----+------------------+
| n  | NULLIF(n+n, n+2) |
+----+------------------+
|  1 |                2 |
|  2 |             NULL |
|  3 |                6 |
|  4 |                8 |
|  5 |               10 |
|  6 |               12 |
|  7 |               14 |
|  8 |               16 |
|  9 |               18 |
| 10 |               20 |
+----+------------------+
10 rows in set (0.00 sec)
```

Here n+n and n+2 both evaluate to 4 if n is 2, which makes both arguments the same and the function return NULL.