---
title: MEMORY_USAGE
summary: Learn the `MEMORY_USAGE` information_schema system table.
---

# メモリ使用量 {#memory-usage}

`MEMORY_USAGE`番目の表は、現在の TiDB インスタンスの現在のメモリ使用量を示しています。

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
11 rows in set (0.000 sec)
```

{{< copyable "" >}}

```sql
SELECT * FROM information_schema.memory_usage;
```

```sql
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
| MEMORY_TOTAL | MEMORY_LIMIT | MEMORY_CURRENT | MEMORY_MAX_USED | CURRENT_OPS | SESSION_KILL_LAST   | SESSION_KILL_TOTAL | GC_LAST             | GC_TOTAL | DISK_USAGE | QUERY_FORCE_DISK |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
|  33674170368 |  10737418240 |     5097644032 |     10826604544 | NULL        | 2022-10-17 22:47:47 |                  1 | 2022-10-17 22:47:47 |       20 |          0 |                0 |
+--------------+--------------+----------------+-----------------+-------------+---------------------+--------------------+---------------------+----------+------------+------------------+
2 rows in set (0.002 sec)
```

`MEMORY_USAGE`表の列は、次のように説明されています。

-   MEMORY_TOTAL: TiDB の使用可能なメモリの合計 (バイト単位)。
-   MEMORY_LIMIT: TiDB のメモリ使用制限 (バイト単位)。値は、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)の値と同じです。
-   MEMORY_CURRENT: TiDB の現在のメモリ使用量 (バイト単位)。
-   MEMORY_MAX_USED: TiDB の起動時から現在までの最大メモリ使用量 (バイト単位)。
-   CURRENT_OPS: &quot;縮小&quot; |ヌル。 「縮小」とは、TiDB がメモリ使用量を縮小する操作を実行していることを意味します。
-   SESSION_KILL_LAST: セッションが最後に終了したときのタイムスタンプ。
-   SESSION_KILL_TOTAL: TiDB が開始されてから現在までにセッションが終了した回数。
-   GC_LAST:メモリ使用量によって最後にGolang GC がトリガーされたときのタイムスタンプ。
-   GC_TOTAL: TiDB が開始されてから現在までに、メモリ使用量によってGolang GC がトリガーされた回数。
-   DISK_USAGE: 現在のデータ スピル操作のディスク使用量 (バイト単位)。
-   QUERY_FORCE_DISK: TiDB が開始されてから現在の時刻までに、データがディスクにスピルされた回数。
