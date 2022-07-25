---
title: DROP USER | TiDB SQL Statement Reference
summary: An overview of the usage of DROP USER for the TiDB database.
---

# ドロップユーザー {#drop-user}

このステートメントは、TiDBシステムデータベースからユーザーを削除します。オプションのキーワード`IF EXISTS`を使用すると、ユーザーが存在しない場合にエラーを消音できます。このステートメントには`CREATE USER`の特権が必要です。

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

-   `IF EXISTS`で存在しないユーザーを削除しても、TiDBに警告は作成されません。 [問題＃10196](https://github.com/pingcap/tidb/issues/10196) 。

## も参照してください {#see-also}

-   [ユーザーを作成](/sql-statements/sql-statement-create-user.md)
-   [ALTER USER](/sql-statements/sql-statement-alter-user.md)
-   [CREATEUSERを表示する](/sql-statements/sql-statement-show-create-user.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
