---
title: MEMORY_USAGE
summary: Learn the `MEMORY_USAGE` information_schema system table.
---

# メモリ使用量 {#memory-usage}

表`MEMORY_USAGE`は、現在の TiDB インスタンスの現在のメモリ使用量を示しています。

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

`MEMORY_USAGE`のテーブルの列は次のように説明されます。

-   MEMORY_TOTAL: TiDB の利用可能なメモリの合計 (バイト単位)。
-   MEMORY_LIMIT: TiDB のメモリ使用制限 (バイト単位)。値はシステム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)と同じです。
-   MEMORY_CURRENT: TiDB の現在のメモリ使用量 (バイト単位)。
-   MEMORY_MAX_USED: TiDB の開始時から現在までの最大メモリ使用量 (バイト単位)。
-   CURRENT_OPS: &quot;縮小中&quot; |ヌル。 「縮小」とは、TiDB がメモリ使用量を縮小する操作を実行していることを意味します。
-   SESSION_KILL_LAST: 最後にセッションが終了したときのタイムスタンプ。
-   SESSION_KILL_TOTAL: TiDB の開始時から現在までの、セッションが終了された回数。
-   GC_LAST:メモリ使用量によってGolang GC が最後にトリガーされたときのタイムスタンプ。
-   GC_TOTAL: TiDB の開始時から現在までに、メモリ使用量によってGolang GC がトリガーされた回数。
-   DISK_USAGE: 現在のデータ流出操作のディスク使用量 (バイト単位)。
-   QUERY_FORCE_DISK: TiDB の開始時から現在までに、データがディスクに流出した回数。
