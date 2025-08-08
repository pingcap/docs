---
title: COLUMNS
summary: COLUMNS` INFORMATION_SCHEMA テーブルについて学習します。
---

# コラム {#columns}

`COLUMNS`表には、表内の列に関する詳細情報が示されています。

```sql
USE INFORMATION_SCHEMA;
DESC COLUMNS;
```

出力は次のようになります。

```sql
+--------------------------+---------------+------+------+---------+-------+
| Field                    | Type          | Null | Key  | Default | Extra |
+--------------------------+---------------+------+------+---------+-------+
| TABLE_CATALOG            | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA             | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64)   | YES  |      | NULL    |       |
| COLUMN_NAME              | varchar(64)   | YES  |      | NULL    |       |
| ORDINAL_POSITION         | bigint(64)    | YES  |      | NULL    |       |
| COLUMN_DEFAULT           | text          | YES  |      | NULL    |       |
| IS_NULLABLE              | varchar(3)    | YES  |      | NULL    |       |
| DATA_TYPE                | varchar(64)   | YES  |      | NULL    |       |
| CHARACTER_MAXIMUM_LENGTH | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_OCTET_LENGTH   | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_PRECISION        | bigint(21)    | YES  |      | NULL    |       |
| NUMERIC_SCALE            | bigint(21)    | YES  |      | NULL    |       |
| DATETIME_PRECISION       | bigint(21)    | YES  |      | NULL    |       |
| CHARACTER_SET_NAME       | varchar(32)   | YES  |      | NULL    |       |
| COLLATION_NAME           | varchar(32)   | YES  |      | NULL    |       |
| COLUMN_TYPE              | text          | YES  |      | NULL    |       |
| COLUMN_KEY               | varchar(3)    | YES  |      | NULL    |       |
| EXTRA                    | varchar(30)   | YES  |      | NULL    |       |
| PRIVILEGES               | varchar(80)   | YES  |      | NULL    |       |
| COLUMN_COMMENT           | varchar(1024) | YES  |      | NULL    |       |
| GENERATION_EXPRESSION    | text          | NO   |      | NULL    |       |
+--------------------------+---------------+------+------+---------+-------+
21 rows in set (0.00 sec)
```

テーブル`test.t1`を作成し、テーブル`COLUMNS`の情報を照会します。

```sql
CREATE TABLE test.t1 (a int);
SELECT * FROM COLUMNS WHERE table_schema='test' AND TABLE_NAME='t1'\G
```

出力は次のようになります。

```sql
*************************** 1. row ***************************
           TABLE_CATALOG: def
            TABLE_SCHEMA: test
              TABLE_NAME: t1
             COLUMN_NAME: a
        ORDINAL_POSITION: 1
          COLUMN_DEFAULT: NULL
             IS_NULLABLE: YES
               DATA_TYPE: int
CHARACTER_MAXIMUM_LENGTH: NULL
  CHARACTER_OCTET_LENGTH: NULL
       NUMERIC_PRECISION: 11
           NUMERIC_SCALE: 0
      DATETIME_PRECISION: NULL
      CHARACTER_SET_NAME: NULL
          COLLATION_NAME: NULL
             COLUMN_TYPE: int(11)
              COLUMN_KEY:
                   EXTRA:
              PRIVILEGES: select,insert,update,references
          COLUMN_COMMENT:
   GENERATION_EXPRESSION:
1 row in set (0.02 sec)
```

`COLUMNS`表の列の説明は次のとおりです。

-   `TABLE_CATALOG` : 列を含むテーブルが属するカタログの名前。値は常に`def` 。
-   `TABLE_SCHEMA` : 列を含むテーブルが配置されているスキーマの名前。
-   `TABLE_NAME` : 列を含むテーブルの名前。
-   `COLUMN_NAME` : 列の名前。
-   `ORDINAL_POSITION` : テーブル内の列の位置。
-   `COLUMN_DEFAULT` : 列のデフォルト値。明示的なデフォルト値が`NULL`の場合、または列定義に`default`句が含まれていない場合、この値は`NULL`なります。
-   `IS_NULLABLE` : 列がNULL値可能かどうか。列がNULL値を格納できる場合、この値は`YES` 、そうでない場合は`NO`なります。
-   `DATA_TYPE` : 列内のデータのタイプ。
-   `CHARACTER_MAXIMUM_LENGTH` : 文字列列の場合、文字の最大長。
-   `CHARACTER_OCTET_LENGTH` : 文字列列の場合、最大長（バイト単位）。
-   `NUMERIC_PRECISION` : 数値型列の数値精度。
-   `NUMERIC_SCALE` : 数値型列の数値スケール。
-   `DATETIME_PRECISION` : 時刻型列の場合、秒の小数部の精度。
-   `CHARACTER_SET_NAME` : 文字列列の文字セットの名前。
-   `COLLATION_NAME` : 文字列列の照合順序の名前。
-   `COLUMN_TYPE` : 列のタイプ。
-   `COLUMN_KEY` : この列がインデックスされているかどうか。このフィールドには次の値が含まれます。
    -   空: この列にはインデックスが付いていません。または、この列にはインデックスが付いていて、複数列の一意でないインデックスの 2 番目の列です。
    -   `PRI` : この列は主キーまたは複数の主キーの 1 つです。
    -   `UNI` : この列は、一意のインデックスの最初の列です。
    -   `MUL` : 列は、特定の値が複数回出現することを許可される、一意でないインデックスの最初の列です。
-   `EXTRA` : 指定された列の追加情報。
-   `PRIVILEGES` : 現在のユーザーがこの列に対して持つ権限。現在、この値はTiDBで固定されており、常に`select,insert,update,references`です。
-   `COLUMN_COMMENT` : 列定義に含まれるコメント。
-   `GENERATION_EXPRESSION` : 生成列の場合、この値は列の値を計算するために使用された式を表示します。非生成列の場合、この値は空です。

対応する`SHOW`ステートメントは次のとおりです。

```sql
SHOW COLUMNS FROM t1 FROM test;
```

出力は次のようになります。

```sql
+-------+---------+------+------+---------+-------+
| Field | Type    | Null | Key  | Default | Extra |
+-------+---------+------+------+---------+-------+
| a     | int(11) | YES  |      | NULL    |       |
+-------+---------+------+------+---------+-------+
1 row in set (0.00 sec)
```

## 参照 {#see-also}

-   [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md)
