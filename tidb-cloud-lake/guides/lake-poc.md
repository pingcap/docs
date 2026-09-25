# TiDB Cloud Lake PoC guide

This guide provides a repeatable proof of concept (PoC) for TiDB Cloud Lake.
Use a representative data sample and the real query shapes. Record query
latency, bytes scanned, rows scanned, warehouse size, concurrency, and storage
size before changing the layout so that every optimization has a comparable
baseline.

## 1. Configure an S3 bucket or PrivateLink

Choose the connectivity model before loading data:

- Use an S3 bucket when the source pipeline already writes Parquet, CSV, or
  JSON objects to object storage. In **Home > Connect**, obtain the Lake IAM
  role ARN and follow [Authenticate with AWS IAM
  Role](/tidb-cloud-lake/guides/aws-credentials.md) to configure the bucket,
  stage, and data load. Grant the role only the permissions required for the
  PoC prefix.
- Use PrivateLink when traffic must stay on a private network path. In **Home
  > Connect**, obtain the PrivateLink service and follow [Connect with AWS
  PrivateLink](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md). Verify
  the endpoint, security-group rules, DNS behavior, and route from the client
  or source cluster.

Test connectivity with a small object before starting the full load. Record
the bucket or endpoint, region, IAM policy, and expected cross-region network
cost. Do not put long-lived access keys in SQL or benchmark scripts.

## 2. Map the source schema before loading

Create a source-to-Lake mapping before the first full load. Check these fields
explicitly:

- decimal precision and scale;
- date, timestamp, and time-zone semantics;
- signed and unsigned integer ranges;
- `NULL` and default-value behavior; and
- maximum string length and character encoding.

Load a small sample and compare row counts, null counts, min/max values, and
aggregates with the source. For file loads, prefer compressed input when the
pipeline permits it. See [Load from local
file](/tidb-cloud-lake/guides/load-from-local-file.md) and [input and output
file formats](/tidb-cloud-lake/guides/input-output-file-formats.md) for
supported formats and compression settings.

## 3. Establish the performance baseline

The main factors affecting Lake query performance are:

1. **Warehouse resources.** CPU, memory, warehouse size, and concurrency limit
   determine how much work can run at once.
2. **Data layout.** Cluster-key order, overlap between blocks, block size, and
   partitioning determine how much data can be pruned.
3. **Cache and network path.** Memory or local-disk cache reduces repeated S3
   reads and network latency. Measure both cold-cache and warm-cache runs.
4. **Query shape.** Project only required columns and make selective predicates
   include the leading cluster-key columns where possible.

Capture `EXPLAIN` for each baseline query. If `TableScan` dominates, inspect
cluster-key pruning, overlap metrics, block size, cache hit rate, and warehouse
capacity before increasing concurrency.

## 4. Always choose a cluster key

Choose a cluster key when creating every table. Use columns that occur often in
filters, joins, or range scans, and put the most commonly used prefix first.
Keep key expressions narrow; for a long string, use a bounded prefix
expression. See the [cluster key guide](/tidb-cloud-lake/guides/cluster-key-performance.md)
for key design details.

```sql
CREATE TABLE lineitem (
  l_orderkey BIGINT NOT NULL,
  l_partkey INT NOT NULL,
  l_shipdate DATE NOT NULL,
  l_quantity DECIMAL(15, 2) NOT NULL,
  l_extendedprice DECIMAL(15, 2) NOT NULL
)
ENGINE = FUSE
CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey)
COMPRESSION = 'zstd'
ENABLE_AUTO_ANALYZE = '1'
STORAGE_FORMAT = 'parquet';
```

A table without a cluster key usually cannot prune effectively for range
predicates. If a table was created without one, add a key and recluster it
before comparing query performance:

```sql
ALTER TABLE lineitem CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey);
ALTER TABLE lineitem RECLUSTER FINAL;
```

## 5. Monitor overlap and run `RECLUSTER FINAL`

A cluster key does not impose one globally sorted file. Bulk loads and large
mutations can leave many blocks overlapping, which reduces pruning while keeping
ingestion fast. Run the following after the initial load and after a major data
change:

```sql
ALTER TABLE lineitem RECLUSTER FINAL;
```

Inspect `CLUSTERING_INFORMATION` before and after reclustering. Track
`average_depth`, `p95_depth`, and `average_overlaps` together with query bytes
scanned and latency. A practical starting target is `p95_depth < 32`, but the
acceptable value must be validated against the workload.

For continuously changing tables, schedule reclustering from the observed
overlap trend and measure its compute cost. If overlap repeatedly returns,
revisit the cluster key and partition design instead of only reclustering more
often.

## 6. Choose an appropriate block size

Start with a block size that matches the write pattern:

- For large appends and analytical reads, evaluate approximately 512 MB:
  `BLOCK_SIZE_THRESHOLD = '536870912'`.
- For frequent small inserts, updates, or deletes, evaluate smaller blocks to
  reduce rewrite cost and write amplification.

Use the same representative load and queries for each trial. Record load time,
storage size, bytes scanned, reclustering time, and query latency. A larger
block is not automatically faster: it can increase the cost of small mutations
and reduce the value of pruning for selective queries.

## 7. Use materialized views for repeated aggregation

When the workload repeatedly aggregates one table at the same grain, use a
materialized view to pre-aggregate the hot dimensions. Keep the base-table and
view cluster keys aligned with the dashboard predicates, then compare the view
query with the baseline query under the same warehouse and cache conditions.

```sql
CREATE MATERIALIZED VIEW mv_account_daily
CLUSTER BY (tenant_id, account)
AS
SELECT
  tenant_id,
  account,
  category_id,
  SUM(amount) AS total_amount
FROM fact_table
GROUP BY tenant_id, account, category_id;
```

Validate refresh latency, freshness, storage overhead, and query-result
equivalence. Materialized views are best suited to single-table aggregation;
check current feature limits before using window functions or a deduplication
pattern. See the [TiDB Cloud Lake materialized view
documentation](/tidb-cloud-lake/sql/materialized-view.md).

## PoC acceptance checklist

- [ ] S3 or PrivateLink connectivity, region, IAM scope, and network path are recorded.
- [ ] Source and Lake schemas match for precision, time zones, nulls, and string lengths.
- [ ] Baseline `EXPLAIN`, latency, bytes scanned, rows scanned, and warehouse settings are saved.
- [ ] Every table has a workload-aligned cluster key.
- [ ] Overlap metrics are captured before and after `RECLUSTER FINAL`.
- [ ] Block size is justified by the append-to-mutation ratio and measured results.
- [ ] Materialized-view freshness, storage cost, and query speed are compared with the baseline.
