---
title: DROP SEQUENCE
summary: TiDB データベースの DROP SEQUENCE の使用法の概要。
---

# ドロップシーケンス {#drop-sequence}

`DROP SEQUENCE`のステートメントは、TiDB 内のシーケンス オブジェクトを削除します。

## 概要 {#synopsis}

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

このステートメントはTiDBの拡張機能です。実装はMariaDBで利用可能なシーケンスをモデルにしています。

## 参照 {#see-also}

-   [シーケンスを作成](/sql-statements/sql-statement-create-sequence.md)
-   [シーケンスの変更](/sql-statements/sql-statement-alter-sequence.md)
-   [シーケンスの作成を表示](/sql-statements/sql-statement-show-create-sequence.md)
