---
title: Troubleshooting
summary: This page describes how to troubleshoot common issues in TiDB Cloud Lake.
---

# Troubleshooting

Diagnose slow queries, errors, resource usage, and login issues using `system_history` tables. Use `profile_history` for per-operator execution analysis (CPU time, I/O, spill, output rows). All tables are per-tenant isolated.

## Tables

### system_history.query_history

Complete SQL execution audit trail. Every query generates entries with start/finish status.

| Field | Type | Description |
|-------|------|-------------|
| log_type | TINYINT | Query status: 1=Start, 2=Finish, 3=Error, 4=Aborted, 5=Closed |
| log_type_name | VARCHAR | String name: "Start", "Finish", "Error", "Aborted", "Closed" |
| handler_type | VARCHAR | Protocol used (e.g., `HTTPQuery`, `MySQL`) |
| tenant_id | VARCHAR | Tenant identifier |
| cluster_id | VARCHAR | Cluster identifier |
| node_id | VARCHAR | Node identifier |
| sql_user | VARCHAR | User who executed the query |
| sql_user_quota | VARCHAR | User quota information |
| sql_user_privileges | VARCHAR | User privileges |
| query_id | VARCHAR | Unique query identifier |
| query_kind | VARCHAR | Query kind (e.g., `Query`, `Insert`, `CopyIntoTable`) |
| query_text | VARCHAR | SQL text of the query |
| query_hash | VARCHAR | Hash of the query text |
| query_parameterized_hash | VARCHAR | Hash ignoring literal values |
| event_date | DATE | Date of the event |
| event_time | TIMESTAMP | Timestamp of the event |
| query_start_time | TIMESTAMP | Query start timestamp |
| query_duration_ms | BIGINT | Total duration in ms (queue + execution) |
| query_queued_duration_ms | BIGINT | Time spent in queue (ms) |
| current_database | VARCHAR | Database in use |
| written_rows | BIGINT UNSIGNED | Rows written |
| written_bytes | BIGINT UNSIGNED | Bytes written |
| join_spilled_rows | BIGINT UNSIGNED | Rows spilled during joins |
| join_spilled_bytes | BIGINT UNSIGNED | Bytes spilled during joins |
| agg_spilled_rows | BIGINT UNSIGNED | Rows spilled during aggregation |
| agg_spilled_bytes | BIGINT UNSIGNED | Bytes spilled during aggregation |
| group_by_spilled_rows | BIGINT UNSIGNED | Rows spilled during group by |
| group_by_spilled_bytes | BIGINT UNSIGNED | Bytes spilled during group by |
| written_io_bytes | BIGINT UNSIGNED | Bytes written to IO |
| written_io_bytes_cost_ms | BIGINT UNSIGNED | IO write cost (ms) |
| scan_rows | BIGINT UNSIGNED | Rows scanned |
| scan_bytes | BIGINT UNSIGNED | Bytes scanned |
| scan_io_bytes | BIGINT UNSIGNED | IO bytes read during scan |
| scan_io_bytes_cost_ms | BIGINT UNSIGNED | IO scan cost (ms) |
| scan_partitions | BIGINT UNSIGNED | Partitions scanned |
| total_partitions | BIGINT UNSIGNED | Total partitions involved |
| result_rows | BIGINT UNSIGNED | Rows in result |
| result_bytes | BIGINT UNSIGNED | Bytes in result |
| bytes_from_remote_disk | BIGINT UNSIGNED | Bytes read from remote disk |
| bytes_from_local_disk | BIGINT UNSIGNED | Bytes read from local disk |
| bytes_from_memory | BIGINT UNSIGNED | Bytes read from memory |
| client_address | VARCHAR | Client address |
| user_agent | VARCHAR | Client user agent |
| exception_code | INT | Exception code (0 = success) |
| exception_text | VARCHAR | Exception message |
| server_version | VARCHAR | Server version |
| query_tag | VARCHAR | Query tag |
| has_profile | BOOLEAN | Whether query has execution profile |
| peek_memory_usage | VARIANT | Peak memory usage (JSON) |
| session_id | VARCHAR | Session identifier |
| session_settings | VARCHAR | Session settings |

### system_history.profile_history

Detailed execution profiles for every query. Use `jq()` to extract per-operator statistics.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | TIMESTAMP | When the profile was recorded |
| query_id | VARCHAR | Query ID |
| profiles | VARIANT | JSON array of operators, each with `id`, `name`, `statistics[]` |
| statistics_desc | VARIANT | JSON describing statistics format |

Statistics array indices: `[0]`=OutputRows, `[1]`=OutputBytes, `[2]`=InputRows, `[3]`=InputBytes, `[4]`=CpuTime(ns).

### system_history.log_history

Raw log entries from all {{{ .lake }}} nodes and components.

| Field | Type | Description |
|-------|------|-------------|
| timestamp | TIMESTAMP | Log entry timestamp |
| path | VARCHAR | Source file path and line number |
| target | VARCHAR | Target module or component |
| log_level | VARCHAR | Log level (`INFO`, `ERROR`, `WARN`, etc.) |
| cluster_id | VARCHAR | Cluster identifier |
| node_id | VARCHAR | Node identifier |
| warehouse_id | VARCHAR | Warehouse identifier |
| query_id | VARCHAR | Associated query ID |
| message | VARCHAR | Log message (plain text) |
| fields | VARIANT | Additional fields (JSON) |
| batch_number | BIGINT | Internal use |

### system_history.access_history

Data lineage and access control audit. Tracks all objects accessed or modified.

| Field | Type | Description |
|-------|------|-------------|
| query_id | VARCHAR | Query ID |
| query_start | TIMESTAMP | Query start time |
| user_name | VARCHAR | User who executed the query |
| base_objects_accessed | VARIANT | Objects accessed (JSON array) |
| direct_objects_accessed | VARIANT | Reserved for future use |
| objects_modified | VARIANT | Objects modified by DML (JSON array) |
| object_modified_by_ddl | VARIANT | Objects modified by DDL (JSON array) |

JSON object fields: `object_domain` (Database/Table/Stage), `object_name`, `columns[]`, `stage_type`, `operation_type` (Create/Alter/Drop/Undrop), `properties`.

### system_history.login_history

Authentication audit trail for all login attempts.

| Field | Type | Description |
|-------|------|-------------|
| event_time | TIMESTAMP | Login event timestamp |
| handler | VARCHAR | Protocol (e.g., `HTTP`, `MySQL`) |
| event_type | VARCHAR | `LoginSuccess` or `LoginFailed` |
| connection_uri | VARCHAR | Connection URI |
| auth_type | VARCHAR | Authentication method (e.g., Password) |
| user_name | VARCHAR | User attempting login |
| client_ip | VARCHAR | Client IP address |
| user_agent | VARCHAR | Client user agent |
| session_id | VARCHAR | Session ID |
| node_id | VARCHAR | Node ID |
| error_message | VARCHAR | Error message if failed |

## Quick Examples

Find slow queries (>5s) in the last hour:

```sql
SELECT query_id, sql_user, query_duration_ms, query_text
FROM system_history.query_history
WHERE query_duration_ms > 5000
  AND event_time > now() - INTERVAL 1 HOUR
  AND log_type = 2
ORDER BY query_duration_ms DESC
LIMIT 20;
```

Find failed queries:

```sql
SELECT query_id, sql_user, exception_code, exception_text, query_text
FROM system_history.query_history
WHERE exception_code != 0
  AND event_time > now() - INTERVAL 1 HOUR
ORDER BY event_time DESC;
```

Check login failures:

```sql
SELECT event_time, user_name, client_ip, error_message
FROM system_history.login_history
WHERE event_type = 'LoginFailed'
  AND event_time > now() - INTERVAL 24 HOUR
ORDER BY event_time DESC;
```
