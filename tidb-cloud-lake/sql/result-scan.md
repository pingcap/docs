---
title: RESULT_SCAN
summary: 通过查询 ID 检索先前查询的缓存结果。
---

# RESULT_SCAN

通过查询 ID 检索先前查询的缓存结果。

另请参阅：[system.query_cache](/tidb-cloud-lake/sql/system-query-cache.md)

## 语法 {#syntax}

```sql
RESULT_SCAN('<query_id>' | LAST_QUERY_ID())
```

## 示例 {#examples}

以下示例展示了如何启用查询结果缓存，并运行一个其结果将被缓存的查询：

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

结果被缓存后，你可以使用 `RESULT_SCAN` 检索该结果，而无需重新运行查询：

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