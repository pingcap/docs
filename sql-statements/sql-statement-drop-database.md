---
title: DROP DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of DROP DATABASE for the TiDB database.
---

# ドロップデータベース {#drop-database}

`DROP DATABASE`ステートメントは、指定されたデータベーススキーマ、および内部で作成されたすべてのテーブルとビューを完全に削除します。ドロップされたデータベースに関連付けられているユーザー権限は影響を受けません。

## あらすじ {#synopsis}

```ebnf+diagram
DropDatabaseStmt ::=
    'DROP' 'DATABASE' IfExists DBName

IfExists ::= ( 'IF' 'EXISTS' )?
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

mysql> DROP DATABASE test;
Query OK, 0 rows affected (0.25 sec)

mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
+--------------------+
3 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
