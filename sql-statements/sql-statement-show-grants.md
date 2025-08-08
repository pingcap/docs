---
title: SHOW GRANTS | TiDB SQL Statement Reference
summary: TiDB データベースの SHOW GRANTS の使用法の概要。
---

# ショーグラント {#show-grants}

このステートメントは、ユーザーに関連付けられた権限のリストを表示します。MySQLと同様に、権限`USAGE` TiDBにログインする権限を示します。

## 概要 {#synopsis}

```ebnf+diagram
ShowGrantsStmt ::=
    "SHOW" "GRANTS" ("FOR" Username ("USING" RolenameList)?)?

Username ::=
    "CURRENT_USER" ( "(" ")" )?
| Username ("@" Hostname)?

RolenameList ::=
    Rolename ("@" Hostname)? ("," Rolename ("@" Hostname)? )*
```

## 例 {#examples}

```sql
mysql> SHOW GRANTS;
+-------------------------------------------+
| Grants for User                           |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'u1';
ERROR 1141 (42000): There is no such grant defined for user 'u1' on host '%'
mysql> CREATE USER u1;
Query OK, 1 row affected (0.04 sec)

mysql> GRANT SELECT ON test.* TO u1;
Query OK, 0 rows affected (0.04 sec)

mysql> SHOW GRANTS FOR u1;
+------------------------------------+
| Grants for u1@%                    |
+------------------------------------+
| GRANT USAGE ON *.* TO 'u1'@'%'     |
| GRANT Select ON test.* TO 'u1'@'%' |
+------------------------------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`SHOW GRANTS`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [表示 ユーザーの作成](/sql-statements/sql-statement-show-create-user.md)
-   [付与](/sql-statements/sql-statement-grant-privileges.md)
