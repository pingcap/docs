---
title: Configure and Manage Tiered Storage
summary: Learn how to configure and manage tiered storage on TiDB Cloud Premium or BYOC, including DDL, partition selectors, and best practices.
---

# Configure and Manage Tiered Storage

This document explains how to configure and manage Infrequent Access (IA) storage, including storage class settings, partition selectors, and recommended operational practices.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .premium }}} and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

## How to use

This section describes how to configure and manage IA storage, including storage class settings, partition selectors, and recommended operational practices.

### Storage class support matrix

This section describes the supported storage class values, table types, and inheritance rules for indexes and related objects.

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
| Range partition | Supported | Must use `ENGINE_ATTRIBUTE` |
| Range Columns partition | Supported | Must use `ENGINE_ATTRIBUTE` |
| List partition | Supported | Must use `ENGINE_ATTRIBUTE` |
| List Columns partitions | Supported | Must use `ENGINE_ATTRIBUTE` |
| Hash partitions | **Not supported** | — |
| Key partitions | **Not supported** | — |

#### Storage type inheritance rules for indexes and related objects

| Object | Inheritance Rule |
|-|-|
| Regular table index | Same as the table |
| Partitioned table Local Index | Same as the owning partition |
| Partitioned table Global Index | Same as the table-level setting |
| TiFlash | **Does not follow table storage settings** |

### Regular table DDL

This section describes how to configure IA storage for regular (non-partitioned) tables.

#### Specify at create time

Syntactic sugar (recommended):

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY,
    created_at DATETIME NOT NULL,
    payload VARCHAR(256) NOT NULL
) ENGINE=InnoDB STORAGE_CLASS='IA';
```

`ENGINE_ATTRIBUTE` method:

```sql
CREATE TABLE t_ia (
    id BIGINT PRIMARY KEY
) ENGINE_ATTRIBUTE='{"storage_class":"IA"}';
```

**Conflict constraint**: `STORAGE_CLASS` syntactic sugar and `ENGINE_ATTRIBUTE`'s `storage_class` **cannot be specified together** — the system will reject with an error.

#### Modify an existing table

```sql
-- Standard → IA
ALTER TABLE t1 STORAGE_CLASS='IA';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}';

-- IA → Standard
ALTER TABLE t1 STORAGE_CLASS='STANDARD';
ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"STANDARD"}';
```

`ALTER` operations preserve all data access, and SQL reads/writes are supported during the conversion.

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

```sql
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

```sql
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

```sql
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

### View and monitor

```sql
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

#### Monitor IA storage space

View in TiDB Cloud console:

- Path: **Overview** > **Monitoring** > **Metrics** > **Instance Overview** (or **Overview** > **Core Metrics**)
- New metrics:
    - `Row-based IA Storage` — Total IA table space
    - `Row-based Standard Storage` — Total Standard table space
- Relationship: `Row-based Storage` = `Row-based IA Storage` + `Row-based Standard Storage`

The single-table space query method remains unchanged:

> **Note:**
>
> This method depends on table statistics and may have significant estimation errors.

```sql
SELECT TABLE_NAME,
    ROUND(DATA_LENGTH / 1024 / 1024, 2) AS Data_MB,
    ROUND(INDEX_LENGTH / 1024 / 1024, 2) AS Index_MB,
    TABLE_ROWS
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'your_database'
  AND TABLE_NAME = 'your_table'
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC;
```

### Configure the IA cache level

The IA cache level controls how much IA data is cached on local disks. A higher level caches more data, which improves cold-read performance and increases cost.

| Cache level | Use case |
|-|-|
| **Economy** | Cold reads are rare and you want to minimize local disk cost |
| **Default** | The system default, suitable for general workloads |
| **Balanced** | A balance between cost and cold-read latency |
| **Deep** | Cold-read latency is critical for your workload |

To change the cache level:

1. In the Cloud Console, go to **Overview** > **Capacity** and click **Update Capacity**.
2. In the **Storage Acceleration** block, select a cache level.
3. Review the cost impact in the **Summary** pane, and then click **Update Capacity**.

The change takes effect without a restart, usually within one minute. TiDB Cloud automatically provisions the underlying resources, so you do not need to check available space or choose a scaling method. Provisioning might take some time.

On {{{ .premium }}}, a higher cache level increases the billed IA storage amount. On {{{ .byoc }}}, the additional local cache resources are provisioned in your own cloud account and are billed by your cloud provider. For details, see [TiDB Cloud Billing](/tidb-cloud/tidb-cloud-billing.md).

### Adjust the IA segment size (BYOC only)

A segment is the smallest unit that TiKV reads from object storage and writes to the local cache. The default size is 1 MiB.

On {{{ .byoc }}}, you can set the TiKV configuration parameter `kvengine.ia.segment-size` to `128 KiB`, `256 KiB`, `512 KiB`, `1 MiB`, or `2 MiB`. This parameter is not available on {{{ .premium }}}.

`kvengine.ia.segment-size` takes effect only at startup. After you change it, perform a rolling restart of the TiKV nodes, preferably during off-peak hours.

Changing the segment size does not rewrite any file in object storage. SST files are stored as whole objects and are not organized by segment, so only the read and cache granularity on local disks changes. After the restart, the local cache is gradually rebuilt at the new granularity as queries arrive.

## Observability

For IA observability, including storage class transition progress, `EXPLAIN ANALYZE` fields, statement summary and slow query metrics, and the cluster-level IA cache performance panels, see [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md).

## Best practices

This section describes recommended operational practices for IA storage, including tiering strategy, rollout strategy, write optimization, query optimization, cache level tuning, segment size selection, switch-back considerations, and configuration stability.

### Tiering strategy: prefer partition-level IA

For partitioned tables, **always prefer partition-level IA** over table-level IA. This gives you precise control over cold/hot boundaries:

- Historical cold partitions (e.g., `p2023`) → IA
- Recent hot partitions (e.g., `p2025`) → Standard
- Future partitions (e.g., `p_future`) → Standard

### Rollout strategy: start with the smallest oldest partition

```
Step 1: Select the oldest and smallest partition → ALTER PARTITION → IA
Step 2: Observe for one full business day (at least 24h)
Step 3: Verify QPS / TPS / P99 Latency / CPU metrics show no degradation
Step 4: Set the next cold partition → IA one by one
Step 5: Repeat Steps 2-4 until all target partitions are covered
```

**Do not batch-set all partitions to IA at once.**

### Write optimization

- Benchmark concurrent writes with the same thread count, workload, and partition distribution before applying this tuning. In one test environment, random writes to IA partitions averaged 50k rows/sec, while fixed single-thread writes to one IA partition averaged 70k rows/sec; these results are not directly comparable.
- Newly imported data only transitions to IA mode after flush/compaction. Large-range queries immediately after import may encounter cold cache.

These figures are from test environments and do not represent real-world production scenarios. You should obtain accurate data based on your own business testing.

### Query optimization

- Queries spanning IA partitions are recommended to cover **no more than 3 partitions**; exceeding this may cause significant response time degradation
- Avoid running concurrent `SELECT *` full-table scans on IA tables simultaneously
- Monitor IA remote read volume via `EXPLAIN ANALYZE` and slow queries, and adjust accordingly

### Tune the IA cache level

Use the **IA Cache Hit Rate** panel to decide whether to change the cache level:

- If the hit rate stays below 85%, raise the cache level. **Balanced** is a reasonable starting point.
- After each change, observe the hit rate for at least one full business day before you change it again.
- If the hit rate is consistently high and you want to reduce cost, lower the cache level to **Economy**.

For the panels and the statement-level metrics used in this tuning loop, see [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md).

### Choose the segment size (BYOC only)

The segment size trades read amplification against the number of object storage requests:

| Segment size | Read amplification per cache miss | Object storage requests | Suitable for |
|-|-|-|-|
| Smaller than 1 MiB | Lower | Higher | Point queries against low-latency object storage, when request costs are not a concern |
| 1 MiB (default) | Medium | Medium | General workloads |
| Larger than 1 MiB | Higher | Lower | Large-range scans with sufficient network bandwidth |

Benchmark with your own workload before you change this parameter, and perform the rolling restart during off-peak hours.

### Switch-back considerations

- IA → Standard conversion downloads all data from object storage, generating significant cold storage bandwidth usage
- Monitor bandwidth usage to ensure smooth operation; if necessary, **contact the TiDB Cloud team in advance** for joint monitoring
- Business SQL reads/writes are not affected during conversion, but performance (e.g., QPS/TPS) may have minor impact — test environment shows less than 5%
- Before you start, query `mysql.tidb_storage_class_transition_history` for the duration of similar past conversions on your cluster, filtered on `STATE = 'COMPLETED'`, to estimate the change window
- During the conversion, run `SHOW STORAGE_CLASS TRANSITIONS` to track progress and detect a stuck conversion

### Configuration stability

Keep the storage class setting stable and avoid frequent switching between IA and Standard. Each switch triggers:

- Region reload
- Object storage data download or metadata rebuild
- IA cache data flushing

The cumulative cost of these operations is not negligible.

If you issue a reverse conversion while the previous conversion is still running, the previous conversion is voided and the progress it had made is discarded. The new conversion starts over from the beginning, so reversing mid-way takes longer overall than waiting for the first conversion to finish. For how to identify a voided conversion, see [Tiered Storage Observability](/tidb-cloud/tiered-storage-observability.md).

This applies to the storage class of a table or partition. Adjusting the IA cache level is a different operation: it is a hot update, does not move data between storage classes, and can be changed as often as your cost and performance targets require.
