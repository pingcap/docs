---
title: SHOW TABLE NEXT_ROW_ID
summary: Learn the usage of `SHOW TABLE NEXT_ROW_ID` in TiDB.
---

# テーブルのNEXT_ROW_IDを表示 {#show-table-next-row-id}

`SHOW TABLE NEXT_ROW_ID`は、テーブルのいくつかの特別な列の詳細を示すために使用されます。次のようなものがあります。

-   TiDB によって自動的に作成される`AUTO_INCREMENT`列、つまり`_tidb_rowid`列。
-   ユーザーが作成した列は`AUTO_INCREMENT` 。
-   ユーザーが作成した列は[`AUTO_RANDOM`](/auto-random.md) 。
-   ユーザーが作成したものは[`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)ます。

## あらすじ {#synopsis}

**ShowTableNextRowIDStmt:**

![ShowTableNextRowIDStmt](/media/sqlgram/ShowTableNextRowIDStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

新しく作成されたテーブルの場合、ロウ ID が割り当てられていないため、 `NEXT_GLOBAL_ROW_ID`は`1`になります。

```sql
create table t(a int);
Query OK, 0 rows affected (0.06 sec)
```

```sql
show table t next_row_id;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |                  1 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

データがテーブルに書き込まれました。データを挿入する TiDBサーバーは、一度に 30,000 ID を割り当ててキャッシュします。したがって、NEXT_GLOBAL_ROW_ID は現在 30001 です。

```sql
insert into t values (), (), ();
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0
```

```sql
show table t next_row_id;
+---------+------------+-------------+--------------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID |
+---------+------------+-------------+--------------------+
| test    | t          | _tidb_rowid |              30001 |
+---------+------------+-------------+--------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [自動ランダム](/auto-random.md)
-   [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
