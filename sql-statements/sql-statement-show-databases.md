---
title: SHOW DATABASES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW DATABASES for the TiDB database.
---

# データベースを表示する {#show-databases}

このステートメントは、現在のユーザーが特権を持っているデータベースのリストを示しています。現在のユーザーがアクセスできないデータベースは、リストから非表示になります。 `information_schema`のデータベースは、常にデータベースのリストの最初に表示されます。

`SHOW SCHEMAS`はこのステートメントのエイリアスです。

## あらすじ {#synopsis}

**ShowDatabasesStmt：**

![ShowDatabasesStmt](/media/sqlgram/ShowDatabasesStmt.png)

**ShowLikeOrWhereOpt：**

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

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [スキーマを表示](/sql-statements/sql-statement-show-schemas.md)
-   [ドロップデータベース](/sql-statements/sql-statement-drop-database.md)
-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
