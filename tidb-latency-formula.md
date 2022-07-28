# TiDB Latency Formula

This document breaks down the latency into metrics, for those who have interests in observation of the metrics, it's a guide of TiDB's critical path diagnosis.

Generally, OLTP workload can be divided into read and write queries, they share some critical codes. This document will break down the latency and then analyze it from user's perspective. It's better to read [Performance Analysis and Tuning](performance-tuning-methods) before this document.

Metrics in this document can be read directly from prometheus of TiDB.

# General SQL Layer

This part of latency is on the top level of TiDB and shared by any queries.

```
e2e duration = 
    tidb_server_get_token_duration_seconds +
    tidb_session_parse_duration_seconds +
    tidb_session_compile_duration_seconds +
    tidb_session_execute_duration_seconds{type="general"}
```




