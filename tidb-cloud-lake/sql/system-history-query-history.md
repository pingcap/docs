---
title: system_history.query_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.764"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='QUERY HISTORY'/>

**Complete SQL execution audit trail** - Records comprehensive details of all SQL queries executed in Databend. Each query generates two entries (start and finish), providing complete visibility into:

- **Performance Analysis**: Query duration, resource usage, and optimization opportunities
- **Security Auditing**: Who executed what queries, when, and from where
- **Compliance Tracking**: Complete audit trail for regulatory requirements
- **Usage Monitoring**: Database activity patterns and user behavior analysis

## Fields

| Field                     | Type             | Description                                                                                   |
|---------------------------|------------------|-----------------------------------------------------------------------------------------------|
| log_type                  | TINYINT          | Query status: 1=Start, 2=Finish, 3=Error, 4=Aborted, 5=Closed.                                     |
| log_type_name             | VARCHAR          | String name of query status: "Start", "Finish", "Error", "Aborted", or "Closed".                                           |
| handler_type              | VARCHAR          | The protocol or handler used for the query (e.g., `HTTPQuery`, `MySQL`).                                 |
| tenant_id                 | VARCHAR          | The tenant identifier.                                                                        |
| cluster_id                | VARCHAR          | The cluster identifier.                                                                       |
| node_id                   | VARCHAR          | The node identifier.                                             |
| sql_user                  | VARCHAR          | The user who executed the query.                                                              |
| sql_user_quota            | VARCHAR          | The quota information of the user.                                                            |
| sql_user_privileges       | VARCHAR          | The privileges of the user.                                                                   |
| query_id                  | VARCHAR          | The unique identifier for the query.                                                          |
| query_kind                | VARCHAR          | The kind of query (e.g., `Query`, `Insert`, `CopyIntoTable`, etc.).                                                |
| query_text                | VARCHAR          | The SQL text of the query.                                                               |
| query_hash                | VARCHAR          | The hash value of the query text.                                                             |
| query_parameterized_hash  | VARCHAR          | The hash value of the query regardless of the specific values.                                                    |
| event_date                | DATE             | The date when the event occurred.                                                             |
| event_time                | TIMESTAMP        | The timestamp when the event occurred.                                                        |
| query_start_time          | TIMESTAMP        | The timestamp when the query started.                                                         |
| query_duration_ms         | BIGINT           | The total duration of the query in milliseconds (includes both queue time and execution time).                                                    |
| query_queued_duration_ms  | BIGINT           | The time the query spent in the queue in milliseconds.                                        |
| current_database          | VARCHAR          | The database in use when the query was executed.                                              |
| written_rows              | BIGINT UNSIGNED  | The number of rows written by the query.                                                      |
| written_bytes             | BIGINT UNSIGNED  | The number of bytes written by the query.                                                     |
| join_spilled_rows         | BIGINT UNSIGNED  | The number of rows spilled during join operations.                                            |
| join_spilled_bytes        | BIGINT UNSIGNED  | The number of bytes spilled during join operations.                                           |
| agg_spilled_rows          | BIGINT UNSIGNED  | The number of rows spilled during aggregation operations.                                     |
| agg_spilled_bytes         | BIGINT UNSIGNED  | The number of bytes spilled during aggregation operations.                                    |
| group_by_spilled_rows     | BIGINT UNSIGNED  | The number of rows spilled during group by operations.                                        |
| group_by_spilled_bytes    | BIGINT UNSIGNED  | The number of bytes spilled during group by operations.                                       |
| written_io_bytes          | BIGINT UNSIGNED  | The number of bytes written to IO.                                                            |
| written_io_bytes_cost_ms  | BIGINT UNSIGNED  | The IO cost in milliseconds for writing.                                                      |
| scan_rows                 | BIGINT UNSIGNED  | The number of rows scanned by the query.                                                      |
| scan_bytes                | BIGINT UNSIGNED  | The number of bytes scanned by the query.                                                     |
| scan_io_bytes             | BIGINT UNSIGNED  | The number of IO bytes read during scanning.                                                  |
| scan_io_bytes_cost_ms     | BIGINT UNSIGNED  | The IO cost in milliseconds for scanning.                                                     |
| scan_partitions           | BIGINT UNSIGNED  | The number of partitions scanned.                                                             |
| total_partitions          | BIGINT UNSIGNED  | The total number of partitions involved.                                                      |
| result_rows               | BIGINT UNSIGNED  | The number of rows in the query result.                                                       |
| result_bytes              | BIGINT UNSIGNED  | The number of bytes in the query result.                                                      |
| bytes_from_remote_disk    | BIGINT UNSIGNED  | The number of bytes read from remote disk.                                                    |
| bytes_from_local_disk     | BIGINT UNSIGNED  | The number of bytes read from local disk.                                                     |
| bytes_from_memory         | BIGINT UNSIGNED  | The number of bytes read from memory.                                                         |
| client_address            | VARCHAR          | The address of the client that issued the query.                                              |
| user_agent                | VARCHAR          | The user agent string of the client.                                                          |
| exception_code            | INT              | The exception code if the query failed.                                                       |
| exception_text            | VARCHAR          | The exception message if the query failed.                                                    |
| server_version            | VARCHAR          | The version of the server that processed the query.                                           |
| query_tag                 | VARCHAR          | The tag associated with the query.                                                            |
| has_profile               | BOOLEAN          | Whether the query has an associated execution profile.                                        |
| peek_memory_usage         | VARIANT          | The peak memory usage during query execution (as a JSON object).                              |
| session_id                | VARCHAR          | The session identifier associated with the query.                                             |


## Examples

Query the history for a specific query using its `query_id`

```sql
SELECT * FROM system_history.query_history WHERE query_id = '4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43';

*************************** 1. row ***************************
                log_type: 2
           log_type_name: Finish
            handler_type: HTTPQuery
               tenant_id: test_tenant
              cluster_id: test_cluster
                 node_id: jxSgvulZFAq1sDckR1bu85
                sql_user: root
          sql_user_quota: NULL
     sql_user_privileges: NULL
                query_id: 4e1f50a9-bce2-45cc-86e4-c7a36b9b8d43
              query_kind: Query
              query_text: SELECT * FROM t
              query_hash: cd36a2072e7f9deaa746db7480200944
query_parameterized_hash: cd36a2072e7f9deaa746db7480200944
              event_date: 2025-06-12
              event_time: 2025-06-12 03:31:35.135987
        query_start_time: 2025-06-12 03:31:35.041725
       query_duration_ms: 94
query_queued_duration_ms: 0
        current_database: default
            written_rows: 0
           written_bytes: 0
       join_spilled_rows: 0
      join_spilled_bytes: 0
        agg_spilled_rows: 0
       agg_spilled_bytes: 0
   group_by_spilled_rows: 0
  group_by_spilled_bytes: 0
        written_io_bytes: 0
written_io_bytes_cost_ms: 0
               scan_rows: 1
              scan_bytes: 20
           scan_io_bytes: 605
   scan_io_bytes_cost_ms: 0
         scan_partitions: 1
        total_partitions: 1
             result_rows: 1
            result_bytes: 20
  bytes_from_remote_disk: 74
   bytes_from_local_disk: 0
       bytes_from_memory: 0
          client_address: 127.0.0.1
              user_agent: bendsql/0.26.2-unknown
          exception_code: 0
          exception_text: 
          server_version: v1.2.753-nightly-c3d5fabb79(rust-1.88.0-nightly-2025-06-12T01:48:36.733925000Z)
               query_tag: 
             has_profile: NULL
       peek_memory_usage: {"jxSgvulZFAq1sDckR1bu85":223840}
              session_id: e3c54c32-f3c0-4ea9-bdd2-65701aa3f2a6
```
