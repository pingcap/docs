---
title: TABLES
summary: テーブル表は、データベース内のテーブルに関する情報を提供します。テーブル内の列の説明は、テーブルが属するカタログの名前、テーブルが属するスキーマの名前、テーブルの名前、テーブルのタイプ、storageエンジンのタイプ、バージョン、行フォーマット、統計におけるテーブルの行数、テーブルの平均行長、データ長、最大データ長、インデックスの長さ、データフラグメント、自動インクリメント主キーの現在のステップ、テーブルが作成された時刻、テーブルが更新された時刻、テーブルがチェックされた時刻、テーブル内の文字列の照合順序、チェックサム、オプションを作成します、テーブルのコメントとメモ、テーブルの内部 ID、テーブルのシャーディング タイプです。
---

# テーブル {#tables}

`TABLES`表は、データベース内のテーブルに関する情報を提供します。

```sql
USE information_schema;
DESC tables;
```

```sql
+---------------------------+---------------+------+------+----------+-------+
| Field                     | Type          | Null | Key  | Default  | Extra |
+---------------------------+---------------+------+------+----------+-------+
| TABLE_CATALOG             | varchar(512)  | YES  |      | NULL     |       |
| TABLE_SCHEMA              | varchar(64)   | YES  |      | NULL     |       |
| TABLE_NAME                | varchar(64)   | YES  |      | NULL     |       |
| TABLE_TYPE                | varchar(64)   | YES  |      | NULL     |       |
| ENGINE                    | varchar(64)   | YES  |      | NULL     |       |
| VERSION                   | bigint(21)    | YES  |      | NULL     |       |
| ROW_FORMAT                | varchar(10)   | YES  |      | NULL     |       |
| TABLE_ROWS                | bigint(21)    | YES  |      | NULL     |       |
| AVG_ROW_LENGTH            | bigint(21)    | YES  |      | NULL     |       |
| DATA_LENGTH               | bigint(21)    | YES  |      | NULL     |       |
| MAX_DATA_LENGTH           | bigint(21)    | YES  |      | NULL     |       |
| INDEX_LENGTH              | bigint(21)    | YES  |      | NULL     |       |
| DATA_FREE                 | bigint(21)    | YES  |      | NULL     |       |
| AUTO_INCREMENT            | bigint(21)    | YES  |      | NULL     |       |
| CREATE_TIME               | datetime      | YES  |      | NULL     |       |
| UPDATE_TIME               | datetime      | YES  |      | NULL     |       |
| CHECK_TIME                | datetime      | YES  |      | NULL     |       |
| TABLE_COLLATION           | varchar(32)   | NO   |      | utf8_bin |       |
| CHECKSUM                  | bigint(21)    | YES  |      | NULL     |       |
| CREATE_OPTIONS            | varchar(255)  | YES  |      | NULL     |       |
| TABLE_COMMENT             | varchar(2048) | YES  |      | NULL     |       |
| TIDB_TABLE_ID             | bigint(21)    | YES  |      | NULL     |       |
| TIDB_ROW_ID_SHARDING_INFO | varchar(255)  | YES  |      | NULL     |       |
+---------------------------+---------------+------+------+----------+-------+
23 rows in set (0.00 sec)
```

```sql
SELECT * FROM tables WHERE table_schema='mysql' AND table_name='user'\G
```

```sql
*************************** 1. row ***************************
            TABLE_CATALOG: def
             TABLE_SCHEMA: mysql
               TABLE_NAME: user
               TABLE_TYPE: BASE TABLE
                   ENGINE: InnoDB
                  VERSION: 10
               ROW_FORMAT: Compact
               TABLE_ROWS: 0
           AVG_ROW_LENGTH: 0
              DATA_LENGTH: 0
          MAX_DATA_LENGTH: 0
             INDEX_LENGTH: 0
                DATA_FREE: 0
           AUTO_INCREMENT: NULL
              CREATE_TIME: 2020-07-05 09:25:51
              UPDATE_TIME: NULL
               CHECK_TIME: NULL
          TABLE_COLLATION: utf8mb4_bin
                 CHECKSUM: NULL
           CREATE_OPTIONS: 
            TABLE_COMMENT: 
            TIDB_TABLE_ID: 5
TIDB_ROW_ID_SHARDING_INFO: NULL
1 row in set (0.00 sec)
```

次のステートメントは同等です。

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES`のテーブルの列の説明は次のとおりです。

-   `TABLE_CATALOG` : テーブルが属するカタログの名前。値は常に`def`です。
-   `TABLE_SCHEMA` : テーブルが属するスキーマの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `TABLE_TYPE` : テーブルのタイプ。
-   `ENGINE` :storageエンジンのタイプ。現在の値は`InnoDB`です。
-   `VERSION` : バージョン。デフォルトの値は`10`です。
-   `ROW_FORMAT` : 行フォーマット。現在の値は`Compact`です。
-   `TABLE_ROWS` : 統計におけるテーブルの行数。
-   `AVG_ROW_LENGTH` : テーブルの平均行長。 `AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS` 。
-   `DATA_LENGTH` : データ長。 `DATA_LENGTH` = `TABLE_ROWS` * タプル内の列のstorage域長の合計。 TiKV のレプリカは考慮されません。
-   `MAX_DATA_LENGTH` : 最大データ長。現在の値は`0`で、データ長に上限がないことを意味します。
-   `INDEX_LENGTH` : インデックスの長さ。 `INDEX_LENGTH` = `TABLE_ROWS` * インデックス タプル内の列の長さの合計。 TiKV のレプリカは考慮されません。
-   `DATA_FREE` : データフラグメント。現在の値は`0`です。
-   `AUTO_INCREMENT` : 自動インクリメント主キーの現在のステップ。
-   `CREATE_TIME` : テーブルが作成された時刻。
-   `UPDATE_TIME` : テーブルが更新された時刻。
-   `CHECK_TIME` : テーブルがチェックされた時刻。
-   `TABLE_COLLATION` : テーブル内の文字列の照合順序。
-   `CHECKSUM` : チェックサム。
-   `CREATE_OPTIONS` : オプションを作成します。
-   `TABLE_COMMENT` : テーブルのコメントとメモ。

テーブル内のほとんどの情報は MySQL と同じです。 TiDB によって新たに定義された列は 2 つだけです。

-   `TIDB_TABLE_ID` : テーブルの内部 ID を示します。この ID は TiDB クラスター内で一意です。
-   `TIDB_ROW_ID_SHARDING_INFO` : テーブルのシャーディング タイプを示します。可能な値は次のとおりです。
    -   `"NOT_SHARDED"` : テーブルはシャード化されていません。
    -   `"NOT_SHARDED(PK_IS_HANDLE)"` : 整数の主キーを行 ID として定義するテーブルはシャード化されません。
    -   `"PK_AUTO_RANDOM_BITS={bit_number}"` : 主キーには`AUTO_RANDOM`属性が割り当てられているため、整数の主キーを行 ID として定義するテーブルはシャーディングされます。
    -   `"SHARD_BITS={bit_number}"` : テーブルは`SHARD_ROW_ID_BITS={bit_number}`を使用してシャード化されます。
    -   NULL: テーブルはシステム テーブルまたはビューであるため、シャーディングできません。
