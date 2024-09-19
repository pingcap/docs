---
title: Vector Data Types
summary: Learn about the Vector data types in TiDB.
---

# Vector Data Types

TiDB provides Vector data type specifically optimized for AI Vector Embedding use cases. By using the Vector data type, you can store and query a sequence of floating numbers efficiently, such as `[0.3, 0.5, -0.1, ...]`.

The following Vector data type is currently available:

- `VECTOR`: A sequence of single-precision floating numbers. The dimensions can be different for each row.
- `VECTOR(D)`: A sequence of single-precision floating numbers with a fixed dimension `D`.

The Vector data type provides these advantages over storing in a `JSON` column:

- Vector Index support. A [Vector Search Index](/tidb-cloud/vector-search-index.md) can be built to speed up vector searching.
- Dimension enforcement. A dimension can be specified to forbid inserting vectors with different dimensions.
- Optimized storage format. Vector data types are stored even more space-efficient than `JSON` data type.

> **Note:**
>
> Vector data types are only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Value syntax

A Vector value contains an arbitrary number of floating numbers. You can use a string in the following syntax to represent a Vector value:

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

As dimension 3 is enforced for the `embedding` column in the preceding example, inserting a vector with a different dimension will result in an error:

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

See [Vector Functions and Operators](/tidb-cloud/vector-search-functions-and-operators.md) for available functions and operators over the Vector data type.

See [Vector Search Index](/tidb-cloud/vector-search-index.md) for building and using a vector search index.

## Vectors with different dimensions

You can store vectors with different dimensions in the same column by omitting the dimension parameter in the `VECTOR` type:

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

However you cannot build a [Vector Search Index](/tidb-cloud/vector-search-index.md) for this column, as vector distances can be only calculated between vectors with the same dimensions.

## Comparison

You can compare vector data types using [comparison operators](/functions-and-operators/operators.md) such as `=`, `!=`, `<`, `>`, `<=`, and `>=`. For a complete list of comparison operators and functions for vector data types, see [Vector Functions and Operators](/tidb-cloud/vector-search-functions-and-operators.md).

Vector data types are compared element-wise numerically. Examples:

- `[1] < [12]`
- `[1,2,3] < [1,2,5]`
- `[1,2,3] = [1,2,3]`
- `[2,2,3] > [1,2,3]`

Vectors with different dimensions are compared using lexicographical comparison, with the following properties:

- Two vectors are compared element by element, and each element is compared numerically.
- The first mismatching element determines which vector is lexicographically _less_ or _greater_ than the other.
- If one vector is a prefix of another, the shorter vector is lexicographically _less_ than the other.
- Vectors of the same length with identical elements are lexicographically _equal_.
- An empty vector is lexicographically _less_ than any non-empty vector.
- Two empty vectors are lexicographically _equal_.

Examples:

- `[] < [1]`
- `[1,2,3] < [1,2,3,0]`

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

Vector data types support element-wise arithmetic operations `+` (addition) and `-` (subtraction). However, performing arithmetic operations between vectors with different dimensions results in an error.

Examples:

```sql
[tidb]> SELECT VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]');
+---------------------------------------------+
| VEC_FROM_TEXT('[4]') + VEC_FROM_TEXT('[5]') |
+---------------------------------------------+
| [9]                                         |
+---------------------------------------------+
1 row in set (0.01 sec)

mysql> SELECT VEC_FROM_TEXT('[2,3,4]') - VEC_FROM_TEXT('[1,2,3]');
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

There are implicit casts when calling functions receiving vector data types:

```sql
-- There is an implicit cast here, since VEC_DIMS only accepts VECTOR arguments:
[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using VEC_FROM_TEXT:
[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

-- Cast explicitly using CAST(... AS VECTOR):
[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

Use explicit casts when operators or functions accept multiple data types. For example, in comparisons, use explicit casts to compare vector numeric values instead of string values:

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

To cast vector into its string representation explicitly, use the `VEC_AS_TEXT()` function:

```sql
-- String representation is normalized:
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

For additional cast functions, see [Vector Functions and Operators](/tidb-cloud/vector-search-functions-and-operators.md).

### Cast between Vector ⇔ other data types

It is currently not possible to cast between Vector and other data types (like `JSON`) directly. You need to use String as an intermediate type.

## Restrictions

- The maximum supported Vector dimension is 16000.
- You cannot store `NaN`, `Infinity`, or `-Infinity` values in the vector data type.
- Currently, Vector data types cannot store double-precision floating point numbers. This is planned to be supported in a future release. In the meantime, if you import double-precision floating point numbers for Vector data types, they are converted to single-precision numbers.

For other limitations, see [Vector Search Limitations](/tidb-cloud/vector-search-limitations.md).

## MySQL compatibility

Vector data types are TiDB specific, and are not supported in MySQL.

## See also

- [Vector Functions and Operators](/tidb-cloud/vector-search-functions-and-operators.md)
- [Vector Search Index](/tidb-cloud/vector-search-index.md)
- [Improve Vector Search Performance](/tidb-cloud/vector-search-improve-performance.md)
