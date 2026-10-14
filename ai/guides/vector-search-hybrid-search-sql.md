---
title: Hybrid Search with SQL
summary: Learn how to combine full-text search and vector search in one SQL query in TiDB, with embeddings generated automatically on insert.
---

# Hybrid Search with SQL

Hybrid search runs a full-text search and a vector search over the same table and merges the two result lists. Full-text search finds exact keywords such as error codes and product names. Vector search finds text with similar meaning even when the words differ. Merging the two result lists helps when a query mixes exact terms with a description of what you mean.

This document shows how to do hybrid search in a single SQL query. TiDB automatically generates embeddings when you insert text. To do the same with the `pytidb` Python SDK, see [Hybrid Search](/ai/guides/vector-search-hybrid-search.md).

## Prerequisites

Full-text search is still in the early stages and is being rolled out to more customers. Currently, full-text search is only available on {{{ .starter }}} in the following regions:

- AWS: `Oregon (us-west-2)`, `N. Virginia (us-east-1)`, `Tokyo (ap-northeast-1)`, `Frankfurt (eu-central-1)`, and `Singapore (ap-southeast-1)`

Auto Embedding is only available on {{{ .starter }}} instances hosted on AWS.

To complete this tutorial, make sure you have a {{{ .starter }}} instance in one of the preceding regions, and a MySQL client connected to it. If you don't have an instance, follow [Creating a {{{ .starter }}} instance](/develop/dev-guide-build-cluster-in-cloud.md) to create one.

## Step 1. Create a table

Create a table with a text column, a vector column that TiDB fills from the text, a full-text index, and a vector index:

```sql
USE test;

CREATE TABLE docs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content TEXT,
    content_vector VECTOR(1024) GENERATED ALWAYS AS (
        EMBED_TEXT("tidbcloud_free/amazon/titan-embed-text-v2", content)
    ) STORED,
    FULLTEXT INDEX ft_content (content) WITH PARSER STANDARD,
    VECTOR INDEX idx_vec ((VEC_COSINE_DISTANCE(content_vector)))
);
```

`EMBED_TEXT()` calls an embedding model hosted by TiDB Cloud, so you do not need an API key for this example. The vector dimension, `1024`, must match the model's output size. For other models, see [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md).

## Step 2. Insert text

Insert text only. TiDB generates the embedding for each row on insert:

```sql
INSERT INTO docs (content) VALUES
  ('TiDB error 8200 means a vector index cannot be added to a partitioned table.'),
  ('Store agent memory in one table with a vector index and transactions.'),
  ('Solar panels convert sunlight into renewable energy.'),
  ('Use EXPLAIN to check whether a query uses the vector index.'),
  ('Partitioning a table by tenant lets the optimizer prune partitions.'),
  ('A cat sat on the warm windowsill all afternoon.');
```

## Step 3. Search by meaning

Pass the query text to `VEC_EMBED_COSINE_DISTANCE()`. TiDB embeds the query with the same model and ranks rows by distance:

```sql
SELECT id, content FROM docs
ORDER BY VEC_EMBED_COSINE_DISTANCE(content_vector, 'why does adding a vector index fail on my partitioned table')
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |
|  2 | Store agent memory in one table with a vector index and transactions.        |
+----+------------------------------------------------------------------------------+
```

## Step 4. Search by keyword

Use `fts_match_word()` to find rows that contain at least one of the query terms, ranked by relevance:

```sql
SELECT id, content FROM docs
WHERE fts_match_word('error 8200', content)
ORDER BY fts_match_word('error 8200', content) DESC
LIMIT 3;
```

```
+----+------------------------------------------------------------------------------+
| id | content                                                                      |
+----+------------------------------------------------------------------------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |
+----+------------------------------------------------------------------------------+
```

## Step 5. Combine both searches in one query

The following query runs both searches, ranks each result list, and performs Reciprocal Rank Fusion (RRF) on the Top-K candidate IDs returned by the vector and full-text searches first. It then joins the fused top hits back to `docs` to fetch the document content. Each row scores `1 / (60 + rank)` for every list it appears in, and the scores are added. A row that ranks well in both lists rises to the top. The constant `60` is the value commonly used for RRF; a larger value reduces the advantage of top-ranked rows over lower-ranked ones.

```sql
WITH
vec AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY distance, id) AS r
  FROM (
    SELECT /*+ READ_FROM_STORAGE(TIFLASH[docs]) */
           id,
           VEC_EMBED_COSINE_DISTANCE(
             content_vector,
             'vector index error 8200 partitioned table'
           ) AS distance
    FROM docs
    ORDER BY distance
    LIMIT 20
  ) v
),
fts AS (
  SELECT id,
         ROW_NUMBER() OVER (ORDER BY score DESC, id) AS r
  FROM (
    SELECT id,
           fts_match_word(
             'vector index error 8200 partitioned table',
             content
           ) AS score
    FROM docs
    WHERE fts_match_word(
      'vector index error 8200 partitioned table',
      content
    )
    ORDER BY score DESC
    LIMIT 20
  ) f
),
hits AS (
  SELECT id,
         1.0 / (60 + r) AS contribution,
         r AS vector_rank,
         NULL AS fulltext_rank
  FROM vec
  UNION ALL
  SELECT id,
         1.0 / (60 + r),
         NULL,
         r
  FROM fts
),
top_hits AS (
  SELECT id,
         SUM(contribution) AS rrf_score,
         MAX(vector_rank) AS vector_rank,
         MAX(fulltext_rank) AS fulltext_rank
  FROM hits
  GROUP BY id
  ORDER BY rrf_score DESC, id
  LIMIT 3
)
SELECT d.id, d.content,
       t.rrf_score,
       t.vector_rank,
       t.fulltext_rank
FROM top_hits t
JOIN docs d ON d.id = t.id
ORDER BY t.rrf_score DESC, t.id;
```

```
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
| id | content                                                                      | rrf_score | vector_rank | fulltext_rank |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
|  1 | TiDB error 8200 means a vector index cannot be added to a partitioned table. |   0.03279 |           1 |             1 |
|  2 | Store agent memory in one table with a vector index and transactions.        |   0.03200 |           3 |             2 |
|  4 | Use EXPLAIN to check whether a query uses the vector index.                  |   0.03200 |           2 |             3 |
+----+------------------------------------------------------------------------------+-----------+-------------+---------------+
```

Each search fetches 20 candidates before merging. Raise that `LIMIT` if relevant rows are missing from the merged result.

Full-text relevance scores can change after TiFlash reorganizes newly written rows in the background, and rows with similar scores can then swap places. On a freshly loaded table, the `fulltext_rank` and `rrf_score` values in your output might therefore differ from the preceding example.

The `READ_FROM_STORAGE(TIFLASH[docs])` hint makes the vector search read from TiFlash, where the vector index lives. On a small table the optimizer might otherwise read from TiKV and skip the vector index. The same can happen to other vector searches on a small table, such as the Step 3 query; add the same hint there if `EXPLAIN` does not show `annIndex:`. To check whether the optimizer selects both indexes, run `EXPLAIN` on the query: the `operator info` column shows `annIndex:` for the vector search and `textSearch:` for the full-text search. For more about checking vector index use, see [Check whether the vector index is used](/ai/reference/vector-search-index.md#check-whether-the-vector-index-is-used).

## See also

- [Hybrid Search](/ai/guides/vector-search-hybrid-search.md)
- [Full-Text Search with SQL](/ai/guides/vector-search-full-text-search-sql.md)
- [Auto Embedding Overview](/ai/integrations/vector-search-auto-embedding-overview.md)
- [Vector Search Index](/ai/reference/vector-search-index.md)
