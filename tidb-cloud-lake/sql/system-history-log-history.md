---
title: system_history.log_history
---

import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.764"/>

import EEFeature from '@site/src/components/EEFeature';

<EEFeature featureName='LOG HISTORY'/>

**System operations audit trail** - Raw log repository from all Databend nodes and components. Foundation for operational intelligence:

- **System Monitoring**: Track system health, performance, and resource usage
- **Troubleshooting**: Debug issues with detailed error logs and system events
- **Operational Analytics**: Analyze system behavior patterns and trends
- **Root Cause Analysis**: Investigate system failures and performance bottlenecks

> **Note:** This table contains raw log data that feeds into other specialized history tables. Other tables provide structured, query-specific views of this data.

## Fields

| Field        | Type      | Description                                      |
|--------------|-----------|--------------------------------------------------|
| timestamp    | TIMESTAMP | The timestamp when the log entry was recorded    |
| path         | VARCHAR   | Source file path and line number of the log      |
| target       | VARCHAR   | Target module or component of the log            |
| log_level    | VARCHAR   | Log level (e.g., `INFO`, `ERROR`)                    |
| cluster_id   | VARCHAR   | Identifier of the cluster                        |
| node_id      | VARCHAR   | Identifier of the node                           |
| warehouse_id | VARCHAR   | Identifier of the warehouse                      |
| query_id     | VARCHAR   | Query ID associated with the log                 |
| message      | VARCHAR   | Log message content                              |
| fields       | VARIANT   | Additional fields (as a JSON object)             |
| batch_number | BIGINT    | Internal use, no special meaning                 |

Note: The `message` field stores plain text logs, while the `fields` field stores logs in JSON format.

For example, the `fields` field of a log entry might look like:
```
fields: {"node_id":"8R5ZMF8q0HHE6x9H7U1gr4","query_id":"72d2319a-b6d6-4b1d-8694-670137a40d87","session_id":"189fd3e2-e6ac-48c3-97ef-73094c141312","sql":"select * from system_history.log_history"}
```

the `message` field of another log entry might appear as follows:
```
message: [HTTP-QUERY] Preparing to plan SQL query
```

## Examples

```sql
SELECT * FROM system_history.log_history LIMIT 1;

*************************** 1. row ***************************
   timestamp: 2025-06-03 01:29:49.335455
        path: databend_common_meta_client::channel_manager: channel_manager.rs:86
      target: databend_common_meta_client::channel_manager
   log_level: INFO
  cluster_id: test_cluster
     node_id: CkdmtwYXLRMhJIvVzl6i11
warehouse_id: NULL
    query_id: NULL
     message: MetaChannelManager done building RealClient to 127.0.0.1:9191, start handshake
      fields: {}
batch_number: 41
```
