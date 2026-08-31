---
title: mysql.tidb_mview_refresh_hist
summary: Learn about the materialized view refresh history table in the `mysql` schema.
---

# `mysql.tidb_mview_refresh_hist`

The `mysql.tidb_mview_refresh_hist` table stores the refresh history of materialized views. You can query this table to review refresh jobs, their duration and status, the number of refreshed rows, and failure information.

To view the structure of the table, use the following SQL statement:

```sql
DESC mysql.tidb_mview_refresh_hist;
```

## Fields

| Field | Type | Description |
| :-- | :-- | :-- |
| `REFRESH_JOB_ID` | `BIGINT UNSIGNED` | The identifier of the refresh job. |
| `MVIEW_ID` | `BIGINT` | The identifier of the materialized view. |
| `MVIEW_SCHEMA` | `VARCHAR(64)` | The schema name of the materialized view. |
| `MVIEW_NAME` | `VARCHAR(64)` | The name of the materialized view. |
| `REFRESH_METHOD` | `VARCHAR(32)` | The method used to refresh the materialized view. |
| `REFRESH_START_TIME` | `DATETIME(6)` | The time when the refresh job started. |
| `REFRESH_END_TIME` | `DATETIME(6)` | The time when the refresh job ended. |
| `REFRESH_DURATION_SEC` | `DECIMAL(18,6)` | The refresh duration in seconds. |
| `REFRESH_SCHEDULE_DURATION_SEC` | `DECIMAL(18,6)` | The time in seconds that the refresh job spent waiting for or being processed by the refresh scheduler. |
| `REFRESH_STATUS` | `VARCHAR(16)` | The status of the refresh job. |
| `REFRESH_ROWS` | `BIGINT` | The number of rows refreshed by the job. |
| `REFRESH_READ_TSO` | `BIGINT UNSIGNED` | The read timestamp used by the refresh job. |
| `REFRESH_COMMIT_TSO` | `BIGINT UNSIGNED` | The commit timestamp of the refresh job. |
| `REFRESH_FAILED_REASON` | `TEXT` | The reason why the refresh job failed. |
| `CANCEL_REQUEST_TIME` | `DATETIME(6)` | The time when a cancellation was requested for the refresh job. |
| `CANCEL_REQUESTED_BY` | `VARCHAR(512)` | The user or session that requested cancellation. |
| `LAST_HEARTBEAT_TIME` | `DATETIME(6)` | The time of the latest heartbeat from the refresh job. |

## Examples

To query the most recent materialized view refresh jobs, run the following statement:

```sql
SELECT *
FROM mysql.tidb_mview_refresh_hist
ORDER BY REFRESH_START_TIME DESC;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`mysql.tidb_mlog_purge_hist`](/mysql-schema/mysql-schema-tidb-mlog-purge-hist.md)
