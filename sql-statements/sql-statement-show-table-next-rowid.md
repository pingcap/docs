---
title: SHOW TABLE NEXT_ROW_ID
summary: Learn the usage of `SHOW TABLE NEXT_ROW_ID` in TiDB.
---

# テーブルの NEXT_ROW_ID を表示 {#show-table-next-row-id}

`SHOW TABLE NEXT_ROW_ID`は、次のようなテーブルのいくつかの特別な列の詳細を表示するために使用されます。

-   TiDB によって自動的に作成される`AUTO_INCREMENT`列、つまり`_tidb_rowid`列。
-   ユーザーが作成した`AUTO_INCREMENT`列。
-   ユーザーが作成した[`AUTO_RANDOM`](/auto-random.md)列。
-   [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)ユーザーによって作成されました。

## あらすじ {#synopsis}

**ShowTableNextRowIDStmt:**

![ShowTableNextRowIDStmt](/media/sqlgram/ShowTableNextRowIDStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

新しく作成されたテーブルの場合、Row ID が割り当てられていないため、 `NEXT_GLOBAL_ROW_ID`は`1`です。

{{< copyable "" >}}

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

テーブルにデータが書き込まれました。データを挿入する TiDBサーバーは、一度に 30000 個の ID を割り当ててキャッシュします。したがって、NEXT_GLOBAL_ROW_ID は現在 30001 です。

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

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
-   [自動ランダム](/auto-random.md)
-   [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
