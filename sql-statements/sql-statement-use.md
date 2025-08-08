---
title: USE | TiDB SQL Statement Reference
summary: TiDB データベースにおける USE の使用法の概要。
---

# 使用 {#use}

`USE`ステートメントは、ユーザー セッションの現在のデータベースを選択します。

## 概要 {#synopsis}

```ebnf+diagram
UseStmt ::=
    "USE" DBName

DBName ::=
    Identifier
```

## 例 {#examples}

```sql
mysql> USE mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> SHOW TABLES;
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
20 rows in set (0.01 sec)

mysql> CREATE DATABASE newtest;
Query OK, 0 rows affected (0.10 sec)

mysql> USE newtest;
Database changed
mysql> SHOW TABLES;
Empty set (0.00 sec)

mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW TABLES;
+-------------------+
| Tables_in_newtest |
+-------------------+
| t1                |
+-------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`USE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
