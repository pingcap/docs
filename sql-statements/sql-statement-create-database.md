---
title: CREATE DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of CREATE DATABASE for the TiDB database.
---

# データベースの作成 {#create-database}

このステートメントは、TiDBに新しいデータベースを作成します。 &#39;データベース&#39;のMySQL用語は、SQL標準のスキーマに最も近いものです。

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
```

## 構文 {#syntax}

`CREATE DATABASE`ステートメントは、データベースを作成し、デフォルトの文字セットや照合順序など、データベースのデフォルトのプロパティを指定するために使用されます。 `CREATE SCHEMA`は`CREATE DATABASE`の同義語です。

```sql
CREATE {DATABASE | SCHEMA} [IF NOT EXISTS] db_name
    [create_specification] ...

create_specification:
    [DEFAULT] CHARACTER SET [=] charset_name
  | [DEFAULT] COLLATE [=] collation_name
```

既存のデータベースを作成し、 `IF NOT EXISTS`を指定しない場合、エラーが表示されます。

`create_specification`オプションは、データベース内の特定の`CHARACTER SET`および`COLLATE`を指定するために使用されます。現在、TiDBは一部の文字セットと照合のみをサポートしています。詳細については、 [文字セットと照合のサポート](/character-set-and-collation.md)を参照してください。

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

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [使用する](/sql-statements/sql-statement-use.md)
-   [ALTER DATABASE](/sql-statements/sql-statement-alter-database.md)
-   [ドロップデータベース](/sql-statements/sql-statement-drop-database.md)
-   [データベースを表示する](/sql-statements/sql-statement-show-databases.md)
