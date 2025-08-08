---
title: SHOW TABLE NEXT_ROW_ID
summary: TiDB での SHOW TABLE NEXT_ROW_ID` の使用方法を学びます。
---

# テーブルの次の行IDを表示 {#show-table-next-row-id}

`SHOW TABLE NEXT_ROW_ID` 、次のようなテーブルの特殊な列の詳細を表示するために使用されます。

-   TiDB によって自動的に作成された[`AUTO_INCREMENT`](/auto-increment.md)列、つまり`_tidb_rowid`列。
-   ユーザーが作成した列は`AUTO_INCREMENT` 。
-   ユーザーが作成した列は[`AUTO_RANDOM`](/auto-random.md) 。
-   ユーザーが作成したものは[`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 。

## 概要 {#synopsis}

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## 例 {#examples}

新しく作成されたテーブルの場合、行 ID が割り当てられていないため、 `NEXT_GLOBAL_ROW_ID` `1`なります。

```sql
CREATE TABLE t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

テーブルにデータが書き込まれました。データを挿入するTiDBサーバーは、一度に30000個のIDを割り当ててキャッシュします。そのため、NEXT_GLOBAL_ROW_IDは現在30001です。IDの数は[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache)で制御されます。

```sql
INSERT INTO t VALUES (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
SHOW TABLE t NEXT_ROW_ID;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [自動ランダム](/auto-random.md)
-   [シーケンスの作成](/sql-statements/sql-statement-create-sequence.md)
