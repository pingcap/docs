---
title: TRUNCATE | TiDB SQL Statement Reference
summary: An overview of the usage of TRUNCATE for the TiDB database.
---

# トランケート {#truncate}

`TRUNCATE`ステートメントは、非トランザクションの方法でテーブルからすべてのデータを削除します。 `TRUNCATE`前の定義の`DROP TABLE` + `CREATE TABLE`と意味的に同じと考えることができます。

`TRUNCATE TABLE tableName`と`TRUNCATE tableName`の両方が有効な構文です。

## あらすじ {#synopsis}

**TruncateTableStmt:**

![TruncateTableStmt](/media/sqlgram/TruncateTableStmt.png)

**オプション テーブル:**

![OptTable](/media/sqlgram/OptTable.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+---+
| a |
+---+
| 1 |
| 2 |
| 3 |
| 4 |
| 5 |
+---+
5 rows in set (0.00 sec)

mysql> TRUNCATE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> SELECT * FROM t1;
Empty set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.01 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> TRUNCATE TABLE t1;
Query OK, 0 rows affected (0.11 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [テーブルを作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
