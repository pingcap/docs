---
title: CREATE DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE DATABASE for the TiDB database.
---

# データベースの作成 {#create-database}

このステートメントは、TiDB に新しいデータベースを作成します。 MySQL の「データベース」という用語は、SQL 標準のスキーマに最もよく対応しています。

## あらすじ {#synopsis}

```ebnf+diagram
CreateDatabaseStmt ::=
    'CREATE' 'DATABASE' IfNotExists DBName DatabaseOptionListOpt

IfNotExists ::=
    ( 'IF' 'NOT' 'EXISTS' )?

DBName ::=
    Identifier

DatabaseOptionListOpt ::=
    DatabaseOptionList?

DatabaseOptionList ::=
    DatabaseOption ( ','? DatabaseOption )*

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
|   DefaultKwdOpt PlacementPolicyOption

PlacementPolicyOption ::=
    "PLACEMENT" "POLICY" EqOpt PolicyName
|   "PLACEMENT" "POLICY" (EqOpt | "SET") "DEFAULT"
```

## 構文 {#syntax}

`CREATE DATABASE`ステートメントは、データベースを作成し、デフォルトの文字セットや照合順序などのデータベースのデフォルトのプロパティを指定するために使用されます。 `CREATE SCHEMA`は`CREATE DATABASE`の同義語です。

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

既存のデータベースを作成し、 `IF NOT EXISTS`を指定しない場合、エラーが表示されます。

`create_specification`オプションは、データベース内の特定の`CHARACTER SET`と`COLLATE`を指定するために使用されます。現在、TiDB は一部の文字セットと照合順序のみをサポートしています。詳細は[<a href="/character-set-and-collation.md">文字セットと照合順序のサポート</a>](/character-set-and-collation.md)を参照してください。

## 例 {#examples}

```sql
mysql> CREATE DATABASE mynewdatabase;
Query OK, 0 rows affected (0.09 sec)

mysql> USE mynewdatabase;
Database changed
mysql> CREATE TABLE t1 (a int);
Query OK, 0 rows affected (0.11 sec)

mysql> SHOW TABLES;
+-------------------------+
| Tables_in_mynewdatabase |
+-------------------------+
| t1                      |
+-------------------------+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全な互換性があると理解されています。 GitHub では互換性の違いは[<a href="https://github.com/pingcap/tidb/issues/new/choose">問題を通じて報告されました</a>](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## こちらも参照 {#see-also}

-   [<a href="/sql-statements/sql-statement-use.md">使用</a>](/sql-statements/sql-statement-use.md)
-   [<a href="/sql-statements/sql-statement-alter-database.md">データベースの変更</a>](/sql-statements/sql-statement-alter-database.md)
-   [<a href="/sql-statements/sql-statement-drop-database.md">データベースを削除</a>](/sql-statements/sql-statement-drop-database.md)
-   [<a href="/sql-statements/sql-statement-show-databases.md">データベースを表示する</a>](/sql-statements/sql-statement-show-databases.md)
