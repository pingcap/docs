---
title: Vector Search Index
summary: Learn how to build and use the vector search index to accelerate K-Nearest neighbors (KNN) queries in TiDB.
---

# Vector Search Index

K-nearest neighbors (KNN) search is the method for finding the K closest points to a given point in a vector space. The most straightforward approach to perform KNN search is a brute force search, which calculates the distance between the given vector and all other vectors in the space. This approach guarantees perfect accuracy, but it is usually too slow for real-world use. Therefore, approximate algorithms are commonly used in KNN search to enhance speed and efficiency.

In TiDB, you can create and use vector search indexes for such approximate nearest neighbor (ANN) searches over columns with [vector data types](/tidb-cloud/vector-search-data-types.md). By using vector search indexes, vector search queries could be finished in milliseconds.

Currently, TiDB supports the [HNSW (Hierarchical Navigable Small World)](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) vector search index algorithm.

## Create the HNSW vector index

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) is one of the most popular vector indexing algorithms. The HNSW index provides good performance with relatively high accuracy, up to 98% in specific cases.

In TiDB, you can create an HNSW index for a column with a [vector data type](/tidb-cloud/vector-search-data-types.md) in either of the following ways:

- When creating a table, use the following syntax to specify the vector column for the HNSW index:

  ```sql
  CREATE TABLE foo (
      id       INT PRIMARY KEY,
      embedding     VECTOR(5),
      VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
  );
  ```

- For an existing table that already contains a vector column, use the following syntax to create an HNSW index for the vector column:

  ```sql
  CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
  ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

  -- You can also explicitly specify "USING HNSW" to build the vector search index.
  CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
  ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
  ```

> **Note:**
>
> The vector search index feature relies on TiFlash replicas for tables.
>
> - If a vector search index is defined when a table is created, TiDB automatically creates a TiFlash replica for the table.
> - If no vector search index is defined when a table is created, and the table currently does not have a TiFlash replica, you need to manually create a TiFlash replica before adding a vector search index to the table. For example: `ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`.

When creating an HNSW vector index, you need to specify the distance function for the vector:

- Cosine Distance: `((VEC_COSINE_DISTANCE(embedding)))`
- L2 Distance: `((VEC_L2_DISTANCE(embedding)))`

The vector index can only be created for fixed-dimensional vector columns, such as a column defined as `VECTOR(3)`. It cannot be created for non-fixed-dimensional vector columns (such as a column defined as `VECTOR`) because vector distances can only be calculated between vectors with the same dimension.

For other limitations, see [Vector index limitations](/tidb-cloud/vector-search-limitations.md#vector-index-limitations).

## Use the vector index

The vector search index can be used in K-nearest neighbor search queries by using the `ORDER BY ... LIMIT` clause as follows:

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

To use an index in a vector search, make sure that the `ORDER BY ... LIMIT` clause uses the same distance function as the one specified when creating the vector index.

## Use the vector index with filters

Queries that contain a pre-filter (using the `WHERE` clause) cannot utilize the vector index because they are not querying for K-Nearest neighbors according to the SQL semantics. For example:

```sql
-- For the following query, the `WHERE` filter is performed before KNN, so the vector index cannot be used:

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

To use the vector index with filters, query for the K-Nearest neighbors first using vector search, and then filter out unwanted results:

```sql
-- For the following query, the `WHERE` filter is performed after KNN, so the vector index cannot be used:

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- Note that this query might return fewer than 5 results if some are filtered out.
```

## View index build progress

After you insert a large volume of data, some of it might not be instantly persisted to TiFlash. For vector data that has already been persisted, the vector search index is built synchronously. For data that has not yet been persisted, the index will be built once the data is persisted. This process does not affect the accuracy and consistency of the data. You can still perform vector searches at any time and get complete results. However, performance will be suboptimal until vector indexes are fully built.

To view the index build progress, you can query the `INFORMATION_SCHEMA.TIFLASH_INDEXES` table as follows:

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- You can check the `ROWS_STABLE_INDEXED` and `ROWS_STABLE_NOT_INDEXED` columns for the index build progress. When `ROWS_STABLE_NOT_INDEXED` becomes 0, the index build is complete.

  As a reference, indexing a 500 MiB vector dataset with 768 dimensions might take up to 20 minutes. The indexer can run in parallel for multiple tables. Currently, adjusting the indexer priority or speed is not supported.

- You can check the `ROWS_DELTA_NOT_INDEXED` column for the number of rows in the Delta layer. Data in the storage layer of TiFlash is stored in two layers: Delta layer and Stable layer. The Delta layer stores recently inserted or updated rows and is periodically merged into the Stable layer according to the write workload. This merge process is called Compaction.

  The Delta layer is always not indexed. To achieve optimal performance, you can force the merge of the Delta layer into the Stable layer so that all data can be indexed:

  ```sql
  ALTER TABLE <TABLE_NAME> COMPACT;
  ```

  For more information, see [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md).

In addition, you can monitor the execution progress of the DDL job by executing `ADMIN SHOW DDL JOBS;` and checking the `row count`. However, this method is not fully accurate, because the `row count` value is obtained from the `rows_stable_indexed` field in `TIFLASH_INDEXES`. You can use this approach as a reference for tracking the progress of indexing.

## Check whether the vector index is used

Use the [`EXPLAIN`](/sql-statements/sql-statement-explain.md) or [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statement to check whether a query is using the vector index. When `annIndex:` is presented in the `operator info` column for the `TableFullScan` executor, it means this table scan is utilizing the vector index.

**Example: the vector index is used**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+-------------------------------------------------------------------------------------+
| ... | operator info                                                                       |
+-----+-------------------------------------------------------------------------------------+
| ... | ...                                                                                 |
| ... | Column#5, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#5 |
| ... | MppVersion: 1, data:ExchangeSender_16                                               |
| ... | ExchangeType: PassThrough                                                           |
| ... | ...                                                                                 |
| ... | Column#4, offset:0, count:10                                                        |
| ... | ..., vec_cosine_distance(test.vector_table_with_index.embedding, [1,2,3])->Column#4 |
| ... | annIndex:COSINE(test.vector_table_with_index.embedding..[1,2,3], limit:10), ...     |
+-----+-------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

**Example: The vector index is not used because of not specifying a Top K**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
     -> ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]');
+--------------------------------+-----+--------------------------------------------------+
| id                             | ... | operator info                                    |
+--------------------------------+-----+--------------------------------------------------+
| Projection_15                  | ... | ...                                              |
| └─Sort_4                       | ... | Column#4                                         |
|   └─Projection_16              | ... | ..., vec_cosine_distance(..., [1,2,3])->Column#4 |
|     └─TableReader_14           | ... | MppVersion: 1, data:ExchangeSender_13            |
|       └─ExchangeSender_13      | ... | ExchangeType: PassThrough                        |
|         └─TableFullScan_12     | ... | keep order:false, stats:pseudo                   |
+--------------------------------+-----+--------------------------------------------------+
6 rows in set, 1 warning (0.01 sec)
```

When the vector index cannot be used, a warning occurs in some cases to help you learn the cause:

```sql
-- Using a wrong distance function:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_L2_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- Using a wrong order:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## Analyze vector search performance

To learn detailed information about how a vector index is used, you can execute the [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statement and check the `execution info` column in the output:

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;
+-----+--------------------------------------------------------+-----+
|     | execution info                                         |     |
+-----+--------------------------------------------------------+-----+
| ... | time:339.1ms, loops:2, RU:0.000000, Concurrency:OFF    | ... |
| ... | time:339ms, loops:2                                    | ... |
| ... | time:339ms, loops:3, Concurrency:OFF                   | ... |
| ... | time:339ms, loops:3, cop_task: {...}                   | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{time:327.5ms, loops:1, threads:4}        | ... |
| ... | tiflash_task:{...}, vector_idx:{                       | ... |
|     |   load:{total:68ms,from_s3:1,from_disk:0,from_cache:0},|     |
|     |   search:{total:0ms,visited_nodes:2,discarded_nodes:0},|     |
|     |   read:{vec_total:0ms,others_total:0ms}},...}          |     |
+-----+--------------------------------------------------------+-----+
```

> **Note:**
>
> The execution information is internal. Fields and formats are subject to change without any notification. Do not rely on them.

Explanation of some important fields:

- `vector_index.load.total`: The total duration of loading index. This field might be larger than the actual query time because multiple vector indexes might be loaded in parallel.
- `vector_index.load.from_s3`: Number of indexes loaded from S3.
- `vector_index.load.from_disk`: Number of indexes loaded from disk. The index was already downloaded from S3 previously.
- `vector_index.load.from_cache`: Number of indexes loaded from cache. The index was already downloaded from S3 previously.
- `vector_index.search.total`: The total duration of searching in the index. Large latency usually means the index is cold (never accessed before, or accessed long ago) so that there are heavy I/O operations when searching through the index. This field might be larger than the actual query time because multiple vector indexes might be searched in parallel.
- `vector_index.search.discarded_nodes`: Number of vector rows visited but discarded during the search. These discarded vectors are not considered in the search result. Large values usually indicate that there are many stale rows caused by `UPDATE` or `DELETE` statements.

See [`EXPLAIN`](/sql-statements/sql-statement-explain.md), [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md), and [EXPLAIN Walkthrough](/explain-walkthrough.md) for interpreting the output.

## Limitations

See [Vector index limitations](/tidb-cloud/vector-search-limitations.md#vector-index-limitations).

## See also

- [Improve Vector Search Performance](/tidb-cloud/vector-search-improve-performance.md)
- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
