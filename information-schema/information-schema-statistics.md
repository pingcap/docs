---
title: STATISTICS
summary: STATISTICS` information_schema テーブルについて学習します。
---

# 統計 {#statistics}

`STATISTICS`テーブルはテーブル インデックスに関する情報を提供します。

```sql
USE information_schema;
DESC statistics;
```

```sql
+---------------+---------------+------+------+---------+-------+
| Field         | Type          | Null | Key  | Default | Extra |
+---------------+---------------+------+------+---------+-------+
| TABLE_CATALOG | varchar(512)  | YES  |      | NULL    |       |
| TABLE_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| TABLE_NAME    | varchar(64)   | YES  |      | NULL    |       |
| NON_UNIQUE    | varchar(1)    | YES  |      | NULL    |       |
| INDEX_SCHEMA  | varchar(64)   | YES  |      | NULL    |       |
| INDEX_NAME    | varchar(64)   | YES  |      | NULL    |       |
| SEQ_IN_INDEX  | bigint(2)     | YES  |      | NULL    |       |
| COLUMN_NAME   | varchar(21)   | YES  |      | NULL    |       |
| COLLATION     | varchar(1)    | YES  |      | NULL    |       |
| CARDINALITY   | bigint(21)    | YES  |      | NULL    |       |
| SUB_PART      | bigint(3)     | YES  |      | NULL    |       |
| PACKED        | varchar(10)   | YES  |      | NULL    |       |
| NULLABLE      | varchar(3)    | YES  |      | NULL    |       |
| INDEX_TYPE    | varchar(16)   | YES  |      | NULL    |       |
| COMMENT       | varchar(16)   | YES  |      | NULL    |       |
| INDEX_COMMENT | varchar(1024) | YES  |      | NULL    |       |
| IS_VISIBLE    | varchar(3)    | YES  |      | NULL    |       |
| Expression    | varchar(64)   | YES  |      | NULL    |       |
+---------------+---------------+------+------+---------+-------+
18 rows in set (0.00 sec)
```

`STATISTICS`テーブル内のフィールドは次のように説明されます。

-   `TABLE_CATALOG` : インデックスを含むテーブルが属するカタログの名前。この値は常に`def` 。
-   `TABLE_SCHEMA` : インデックスを含むテーブルが属するデータベースの名前。
-   `TABLE_NAME` : インデックスを含むテーブルの名前。
-   `NON_UNIQUE` : インデックスに重複する値を含めることができない場合、値は`0`になります。インデックスで重複する値が許可される場合は、値は`1`なります。
-   `INDEX_SCHEMA` : インデックスが属するデータベースの名前。
-   `INDEX_NAME` : インデックスの名前。インデックスが主キーの場合、値は常に`PRIMARY`なります。
-   `SEQ_IN_INDEX` : インデックス内の列番号`1`から始まります。
-   `COLUMN_NAME` : 列名。2列`Expression`の説明を参照してください。
-   `COLLATION` : インデックス内の列のソート方法。値は`A` （昇順）、 `D` （降順）、または`NULL` （ソートなし）のいずれかになります。
-   `CARDINALITY` : TiDBはこのフィールドを使用しません。フィールド値は常に`0`です。
-   `SUB_PART` : インデックスのプレフィックス。列のプレフィックスの一部のみがインデックスされている場合、値はインデックスされた文字数になります。列全体がインデックスされている場合、値は`NULL`なります。
-   `PACKED` : TiDBはこのフィールドを使用しません。この値は常に`NULL` 。
-   `NULLABLE` : 列に`NULL`値が含まれる可能性がある場合、値は`YES`なります。そうでない場合、値は`''`になります。
-   `INDEX_TYPE` : インデックスのタイプ。
-   `COMMENT` : インデックスに関連するその他の情報。
-   `INDEX_COMMENT` : インデックスの作成時にインデックスに指定されたコメント属性を持つコメント。
-   `IS_VISIBLE` : このインデックスが表示されるかどうか。2 [目に見えないインデックス](/sql-statements/sql-statement-create-index.md#invisible-index)参照してください。
-   `Expression`非式部分のインデックスキーの場合、この値は`NULL`です。式部分のインデックスキーの場合、この値は式そのものです[表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)を参照してください。

次の文は同等です。

```sql
SELECT * FROM INFORMATION_SCHEMA.STATISTICS
  WHERE table_name = 'tbl_name'
  AND table_schema = 'db_name'

SHOW INDEX
  FROM tbl_name
  FROM db_name
```
