---
title: Vector Data Types
summary: Learn about the Vector data types in TiDB.
---

# Vector Type

TiDB provides Vector data type specifically optimized for AI Vector Embedding use cases. By using the Vector data type, you can store and query a sequence of floating numbers efficiently, such as `[0.3, 0.5, -0.1, ...]`.

The following Vector data type is currently available:

- `VECTOR`: A sequence of single-precision floating numbers. The dimensions can be different for each row.
- `VECTOR(D)`: A sequence of single-precision floating numbers with a fixed dimension `D`.

The Vector data type provides these advantages over storing in a `JSON` column:

- Vector Index support. A [Vector Search Index] can be built to speed up vector searching.
- Dimension enforcement. A dimension can be specified to forbid inserting vectors with different dimensions.
- Optimized storage format. Vector data types is stored even more space-efficient than `JSON` data type.

> **Note:**
>
> Vector data types are only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## Value Syntax

A Vector value contains arbitrary number of floating numbers. You can use a string in the following syntax to represent a Vector value:

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

As dimension 3 is enforced for the `embedding` column in the example above, inserting a vector with a different dimension will result in an error:

```sql
[tidb]> INSERT INTO vector_table VALUES (4, '[0.3, 0.5]');
ERROR 1105 (HY000): vector has 2 dimensions, does not fit VECTOR(3)
```

See [Vector Functions and Operators] for available functions and operators over the Vector data type.

See [Vector Search Index] for building and using a vector search index.

## Vectors with Different Dimensions

You can store vectors with different dimensions in the same column by omitting the dimension parameter in the `VECTOR` type:

```sql
CREATE TABLE vector_table (
    id INT PRIMARY KEY,
    embedding VECTOR
);

INSERT INTO vector_table VALUES (1, '[0.3, 0.5, -0.1]'); -- 3 dimensions vector, OK
INSERT INTO vector_table VALUES (2, '[0.3, 0.5]');       -- 2 dimensions vector, OK
```

However you cannot build a [Vector Search Index] for this column, as vector distances can be only calculated between vectors with the same dimensions.

## Cast

### Cast between Vector ⇔ String

To cast between Vector and String, use the following functions:

- `CAST(... AS VECTOR)`: String ⇒ Vector
- `CAST(... AS CHAR)`: Vector ⇒ String
- `VEC_FROM_TEXT`: String ⇒ Vector
- `VEC_AS_TEXT`: Vector ⇒ String

There are implicit casts when calling functions receiving vector data types:

```sql
-- Examples below are the same:

[tidb]> SELECT VEC_DIMS('[0.3, 0.5, -0.1]');
+------------------------------+
| VEC_DIMS('[0.3, 0.5, -0.1]') |
+------------------------------+
|                            3 |
+------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]'));
+---------------------------------------------+
| VEC_DIMS(VEC_FROM_TEXT('[0.3, 0.5, -0.1]')) |
+---------------------------------------------+
|                                           3 |
+---------------------------------------------+
1 row in set (0.01 sec)

[tidb]> SELECT VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR));
+----------------------------------------------+
| VEC_DIMS(CAST('[0.3, 0.5, -0.1]' AS VECTOR)) |
+----------------------------------------------+
|                                            3 |
+----------------------------------------------+
1 row in set (0.01 sec)
```

However in arithmetic operations, you need to cast explicitly because the operator accepts any data type so that no implicit cast is applied:

```sql
[tidb]> SELECT '[0.1]'+'[0.2]';
+-----------------+
| '[0.1]'+'[0.2]' |
+-----------------+
|               0 |
+-----------------+
1 row in set, 2 warnings (0.01 sec)

[tidb]> SELECT VEC_FROM_TEXT('[0.1]')+VEC_FROM_TEXT('[0.2]');
+-----------------------------------------------+
| VEC_FROM_TEXT('[0.1]')+VEC_FROM_TEXT('[0.2]') |
+-----------------------------------------------+
| [0.3]                                         |
+-----------------------------------------------+
1 row in set (0.01 sec)

```

To cast vector into its string representation explicitly, use `VEC_AS_TEXT` function:

```sql
[tidb]> SELECT VEC_AS_TEXT('[0.3,     0.5,  -0.1]');
+--------------------------------------+
| VEC_AS_TEXT('[0.3,     0.5,  -0.1]') |
+--------------------------------------+
| [0.3,0.5,-0.1]                       |
+--------------------------------------+
1 row in set (0.01 sec)
```

See [Vector Functions and Operators] for more information.

### Cast between Vector ⇔ Other Data Types

It is currently not possible to cast between Vector and other data types (like `JSON`) directly. You need to use String as an intermediate type.

## Restrictions

- The maximum supported Vector dimension is 16000.
- You cannot store `NaN`, `Infinity`, `-Infinity` values in the vector data type.
- Currently Vector data types cannot store double-precision floating numbers. This will be supported in future release.

For other limitations, see [Vector Search Limitations].

## MySQL Compatibility

Vector data types are TiDB specific, and are not supported in MySQL.

## See Also

- [Vector Functions and Operators]
- [Vector Search Index]
- [Improve Vector Search Performance]

[Vector Functions and Operators]: /tidb-cloud/vector-search-functions-and-operators.md
[Vector Search Index]: /tidb-cloud/vector-search-index.md
[Improve Vector Search Performance]: /tidb-cloud/vector-search-improve-performance.md
[Vector Search Limitations]: /tidb-cloud/vector-search-limitations.md
