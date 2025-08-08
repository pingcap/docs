---
title: DROP USER | TiDB SQL Statement Reference
summary: TiDB データベースの DROP USER の使用法の概要。
---

# ユーザーを削除 {#drop-user}

この文は、TiDBシステムデータベースからユーザーを削除します。オプションのキーワード`IF EXISTS`使用すると、ユーザーが存在しない場合にエラーを出力しません。この文には`CREATE USER`権限が必要です。

## 概要 {#synopsis}

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

-   `IF EXISTS`で存在しないユーザーを削除しても、TiDB に警告は作成されません[問題番号 #10196](https://github.com/pingcap/tidb/issues/10196) 。

## 参照 {#see-also}

-   [ユーザーの作成](/sql-statements/sql-statement-create-user.md)
-   [ユーザーの変更](/sql-statements/sql-statement-alter-user.md)
-   [表示 ユーザーの作成](/sql-statements/sql-statement-show-create-user.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
