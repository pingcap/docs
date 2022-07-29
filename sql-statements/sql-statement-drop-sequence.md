---
title: DROP SEQUENCE
summary: An overview of the usage of DROP SEQUENCE for the TiDB database.
---

# ドロップシーケンス {#drop-sequence}

`DROP SEQUENCE`ステートメントは、TiDBのシーケンスオブジェクトを削除します。

## あらすじ {#synopsis}

```ebnf+diagram
DropSequenceStmt ::=
    'DROP' 'SEQUENCE' IfExists TableNameList

IfExists ::= ( 'IF' 'EXISTS' )?

TableNameList ::=
    TableName ( ',' TableName )*

TableName ::=
    Identifier ('.' Identifier)?
```

## 例 {#examples}

{{< copyable "" >}}

```sql
DROP SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.10 sec)
```

{{< copyable "" >}}

```sql
DROP SEQUENCE seq, seq2;
```

```
Query OK, 0 rows affected (0.03 sec)
```

## MySQLの互換性 {#mysql-compatibility}

このステートメントはTiDB拡張です。実装は、MariaDBで利用可能なシーケンスをモデルにしています。

## も参照してください {#see-also}

-   [シーケンスの作成](/sql-statements/sql-statement-create-sequence.md)
-   [CREATESEQUENCEを表示する](/sql-statements/sql-statement-show-create-sequence.md)
