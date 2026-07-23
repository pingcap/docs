---
title: Aggregate (GROUP BY) Functions
summary: Learn about the supported aggregate functions in TiDB.
aliases: ['/docs/dev/functions-and-operators/aggregate-group-by-functions/','/docs/dev/reference/sql/functions-and-operators/aggregate-group-by-functions/']
---

# Aggregate (GROUP BY) Functions

This document describes details about the supported aggregate functions in TiDB.

## Supported aggregate functions

This section describes the supported MySQL `GROUP BY` aggregate functions in TiDB.

| Name                                                                                                           | Description                                       |
|:---------------------------------------------------------------------------------------------------------------|:--------------------------------------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                   | Return a count of the number of rows returned     |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)  | Return the count of a number of different values  |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                       | Return the sum                                    |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                       | Return the average value of the argument          |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                       | Return the maximum value                          |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                       | Return the minimum value                          |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)     | Return a concatenated string                      |
| [`VARIANCE()`, `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop) | Return the population standard variance           |
| [`STD()`, `STDDEV()`, `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std) | Return the population standard deviation      |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)             | Return the sample variance                        |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)       | Return the sample standard deviation              |
| [`JSON_ARRAYAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)         | Return the result set as a single JSON array      |
| [`JSON_OBJECTAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg)       | Return the result set as a single JSON object containing key-value pairs |

- Unless otherwise stated, group functions ignore `NULL` values.
- If you use a group function in a statement containing no `GROUP BY` clause, it is equivalent to grouping on all rows.

In addition, TiDB also provides the following aggregate functions:

+ `SUM_INT(expr)`

    This function returns the sum of the integer expression `expr`. It works similarly to `SUM(expr)`, but only accepts integer arguments, including `TINYINT`, `SMALLINT`, `MEDIUMINT`, `INT`, and `BIGINT` (both signed and unsigned). For a signed integer argument, the return type is `BIGINT`. For an unsigned integer argument, the return type is `BIGINT UNSIGNED`. If the sum of non-`NULL` values exceeds the range of the return type, TiDB returns an integer overflow error.

    `SUM_INT()` ignores `NULL` values. If there are no non-`NULL` values, it returns `NULL`. `SUM_INT()` supports `DISTINCT` and can be used as a [window function](/functions-and-operators/window-functions.md).

    The following example shows how to use `SUM_INT()`:

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(id INT PRIMARY KEY, a BIGINT, b BIGINT UNSIGNED);
    INSERT INTO t VALUES(1, 1, 1), (2, 1, 1), (3, 2, 2), (4, NULL, NULL);
    ```

    ```sql
    SELECT SUM_INT(a), SUM_INT(DISTINCT a), SUM_INT(b) FROM t;
    ```

    ```sql
    +------------+---------------------+------------+
    | SUM_INT(a) | SUM_INT(DISTINCT a) | SUM_INT(b) |
    +------------+---------------------+------------+
    |          4 |                   3 |          4 |
    +------------+---------------------+------------+
    1 row in set (0.00 sec)
    ```

    The following example uses `SUM_INT()` as a window function:

    ```sql
    SELECT id, a, SUM_INT(a) OVER (ORDER BY id ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS rolling_sum
    FROM t
    ORDER BY id;
    ```

    ```sql
    +----+------+-------------+
    | id | a    | rolling_sum |
    +----+------+-------------+
    |  1 |    1 |           1 |
    |  2 |    1 |           2 |
    |  3 |    2 |           3 |
    |  4 | NULL |           2 |
    +----+------+-------------+
    4 rows in set (0.00 sec)
    ```

+ `MAX_COUNT([ALL] expr)` and `MIN_COUNT([ALL] expr)`

    These functions are TiDB-specific aggregate functions that count occurrences of the maximum or minimum value in a group. `MAX_COUNT(expr)` returns the number of rows whose value equals the maximum non-`NULL` value of `expr` in the current group. `MIN_COUNT(expr)` returns the number of rows whose value equals the minimum non-`NULL` value of `expr` in the current group.

    These functions ignore `NULL` values by default. If there are no non-`NULL` values in the current group, they return `0`. The return type is `BIGINT`. These functions support omitting `ALL` or explicitly specifying `ALL`, but do not support `DISTINCT`. For example, `MAX_COUNT(DISTINCT expr)` and `MIN_COUNT(DISTINCT expr)` return a syntax error. These functions can also be used as [window functions](/functions-and-operators/window-functions.md).

    The following example shows how to use these functions:

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT);
    INSERT INTO t VALUES(1), (1), (2), (2), (2), (NULL);
    ```

    ```sql
    SELECT MAX_COUNT(a), MIN_COUNT(a) FROM t;
    ```

    ```sql
    +--------------+--------------+
    | MAX_COUNT(a) | MIN_COUNT(a) |
    +--------------+--------------+
    |            3 |            2 |
    +--------------+--------------+
    1 row in set (0.00 sec)
    ```

    If there are no non-`NULL` values, these functions return `0`:

    ```sql
    SELECT MAX_COUNT(a), MIN_COUNT(a) FROM t WHERE a IS NULL;
    ```

    ```sql
    +--------------+--------------+
    | MAX_COUNT(a) | MIN_COUNT(a) |
    +--------------+--------------+
    |            0 |            0 |
    +--------------+--------------+
    1 row in set (0.00 sec)
    ```

    The following example uses `MAX_COUNT()` and `MIN_COUNT()` as window functions:

    ```sql
    SELECT
        MAX_COUNT(a) OVER () AS max_count,
        MIN_COUNT(a) OVER () AS min_count
    FROM t
    LIMIT 1;
    ```

    ```sql
    +-----------+-----------+
    | max_count | min_count |
    +-----------+-----------+
    |         3 |         2 |
    +-----------+-----------+
    1 row in set (0.00 sec)
    ```

+ `APPROX_PERCENTILE(expr, constant_integer_expr)`

    This function returns the percentile of `expr`. The `constant_integer_expr` argument indicates the percentage value which is a constant integer in the range of `[1,100]`. A percentile P<sub>k</sub> (`k` represents percentage) indicates that there are at least `k%` values in the data set that are less than or equal to P<sub>k</sub>.

    This function only supports the [numeric type](/data-type-numeric.md) and the [date and time type](/data-type-date-and-time.md) as the returned type of `expr`. For other returned types, `APPROX_PERCENTILE` only returns `NULL`.

    The following example shows how to calculate the fiftieth percentile of a `INT` column:

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT);
    INSERT INTO t VALUES(1), (2), (3);
    ```

    ```sql
    SELECT APPROX_PERCENTILE(a, 50) FROM t;
    ```

    ```sql
    +--------------------------+
    | APPROX_PERCENTILE(a, 50) |
    +--------------------------+
    |                        2 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

+ `APPROX_COUNT_DISTINCT(expr, [expr...])`

    This function is similar to `COUNT(DISTINCT)` in counting the number of distinct values but returns an approximate result. It uses the `BJKST` algorithm, significantly reducing memory consumption when processing large datasets with a power-law distribution. Moreover, for low-cardinality data, this function provides high accuracy while maintaining efficient CPU utilization.

    The following example shows how to use this function:

    ```sql
    DROP TABLE IF EXISTS t;
    CREATE TABLE t(a INT, b INT, c INT);
    INSERT INTO t VALUES(1, 1, 1), (2, 1, 1), (2, 2, 1), (3, 1, 1), (5, 1, 2), (5, 1, 2), (6, 1, 2), (7, 1, 2);
    ```

    ```sql
    SELECT APPROX_COUNT_DISTINCT(a, b) FROM t GROUP BY c;
    ```

    ```
    +-----------------------------+
    | approx_count_distinct(a, b) |
    +-----------------------------+
    |                           3 |
    |                           4 |
    +-----------------------------+
    2 rows in set (0.00 sec)
    ```

Except for the `GROUP_CONCAT()`, `APPROX_PERCENTILE()`, and `APPROX_COUNT_DISTINCT()` functions, all the preceding functions can serve as [window functions](/functions-and-operators/window-functions.md).

## GROUP BY modifiers

Starting from v7.4.0, the `GROUP BY` clause of TiDB supports the `WITH ROLLUP` modifier. For more information, see [GROUP BY modifiers](/functions-and-operators/group-by-modifier.md).

## SQL mode support

TiDB supports the SQL Mode `ONLY_FULL_GROUP_BY`, and when enabled TiDB will refuse queries with ambiguous non-aggregated columns. For example, this query is invalid with `ONLY_FULL_GROUP_BY` enabled because the non-aggregated column "b" in the `SELECT` list does not appear in the `GROUP BY` statement:

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 3), (2, 2, 3), (3, 2, 3);

mysql> select a, b, sum(c) from t group by a;
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 rows in set (0.01 sec)

mysql> set sql_mode = 'ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.00 sec)

mysql> select a, b, sum(c) from t group by a;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

TiDB currently enables the [`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences) mode by default.

### Differences from MySQL

The current implementation of `ONLY_FULL_GROUP_BY` is less strict than that in MySQL 5.7. For example, suppose that we execute the following query, expecting the results to be ordered by "c":

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

To order the result, duplicates must be eliminated first. But to do so, which row should we keep? This choice influences the retained value of "c", which in turn influences ordering and makes it arbitrary as well.

In MySQL, a query that has `DISTINCT` and `ORDER BY` is rejected as invalid if any `ORDER BY` expression does not satisfy at least one of these conditions:

- The expression is equal to one in the `SELECT` list
- All columns referenced by the expression and belonging to the query's selected tables are elements of the `SELECT` list

But in TiDB, the above query is legal, for more information see [#4254](https://github.com/pingcap/tidb/issues/4254).

Another TiDB extension to standard SQL permits references in the `HAVING` clause to aliased expressions in the `SELECT` list. For example, the following query returns "name" values that occur only once in table "orders":

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

The TiDB extension permits the use of an alias in the `HAVING` clause for the aggregated column:

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

Standard SQL permits only column expressions in `GROUP BY` clauses, so a statement such as this is invalid because "FLOOR(value/100)" is a noncolumn expression:

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB extends standard SQL to permit noncolumn expressions in `GROUP BY` clauses and considers the preceding statement valid.

Standard SQL also does not permit aliases in `GROUP BY` clauses. TiDB extends standard SQL to permit aliases, so another way to write the query is as follows:

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## Related system variables

The [`group_concat_max_len`](/system-variables.md#group_concat_max_len) variable sets the maximum number of items for the `GROUP_CONCAT()` function.
