---
title: TIFLASH_INDEXES
summary: INFORMATION_SCHEMA` の `TIFLASH_INDEXES` テーブルについて学習します。
---

# TIFLASH_INDEXES {#tiflash-indexes}

> **警告：**
>
> 現在、このテーブルは実験的です。本番環境での使用は推奨されません。このテーブルのフィールドはまだ安定しておらず、将来のTiDBバージョンで変更される可能性があります。バグを発見した場合は、GitHubで[問題](https://github.com/pingcap/tidb/issues)報告してください。

`TIFLASH_INDEXES`表は、 TiFlashレプリカ上のインデックス構築に関する統計を提供します。

```sql
USE INFORMATION_SCHEMA;
DESC TIFLASH_INDEXES;
```

出力は次のようになります。

```sql
+-------------------------+---------------+------+------+---------+-------+
| Field                   | Type          | Null | Key  | Default | Extra |
+-------------------------+---------------+------+------+---------+-------+
| TIDB_DATABASE           | varchar(64)   | YES  |      | NULL    |       |
| TIDB_TABLE              | varchar(64)   | YES  |      | NULL    |       |
| TABLE_ID                | bigint        | YES  |      | NULL    |       |
| COLUMN_NAME             | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME              | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_ID               | bigint        | YES  |      | NULL    |       |
| INDEX_ID                | bigint        | YES  |      | NULL    |       |
| INDEX_KIND              | varchar(64)   | YES  |      | NULL    |       |
| ROWS_STABLE_INDEXED     | bigint        | YES  |      | NULL    |       |
| ROWS_STABLE_NOT_INDEXED | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_INDEXED      | bigint        | YES  |      | NULL    |       |
| ROWS_DELTA_NOT_INDEXED  | bigint        | YES  |      | NULL    |       |
| ERROR_MESSAGE           | varchar(1024) | YES  |      | NULL    |       |
| TIFLASH_INSTANCE        | varchar(64)   | YES  |      | NULL    |       |
+-------------------------+---------------+------+------+---------+-------+
```

`TIFLASH_INDEXES`テーブル内のフィールドは次のように説明されます。

-   `TIDB_DATABASE` : テーブルが属するデータベースの名前。
-   `TIDB_TABLE` : テーブルの名前。
-   `TABLE_ID` : テーブルの内部 ID。TiDB クラスター内で一意です。
-   `COLUMN_NAME` : インデックスが構築される列の名前。
-   `INDEX_NAME` : インデックスの名前。
-   `COLUMN_ID` : インデックスが構築される列の ID。
-   `INDEX_ID` : インデックスの ID。
-   `INDEX_KIND` : インデックスのタイプ。
-   `ROWS_STABLE_INDEXED` : 安定レイヤーがインデックス構築を完了したTiFlashレプリカ内の行数。
-   `ROWS_STABLE_NOT_INDEXED` : 安定レイヤーがインデックス構築を完了していないTiFlashレプリカ内の行数。
-   `ROWS_DELTA_INDEXED` : Deltaレイヤーがインデックス構築を完了したTiFlashレプリカ内の行数。
-   `ROWS_DELTA_NOT_INDEXED` : Deltaレイヤーがインデックス構築を完了していないTiFlashレプリカ内の行数。
-   `ERROR_MESSAGE` : インデックス構築中に発生した回復不能なエラーの詳細。
-   `TIFLASH_INSTANCE` : インデックス構築タスクを実行するTiFlashインスタンスのアドレス。
