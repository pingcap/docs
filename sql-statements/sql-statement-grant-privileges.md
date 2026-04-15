---
title: GRANT <privileges> | TiDB SQL Statement Reference
summary: TiDBデータベースに対するGRANT <権限>の使用方法の概要。
---

# <code>GRANT &#x3C;privileges></code> {#code-grant-x3c-privileges-code}

このステートメントは、TiDB の既存ユーザーに権限を割り当てます。TiDB の権限システムは MySQL に準拠しており、データベース/テーブルパターンに基づいて認証情報が割り当てられます。このステートメントを実行するには、 `GRANT OPTION`権限と、割り当てるすべての権限が必要です。

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

## MySQLとの互換性 {#mysql-compatibility}

-   MySQLと同様に、 `USAGE`権限はTiDBサーバーにログインする能力を示します。
-   バージョン8.5.6以降、TiDBはMySQL互換の列レベルの権限管理メカニズムをサポートしています。指定したテーブルの特定の列に対して、 `SELECT` 、 `INSERT` 、 `UPDATE` 、および`REFERENCES`権限を付与または取り消すことができます。詳細については、[列レベルの権限管理](/column-privilege-management.md)を参照してください。
-   MySQLと同様に、 `NO_AUTO_CREATE_USER` SQLモードが存在しない場合、 `GRANT`ステートメントは、ユーザーが存在しない場合に、パスワードが空の新しいユーザーを自動的に作成します。このSQLモードを削除すると（デフォルトでは有効になっています）、セキュリティ上のリスクが生じます。
-   TiDB では、 `GRANT <privileges>`ステートメントが正常に実行されると、実行結果は現在の接続に直ちに有効になります。一方[MySQLでは、一部の権限では、実行結果は後続の接続でのみ有効になります。](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html)詳細については、 [TiDB #39356](https://github.com/pingcap/tidb/issues/39356)を参照してください。

## 関連項目 {#see-also}

-   [`GRANT &#x3C;role>`](/sql-statements/sql-statement-grant-role.md)
-   [`REVOKE &#x3C;privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
-   [ショー助成金](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

-   [権限管理](/privilege-management.md)

</CustomContent>
