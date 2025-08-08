---
title: MEMORY_USAGE_OPS_HISTORY
summary: MEMORY_USAGE_OPS_HISTORY` information_schema システム テーブルについて学習します。
---

# メモリ使用量オペレーション履歴 {#memory-usage-ops-history}

`MEMORY_USAGE_OPS_HISTORY`テーブルは、メモリ関連の操作の履歴と現在の TiDB インスタンスの実行基準を示します。

```sql
USE information_schema;
DESC memory_usage_ops_history;
```

```sql
+----------------+---------------------+------+------+---------+-------+
| Field          | Type                | Null | Key  | Default | Extra |
+----------------+---------------------+------+------+---------+-------+
| TIME           | datetime            | NO   |      | NULL    |       |
| OPS            | varchar(20)         | NO   |      | NULL    |       |
| MEMORY_LIMIT   | bigint(21)          | NO   |      | NULL    |       |
| MEMORY_CURRENT | bigint(21)          | NO   |      | NULL    |       |
| PROCESSID      | bigint(21) unsigned | YES  |      | NULL    |       |
| MEM            | bigint(21) unsigned | YES  |      | NULL    |       |
| DISK           | bigint(21) unsigned | YES  |      | NULL    |       |
| CLIENT         | varchar(64)         | YES  |      | NULL    |       |
| DB             | varchar(64)         | YES  |      | NULL    |       |
| USER           | varchar(16)         | YES  |      | NULL    |       |
| SQL_DIGEST     | varchar(64)         | YES  |      | NULL    |       |
| SQL_TEXT       | varchar(256)        | YES  |      | NULL    |       |
+----------------+---------------------+------+------+---------+-------+
12 rows in set (0.000 sec)
```

```sql
SELECT * FROM information_schema.memory_usage_ops_history;
```

```sql
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| TIME                | OPS         | MEMORY_LIMIT | MEMORY_CURRENT | PROCESSID           | MEM        | DISK | CLIENT          | DB   | USER | SQL_DIGEST                                                       | SQL_TEXT                                                             |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
| 2022-10-17 22:46:25 | SessionKill |  10737418240 |    10880237568 | 6718275530455515543 | 7905028235 |    0 | 127.0.0.1:34394 | test | root | 146b3d812852663a20635fbcf02be01688f52c8d433dafec0d496a14f0b59df6 | desc analyze select * from t t1 join t t2 on t1.a=t2.a order by t1.a |
+---------------------+-------------+--------------+----------------+---------------------+------------+------+-----------------+------+------+------------------------------------------------------------------+----------------------------------------------------------------------+
2 rows in set (0.002 sec)
```

`MEMORY_USAGE_OPS_HISTORY`テーブル内の列は次のように説明されます。

-   `TIME` : セッションが終了したときのタイムスタンプ。
-   `OPS` ：「セッションキル」
-   `MEMORY_LIMIT` : TiDB終了時のメモリ使用量制限（バイト単位）。この値はシステム変数`tidb_server_memory_limit`の値と同じです。[/system-variables.md#tidb_server_memory_limit-new-in-v640]。
-   `MEMORY_CURRENT` : TiDB の現在のメモリ使用量 (バイト単位)。
-   `PROCESSID` : 終了したセッションの接続 ID。
-   `MEM` : 終了したセッションのメモリ使用量（バイト単位）。
-   `DISK` : 終了したセッションのディスク使用量（バイト単位）。
-   `CLIENT` : 終了したセッションのクライアント接続アドレス。
-   `DB` : 終了したセッションに接続されていたデータベースの名前。
-   `USER` : 終了したセッションのユーザー名。
-   `SQL_DIGEST` : 終了したセッションで実行されている SQL ステートメントのダイジェスト。
-   `SQL_TEXT` : 終了したセッションで実行されている SQL ステートメント。
