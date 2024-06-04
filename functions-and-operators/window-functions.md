---
title: Window Functions
summary: This document introduces window functions supported in TiDB.
aliases: ['/docs/dev/functions-and-operators/window-functions/','/docs/dev/reference/sql/functions-and-operators/window-functions/']
---

# Window Functions

The usage of window functions in TiDB is similar to that in MySQL 8.0. For details, see [MySQL Window Functions](https://dev.mysql.com/doc/refman/8.0/en/window-functions.html).

Because window functions reserve additional [keywords](/keywords.md) in the parser, TiDB provides an option to disable window functions. If you receive errors parsing SQL statements after upgrading, try setting [`tidb_enable_window_function=0`](/system-variables.md#tidb_enable_window_function).

The pipeline execution algorithm for window functions can be disabled with the [`tidb_enable_pipelined_window_function`](/system-variables.md#tidb_enable_pipelined_window_function) system variable.

Another system variable that influences window functions is [`windowing_use_high_precision`](/system-variables.md#windowing_use_high_precision). You can use this variable to turn off high precision mode.

The window functions [listed here](/tiflash/tiflash-supported-pushdown-calculations.md) can be pushed down to TiFlash.

Except for `GROUP_CONCAT()` and `APPROX_PERCENTILE()`, TiDB supports all [`GROUP BY` aggregate functions](/functions-and-operators/aggregate-group-by-functions.md). In addition, TiDB supports the following window functions:

| Function name | Feature description |
| :-------------- | :------------------------------------- |
| [`CUME_DIST()`](#cume_dist) | Returns the cumulative distribution of a value within a group of values. |
| [`DENSE_RANK()`](#dense_rank) | Returns the rank of the current row within the partition, and the rank is without gaps. |
| [`FIRST_VALUE()`](#first_value) | Returns the expression value of the first row in the current window. |
| [`LAG()`](#lag) | Returns the expression value from the row that precedes the current row by N rows within the partition. |
| [`LAST_VALUE()`](#last_value) | Returns the expression value of the last row in the current window. |
| [`LEAD()`](#lead) | Returns the expression value from the row that follows the current row by N rows within the partition. |
| [`NTH_VALUE()`](#nth_value) | Returns the expression value from the N-th row of the current window. |
| [`NTILE()`](#ntile)| Divides a partition into N buckets, assigns the bucket number to each row in the partition, and returns the bucket number of the current row within the partition. |
| [`PERCENT_RANK()`](#percent_rank)| Returns the percentage of partition values that are less than the value in the current row. |
| [`RANK()`](#rank)| Returns the rank of the current row within the partition. The rank may be with gaps. |
| [`ROW_NUMBER()`](#row_number)| Returns the number of the current row in the partition. |

## [`CUME_DIST()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_cume-dist)

`CUME_DIST()` calculates the cumulative distance. Note that the window definition should use an `ORDER BY`, otherwise this will not return the expected values.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+2
    FROM
        cte
    WHERE 
        n<6
)
SELECT
    *,
    CUME_DIST() OVER(ORDER BY n)
FROM
    cte;
```

```
+------+------------------------------+
| n    | CUME_DIST() OVER(ORDER BY n) |
+------+------------------------------+
|    1 |                         0.25 |
|    3 |                          0.5 |
|    5 |                         0.75 |
|    7 |                            1 |
+------+------------------------------+
4 rows in set (0.00 sec)
```

## [`DENSE_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_dense-rank)

The `DENSE_RANK()` function is similar to [`RANK()`](#rank) but won't leave any gaps in case of ties.

```sql
SELECT 
    *,
    DENSE_RANK() OVER (ORDER BY n) 
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+--------------------------------+
| n  | DENSE_RANK() OVER (ORDER BY n) |
+----+--------------------------------+
|  5 |                              1 |
|  5 |                              1 |
|  8 |                              2 |
| 30 |                              3 |
| 31 |                              4 |
| 32 |                              5 |
+----+--------------------------------+
6 rows in set (0.00 sec)
```

## [`FIRST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_first-value)

The `FIRST_VALUE(expr)` returns the first value of a group.

In the following example we use two different window definitions:

1. `PARTITION BY n MOD 2 ORDER BY n` resulting in two groups: `1, 3` and `2, 4`. So this returns either 1 or 2 as those are the first values of those groups.
2. `PARTITION BY n <= 2 ORDER BY n` resulting in two groups: `1, 2` and `3, 4` So this returns either 1 or 3 depending on which group it is group.

```sql
SELECT 
    n,
    FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n),
    FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n)
FROM (
    SELECT 1 AS 'n'
    UNION
    SELECT 2
    UNION
    SELECT 3
    UNION
    SELECT 4
) a
ORDER BY 
    n;
```

```
+------+-------------------------------------------------------+------------------------------------------------------+
| n    | FIRST_VALUE(n) OVER (PARTITION BY n MOD 2 ORDER BY n) | FIRST_VALUE(n) OVER (PARTITION BY n <= 2 ORDER BY n) |
+------+-------------------------------------------------------+------------------------------------------------------+
|    1 |                                                     1 |                                                    1 |
|    2 |                                                     2 |                                                    1 |
|    3 |                                                     1 |                                                    3 |
|    4 |                                                     2 |                                                    3 |
+------+-------------------------------------------------------+------------------------------------------------------+
4 rows in set (0.00 sec)
```

## [`LAG()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lag)

The `LAG(expr [, num [, default]])` function returns the value that is lagging behind `num` values behind the the current value. If there is no current value then `default` is returned, which defaults to `NULL`.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT 1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT 
    n,
    LAG(n) OVER ()
FROM
    cte;
```

```
+------+----------------+
| n    | LAG(n) OVER () |
+------+----------------+
|    1 |           NULL |
|    2 |              1 |
|    3 |              2 |
|    4 |              3 |
|    5 |              4 |
|    6 |              5 |
|    7 |              6 |
|    8 |              7 |
|    9 |              8 |
|   10 |              9 |
+------+----------------+
10 rows in set (0.01 sec)
```

## [`LAST_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_last-value)

The `LAST_VALUE()` function returns the last value in the window.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1 
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LAST_VALUE(n) OVER (PARTITION BY n<=5)
FROM
    cte
ORDER BY
    n;
```

```
+------+----------------------------------------+
| n    | LAST_VALUE(n) OVER (PARTITION BY n<=5) |
+------+----------------------------------------+
|    1 |                                      5 |
|    2 |                                      5 |
|    3 |                                      5 |
|    4 |                                      5 |
|    5 |                                      5 |
|    6 |                                     10 |
|    7 |                                     10 |
|    8 |                                     10 |
|    9 |                                     10 |
|   10 |                                     10 |
+------+----------------------------------------+
10 rows in set (0.00 sec)
```

## [`LEAD()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_lead)

The `LEAD(expr [, num [,default]])` function returns the value leading (preceding) in the window. It is leading by `num` values, by default `1`. And `default` is returned if there is no leading value, this is `NULL` by default.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    LEAD(n) OVER ()
FROM
    cte;
```

```
+------+-----------------+
| n    | LEAD(n) OVER () |
+------+-----------------+
|    1 |               2 |
|    2 |               3 |
|    3 |               4 |
|    4 |               5 |
|    5 |               6 |
|    6 |               7 |
|    7 |               8 |
|    8 |               9 |
|    9 |              10 |
|   10 |            NULL |
+------+-----------------+
10 rows in set (0.00 sec)
```

## [`NTH_VALUE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_nth-value)

The `NTH_VALUE(expr, n)` function returns the `n`-th value of the window.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1 
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
        n<10
)
SELECT
    n,
    FIRST_VALUE(n) OVER w AS 'First',
    NTH_VALUE(n, 2) OVER w AS 'Second',
    NTH_VALUE(n, 3) OVER w AS 'Third',
    LAST_VALUE(n) OVER w AS 'Last'
FROM
    cte
WINDOW
    w AS (PARTITION BY n<=5)
ORDER BY
    n;
```

```
+------+-------+--------+-------+------+
| n    | First | Second | Third | Last |
+------+-------+--------+-------+------+
|    1 |     1 |      2 |     3 |    5 |
|    2 |     1 |      2 |     3 |    5 |
|    3 |     1 |      2 |     3 |    5 |
|    4 |     1 |      2 |     3 |    5 |
|    5 |     1 |      2 |     3 |    5 |
|    6 |     6 |      7 |     8 |   10 |
|    7 |     6 |      7 |     8 |   10 |
|    8 |     6 |      7 |     8 |   10 |
|    9 |     6 |      7 |     8 |   10 |
|   10 |     6 |      7 |     8 |   10 |
+------+-------+--------+-------+------+
10 rows in set (0.00 sec)
```

## [`NTILE()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_ntile)

The `NTILE(n)` function divides the window in `n` groups and returns the number of the group.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+1
    FROM
        cte
    WHERE
    n<10
)
SELECT
    n,
    NTILE(5) OVER (),
    NTILE(2) OVER ()
FROM
    cte;
```

```
+------+------------------+------------------+
| n    | NTILE(5) OVER () | NTILE(2) OVER () |
+------+------------------+------------------+
|    1 |                1 |                1 |
|    2 |                1 |                1 |
|    3 |                2 |                1 |
|    4 |                2 |                1 |
|    5 |                3 |                1 |
|    6 |                3 |                2 |
|    7 |                4 |                2 |
|    8 |                4 |                2 |
|    9 |                5 |                2 |
|   10 |                5 |                2 |
+------+------------------+------------------+
10 rows in set (0.00 sec)

```

## [`PERCENT_RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_percent-rank)

The `PERCENT_RANK()` function returns a number between 0 and 1 indicating the percentage of rows with a value less than the current window.

```sql
SELECT 
    *,
    PERCENT_RANK() OVER (ORDER BY n),
    PERCENT_RANK() OVER (ORDER BY n DESC)
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+----------------------------------+---------------------------------------+
| n  | PERCENT_RANK() OVER (ORDER BY n) | PERCENT_RANK() OVER (ORDER BY n DESC) |
+----+----------------------------------+---------------------------------------+
|  5 |                                0 |                                   0.8 |
|  5 |                                0 |                                   0.8 |
|  8 |                              0.4 |                                   0.6 |
| 30 |                              0.6 |                                   0.4 |
| 31 |                              0.8 |                                   0.2 |
| 32 |                                1 |                                     0 |
+----+----------------------------------+---------------------------------------+
6 rows in set (0.00 sec)
```

## [`RANK()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_rank)

The `RANK()` function is similar to [`DENSE_RANK()`](#dense_rank) but will leave any gaps in case of ties.

```sql
SELECT 
    *,
    RANK() OVER (ORDER BY n),
    DENSE_RANK() OVER (ORDER BY n) 
FROM (
    SELECT 5 AS 'n'
    UNION ALL
    SELECT 8
    UNION ALL
    SELECT 5
    UNION ALL
    SELECT 30
    UNION ALL
    SELECT 31
    UNION ALL
    SELECT 32) a;
```

```
+----+--------------------------+--------------------------------+
| n  | RANK() OVER (ORDER BY n) | DENSE_RANK() OVER (ORDER BY n) |
+----+--------------------------+--------------------------------+
|  5 |                        1 |                              1 |
|  5 |                        1 |                              1 |
|  8 |                        3 |                              2 |
| 30 |                        4 |                              3 |
| 31 |                        5 |                              4 |
| 32 |                        6 |                              5 |
+----+--------------------------+--------------------------------+
6 rows in set (0.00 sec)
```

## [`ROW_NUMBER()`](https://dev.mysql.com/doc/refman/8.0/en/window-function-descriptions.html#function_row-number)

The `ROW_NUMBER()` returns the row number of the resultset.

```sql
WITH RECURSIVE cte(n) AS (
    SELECT
        1
    UNION
    SELECT
        n+3
    FROM
        cte
    WHERE
        n<30
)
SELECT
    n,
    ROW_NUMBER() OVER ()
FROM
    cte;
```

```
+------+----------------------+
| n    | ROW_NUMBER() OVER () |
+------+----------------------+
|    1 |                    1 |
|    4 |                    2 |
|    7 |                    3 |
|   10 |                    4 |
|   13 |                    5 |
|   16 |                    6 |
|   19 |                    7 |
|   22 |                    8 |
|   25 |                    9 |
|   28 |                   10 |
|   31 |                   11 |
+------+----------------------+
11 rows in set (0.00 sec)
```