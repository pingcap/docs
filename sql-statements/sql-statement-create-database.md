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

`create_specification`オプションは、データベース内の特定の`CHARACTER SET`と`COLLATE`を指定するために使用されます。現在、TiDB は一部の文字セットと照合順序のみをサポートしています。詳細は[文字セットと照合順序のサポート](/character-set-and-collation.md)を参照してください。

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

TiDB の`CREATE DATABASE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [使用](/sql-statements/sql-statement-use.md)
-   [データベースの変更](/sql-statements/sql-statement-alter-database.md)
-   [データベースを削除](/sql-statements/sql-statement-drop-database.md)
-   [データベースを表示する](/sql-statements/sql-statement-show-databases.md)
