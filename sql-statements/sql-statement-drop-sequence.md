---
title: DROP SEQUENCE
summary: DROP SEQUENCEステートメントは、TiDB内のシーケンスオブジェクトを削除します。このステートメントはTiDB拡張機能であり、MariaDBで利用可能なシーケンスに基づいてモデル化されています。SEQUENCEステートメントの例として、"DROP SEQUENCE seq;"や"DROP SEQUENCE seq, seq2;"があります。関連する操作として、シーケンスの作成やシーケンスの作成を表示する操作があります。
---

# ドロップシーケンス {#drop-sequence}

`DROP SEQUENCE`ステートメントは、TiDB 内のシーケンス オブジェクトを削除します。

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

```sql
DROP SEQUENCE seq;
```

    Query OK, 0 rows affected (0.10 sec)

```sql
DROP SEQUENCE seq, seq2;
```

    Query OK, 0 rows affected (0.03 sec)

## MySQLの互換性 {#mysql-compatibility}

このステートメントは TiDB 拡張機能です。この実装は、MariaDB で利用可能なシーケンスに基づいてモデル化されています。

## こちらも参照 {#see-also}

-   [シーケンスの作成](/sql-statements/sql-statement-create-sequence.md)
-   [シーケンスの作成を表示](/sql-statements/sql-statement-show-create-sequence.md)
