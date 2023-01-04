---
title: SHOW DATABASES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW DATABASES for the TiDB database.
---

# データベースを表示 {#show-databases}

このステートメントは、現在のユーザーが権限を持つデータベースのリストを表示します。現在のユーザーがアクセスできないデータベースは、リストに表示されません。 `information_schema`データベースは、常にデータベースのリストの最初に表示されます。

`SHOW SCHEMAS`は、このステートメントの別名です。

## あらすじ {#synopsis}

**ShowDatabasesStmt:**

![ShowDatabasesStmt](/media/sqlgram/ShowDatabasesStmt.png)

**ShowLikeOrWhereOpt:**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## 例 {#examples}

```sql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)

mysql> CREATE DATABASE mynewdb;
Query OK, 0 rows affected (0.10 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mynewdb            |
| mysql              |
| test               |
+--------------------+
5 rows in set (0.00 sec)
```

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [スキーマを表示](/sql-statements/sql-statement-show-schemas.md)
-   [データベースをドロップ](/sql-statements/sql-statement-drop-database.md)
-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
