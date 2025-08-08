---
title: GRANT <privileges> | TiDB SQL Statement Reference
summary: TiDB データベースに対する GRANT <権限> の使用法の概要。
---

# <code>GRANT &#x3C;privileges></code> {#code-grant-x3c-privileges-code}

この文は、TiDB内の既存のユーザーに権限を割り当てます。TiDBの権限システムはMySQLに準拠しており、資格情報はデータベース/テーブルパターンに基づいて割り当てられます。この文を実行するには、 `GRANT OPTION`権限と割り当てたすべての権限が必要です。

## 概要 {#synopsis}

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

RequireClauseOpt ::= ('REQUIRE' ('NONE' | 'SSL' | 'X509' | RequireListElement ('AND'? RequireListElement)*))?

RequireListElement ::= 'ISSUER' Issuer | 'SUBJECT' Subject | 'CIPHER' Cipher | 'SAN' SAN | 'TOKEN_ISSUER' TokenIssuer
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

-   MySQL と同様に、 `USAGE`権限は TiDBサーバーにログインする機能を示します。
-   カラムレベルの権限は現在サポートされていません。
-   MySQLと同様に、 `NO_AUTO_CREATE_USER` SQLモードが存在しない場合、 `GRANT`ステートメントは、ユーザーが存在しない場合に空のパスワードを持つ新しいユーザーを自動的に作成します。このSQLモードを削除すると（デフォルトで有効になっています）、セキュリティリスクが生じます。
-   TiDBでは、 `GRANT <privileges>`文が正常に実行されると、その実行結果が現在の接続に直ちに反映されます。一方、 [MySQLでは、一部の権限では、実行結果は後続の接続にのみ反映されます。](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html)文については、詳細は[TiDB #39356](https://github.com/pingcap/tidb/issues/39356)参照してください。

## 参照 {#see-also}

-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
-   [ショーグラント](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
