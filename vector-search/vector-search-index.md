---
title: Vector Search Index
summary: 学习如何构建和使用向量搜索索引，以加速 TiDB 中的 K-Nearest neighbors (KNN) 查询。
---

# Vector Search Index

如 [Vector Search](/vector-search/vector-search-overview.md) 文档所述，向量搜索通过计算给定向量与数据库中存储的所有向量之间的距离，识别出前 K 个最近邻（KNN）。虽然这种方法可以提供准确的结果，但当表中包含大量向量时，速度可能较慢，因为涉及全表扫描。 [^1]

为了提高搜索效率，你可以在 TiDB 中创建向量搜索索引，用于近似 KNN（ANN）搜索。当使用向量索引进行向量搜索时，TiDB 可以大大提升查询性能，误差仅有微小的降低，通常能保持在 90% 以上的搜索召回率。

<CustomContent platform="tidb">

> **Warning:**
>
> 向量搜索功能处于实验阶段。不建议在生产环境中使用此功能。此功能可能在未提前通知的情况下进行更改。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 向量搜索功能处于测试版。可能会在未提前通知的情况下进行更改。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

</CustomContent>

> **Note:**
>
> 向量搜索功能在 TiDB Self-Managed、[{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated) 上均可使用。对于 TiDB Self-Managed 和 TiDB Cloud Dedicated，TiDB 版本必须为 v8.4.0 及以上（建议使用 v8.5.0 及以上）。

目前，TiDB 支持 [HNSW (Hierarchical Navigable Small World)](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 向量搜索索引算法。

## 限制

- 必须提前在集群中部署 TiFlash 节点。
- 向量搜索索引不能用作主键或唯一索引。
- 向量搜索索引只能在单个向量列上创建，不能与其他列（如整数或字符串）组合形成复合索引。
- 创建和使用向量搜索索引时，必须指定距离函数。目前仅支持余弦距离 `VEC_COSINE_DISTANCE()` 和 L2 距离 `VEC_L2_DISTANCE()`。
- 对于同一列，不支持使用相同距离函数创建多个向量搜索索引。
- 不支持直接删除带有向量搜索索引的列。可以先删除该列上的向量搜索索引，再删除列本身。
- 不支持修改带有向量索引的列的类型。
- 不支持将向量搜索索引设置为 [invisible](/sql-statements/sql-statement-alter-index.md)。
- 在启用 [encryption at rest](https://docs.pingcap.com/tidb/stable/encryption-at-rest) 的 TiFlash 节点上构建向量搜索索引不被支持。

## 创建 HNSW 向量索引

[HNSW](https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world) 是最流行的向量索引算法之一。HNSW 索引在性能和准确率方面表现良好，在特定情况下最高可达 98%。

在 TiDB 中，你可以通过以下两种方式为具有 [vector data type](/vector-search/vector-search-data-types.md) 的列创建 HNSW 索引：

- 在创建表时，使用以下语法指定向量列以建立 HNSW 索引：

    ```sql
    CREATE TABLE foo (
        id       INT PRIMARY KEY,
        embedding     VECTOR(5),
        VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
    );
    ```

- 对已包含向量列的现有表，使用以下语法为该列创建 HNSW 索引：

    ```sql
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding)));
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)));

    -- 你也可以显式指定 "USING HNSW" 来构建向量搜索索引。
    CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
    ```

> **Note:**
>
> 向量搜索索引功能依赖于表的 TiFlash 副本。
>
> - 如果在创建表时定义了向量搜索索引，TiDB 会自动为该表创建 TiFlash 副本。
> - 如果在创建表时未定义向量搜索索引，且该表目前没有 TiFlash 副本，则需要手动创建 TiFlash 副本后，才能为表添加向量搜索索引。例如：`ALTER TABLE 'table_name' SET TIFLASH REPLICA 1;`。

在创建 HNSW 向量索引时，需要指定向量的距离函数：

- 余弦距离：`((VEC_COSINE_DISTANCE(embedding)))`
- L2 距离：`((VEC_L2_DISTANCE(embedding)))`

索引只能用于固定维度的向量列，例如定义为 `VECTOR(3)` 的列。不能用于非固定维度的向量列（如定义为 `VECTOR`），因为只能在相同维度的向量之间计算距离。

关于向量搜索索引的限制和注意事项，请参见 [Restrictions](#restrictions)。

## 使用向量索引

可以在 K 最近邻搜索查询中使用向量搜索索引，通过 `ORDER BY ... LIMIT` 子句实现，例如：

```sql
SELECT *
FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3, 4, 5]')
LIMIT 10
```

使用索引进行向量搜索时，确保 `ORDER BY ... LIMIT` 子句使用的距离函数与创建索引时指定的相同。

## 在过滤条件下使用向量索引

包含预过滤（使用 `WHERE` 子句）的查询无法利用向量索引，因为它们不是按照 SQL 语义进行 KNN 查询。例如：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之前执行，因此无法使用向量索引：

SELECT * FROM vec_table
WHERE category = "document"
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 5;
```

要在过滤条件下使用向量索引，可以先用向量搜索查询出 K 最近邻，然后再过滤掉不需要的结果：

```sql
-- 对于以下查询，`WHERE` 过滤在 KNN 之后执行，因此无法使用向量索引：

SELECT * FROM
(
  SELECT * FROM vec_table
  ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]')
  LIMIT 5
) t
WHERE category = "document";

-- 注意：如果过滤掉一些结果，最终返回的结果可能少于 5 条。
```

## 查看索引构建进度

在插入大量数据后，部分数据可能不会立即持久化到 TiFlash。对于已持久化的向量数据，向量搜索索引会同步构建。对于尚未持久化的数据，索引会在数据持久化后进行构建。此过程不会影响数据的准确性和一致性，你仍然可以随时进行向量搜索并获得完整结果，但性能会在索引完全构建前不理想。

你可以通过查询 `INFORMATION_SCHEMA.TIFLASH_INDEXES` 表来查看索引构建进度，示例如下：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIFLASH_INDEXES;
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| TIDB_DATABASE | TIDB_TABLE | TABLE_ID | COLUMN_NAME | INDEX_NAME    | COLUMN_ID | INDEX_ID | INDEX_KIND | ROWS_STABLE_INDEXED | ROWS_STABLE_NOT_INDEXED | ROWS_DELTA_INDEXED | ROWS_DELTA_NOT_INDEXED | ERROR_MESSAGE | TIFLASH_INSTANCE |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
| test          | tcff1d827  |      219 | col1fff     | 0a452311      |         7 |        1 | HNSW       |               29646 |                       0 |                  0 |                      0 |               | 127.0.0.1:3930   |
| test          | foo        |      717 | embedding   | idx_embedding |         2 |        1 | HNSW       |                   0 |                       0 |                  0 |                      3 |               | 127.0.0.1:3930   |
+---------------+------------+----------+-------------+---------------+-----------+----------+------------+---------------------+-------------------------+--------------------+------------------------+---------------+------------------+
```

- 你可以检查 `ROWS_STABLE_INDEXED` 和 `ROWS_STABLE_NOT_INDEXED` 列以了解索引构建进度。当 `ROWS_STABLE_NOT_INDEXED` 变为 0 时，索引构建完成。

    作为参考，索引一个 768 维、500 MiB 大小的向量数据集可能需要最多 20 分钟。索引器可以对多个表并行运行。目前不支持调整索引器的优先级或速度。

- 你可以检查 `ROWS_DELTA_NOT_INDEXED` 列，了解 Delta 层中的行数。TiFlash 的存储层数据分为 Delta 层和 Stable 层。Delta 层存储最近插入或更新的行，且会根据写入负载定期合并到 Stable 层，这一过程称为压缩（Compaction）。

    Delta 层始终不被索引。为了获得最佳性能，可以强制将 Delta 层合并到 Stable 层，使所有数据都能被索引：

    ```sql
    ALTER TABLE <TABLE_NAME> COMPACT;
    ```

    更多信息请参见 [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md)。

此外，你还可以通过执行 `ADMIN SHOW DDL JOBS;` 并检查 `row count` 来监控 DDL 任务的执行进度，但此方法不完全准确，因为 `row count` 值来自 `TIFLASH_INDEXES` 中的 `rows_stable_indexed` 字段。你可以用此方法作为索引进度的参考。

## 查看是否使用向量索引

使用 [`EXPLAIN`](/sql-statements/sql-statement-explain.md) 或 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 语句检查查询是否使用了向量索引。当 `operator info` 列中的 `annIndex:` 出现，表示此表扫描利用了向量索引。

**示例：使用了向量索引**

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

**示例：未使用向量索引（未指定前 K）**

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

当无法使用向量索引时，某些情况下会出现警告，帮助你了解原因：

```sql
-- 使用了错误的距离函数：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_L2_DISTANCE(embedding, '[1, 2, 3]')
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: not ordering by COSINE distance

-- 使用了错误的排序方式：
[tidb]> EXPLAIN SELECT * FROM vector_table_with_index
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1, 2, 3]') DESC
LIMIT 10;

[tidb]> SHOW WARNINGS;
ANN index not used: index can be used only when ordering by vec_cosine_distance() in ASC order
```

## 分析向量搜索性能

想了解向量索引的详细使用情况，可以执行 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 并查看输出中的 `execution info` 列，例如：

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
> 该执行信息为内部信息，字段和格式可能会在没有通知的情况下发生变化。请勿依赖。

一些重要字段的说明：

- `vector_index.load.total`：加载索引的总时长。此字段可能大于实际查询时间，因为多个向量索引可能同时加载。
- `vector_index.load.from_s3`：从 S3 加载的索引数量。
- `vector_index.load.from_disk`：从磁盘加载的索引数量，之前已从 S3 下载。
- `vector_index.load.from_cache`：从缓存加载的索引数量，之前已从 S3 下载。
- `vector_index.search.total`：在索引中搜索的总时长。较大的延迟通常意味着索引冷（未访问过或很久未访问），在搜索时会有较重的 I/O 操作。此字段可能大于实际查询时间，因为多个向量索引可能同时搜索。
- `vector_index.search.discarded_nodes`：在搜索过程中访问但被丢弃的向量行数。这些被丢弃的向量不会计入搜索结果。数值较大通常表示存在大量陈旧行，可能由 `UPDATE` 或 `DELETE` 语句引起。

请参见 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)、[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) 和 [EXPLAIN Walkthrough](/explain-walkthrough.md) 来理解输出内容。

## 相关链接

- [Improve Vector Search Performance](/vector-search/vector-search-improve-performance.md)
- [Vector Data Types](/vector-search/vector-search-data-types.md)

[^1]: KNN 搜索的说明借鉴自由 [rschu1ze](https://github.com/rschu1ze) 在 ClickHouse 文档中撰写的 [Approximate Nearest Neighbor Search Indexes](https://github.com/ClickHouse/ClickHouse/pull/50661/files#diff-7ebd9e71df96e74230c9a7e604fa7cb443be69ba5e23bf733fcecd4cc51b7576) 文档，授权协议为 Apache License 2.0。