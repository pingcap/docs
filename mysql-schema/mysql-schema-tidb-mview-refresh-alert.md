---
title: mysql.tidb_mview_refresh_alert
summary: Learn about the materialized view refresh alert table in the `mysql` schema.
---

# `mysql.tidb_mview_refresh_alert`

The `mysql.tidb_mview_refresh_alert` table stores the current refresh alert information for each materialized view. You can query this table to check the alert level and the latest refresh status of materialized views.

To view the structure of the table, use the following SQL statement:

```sql
DESC mysql.tidb_mview_refresh_alert;
```

## Fields

| Field | Type | Description |
| :-- | :-- | :-- |
| `MVIEW_ID` | `BIGINT` | The identifier of the materialized view. |
| `MVIEW_SCHEMA` | `VARCHAR(64)` | The schema name of the materialized view. |
| `MVIEW_NAME` | `VARCHAR(64)` | The name of the materialized view. |
| `ALERT_LEVEL` | `VARCHAR(16)` | The current alert level of the materialized view. |
| `REFRESH_FAILED` | `VARCHAR(3)` | Indicates whether the materialized view refresh failed. |
| `LAST_SUCCESS_SNAPSHOT_TIME` | `DATETIME(6)` | The time of the latest successful snapshot. |
| `UPDATE_TIME` | `DATETIME(6)` | The time when the alert information was updated. |

## Examples

To query the refresh alert information for materialized views, run the following statement:

```sql
SELECT *
FROM mysql.tidb_mview_refresh_alert;
```

## See also

- [Materialized Views](/materialized-views.md)
- [`mysql.tidb_mview_refresh_hist`](/mysql-schema/mysql-schema-tidb-mview-refresh-hist.md)
