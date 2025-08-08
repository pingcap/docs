---
title: TIFLASH_SEGMENTS
summary: TIFLASH_SEGMENTS` information_schema テーブルについて学習します。
---

# TIFLASH_SEGMENTS {#tiflash-segments}

> **警告：**
>
> このテーブルは不安定であり、TiDB の新しいリリースで予告なく変更される可能性があるため、本番環境では使用しないでください。

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

`TIFLASH_SEGMENTS`テーブル内のフィールドは次のように説明されます。

-   `DATABASE` : TiFlash内のデータベース名。セグメントはこのデータベース内のテーブルに属します。
-   `TABLE` : TiFlash内のテーブル名。セグメントはこのテーブルに属します。
-   `TIDB_DATABASE` : TiDB内のデータベース名。セグメントはこのデータベース内のテーブルに属します。
-   `TIDB_TABLE` : TiDB内のテーブル名。セグメントはこのテーブルに属します。
-   `TABLE_ID` : セグメントが属するテーブルの内部ID。このIDはTiDBクラスタ内で一意です。
-   `IS_TOMBSTONE` : セグメントが属するテーブルがリサイクル可能かどうかを示します。2 `1`テーブルがリサイクル可能であることを示します。4 `0`テーブルが通常の状態であることを示します。
-   `SEGMENT_ID` : テーブル内で一意のセグメント ID。
-   `RANGE` : セグメントに含まれるデータの範囲。
-   `EPOCH` ：セグメントの更新バージョン。各セグメントのバージョン番号は単調に増加します。
-   `ROWS` : セグメント内の行の合計数。
-   `SIZE` : セグメント データの合計サイズ (バイト単位)。
-   `DELTA_RATE` : デルタレイヤーの合計行数とセグメントの合計行数の比率。
-   `DELTA_MEMTABLE_ROWS` : デルタレイヤーにキャッシュされた行の合計数。
-   `DELTA_MEMTABLE_SIZE` : Deltaレイヤーにキャッシュされたデータの合計サイズ (バイト単位)。
-   `DELTA_MEMTABLE_COLUMN_FILES` : デルタレイヤーにキャッシュされるカラムファイルの数。
-   `DELTA_MEMTABLE_DELETE_RANGES` : デルタレイヤーにキャッシュされた削除範囲の数。
-   `DELTA_PERSISTED_PAGE_ID` : デルタレイヤーのディスクに保存されているデータの ID。
-   `DELTA_PERSISTED_ROWS` : デルタレイヤーに保存されたデータの行の総数。
-   `DELTA_PERSISTED_SIZE` : Deltaレイヤーに保存されるデータの合計サイズ (バイト単位)。
-   `DELTA_PERSISTED_COLUMN_FILES` : デルタレイヤー内の永続化されたカラムファイルの数。
-   `DELTA_PERSISTED_DELETE_RANGES` : デルタレイヤーに保持される削除範囲の数。
-   `DELTA_CACHE_SIZE` : Deltaレイヤーのキャッシュのサイズ (バイト単位)。
-   `DELTA_INDEX_SIZE` : Deltaレイヤー内のインデックスのサイズ (バイト単位)。
-   `STABLE_PAGE_ID` : 安定レイヤーのデータのディスクstorageID。
-   `STABLE_ROWS` : 安定レイヤー内の行の合計数。
-   `STABLE_SIZE` : 安定レイヤーのデータの合計サイズ (バイト単位)。
-   `STABLE_DMFILES` : 安定レイヤー内の DMFiles の数。
-   `STABLE_DMFILES_ID_0` : 安定レイヤーの最初の DMFile のディスクstorageID。
-   `STABLE_DMFILES_ROWS` : 安定レイヤーの DMFile 内の行の合計数。
-   `STABLE_DMFILES_SIZE` : 安定レイヤーの DMFile 内のデータの合計サイズ (バイト単位)。
-   `STABLE_DMFILES_SIZE_ON_DISK` : 安定レイヤーで DMFile が占めるディスク領域 (バイト単位)。
-   `STABLE_DMFILES_PACKS` : 安定レイヤーの DMFile 内のパックの数。
-   `TIFLASH_INSTANCE` : TiFlashインスタンスのアドレス。
