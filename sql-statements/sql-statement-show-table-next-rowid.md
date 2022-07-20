---
title: SHOW TABLE NEXT_ROW_ID
summary: Learn the usage of `SHOW TABLE NEXT_ROW_ID` in TiDB.
---

# テーブルNEXT_ROW_IDを表示 {#show-table-next-row-id}

`SHOW TABLE NEXT_ROW_ID`は、次のようなテーブルのいくつかの特別な列の詳細を示すために使用されます。

-   TiDBによって自動的に作成される`AUTO_INCREMENT`列、つまり`_tidb_rowid`列。
-   `AUTO_INCREMENT`列はユーザーによって作成されました。
-   [`AUTO_RANDOM`](/auto-random.md)列はユーザーによって作成されました。
-   [`SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)ユーザーによって作成されました。

## あらすじ {#synopsis}

**ShowTableNextRowIDStmt：**

![ShowTableNextRowIDStmt](/media/sqlgram/ShowTableNextRowIDStmt.png)

**TableName：**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

新しく作成されたテーブルの場合、行IDが割り当てられていないため、 `NEXT_GLOBAL_ROW_ID`は`1`です。

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

データがテーブルに書き込まれました。データを挿入するTiDBサーバーは、一度に30000個のIDを割り当ててキャッシュします。したがって、NEXT_GLOBAL_ROW_IDは30001になります。

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

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [AUTO_RANDOM](/auto-random.md)
-   [CREATE_SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
