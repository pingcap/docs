---
title: DROP SEQUENCE
summary: An overview of the usage of DROP SEQUENCE for the TiDB database.
---

# ドロップシーケンス {#drop-sequence}

`DROP SEQUENCE`ステートメントは、シーケンス オブジェクトを TiDB にドロップします。

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

## MySQL の互換性 {#mysql-compatibility}

このステートメントは TiDB 拡張機能です。実装は、MariaDB で利用可能なシーケンスをモデルにしています。

## こちらもご覧ください {#see-also}

-   [シーケンスを作成](/sql-statements/sql-statement-create-sequence.md)
-   [作成シーケンスを表示](/sql-statements/sql-statement-show-create-sequence.md)
