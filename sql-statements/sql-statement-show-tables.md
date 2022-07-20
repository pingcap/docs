---
title: SHOW [FULL] TABLES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] TABLES for the TiDB database.
---

# [フル]テーブルを表示 {#show-full-tables}

このステートメントは、現在選択されているデータベース内のテーブルとビューのリストを示しています。オプションのキーワード`FULL`は、テーブルのタイプが`BASE TABLE`か`VIEW`かを示します。

別のデータベースのテーブルを表示するには、 `SHOW TABLES IN DatabaseName`を使用します。

## あらすじ {#synopsis}

**ShowTablesStmt：**

![ShowTablesStmt](/media/sqlgram/ShowTablesStmt.png)

**OptFull：**

![OptFull](/media/sqlgram/OptFull.png)

**ShowDatabaseNameOpt：**

![ShowDatabaseNameOpt](/media/sqlgram/ShowDatabaseNameOpt.png)

**ShowLikeOrWhereOpt：**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.12 sec)

mysql> CREATE VIEW v1 AS SELECT 1;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+----------------+
| Tables_in_test |
+----------------+
| t1             |
| v1             |
+----------------+
2 rows in set (0.00 sec)

mysql> SHOW FULL TABLES;
+----------------+------------+
| Tables_in_test | Table_type |
+----------------+------------+
| t1             | BASE TABLE |
| v1             | VIEW       |
+----------------+------------+
2 rows in set (0.00 sec)

mysql> SHOW TABLES IN mysql;
+-------------------------+
| Tables_in_mysql         |
+-------------------------+
| GLOBAL_VARIABLES        |
| bind_info               |
| columns_priv            |
| db                      |
| default_roles           |
| expr_pushdown_blacklist |
| gc_delete_range         |
| gc_delete_range_done    |
| global_priv             |
| help_topic              |
| opt_rule_blacklist      |
| role_edges              |
| stats_buckets           |
| stats_feedback          |
| stats_histograms        |
| stats_meta              |
| stats_top_n             |
| tables_priv             |
| tidb                    |
| user                    |
+-------------------------+
20 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [ドロップテーブル](/sql-statements/sql-statement-drop-table.md)
-   [作成テーブルを表示](/sql-statements/sql-statement-show-create-table.md)
