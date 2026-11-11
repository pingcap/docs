---
title: Troubleshoot Slow Queries with Vector Indexes
summary: Learn how to diagnose slow TiDB vector searches by checking execution plans, unindexed data, and index loading during cold access.
---

# Troubleshoot Slow Queries with Vector Indexes

If a vector search remains slow after you create a vector index, check whether the query uses the index, whether data remains unindexed, and whether the first execution has additional loading overhead.

The examples use MySQL-compatible SQL and TiFlash vector indexes. For supported deployments, versions, and restrictions, see [Vector Search Index](/ai/reference/vector-search-index.md).

## Choose a starting point

| Symptom | Check first | Next step |
| --- | --- | --- |
| Every execution is slow | Look for `annIndex:` in the execution plan. | If absent, check the query structure and TiFlash replica. If present, check index build status. |
| The first execution is slow, but subsequent executions are faster | Compare index loading information across executions. | Investigate cold access. |
| Queries become slow after a bulk load | Check unindexed data in the Stable and Delta layers. | Observe the counts over time and record concurrent writes. |

These checks narrow the investigation. A single field or execution does not establish the root cause.

## Prepare the original query

Save the slow SQL statement, query vector, Top K, and table definition. Keep the query unchanged when comparing executions, and record query concurrency and concurrent writes.

The examples assume an existing `test.documents` table with `id`, `embedding VECTOR(3)`, and a vector index on `VEC_COSINE_DISTANCE(embedding)`. Replace the database, table, columns, and vector to match your workload. The query vector must have the same dimension as the indexed column.

Inspect the table definition and run `EXPLAIN` on the original query. The following simplified query illustrates the syntax:

```sql
SHOW CREATE TABLE test.documents;

EXPLAIN
SELECT id,
       VEC_COSINE_DISTANCE(embedding, '[1,2,3]') AS distance
FROM test.documents
ORDER BY distance
LIMIT 10;

SHOW WARNINGS;
```

Run `SHOW WARNINGS` immediately after `EXPLAIN` to capture any explanation for an unused vector index. No warnings does not prove index usage; inspect the plan as well. Save the original plan before simplifying the SQL to investigate differences.

## Step 1. Check whether the plan uses the vector index

Look for `annIndex:` in `operator info`. A `TableFullScan` operator can use a vector index, so its name alone does not indicate a brute-force vector scan.

The following excerpt illustrates the marker, rather than output from a measured execution:

```text
annIndex:COSINE(...embedding..[1,2,3], limit:10)
```

If the marker is absent, check the following:

1. The table has the intended vector index.
2. The query uses the same distance function as the index.
3. The query includes `ORDER BY ... LIMIT` and sorts by distance in ascending order.
4. The query does not introduce a same-level `WHERE` condition, additional sort items, or arithmetic on the distance expression. Compare it with a simple distance-ordering query, and restore business conditions one at a time.
5. The TiFlash replica is available and session settings allow reading from TiFlash.

```sql
SELECT TABLE_SCHEMA, TABLE_NAME, REPLICA_COUNT, AVAILABLE, PROGRESS
FROM INFORMATION_SCHEMA.TIFLASH_REPLICA
WHERE TABLE_SCHEMA = 'test'
  AND TABLE_NAME = 'documents';

SHOW VARIABLES LIKE 'tidb_isolation_read_engines';
```

If the replica is missing or unavailable, investigate its configuration and replication status first. Replica availability does not establish that all vector data is indexed. For field definitions, see [`TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md).

Keep required business filters. Moving a filter after candidate retrieval changes query semantics and can return fewer than Top K results. Choose a pattern that meets your requirements using [Use the vector index with filters](/ai/reference/vector-search-index.md#use-the-vector-index-with-filters), and check the plan again.

**Next step:** If the original query has `annIndex:`, check index build status. If only the simplified query has the marker, investigate the query structure differences first.

## Step 2. Check for unindexed data

Even when the plan has `annIndex:`, inspect index build status, especially after bulk loading or during continuous writes:

```sql
SELECT TIDB_DATABASE, TIDB_TABLE, INDEX_NAME, INDEX_KIND,
       TIFLASH_INSTANCE,
       ROWS_STABLE_INDEXED, ROWS_STABLE_NOT_INDEXED,
       ROWS_DELTA_INDEXED, ROWS_DELTA_NOT_INDEXED,
       ERROR_MESSAGE
FROM INFORMATION_SCHEMA.TIFLASH_INDEXES
WHERE TIDB_DATABASE = 'test'
  AND TIDB_TABLE = 'documents'
ORDER BY INDEX_NAME, TIFLASH_INSTANCE;
```

Identify the intended vector index by `INDEX_NAME` and inspect each TiFlash instance. Do not inspect only the first row. To observe progress, collect samples over time and record whether writes continue between samples.

| Observation | Interpretation and next action |
| --- | --- |
| `ERROR_MESSAGE` is nonempty | Save the error and investigate logs for the corresponding TiFlash instance. Do not assume the index is merely building slowly. |
| `ROWS_STABLE_NOT_INDEXED` is greater than 0 | Stable data remains unindexed. Observe its trend and check for errors. |
| `ROWS_STABLE_NOT_INDEXED` is 0, but `ROWS_DELTA_NOT_INDEXED` is greater than 0 | This Stable-layer check passes, but Delta data remains unindexed. Do not conclude that all data is indexed. |
| No rows are returned | Verify the database, table, index, and replica status. An empty result does not establish build completion. |

Recent writes can reside in the Delta layer, and query performance can differ from that of fully indexed data. Unindexed data does not mean unsearchable data. For query behavior during index building, see [View index build progress](/ai/reference/vector-search-index.md#view-index-build-progress).

`TIFLASH_INDEXES` is experimental and its fields can change. Check `DESC INFORMATION_SCHEMA.TIFLASH_INDEXES;` for your version before using the query. See [`TIFLASH_INDEXES`](/information-schema/information-schema-tiflash-indexes.md).

**Next step:** If data remains unindexed, retain samples showing its trend. Before manually triggering a Delta-to-Stable merge, review [View index build progress](/ai/reference/vector-search-index.md#view-index-build-progress) and [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md), including CPU and I/O costs. If these checks reveal no outstanding issue, compare first and subsequent executions.

## Step 3. Compare first and subsequent executions

If the original query uses the vector index but the first request is slower, add `EXPLAIN ANALYZE` before the original SQL. Keep its selected columns, filters, ordering, vector, and Top K unchanged. Record the first and subsequent executions under comparable conditions.

The following is a syntax example. Use the actual slow query during diagnosis; the simplified query cannot substitute for its timings:

```sql
EXPLAIN ANALYZE
SELECT id,
       VEC_COSINE_DISTANCE(embedding, '[1,2,3]') AS distance
FROM test.documents
ORDER BY distance
LIMIT 10;
```

`EXPLAIN ANALYZE` executes the query. Save the first output before repeating it. Keeping only later outputs can hide cold-access behavior.

Some versions include `vector_idx` information in `execution info` to help distinguish loading, search, and read overhead. Compare loading sources and durations across executions. For field explanations, see [Analyze vector search performance](/ai/reference/vector-search-index.md#analyze-vector-search-performance). These internal fields and formats can change; do not depend on a fixed structure for long-term monitoring.

If repeated queries become faster, investigate cold access. Before actual workload, you can warm up the index using representative vector queries. One faster query does not establish that the whole workload is warm. See [Improve Vector Search Performance](/ai/reference/vector-search-improve-performance.md).

**Next step:** If repeated executions remain slow, retain the evidence and investigate TiFlash resources. If database execution time does not explain application response time, investigate the application request path. `EXPLAIN ANALYZE` timing does not replace end-to-end timing for fetching the original results.

## Collect information for further investigation

When reporting the problem or contacting support, include the following information. Redact sensitive data, connection details, and logs before sharing them publicly. Explain if redaction changes the plan or reproduction results.

```text
- Deployment type, TiDB/TiKV/TiFlash versions, and TiFlash resource specifications:
- Incident time with time zone, normal/slow timings, and timing boundaries:
- Table definition, original SQL, vector dimension, Top K, and data size:
- Query concurrency and concurrent writes:
- Original EXPLAIN, SHOW WARNINGS, and session read-engine setting:
- Each EXPLAIN ANALYZE output with corresponding replica and index status:
- Actions attempted and before/after observations:
```

Keep timestamps, SQL, and instance identifiers aligned so that execution information can be compared with index status from the same period.

## See also

- [Vector Search Index](/ai/reference/vector-search-index.md)
- [Improve Vector Search Performance](/ai/reference/vector-search-improve-performance.md)
