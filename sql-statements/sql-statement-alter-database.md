---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: TiDB データベースに対する ALTER DATABASE の使用法の概要。
---

# データベースの変更 {#alter-database}

`ALTER DATABASE` 、現在のデータベースのデフォルトの文字セットと照合順序を指定または変更するために使用されます。 `ALTER SCHEMA` `ALTER DATABASE`と同じ効果があります。

## 概要 {#synopsis}

```ebnf+diagram
AlterDatabaseStmt ::=
    'ALTER' 'DATABASE' DBName? DatabaseOptionList

DatabaseOption ::=
    DefaultKwdOpt ( CharsetKw '='? CharsetName | 'COLLATE' '='? CollationName | 'ENCRYPTION' '='? EncryptionOpt )
```

## 例 {#examples}

utf8mb4 文字セットを使用するようにテスト データベース スキーマを変更します。

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

現在、TiDBは一部の文字セットと照合順序のみをサポートしています。詳細は[文字セットと照合順序のサポート](/character-set-and-collation.md)ご覧ください。

## MySQLの互換性 {#mysql-compatibility}

TiDBの`ALTER DATABASE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [データベースを表示](/sql-statements/sql-statement-show-databases.md)
