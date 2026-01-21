---
title: TABLES
summary: TABLES` information_schema テーブルについて学習します。
---

# テーブル {#tables}

`TABLES`テーブルは、データベース内のテーブルに関する情報を提供します。

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
| TIDB_PK_TYPE              | varchar(64)   | YES  |      | NULL     |       |
| TIDB_PLACEMENT_POLICY_NAME | varchar(64)  | YES  |      | NULL     |       |
| TIDB_TABLE_MODE           | varchar(16)   | YES  |      | NULL     |       |
| TIDB_AFFINITY             | varchar(128)  | YES  |      | NULL     |       |
+---------------------------+---------------+------+------+----------+-------+
27 rows in set (0.00 sec)
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
             TIDB_PK_TYPE: CLUSTERED
TIDB_PLACEMENT_POLICY_NAME: NULL
           TIDB_TABLE_MODE: Normal
             TIDB_AFFINITY: NULL
1 row in set (0.00 sec)
```

次の文は同等です。

```sql
SELECT table_name FROM INFORMATION_SCHEMA.TABLES
  WHERE table_schema = 'db_name'
  [AND table_name LIKE 'wild']

SHOW TABLES
  FROM db_name
  [LIKE 'wild']
```

`TABLES`テーブル内の列の説明は次のとおりです。

-   `TABLE_CATALOG` : テーブルが属するカタログの名前。値は常に`def`です。
-   `TABLE_SCHEMA` : テーブルが属するスキーマの名前。
-   `TABLE_NAME` : テーブルの名前。
-   `TABLE_TYPE` : テーブルのタイプ。
-   `ENGINE` :storageエンジンの種類。現在の値は`InnoDB`です。
-   `VERSION` : バージョン。デフォルトの値は`10`です。
-   `ROW_FORMAT` : 行形式。現在の値は`Compact`です。
-   `TABLE_ROWS` : 統計におけるテーブル内の行数。
-   `AVG_ROW_LENGTH` : 表の平均行の長さ`AVG_ROW_LENGTH` = `DATA_LENGTH` / `TABLE_ROWS` 。
-   `DATA_LENGTH` : データ長。2 = `DATA_LENGTH` * タプル内の列`TABLE_ROWS`storage長の合計。TiKVのレプリカは考慮されません。
-   `MAX_DATA_LENGTH` : 最大データ長。現在の値は`0` 、データ長に上限がないことを意味します。
-   `INDEX_LENGTH` : インデックスの長さ`INDEX_LENGTH` = `TABLE_ROWS` * インデックスタプル内の列の長さの合計。TiKVのレプリカは考慮されません。
-   `DATA_FREE` : データフラグメント。現在の値は`0`です。
-   `AUTO_INCREMENT` : 自動インクリメント主キーの現在のステップ。
-   `CREATE_TIME` : テーブルが作成された時刻。
-   `UPDATE_TIME` : テーブルが更新される時刻。
-   `CHECK_TIME` : テーブルがチェックされる時刻。
-   `TABLE_COLLATION` : テーブル内の文字列の照合順序。
-   `CHECKSUM` : チェックサム。
-   `CREATE_OPTIONS` : オプションを作成します。
-   `TABLE_COMMENT` : 表のコメントとメモ。

テーブル内の情報の大部分はMySQLと同じです。以下の列はTiDBによって新たに定義されています。

-   `TIDB_TABLE_ID` : テーブルの内部IDを示します。このIDはTiDBクラスタ内で一意です。
-   `TIDB_ROW_ID_SHARDING_INFO` : テーブルのシャーディングタイプを示します。可能な値は次のとおりです。
    -   `"NOT_SHARDED"` : テーブルはシャード化されていません。
    -   `"NOT_SHARDED(PK_IS_HANDLE)"` : 行 ID として整数の主キーを定義するテーブルはシャード化されません。
    -   `"PK_AUTO_RANDOM_BITS={bit_number}"` : 整数の主キーを行 ID として定義するテーブルは、主キーに`AUTO_RANDOM`属性が割り当てられているため、シャードされます。
    -   `"SHARD_BITS={bit_number}"` : テーブルは`SHARD_ROW_ID_BITS={bit_number}`を使用して分割されます。
    -   `NULL` : テーブルはシステム テーブルまたはビューであるため、シャード化できません。
-   `TIDB_PK_TYPE` : テーブルの主キーの種類。可能な値は`CLUSTERED` (クラスター化主キー) と`NONCLUSTERED` (非クラスター化主キー) です。
-   `TIDB_PLACEMENT_POLICY_NAME` : テーブルに適用された配置ポリシーの名前。
-   `TIDB_TABLE_MODE` : テーブルのモード。たとえば、 `Normal` 、 `Import` 、 `Restore` 。
-   `TIDB_AFFINITY` : テーブルのアフィニティレベル。パーティション化されていないテーブルの場合は`table` 、パーティション化されたテーブルの場合は`partition` 、アフィニティが有効化されていない場合は`NULL`なります。
