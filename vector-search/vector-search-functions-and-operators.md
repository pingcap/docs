---
title: Vector Functions and Operators
summary: Learn about functions and operators available for Vector data types.
---

# Vector Functions and Operators

This document lists the functions and operators available for Vector data types.

<CustomContent platform="tidb">

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> Vector data types and these vector functions are only available for TiDB Self-Managed clusters and [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

## Vector functions

The following functions are designed specifically for [Vector data types](/vector-search/vector-search-data-types.md).

**Vector distance functions:**

| Function Name                                             | Description                                                      |
| --------------------------------------------------------- | ---------------------------------------------------------------- |
| [`VEC_L2_DISTANCE`](#vec_l2_distance)                       | Calculates L2 distance (Euclidean distance) between two vectors  |
| [`VEC_COSINE_DISTANCE`](#vec_cosine_distance)               | Calculates the cosine distance between two vectors               |
| [`VEC_NEGATIVE_INNER_PRODUCT`](#vec_negative_inner_product) | Calculates the negative of the inner product between two vectors |
| [`VEC_L1_DISTANCE`](#vec_l1_distance)                       | Calculates L1 distance (Manhattan distance) between two vectors  |

**Other vector functions:**

| Function Name                   | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| [`VEC_DIMS`](#vec_dims)           | Returns the dimension of a vector                   |
| [`VEC_L2_NORM`](#vec_l2_norm)     | Calculates the L2 norm (Euclidean norm) of a vector |
| [`VEC_FROM_TEXT`](#vec_from_text) | Converts a string into a vector                     |
| [`VEC_AS_TEXT`](#vec_as_text)     | Converts a vector into a string                     |

## Extended built-in functions and operators

The following built-in functions and operators are extended to support operations on [Vector data types](/vector-search/vector-search-data-types.md).

**Arithmetic operators:**

| Name                                                                                    | Description                              |
| :-------------------------------------------------------------------------------------- | :--------------------------------------- |
| [`+`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_plus)  | Vector element-wise addition operator    |
| [`-`](https://dev.mysql.com/doc/refman/8.0/en/arithmetic-functions.html#operator_minus) | Vector element-wise subtraction operator |

For more information about how vector arithmetic works, see [Vector Data Type | Arithmetic](/vector-search/vector-search-data-types.md#arithmetic).

**Aggregate (GROUP BY) functions:**

| Name                              | Description                                      |
| :----------------------- | :----------------------------------------------- |
| [`COUNT()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count)                  | Return a count of the number of rows returned    |
| [`COUNT(DISTINCT)`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_count-distinct) | Return the count of a number of different values |
| [`MAX()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_max)                      | Return the maximum value                         |
| [`MIN()`](https://dev.mysql.com/doc/refman/8.0/en/aggregate-functions.html#function_min)                      | Return the minimum value                         |

**Comparison functions and operators:**

| Name                                  | Description                                           |
| ---------------------------------------- | ----------------------------------------------------- |
| [`BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_between)         | Check whether a value is within a range of values     |
| [`COALESCE()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_coalesce)                 | Return the first non-NULL argument                    |
| [`=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal)                             | Equal operator                                        |
| [`<=>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_equal-to)                        | NULL-safe equal to operator                           |
| [`>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than)                      | Greater than operator                                 |
| [`>=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_greater-than-or-equal)            | Greater than or equal operator                        |
| [`GREATEST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_greatest)                 | Return the largest argument                           |
| [`IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_in)                             | Check whether a value is within a set of values       |
| [`IS NULL`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_is-null)                     | Test whether a value is `NULL`                                     |
| [`ISNULL()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_isnull)                     | Test whether the argument is `NULL`                     |
| [`LEAST()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#function_least)                       | Return the smallest argument                          |
| [`<`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than)                         | Less than operator                                    |
| [`<=`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_less-than-or-equal)               | Less than or equal operator                           |
| [`NOT BETWEEN ... AND ...`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-between) | Check whether a value is not within a range of values |
| [`!=`, `<>`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-equal)                  | Not equal operator                                    |
| [`NOT IN()`](https://dev.mysql.com/doc/refman/8.0/en/comparison-operators.html#operator_not-in)                     | Check whether a value is not within a set of values   |

For more information about how vectors are compared, see [Vector Data Type | Comparison](/vector-search/vector-search-data-types.md#comparison).

**Control flow functions:**

| Name                                                                                              | Description                  |
| :------------------------------------------------------------------------------------------------ | :--------------------------- |
| [`CASE`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#operator_case)       | Case operator                |
| [`IF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_if)         | If/else construct            |
| [`IFNULL()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_ifnull) | Null if/else construct       |
| [`NULLIF()`](https://dev.mysql.com/doc/refman/8.0/en/flow-control-functions.html#function_nullif) | Return `NULL` if expr1 = expr2 |

**Cast functions:**

| Name                                                                                        | Description                    |
| :------------------------------------------------------------------------------------------ | :----------------------------- |
| [`CAST()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_cast)       | Cast a value as a string or vector |
| [`CONVERT()`](https://dev.mysql.com/doc/refman/8.0/en/cast-functions.html#function_convert) | Cast a value as a string |

For more information about how to use `CAST()`, see [Vector Data Type | Cast](/vector-search/vector-search-data-types.md#cast).

## Full references

### VEC_L2_DISTANCE

```sql
VEC_L2_DISTANCE(vector1, vector2)
```

Calculates the [L2 distance](https://en.wikipedia.org/wiki/Euclidean_distance) (Euclidean distance) between two vectors using the following formula:

$DISTANCE(p,q)=\sqrt {\sum \limits _{i=1}^{n}{(p_{i}-q_{i})^{2}}}$

The two vectors must have the same dimension. Otherwise, an error is returned.

Example:

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

Calculates the [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity) between two vectors using the following formula:

$DISTANCE(p,q)=1.0 - {\frac {\sum \limits _{i=1}^{n}{p_{i}q_{i}}}{{\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}}\cdot {\sqrt {\sum \limits _{i=1}^{n}{q_{i}^{2}}}}}}$

The two vectors must have the same dimension. Otherwise, an error is returned.

Example:

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

Calculates the distance by using the negative of the [inner product](https://en.wikipedia.org/wiki/Dot_product) between two vectors, using the following formula:

$DISTANCE(p,q)=- INNER\_PROD(p,q)=-\sum \limits _{i=1}^{n}{p_{i}q_{i}}$

The two vectors must have the same dimension. Otherwise, an error is returned.

Example:

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

Calculates the [L1 distance](https://en.wikipedia.org/wiki/Taxicab_geometry) (Manhattan distance) between two vectors using the following formula:

$DISTANCE(p,q)=\sum \limits _{i=1}^{n}{|p_{i}-q_{i}|}$

The two vectors must have the same dimension. Otherwise, an error is returned.

Example:

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

Returns the dimension of a vector.

Examples:

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

Calculates the [L2 norm](https://en.wikipedia.org/wiki/Norm_(mathematics)) (Euclidean norm) of a vector using the following formula:

$NORM(p)=\sqrt {\sum \limits _{i=1}^{n}{p_{i}^{2}}}$

Example:

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

Converts a string into a vector.

Example:

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

Converts a vector into a string.

Example:

```sql
[tidb]> SELECT VEC_AS_TEXT('[1.000,   2.5]');
+-------------------------------+
| VEC_AS_TEXT('[1.000,   2.5]') |
+-------------------------------+
| [1,2.5]                       |
+-------------------------------+
```

## MySQL compatibility

The vector functions and the extended usage of built-in functions and operators over vector data types are TiDB specific, and are not supported in MySQL.

## See also

- [Vector Data Types](/vector-search/vector-search-data-types.md)
