---
title: Vector Search Index
summary: Learn how to build and use the vector search index to accelerate K-Nearest neighbors (KNN) queries in TiDB.
---

# Vector Search Index

K-nearest neighbors (KNN) search is the problem of finding the K closest points for a given point in a vector space. The most straightforward approach to solving this problem is a brute force search, where the distance between all points in the vector space and the reference point is computed. This method guarantees perfect accuracy, but it is usually too slow for practical applications. Thus, nearest neighbors search problems are often solved with approximate algorithms.

In TiDB, you can create and utilize vector search indexes for such approximate nearest neighbor (ANN) searches over columns with [vector data types](/tidb-cloud/vector-search-data-types.md). By using vector search indexes, vector search queries could be finished in milliseconds.

TiDB currently supports the following vector search index algorithms:

- HNSW

> **Note:**
>
> Vector search index is only available for [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) clusters.

## Create the HNSW vector index

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) is one of the most popular vector indexing algorithms. The HNSW index provides good performance with relatively high accuracy (> 98% in typical cases).

To create an HNSW vector index, specify the index definition in the comment of a column with a [vector data type](/tidb-cloud/vector-search-data-types.md) when creating the table:

```sql
CREATE TABLE vector_table_with_index (
    id INT PRIMARY KEY, doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
);
```

> **Note:**
>
> The syntax to create a vector index might change in future releases.

You must specify the distance metric via the `distance=<metric>` configuration when creating the vector index:

- Cosine Distance: `COMMENT "hnsw(distance=cosine)"`
- L2 Distance: `COMMENT "hnsw(distance=l2)"`

The vector index can only be created for fixed-dimensional vector columns like `VECTOR(3)`. It cannot be created for mixed-dimensional vector columns like `VECTOR` because vector distances can only be calculated between vectors with the same dimensions.

If you are using programming language SDKs or ORMs, refer to the following documentation for creating vector indexes:

- Python: [TiDB Vector SDK for Python](https://github.com/pingcap/tidb-vector-python)
- Python: [SQLAlchemy](/tidb-cloud/vector-search-integrate-with-sqlalchemy.md)
- Python: [Peewee](/tidb-cloud/vector-search-integrate-with-peewee.md)
- Python: [Django](/tidb-cloud/vector-search-integrate-with-django-orm.md)

Be aware of the following limitations when creating the vector index. These limitations might be removed in future releases:

- L1 distance and inner product are not supported for the vector index yet.

- You can only define and create a vector index when the table is created. You cannot create the vector index on demand using DDL statements after the table is created. You cannot drop the vector index using DDL statements as well.

## Use the vector index

The vector search index can be used in K-nearest neighbor search queries by using the `ORDER BY ... LIMIT` form like below:

```sql
SELECT *
FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
LIMIT 10
```

You must use the same distance metric as you have defined when creating the vector index if you want to utilize the index in vector search.

## Use the vector index with filters

Queries that contain a pre-filter (using the `WHERE` clause) cannot utilize the vector index because they are not querying for K-Nearest neighbors according to the SQL semantics. For example:

```sql
-- Filter is performed before kNN, so Vector Index cannot be used:

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

Several workarounds are as follows:

**Post-Filter after Vector Search:** Query for the K-Nearest neighbors first, then filter out unwanted results:

```sql
-- The filter is performed after kNN for these queries, so Vector Index can be used:

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- Note that this query may return less than 5 results if some are filtered out.
```

**Use Table Partitioning**: Queries within the [table partition](/partitioned-table.md) can fully utilize the vector index. This can be useful if you want to perform equality filters, as equality filters can be turned into accessing specified partitions.

Example: Suppose you want to find the closest documentation for a specific product version.

```sql
-- Filter is performed before kNN, so Vector Index cannot be used:
SELECT * FROM docs
WHERE ver = "v2.0"
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

Instead of writing a query using the `WHERE` clause, you can partition the table and then query within the partition using the [`PARTITION` keyword](/partitioned-table.md#partition-selection):

```sql
CREATE TABLE docs (
    id INT,
    ver VARCHAR(10),
    doc TEXT,
    embedding VECTOR(3) COMMENT "hnsw(distance=cosine)"
) PARTITION BY LIST COLUMNS (ver) (
    PARTITION p_v1_0 VALUES IN ('v1.0'),
    PARTITION p_v1_1 VALUES IN ('v1.1'),
    PARTITION p_v1_2 VALUES IN ('v1.2'),
    PARTITION p_v2_0 VALUES IN ('v2.0')
);

SELECT * FROM docs
PARTITION (p_v2_0)
ORDER BY Vec_Cosine_distance(embedding, '[1, 2, 3]')
LIMIT 5;
```

See [Table Partitioning](/partitioned-table.md) for more information.

## View index build progress

Unlike other indexes, vector indexes are built asynchronously. Therefore, vector indexes might not be immediately available after bulk data insertion. This does not affect data correctness or consistency, and you can perform vector searches at any time and get complete results. However, performance will be suboptimal until vector indexes are fully built. 

To view the index build progress, you can query the `INFORMATION_SCHEMA.TIFLASH_INDEXES` table as follows:

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TIDB_PARTITION | TABLE_ID | BELONGING_TABLE_ID | COLUMN_NAME | COLUMN_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | TIFLASH_INSTANCE |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |                   0 |                   13000 |                  0 |                   2000 | store-6ba728d2   |
| test          | sample     | NULL           |      106 |                 -1 | vec         |         2 | HNSW       |               10500 |                       0 |                  0 |                   4500 | store-7000164f   |
+---------------+------------+----------------+----------+--------------------+-------------+-----------+------------+---------------------+-------------------------+--------------------+------------------------+------------------+
```

- The `ROWS_STABLE_INDEXED` and `ROWS_STABLE_NOT_INDEXED` columns show the index build progress. When `ROWS_STABLE_NOT_INDEXED` becomes 0, the index build is complete.

    As a reference, indexing a 500 MiB vector dataset might take up to 20 minutes. The indexer can run in parallel for multiple tables. Currently, adjusting the indexer priority or speed is not supported.

- The `ROWS_DELTA_NOT_INDEXED` column shows the number of rows in the Delta layer. The Delta layer stores _recently_ inserted or updated rows and is periodically merged into the Stable layer according to the write workload. This merge process is called Compaction.

    The Delta layer is always not indexed. To achieve optimal performance, you can force the merge of the Delta layer into the Stable layer so that all data can be indexed:

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    For more information, see [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md).

## Check whether the vector index is used

Use the [`EXPLAIN`](/sql-statements/sql-statement-explain.md) or [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statement to check whether this query is using the vector index. When `annIndex:` is presented in the `operator info` column for the `TableFullScan` executor, it means this table scan is utilizing the vector index.

**Example: the vector index is used**

```sql
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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
     -> ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]');
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
-- Using a wrong distance metric:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_l2_Distance(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- Using a wrong order:
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## Analyze vector search performance

The [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) statement contains detailed information about how the vector index is used in the `execution info` column:

```sql
[tidb]> EXPLAIN ANALYZE SELECT * FROM vector_table_with_index
ORDER BY Vec_Cosine_Distance(embedding, '[1, 2, 3]')
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

- `vector_index.load.total`: The total duration of loading index. This field could be larger than actual query time because multiple vector indexes may be loaded in parallel.
- `vector_index.load.from_s3`: Number of indexes loaded from S3.
- `vector_index.load.from_disk`: Number of indexes loaded from disk. The index was already downloaded from S3 previously.
- `vector_index.load.from_cache`: Number of indexes loaded from cache. The index was already downloaded from S3 previously.
- `vector_index.search.total`: The total duration of searching in the index. Large latency usually means the index is cold (never accessed before, or accessed long ago) so that there is heavy IO when searching through the index. This field could be larger than actual query time because multiple vector indexes may be searched in parallel.
- `vector_index.search.discarded_nodes`: Number of vector rows visited but discarded during the search. These discarded vectors are not considered in the search result. Large values usually indicate that there are many stale rows caused by UPDATE or DELETE statements.

See [`EXPLAIN`](/sql-statements/sql-statement-explain.md), [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md), and [EXPLAIN Walkthrough](/explain-walkthrough.md) for interpreting the output.

## See also

- [Improve Vector Search Performance](/tidb-cloud/vector-search-improve-performance.md)
- [Vector Data Types](/tidb-cloud/vector-search-data-types.md)
