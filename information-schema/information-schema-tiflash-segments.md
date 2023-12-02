---
title: TIFLASH_SEGMENTS
summary: Learn the `TIFLASH_SEGMENTS` information_schema table.
---

# TIFLASH_SEGMENTS {#tiflash-segments}

> **警告：**
>
> このテーブルのフィールドは不安定であり、TiDB の新しいリリースでは予告なく変更される可能性があるため、このテーブルを本番環境では使用しないでください。

> **注記：**
>
> このテーブルは[TiDB サーバーレス](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless)クラスターでは使用できません。

`TIFLASH_SEGMENTS`表は、 TiFlashのデータ テーブルに関する統計情報を提供します。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| DATABASE                      | varchar(64) | YES  |      | NULL    |       |
| TABLE                         | varchar(64) | YES  |      | NULL    |       |
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint(64)  | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint(64)  | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint(64)  | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint(64)  | YES  |      | NULL    |       |
| ROWS                          | bigint(64)  | YES  |      | NULL    |       |
| SIZE                          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint(64)  | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint(64)  | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint(64)  | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint(64)  | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint(64)  | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint(64)  | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
33 rows in set (0.00 sec)
```

`TIFLASH_SEGMENTS`テーブルのフィールドは次のように説明されています。

-   `DATABASE` : TiFlashのデータベース名。セグメントはこのデータベース内のテーブルに属しています。
-   `TABLE` : TiFlashのテーブル名。セグメントはこのテーブルに属します。
-   `TIDB_DATABASE` : TiDB 内のデータベース名。セグメントはこのデータベース内のテーブルに属しています。
-   `TIDB_TABLE` : TiDB 内のテーブル名。セグメントはこのテーブルに属します。
-   `TABLE_ID` : セグメントが属するテーブルの内部 ID。この ID は TiDB クラスター内で一意です。
-   `IS_TOMBSTONE` : セグメントが属するテーブルがリサイクル可能かどうかを示します。 `1` 、テーブルをリサイクルできることを示します。 `0`テーブルが正常な状態であることを示します。
-   `SEGMENT_ID` : テーブル内で一意のセグメント ID。
-   `RANGE` : セグメントに含まれるデータの範囲。
-   `EPOCH` : セグメントの更新されたバージョン。各セグメントのバージョン番号は単調増加します。
-   `ROWS` : セグメント内の行の総数。
-   `SIZE` : セグメントデータの合計サイズ(バイト単位)。
-   `DELTA_RATE` : デルタレイヤーの合計行数とセグメント内の行数の比率。
-   `DELTA_MEMTABLE_ROWS` : デルタレイヤー内のキャッシュされた行の総数。
-   `DELTA_MEMTABLE_SIZE` : デルタレイヤーにキャッシュされたデータの合計サイズ (バイト単位)。
-   `DELTA_MEMTABLE_COLUMN_FILES` : デルタレイヤーにキャッシュされたカラムファイルの数。
-   `DELTA_MEMTABLE_DELETE_RANGES` : デルタレイヤーにキャッシュされた削除範囲の数。
-   `DELTA_PERSISTED_PAGE_ID` : デルタレイヤーのディスクに保存されているデータの ID。
-   `DELTA_PERSISTED_ROWS` : デルタレイヤー内の永続化データの総行数。
-   `DELTA_PERSISTED_SIZE` : デルタレイヤー内の永続化データの合計サイズ (バイト単位)。
-   `DELTA_PERSISTED_COLUMN_FILES` : デルタレイヤーに保持されるカラムファイルの数。
-   `DELTA_PERSISTED_DELETE_RANGES` : デルタレイヤー内に保持される削除範囲の数。
-   `DELTA_CACHE_SIZE` : デルタレイヤーのキャッシュのサイズ (バイト単位)。
-   `DELTA_INDEX_SIZE` : デルタレイヤーのインデックスのサイズ (バイト単位)。
-   `STABLE_PAGE_ID` : 安定レイヤーのデータのディスクstorageID。
-   `STABLE_ROWS` : 安定レイヤーの行の総数。
-   `STABLE_SIZE` : Stableレイヤーのデータの合計サイズ (バイト単位)。
-   `STABLE_DMFILES` : Stableレイヤー内の DMFile の数。
-   `STABLE_DMFILES_ID_0` : 安定レイヤーの最初の DMFile のディスクstorageID。
-   `STABLE_DMFILES_ROWS` : Stableレイヤーの DMFile 内の行の合計数。
-   `STABLE_DMFILES_SIZE` : Stableレイヤーの DMFile 内のデータの合計サイズ (バイト単位)。
-   `STABLE_DMFILES_SIZE_ON_DISK` : 安定レイヤーの DMFile が占めるディスク容量 (バイト単位)。
-   `STABLE_DMFILES_PACKS` : Stableレイヤーの DMFile 内のパックの数。
-   `TIFLASH_INSTANCE` : TiFlashインスタンスのアドレス。
