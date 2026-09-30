---
title: PostgreSQL Limits and Constraints
summary: Learn about SQL engine limits and constraints for PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Limits and Constraints

This document describes SQL engine limits and constraints that apply to PostgreSQL-compatible {{{ .starter }}}.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in limited public preview. Limits and constraints might change during the preview.

This page focuses on SQL engine behavior. For the monthly free quota and product-level limits of PostgreSQL-compatible {{{ .starter }}}, see [TiDB Cloud Starter plan documentation](/tidb-cloud/select-cluster-tier.md#postgresql-compatible-starter).

## Engine limits

The following limits apply:

| Resource | Limit |
| --- | --- |
| Statement timeout | 60 seconds by default |
| Idle transaction timeout | 600 seconds (10 minutes) by default |
| View nesting depth | 64 levels |
| Pending portals per connection | 32 |
| Identifier length | 63 bytes |
| Encoding | UTF-8 only |

The statement timeout can be changed for the current session.

For example:

```sql
SET statement_timeout = '120s';
```

Set it to `0` to disable the timeout for the current session:

```sql
SET statement_timeout = 0;
```

## Character encoding

PostgreSQL-compatible {{{ .starter }}} stores text in UTF-8.

The server encoding is reported as:

```sql
SHOW server_encoding;
```

The result is:

```text
UTF8
```

Make sure imported text data is valid UTF-8.

## Identifier length

PostgreSQL-compatible identifiers are limited to 63 bytes.

You can view the limit using:

```sql
SHOW max_identifier_length;
```

For portability, keep schema, table, column, index, constraint, function, and role names within this limit.

## Recursive CTE limit

Recursive common table expressions are limited to 1,000 iterations.

For example:

```sql
WITH RECURSIVE numbers AS (
    SELECT 1 AS n

    UNION ALL

    SELECT n + 1
    FROM numbers
    WHERE n < 100
)
SELECT *
FROM numbers;
```

## Array constraints

One-dimensional arrays are supported.

Multi-dimensional PostgreSQL arrays are not supported.

For example:

```sql
CREATE TABLE articles (
    id BIGSERIAL PRIMARY KEY,
    tags TEXT[]
);
```

## COPY constraints

The PostgreSQL `COPY` protocol supports text and CSV data.

| COPY capability | Support |
| --- | --- |
| Table-form `COPY FROM` | Supported |
| Table-form `COPY TO STDOUT` | Supported |
| Text format | Supported |
| CSV format | Supported |
| Binary format | Not supported |
| `COPY (SELECT ...) TO STDOUT` | Not supported |

For local files, use the `psql` `\copy` command so that the client reads the file and transfers the data through the PostgreSQL connection.

## Transaction constraints

The default isolation level is `READ COMMITTED`.

`REPEATABLE READ` is supported.

`READ UNCOMMITTED` behaves as `READ COMMITTED`.

PostgreSQL Serializable Snapshot Isolation is not supported. If `SERIALIZABLE` is requested over the PostgreSQL wire protocol, the effective isolation level is `REPEATABLE READ`.

`DEFERRABLE` transaction semantics are not supported.

## Index constraints

The supported index access methods are:

- B-tree
- GIN
- HNSW

The following PostgreSQL index access methods are not supported:

- GiST
- Hash
- SP-GiST
- BRIN

## HNSW constraints

HNSW indexes have additional requirements.

In particular:

- An HNSW index contains one vector column.
- The indexed column must declare an explicit vector dimension, such as `VECTOR(1024)`.
- The table must have a single-column primary key. If the primary key is `INTEGER` or `BIGINT`, its values must be non-negative.
- Partial HNSW indexes are not supported.
- The query must use a compatible distance operator and query shape for the optimizer to use the HNSW index.

Queries that do not meet the HNSW planning requirements fall back to an exact scan.

## Full-text search constraints

PostgreSQL-compatible full-text search has the following notable constraints:

- Only the documented text search configurations are supported.
- Prefix matching with the `:*` flag is not supported.
- `ts_headline()` does not highlight Chinese Han-script terms.
- The maximum `TSVECTOR` value size is 1 MiB.

## PL/pgSQL constraints

PL/pgSQL supports common variables, conditionals, `FOR` loops, dynamic SQL, `SELECT ... INTO`, DML `RETURNING ... INTO`, and other common constructs.

The following constructs are not supported:

- `WHILE`
- `FOREACH`
- Cursor operations
- `REFCURSOR`

Exception handlers and nested procedural blocks are supported only in `DO` blocks.

`BEFORE` trigger functions have additional procedural limitations.

## Trigger constraints

Supported trigger timing:

- `BEFORE`
- `AFTER`

Supported events:

- `INSERT`
- `UPDATE`
- `DELETE`

`FOR EACH STATEMENT` is accepted but currently executes with per-row behavior. Use `FOR EACH ROW` when you need predictable trigger semantics.

## Sequence constraints

Sequence options such as the following can be specified when a sequence is created:

- `START`
- `INCREMENT`
- `MINVALUE`
- `MAXVALUE`
- `CACHE`
- `CYCLE`

`ALTER SEQUENCE` supports ownership operations but does not support changing these generation options after the sequence is created.

Use `setval()` to reposition an existing sequence.

## Custom type constraints

Enum and composite types are supported with compatibility differences. Composite types can be declared and written using text literals, but their fields cannot be read individually.

For enum types, comparison and ordering use label text rather than declaration order.

If application logic depends on enum order, use an explicit rank instead of relying on enum comparison order.

## Collation constraints

Custom collations are supported with the following limitations:

- The specified locale does not select distinct locale-specific behavior.
- Text without an explicit custom collation uses bytewise ordering.
- Aggregate and window `ORDER BY` expressions do not apply custom collation ordering.
- Custom collations are not fully represented in the PostgreSQL system catalogs.

## System catalog constraints

The PostgreSQL-compatible system catalog is intended for common introspection workflows but is not identical to upstream PostgreSQL.

In particular:

- Not every upstream system catalog relation or view is available.
- Some system catalog relations expose a subset of upstream PostgreSQL columns.
- Some catalog objects can exist for compatibility even when the corresponding PostgreSQL feature is unsupported.
- `information_schema.views` is not available.

## Extension limits

Extensions and built-in capabilities can have their own limits.

For example:

- Vector search has HNSW index and query-shape constraints.
- Full-text search has tokenizer and query constraints.
- Parquet import supports only documented URL schemes and type mappings.
- Only extensions explicitly provided by TiDB Cloud are supported.
