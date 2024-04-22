---
title: ALTER DATABASE | TiDB SQL Statement Reference
summary: ALTER DATABASEは、デフォルトの文字セットと照合順序を変更するために使用されます。TiDBはMySQLと完全な互換性があります。文字セットと照合順序のサポートについては、詳細を参照してください。
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

```sql
ALTER DATABASE test DEFAULT CHARACTER SET = utf8mb4;
```

```sql
Query OK, 0 rows affected (0.00 sec)
```

現在、TiDB は一部の文字セットと照合順序のみをサポートしています。詳細については[文字セットと照合順序のサポート](/character-set-and-collation.md)を参照してください。

## MySQLの互換性 {#mysql-compatibility}

TiDB の`ALTER DATABASE`ステートメントは MySQL と完全な互換性があります。互換性の違いが見つかった場合は、 [バグを報告](https://docs.pingcap.com/tidb/stable/support) .

## こちらも参照 {#see-also}

-   [データベースの作成](/sql-statements/sql-statement-create-database.md)
-   [データベースを表示する](/sql-statements/sql-statement-show-databases.md)
