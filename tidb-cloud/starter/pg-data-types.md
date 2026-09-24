---
title: PostgreSQL Data Types
summary: Learn about the PostgreSQL-compatible data types supported by PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Data Types

PostgreSQL-compatible {{{ .starter }}} supports common PostgreSQL data types for numeric, text, binary, date and time, JSON, array, vector, and full-text search workloads.

## Supported data types

The following data types are supported:

| Data type | Aliases | Description |
| --- | --- | --- |
| `BOOLEAN` | `BOOL` | Boolean value. |
| `INTEGER` | `INT`, `INT4` | 4-byte signed integer. |
| `BIGINT` | `INT8` | 8-byte signed integer. |
| `DOUBLE PRECISION` | `FLOAT8` | 8-byte IEEE 754 floating-point number. |
| `NUMERIC` | `NUMERIC(p,s)`, `DECIMAL` | Exact numeric value with optional precision and scale. |
| `TEXT` | - | Variable-length UTF-8 text. |
| `VARCHAR(n)` | `CHARACTER VARYING(n)` | Variable-length text with a maximum length of `n` characters. |
| `BYTEA` | - | Binary data. |
| `TIMESTAMP` | `TIMESTAMP WITHOUT TIME ZONE` | Date and time without a time zone. |
| `TIMESTAMPTZ` | `TIMESTAMP WITH TIME ZONE` | Date and time with time zone semantics. |
| `DATE` | - | Calendar date. |
| `TIME` | `TIME WITHOUT TIME ZONE` | Time of day. |
| `INTERVAL` | - | Time interval. |
| `UUID` | - | 128-bit UUID value. |
| `INET` | - | IPv4 or IPv6 host or network address. |
| `JSON` | - | JSON data that preserves the input text representation. |
| `JSONB` | - | JSON data stored in a canonical representation. |
| `SERIAL` | - | Auto-incrementing 4-byte integer backed by a sequence. |
| `BIGSERIAL` | - | Auto-incrementing 8-byte integer backed by a sequence. |
| `type[]` | - | Array of a supported data type. |
| `VECTOR(n)` | - | Fixed-dimension dense vector for vector search. |
| `TSVECTOR` | - | Full-text search document representation. |
| `TSQUERY` | - | Full-text search query representation. |
| `NAME` | - | PostgreSQL-compatible identifier type used by system catalogs. |

The following common PostgreSQL types are not supported:

- `SMALLINT` and `INT2`: use `INTEGER` instead.
- `REAL` and `FLOAT4`: use `DOUBLE PRECISION` instead.
- `CHAR(n)` and `CHARACTER(n)`: use `VARCHAR(n)` instead.

## Numeric types

Use `INTEGER` or `BIGINT` for integer values:

```sql
CREATE TABLE counters (
    id BIGSERIAL PRIMARY KEY,
    count INTEGER NOT NULL,
    total BIGINT
);
```

Use `NUMERIC` when exact decimal values are required:

```sql
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    price NUMERIC(10, 2)
);
```

Use `DOUBLE PRECISION` for floating-point values:

```sql
CREATE TABLE measurements (
    id BIGSERIAL PRIMARY KEY,
    value DOUBLE PRECISION
);
```

## Character and binary types

Use `TEXT` for variable-length text:

```sql
CREATE TABLE documents (
    id BIGSERIAL PRIMARY KEY,
    title TEXT,
    body TEXT
);
```

Use `VARCHAR(n)` when you want to enforce a maximum character length:

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(64) NOT NULL
);
```

Use `BYTEA` to store binary data:

```sql
CREATE TABLE files (
    id BIGSERIAL PRIMARY KEY,
    content BYTEA
);
```

## Date and time types

PostgreSQL-compatible {{{ .starter }}} supports `DATE`, `TIME`, `TIMESTAMP`, `TIMESTAMPTZ`, and `INTERVAL`.

For example:

```sql
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_date DATE,
    start_time TIME,
    created_at TIMESTAMP,
    published_at TIMESTAMPTZ,
    duration INTERVAL
);
```

Use PostgreSQL typed literals when needed:

```sql
SELECT
    DATE '2026-09-19',
    TIME '15:30:00',
    TIMESTAMP '2026-09-19 15:30:00',
    TIMESTAMPTZ '2026-09-19 15:30:00+00',
    INTERVAL '2 hours';
```

### Timestamp precision

Timestamps are stored with microsecond precision.

Precision parameters from 0 to 6 are accepted in the type syntax, but they do not truncate the stored fractional seconds.

For example, `TIMESTAMP(3)` can still preserve six fractional digits.

## Interval operations

Intervals preserve month-based and sub-month components separately, which enables calendar-aware date arithmetic.

You can add, subtract, multiply, divide, and negate intervals:

```sql
SELECT
    INTERVAL '1 day' * 2 AS two_days,
    2 * INTERVAL '1 day' AS two_days_again,
    INTERVAL '1 day' / 2 AS half_day,
    INTERVAL '1 day' + INTERVAL '1 hour' AS day_and_hour,
    INTERVAL '3 days' - INTERVAL '1 day' AS two_days,
    -INTERVAL '1 day' AS negative_day,
    NOW() - 7 * INTERVAL '1 day' AS one_week_ago;
```

## UUID

Use `UUID` to store 128-bit UUID values:

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    user_id BIGINT NOT NULL
);
```


## INET

Use `INET` to store IPv4 or IPv6 host or network addresses:

```sql
CREATE TABLE access_log (
    id BIGSERIAL PRIMARY KEY,
    client_ip INET
);
```

For example:

```sql
INSERT INTO access_log (client_ip)
VALUES
    ('192.168.1.10'),
    ('10.0.0.0/8'),
    ('::1');
```

Equality and ordering comparisons are supported. Some PostgreSQL network operators and functions are not supported. See [PostgreSQL Compatibility](/tidb-cloud/starter/postgresql-compatibility.md).

## JSON and JSONB

Use `JSON` when preserving the original JSON text representation is important. Use `JSONB` for a canonical representation and operations such as JSON containment.

For example:

```sql
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    settings JSONB
);

INSERT INTO profiles (settings)
VALUES ('{"theme":"dark","notifications":true}');

SELECT *
FROM profiles
WHERE settings @> '{"theme":"dark"}';
```

## Arrays

Use `type[]` to define an array:

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

Insert and access array values:

```sql
INSERT INTO articles (tags)
VALUES (ARRAY['database', 'cloud', 'postgresql']);

SELECT tags[1]
FROM articles;
```


## Vector and full-text search types

`VECTOR(n)` is available for vector search:

```sql
CREATE TABLE embeddings (
    id BIGSERIAL PRIMARY KEY,
    embedding VECTOR(3)
);
```

For vector operators and HNSW indexes, see [Vector Search](/tidb-cloud/starter/pg-vector-search.md).

`TSVECTOR` and `TSQUERY` are available for PostgreSQL-compatible full-text search:

```sql
SELECT
    to_tsvector('simple', 'PostgreSQL full text search')
    @@ plainto_tsquery('simple', 'PostgreSQL');
```

For more information, see [Full-Text Search](/tidb-cloud/starter/pg-full-text-search.md).

## Type coercion

PostgreSQL-compatible {{{ .starter }}} supports PostgreSQL-style type coercion in common SQL contexts.

### `UNION`, `CASE`, `COALESCE`, and `VALUES`

When text is combined with another typed value, the expression can resolve to text.

For example:

```sql
SELECT 1
UNION
SELECT 'a';
```

### Comparisons

When a text literal is compared with a typed value, the text literal is coerced to the type of the other operand when possible.

For example:

```sql
CREATE TABLE example (
    id INTEGER PRIMARY KEY
);

SELECT *
FROM example
WHERE id = '42';
```

In this example, `'42'` is coerced to `INTEGER`.

### Numeric type promotion

When numeric types are combined, the result is promoted according to the following general precedence:

```text
INTEGER -> BIGINT -> DOUBLE PRECISION -> NUMERIC
```

### Temporal type promotion

Common temporal expressions are promoted as follows:

| Expression types | Result type |
| --- | --- |
| `DATE` and `TIMESTAMP` | `TIMESTAMP` |
| `TIMESTAMP` and `TIMESTAMPTZ` | `TIMESTAMPTZ` |
| `DATE` and `TIMESTAMPTZ` | `TIMESTAMPTZ` |

## Type casts

Use either PostgreSQL cast syntax:

```sql
SELECT CAST('42' AS INTEGER);
SELECT '42'::INTEGER;
```

Explicit casts are more permissive than assignment and implicit casts. For example, explicit casts can perform some conversions that an `INSERT` or `UPDATE` assignment rejects.