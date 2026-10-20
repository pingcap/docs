# Tiered Storage Observability on TiDB Cloud Essential

> This note describes how to monitor tiered storage on a TiDB Cloud Essential instance for which tiered storage has been enabled through a special allowlist request. For the capability differences between Essential and Premium, see [Tiered Storage on TiDB Cloud Essential — Capability Notes](/tidb-cloud/tiered-storage-essential-capability-notes.md).

> **Note:**
>
> Tiered storage is in **private preview** and is not offered on TiDB Cloud Essential by default. It is enabled on an Essential instance only through an allowlist. The behavior described in this note reflects the current preview implementation and might change before general availability (GA).

## Observability scope on Essential

- IA cache hit rate and cache miss rate data are not available on Essential. The local cache capacity is system-managed and fixed on Essential and cannot be tuned. Judge IA behavior from the statement-level signals described in [Monitor IA reads at the SQL level](#monitor-ia-reads-at-the-sql-level) and the cluster-level IA remote read panels.
- All other monitoring capabilities — storage class transition tracking, `EXPLAIN ANALYZE` IA fields, statement summary IA columns, slow query IA fields, and the IA remote read panels — are fully available on Essential.

## Monitor storage class transitions

This section describes how to track the progress of a storage class conversion and how to review past conversions.

Conversion progress is tracked the same way whichever form you use to change the storage class:

- The `STORAGE_CLASS` syntactic sugar, for example `ALTER TABLE t1 STORAGE_CLASS='IA'`
- The `ENGINE_ATTRIBUTE` form, for example `ALTER TABLE t1 ENGINE_ATTRIBUTE='{"storage_class":"IA"}'`
- A partition-level change made with `ENGINE_ATTRIBUTE`

Partitioned tables support only `ENGINE_ATTRIBUTE`, so partition conversions appear in the same views as table-level conversions. A table or partition that is created directly in the IA storage class has no data to migrate, so it does not appear in these views.

The `ALTER TABLE` statement itself updates the schema metadata within seconds. The region-level data migration then runs asynchronously in TiKV and is decoupled from the DDL lifecycle, so `ADMIN SHOW DDL JOBS` does not report its progress. Use `SHOW STORAGE_CLASS TRANSITIONS` to track a conversion in progress, and query `mysql.tidb_storage_class_transition_history` to review past and ongoing conversions. A record is inserted into the history table when a conversion starts, with `state = 'RUNNING'`, and is updated in place when the conversion reaches a final state.

### View in-progress transitions

```sql
SHOW STORAGE_CLASS TRANSITIONS;
SHOW STORAGE_CLASS TRANSITIONS LIKE 'table_name';
SHOW STORAGE_CLASS TRANSITIONS WHERE DIRECTION = 'TO_STANDARD';
```

`SHOW STORAGE_CLASS TRANSITIONS` is equivalent to `SELECT * FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS`.

The `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` table lists the conversions that are currently in progress. It has no state column, because every row in it is an in-progress conversion. The table has the following columns:

| Column | Type | Description |
|-|-|-|
| `TABLE_SCHEMA` | VARCHAR(64) | The database name |
| `TABLE_NAME` | VARCHAR(64) | The table name |
| `TABLE_ID` | BIGINT(21) | The internal ID of the table |
| `PARTITION_NAME` | VARCHAR(64) | The partition name. The value is `NULL` for a table-level conversion |
| `PARTITION_ID` | BIGINT(21) | The internal ID of the partition. The value is `NULL` for a table-level conversion |
| `DIRECTION` | VARCHAR(16) | The conversion direction: `TO_IA` or `TO_STANDARD` |
| `TOTAL_REPLICAS` | BIGINT(21) UNSIGNED | The total number of replicas involved in the conversion. The value is `NULL` before the first successful observation |
| `COMPLETED_REPLICAS` | BIGINT(21) UNSIGNED | The number of replicas that are ready. The value is `NULL` before the first successful observation |
| `PROGRESS` | DOUBLE | The ratio of `COMPLETED_REPLICAS` to `TOTAL_REPLICAS`, from `0` to `1`. Multiply it by 100 to get a percentage. The value is `NULL` until an observation reports a valid progress ratio, which can be later than the first observation that populates `TOTAL_REPLICAS` and `COMPLETED_REPLICAS` |
| `START_TIME` | DATETIME(6) | The time when the conversion started, in the session time zone |
| `DURATION` | BIGINT(21) UNSIGNED | The elapsed time in seconds from the start of the conversion to now |
| `LAST_UPDATE_TIME` | DATETIME(6) | The time of the most recent successful progress observation |

> **Note:**
>
> - A row is visible only if you have the `ALL` privilege on the table. Rows for tables that you cannot access are skipped, without an error or a warning.
> - Progress is collected every 10 seconds, so the values are not real-time.

To check the progress and elapsed time of a specific conversion:

```sql
SELECT TABLE_NAME, DIRECTION, COMPLETED_REPLICAS, TOTAL_REPLICAS,
       ROUND(PROGRESS * 100, 1) AS PROGRESS_PCT,
       DURATION, LAST_UPDATE_TIME
FROM INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS
WHERE TABLE_SCHEMA = 'db_name' AND TABLE_NAME = 'table_name';
```

A conversion goes through one in-progress state and ends in one of two final states. Every state is also recorded in `mysql.tidb_storage_class_transition_history`:

| State | Where it is recorded | Description |
|-|-|-|
| `RUNNING` | `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` and the `state` column of `mysql.tidb_storage_class_transition_history` | The region-level conversion is in progress. The `INFORMATION_SCHEMA` table lists only these conversions and has no state column. While a conversion is `RUNNING`, its history record has `NULL` in `finish_time`, `duration`, `total_replicas`, and `completed_replicas`. Track progress with `PROGRESS`, `COMPLETED_REPLICAS`, and `TOTAL_REPLICAS`, and track elapsed time with `DURATION` |
| `COMPLETED` | The `state` column of `mysql.tidb_storage_class_transition_history` | All replicas are ready. The conversion is removed from `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS` and its history record is updated to `COMPLETED` |
| `SUPERSEDED` | The `state` column of `mysql.tidb_storage_class_transition_history` | The conversion was voided because a reverse conversion was issued before it finished. Its history record is updated to `SUPERSEDED` |

### Determine whether a conversion is stuck

Watch `LAST_UPDATE_TIME`, `COMPLETED_REPLICAS`, and `DURATION` together:

- `COMPLETED_REPLICAS` increases and `LAST_UPDATE_TIME` keeps advancing: the conversion is progressing normally and the data volume is simply large.
- `DURATION` keeps growing but `COMPLETED_REPLICAS` does not increase for a long time: the conversion might be stuck because of a system exception, such as a TiKV rolling restart, temporarily insufficient resources, or short-term object storage unavailability.
- `TOTAL_REPLICAS`, `COMPLETED_REPLICAS`, `PROGRESS`, and `LAST_UPDATE_TIME` all stay `NULL`: no successful observation has been made yet. These columns are populated and cleared together, so `LAST_UPDATE_TIME` cannot tell whether observations are still being attempted. Check `DURATION` instead: it always increases while the conversion is being tracked. If these columns stay `NULL` while `DURATION` keeps growing, polling is still running but has not returned a valid observation.

You cannot resolve a stuck conversion yourself. Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for help. After the issue is resolved, `COMPLETED_REPLICAS` continues to increase until the conversion reaches `COMPLETED`, and no additional action is required from you.

### Reverse a conversion that is still in progress

If you issue a reverse conversion for a table or partition while the previous conversion is still in progress, the previous conversion is voided:

- In `INFORMATION_SCHEMA.TIKV_STORAGE_CLASS_TRANSITIONS`, the row for that table or partition is replaced by the new conversion. `DIRECTION` shows the new direction, `START_TIME` is the start time of the new conversion, and the progress counts from the beginning again. Only one row remains for that table or partition.
- The history record of the voided conversion in `mysql.tidb_storage_class_transition_history` is updated to `state = 'SUPERSEDED'`. Its `finish_time` is the start time of the new conversion, and its `total_replicas` and `completed_replicas` are the last values observed before it was voided. If nothing had been observed yet, both columns are `NULL`.

To find out how far a voided conversion had progressed, query the history table for records with `state = 'SUPERSEDED'`.

### Query transition history

Every conversion is recorded in the `mysql.tidb_storage_class_transition_history` table when it starts, and its record is updated as the conversion progresses. The table has the following columns:

| Column | Type | Description |
|-|-|-|
| `table_schema` | VARCHAR(64) | The database name |
| `table_name` | VARCHAR(64) | The table name |
| `table_id` | BIGINT | The internal ID of the table. Together with `start_ts` and `direction`, it forms the primary key of this table |
| `partition_name` | VARCHAR(64) | The partition name. The value is `NULL` for a table-level conversion |
| `partition_id` | BIGINT | The internal ID of the partition. The value is `NULL` for a table-level conversion |
| `direction` | VARCHAR(16) | The conversion direction: `TO_IA` or `TO_STANDARD` |
| `state` | VARCHAR(16) | The state of the conversion: `RUNNING`, `COMPLETED`, or `SUPERSEDED` |
| `total_replicas` | BIGINT UNSIGNED | The total number of replicas involved in the conversion. For a `SUPERSEDED` record, this is the last value observed before the conversion was voided, or `NULL` if nothing was observed. The value is `NULL` while the conversion is `RUNNING` |
| `completed_replicas` | BIGINT UNSIGNED | The number of replicas that were ready. For a `COMPLETED` record, this equals `total_replicas`. For a `SUPERSEDED` record, this is the last value observed before the conversion was voided, or `NULL` if nothing was observed. The value is `NULL` while the conversion is `RUNNING` |
| `schema_version` | BIGINT | The TiDB schema version that the conversion belongs to |
| `start_ts` | BIGINT UNSIGNED | The start TSO of the conversion. It identifies the conversion together with `table_id` and `direction` |
| `start_time` | DATETIME(6) | The time when the conversion started |
| `finish_time` | DATETIME(6) | The time when the conversion reached its final state. For a `COMPLETED` record, this is when all replicas were ready. For a `SUPERSEDED` record, this is the start time of the new conversion. The value is `NULL` until the conversion reaches a final state |
| `duration` | BIGINT UNSIGNED | The total duration in seconds. For a `SUPERSEDED` record, this covers only the time from the start until the conversion was voided, not a full conversion. The value is `NULL` while the conversion is still `RUNNING` |

Use this table to estimate how long a similar conversion takes on your own cluster, which is more reliable than any reference figure from a test environment:

```sql
-- Average duration of completed conversions, grouped by direction.
-- Filter on state = 'COMPLETED': the duration of a SUPERSEDED record
-- does not represent a full conversion.
SELECT direction,
       COUNT(*) AS total_conversions,
       ROUND(AVG(duration), 0) AS avg_duration_sec,
       MIN(duration) AS min_duration_sec,
       MAX(duration) AS max_duration_sec
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'COMPLETED'
GROUP BY direction;

-- The most recent finished conversion of a specific table
SELECT table_name, direction, state, duration AS total_duration_sec,
       total_replicas, completed_replicas, start_time, finish_time
FROM mysql.tidb_storage_class_transition_history
WHERE table_schema = 'db_name' AND table_name = 'table_name'
    AND state <> 'RUNNING'
ORDER BY finish_time DESC
LIMIT 1;

-- Conversions that were voided by a reverse conversion
SELECT table_schema, table_name, partition_name, direction,
       completed_replicas, total_replicas, start_time, finish_time, duration
FROM mysql.tidb_storage_class_transition_history
WHERE state = 'SUPERSEDED'
ORDER BY finish_time DESC;
```

#### Retention of history records

The maximum number of records retained in `mysql.tidb_storage_class_transition_history` is controlled by the system variable [`tidb_storage_class_transition_history_size`](#tidb_storage_class_transition_history_size). When the number of records exceeds this limit, the oldest records, ordered by `finish_time`, are removed first. Retention is enforced at most once per minute, so the row count can temporarily exceed the limit.

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
- Type: Integer
- Default value: `1000`
- Range: `[100, 100000]`
- This variable is used to set the maximum number of storage class transition records retained in the `mysql.tidb_storage_class_transition_history` table. A larger value retains history for longer and uses more space in the `mysql` database.

## Monitor IA reads at the SQL level

This section describes the IA metrics available in `EXPLAIN ANALYZE`, the statement summary tables, and the TiDB Cloud console. On Essential, these are your primary signals for IA cold-read behavior.

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

> **Note:**
>
> Because of the [TiDB X architecture](/tidb-cloud/tidb-x-architecture.md), the `ADMIN SHOW SLOW` statement and the `SLOW_QUERY` and `CLUSTER_SLOW_QUERY` tables in `INFORMATION_SCHEMA` are not supported on Essential. Use the TiDB Cloud console to view slow queries. For the complete list of unsupported SQL features, see [Limited SQL Features on TiDB X Instances](/tidb-cloud/limited-sql-features-tidb-x.md).

The following IA fields are recorded for each slow query and displayed in the slow query details in the TiDB Cloud console:

- `IA_remote_read_segment_count`
- `IA_remote_read_segment_size`
- `IA_remote_read_segment_wait_time`

To view these fields:

1. Go to **Monitoring** > **Diagnosis** > **Slow Query**.
2. Click a slow query in the list to open its details.

For more information about the slow query page, see [Slow Query](/tidb-cloud/tune-performance.md#slow-query).

The field semantics and units are the same as the corresponding fields in the `EXPLAIN ANALYZE` output. For a query that does not involve IA tables, the values are `NULL` or `0`.

### SQL statement list in the console

The `IA_EXEC_COUNT` column is also displayed in the SQL statement diagnosis list:

- **Cloud Console**: **Monitoring** > **Diagnosis** > **SQL Statement**
- **Clinic**: **Diagnosis** > **SQL Statements**

The column is named **Exec Count of IA** and is placed right after **Executions Count** so that you can compare the two values directly. It supports ascending and descending sorting like the other columns. For a statement that does not involve IA tables, the value is `0`.

## Monitor IA remote reads at the cluster level

This section describes the cluster-level panels for IA remote read behavior in the TiDB Cloud console.

### IA remote read panels

Path: **Monitoring** > **Metrics** > **Instance Overview** > **IA Cache Performance**.

The following panels are available on Essential:

| Panel | Description |
|-|-|
| **IA Remote Read Segment** | The frequency (Count) and data volume (Size) of segments read from object storage. Use it to assess object storage request volume and bandwidth consumption |
| **IA Remote Read Segment Wait Time** | The wait time of a single remote read, shown as P99 and Avg. A sustained increase indicates degraded object storage latency or bandwidth limits |

You can change the time window with the time picker to observe longer trends. If the cluster has no IA tables, the panels show **No IA data** instead of `0` or an error.

To monitor the cold data volume of a single statement, use the `IA Remote Read Segment Size` panel in **Monitoring** > **Diagnosis** > **Slow Query** > **Coprocessor**.

### Interpret the panels

On Essential, judge IA health from the remote read volume and latency:

- **Rising IA Remote Read Segment (Count or Size)**: cold reads are increasing. Identify which statements trigger them with the statement summary tables — look for a rising `IA_EXEC_COUNT / EXEC_COUNT` ratio, then use `EXPLAIN ANALYZE` on those statements to confirm the remote read volume.
- **Sustained increase in IA Remote Read Segment Wait Time**: object storage latency is degrading or bandwidth limits are approached. Check whether a batch of analytical queries is scanning IA tables; if so, reduce the IA scope or optimize those queries.
- **Evaluating whether a table suits IA**: after setting a partition to IA, observe the statement-level cold-read ratio and the remote read volume for at least one full business day. A low, stable cold-read ratio means the access pattern suits IA. A consistently high ratio means the data is accessed too scatteredly for IA.

The local cache capacity is system-managed and fixed. When these signals indicate sustained cold-read pressure, your options are to move the affected data back to Standard storage, optimize the offending queries, or contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

## Diagnostic workflows

### Estimate the conversion window before a change

1. Run `SHOW STORAGE_CLASS TRANSITIONS` to check whether other conversions are already in progress. The table lists only in-progress conversions.
2. Query `mysql.tidb_storage_class_transition_history` for the `duration` of similar past conversions on your cluster, filtered on `state = 'COMPLETED'`.
3. During the conversion, combine `DURATION` with `PROGRESS` to estimate the remaining time.

### Investigate a rise in cold reads

1. Confirm the rise in the **IA Remote Read Segment** panel, and check whether **IA Remote Read Segment Wait Time** increases at the same time.
2. Identify the statements with a high `IA_EXEC_COUNT / EXEC_COUNT` ratio in the statement summary tables.
3. If many statements show the ratio rising at the same time, a batch of analytical queries is probably scanning IA tables and evicting hot data from the cache.
4. Move the affected data back to Standard storage or optimize the offending queries. If the impact is not acceptable, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

### Decide whether to keep a table in IA

1. Aggregate `IA_EXEC_COUNT / EXEC_COUNT` for the statements that access the table, and watch the **IA Remote Read Segment** volume.
2. If most statements keep a high cold-read ratio, the table is accessed too scatteredly for IA. Consider switching it back to Standard.
3. If the cold-read ratio is low but a few statements read a large volume each time, optimize those statements instead of switching the whole table back.

## See also

- [Tiered Storage on TiDB Cloud Essential — Capability Notes](/tidb-cloud/tiered-storage-essential-capability-notes.md)
- [Tiered Storage Overview](/tidb-cloud/tiered-storage-overview.md)
- [Configure and Manage Tiered Storage](/tidb-cloud/tiered-storage-guide.md)
- [Tiered Storage Limitations](/tidb-cloud/tiered-storage-limitations.md)
- [Tiered Storage FAQ](/tidb-cloud/tiered-storage-faq.md)
