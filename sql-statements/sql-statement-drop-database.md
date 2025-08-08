---
title: DROP DATABASE | TiDB SQL Statement Reference
summary: TiDB データベースの DROP DATABASE の使用法の概要。
---

# データベースの削除 {#drop-database}

`DROP DATABASE`文は、指定されたデータベーススキーマと、その中に作成されたすべてのテーブルとビューを永久に削除します。削除されたデータベースに関連付けられているユーザー権限は影響を受けません。

## 概要 {#synopsis}

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

TiDBの`DROP DATABASE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [データベースの変更](/sql-statements/sql-statement-alter-database.md)
