---
title: 聚合（GROUP BY）函数
summary: 了解 TiDB 支持的聚合函数。
---

# 聚合（GROUP BY）函数

本文档介绍了 TiDB 支持的聚合函数的详细信息。

## 支持的聚合函数

本节介绍了 TiDB 支持的 MySQL `GROUP BY` 聚合函数。

| 名称                                                                                                           | 描述                                       |
|:---------------------------------------------------------------------------------------------------------------|:-------------------------------------------|
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                   | 返回结果集中的行数                         |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct)  | 返回不同值的数量                           |
| [`SUM()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_sum)                       | 返回总和                                   |
| [`AVG()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_avg)                       | 返回参数的平均值                           |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                       | 返回最大值                                 |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                       | 返回最小值                                 |
| [`GROUP_CONCAT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_group-concat)     | 返回拼接后的字符串                         |
| [`VARIANCE()`, `VAR_POP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-pop) | 返回总体方差                               |
| [`STD()`, `STDDEV()`, `STDDEV_POP`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_std) | 返回总体标准差                        |
| [`VAR_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_var-samp)             | 返回样本方差                               |
| [`STDDEV_SAMP()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_stddev-samp)       | 返回样本标准差                             |
| [`JSON_ARRAYAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_arrayagg)         | 将结果集作为单个 JSON 数组返回             |
| [`JSON_OBJECTAGG()`](/functions-and-operators/json-functions/json-functions-aggregate.md#json_objectagg)       | 将结果集作为包含键值对的单个 JSON 对象返回 |

- 除非另有说明，聚合函数会忽略 `NULL` 值。
- 如果你在没有 `GROUP BY` 子句的语句中使用聚合函数，则等价于对所有行进行分组。

此外，TiDB 还提供了以下聚合函数：

+ `APPROX_PERCENTILE(expr, constant_integer_expr)`

    该函数返回 `expr` 的百分位数。`constant_integer_expr` 参数表示百分比值，是一个取值范围为 `[1,100]` 的常量整数。百分位数 P<sub>k</sub>（`k` 表示百分比）表示数据集中至少有 `k%` 的值小于或等于 P<sub>k</sub>。

    该函数仅支持 [数值类型](/data-type-numeric.md) 和 [日期与时间类型](/data-type-date-and-time.md) 作为 `expr` 的返回类型。对于其他返回类型，`APPROX_PERCENTILE` 只会返回 `NULL`。

    以下示例展示了如何计算 `INT` 列的第 50 百分位数：

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

    该函数与 `COUNT(DISTINCT)` 类似，用于统计不同值的数量，但返回近似结果。它使用 `BJKST` 算法，在处理具有幂律分布的大型数据集时能显著降低内存消耗。此外，对于低基数数据，该函数在保持高效 CPU 利用率的同时，能够提供较高的准确性。

    以下示例展示了如何使用该函数：

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

除 `GROUP_CONCAT()`、`APPROX_PERCENTILE()` 和 `APPROX_COUNT_DISTINCT` 外，以上所有函数都可以作为 [窗口函数](/functions-and-operators/window-functions.md) 使用。

## GROUP BY 修饰符

自 v7.4.0 起，TiDB 的 `GROUP BY` 子句支持 `WITH ROLLUP` 修饰符。更多信息请参见 [GROUP BY 修饰符](/functions-and-operators/group-by-modifier.md)。

## SQL 模式支持

TiDB 支持 SQL 模式 `ONLY_FULL_GROUP_BY`，启用后，TiDB 会拒绝包含不明确的非聚合列的查询。例如，以下查询在启用 `ONLY_FULL_GROUP_BY` 时是无效的，因为 `SELECT` 列表中的非聚合列 "b" 没有出现在 `GROUP BY` 语句中：

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

TiDB 当前默认启用 [`ONLY_FULL_GROUP_BY`](/mysql-compatibility.md#default-differences) 模式。

### 与 MySQL 的差异

当前 `ONLY_FULL_GROUP_BY` 的实现比 MySQL 5.7 更宽松。例如，假设我们执行以下查询，期望结果按 "c" 排序：

```sql
drop table if exists t;
create table t(a bigint, b bigint, c bigint);
insert into t values(1, 2, 1), (1, 2, 2), (1, 3, 1), (1, 3, 2);
select distinct a, b from t order by c;
```

为了对结果排序，必须先去重。但在去重时，应该保留哪一行？这个选择会影响 "c" 的保留值，进而影响排序，使其变得不确定。

在 MySQL 中，如果 `DISTINCT` 和 `ORDER BY` 同时出现在查询中，且任一 `ORDER BY` 表达式不满足以下至少一个条件，则该查询会被判定为无效：

- 该表达式等于 `SELECT` 列表中的某个表达式
- 该表达式引用的所有列都属于查询所选表，并且这些列都是 `SELECT` 列表的元素

但在 TiDB 中，上述查询是合法的，更多信息请参见 [#4254](https://github.com/pingcap/tidb/issues/4254)。

TiDB 对标准 SQL 的另一个扩展是允许在 `HAVING` 子句中引用 `SELECT` 列表中的别名表达式。例如，以下查询返回在表 "orders" 中只出现一次的 "name" 值：

```sql
select name, count(name) from orders
group by name
having count(name) = 1;
```

TiDB 扩展允许在 `HAVING` 子句中使用聚合列的别名：

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

TiDB 扩展了标准 SQL，允许在 `GROUP BY` 子句中使用非列表达式，并认为上述语句是有效的。

标准 SQL 也不允许在 `GROUP BY` 子句中使用别名。TiDB 扩展了标准 SQL，允许使用别名，因此还可以如下方式编写查询：

```sql
select id, floor(value/100) as val
from tbl_name
group by id, val;
```

## 相关系统变量

[`group_concat_max_len`](/system-variables.md#group_concat_max_len) 变量用于设置 `GROUP_CONCAT()` 函数的最大项数。