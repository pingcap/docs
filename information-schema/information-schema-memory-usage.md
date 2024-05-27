---
title: MEMORY_USAGE
summary: MEMORY_USAGE information_schema システム テーブルについて学習します。
---

# メモリ使用量 {#memory-usage}

`MEMORY_USAGE`表は、現在の TiDB インスタンスの現在のメモリ使用量を示します。

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

`MEMORY_USAGE`の表の列は次のように説明されます。

-   MEMORY_TOTAL: TiDB の使用可能なメモリの合計 (バイト単位)。
-   MEMORY_LIMIT: TiDB のメモリ使用量制限 (バイト単位)。値はシステム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)の値と同じです。
-   MEMORY_CURRENT: TiDB の現在のメモリ使用量 (バイト単位)。
-   MEMORY_MAX_USED: TiDB の起動時から現在までのメモリ使用量 (バイト単位)。
-   CURRENT_OPS: &quot;shrinking&quot; | null。&quot;shrinking&quot; は、TiDB がメモリ使用量を削減する操作を実行していることを意味します。
-   SESSION_KILL_LAST: セッションが最後に終了した時のタイムスタンプ。
-   SESSION_KILL_TOTAL: TiDB の開始時から現在までのセッションが終了した回数。
-   GC_LAST:メモリ使用量によってGolang GC が最後にトリガーされたときのタイムスタンプ。
-   GC_TOTAL: TiDB の起動時から現在までの、メモリ使用量によってGolang GC がトリガーされた回数。
-   DISK_USAGE: 現在のデータスピル操作のディスク使用量（バイト単位）。
-   QUERY_FORCE_DISK: TiDB が開始されてから現在までにデータがディスクに書き出された回数。

## 参照 {#see-also}

<CustomContent platform="tidb">

-   [TiDBメモリ制御](/configure-memory-usage.md)
-   [TiKVメモリパラメータのパフォーマンスを調整する](/tune-tikv-memory-performance.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiDBメモリ制御](https://docs.pingcap.com/tidb/stable/configure-memory-usage)
-   [TiKVメモリパラメータのパフォーマンスを調整する](https://docs.pingcap.com/tidb/stable/tune-tikv-memory-performance)

</CustomContent>
