---
title: PostgreSQL Compatibility
summary: Learn about the compatibility of PostgreSQL-compatible TiDB Cloud Starter with PostgreSQL, including unsupported features and behavioral differences.
---

# PostgreSQL Compatibility

PostgreSQL-compatible {{{ .starter }}} instances support the PostgreSQL wire protocol (pgwire v3) and common PostgreSQL SQL syntax and application patterns. Most PostgreSQL clients, drivers, and ORMs can connect by using standard PostgreSQL connection strings.

However, the implementation is not identical to PostgreSQL. Some PostgreSQL features are not supported or behave differently, especially features that depend on PostgreSQL-specific storage, replication, extension, or transaction semantics.

> **Note:**
>
> This page describes general PostgreSQL compatibility for PostgreSQL-compatible {{{ .starter }}} instances. It does not apply to MySQL-compatible TiDB clusters.
>
> During the Limited Public Preview, compatibility coverage and behavior might continue to evolve. Before migrating a production workload, validate the PostgreSQL features that your application depends on.

## Supported features

PostgreSQL-compatible {{{ .starter }}} instances support the following PostgreSQL features:

+ **Wire protocol**: PostgreSQL wire protocol v3, including Simple Query and Extended Query (`Parse`/`Bind`/`Describe`/`Execute`).
+ **DDL**: `CREATE`, `ALTER`, and `DROP` for tables; B-tree, GIN, and HNSW indexes; views; materialized views; schemas; sequences; functions; triggers; types; and collations.
+ **DML**: `INSERT`, `UPDATE`, and `DELETE` with `RETURNING`, as well as `INSERT ... ON CONFLICT` (upsert).
+ **Queries**: joins (inner, left, right, full outer, cross, and lateral), common table expressions (CTEs), recursive CTEs, window functions, subqueries, and set operations (`UNION`, `INTERSECT`, and `EXCEPT`).
+ **Transactions**: `BEGIN`, `COMMIT`, `ROLLBACK`, savepoints, and autocommit.
+ **Data types**: Boolean, integer, bigint, double precision, numeric, text, varchar, bytea, timestamp/timestamptz, date, time, interval, UUID, JSON/JSONB, arrays, serial/bigserial, vector, tsvector, and tsquery.
+ **PL/pgSQL**: Functions, procedures, control flow, and dynamic `EXECUTE`, with some limitations. `WHILE`, `FOREACH`, and cursors are not supported. `EXCEPTION` and nested blocks require a `DO` block.
+ **Triggers**: `BEFORE` and `AFTER` triggers on `INSERT`, `UPDATE`, and `DELETE`, with some limitations. For details, see [PL/pgSQL](#plpgsql).
+ **Indexes**: B-tree (default), GIN, partial indexes, expression indexes, `CREATE INDEX CONCURRENTLY`, and HNSW vector indexes. GiST, Hash, SP-GiST, and BRIN indexes are not supported.

## Unsupported features

The following PostgreSQL features are not supported:

+ Table partitioning, including `RANGE`, `LIST`, and `HASH` partitioning.
+ Table inheritance.
+ Foreign data wrappers (FDW).
+ Tablespaces.
+ Rules created using `CREATE RULE`.
+ Logical replication.
+ Streaming replication.
+ True `SERIALIZABLE` isolation.
+ `DEFERRABLE` transactions.
+ PostgreSQL large objects (OID-based large object storage). Use `BYTEA` for binary data instead.
+ The `XML`, `CIDR`, and `MACADDR` data types.
+ PostgreSQL range types, except for partial support for `INT4RANGE`.
+ Procedural languages other than PL/pgSQL, such as PL/Python, PL/Perl, and PL/v8.
+ PL/pgSQL `WHILE` loops, `FOREACH` loops, and cursor operations.
+ Custom or third-party PostgreSQL extensions.

## Differences from PostgreSQL

### Transaction isolation

`READ COMMITTED` is the default transaction isolation level. `READ COMMITTED` and `REPEATABLE READ` are supported.

`READ UNCOMMITTED` behaves as `READ COMMITTED`, consistent with PostgreSQL behavior.

PostgreSQL Serializable Snapshot Isolation (SSI) is not supported. If you request `SERIALIZABLE` over the PostgreSQL wire protocol, the transaction is downgraded to `REPEATABLE READ` and a warning is returned.

For example:

```sql
BEGIN ISOLATION LEVEL SERIALIZABLE;
SHOW transaction_isolation;
```

The effective isolation level is `REPEATABLE READ`.

If your application relies on true serializability, use explicit row locking such as `SELECT ... FOR UPDATE` or database constraints to protect application invariants.

### Data types

Most commonly used PostgreSQL data types are supported, but the following types have compatibility differences:

| PostgreSQL type | Behavior |
| --- | --- |
| `SMALLINT` / `INT2` | Accepted, but stored internally as a 32-bit integer. |
| `REAL` / `FLOAT4` | Accepted, but stored internally as double precision. |
| `CHAR(n)` / `CHARACTER(n)` | Accepted, but stored internally as `VARCHAR`. Fixed-length padding semantics differ from PostgreSQL. |
| `INET` | IPv4 and IPv6 host or network addresses are supported for equality and ordering. PostgreSQL network-specific operators and functions are not supported. |
| `INT4RANGE` | Partially supported. Common range operators are available, but some PostgreSQL range functions are not supported or behave differently. |
| Composite types | Can be declared and written using text literals, but values cannot be read field by field. |
| `BIT` / `VARBIT` | Accepted with compatibility differences. In particular, over-length values can be silently truncated instead of returning an error. |
| Arrays | One-dimensional arrays are supported. Multi-dimensional arrays are not supported. |

The following PostgreSQL data types are not supported:

+ `XML`
+ `CIDR`
+ `MACADDR`
+ `MONEY`
+ `INT8RANGE`
+ `NUMRANGE`
+ `DATERANGE`
+ `TSRANGE`
+ `TSTZRANGE`

### DDL and schema behavior

Most common PostgreSQL DDL is supported, but some operations differ:

+ `CREATE TABLE AS` and `SELECT INTO` are supported, but the resulting table contains an additional `_rowid` primary key column that is visible in `SELECT *`.
+ `ALTER SEQUENCE` supports only ownership-related operations such as `OWNER TO` and `OWNED BY`. Other clauses, including `RESTART` and `INCREMENT BY`, are not supported.
+ `TRUNCATE` supports only the basic single-table form. Multi-table `TRUNCATE` and optional clauses such as `CASCADE`, `RESTRICT`, `ONLY`, `RESTART IDENTITY`, and `CONTINUE IDENTITY` are not supported.
+ Foreign keys and the `CASCADE`, `SET NULL`, `SET DEFAULT`, `RESTRICT`, and `NO ACTION` referential actions are supported. However, dropping a referenced table does not perform the same foreign-key dependency check as PostgreSQL and can leave a dangling foreign-key constraint.
+ Enum types are supported, but enum values sort by label text rather than declaration order.
+ PostgreSQL table partitioning and table inheritance are not supported.

### Indexes

B-tree, GIN, and HNSW index access methods are supported.

Unique indexes, expression indexes, partial indexes, and `CREATE INDEX CONCURRENTLY` are also supported.

The following PostgreSQL index access methods are not supported:

+ GiST
+ Hash
+ SP-GiST
+ BRIN

HNSW is the supported approximate nearest-neighbor index type for vector workloads. It has additional structural and query-shape requirements.

PostgreSQL vector index types that are not provided by TiDB Cloud, such as IVFFlat, are not available.

### `COPY`

`COPY FROM` supports text and CSV formats over the PostgreSQL wire protocol.

The following PostgreSQL `COPY` capabilities are not supported:

+ Binary `COPY`
+ `COPY (SELECT ...) TO STDOUT`

### PL/pgSQL

PL/pgSQL is partially supported. Common constructs such as variables, assignments, `SELECT INTO`, `IF`/`ELSIF`/`ELSE`, `FOR` loops, `PERFORM`, `EXIT`, `CONTINUE`, `RAISE`, and dynamic `EXECUTE` are supported.

The following limitations apply:

+ `WHILE` loops are not supported.
+ `FOREACH` loops are not supported.
+ Cursor and `REFCURSOR` operations are not supported.
+ Exception handling with `BEGIN ... EXCEPTION` is supported only in `DO` blocks.
+ Nested procedural blocks are supported only in `DO` blocks.

### Triggers

`BEFORE` and `AFTER` triggers on `INSERT`, `UPDATE`, and `DELETE` are supported, with the following compatibility differences:

+ `BEFORE` trigger functions cannot use loops, PL/pgSQL `CASE` statements, dynamic `EXECUTE`, exception handlers, or nested blocks.
+ `FOR EACH STATEMENT` is accepted but executes with per-row semantics rather than PostgreSQL statement-level semantics.
+ In an `AFTER` trigger, a bare `RETURN NEW` or `RETURN OLD` must appear as the only statement on its line.

### Extensions

PostgreSQL-compatible {{{ .starter }}} instances provide a predefined set of extensions and built-in capabilities.

Arbitrary custom or third-party PostgreSQL extensions cannot be installed. Only extensions explicitly supported by TiDB Cloud are available.

For the list of available extensions and extension-specific limitations, see [Supported PostgreSQL extensions](<link>).

### Replication

PostgreSQL logical replication and streaming replication are not supported.

Some publication and replication-slot catalog objects or functions might be present for PostgreSQL compatibility, but they do not provide working replication or change data capture (CDC). `CREATE SUBSCRIPTION` is not supported.

### System catalogs and tooling

PostgreSQL-compatible {{{ .starter }}} instances implement commonly used `pg_catalog` and `information_schema` objects for schema introspection.

The catalog surface is not identical to PostgreSQL. Some catalog views, columns, statistics, and PostgreSQL-specific server functions are unavailable or only partially implemented.

Tools that depend on PostgreSQL-specific catalog or statistics behavior should be validated before use.


## Migration considerations

Before migrating an existing PostgreSQL application, review whether the workload depends on features that are unsupported or behave differently, including:

+ Table partitioning or table inheritance.
+ Foreign data wrappers.
+ Logical or streaming replication.
+ `SERIALIZABLE` transaction isolation.
+ Unsupported PostgreSQL data types.
+ Unsupported index access methods, including GiST, Hash, SP-GiST, and BRIN.
+ Custom or third-party PostgreSQL extensions.
+ PL/pgSQL features that are not supported, such as `WHILE` loops, `FOREACH` loops, cursors, and exception handling in function bodies.

Review and test your application schema and queries before migrating production workloads.
