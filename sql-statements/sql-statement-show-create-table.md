---
title: SHOW CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE TABLE for the TiDB database.
---

# テーブルの作成を表示 {#show-create-table}

このステートメントは、SQL を使用して既存のテーブルを再作成するための正確なステートメントを示しています。

## あらすじ {#synopsis}

**ShowCreateTableStmt:**

![ShowCreateTableStmt](/media/sqlgram/ShowCreateTableStmt.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.12 sec)

mysql> SHOW CREATE TABLE t1;
+-------+------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                               |
+-------+------------------------------------------------------------------------------------------------------------+
| t1    | CREATE TABLE `t1` (
  `a` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin |
+-------+------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SHOW CREATE TABLE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [次の列を表示](/sql-statements/sql-statement-show-columns-from.md)
