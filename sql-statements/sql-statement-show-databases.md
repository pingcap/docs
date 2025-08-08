---
title: SHOW DATABASES | TiDB SQL Statement Reference
summary: TiDB データベースに対する SHOW DATABASES の使用法の概要。
---

# データベースを表示 {#show-databases}

このステートメントは、現在のユーザーが権限を持つデータベースのリストを表示します。現在のユーザーがアクセスできないデータベースはリストに表示されません。データベース`information_schema`常にデータベースリストの先頭に表示されます。

`SHOW SCHEMAS`はこのステートメントのエイリアスです。

## 概要 {#synopsis}

```ebnf+diagram
ShowDatabasesStmt ::=
    "SHOW" "DATABASES" ShowLikeOrWhere?

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

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

TiDBの`SHOW DATABASES`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [スキーマを表示](/sql-statements/sql-statement-show-schemas.md)
-   [データベースの削除](/sql-statements/sql-statement-drop-database.md)
-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [`INFORMATION_SCHEMA.SCHEMATA`](/information-schema/information-schema-schemata.md)
