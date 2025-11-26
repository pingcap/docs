---
title: TIFLASH_SEGMENTS
summary: TIFLASH_SEGMENTS` information_schema テーブルについて学習します。
---

# TIFLASH_セグメント {#tiflash-segments}

> **警告：**
>
> このテーブルは不安定であり、TiDB の新しいリリースで予告なく変更される可能性があるため、本番環境では使用しないでください。

`TIFLASH_SEGMENTS`テーブルは、 TiFlashのデータ テーブル内のセグメントに関する統計情報を提供します。

```sql
USE information_schema;
DESC tiflash_segments;
```

```sql
+-------------------------------+-------------+------+------+---------+-------+
| Field                         | Type        | Null | Key  | Default | Extra |
+-------------------------------+-------------+------+------+---------+-------+
| TIDB_DATABASE                 | varchar(64) | YES  |      | NULL    |       |
| TIDB_TABLE                    | varchar(64) | YES  |      | NULL    |       |
| TABLE_ID                      | bigint      | YES  |      | NULL    |       |
| IS_TOMBSTONE                  | bigint      | YES  |      | NULL    |       |
| SEGMENT_ID                    | bigint      | YES  |      | NULL    |       |
| RANGE                         | varchar(64) | YES  |      | NULL    |       |
| EPOCH                         | bigint      | YES  |      | NULL    |       |
| ROWS                          | bigint      | YES  |      | NULL    |       |
| SIZE                          | bigint      | YES  |      | NULL    |       |
| DELTA_RATE                    | double      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_ROWS           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_SIZE           | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_COLUMN_FILES   | bigint      | YES  |      | NULL    |       |
| DELTA_MEMTABLE_DELETE_RANGES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_PAGE_ID       | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_ROWS          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_SIZE          | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_COLUMN_FILES  | bigint      | YES  |      | NULL    |       |
| DELTA_PERSISTED_DELETE_RANGES | bigint      | YES  |      | NULL    |       |
| DELTA_CACHE_SIZE              | bigint      | YES  |      | NULL    |       |
| DELTA_INDEX_SIZE              | bigint      | YES  |      | NULL    |       |
| STABLE_PAGE_ID                | bigint      | YES  |      | NULL    |       |
| STABLE_ROWS                   | bigint      | YES  |      | NULL    |       |
| STABLE_SIZE                   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES                | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ID_0           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_ROWS           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE           | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_SIZE_ON_DISK   | bigint      | YES  |      | NULL    |       |
| STABLE_DMFILES_PACKS          | bigint      | YES  |      | NULL    |       |
| TIFLASH_INSTANCE              | varchar(64) | YES  |      | NULL    |       |
+-------------------------------+-------------+------+------+---------+-------+
```

`TIFLASH_SEGMENTS`テーブル内のフィールドは次のように説明されます。

-   `TIDB_DATABASE` : TiDB内のデータベース名。セグメントはこのデータベース内のテーブルに属します。
-   `TIDB_TABLE` : TiDB内のテーブル名。セグメントはこのテーブルに属します。
-   `TABLE_ID` : セグメントが属するテーブルの内部ID。このIDはTiDBクラスタ内で一意です。
-   `IS_TOMBSTONE` : セグメントが属するテーブルがリサイクル可能かどうかを示します。2 `1`テーブルがリサイクル可能であることを示します。4 `0`テーブルが通常の状態であることを示します。
-   `SEGMENT_ID` : テーブル内で一意のセグメント ID。
-   `RANGE` : セグメントに含まれるデータの範囲。
-   `EPOCH` : セグメントの更新バージョン。各セグメントのバージョン番号は単調に増加します。
-   `ROWS` : セグメント内の行の合計数。
-   `SIZE` : セグメント データの合計サイズ (バイト単位)。
-   `DELTA_RATE` : デルタレイヤーの合計行数とセグメントの合計行数の比率。
-   `DELTA_MEMTABLE_ROWS` : デルタレイヤーにキャッシュされた行の合計数。
-   `DELTA_MEMTABLE_SIZE` : Deltaレイヤーにキャッシュされたデータの合計サイズ (バイト単位)。
-   `DELTA_MEMTABLE_COLUMN_FILES` : デルタレイヤーにキャッシュされたカラムファイルの数。
-   `DELTA_MEMTABLE_DELETE_RANGES` : デルタレイヤーにキャッシュされた削除範囲の数。
-   `DELTA_PERSISTED_PAGE_ID` : デルタレイヤーのディスクに保存されているデータの ID。
-   `DELTA_PERSISTED_ROWS` : デルタレイヤーに保存されたデータの行の合計数。
-   `DELTA_PERSISTED_SIZE` : Deltaレイヤーに保存されたデータの合計サイズ (バイト単位)。
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
