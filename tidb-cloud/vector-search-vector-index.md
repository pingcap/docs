---
title: Vector Search Index
---

#  Vector Search Index

In TiDB, you can create and utilize Vector Search Indexes for such approximate nearest neighbor (ANN) searches. By using Vector Search Indexes, vector search queries could be finished in milliseconds.

> **Note**
>
> The vector search feature is currently in beta and only available for [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless) clusters.

## HNSW Index

HNSW index is an index suitable for vector search. You can create an HNSW index to speed up the vector search query when you define the table.

For example, to create an HNSW index with cosine distance:

```sql
CREATE TABLE vector_table_with_index (
    id int PRIMARY KEY, doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
);
```

Note: The syntax to create HNSW Index may be changed in future.
Currently you can create an HNSW index with L2 and cosine distance.

