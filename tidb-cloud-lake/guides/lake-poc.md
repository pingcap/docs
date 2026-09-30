# TiDB Cloud Lake PoC guide

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
Role](https://docs.pingcap.com/tidbcloudlake/authenticate-with-aws-iam-role/)
to configure the S3 connection, stage, and data load.


## 2. Configure PrivateLink

Use PrivateLink when traffic must stay on a private network path. In **Home >
Connect**, obtain the PrivateLink service and follow [Connect with AWS
PrivateLink](https://docs.pingcap.com/tidbcloudlake/connect-with-aws-privatelink/)
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
Lake](https://docs.pingcap.com/tidb-cloud/data-pipeline/data-pipeline-overview.md).

For the PoC, select representative tables and record their schemas, expected
row counts, and freshness targets. After the initial snapshot completes,
compare row counts, null counts, sample aggregates, and minimum and maximum
values with the source. Then generate representative inserts, updates, and
deletes in the source and verify that TiDB Cloud Lake reflects them within the
expected replication latency. Record snapshot duration, replication lag,
rejected records, and schema-mapping errors before using the replicated tables
for query-performance tests.

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

## 5. Always choose a cluster key

Choose a cluster key when creating every table. Use columns that frequently
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
ENABLE_AUTO_ANALYZE = '1'
STORAGE_FORMAT = 'parquet';
```

A table without a cluster key usually cannot prune effectively for range
predicates. If a table was created without one, add a key and recluster it
before comparing query performance.

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
change:

```sql
ALTER TABLE lineitem RECLUSTER FINAL;
```

Inspect `CLUSTERING_INFORMATION` before and after reclustering. Track
`average_overlaps`, `average_depth`, `p95_depth`, and `p99_depth` together with
bytes scanned and query latency. Use these metrics to compare the same workload
before and after reclustering. A practical starting target is `p95_depth < 32`,
but validate the threshold against your workload and data distribution.

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

The following is an illustrative result with relatively moderate overlap. The
values are examples, not universal healthy thresholds:

```json
{
  "cluster_key": "(yyyymm)",
  "info": {
    "average_depth": 40.6131,
    "average_overlaps": 40.7653,
    "p95_depth": 42,
    "p99_depth": 42,
    "total_block_count": 473
  },
  "type": "linear"
}
```

The following result shows severe overlap. A `p95_depth` above 10,000 indicates
that reclustering should be scheduled promptly and that the cluster-key design
should be reviewed:

```json
{
  "cluster_key": "(DATE_TRUNC(MONTH, l_shipdate), l_orderkey)",
  "info": {
    "average_depth": 10181.3357,
    "average_overlaps": 10211.5616,
    "p95_depth": 10182,
    "p99_depth": 10182,
    "total_block_count": 10214
  },
  "type": "linear"
}
```

For continuously changing tables, create a task to recluster the table and
maintain acceptable overlap. Schedule it according to the observed overlap
trend and measure its compute cost:

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

- For large appends and analytical reads, evaluate approximately 512 MB:
  `BLOCK_SIZE_THRESHOLD = '536870912'`.
- For frequent small inserts, updates, or deletes, evaluate smaller blocks to
  reduce rewrite cost and write amplification.

As a starting point, choose a larger block of approximately 512 MB for large
append workloads.

## 8. Use materialized views for repeated aggregation

When the workload repeatedly aggregates one table at the same granularity, use
a materialized view to pre-aggregate the frequently queried dimensions. Keep
the base-table and view cluster keys aligned with the dashboard predicates,
then compare the view query with the baseline query under the same warehouse
and cache conditions.

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

Materialized views are best suited to single-table aggregation. See the
[TiDB Cloud Lake materialized view documentation](/tidb-cloud-lake/sql/materialized-view.md).