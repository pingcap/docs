---
title: PostgreSQL Extensions
summary: Learn about the PostgreSQL extensions and built-in capabilities supported by PostgreSQL-compatible TiDB Cloud Starter.
---

# PostgreSQL Extensions

PostgreSQL-compatible {{{ .starter }}} provides a predefined set of PostgreSQL extensions and built-in capabilities for vector search, full-text search, data import, integration, and common PostgreSQL development workflows.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in limited public preview. Extension availability and functionality might change during the preview.

## Supported extensions and capabilities

The following extensions and capabilities are currently supported:

| Extension or capability | Description | Enablement |
| --- | --- | --- |
| `vector` | Provides pgvector-compatible `VECTOR` types, distance operators, similarity search, and HNSW indexing. | Built in. `CREATE EXTENSION vector` can be used to register extension metadata. |
| `embedding` | Provides server-side text embedding functions such as `embedding()` and `embed_text()`. | Run `CREATE EXTENSION embedding`. |
| Full-Text Search | Provides PostgreSQL-compatible full-text search using `tsvector`, `tsquery`, ranking functions, and GIN indexes. | Built in. |
| `zhparser` | Provides Chinese-language tokenization for full-text search. | Built in and always available. |
| `parquet` | Enables querying and importing Parquet data from supported URLs. | Run `CREATE EXTENSION parquet`. |
| `http` | Enables HTTP requests directly from SQL. | Pre-enabled. |
| `pg_cron` | Provides PostgreSQL-compatible cron metadata and management interfaces. Scheduled job execution is not currently available during the limited public preview. | Pre-enabled. |
| `uuid-ossp` | Provides common UUID generation functions, such as `uuid_generate_v4()`. | Built in. `CREATE EXTENSION "uuid-ossp"` can be used to register extension metadata. |


## Enable an extension

Some extensions are available automatically, while others must be enabled explicitly with `CREATE EXTENSION`.

For example:

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
CREATE EXTENSION IF NOT EXISTS parquet;
```

The `vector` type and vector operators are built in. You can also run the following statement to register `vector` in `pg_extension` for compatibility with tools and ORMs that inspect extension metadata:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

To view extensions that are available to the current database, run:

```sql
SELECT *
FROM pg_available_extensions;
```

To view extensions registered in the current database, run:

```sql
SELECT *
FROM pg_extension;
```

## Limitations

The following limitations apply:

- Only extensions and built-in capabilities explicitly provided by TiDB Cloud are supported.
- You cannot install arbitrary custom or third-party PostgreSQL extensions.
- Some supported extensions provide only a subset of the behavior available in upstream PostgreSQL or the corresponding open-source extension.
- Extension availability and behavior might change during the limited public preview.
