---
title: TIFLASH_TABLES
summary: TIFLASH_TABLES` information_schema テーブルについて学習します。
---

# TIFLASH_TABLES {#tiflash-tables}

> **警告：**
>
> このテーブルは不安定であり、TiDB の新しいリリースで予告なく変更される可能性があるため、本番環境では使用しないでください。

`TIFLASH_TABLES`表は、 TiFlashのデータ テーブルに関する統計情報を提供します。

```sql
USE information_schema;
DESC tiflash_tables;
```

```sql
+-------------------------------------------+--------------+------+------+---------+-------+
| Field                                     | Type         | Null | Key  | Default | Extra |
+-------------------------------------------+--------------+------+------+---------+-------+
| TIDB_DATABASE                             | varchar(64)  | YES  |      | NULL    |       |
| TIDB_TABLE                                | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID                                  | bigint       | YES  |      | NULL    |       |
| IS_TOMBSTONE                              | bigint       | YES  |      | NULL    |       |
| SEGMENT_COUNT                             | bigint       | YES  |      | NULL    |       |
| TOTAL_ROWS                                | bigint       | YES  |      | NULL    |       |
| TOTAL_SIZE                                | bigint       | YES  |      | NULL    |       |
| TOTAL_DELETE_RANGES                       | bigint       | YES  |      | NULL    |       |
| DELTA_RATE_ROWS                           | double       | YES  |      | NULL    |       |
| DELTA_RATE_SEGMENTS                       | double       | YES  |      | NULL    |       |
| DELTA_PLACED_RATE                         | double       | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE                          | bigint       | YES  |      | NULL    |       |
| DELTA_CACHE_RATE                          | double       | YES  |      | NULL    |       |
| DELTA_CACHE_WASTED_RATE                   | double       | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE                          | bigint       | YES  |      | NULL    |       |
| AVG_SEGMENT_ROWS                          | double       | YES  |      | NULL    |       |
| AVG_SEGMENT_SIZE                          | double       | YES  |      | NULL    |       |
| DELTA_COUNT                               | bigint       | YES  |      | NULL    |       |
| TOTAL_DELTA_ROWS                          | bigint       | YES  |      | NULL    |       |
| TOTAL_DELTA_SIZE                          | bigint       | YES  |      | NULL    |       |
| AVG_DELTA_ROWS                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_SIZE                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_DELETE_RANGES                   | double       | YES  |      | NULL    |       |
| STABLE_COUNT                              | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_ROWS                         | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE                         | bigint       | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE_ON_DISK                 | bigint       | YES  |      | NULL    |       |
| AVG_STABLE_ROWS                           | double       | YES  |      | NULL    |       |
| AVG_STABLE_SIZE                           | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_DELTA                 | bigint       | YES  |      | NULL    |       |
| MAX_PACK_COUNT_IN_DELTA                   | bigint       | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_DELTA                   | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_DELTA                    | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_DELTA                    | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_STABLE                | bigint       | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_STABLE                  | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_STABLE                   | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_STABLE                   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_NUM_SNAPSHOTS              | bigint       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID  | bigint       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID | varchar(128) | YES  |      | NULL    |       |
| STORAGE_DELTA_NUM_SNAPSHOTS               | bigint       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME    | double       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID   | bigint       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID  | varchar(128) | YES  |      | NULL    |       |
| STORAGE_META_NUM_SNAPSHOTS                | bigint       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_LIFETIME     | double       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID    | bigint       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID   | varchar(128) | YES  |      | NULL    |       |
| BACKGROUND_TASKS_LENGTH                   | bigint       | YES  |      | NULL    |       |
| TIFLASH_INSTANCE                          | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------------------+--------------+------+------+---------+-------+
```

`TIFLASH_TABLES`テーブル内のフィールドは次のように説明されます。

-   `TIDB_DATABASE` : TiDB 内でテーブルが属するデータベースの名前。
-   `TIDB_TABLE` : TiDB 内のテーブルの名前。
-   `TABLE_ID` : テーブルの内部 ID。TiDB クラスター内で一意です。
-   `IS_TOMBSTONE` : テーブルがリサイクル可能かどうかを示します。2 `1`テーブルがリサイクル可能であることを示し、 `0`テーブルが通常の状態であることを示します。
-   `SEGMENT_COUNT` : テーブル内のセグメント数。セグメントはTiFlashにおけるデータ管理単位です。
-   `TOTAL_ROWS` : テーブル内の行の合計数。
-   `TOTAL_SIZE` : テーブルの合計サイズ (バイト単位)。
-   `TOTAL_DELETE_RANGES` : テーブル内の削除範囲の合計数。
-   `DELTA_RATE_ROWS` : Deltaレイヤー内のテーブルの合計行数とそのテーブルの合計行数の比率。
-   `DELTA_RATE_SEGMENTS` : テーブル内の空でないデルタレイヤーを含むセグメントの割合。
-   `DELTA_PLACED_RATE` : デルタレイヤー内のテーブルのインデックス構築が完了した行の割合。
-   `DELTA_CACHE_SIZE` : Deltaレイヤー内のテーブルのキャッシュのサイズ (バイト単位)。
-   `DELTA_CACHE_RATE` : デルタレイヤー内のテーブルのキャッシュデータの割合。
-   `DELTA_CACHE_WASTED_RATE` : デルタレイヤー内のテーブルの無効なキャッシュデータの割合。
-   `DELTA_INDEX_SIZE` : Deltaレイヤー内のインデックスによって占有されるメモリのサイズ (バイト単位)。
-   `AVG_SEGMENT_ROWS` : テーブルのすべてのセグメント内の行の平均数。
-   `AVG_SEGMENT_SIZE` : テーブルのすべてのセグメントの平均サイズ (バイト単位)。
-   `DELTA_COUNT` : テーブル内の空でないデルタレイヤーを含むセグメントの数。
-   `TOTAL_DELTA_ROWS` : デルタレイヤー内の行の合計数。
-   `TOTAL_DELTA_SIZE` : Deltaレイヤーのデータの合計サイズ (バイト単位)。
-   `AVG_DELTA_ROWS` : すべての Delta レイヤー内のデータの平均行数。
-   `AVG_DELTA_SIZE` : すべての Delta レイヤーのデータの平均サイズ (バイト単位)。
-   `AVG_DELTA_DELETE_RANGES` : すべての Delta レイヤーにおける範囲削除操作の平均数。
-   `STABLE_COUNT` : テーブル内の空でない安定レイヤーを含むセグメントの数。
-   `TOTAL_STABLE_ROWS` : すべての安定レイヤーの行の合計数。
-   `TOTAL_STABLE_SIZE` : すべての安定レイヤーのデータの合計サイズ (バイト単位)。
-   `TOTAL_STABLE_SIZE_ON_DISK` : すべての安定レイヤーのデータが占めるディスク領域 (バイト単位)。
-   `AVG_STABLE_ROWS` : すべての安定レイヤー内のデータの平均行数。
-   `AVG_STABLE_SIZE` : すべての安定レイヤーのデータの平均サイズ (バイト単位)。
-   `TOTAL_PACK_COUNT_IN_DELTA` : すべての Delta レイヤー内のカラムファイルの合計数。
-   `MAX_PACK_COUNT_IN_DELTA` : 単一の Deltaレイヤー内のカラムファイルの最大数。
-   `AVG_PACK_COUNT_IN_DELTA` : すべてのデルタ レイヤー内のカラムファイルの平均数。
-   `AVG_PACK_ROWS_IN_DELTA` : すべてのデルタ レイヤー内のすべてのカラムファイル内の行の平均数。
-   `AVG_PACK_SIZE_IN_DELTA` : すべての Delta レイヤー内のすべてのカラムファイルのデータの平均サイズ (バイト単位)。
-   `TOTAL_PACK_COUNT_IN_STABLE` : すべての安定レイヤー内のパックの合計数。
-   `AVG_PACK_COUNT_IN_STABLE` : すべての安定レイヤー内のパックの平均数。
-   `AVG_PACK_ROWS_IN_STABLE` : すべての安定レイヤー内のすべてのパック内の行の平均数。
-   `AVG_PACK_SIZE_IN_STABLE` : 安定レイヤー内のすべてのパックのデータの平均サイズ (バイト単位)。
-   `STORAGE_STABLE_NUM_SNAPSHOTS` : 安定レイヤー内のスナップショットの数。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME` : 安定レイヤーの最も古いスナップショットの継続時間 (秒単位)。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID` : 安定レイヤーの最も古いスナップショットのスレッド ID。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID` : 安定レイヤー内の最も古いスナップショットのトレース ID。
-   `STORAGE_DELTA_NUM_SNAPSHOTS` : デルタレイヤー内のスナップショットの数。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME` : Deltaレイヤー内の最も古いスナップショットの期間 (秒単位)。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID` : デルタレイヤー内の最も古いスナップショットのスレッド ID。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID` : Deltaレイヤー内の最も古いスナップショットのトレース ID。
-   `STORAGE_META_NUM_SNAPSHOTS` : メタ情報内のスナップショットの数。
-   `STORAGE_META_OLDEST_SNAPSHOT_LIFETIME` : メタ情報内の最も古いスナップショットの継続時間 (秒単位)。
-   `STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID` : メタ情報内の最も古いスナップショットのスレッド ID。
-   `STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID` : メタ情報内の最も古いスナップショットのトレース ID。
-   `BACKGROUND_TASKS_LENGTH` : バックグラウンドのタスク キューの長さ。
-   `TIFLASH_INSTANCE` : TiFlashインスタンスのアドレス。
