---
title: GRANT <privileges> | TiDB SQL Statement Reference
summary: An overview of the usage of GRANT <privileges> for the TiDB database.
---

# <code>GRANT &#x3C;privileges></code> {#code-grant-x3c-privileges-code}

このステートメントは、TiDB 内の既存のユーザーに権限を割り当てます。 TiDB の権限システムは MySQL に従っており、データベース/テーブルのパターンに基づいて資格情報が割り当てられます。このステートメントを実行するには、 `GRANT OPTION`権限と、割り当てたすべての権限が必要です。

## あらすじ {#synopsis}

```ebnf+diagram
GrantStmt ::=
    'GRANT' PrivElemList 'ON' ObjectType PrivLevel 'TO' UserSpecList RequireClauseOpt WithGrantOptionOpt

PrivElemList ::=
    PrivElem ( ',' PrivElem )*

PrivElem ::=
    PrivType ( '(' ColumnNameList ')' )?

PrivType ::=
    'ALL' 'PRIVILEGES'?
|    'ALTER' 'ROUTINE'?
|   'CREATE' ( 'USER' | 'TEMPORARY' 'TABLES' | 'VIEW' | 'ROLE' | 'ROUTINE' )?
|   'TRIGGER'
|   'DELETE'
|   'DROP' 'ROLE'?
|    'PROCESS'
|   'EXECUTE'
|   'INDEX'
|   'INSERT'
|   'SELECT'
|   'SUPER'
|   'SHOW' ( 'DATABASES' | 'VIEW' )
|   'UPDATE'
|    'GRANT' 'OPTION'
|    'REFERENCES'
|    'REPLICATION' ( 'SLAVE' | 'CLIENT' )
|    'USAGE'
|   'RELOAD'
|   'FILE'
|   'CONFIG'
|   'LOCK' 'TABLES'
|   'EVENT'
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
```

## MySQLの互換性 {#mysql-compatibility}

-   MySQL と同様に、 `USAGE`特権は TiDBサーバーにログインできることを示します。
-   カラムレベルの権限は現在サポートされていません。
-   MySQL と同様に、 `NO_AUTO_CREATE_USER` SQL モードが存在しない場合、ユーザーが存在しない場合、 `GRANT`ステートメントは空のパスワードを持つ新しいユーザーを自動的に作成します。この SQL モードを削除すると (デフォルトで有効になっています)、セキュリティ上のリスクが生じます。
-   TiDB では、 `GRANT <privileges>`ステートメントが正常に実行されると、実行結果は現在の接続に即座に反映されます。一方、 [MySQL では、一部の権限については、実行結果は後続の接続でのみ有効になります。](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html) 。詳細は[TiDB #39356](https://github.com/pingcap/tidb/issues/39356)を参照してください。

## こちらも参照 {#see-also}

-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
-   [助成金を表示する](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
