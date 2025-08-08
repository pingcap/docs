---
title: SHOW CREATE DATABASE
summary: TiDB データベースでの SHOW CREATE DATABASE の使用の概要。
---

# 表示データベースの作成 {#show-create-database}

`SHOW CREATE DATABASE`は、既存のデータベースを再作成するための正確な SQL ステートメントを表示するために使用されます。2 `SHOW CREATE SCHEMA`その同義語です。

## 概要 {#synopsis}

**データベースステートメントの作成を表示:**

```ebnf+diagram
ShowCreateDatabaseStmt ::=
    "SHOW" "CREATE" ("DATABASE" | "SCHEMA") ("IF" "NOT" "EXISTS")? DBName
```

## 例 {#examples}

```sql
CREATE DATABASE test;
```

```sql
Query OK, 0 rows affected (0.12 sec)
```

```sql
SHOW CREATE DATABASE test;
```

```sql
+----------+------------------------------------------------------------------+
| Database | Create Database                                                  |
+----------+------------------------------------------------------------------+
| test     | CREATE DATABASE `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+------------------------------------------------------------------+
1 row in set (0.00 sec)
```

```sql
SHOW CREATE SCHEMA IF NOT EXISTS test;
```

```sql
+----------+-------------------------------------------------------------------------------------------+
| Database | Create Database                                                                           |
+----------+-------------------------------------------------------------------------------------------+
| test     | CREATE DATABASE /*!32312 IF NOT EXISTS*/ `test` /*!40100 DEFAULT CHARACTER SET utf8mb4 */ |
+----------+-------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

`SHOW CREATE DATABASE` MySQL と完全に互換性があると予想されます。互換性に違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [テーブルを削除](/sql-statements/sql-statement-drop-table.md)
-   [テーブルを表示](/sql-statements/sql-statement-show-tables.md)
-   [列を表示](/sql-statements/sql-statement-show-columns-from.md)
