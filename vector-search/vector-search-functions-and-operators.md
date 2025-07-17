---
title: Vector Functions and Operators
summary: 了解可用于 Vector 数据类型的函数和操作符。
---

# Vector Functions and Operators

本文档列出了可用于 Vector 数据类型的函数和操作符。

<CustomContent platform="tidb">

> **Warning:**
>
> 该功能为实验性功能。不建议在生产环境中使用。该功能可能在未通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 该功能处于测试阶段。可能会在未通知的情况下进行更改。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> Vector 数据类型和这些 Vector 函数在 TiDB 自托管版、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB 自托管版和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（建议使用 v8.5.0 及以上）。

## Vector 函数

以下函数专为 [Vector 数据类型](/vector-search/vector-search-data-types.md) 设计。

**Vector 距离函数：**

| 函数名 | 描述 |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| [`VEC_L2_DISTANCE`](#vec_l2_distance) | 计算两个向量之间的 L2 距离（欧几里得距离） |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance) | 计算两个向量之间的余弦距离 |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | 计算两个向量的内积的负值 |
| [`VEC_L1_DISTANCE`](#vec_l1_distance) | 计算两个向量之间的 L1 距离（曼哈顿距离） |

**其他向量函数：**

| 函数名 | 描述 |
| ------------------------------- | --------------------------------------------------- |
| [`VEC_DIMS`](#vec_dims) | 返回向量的维度 |
| [`VEC_L2_NORM`](#vec_l2_norm) | 计算向量的 L2 范数（欧几里得范数） |
| [`VEC_FROM_TEXT`](#vec_from_text) | 将字符串转换为向量 |
| [`VEC_AS_TEXT`](#vec_as_text) | 将向量转换为字符串 |

## 扩展的内置函数和操作符

以下内置函数和操作符已扩展支持对 [Vector 数据类型](/vector-search/vector-search-data-types.md) 的操作。

**算术操作符：**

| 名称 | 描述 |
| :-------------------------------------------------------------------------------------- | :--------------------------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus) | 向量元素逐个相加操作符 |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | 向量元素逐个相减操作符 |

关于向量算术的详细工作原理，请参见 [Vector Data Type | Arithmetic](/vector-search/vector-search-data-types.md#arithmetic)。

**聚合（GROUP BY）函数：**

| 名称 | 描述 |
| :----------------------- | :----------------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count) | 返回满足条件的行数 |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | 返回不同值的个数 |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max) | 返回最大值 |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min) | 返回最小值 |

**比较函数和操作符：**

| 名称 | 描述 |
| ---------------------------------------- | ----------------------------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between) | 检查值是否在某个范围内 |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce) | 返回第一个非 NULL 的参数 |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal) | 等于操作符 |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to) | 空安全相等操作符 |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than) | 大于操作符 |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal) | 大于或等于操作符 |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest) | 返回最大参数 |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in) | 检查值是否在某个集合内 |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null) | 测试值是否为 `NULL` |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull) | 测试参数是否为 `NULL` |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least) | 返回最小参数 |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than) | 小于操作符 |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal) | 小于或等于操作符 |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | 检查值是否不在某个范围内 |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal) | 不等于操作符 |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in) | 检查值是否不在某个集合内 |

关于向量比较的详细信息，请参见 [Vector Data Type | Comparison](/vector-search/vector-search-data-types.md#comparison)。

**流程控制函数：**

| 名称 | 描述 |
| :------------------------------------------------------------------------------------------------ | :--------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case) | 条件表达式 |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if) | 条件判断（if/else） |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | 空值判断（null if/else） |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | 如果 expr1 = expr2 则返回 `NULL` |

**类型转换函数：**

| 名称 | 描述 |
| :------------------------------------------------------------------------------------------ | :----------------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast) | 将值转换为字符串或向量 |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | 将值转换为字符串 |

关于如何使用 `CAST()` 的详细信息，请参见 [Vector Data Type | Cast](/vector-search/vector-search-data-types.md#cast)。

## 完整参考

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [L2 距离](https://en.wikipedia.org/wiki/Euclidean_distance)（欧几里得距离）：

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

两个向量的维度必须相同，否则会返回错误。

示例：

```sql
[tidb]> SELECT VEC_L2_DISTANCE('[0,3]', '[4,0]');
+-----------------------------------+
| VEC_L2_DISTANCE('[0,3]', '[4,0]') |
+-----------------------------------+
|                                 5 |
+-----------------------------------+
```

### VEC_COSINE_DISTANCE

```sql
VEC_COSINE_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [余弦距离](https://en.wikipedia.org/wiki/Cosine_similarity)：

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

两个向量的维度必须相同，否则会返回错误。

示例：

```sql
[tidb]> SELECT VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]');
+-------------------------------------------+
| VEC_COSINE_DISTANCE('[1, 1]', '[-1, -1]') |
+-------------------------------------------+
|                                         2 |
+-------------------------------------------+
```

### VEC_NEGATIVE_INNER_PRODUCT

```sql
VEC_NEGATIVE_INNER_PRODUCT(vector1, vector2)
```

通过使用两个向量的内积的负值计算距离，公式如下：

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

两个向量的维度必须相同，否则会返回错误。

示例：

```sql
[tidb]> SELECT VEC_NEGATIVE_INNER_PRODUCT('[1,2]', '[3,4]');
+----------------------------------------------+
| VEC_NEGATIVE_INNER_PRODUCT('[1,2]', '[3,4]') |
+----------------------------------------------+
|                                          -11 |
+----------------------------------------------+
```

### VEC_L1_DISTANCE

```sql
VEC_L1_DISTANCE(vector1, vector2)
```

使用以下公式计算两个向量之间的 [L1 距离](https://en.wikipedia.org/wiki/Taxicab_geometry)（曼哈顿距离）：

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

两个向量的维度必须相同，否则会返回错误。

示例：

```sql
[tidb]> SELECT VEC_L1_DISTANCE('[0,0]', '[3,4]');
+-----------------------------------+
| VEC_L1_DISTANCE('[0,0]', '[3,4]') |
+-----------------------------------+
|                                 7 |
+-----------------------------------+
```

### VEC_DIMS

```sql
VEC_DIMS(vector)
```

返回向量的维度。

示例：

```sql
[tidb]> SELECT VEC_DIMS('[1,2,3]');
+---------------------+
| VEC_DIMS('[1,2,3]') |
+---------------------+
|                   3 |
+---------------------+

[tidb]> SELECT VEC_DIMS('[]');
+----------------+
| VEC_DIMS('[]') |
+----------------+
|              0 |
+----------------+
```

### VEC_L2_NORM

```sql
VEC_L2_NORM(vector)
```

使用以下公式计算向量的 [L2 范数](https://en.wikipedia.org/wiki/Norm_(mathematics))（欧几里得范数）：

$NORM(p)=\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}$

示例：

```sql
[tidb]> SELECT VEC_L2_NORM('[3,4]');
+----------------------+
| VEC_L2_NORM('[3,4]') |
+----------------------+
|                    5 |
+----------------------+
```

### VEC_FROM_TEXT

```sql
VEC_FROM_TEXT(string)
```

将字符串转换为向量。

示例：

```sql
[tidb]> SELECT VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]');
+-------------------------------------------------+
| VEC_FROM_TEXT('[1,2]') + VEC_FROM_TEXT('[3,4]') |
+-------------------------------------------------+
| [4,6]                                           |
+-------------------------------------------------+
```

### VEC_AS_TEXT

```sql
VEC_AS_TEXT(vector)
```

将向量转换为字符串。

示例：

```sql
[tidb]> SELECT VEC_AS_TEXT('[1.000,   2.5]');
+-------------------------------+
| VEC_AS_TEXT('[1.000,   2.5]') |
+-------------------------------+
| [1,2.5]                       |
+-------------------------------+
```

## MySQL 兼容性

向量函数以及对向量数据类型的扩展内置函数和操作符仅在 TiDB 中支持，不支持 MySQL。

## 另请参见

- [Vector Data Types](/vector-search/vector-search-data-types.md)
