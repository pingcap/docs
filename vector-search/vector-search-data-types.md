---
title: Vector Data Types
summary: Learn about the Vector data types in TiDB.
---

# Vector Data Types

A vector is a sequence of floating-point numbers, such as `[0.3, 0.5, -0.1, ...]`. TiDB offers Vector data types, specifically optimized for efficiently storing and querying vector embeddings widely used in AI applications.

<CustomContent platform="tidb">

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

</CustomContent>

> **Note:**
>
> Vector data types are only available for TiDB Self-Managed clusters and [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) clusters.

The following Vector data types are currently available:

- `VECTOR`: A sequence of single-precision floating-point numbers with any dimension.
- `VECTOR(D)`: A sequence of single-precision floating-point numbers with a fixed dimension `D`.

Using vector data types provides the following advantages over using the [`JSON`](/data-type-json.md) type:

- Vector index support: You can build a [vector search index](/vector-search-index.md) to speed up vector searching.
- Dimension enforcement: You can specify a dimension to forbid inserting vectors with different dimensions.
- Optimized storage format: Vector data types are optimized for handling vector data, offering better space efficiency and performance compared to `JSON` types.

## Syntax

You can use a string in the following syntax to represent a Vector value:

```sql
'[<float>, <float>, ...]'
```

Example:

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR(3)
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]');

INSERT INTO vector_table VALUES (2, NULL);
```

Inserting vector values with invalid syntax will result in an error:

```sql
[tidb]> INSERT INTO vector_table VALUES (3, '[5, ]');
ERROR 1105 (HY000): Invalid vector text: [5, ]
```

In the following example, because dimension `3` is enforced for the `embedding` column when the table is created, inserting a vector with a different dimension will result in an error:

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

For available functions and operators over the vector data types, see [Vector Functions and Operators](/vector-search-functions-and-operators.md).

For more information about building and using a vector search index, see [Vector Search Index](/vector-search-index.md).

## Store vectors with different dimensions

You can store vectors with different dimensions in the same column by omitting the dimension parameter in the `VECTOR` type:

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

However, note that you cannot build a [vector search index](/vector-search-index.md) for this column, as vector distances can be only calculated between vectors with the same dimensions.

## Comparison

You can compare vector data types using [comparison operators](/functions-and-operators/operators.md) such as `=`, `!=`, `<`, `>`, `<=`, and `>=`. For a complete list of comparison operators and functions for vector data types, see [Vector Functions and Operators](/vector-search-functions-and-operators.md).

Vector data types are compared element-wise numerically. For example:

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

Two vectors with different dimensions are compared using lexicographical comparison, with the following rules:

- Two vectors are compared element by element from the start, and each element is compared numerically.
- The first mismatching element determines which vector is lexicographically _less_ or _greater_ than the other.
- If one vector is a prefix of another, the shorter vector is lexicographically _less_ than the other. For example, `[1,2,3] < [1,2,3,0]`.
- Vectors of the same length with identical elements are lexicographically _equal_.
- An empty vector is lexicographically _less_ than any non-empty vector. For example, `[] < [1]`.
- Two empty vectors are lexicographically _equal_.

When comparing vector constants, consider performing an [explicit cast](#cast) from string to vector to avoid comparisons based on string values:

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

## Arithmetic

Vector data types support arithmetic operations `+` (addition) and `-` (subtraction). However, arithmetic operations between vectors with different dimensions are not supported and will result in an error.

Examples:

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
+-----------------------------------------------------+
| VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]') |
+-----------------------------------------------------+
| [1,1,1]                                             |
+-----------------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[1,2,3]');
ERROR 1105 (HY000): vectors have different dimensions: 1 and 3
```

## Cast

### Cast between Vector ⇔ String

To cast between Vector and String, use the following functions:

- `CAST(... AS VECTOR)`: String ⇒ Vector
- `CAST(... AS CHAR)`: Vector ⇒ String
- `VEC_FROM_TEXT`: String ⇒ Vector
- `VEC_AS_TEXT`: Vector ⇒ String

To improve usability, if you call a function that only supports vector data types, such as a vector correlation distance function, you can also just pass in a format-compliant string. TiDB automatically performs an implicit cast in this case.

```sql
-- The VEC_DIMS function only accepts VECTOR arguments, so you can directly pass in a string for an implicit cast.
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- You can also explicitly cast a string to a vector using VEC_FROM_TEXT and then pass the vector to the VEC_DIMS function.
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- You can also cast explicitly using CAST(... AS VECTOR):
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

When using an operator or function that accepts multiple data types, you need to explicitly cast the string type to the vector type before passing the string to that operator or function, because TiDB does not perform implicit casts in this case. For example, before performing comparison operations, you need to explicitly cast strings to vectors; otherwise, TiDB compares them as string values rather than as vector numeric values:

```sql
-- Because string is given, TiDB is comparing strings:
[tidb]> SELECT '[12.0]' < '[4.0]';
+--------------------+
| '[12.0]' < '[4.0]' |
+--------------------+
|                  1 |
+--------------------+
1 row in set (0.01 sec)

-- Cast to vector explicitly to compare by vectors:
[tidb]> SELECT VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]');
+--------------------------------------------------+
| VEC_FROM_TEXT('[12.0]') < VEC_FROM_TEXT('[4.0]') |
+--------------------------------------------------+
|                                                0 |
+--------------------------------------------------+
1 row in set (0.01 sec)
```

You can also explicitly cast a vector to its string representation. Take using the `VEC_AS_TEXT()` function as an example:

```sql
-- The string is first implicitly cast to a vector, and then the vector is explicitly cast to a string, thus returning a string in the normalized format:
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

For additional cast functions, see [Vector Functions and Operators](/vector-search-functions-and-operators.md).

### Cast between Vector ⇔ other data types

Currently, direct casting between Vector and other data types (such as `JSON`) is not supported. To work around this limitation, use String as an intermediate data type for casting in your SQL statement.

Note that vector data type columns stored in a table cannot be converted to other data types using `ALTER TABLE ... MODIFY COLUMN ...`.

## Restrictions

For restrictions on vector data types, see [Vector search limitations](/vector-search-limitations.md) and [Vector index restrictions](/vector-search-index.md#restrictions).

## MySQL compatibility

Vector data types are TiDB specific, and are not supported in MySQL.

## See also

- [Vector Functions and Operators](/vector-search-functions-and-operators.md)
- [Vector Search Index](/vector-search-index.md)
- [Improve Vector Search Performance](/vector-search-improve-performance.md)