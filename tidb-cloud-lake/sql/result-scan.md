---
title: RESULT_SCAN
summary: クエリ ID を使用して、以前のクエリのキャッシュされた結果を取得します。
---

# RESULT_SCAN

クエリ ID を使用して、以前のクエリのキャッシュされた結果を取得します。

関連情報: [system.query_cache](/tidb-cloud-lake/sql/system-query-cache.md)

## 構文 {#syntax}

```sql
RESULT_SCAN('<query_id>' | LAST_QUERY_ID())
```

## 例 {#examples}

次の例は、クエリ結果キャッシュを有効にし、結果がキャッシュされるクエリを実行する方法を示しています。

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

結果がキャッシュされると、`RESULT_SCAN` を使用してクエリを再実行せずにその結果を取得できます。

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