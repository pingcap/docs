---
title: SHOW CREATE TABLE | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW CREATE TABLE for the TiDB database.
---

# CREATETABLEを表示する {#show-create-table}

このステートメントは、SQLを使用して既存のテーブルを再作成するための正確なステートメントを示しています。

## あらすじ {#synopsis}

**ShowCreateTableStmt：**

![ShowCreateTableStmt](/media/sqlgram/ShowCreateTableStmt.png)

**TableName：**

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

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [CREATE TABLE](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [から列を表示](/sql-statements/sql-statement-show-columns-from.md)
