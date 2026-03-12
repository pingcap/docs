---
title: system.query_cache
---

Stores information about cached query results, including details such as the query ID, result size, and the location of the cached data.

| Column               | Type    | Description                                                           |
|----------------------|---------|-----------------------------------------------------------------------|
| `sql`                | String  | The original SQL text of the cached query.                            |
| `query_id`           | String  | The unique identifier of the query whose result is cached.            |
| `result_size`        | UInt64  | The size (in bytes) of the cached result file.                        |
| `num_rows`           | UInt64  | The number of rows in the cached result.                              |
| `partitions_sha`     | String  | The hash of the source partitions used to validate cache consistency. |
| `location`           | String  | The storage location (e.g., internal path) of the cached result file. |
| `active_result_scan` | Boolean | Whether the cached result is currently being used by a `RESULT_SCAN`. |

Example:

```sql
SELECT * FROM system.query_cache;

┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│        sql       │               query_id               │ result_size │ num_rows │                          partitions_sha                          │                                                         location                                                        │ active_result_scan │
├──────────────────┼──────────────────────────────────────┼─────────────┼──────────┼──────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┼────────────────────┤
│ SELECT * FROM t1 │ 39497827-9f20-464d-8389-0fb08129d9d4 │          13 │        3 │ 0756b2601aec1bccd8cc4b31f15692a993609364eead4595555933f2ec5f4f0d │ _result_cache/60050f5b0dc42f13b9803380b8dd576e582c66fcac68db0cdd1af915db166843/7468ce283bf9487fbc039b76c93047c1.parquet │ false              │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```