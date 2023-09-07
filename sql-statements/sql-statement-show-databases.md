---
title: SHOW DATABASES | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW DATABASES for the TiDB database.
---

# データベースを表示する {#show-databases}

このステートメントは、現在のユーザーが権限を持つデータベースのリストを表示します。現在のユーザーがアクセスできないデータベースは、リストに表示されません。 `information_schema`データベースは常にデータベースのリストの最初に表示されます。

`SHOW SCHEMAS`はこのステートメントの別名です。

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

## MySQLの互換性 {#mysql-compatibility}

TiDB の`SHOW DATABASES`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [スキーマの表示](/sql-statements/sql-statement-show-schemas.md)
-   [データベースを削除](/sql-statements/sql-statement-drop-database.md)
-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
