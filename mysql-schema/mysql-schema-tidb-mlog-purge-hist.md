---
title: mysql.tidb_mlog_purge_hist
summary: Learn about the materialized view log purge history table in the `mysql` schema.
---

# `mysql.tidb_mlog_purge_hist`

The `mysql.tidb_mlog_purge_hist` table stores the purge history of materialized view logs. You can query this table to review purge jobs, their duration and status, the number of purged rows, and failure information.

To view the structure of the table, use the following SQL statement:

```sql
DESC mysql.tidb_mlog_purge_hist;
```

## Fields

| Field | Type | Description |
| :-- | :-- | :-- |
| `PURGE_JOB_ID` | `BIGINT UNSIGNED` | The identifier of the purge job. |
| `MLOG_ID` | `BIGINT` | The identifier of the materialized view log. |
| `BASE_TABLE_SCHEMA` | `VARCHAR(64)` | The schema name of the base table for the materialized view log. |
| `BASE_TABLE_NAME` | `VARCHAR(64)` | The name of the base table for the materialized view log. |
| `PURGE_METHOD` | `VARCHAR(32)` | The method used to purge the materialized view log. |
| `PURGE_START_TIME` | `DATETIME(6)` | The time when the purge job started. |
| `PURGE_END_TIME` | `DATETIME(6)` | The time when the purge job ended. |
| `PURGE_DURATION_SEC` | `DECIMAL(18,6)` | The purge duration in seconds. |
| `PURGE_ROWS` | `BIGINT` | The number of rows purged by the job. |
| `PURGE_STATUS` | `VARCHAR(16)` | The status of the purge job. |
| `PURGE_CUTOFF_TSO` | `BIGINT UNSIGNED` | The cutoff timestamp used by the purge job. |
| `PURGE_FAILED_REASON` | `TEXT` | The reason why the purge job failed. |
| `CANCEL_REQUEST_TIME` | `DATETIME(6)` | The time when a cancellation was requested for the purge job. |
| `CANCEL_REQUESTED_BY` | `VARCHAR(512)` | The user or session that requested cancellation. |
| `LAST_HEARTBEAT_TIME` | `DATETIME(6)` | The time of the latest heartbeat from the purge job. |

## Examples

To query the most recent materialized view log purge jobs, run the following statement:

```sql
SELECT *
FROM mysql.tidb_mlog_purge_hist
ORDER BY PURGE_START_TIME DESC;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md)
