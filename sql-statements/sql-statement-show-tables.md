---
title: SHOW [FULL] TABLES | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW [FULL] TABLES の使用法の概要。
---

# [全]テーブルを表示 {#show-full-tables}

このステートメントは、現在選択されているデータベース内のテーブルとビューのリストを表示します。オプションのキーワード`FULL`は、テーブルのタイプが`BASE TABLE` 、 `SEQUENCE` 、または`VIEW`であるかどうかを示します。

別のデータベース内のテーブルを表示するには、 `SHOW TABLES IN DatabaseName`使用します。

## 概要 {#synopsis}

```ebnf+diagram
ShowTableStmt ::=
    "SHOW" "FULL"? "TABLES" ("FROM" Identifier | "IN" Identifier )? ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

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

## MySQL 互換性 {#mysql-compatibility}

TiDB の`SHOW [FULL] TABLES`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
-   [表示テーブルの作成](/sql-statements/sql-statement-show-create-table.md)
-   [`INFORMATION_SCHEMA.TABLES`](/information-schema/information-schema-tables.md)
