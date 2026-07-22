---
title: Tiered Storage Operations Guide
summary: Learn how to configure and manage Tiered Storage on TiDB Cloud Essential, including DDL, partition selectors, observability, and best practices.
---

# Tiered Storage Operations Guide

> **Note:**
>
> - **Version:** Private Preview
> - **Platform:** TiDB Cloud Essential
> - This document reflects the current system state only. Some behaviors may change when the feature reaches GA.

---

## How to use

### Storage class support matrix

#### Storage class values

| Value | Meaning | Default |
|-|-|-|
| `Standard` | Local hot storage, full data on local disk | Yes |
| `IA` | Remote cold storage, full data in object storage, local on-demand caching | No |

Values are case-insensitive.

#### Supported table types

| Table Type | IA Support | Notes |
|-|-|-|
| Regular non-partitioned table | Supported | Via `STORAGE_CLASS` syntactic sugar or `ENGINE_ATTRIBUTE` |
| Range partitioned table | Supported | Must use `ENGINE_ATTRIBUTE` |
| Range Columns partitioned table | Supported | Must use `ENGINE_ATTRIBUTE` |
| List partitioned table | Supported | Must use `ENGINE_ATTRIBUTE` |
| List Columns partitioned table | Supported | Must use `ENGINE_ATTRIBUTE` |
| Hash partitioned table | **Not supported** | — |
| Key partitioned table | **Not supported** | — |

#### Storage type inheritance rules for indexes and related objects

| Object | Inheritance Rule |
|-|-|
| Regular table index | Same as the table |
| Partitioned table Local Index | Same as the owning partition |
| Partitioned table Global Index | Same as the table-level setting |
| TiFlash | **Does not follow table storage settings** |

### Regular table DDL

#### Specifying at create time

Syntactic sugar (recommended):

```SQL
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    payload VARCHAR(256) NOT NULL
) ENGINE=InnoDB STORAGE_CLASS='IA';
```

`ENGINE_ATTRIBUTE` method:

```SQL
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY
) ENGINE_ATTRIBUTE='{"storage_class":"IA"}';
```

> **Conflict constraint**: `STORAGE_CLASS` syntactic sugar and `ENGINE_ATTRIBUTE`'s `storage_class` **cannot be specified together** — the system will reject with an error.

#### Modifying an existing table

```SQL
-- Standard → IA
ALTER TABLE t1 STORAGE_CLASS='IA';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}';

-- IA → Standard
ALTER TABLE t1 STORAGE_CLASS='STANDARD';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"STANDARD"}';
```

ALTER operations preserve all data access, and SQL reads/writes are not affected during the conversion.

### Partitioned table DDL

Partitioned tables **do not support** the `STORAGE_CLASS` syntactic sugar and must use `ENGINE_ATTRIBUTE`.

Partition attributes support three selector types (cannot be mixed) plus a table-level default:

| Configuration Method | Syntax | Applicable Partition Types | Purpose |
|-|-|-|-|
| Table-level default | `{"storage_class":"IA"}` | All | Set all partitions to IA uniformly |
| By partition name | `"names_in":["p1","p2"]` | All | Specify an exact list of partition names |
| By range | `"less_than":"2024-01-01"` | RANGE / RANGE COLUMNS | Match partitions by boundary value |
| By list value | `"values_in":["1","2"]` | LIST / LIST COLUMNS | Match partitions by list value |

#### Example A: table-level IA with specific partitions overridden to Standard

```SQL
CREATE TABLE orders (
    order_id BIGINT NOT NULL,
    created_at DATETIME NOT NULL,
    PRIMARY KEY (order_id, created_at)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia"},
        {"tier":"standard","names_in":["p2025","p_future"]}
    ]
}'
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

Result: p2023 / p2024 → IA, p2025 / p_future → Standard.

#### Example B: range selector

```SQL
CREATE TABLE users (
    user_id BIGINT NOT NULL,
    PRIMARY KEY (user_id)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","less_than":"2000000"}
    ]
}'
PARTITION BY RANGE (user_id) (
    PARTITION p0 VALUES LESS THAN (1000000),
    PARTITION p1 VALUES LESS THAN (2000000),
    PARTITION p2 VALUES LESS THAN (3000000),
    PARTITION p3 VALUES LESS THAN MAXVALUE
);
```

Result: p0 / p1 → IA, p2 / p3 → Standard.

#### Example C: list value selector

```SQL
CREATE TABLE order_status_log (
    log_id BIGINT NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (log_id, status)
) ENGINE_ATTRIBUTE='{
    "storage_class":[
        {"tier":"ia","values_in":["1","2"]}
    ]
}'
PARTITION BY LIST (status) (
    PARTITION p_pending VALUES IN (1),
    PARTITION p_paid VALUES IN (2),
    PARTITION p_shipped VALUES IN (3),
    PARTITION p_completed VALUES IN (4)
);
```

Result: p_pending / p_paid → IA, p_shipped / p_completed → Standard.

#### Partition selector rules

- **Priority**: Partition-level configuration **overrides** table-level configuration
- **Mutual exclusion**: Multiple matching methods (e.g., `"names_in"` and `"less_than"`) cannot be used together in the same selector — this will raise an error
- **Forward compatibility**: New partitions added later (`ADD PARTITION` / `REORGANIZE PARTITION`) are automatically evaluated against the persistent storage class rules; matching partitions inherit the configuration

### Viewing and monitoring

```SQL
-- View DDL definition
SHOW CREATE TABLE t1\G

-- View table-level storage type
SELECT TABLE_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';

-- View partition-level storage type
SELECT PARTITION_NAME, TIDB_STORAGE_CLASS
FROM INFORMATION_SCHEMA.PARTITIONS
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table';
```

#### Monitoring IA storage space

View in Cloud Console:

- **Path**: Cloud Console → Monitoring → Metrics → Instance Overview (or Overview → Core Metrics)
- **New metrics**:
    - `Row-based IA Storage` — Total IA table space
    - `Row-based Standard Storage` — Total Standard table space
- **Relationship**: `Row-based Storage` = `Row-based IA Storage` + `Row-based Standard Storage`

The single-table space query method remains unchanged:

> Note: This method depends on table statistics and may have significant estimation errors.

```SQL
SELECT TABLE_NAME,
    ROUND(DATA_LENGTH / 1024 / 1024, 2) AS Data_MB,
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS Index_MB,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

---

## Observability

### EXPLAIN ANALYZE

When a query involves remote data loading, the `scan_detail` includes new fields:

```SQL
EXPLAIN ANALYZE SELECT * FROM t_ia WHERE id BETWEEN 1 AND 50000;
-- The output includes:
-- ia_remote_read_segment_size: 2320453     -- Total bytes loaded remotely
-- ia_remote_read_segment_count: 3           -- Number of remote loading events
-- ia_remote_read_segment_wait_time: 0.008   -- Remote wait time (seconds)
```

> Note: The IA signal is per-request read path evidence, not a table-level stable flag — the same query may show IA information on the first run but not after a cache hit.
>
> Additionally, ia_remote_read_segment_wait_time is the aggregate time of all remote requests. Due to TiKV's underlying parallel reading mechanism, this value may exceed the SQL's actual execution time.

### Statement summary

`STATEMENTS_SUMMARY_HISTORY` and `CLUSTER_STATEMENTS_SUMMARY_HISTORY` have 6 new columns:

| Column Name | Description |
|-|-|
| `AVG_IA_REMOTE_READ_SEGMENT_COUNT` | Average number of remote segments read |
| `MAX_IA_REMOTE_READ_SEGMENT_COUNT` | Maximum number of remote segments read |
| `AVG_IA_REMOTE_READ_SEGMENT_SIZE` | Average remote read data volume |
| `MAX_IA_REMOTE_READ_SEGMENT_SIZE` | Maximum remote read data volume |
| `AVG_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | Average remote wait time |
| `MAX_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | Maximum remote wait time |

### Slow queries

`INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` has 3 new columns:

- `IA_remote_read_segment_count`
- `IA_remote_read_segment_size`
- `IA_remote_read_segment_wait_time`

Corresponding panels are also visible in the Cloud Console slow query details.

---

## Best practices

### Tiering strategy: prefer partition-level IA

For partitioned tables, **always prefer partition-level IA** over table-level IA. This gives you precise control over cold/hot boundaries:

- Historical cold partitions (e.g., `p2023`) → IA
- Recent hot partitions (e.g., `p2025`) → Standard
- Future partitions (e.g., `p_future`) → Standard

### Rollout strategy: start with the smallest oldest partition

```Plaintext
Step 1: Select the oldest and smallest partition → ALTER PARTITION → IA
Step 2: Observe for one full business day (at least 24h)
Step 3: Verify QPS / TPS / P99 Latency / CPU metrics show no degradation
Step 4: Set the next cold partition → IA one by one
Step 5: Repeat Steps 2-4 until all target partitions are covered
```

**Do not batch-set all partitions to IA at once.**

### Write optimization

- When importing concurrently into IA partitions, having each thread target a different IA partition reduces lock contention and improves throughput. Test environment measurements: random writes to IA partitions averaged 50k rows/sec; fixed single-thread writes to the same IA partition averaged 70k rows/sec (~40% improvement).
- Newly imported data only transitions to IA mode after flush/compaction. Large-range queries immediately after import may encounter cold cache.

> These figures are from test environments and do not represent real-world production scenarios. You should obtain accurate data based on your own business testing.

### Query optimization

- Queries spanning IA partitions are recommended to cover **no more than 3 partitions**; exceeding this may cause significant response time degradation
- Avoid running many `SELECT *` full table scans on IA tables simultaneously
- Monitor IA remote read volume via `EXPLAIN ANALYZE` and slow queries, and adjust accordingly

### Switch-back considerations

- IA → Standard conversion downloads all data from S3, generating significant cold storage bandwidth usage
- Monitor bandwidth usage to ensure smooth operation; if necessary, **contact the TiDB Cloud team in advance** for joint monitoring
- Business SQL reads/writes are not affected during conversion, but performance (e.g., QPS/TPS) may have minor impact — test environment shows less than 5%

### Configuration stability

Keep the storage class setting stable and avoid frequent switching between IA and Standard. Each switch triggers:

- Region reload
- S3 data download or metadata rebuild
- IA cache data flushing

The cumulative cost of these operations is not negligible.
