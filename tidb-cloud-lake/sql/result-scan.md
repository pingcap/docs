---
title: RESULT_SCAN
---

Retrieves the cached result of a previous query by its query ID.

See also: [system.query_cache](/sql/sql-reference/system-tables/system-query-cache)

## Syntax

```sql
RESULT_SCAN('<query_id>' | LAST_QUERY_ID())
```

## Examples

This example shows how to enable the query result cache and run a query whose result will be cached:

```bash
# Enable the query result cache feature
mysql> SET enable_query_result_cache = 1;
Query OK, 0 rows affected (0.01 sec)

# Cache all queries regardless of how fast they execute
mysql> SET query_result_cache_min_execute_secs = 0;
Query OK, 0 rows affected (0.01 sec)

# Execute a query and cache its result
mysql> SELECT * FROM t1 ORDER BY a;
+------+
| a    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.02 sec)
Read 0 rows, 0.00 B in 0.006 sec., 0 rows/sec., 0.00 B/sec.
```

Once the result is cached, you can use `RESULT_SCAN` to retrieve it without re-running the query:

```bash
# Retrieve the cached result of the previous query using its query ID
mysql> SELECT * FROM RESULT_SCAN(LAST_QUERY_ID()) ORDER BY a;
+------+
| a    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.02 sec)
Read 3 rows, 13.00 B in 0.006 sec., 464.06 rows/sec., 1.96 KiB/sec.
```