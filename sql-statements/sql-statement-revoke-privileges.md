---
title: REVOKE <privileges> | TiDB SQL Statement Reference
summary: TiDB データベースに対する REVOKE <権限> の使用法の概要。
---

# <code>REVOKE &#x3C;privileges></code> {#code-revoke-x3c-privileges-code}

このステートメントは、既存のユーザーから権限を削除します。このステートメントを実行するには、 `GRANT OPTION`権限と取り消すすべての権限が必要です。

## 概要 {#synopsis}

```ebnf+diagram
RevokeStmt ::=
    'REVOKE' PrivElemList 'ON' ObjectType PrivLevel 'FROM' UserSpecList

PrivElemList ::=
    PrivElem ( ',' PrivElem )*

PrivElem ::=
    PrivType ( '(' ColumnNameList ')' )?

PrivType ::=
    'ALL' 'PRIVILEGES'?
|   'ALTER' 'ROUTINE'?
|   'CREATE' ( 'USER' | 'TEMPORARY' 'TABLES' | 'VIEW' | 'ROLE' | 'ROUTINE' )?
|    'TRIGGER'
|   'DELETE'
|    'DROP' 'ROLE'?
|    'PROCESS'
|    'EXECUTE'
|   'INDEX'
|   'INSERT'
|   'SELECT'
|   'SUPER'
|    'SHOW' ( 'DATABASES' | 'VIEW' )
|   'UPDATE'
|   'GRANT' 'OPTION'
|   'REFERENCES'
|   'REPLICATION' ( 'SLAVE' | 'CLIENT' )
|   'USAGE'
|    'RELOAD'
|   'FILE'
|   'CONFIG'
|   'LOCK' 'TABLES'
|    'EVENT'
|   'SHUTDOWN'

ObjectType ::=
    'TABLE'?

PrivLevel ::=
    '*' ( '.' '*' )?
|    Identifier ( '.' ( '*' | Identifier ) )?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*
```

## 例 {#examples}

```sql
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

## MySQL 互換性 {#mysql-compatibility}

-   TiDB では、 `REVOKE <privileges>`ステートメントが正常に実行されると、実行結果が現在の接続に直ちに反映されます。一方、 [MySQLでは、一部の権限では、実行結果は後続の接続にのみ有効になります。](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html)については、詳細については[ティDB #39356](https://github.com/pingcap/tidb/issues/39356)参照してください。

## 参照 {#see-also}

-   [`GRANT &#x3C;privileges>`](/sql-statements/sql-statement-grant-privileges.md)
-   [ショーグラント](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
