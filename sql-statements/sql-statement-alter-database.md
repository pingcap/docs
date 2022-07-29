---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER DATABASE for the TiDB database.
---

# ALTER DATABASE {#alter-database}

`ALTER DATABASE`は、現在のデータベースのデフォルトの文字セットと照合順序を指定または変更するために使用されます。 `ALTER SCHEMA`は`ALTER DATABASE`と同じ効果があります。

## あらすじ {#synopsis}

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 例 {#examples}

utf8mb4文字セットを使用するようにテストデータベーススキーマを変更します。

{{< copyable "" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

現在、TiDBは一部の文字セットと照合のみをサポートしています。詳細については、 [文字セットと照合のサポート](/character-set-and-collation.md)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQLと完全に互換性があると理解されています。互換性の違いは、GitHubでは[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)である必要があります。

## も参照してください {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [データベースを表示する](/sql-statements/sql-statement-show-databases.md)
