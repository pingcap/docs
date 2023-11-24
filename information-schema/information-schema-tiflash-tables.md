---
title: TIFLASH_TABLES
summary: Learn the `TIFLASH_TABLES` information_schema table.
---

# TIFLASH_TABLES {#tiflash-tables}

> **警告：**
>
> このテーブルのフィールドは不安定であり、TiDB の新しいリリースでは予告なく変更される可能性があるため、このテーブルを本番環境では使用しないでください。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

`TIFLASH_TABLES`表は、 TiFlashのデータ テーブルに関する統計情報を提供します。

```sql
USE information_schema;
DESC tiflash_tables;
```

```sql
+-------------------------------------------+--------------+------+------+---------+-------+
| Field                                     | Type         | Null | Key  | Default | Extra |
+-------------------------------------------+--------------+------+------+---------+-------+
| DATABASE                                  | varchar(64)  | YES  |      | NULL    |       |
| TABLE                                     | varchar(64)  | YES  |      | NULL    |       |
| TIDB_DATABASE                             | varchar(64)  | YES  |      | NULL    |       |
| TIDB_TABLE                                | varchar(64)  | YES  |      | NULL    |       |
| TABLE_ID                                  | bigint(64)   | YES  |      | NULL    |       |
| IS_TOMBSTONE                              | bigint(64)   | YES  |      | NULL    |       |
| SEGMENT_COUNT                             | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_ROWS                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_SIZE                                | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELETE_RANGES                       | bigint(64)   | YES  |      | NULL    |       |
| DELTA_RATE_ROWS                           | double       | YES  |      | NULL    |       |
| DELTA_RATE_SEGMENTS                       | double       | YES  |      | NULL    |       |
| DELTA_PLACED_RATE                         | double       | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| DELTA_CACHE_RATE                          | double       | YES  |      | NULL    |       |
| DELTA_CACHE_WASTED_RATE                   | double       | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_SEGMENT_ROWS                          | double       | YES  |      | NULL    |       |
| AVG_SEGMENT_SIZE                          | double       | YES  |      | NULL    |       |
| DELTA_COUNT                               | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_ROWS                          | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_DELTA_SIZE                          | bigint(64)   | YES  |      | NULL    |       |
| AVG_DELTA_ROWS                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_SIZE                            | double       | YES  |      | NULL    |       |
| AVG_DELTA_DELETE_RANGES                   | double       | YES  |      | NULL    |       |
| STABLE_COUNT                              | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_ROWS                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE                         | bigint(64)   | YES  |      | NULL    |       |
| TOTAL_STABLE_SIZE_ON_DISK                 | bigint(64)   | YES  |      | NULL    |       |
| AVG_STABLE_ROWS                           | double       | YES  |      | NULL    |       |
| AVG_STABLE_SIZE                           | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_DELTA                 | bigint(64)   | YES  |      | NULL    |       |
| MAX_PACK_COUNT_IN_DELTA                   | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_DELTA                   | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_DELTA                    | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_DELTA                    | double       | YES  |      | NULL    |       |
| TOTAL_PACK_COUNT_IN_STABLE                | bigint(64)   | YES  |      | NULL    |       |
| AVG_PACK_COUNT_IN_STABLE                  | double       | YES  |      | NULL    |       |
| AVG_PACK_ROWS_IN_STABLE                   | double       | YES  |      | NULL    |       |
| AVG_PACK_SIZE_IN_STABLE                   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_NUM_SNAPSHOTS              | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME   | double       | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID  | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID | varchar(128) | YES  |      | NULL    |       |
| STORAGE_DELTA_NUM_SNAPSHOTS               | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME    | double       | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID   | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID  | varchar(128) | YES  |      | NULL    |       |
| STORAGE_META_NUM_SNAPSHOTS                | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_LIFETIME     | double       | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID    | bigint(64)   | YES  |      | NULL    |       |
| STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID   | varchar(128) | YES  |      | NULL    |       |
| BACKGROUND_TASKS_LENGTH                   | bigint(64)   | YES  |      | NULL    |       |
| TIFLASH_INSTANCE                          | varchar(64)  | YES  |      | NULL    |       |
+-------------------------------------------+--------------+------+------+---------+-------+
54 rows in set (0.00 sec)
```

`TIFLASH_TABLES`テーブルのフィールドは次のように説明されています。

-   `DATABASE` : TiFlashでテーブルが属するデータベースの名前。
-   `TABLE` : TiFlash内のテーブルの名前。
-   `TIDB_DATABASE` : TiDB 内でテーブルが属するデータベースの名前。
-   `TIDB_TABLE` : TiDB 内のテーブルの名前。
-   `TABLE_ID` : テーブルの内部 ID。TiDB クラスター内で一意です。
-   `IS_TOMBSTONE` : テーブルをリサイクルできるかどうかを示します。 `1`テーブルが再利用できることを示し、 `0`はテーブルが正常な状態であることを示します。
-   `SEGMENT_COUNT` : テーブル内のセグメントの数。セグメントは、 TiFlashにおけるデータ管理単位です。
-   `TOTAL_ROWS` : テーブル内の行の総数。
-   `TOTAL_SIZE` : テーブルの合計サイズ (バイト単位)。
-   `TOTAL_DELETE_RANGES` : テーブル内の削除範囲の総数。
-   `DELTA_RATE_ROWS` : デルタレイヤー内のテーブルの合計行数とそのテーブルの合計行数の比率。
-   `DELTA_RATE_SEGMENTS` : テーブル内に空ではないデルタレイヤーを含むセグメントの割合。
-   `DELTA_PLACED_RATE` : デルタレイヤー内のテーブルのインデックス構築が完了した行の割合。
-   `DELTA_CACHE_SIZE` : デルタレイヤーのテーブルのキャッシュのサイズ (バイト単位)。
-   `DELTA_CACHE_RATE` : デルタレイヤー内のテーブルのキャッシュ データの割合。
-   `DELTA_CACHE_WASTED_RATE` : デルタレイヤー内のテーブルの無効なキャッシュ データの割合。
-   `DELTA_INDEX_SIZE` : デルタレイヤーのインデックスが占有するメモリのサイズ (バイト単位)。
-   `AVG_SEGMENT_ROWS` : テーブルのすべてのセグメントの平均行数。
-   `AVG_SEGMENT_SIZE` : テーブルのすべてのセグメントの平均サイズ (バイト単位)。
-   `DELTA_COUNT` : テーブル内に空ではないデルタレイヤーを含むセグメントの数。
-   `TOTAL_DELTA_ROWS` : デルタレイヤーの総行数。
-   `TOTAL_DELTA_SIZE` : デルタレイヤーのデータの合計サイズ (バイト単位)。
-   `AVG_DELTA_ROWS` : すべてのデルタ レイヤー内のデータの平均行数。
-   `AVG_DELTA_SIZE` : すべてのデルタ レイヤーのデータの平均サイズ (バイト単位)。
-   `AVG_DELTA_DELETE_RANGES` : すべてのデルタ レイヤーにおける範囲削除操作の平均数。
-   `STABLE_COUNT` : テーブル内に空ではない安定レイヤーを含むセグメントの数。
-   `TOTAL_STABLE_ROWS` : すべての安定層の行の合計数。
-   `TOTAL_STABLE_SIZE` : すべての安定層のデータの合計サイズ (バイト単位)。
-   `TOTAL_STABLE_SIZE_ON_DISK` : すべての安定層のデータが占めるディスク容量 (バイト単位)。
-   `AVG_STABLE_ROWS` : すべての安定層のデータの平均行数。
-   `AVG_STABLE_SIZE` : すべての安定層のデータの平均サイズ (バイト単位)。
-   `TOTAL_PACK_COUNT_IN_DELTA` : すべてのデルタ レイヤー内のカラムファイルの合計数。
-   `MAX_PACK_COUNT_IN_DELTA` : 単一デルタレイヤー内のカラムファイルの最大数。
-   `AVG_PACK_COUNT_IN_DELTA` : すべてのデルタ レイヤー内のカラムファイルの平均数。
-   `AVG_PACK_ROWS_IN_DELTA` : すべてのカラムレイヤーのすべての列ファイルの平均行数。
-   `AVG_PACK_SIZE_IN_DELTA` : すべてのカラムレイヤーのすべての列ファイルのデータの平均サイズ (バイト単位)。
-   `TOTAL_PACK_COUNT_IN_STABLE` : すべての安定層のパックの合計数。
-   `AVG_PACK_COUNT_IN_STABLE` : すべての安定層のパックの平均数。
-   `AVG_PACK_ROWS_IN_STABLE` : すべての安定層のすべてのパックの平均行数。
-   `AVG_PACK_SIZE_IN_STABLE` : 安定レイヤーのすべてのパックのデータの平均サイズ (バイト単位)。
-   `STORAGE_STABLE_NUM_SNAPSHOTS` : 安定レイヤーのスナップショットの数。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_LIFETIME` : 安定レイヤー内の最も古いスナップショットの継続時間 (秒単位)。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_THREAD_ID` : 安定レイヤー内の最も古いスナップショットのスレッド ID。
-   `STORAGE_STABLE_OLDEST_SNAPSHOT_TRACING_ID` : 安定レイヤー内の最も古いスナップショットのトレース ID。
-   `STORAGE_DELTA_NUM_SNAPSHOTS` : デルタレイヤーのスナップショットの数。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_LIFETIME` : デルタレイヤーの最も古いスナップショットの継続時間 (秒単位)。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_THREAD_ID` : デルタレイヤーの最も古いスナップショットのスレッド ID。
-   `STORAGE_DELTA_OLDEST_SNAPSHOT_TRACING_ID` : デルタレイヤーの最も古いスナップショットのトレース ID。
-   `STORAGE_META_NUM_SNAPSHOTS` : メタ情報のスナップショット数。
-   `STORAGE_META_OLDEST_SNAPSHOT_LIFETIME` : メタ情報内の最も古いスナップショットの継続時間 (秒単位)。
-   `STORAGE_META_OLDEST_SNAPSHOT_THREAD_ID` : メタ情報内の最も古いスナップショットのスレッド ID。
-   `STORAGE_META_OLDEST_SNAPSHOT_TRACING_ID` : メタ情報内の最も古いスナップショットのトレース ID。
-   `BACKGROUND_TASKS_LENGTH` : バックグラウンドのタスクキューの長さ。
-   `TIFLASH_INSTANCE` : TiFlashインスタンスのアドレス。
