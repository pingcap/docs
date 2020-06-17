---
title: LOAD STATS
summary: An overview of the usage of LOAD STATS for the TiDB database.
category: reference
---

# LOAD STATS

The `LOAD STATS` statement is used to load statistics data into TiDB.

## Synopsis

**LoadStatsStmt:**

![LoadStatsStmt](/media/sqlgram/LoadStatsStmt.png)

## Examples

Users can access the address `http://${tidb-server-ip}:${tidb-server-status-port}/stats/dump/${db_name}/${table_name}` to download the TiDB instance's statistics data.

Users can use `LOAD STATS ${stats_path}` to load the specific statistics file.

The `${stats_path}` can be an absolute path or a relative path, and here is an example:

{{< copyable "sql" >}}

```sql
LOAD STATS '/tmp/stats.json';
```

```
Query OK, 0 rows affected (0.00 sec)
```

## See also

* [Statistics](/statistics.md)