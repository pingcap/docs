---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: An overview of the usage of ALTER DATABASE for the TiDB database.
---

# データベースの変更 {#alter-database}

`ALTER DATABASE`は、現在のデータベースのデフォルトの文字セットと照合順序を指定または変更するために使用されます。 `ALTER SCHEMA` `ALTER DATABASE`と同じ効果があります。

## あらすじ {#synopsis}

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 例 {#examples}

utf8mb4 文字セットを使用するようにテスト データベース スキーマを変更します。

{{< copyable "" >}}

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

現在、TiDB は一部の文字セットと照合のみをサポートしています。詳細は[文字セットと照合のサポート](/character-set-and-collation.md)を参照してください。

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL と完全に互換性があると理解されています。互換性の違いは、GitHub で[問題を介して報告された](https://github.com/pingcap/tidb/issues/new/choose)にする必要があります。

## こちらもご覧ください {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [データベースを表示](/sql-statements/sql-statement-show-databases.md)
