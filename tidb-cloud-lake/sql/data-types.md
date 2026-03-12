---
title: Data Types
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.100"/>

Databend stores data in strongly typed columns. This page summarizes the supported data types, how automatic/explicit conversions work, and what happens with NULL or default values.

## Foundational Types

| Data Type                                   | Alias      | Storage / Resolution              | Min Value                | Max Value                      |
|--------------------------------------------|------------|-----------------------------------|--------------------------|--------------------------------|
| [BOOLEAN](boolean.md)                      | BOOL       | 1 byte                            | –                        | –                              |
| [BINARY](binary.md)                        | VARBINARY  | variable                          | –                        | –                              |
| [VARCHAR](string.md)                       | STRING     | variable                          | –                        | –                              |
| [TINYINT](numeric.md#integer-data-types)   | INT8       | 1 byte                            | -128                     | 127                            |
| [SMALLINT](numeric.md#integer-data-types)  | INT16      | 2 bytes                           | -32768                   | 32767                          |
| [INT](numeric.md#integer-data-types)       | INT32      | 4 bytes                           | -2147483648              | 2147483647                     |
| [BIGINT](numeric.md#integer-data-types)    | INT64      | 8 bytes                           | -9223372036854775808     | 9223372036854775807            |
| [FLOAT](numeric.md#floating-point-data-types) | –        | 4 bytes (Float32)                | -3.40e38                 | 3.40e38                        |
| [DOUBLE](numeric.md#floating-point-data-types) | –       | 8 bytes (Float64)                | -1.79e308                | 1.79e308                       |
| [DECIMAL](decimal.md)                      | –          | 16/32 bytes (precision ≤38/76)    | `-(10^P-1)/10^S`         | `(10^P-1)/10^S`                |

## Date & Time Types

| Data Type                 | Alias     | Resolution / Notes                   |
|---------------------------|-----------|--------------------------------------|
| [DATE](datetime.md)       | –         | Day precision                        |
| [TIMESTAMP](datetime.md)  | DATETIME  | Microsecond, session timezone output |
| [TIMESTAMP_TZ](datetime.md) | –       | Microsecond + stored offset          |
| [INTERVAL](interval.md)   | –         | Microseconds, supports negative span |

## Structured & Semi-Structured Types

| Data Type             | Sample                                | Description |
|-----------------------|----------------------------------------|-------------|
| [ARRAY](array.md)     | `[1, 2, 3]`                            | Ordered list of values with the same inner type. |
| [TUPLE](tuple.md)     | `('2023-02-14','Valentine's Day')`     | Fixed-length ordered list with declared element types. |
| [MAP](map.md)         | `{'a': 1, 'b': 2}`                     | Key-value collection (internally tuples of key and value types). |
| [VARIANT](variant.md) | `[1, {"name":"databend"}]`             | JSON-like container that can mix primitives, arrays, and objects. |
| [BITMAP](bitmap.md)   | `<bitmap binary>`                      | Compressed bitmap optimized for membership and set operations. |

## Domain-Specific Types

| Data Type                           | Description |
|------------------------------------|-------------|
| [VECTOR](vector.md)                | Float32 embeddings for similarity search / ML workloads. |
| [GEOMETRY](geospatial.md) / GEOGRAPHY | Spatial objects stored in WKB/EWKB format. |

## Casting and Conversion

### Explicit Casting

- `CAST(expr AS TYPE)` uses ANSI syntax and fails when conversion is invalid.
- `expr::TYPE` is the PostgreSQL-style shorthand.
- `TRY_CAST(expr AS TYPE)` returns NULL instead of raising an error when conversion fails.

### Implicit Casting (Coercion)

Databend performs automatic conversions in well-defined situations:

1. Integers upcast to `INT64`. Example: `UInt8 -> INT64`.
2. Numeric values upcast to `FLOAT64` when necessary.
3. Any type `T` can become `Nullable(T)` if a NULL appears in an expression.
4. All types can upcast to `VARIANT`.
5. Complex types coerce element-wise (`Array<T> -> Array<U>` when `T -> U`; same for tuples/maps).

When a target column is `NOT NULL`, explicitly cast to `Nullable<T>` or use `TRY_CAST` if your data may contain NULLs.

```sql
SELECT CONCAT('1', col);      -- safe (strings)
SELECT CONCAT(1, col);        -- may fail if `col` can't coerce to number
```

## NULL Handling and Defaults

Columns allow NULL values unless declared `NOT NULL`. When a `NOT NULL` column is omitted during INSERT, Databend writes a type-specific default value:

| Type Category            | Default |
|--------------------------|---------|
| Integer                  | `0`     |
| Floating-point           | `0.0`   |
| String / Binary          | empty string / empty binary |
| Date                     | `1970-01-01` |
| Timestamp                | `1970-01-01 00:00:00` |
| Boolean                  | `FALSE` |

Example:

```sql
CREATE TABLE test (
    id   INT64,
    name STRING NOT NULL,
    age  INT32
);

INSERT INTO test (id, name, age) VALUES (2, 'Alice', NULL);  -- allowed
INSERT INTO test (id, name) VALUES (1, 'John');              -- age becomes NULL
INSERT INTO test (id, age) VALUES (3, 45);                   -- name uses default ''
```

Use `DESC test` or `SHOW CREATE TABLE test` to inspect column defaults and nullability at any time.
