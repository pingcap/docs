---
title: MEMORY_USAGE
summary: 了解 `MEMORY_USAGE` information_schema 系统表。
---

# MEMORY_USAGE

`MEMORY_USAGE` 表描述了当前 TiDB 实例的内存使用情况。

```sql
USE information_schema;
DESC memory_usage;
```

```sql
+--------------------+-------------+------+------+---------+-------+
| Field              | Type        | Null | Key  | Default | Extra |
+--------------------+-------------+------+------+---------+-------+
| MEMORY_TOTAL       | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_LIMIT       | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_CURRENT     | bigint(21)  | NO   |      | NULL    |       |
| MEMORY_MAX_USED    | bigint(21)  | NO   |      | NULL    |       |
| CURRENT_OPS        | varchar(50) | YES  |      | NULL    |       |
| SESSION_KILL_LAST  | datetime    | YES  |      | NULL    |       |
| SESSION_KILL_TOTAL | bigint(21)  | NO   |      | NULL    |       |
| GC_LAST            | datetime    | YES  |      | NULL    |       |
| GC_TOTAL           | bigint(21)  | NO   |      | NULL    |       |
| DISK_USAGE         | bigint(21)  | NO   |      | NULL    |       |
| QUERY_FORCE_DISK   | bigint(21)  | NO   |      | NULL    |       |
+--------------------+-------------+------+------+---------+-------+
11 行，耗时 0.000 秒
```


```sql
SELECT * FROM information_schema.memory_usage;
```

```sql
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
| MEMORY_TOTAL | MEMORY_LIMIT | MEMORY_CURRENT | MEMORY_MAX_USED | CURRENT_OPS | SESSION_KILL_LAST   | SESSION_KILL_TOTAL | GC_LAST             | GC_TOTAL | DISK_USAGE | QUERY_FORCE_DISK |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
|  33674170368 |  10737418240 |     5097644032 |     10826604544 | NULL        | 2022-10-17 22:47:47 |                  1 | 2022-10-17 22:47:47 |       20 |          0 |                0 |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
2 行，耗时 0.002 秒
```

`MEMORY_USAGE` 表中的列说明如下：

* MEMORY_TOTAL：TiDB 的总可用内存，单位为字节。
* MEMORY_LIMIT：TiDB 的内存使用限制，单位为字节。该值与系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 的值相同。
* MEMORY_CURRENT：TiDB 当前的内存使用量，单位为字节。
* MEMORY_MAX_USED：TiDB 从启动到当前的最大内存使用量，单位为字节。
* CURRENT_OPS： "shrinking" | null。 "shrinking" 表示 TiDB 正在执行缩减内存的操作。
* SESSION_KILL_LAST：上次终止会话的时间戳。
* SESSION_KILL_TOTAL：自 TiDB 启动以来，终止会话的次数。
* GC_LAST：上次由内存使用触发的 Golang 垃圾回收（GC）时间戳。
* GC_TOTAL：自 TiDB 启动以来，由内存使用触发的 Golang 垃圾回收（GC）次数。
* DISK_USAGE：当前数据溢出操作的磁盘使用量，单位为字节。
* QUERY_FORCE_DISK：自 TiDB 启动以来，数据溢出到磁盘的次数。

## 相关链接

<CustomContent platform="tidb">

- [TiDB memory control](/configure-memory-usage.md)
- [Tune TiKV memory parameter performance](/tune-tikv-memory-performance.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

- [TiDB memory control](https://docs.pingcap.com/tidb/stable/configure-memory-usage)
- [Tune TiKV memory parameter performance](https://docs.pingcap.com/tidb/stable/tune-tikv-memory-performance)

</CustomContent>