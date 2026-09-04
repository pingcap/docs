---
title: Tiered Storage Observability
summary: Learn how to monitor tiered storage on TiDB Cloud Premium or BYOC, including conversion progress, IA read metrics, and cache performance panels.
---

# Tiered Storage Observability

This document describes how to monitor Infrequent Access (IA) storage, including storage class transition progress, IA read metrics at the SQL level, and IA cache performance at the cluster level.

> **Note:**
>
> Tiered storage is in **Private Preview** for {{{ .premium }}} and {{{ .byoc }}}. The behavior described on this page reflects the current preview implementation and might change before general availability (GA).

## Monitor storage class transitions

This section describes how to track the progress of a storage class conversion and how to review completed conversions.

`ALTER TABLE ... STORAGE_CLASS` updates the schema metadata within seconds. The region-level data migration runs asynchronously in TiKV and is decoupled from the DDL lifecycle, so `ADMIN SHOW DDL JOBS` does not report its progress. Use `SHOW STORAGE_CLASS TRANSITIONS` to track a conversion in progress, and query `mysql.tidb_storage_class_transition_history` to review completed conversions.

### View in-progress transitions

```sql
SHOW STORAGE_CLASS TRANSITIONS;
SHOW STORAGE_CLASS TRANSITIONS LIKE 'table_name';
SHOW STORAGE_CLASS TRANSITIONS WHERE DIRECTION = 'TO_STANDARD';
SHOW STORAGE_CLASS TRANSITIONS WHERE STATE = 'RUNNING';
```

`SHOW STORAGE_CLASS TRANSITIONS` is equivalent to `SELECT * FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS`, and additionally provides a `PROGRESS` column calculated as `COMPLETED_REPLICAS / TOTAL_REPLICAS * 100`.

The `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` table has the following columns:

| Column | Type | Description |
|-|-|-|
| `TABLE_SCHEMA` | VARCHAR(64) | The database name |
| `TABLE_NAME` | VARCHAR(64) | The table name |
| `PARTITION_NAME` | VARCHAR(64) | The partition name. The value is `NULL` for a table-level conversion |
| `DIRECTION` | ENUM('TO_IA', 'TO_STANDARD') | The conversion direction |
| `TOTAL_REPLICAS` | BIGINT | The total number of replicas involved in the conversion |
| `COMPLETED_REPLICAS` | BIGINT | The number of replicas that have completed the conversion |
| `STATE` | ENUM('RUNNING') | The conversion state. This table only records conversions in progress, so the value is always `RUNNING` |
| `START_TIME` | DATETIME | The time when the conversion started |
| `DURATION` | BIGINT | The elapsed time in seconds from the start of the conversion to now |

To check the progress and elapsed time of a specific conversion:

```sql
SELECT TABLE_NAME, DIRECTION, COMPLETED_REPLICAS, TOTAL_REPLICAS,
       ROUND(COMPLETED_REPLICAS / TOTAL_REPLICAS * 100, 1) AS PROGRESS_PCT,
       DURATION
FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name';
```

A conversion has only two states:

| State | Description |
|-|-|
| `RUNNING` | The region-level conversion is in progress. Track progress with `COMPLETED_REPLICAS` and `TOTAL_REPLICAS`, and track elapsed time with `DURATION` |
| `COMPLETED` | All regions have completed the conversion. This is the final state. The record is removed from `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` and written to `mysql.tidb_storage_class_transition_history` |

### Determine whether a conversion is stuck

In the `RUNNING` state, watch `COMPLETED_REPLICAS` and `DURATION` together:

- `COMPLETED_REPLICAS` increases as `DURATION` grows: the conversion is progressing normally and the data volume is simply large.
- `DURATION` keeps growing but `COMPLETED_REPLICAS` does not increase for a long time: the conversion might be stuck because of a system exception, such as a TiKV rolling restart, temporarily insufficient resources, or short-term object storage unavailability.

You cannot resolve a stuck conversion yourself. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for help. After the issue is resolved, `COMPLETED_REPLICAS` continues to increase until the conversion reaches `COMPLETED`, and no additional action is required from you.

### Query transition history

Completed conversions are recorded in the `mysql.tidb_storage_class_transition_history` table, which has the following columns:

| Column | Type | Description |
|-|-|-|
| `TABLE_SCHEMA` | VARCHAR(64) | The database name |
| `TABLE_NAME` | VARCHAR(64) | The table name |
| `PARTITION_NAME` | VARCHAR(64) | The partition name. The value is `NULL` for a table-level conversion |
| `DIRECTION` | ENUM('TO_IA', 'TO_STANDARD') | The conversion direction |
| `TOTAL_REGIONS` | BIGINT | The total number of regions involved in the conversion |
| `STATE` | ENUM('COMPLETED') | The final state of the conversion. Only completed conversions are recorded |
| `DURATION` | BIGINT | The total duration of the conversion in seconds, calculated as `FINISH_TIME - START_TIME` |
| `START_TIME` | DATETIME | The time when the conversion started |
| `FINISH_TIME` | DATETIME | The time when the conversion finished |

Use this table to estimate how long a similar conversion takes on your own cluster, which is more reliable than any reference figure from a test environment:

```sql
-- Average duration of completed conversions, grouped by direction
SELECT DIRECTION,
       COUNT(*) AS total_conversions,
       ROUND(AVG(DURATION), 0) AS avg_duration_sec,
       MIN(DURATION) AS min_duration_sec,
       MAX(DURATION) AS max_duration_sec
FROM mysql.tidb_storage_class_transition_history
GROUP BY DIRECTION;

-- The most recent conversion of a specific table
SELECT TABLE_NAME, DIRECTION, DURATION AS total_duration_sec,
       TOTAL_REGIONS, START_TIME, FINISH_TIME
FROM mysql.tidb_storage_class_transition_history
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name'
ORDER BY FINISH_TIME DESC
LIMIT 1;
```

#### Retention of history records

The maximum number of records retained in `mysql.tidb_storage_class_transition_history` is controlled by the system variable [`tidb_storage_class_transition_history_size`](#tidb_storage_class_transition_history_size). When a new record causes the row count to exceed this limit, the oldest records are removed first based on `FINISH_TIME`.

```sql
-- View the current retention limit
SELECT @@tidb_storage_class_transition_history_size;

-- Retain up to 500 records
SET GLOBAL tidb_storage_class_transition_history_size = 500;
```

#### tidb_storage_class_transition_history_size

- Scope: GLOBAL
- Persists to cluster: Yes
- Applies to hint [SET_VAR](/optimizer-hints.md#set_varvar_namevar_value): No
- Type: Integer (Unsigned)
- Default value: `1000`
- Range: `[100, 100000]`
- This variable is used to set the maximum number of storage class transition records retained in the `mysql.tidb_storage_class_transition_history` table. A larger value retains history for longer and uses more space in the `mysql` database.

## Monitor IA reads at the SQL level

This section describes the IA metrics available in `EXPLAIN ANALYZE`, statement summary tables, slow query logs, and the TiDB Cloud console.

### EXPLAIN ANALYZE

When a query involves remote data loading, the `scan_detail` includes the following fields:

```sql
EXPLAIN ANALYZE SELECT * FROM t_ia WHERE id BETWEEN 1 AND 50000;
-- The output includes:
-- ia_remote_read_segment_size: 2320453     -- Total bytes loaded remotely
-- ia_remote_read_segment_count: 3           -- Number of remote loading events
-- ia_remote_read_segment_wait_time: 0.008   -- Remote wait time (seconds)
```

> **Note:**
>
> The IA signal is per-request read path evidence, not a table-level stable flag — the same query may show IA information on the first run but not after a cache hit.
>
> Additionally, `ia_remote_read_segment_wait_time` is the aggregate time of all remote requests. Due to TiKV's underlying parallel reading mechanism, this value may exceed the SQL's actual execution time.

### Statement summary

`STATEMENTS_SUMMARY`, `STATEMENTS_SUMMARY_HISTORY`, and their `CLUSTER_` counterparts include the following IA columns:

| Column | Description |
|-|-|
| `IA_EXEC_COUNT` | The number of executions that triggered at least one IA remote read. Compare it with `EXEC_COUNT` to get the proportion of executions that accessed IA data. For example, `IA_EXEC_COUNT = 2` with `EXEC_COUNT = 1000` means only 0.2% of the executions accessed IA data |
| `AVG_IA_REMOTE_READ_SEGMENT_COUNT` | The average number of remote segments read per execution |
| `MAX_IA_REMOTE_READ_SEGMENT_COUNT` | The maximum number of remote segments read in a single execution |
| `AVG_IA_REMOTE_READ_SEGMENT_SIZE` | The average remote read data volume per execution |
| `MAX_IA_REMOTE_READ_SEGMENT_SIZE` | The maximum remote read data volume in a single execution |
| `AVG_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | The average remote wait time per execution |
| `MAX_IA_REMOTE_READ_SEGMENT_WAIT_TIME` | The maximum remote wait time in a single execution |

The `AVG_` and `MAX_` columns answer how much data each execution read remotely, while `IA_EXEC_COUNT` answers how many executions read remotely at all. Use both dimensions together: a statement with a small `AVG_IA_REMOTE_READ_SEGMENT_SIZE` but a high `IA_EXEC_COUNT / EXEC_COUNT` ratio accesses cold data frequently in small amounts.

For queries that do not involve IA tables, these columns are `0` or `NULL`.

To find the statements with the highest proportion of cold-read executions:

```sql
SELECT DIGEST_TEXT, EXEC_COUNT, IA_EXEC_COUNT,
       ROUND(IA_EXEC_COUNT / EXEC_COUNT * 100, 2) AS ia_exec_pct,
       AVG_IA_REMOTE_READ_SEGMENT_SIZE
FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY
WHERE IA_EXEC_COUNT > 0
ORDER BY ia_exec_pct DESC
LIMIT 10;
```

### Slow queries

`INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` includes the following IA columns:

- `IA_remote_read_segment_count`
- `IA_remote_read_segment_size`
- `IA_remote_read_segment_wait_time`

The same fields are available in the `ADMIN SHOW SLOW` output:

```sql
ADMIN SHOW SLOW RECENT 10;
ADMIN SHOW SLOW TOP INTERNAL 10;
ADMIN SHOW SLOW TOP ALL 10;
```

The field semantics and units are the same as in the `SLOW_QUERY` table. For a query that does not involve IA tables, the values are `NULL` or `0`. The corresponding fields are also visible in the slow query details in the TiDB Cloud console.

### SQL statement list in the console

The `IA_EXEC_COUNT` column is also displayed in the SQL statement diagnosis list:

- **Cloud Console**: **Monitoring** > **Diagnosis** > **SQL Statement**
- **Clinic**: **Diagnosis** > **SQL Statements**

The column is named **Exec Count of IA** and is placed right after **Executions Count** so that you can compare the two values directly. It supports ascending and descending sorting like the other columns. For a statement that does not involve IA tables, the value is `0`.

## Monitor IA cache performance at the cluster level

This section describes the cluster-level panels for IA cache behavior in the TiDB Cloud console.

### IA Cache Performance panels

Path: **Monitoring** > **Metrics** > **Instance Overview** > **IA Cache Performance**.

| Panel | Description |
|-|-|
| **IA Cache Hit Rate (%)** | The overall IA cache hit rate of the cluster. A yellow indicator appears when the value drops below 85% |
| **IA Cache Miss Rate (ops/s)** | The frequency of IA cache misses. This value normally stays low. A sudden increase indicates a large volume of cold reads or a cache under pressure |
| **IA Remote Read Segment** | The frequency (Count) and data volume (Size) of segments read from object storage. Use it to assess object storage request volume and bandwidth consumption |
| **IA Remote Read Segment Wait Time** | The wait time of a single remote read, shown as P99 and Avg. A sustained increase indicates degraded object storage latency or bandwidth limits |

You can change the time window with the time picker to observe longer trends. If the cluster has no IA tables, the panels show **No IA data** instead of `0%` or an error.

To monitor the cold data volume of a single statement, use the `IA Remote Read Segment Size` panel in **Monitoring** > **Diagnosis** > **Slow Query** > **Coprocessor**.

### Interpret the panels

Cache hit rates depend on your actual access patterns. Concentrated access can exceed 95%, while scattered access might fall below 95%.

- **Sudden drop in hit rate**: check whether **IA Cache Miss Rate** rises at the same time. A simultaneous rise confirms a real increase in cold reads rather than a collection issue. Then use `IA_EXEC_COUNT` in the statement summary tables to identify which statements triggered the cold reads.
- **Sustained low hit rate**: the cache is under pressure from cold data. Consider raising the IA cache level, or reducing the amount of data set to IA. See [Configure and Manage Tiered Storage](/tidb-cloud/tiered-storage-guide.md).
- **Evaluating whether a table suits IA**: after setting a partition to IA, observe **IA Cache Hit Rate** for at least one full business day. A stable hit rate means the access pattern suits IA. Large fluctuations or a low average means the data is accessed too scatteredly for IA.

## Diagnostic workflows

### Estimate the conversion window before a change

1. Run `SHOW STORAGE_CLASS TRANSITIONS WHERE STATE = 'RUNNING'` to check whether other conversions are already in progress.
2. Query `mysql.tidb_storage_class_transition_history` for the `DURATION` of similar past conversions on your cluster.
3. During the conversion, combine `DURATION` with `COMPLETED_REPLICAS / TOTAL_REPLICAS` to estimate the remaining time.

### Investigate a sudden drop in cache hit rate

1. Confirm the drop in **IA Cache Hit Rate** and check whether **IA Cache Miss Rate** rises at the same time.
2. Identify the statements with a high `IA_EXEC_COUNT / EXEC_COUNT` ratio in the statement summary tables.
3. If many statements show the ratio rising at the same time, a batch of analytical queries is probably scanning IA tables and evicting hot data from the cache.
4. Decide whether to raise the IA cache level or to move the affected data back to Standard storage.

### Decide whether to keep a table in IA

1. Aggregate `IA_EXEC_COUNT / EXEC_COUNT` for the statements that access the table.
2. If most statements keep a high cold-read ratio, the cache hit rate is too low for IA. Consider switching the table back to Standard.
3. If the cold-read ratio is low but a few statements read a large volume each time, optimize those statements instead of switching the whole table back.

## See also

- [Tiered Storage Overview](/tidb-cloud/tiered-storage-overview.md)
- [Configure and Manage Tiered Storage](/tidb-cloud/tiered-storage-guide.md)
- [Tiered Storage Limitations](/tidb-cloud/tiered-storage-limitations.md)
- [Tiered Storage FAQ](/tidb-cloud/tiered-storage-faq.md)
