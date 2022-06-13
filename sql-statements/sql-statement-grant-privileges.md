---
title: GRANT <privileges> | TiDB SQL Statement Reference
summary: An overview of the usage of GRANT <privileges> for the TiDB database.
---

# <code>GRANT &#x3C;privileges></code> {#code-grant-x3c-privileges-code}

このステートメントは、TiDBの既存のユーザーに特権を割り当てます。 TiDBの特権システムはMySQLに従い、データベース/テーブルパターンに基づいて資格情報が割り当てられます。このステートメントを実行するには、 `GRANT OPTION`の特権と割り当てたすべての特権が必要です。

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

-   MySQLと同様に、 `USAGE`特権はTiDBサーバーにログインする機能を示します。
-   列レベルの権限は現在サポートされていません。
-   MySQLと同様に、 `NO_AUTO_CREATE_USER` sqlモードが存在しない場合、ユーザーが存在しない場合、 `GRANT`ステートメントは空のパスワードで新しいユーザーを自動的に作成します。このsql-modeを削除すると（デフォルトで有効になっています）、セキュリティ上のリスクがあります。

## も参照してください {#see-also}

-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
-   [助成金を表示](/sql-statements/sql-statement-show-grants.md)
-   [権限管理](/privilege-management.md)
