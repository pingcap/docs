---
title: Aggregate (GROUP BY) Functions
summary: 了解 TiDB 支持的聚合函数。
---

# Aggregate (GROUP BY) Functions

本文档描述了 TiDB 支持的聚合函数的详细信息。

## 支持的聚合函数

本节介绍 TiDB 中支持的 MySQL `GROUP BY` 聚合函数。

| 名称                                                                                                           | 描述                                       |
|:--------------------------------------------------------------------------------------------------------------|:------------------------------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                   | 返回满足条件的行数                        |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)  | 返回不同值的个数                         |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                       | 返回总和                                |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                       | 返回参数的平均值                        |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                       | 返回最大值                            |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                       | 返回最小值                            |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)     | 返回连接后的字符串                      |
| [`VARIANCE()`, `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop) | 返回总体标准差方差                     |
| [`STD()`, `STDDEV()`, `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std) | 返回总体标准差                        |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)             | 返回样本方差                          |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)       | 返回样本标准差                        |
| [`JSON_ARRAYAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)         | 以单个 JSON 数组形式返回结果集        |
| [`JSON_OBJECTAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg)       | 以包含键值对的单个 JSON 对象形式返回结果集 |

- 除非另有说明，否则组函数会忽略 `NULL` 值。
- 如果在不包含 `GROUP BY` 子句的语句中使用组函数，则等同于对所有行进行分组。

此外，TiDB 还提供以下聚合函数：

+ `APPROX_PERCENTILE(expr, constant_integer_expr)`

    该函数返回 `expr` 的百分位数。`constant_integer_expr` 参数表示百分比值，是范围在 `[1,100]` 的常数整数。百分位 P<sub>k</sub>（`k` 代表百分比）表示数据集中至少有 `k%` 的值小于或等于 P<sub>k</sub>。

    该函数仅支持 [数值类型](/data-type-numeric.md) 和 [日期时间类型](/data-type-date-and-time.md) 作为 `expr` 的返回类型。对于其他返回类型，`APPROX_PERCENTILE` 仅返回 `NULL`。

    以下示例演示如何计算 `INT` 列的第50百分位数：

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
    1 行结果（0.00 秒）
    ```

+ `APPROX_COUNT_DISTINCT(expr, [expr...])`

    该函数类似于 `COUNT(DISTINCT)`，用于统计不同值的个数，但返回近似结果。它采用 `BJKST` 算法，在处理具有幂律分布的大型数据集时显著减少内存消耗。此外，对于低基数数据，该函数提供高精度，同时保持高效的 CPU 利用率。

    以下示例演示如何使用该函数：

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
    2 行结果（0.00 秒）
    ```

除了 `GROUP_CONCAT()`、`APPROX_PERCENTILE()` 和 `APPROX_COUNT_DISTINCT` 函数外，以上所有函数都可以作为 [Window functions](/functions-and-operators/window-functions.md) 使用。

## GROUP BY 修饰符

从 v7.4.0 版本开始，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。更多信息请参见 [GROUP BY modifiers](/functions-and-operators/group-by-modifier.md)。

## SQL 模式支持

TiDB 支持 SQL 模式 `ONLY_FULL_GROUP_BY`，启用后 TiDB 会拒绝存在歧义的非聚合列的查询。例如，启用 `ONLY_FULL_GROUP_BY` 后，以下查询是非法的，因为 `SELECT` 列表中的非聚合列 "b" 没有出现在 `GROUP BY` 子句中：

```sql
DROP TABLE IF EXISTS t;
CREATE TABLE t(a BIGINT, b BIGINT, c BIGINT);
INSERT INTO t VALUES(1, 2, 3), (2, 2, 3), (3, 2, 3);

mysql> SELECT a, b, SUM(c) FROM t GROUP BY a;
+------+------+--------+
| a    | b    | sum(c) |
+------+------+--------+
|    1 |    2 |      3 |
|    2 |    2 |      3 |
|    3 |    2 |      3 |
+------+------+--------+
3 行结果（0.01 秒）

mysql> SET sql_mode = 'ONLY_FULL_GROUP_BY';
Query OK, 0 行受影响（0.00 秒）

mysql> SELECT a, b, SUM(c) FROM t GROUP BY a;
ERROR 1055 (42000): Expression #2 of SELECT list is not in GROUP BY clause and contains nonaggregated column 'b' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

TiDB 当前默认启用 [`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences) 模式。

### 与 MySQL 的差异

`ONLY_FULL_GROUP_BY` 的当前实现比 MySQL 5.7 中的要求宽松。例如，假设执行以下查询，期望结果按 "c" 排序：

```sql
DROP TABLE IF EXISTS t;
CREATE TABLE t(a BIGINT, b BIGINT, c BIGINT);
INSERT INTO t VALUES(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
SELECT DISTINCT a, b FROM t ORDER BY c;
```

为了排序，必须先去重。但去重后，应保留哪一行？这个选择会影响 "c" 的值，从而影响排序，变得任意。

在 MySQL 中，如果 `DISTINCT` 和 `ORDER BY` 一起使用，只要 `ORDER BY` 的表达式不满足以下条件之一，查询就会被拒绝：

- 表达式等于 `SELECT` 列表中的某一项
- 表达式引用的所有列都属于查询的 `SELECT` 列表中的元素

但在 TiDB 中，上述查询是合法的，更多信息请参见 [#4254](https://github.com/pingcap/tidb/issues/4254)。

TiDB 还扩展了标准 SQL，允许在 `HAVING` 子句中引用 `SELECT` 列表中的别名表达式。例如，以下查询返回在 `orders` 表中只出现一次的 "name" 值：

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB 扩展允许在 `HAVING` 子句中使用别名来引用聚合列：

```sql
select name, count(name) as c from orders
group by name
having c = 1;
```

标准 SQL 只允许在 `GROUP BY` 子句中使用列表达式，因此如下语句是无效的，因为 "FLOOR(value/100)" 是非列表达式：

```sql
select id, floor(value/100)
from tbl_name
group by id, floor(value/100);
```

TiDB 扩展了标准 SQL，允许在 `GROUP BY` 子句中使用非列表达式，并认为上述语句是合法的。

标准 SQL 也不允许在 `GROUP BY` 中使用别名。TiDB 扩展了标准 SQL，允许使用别名，因此另一种写法如下：

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```