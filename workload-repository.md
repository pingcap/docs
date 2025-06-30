---
title: TiDB Workload Repository
summary: Introduces the workload repository system for collecting and storing historical workload data from a TiDB cluster.
---

# TiDB Workload Repository

The Workload Repository is a system for collecting and storing historical workload data from a TiDB cluster. It periodically samples various system tables to track cluster performance and usage patterns over time.

## Enable the Workload Repository

To enable the Workload Repository, set the [`tidb_workload_repository_dest`](/system-variables.md#tidb_workload_repository_dest-new-in-v900) system variable:

```sql
SET GLOBAL tidb_workload_repository_dest = 'table';
```

To disable it:

```sql
SET GLOBAL tidb_workload_repository_dest = '';
```

## Data collection

The Workload Repository stores data in tables under the `WORKLOAD_SCHEMA` database. It collects data via two different methods:

* The snapshot sampling process, which runs at configurable intervals, hourly by default, and can be triggered manually.
* The time-based sampling process, which runs at shorter intervals, typically every 5 seconds.

## Snapshot sampling process (hourly by default)

The snapshot sampling process, which runs every 15 minutes to 2 hours, samples data from various cumulative metrics tables. Snapshots are initiated from one of the TiDB nodes at the specified intervals, and the process is as follows:

1. From the initiating node, a row is inserted into `WORKLOAD_SCHEMA.HIST_SNAPSHOTS`, capturing the snapshot ID, start and end timestamps, and server version details.
2. On each TiDB node, all rows from the source tables are copied to the corresponding target tables with the `HIST_` prefix. The copied data includes the original columns from the source tables plus additional columns for the timestamp, instance ID, and snapshot ID.

Note that the sampled tables return data specific to the TiDB node from which they are queried.

Data is sampled from the following tables:

| Source table | Destination table | Description |
| --- | --- | --- |
| [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) | `HIST_TIDB_INDEX_USAGE` | Index usage statistics |
| [`TIDB_STATEMENTS_STATS`](/statement-summary-tables.md) | `HIST_TIDB_STATEMENTS_STATS` | Statement statistics |
| [`CLIENT_ERRORS_SUMMARY_BY_HOST`](/information-schema/client-errors-summary-by-host.md) | `HIST_CLIENT_ERRORS_SUMMARY_BY_HOST` | Client error summaries by host |
| [`CLIENT_ERRORS_SUMMARY_BY_USER`](/information-schema/client-errors-summary-by-user.md) | `HIST_CLIENT_ERRORS_SUMMARY_BY_USER` | Client error summaries by user |
| [`CLIENT_ERRORS_SUMMARY_GLOBAL`](/information-schema/client-errors-summary-global.md) | `HIST_CLIENT_ERRORS_SUMMARY_GLOBAL` | Client error summaries by global |

The snapshot sampling interval can be controlled with [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval-new-in-v900):

```sql
SET GLOBAL tidb_workload_repository_snapshot_interval = 900; -- set the interval to 15 minutes
```

## Manual snapshots

Note that while the snapshot sampling process runs automatically based on the configured interval, you can also trigger a manual snapshot using the following SQL statement:

```sql
ADMIN CREATE WORKLOAD SNAPSHOT;
```

Manually triggering snapshots does not change the interval or timing of automatic snapshots.

## Time-based sampling process (every 5 seconds by default)

The time-based sampling process samples data from various non-cumulative metrics tables at intervals ranging from 1 to 600 seconds.

When the time-base sampling process runs, all rows from the source tables are copied to the corresponding target tables with the `HIST_` prefix. The copied data includes the original columns from the source tables plus additional columns for the timestamp and instance ID.

Unlike the snapshot sampling process, a row will not be added to the `HIST_SNAPSHOTS` table.

Note that the sampled tables return data specific to the TiDB node from which they are queried.

Data is sampled from the following tables:

| Source table | Destination table | Description |
| --- | --- | --- |
| [`PROCESSLIST`](/information-schema/information-schema-processlist.md) | `HIST_PROCESSLIST` | Active sessions |
| [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) | `HIST_DATA_LOCK_WAITS` | Data lock waits |
| [`TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) | `HIST_TIDB_TRX` | Active transactions |
| [`MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md) | `HIST_MEMORY_USAGE` | Memory usage |
| [`DEADLOCKS`](/information-schema/information-schema-deadlocks.md) | `HIST_DEADLOCKS` | Deadlock information |

The time-based sampling interval can be controlled with [`tidb_workload_repository_active_sampling_interval`](/system-variables.md#tidb_workload_repository_active_sampling_interval-new-in-v900):

```sql
SET GLOBAL tidb_workload_repository_active_sampling_interval = 20; -- set the interval to 20 seconds
```

Setting this global variable to `0` disables the time-based sampling process.

## Data retention

Historical data in the Workload Repository is retained for seven days by default. The system automatically purges data based on the retention period setting, using partitions for efficient data management.

By default the Workload Repository retains historical data for seven days, but the [`tidb_workload_repository_retention_days`](/system-variables.md#tidb_workload_repository_retention_days-new-in-v900) variable can be used to control the length of this period. For example, to keep data for 30 days, run the following:

```sql
SET GLOBAL tidb_workload_repository_retention_days = 30;
```

A higher value for this variable allows for longer data retention, which might be beneficial for workload analysis, but will increase storage requirements.

## Notes

- Enabling the Workload Repository might have a small performance impact on the system.
- Setting sampling intervals too short might increase system overhead.
- Setting retention days to `0` disables automatic purging of old data.

## Best practices

- Start with default settings and adjust based on your monitoring needs.
- Set reasonable retention periods based on your storage capacity.
- Monitor the size of the `WORKLOAD_SCHEMA` database.
- Use longer sampling intervals in production environments to minimize overhead.
