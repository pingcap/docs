---
title: TiDB Cloud Lake PoC Guide
summary: Evaluate TiDB Cloud Lake with a representative workload using schema mapping, cluster keys, reclustering, block sizes, and materialized views.
---

# TiDB Cloud Lake PoC Guide

This guide describes a repeatable proof of concept (PoC) for TiDB Cloud Lake.
It focuses on the decisions that have the largest impact on a representative
workload: object-storage and PrivateLink connectivity, schema compatibility, data
layout, overlap maintenance, block size, and pre-aggregation.

Run the PoC with a representative data sample and the query shapes used in
production. Record query latency, QPS, warehouse size, and storage size so that
you can compare each optimization with the same baseline.

## 1. Configure an S3 connection

Use an S3 bucket when the source pipeline already writes Parquet, CSV, or
JSON objects to object storage. In **Home > Connect**, obtain the IAM role ARN
for your TiDB Cloud Lake deployment and follow [Authenticate with AWS IAM
Role](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md)
to configure the S3 connection, stage, and data load.

## 2. Configure PrivateLink

Use PrivateLink when traffic must stay on a private network path. In **Home >
Connect**, obtain the PrivateLink service and follow [Connect with AWS
PrivateLink](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md)
to configure the connection. Verify the endpoint, security-group rules, DNS
behavior, and route from the client or source cluster before starting the load.

## 3. Use Data Pipeline to replicate data from a TiDB Cloud Premium instance to TiDB Cloud Lake

Use TiDB Cloud Data Pipeline to replicate data from a TiDB Cloud Premium
instance to TiDB Cloud Lake without introducing a third-party ETL tool. Data
Pipeline first exports a full snapshot of the selected source data and then
continuously replicates row-level changes so that the data in TiDB Cloud Lake
stays up to date.

Data Pipeline uses TiCDC for incremental replication and an external stage to
transfer data between TiDB Cloud and TiDB Cloud Lake. Before starting the PoC,
verify that the required feature is available for your TiDB Cloud plan and that
the external stage and access policy are configured. For current availability
and configuration requirements, see [Data Pipeline to TiDB Cloud
Lake](https://docs.pingcap.com/tidbcloud/data-pipeline-sink-to-lake/).

For the PoC, select representative tables and record their schemas, expected
row counts, and freshness targets. After the initial snapshot completes,
compare row counts, null counts, sample aggregates, and minimum and maximum
values with the source. Then generate representative inserts, updates, and
deletes in the source and verify that TiDB Cloud Lake reflects them within the
expected replication latency. Record snapshot duration, replication lag,
rejected records, and schema-mapping errors before using the replicated tables
for query-performance tests.

### Map and validate the source schema

Before loading files or starting replication, record each source column and its
target Lake column, data type, nullability, default value, and any required
conversion. Check decimal precision and scale, signed and unsigned integer
ranges, timestamp precision and time zones, and string encoding. Use the
[Lake data types reference](/tidb-cloud-lake/sql/data-types.md) to choose target
types; do not assume that matching type names have identical semantics.

Load a small sample that includes nulls and boundary values. Compare row and
null counts, minimum and maximum values, and aggregates with the source at the
same snapshot or replication checkpoint. Verify that conversions preserve
precision and timestamp meaning, and investigate rejected or truncated values
before starting the full load.

## 4. Establish the performance baseline

The main factors affecting Lake query performance are:

1. **Warehouse resources.** CPU, memory, warehouse size, and concurrency limit
   determine how much work can run at once.
2. **Data layout.** Cluster-key order, block overlap, and block size determine
   how much data can be pruned.
3. **Query shape.** Project only required columns and make selective predicates
   include the leading cluster-key columns where possible.

Capture `EXPLAIN` output for each baseline query. If `TableScan` dominates,
inspect cluster-key pruning, overlap metrics, block size, cache hit rate, and
warehouse capacity before increasing concurrency.

## 5. Choose a cluster key when the workload benefits

Evaluate a cluster key when creating a large table with predictable filters or
range scans. Small tables, random access patterns, and frequent changes might
not benefit enough to justify the maintenance cost. Use columns that frequently
appear in filters, joins, or range scans, and put the most commonly filtered
columns first. Keep key expressions narrow; for a long string, use a bounded
prefix expression.

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
STORAGE_FORMAT = 'parquet';
```

If range predicates scan many blocks on a large table without a cluster key,
evaluate adding a key and reclustering before comparing query performance.

```sql
ALTER TABLE lineitem CLUSTER BY (DATE_TRUNC(MONTH, l_shipdate), l_orderkey);
ALTER TABLE lineitem RECLUSTER FINAL;
```

See the [cluster key guide](/tidb-cloud-lake/guides/cluster-key-performance.md)
for key design details.

## 6. Monitor overlap and run `RECLUSTER FINAL`

A cluster key does not impose one globally sorted file. Bulk loads and large
mutations can leave many blocks overlapping, reducing pruning while keeping
ingestion fast. Run the following after the initial load and after a major data
change when the overlap metrics indicate that it is needed. Pause writes,
including replication into the table, during the operation. Do not perform DML
while `RECLUSTER` runs. For details, see [RECLUSTER TABLE](/tidb-cloud-lake/sql/recluster-table.md).

```sql
ALTER TABLE lineitem RECLUSTER FINAL;
```

Inspect [CLUSTERING_INFORMATION](/tidb-cloud-lake/sql/clustering-information.md)
before and after reclustering. Track `average_overlaps`, `average_depth`, and
`block_depth_histogram` together with bytes scanned and query latency. Lower
depth and overlap generally indicate better clustering. Compare the same
workload before and after reclustering to establish a useful maintenance
threshold for your data distribution.

```sql
CREATE TABLE mytable(a INT, b INT) CLUSTER BY (a + 1);

INSERT INTO mytable VALUES (1, 1), (3, 3);
INSERT INTO mytable VALUES (2, 2), (5, 5);
INSERT INTO mytable VALUES (4, 4);

SELECT * FROM CLUSTERING_INFORMATION('default', 'mytable')\G
*************************** 1. row ***************************
            cluster_key: ((a + 1))
      total_block_count: 3
   constant_block_count: 1
 unclustered_block_count: 0
       average_overlaps: 1.3333
          average_depth: 2.0
   block_depth_histogram: {"00002":3}
```

The following metric summary illustrates relatively moderate overlap. These
values are not universal healthy thresholds or the function's full output:

```json
{
  "cluster_key": "(yyyymm)",
  "info": {
    "average_depth": 40.6131,
    "average_overlaps": 40.7653,
    "total_block_count": 473
  },
  "type": "linear"
}
```

The following metric summary shows severe overlap: `average_depth` is close to
the total block count. Review query scans and latency, schedule reclustering,
and revisit the cluster-key design if this pattern persists:

```json
{
  "cluster_key": "(DATE_TRUNC(MONTH, l_shipdate), l_orderkey)",
  "info": {
    "average_depth": 10181.3357,
    "average_overlaps": 10211.5616,
    "total_block_count": 10214
  },
  "type": "linear"
}
```

For continuously changing tables, schedule reclustering during a maintenance
window when DML and replication writes are paused. Choose the schedule based on
the observed overlap trend and measure its compute cost. The following hourly
task is an example; it does not pause writers, so coordinate the maintenance
window before resuming it:

```sql
CREATE OR REPLACE TASK lineitem_hourly
  WAREHOUSE = 'default'
  SCHEDULE = 60 MINUTE
  COMMENT = 'Hourly FINAL recluster for lineitem'
AS
  ALTER TABLE lineitem RECLUSTER FINAL;

ALTER TASK lineitem_hourly RESUME;
```

## 7. Choose an appropriate block size

Start with a block size that matches the write pattern:

- For large appends and analytical reads, evaluate a threshold of 536870912
  bytes (512 MiB).
- For frequent small inserts, updates, or deletes, evaluate smaller blocks to
  reduce rewrite cost and write amplification.

Apply the option before loading the PoC data:

```sql
ALTER TABLE lineitem SET OPTIONS (BLOCK_SIZE_THRESHOLD = 536870912);
```

This is a starting point for evaluation, not a universal default. Compare load
time, write cost, bytes scanned, and query latency with the same data and queries.

## 8. Use materialized views for repeated aggregation

When the workload repeatedly aggregates one table at the same granularity, use
a materialized view to pre-aggregate the frequently queried dimensions. Keep
the base-table and view cluster keys aligned with the dashboard predicates,
then refresh the view before comparing its query with the baseline under the
same warehouse and cache conditions. Creation records the definition; the
first refresh populates physical storage.

```sql
CREATE TABLE fact_table (
  tenant_id INT,
  account BIGINT,
  category_id INT,
  amount DECIMAL(19, 6)
);

-- Load representative data into fact_table before benchmarking.
CREATE MATERIALIZED VIEW mv_account_totals
  (tenant_id, account, category_id, total_amount)
CLUSTER BY (tenant_id, account)
AS
SELECT
  tenant_id,
  account,
  category_id,
  SUM(amount) AS total_amount
FROM fact_table
GROUP BY tenant_id, account, category_id;

REFRESH MATERIALIZED VIEW mv_account_totals;
```

Materialized views are best suited to single-table aggregation. See the
[TiDB Cloud Lake materialized view documentation](/tidb-cloud-lake/sql/materialized-view.md).
