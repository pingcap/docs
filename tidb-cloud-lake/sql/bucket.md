---
title: BUCKET
summary: Maps a supported value to one of a fixed number of hash buckets.
---

# BUCKET

Maps a supported value to one of a fixed number of hash buckets. `BUCKET()` returns a deterministic `UInt32` value from `0` through `bucket_count - 1` and is designed for [`PARTITION BY`](/tidb-cloud-lake/guides/partition-by.md) and `CLUSTER BY` expressions.

## Syntax

```sql
BUCKET(<bucket_count>, <value>)
```

## Arguments

| Argument | Description |
|----------|-------------|
| `bucket_count` | An integer from `1` through `4294967295`. In a `PARTITION BY` or `CLUSTER BY` expression, it must be a constant literal. |
| `value` | An integer, string, date, or timestamp value to hash. |

The function returns `NULL` when either argument is `NULL`.

> **Note:**
>
> Bucket results are stable for a value's data type, but the same logical value represented by different data types can map to different buckets. Avoid changing the data type of a bucketed key.

## Examples

```sql
-- Returns an integer from 0 through 15.
SELECT BUCKET(16, 'customer-123');
```

Use a fixed bucket count to partition a high-cardinality key:

```sql
CREATE TABLE customer_events (
    customer_id BIGINT,
    event_time  TIMESTAMP,
    payload     VARIANT
)
PARTITION BY (BUCKET(32, customer_id));
```

For distributed ingestion, rows with the same evaluated partition value can be routed to the same writer:

```sql
CREATE TABLE customer_events_distributed (
    customer_id BIGINT,
    event_time  TIMESTAMP
)
PARTITION BY (BUCKET(32, customer_id))
WRITE_DISTRIBUTION_MODE = 'hash';
```

`WRITE_DISTRIBUTION_MODE = 'hash'` requires a `PARTITION BY` clause.
