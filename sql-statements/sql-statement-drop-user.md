---
title: DROP USER | TiDB SQL Statement Reference
summary: An overview of the usage of DROP USER for the TiDB database.
---

# ユーザーを削除する {#drop-user}

このステートメントは、TiDB システム データベースからユーザーを削除します。オプションのキーワード`IF EXISTS`使用すると、ユーザーが存在しない場合にエラーを黙らせることができます。このステートメントには`CREATE USER`権限が必要です。

## あらすじ {#synopsis}

```ebnf+diagram
DropUserStmt ::=
    'DROP' 'USER' ( 'IF' 'EXISTS' )? UsernameList

Username ::=
    StringName ('@' StringName | singleAtIdentifier)? | 'CURRENT_USER' OptionalBraces
```

## 例 {#examples}

```sql
mysql> DROP USER idontexist;
ERROR 1396 (HY000): Operation DROP USER failed for idontexist@%

mysql> DROP USER IF EXISTS 'idontexist';
Query OK, 0 rows affected (0.01 sec)

mysql> CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)

mysql> REVOKE ALL ON test.* FROM 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)

mysql> DROP USER 'newuser';
Query OK, 0 rows affected (0.14 sec)

mysql> SHOW GRANTS FOR 'newuser';
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQLの互換性 {#mysql-compatibility}

-   `IF EXISTS`を使用して存在しないユーザーを削除しても、TiDB で警告は生成されません。 [問題 #10196](https://github.com/pingcap/tidb/issues/10196) ．

## こちらも参照 {#see-also}

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
-   [ユーザーの作成を表示](/sql-statements/sql-statement-show-create-user.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
