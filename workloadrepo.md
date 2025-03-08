---
title: TiDB Workload Repository
summary: The workload repository is a system for collecting and storing historical workload data from a TiDB cluster.
---

# TiDB Workload Repository

The workload repository is a system for collecting and storing historical workload data from a TiDB cluster. It periodically samples various system tables to track cluster performance and usage patterns over time.

## Enabling the Workload Repository

To enable the Workload Repository, set the following system variable:

```sql
SET GLOBAL tidb_workload_repository_dest = 'table';
```

To disable it:

```sql
SET GLOBAL tidb_workload_repository_dest = '';
```

## Data Collection

The Workload Repository stores data in tables under the `WORKLOAD_SCHEMA` database. It collects data via two different methods:
* The Snapshot process, which runs at configurable intervals, typically hourly, and can be triggered manually.
* The Time-based process, which runs at shorter intervals, typically every 5 seconds.

## Snapshot Sampling Process (Hourly by default)
The snapshot sampling process, which runs every 15 minutes to 2 hours, samples data from various monitoring tables. Snapshots are initiated from one of the TiDB nodes at the specified intervals, and process is as follows:

 1. From the initiating node a row is inserted into HIST_SNAPSHOTS, capturing the snapshot’s ID, start and end timestamps, and server version details.
 2. On each TiDB node, all rows from the source tables are copied to the corresponding history tables with the 'HIST_' prefix. The copied data includes the original columns from the source tables plus additional columns for the timestamp, instance ID, and snapshot ID.

Note that the sampled tables return data specific to the TiDB node from which they are queried.

Data is sampled from the following tables:

| Table Name | Destination Table | Description |
| --- | --- | --- |
| TIDB_INDEX_USAGE | HIST_TIDB_INDEX_USAGE | Index usage statistics |
| TIDB_STATEMENTS_STATS | HIST_TIDB_STATEMENTS_STATS | Statement statistics |
| CLIENT_ERRORS_SUMMARY_BY_HOST | HIST_CLIENT_ERRORS_SUMMARY_BY_HOST | Client error summaries by host |
| CLIENT_ERRORS_SUMMARY_BY_USER | HIST_CLIENT_ERRORS_SUMMARY_BY_USER | Client error summaries by user |
| CLIENT_ERRORS_SUMMARY_GLOBAL | HIST_CLIENT_ERRORS_SUMMARY_GLOBAL | Client error summaries by global |

The snapshot sampling interval may be controlled with [`tidb_workload_repository_snapshot_interval`](/system-variables.md#tidb_workload_repository_snapshot_interval):
```sql
SET GLOBAL tidb_workload_repository_snapshot_interval = 900; -- set interval to 15 minutes
```

## Taking Manual Snapshots

Note that while the snapshot sampling process runs automatically based on the configured interval, you can also trigger a manual snapshot using:

```sql
ADMIN WORKLOAD REPOSITORY TAKE SNAPSHOT;
```

## Time-based Sampling Process (Every 5 seconds by default)
The time-based sampling process, which runs every 1 to 600 seconds, samples data from various monitoring tables.

When the time-base sampling process runs all rows from the source tables are copied to the corresponding history tables with the 'HIST_' prefix. The copied data includes the original columns from the source tables plus additional columns for the timestamp and instance ID.

Unlike the Snapshot Sampling process, a row will not be added to the `HIST_SNAPSHOTS` table.

Note that the sampled tables return data specific to the TiDB node from which they are queried.

Data is sampled from the following tables:


| Table Name | Destination Table | Description |
| --- | --- | --- |
| PROCESSLIST | HIST_PROCESSLIST | Active sessions
| DATA_LOCK_WAITS | HIST_DATA_LOCK_WAITS | Data lock waits |
| TIDB_TRX | HIST_TIDB_TRX | Active transactions |
| MEMORY_USAGE | HIST_MEMORY_USAGE | Memory usage |
| DEADLOCKS | HIST_DEADLOCKS | Deadlock information |

The time-based sampling interval may be controlled with [tidb_workload_repository_active_sampling_interval](/system-variables.md#tidb_workload_repository_active_sampling_interval):
```sql
SET GLOBAL tidb_workload_repository_active_sampling_interval = 20; -- set interval to 20 seconds
```

## Data Retention

The system automatically purges data based on the retention period setting, using partitions for efficient data management.

The [tidb_workload_repository_retention_days](/system-variables.md#tidb_workload_repository_retention_days) variable controls the retention period for historical data in the Workload Repository. For example, to keep data for 30 days:

```sql
SET GLOBAL tidb_workload_repository_retention_days = 30;
```

A higher value for this variable allows for longer data retention, which may be beneficial for workload analysis, but will increase storage requirements.


## Notes

- Enabling the Workload Repository may have a small performance impact on the system.
- Setting sampling intervals too low may increase system overhead.
- Setting retention days to 0 disables automatic purging of old data.

## Best Practices

1. Start with default settings and adjust based on your monitoring needs.
2. Set reasonable retention periods based on your storage capacity.
3. Monitor the size of the `WORKLOAD_SCHEMA` database.
4. Use longer sampling intervals in production environments to minimize overhead.
