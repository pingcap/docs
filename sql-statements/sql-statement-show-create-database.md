---
title: SHOW CREATE DATABASE
summary: An overview of the use of SHOW CREATE DATABASE in the TiDB database.
---

# 表示 データベースの作成 {#show-create-database}

`SHOW CREATE DATABASE`は、既存のデータベースを再作成するための正確な SQL ステートメントを示すために使用されます。 `SHOW CREATE SCHEMA`はその同義語です。

## あらすじ {#synopsis}

**ShowCreateDatabaseStmt:**

```ebnf+diagram
ShowCreateDatabaseStmt ::=
    "SHOW" "CREATE" "DATABASE" | "SCHEMA" ("IF" "NOT" "EXISTS")? DBName
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

`SHOW CREATE DATABASE`は MySQL と完全な互換性があることが期待されています。互換性の違いを見つけた場合は、 GitHub [<a href="https://github.com/pingcap/tidb/issues/new/choose">問題</a>](https://github.com/pingcap/tidb/issues/new/choose)を送信してください。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-create-table.md">テーブルの作成</a>](/sql-statements/sql-statement-create-table.md)
-   [<a href="/sql-statements/sql-statement-drop-table.md">ドロップテーブル</a>](/sql-statements/sql-statement-drop-table.md)
-   [<a href="/sql-statements/sql-statement-show-tables.md">テーブルを表示</a>](/sql-statements/sql-statement-show-tables.md)
-   [<a href="/sql-statements/sql-statement-show-columns-from.md">次の列を表示</a>](/sql-statements/sql-statement-show-columns-from.md)
