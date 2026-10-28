---
title: Partitioning Fuse Tables
summary: Learn how to partition Fuse tables in TiDB Cloud Lake for faster query pruning and predictable data layout.
---

# Partitioning Fuse Tables for Faster Pruning and Predictable Data Layout

`PARTITION BY` physically separates a Fuse table into partitions. {{{ .lake }}} keeps blocks and segments from different partition values separate, records the partition values in metadata, and prunes partitions that cannot match a query predicate.

Use partitioning when large tables are commonly filtered by time ranges, tenant or region identifiers, or another stable dimension. For high-cardinality keys, use `BUCKET()` to create a fixed number of hash partitions.

## What Problem Does It Solve?

| Problem | Impact | `PARTITION BY` solution |
|---------|--------|-------------------------|
| Queries target a small slice of a large table | Unrelated segments and blocks must be inspected | Partition metadata eliminates unrelated partitions before scanning |
| Time-series data spans many days or months | Recent-period queries read historical data | A date expression groups data into time partitions |
| A natural key has very high cardinality | One partition per value creates excessive fragmentation | `BUCKET()` maps values to a fixed number of hash partitions |
| Distributed writers produce many small blocks | The same partition can be written independently on several nodes | Hash write distribution routes each partition value to one writer |

## Partitioning vs. Clustering

`PARTITION BY` and `CLUSTER BY` are complementary:

| Feature | `PARTITION BY` | `CLUSTER BY` |
|---------|----------------|--------------|
| Physical guarantee | Blocks and segments do not cross partition boundaries | Rows are sorted and related values are colocated |
| Main benefit | Partition-level pruning and isolation | Fine-grained block pruning within partitions |
| Typical cardinality | Low or bounded | Medium to high |
| Typical expressions | `DATE_TRUNC(day, event_time)`, `region`, `BUCKET(32, customer_id)` | `event_time`, `customer_id`, `(region, event_time)` |
| Maintenance | Preserved by writes, mutations, compaction, and reclustering | Maintained through clustering and reclustering |

You can use both on one table. The partition key does not become part of the user-visible cluster key:

```sql
CREATE TABLE events (
    event_time TIMESTAMP,
    tenant_id  BIGINT,
    payload    VARIANT
)
PARTITION BY (DATE_TRUNC(day, event_time))
CLUSTER BY (tenant_id, event_time);
```

## Quick Setup

Create a table partitioned by day:

```sql
CREATE TABLE events (
    event_id   BIGINT,
    event_time TIMESTAMP,
    event_type STRING
)
PARTITION BY (DATE_TRUNC(day, event_time));
```

All subsequent writes honor the partition boundary:

```sql
INSERT INTO events VALUES
    (1, '2026-07-08 10:00:00', 'login'),
    (2, '2026-07-08 18:30:00', 'purchase'),
    (3, '2026-07-09 09:15:00', 'logout');
```

A time predicate can then prune unrelated day partitions:

```sql
EXPLAIN
SELECT *
FROM events
WHERE event_time >= TIMESTAMP '2026-07-08'
  AND event_time <  TIMESTAMP '2026-07-09';
```

In the `EXPLAIN` output, compare `partitions total` with `partitions scanned` and check the `range pruning` statistics. Fewer scanned partitions indicate that partition pruning was applied.

## Partitioning Strategies

This section describes different strategies for partitioning Fuse tables in {{{ .lake }}}.

### Time-Based Partitioning

Apply a deterministic expression to a timestamp or date column:

```sql
-- Daily partitions
PARTITION BY (DATE_TRUNC(day, event_time))

-- Monthly partitions
PARTITION BY (DATE_TRUNC(month, event_time))
```

Choose a granularity that matches common filters while keeping each partition large enough to avoid fragmentation. Daily partitions usually suit high-volume event data; monthly partitions often work better for lower-volume historical data.

### Identity Partitioning

Use the column directly when it already has a small, stable set of values:

```sql
CREATE TABLE regional_sales (
    region     STRING,
    order_id   BIGINT,
    order_date DATE,
    amount     DECIMAL(18, 2)
)
PARTITION BY (region);
```

Good identity keys include region, country, tenant tier, or another bounded business dimension. Avoid partitioning directly by unique IDs.

### Hash Partitioning with `BUCKET()`

`BUCKET(<count>, <column>)` deterministically maps supported values to an unsigned partition number in the range `0` through `<count> - 1`. The bucket count must be a constant integer from `1` through `4294967295`.

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

Bucket partitioning is useful when equality filters target a high-cardinality column but creating one physical partition per distinct value would be impractical.

Supported `BUCKET()` value types are integers, strings, dates, and timestamps. See [`BUCKET()`](/tidb-cloud-lake/sql/bucket.md) for details.

### Composite Partitioning

List multiple expressions to form a composite partition key:

```sql
CREATE TABLE tenant_events (
    tenant_id  BIGINT,
    event_time TIMESTAMP,
    payload    VARIANT
)
PARTITION BY (
    DATE_TRUNC(month, event_time),
    BUCKET(16, tenant_id)
);
```

Each partition expression must reference exactly one source column. To partition by two columns, use separate expressions as shown above; an expression such as `tenant_id + another_id` is not valid.

## Hash-Distributed Writes

For distributed or highly parallel ingestion into partitioned tables, set `WRITE_DISTRIBUTION_MODE = 'hash'`:

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

This mode hashes the evaluated partition key and routes rows with the same partition value to the same writer before local sorting. It can reduce small-block fragmentation when several nodes or pipelines write the same partitions concurrently.

`WRITE_DISTRIBUTION_MODE` accepts:

- `'none'` (default): Do not redistribute rows before writing.
- `'hash'`: Redistribute rows by the partition key before writing. This value requires `PARTITION BY`.

Hash redistribution adds a network shuffle. Enable it for distributed or parallel loads where improved block layout outweighs the shuffle cost; it may not benefit small, single-writer inserts.

## Adding Partitioning to an Existing Table

Add a partition key to an existing Fuse table with `ALTER TABLE`:

```sql
ALTER TABLE events
PARTITION BY (DATE_TRUNC(day, event_time));
```

Rows written before this statement remain visible, but their existing segments do not gain partition metadata or get physically reorganized. New writes use the partitioned layout.

> **Important:**
>
> A partition key can be added only once. Repeating the same normalized definition is harmless, but changing an existing partition key is not supported. Choose the key carefully before applying it to a production table.

## Expression Rules and Table Changes

For Fuse table partition expressions:

- Each expression must be deterministic and reference exactly one source column.
- Use multiple expressions—not one multi-column expression—for composite partitioning.
- `BUCKET()` requires a constant bucket count from `1` through `4294967295`.
- Columns referenced by the partition key cannot be dropped or have their data types changed.
- Renaming a referenced column updates the stored partition expression.
- The internal `partition_by` metadata cannot be changed with `SET OPTIONS`.
- `PARTITION BY` is supported for Fuse tables. Other engines may implement different partitioning syntax and semantics.

## Best Practices

| Practice | Why it helps |
|----------|--------------|
| Match partition expressions to frequent filters | Enables the optimizer to eliminate partitions early |
| Prefer low or bounded cardinality | Avoids excessive small partitions and metadata |
| Use `BUCKET()` for high-cardinality equality keys | Keeps partition count predictable |
| Combine partitioning with a cluster key | Adds fine-grained pruning inside each partition |
| Test with representative ingestion concurrency | Determines whether hash-distributed writes reduce fragmentation |
| Verify with `EXPLAIN` | Confirms that predicates reduce `partitions scanned` |

> **Tip:**
>
> Good Candidates:
>
> - Event and log tables filtered by day or month
> - Multi-tenant tables filtered by tenant
> - Regional or categorical datasets with bounded values
> - High-cardinality equality lookups using a fixed bucket count

> **Note:**
>
> **When Not to Partition:** Small tables, tables without stable filter patterns, and keys that create many tiny partitions generally do not benefit from physical partitioning. In those cases, a [cluster key](/tidb-cloud-lake/guides/cluster-key-performance.md) alone may be a better fit.
