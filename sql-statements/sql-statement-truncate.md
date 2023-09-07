---
title: TRUNCATE | TiDB SQL Statement Reference
summary: An overview of the usage of TRUNCATE for the TiDB database.
---

# 切り詰める {#truncate}

`TRUNCATE`ステートメントは、非トランザクション的な方法でテーブルからすべてのデータを削除します。 `TRUNCATE`前の定義の`DROP TABLE` + `CREATE TABLE`と意味的に同じと考えることができます。

`TRUNCATE TABLE tableName`と`TRUNCATE tableName`はどちらも有効な構文です。

## あらすじ {#synopsis}

**TruncateTableStmt:**

![TruncateTableStmt](/media/sqlgram/TruncateTableStmt.png)

**オプトテーブル:**

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

## MySQLの互換性 {#mysql-compatibility}

TiDB の`TRUNCATE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [消去](/sql-statements/sql-statement-delete.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルの作成を表示](/sql-statements/sql-statement-show-create-table.md)
