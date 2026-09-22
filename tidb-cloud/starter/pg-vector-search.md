---
title: Vector Search
summary: Learn how to store embeddings, perform similarity search, and create HNSW indexes on PostgreSQL-compatible TiDB Cloud Starter.
---

# Vector Search

PostgreSQL-compatible {{{ .starter }}} provides pgvector-compatible vector storage and similarity search, including the `VECTOR` type, distance operators, HNSW indexes, and server-side embedding functions.

> **Note:**
>
> PostgreSQL-compatible {{{ .starter }}} is currently in Limited Public Preview.

## Enable vector search

The `VECTOR` type and vector operators are built in. To register the `vector` extension metadata, run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

To use server-side embedding functions, enable the `embedding` extension:

```sql
CREATE EXTENSION IF NOT EXISTS embedding;
```

## Store vectors

Use `VECTOR(n)` to store fixed-dimension vectors.

For example:

```sql
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding VECTOR(3)
);
```

You can insert vectors using vector literals:

```sql
INSERT INTO documents (content, embedding)
VALUES ('hello world', '[0.1, 0.2, 0.3]'::vector);
```

The number of dimensions in a vector must match the dimension declared by the target `VECTOR(n)` column.

## Distance operators

PostgreSQL-compatible {{{ .starter }}} supports the following pgvector-compatible distance operators:

| Operator | Distance metric | Function equivalent |
| --- | --- | --- |
| `<->` | L2 (Euclidean) distance | `l2_distance(a, b)` |
| `<=>` | Cosine distance | `cosine_distance(a, b)` |
| `<#>` | Negative inner product | `vector_negative_inner_product(a, b)` |

For example, the following query performs a cosine-distance search:

```sql
SELECT
    id,
    content,
    embedding <=> '[0.1, 0.2, 0.3]'::vector AS distance
FROM documents
ORDER BY distance
LIMIT 5;
```

The following utility functions are also available:

| Function | Description |
| --- | --- |
| `l2_distance(a, b)` | Calculates Euclidean distance. |
| `cosine_distance(a, b)` | Calculates cosine distance. |
| `inner_product(a, b)` | Calculates the inner product. |
| `vector_negative_inner_product(a, b)` | Calculates the negative inner product used by `<#>`. |
| `vector_dims(v)` | Returns the number of dimensions. |
| `vector_norm(v)` | Returns the L2 norm. |
| `l2_normalize(v)` | Returns an L2-normalized vector. |

## Create an HNSW index

HNSW (Hierarchical Navigable Small World) indexes accelerate approximate nearest-neighbor search.

Create an index whose operator class matches the distance metric used by your queries.

For cosine distance:

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops);
```

For L2 distance:

```sql
CREATE INDEX idx_documents_embedding_l2
ON documents
USING hnsw (embedding vector_l2_ops);
```

For inner product:

```sql
CREATE INDEX idx_documents_embedding_ip
ON documents
USING hnsw (embedding vector_ip_ops);
```

### Configure HNSW index parameters

You can configure HNSW index build parameters when creating an index:

```sql
CREATE INDEX idx_documents_embedding
ON documents
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

| Parameter | Default | Description |
| --- | --- | --- |
| `m` | 16 | Number of connections per layer. A higher value can improve recall at the cost of additional memory. |
| `ef_construction` | 64 | Search width during index construction. A higher value can improve index quality at the cost of a slower build. |

You can configure the HNSW search expansion factor for the current session:

```sql
SET hnsw.ef_search = 100;
```

The default value of `hnsw.ef_search` is `40`. A higher value can improve recall at the cost of additional query latency.

### When an HNSW index is used

The optimizer can use an HNSW index when all of the following conditions are met:

- The query orders by a distance expression on the indexed vector column and a constant vector.
- The query contains a `LIMIT` clause.
- The HNSW index uses an operator class that matches the distance metric in the query.
- The index is ready.
- The vector-search query itself does not contain a `WHERE` filter.

For example:

```sql
SELECT id, content
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, 0.3]'::vector
LIMIT 10;
```

If these conditions are not met, the query falls back to an exact sequential scan. The result remains correct, but the HNSW index is not used.

> **Note:**
>
> A bound parameter in the vector probe position is not treated as a constant for HNSW planning. For example, `ORDER BY embedding <=> $1::vector LIMIT 10` falls back to a sequential scan.

## Generate embeddings in SQL

The `embedding` extension provides server-side embedding functions.

Generate an embedding from text:

```sql
SELECT embedding('hello world');
```

You can also use `embed_text()` with an explicit model:

```sql
SELECT embed_text('text-embedding-v4', 'hello world');
```

The currently supported embedding dimensions are 256, 512, and 1024. The default output dimension is 1024.

To change the output dimension for the current session:

```sql
SET embedding.dimensions = 512;

SELECT embedding('hello world');
```

### Search with automatic embedding

You can embed query text and calculate distance in one function call:

```sql
SELECT id, content
FROM documents
ORDER BY vec_embed_cosine_distance(embedding, 'database for AI applications')
LIMIT 5;
```

The following functions are available:

| Function | Equivalent operation |
| --- | --- |
| `vec_embed_l2_distance(vec, text)` | `l2_distance(vec, embedding(text))` |
| `vec_embed_cosine_distance(vec, text)` | `cosine_distance(vec, embedding(text))` |
| `vec_embed_inner_product(vec, text)` | `inner_product(vec, embedding(text))` |

## End-to-end example

The following example creates a table, generates embeddings, creates an HNSW index, and performs semantic search:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS embedding;

CREATE TABLE docs (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    vec VECTOR(1024)
);

INSERT INTO docs (content, vec) VALUES
    ('PostgreSQL is a relational database',
     embedding('PostgreSQL is a relational database')),
    ('TiDB Cloud provides a managed database service',
     embedding('TiDB Cloud provides a managed database service')),
    ('Vector search finds semantically similar documents',
     embedding('Vector search finds semantically similar documents'));

CREATE INDEX idx_docs_vec
ON docs
USING hnsw (vec vector_cosine_ops);

SELECT content
FROM docs
ORDER BY vec_embed_cosine_distance(vec, 'managed database')
LIMIT 3;
```

## Limitations

The following limitations apply to vector search during the Limited Public Preview:

- IVFFlat indexes are not supported. HNSW is the supported approximate nearest-neighbor index type.
- An HNSW index can contain only one vector column.
- The indexed vector column must declare an explicit dimension, such as `VECTOR(1024)`. Do not use a bare `VECTOR` column for HNSW indexing.
- The table must have a single-column primary key. Tables without a primary key or with a composite primary key cannot use an HNSW index.
- If the primary key is `INTEGER` or `BIGINT`, its values must be non-negative. `UUID` and `TEXT` primary keys do not have this restriction.
- Partial HNSW indexes are not supported.
- Distance operations require vectors with matching dimensions.
- The `embedding()` and `embed_text()` functions require a database user with sufficient privileges.
- HNSW acceleration has query-shape restrictions. Queries that do not meet the requirements described in [When an HNSW index is used](#when-an-hnsw-index-is-used) use an exact sequential scan instead.

