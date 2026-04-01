---
title: SHOW TABLE NEXT_ROW_ID
summary: TiDBにおけるSHOW TABLE NEXT_ROW_ID`の使い方を学びましょう。
---

# SHOW TABLE NEXT_ROW_ID {#show-table-next-row-id}

`SHOW TABLE NEXT_ROW_ID`は、以下のようなテーブルの特定の列の詳細を表示するために使用されます。

-   [`_tidb_rowid`](/tidb-rowid.md) 、サポートされているテーブルの場合、TiDB によって自動的に管理される非表示の行 ID 列です。
-   ユーザーによって作成された列は`AUTO_INCREMENT` 。
-   ユーザーによって作成された列は[`AUTO_RANDOM`](/auto-random.md) 。
-   ユーザーによって作成されたファイル数は[`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) 。

## あらすじ {#synopsis}

```ebnf+diagram
ShowTableNextRowIDStmt ::=
    "SHOW" "TABLE" (SchemaName ".")? TableName "NEXT_ROW_ID"
```

## 例 {#examples}

新しく作成されたテーブルの場合、行IDが割り当てられないため、 `NEXT_GLOBAL_ROW_ID`は`1`になります。

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

データがテーブルに書き込まれました。データを挿入する TiDBサーバーは、一度に 30000 個の ID を割り当ててキャッシュします。したがって、NEXT_GLOBAL_ROW_ID は現在 30001 です。ID の数は[`AUTO_ID_CACHE`](/auto-increment.md#auto_id_cache)で制御されます。

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

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [テーブルを作成する](/sql-statements/sql-statement-create-table.md)
-   [自動乱数](/auto-random.md)
-   [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
-   [_tidb_rowid](/tidb-rowid.md)
