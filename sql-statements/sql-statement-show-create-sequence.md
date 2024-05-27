---
title: SHOW CREATE SEQUENCE
summary: TiDB データベースの SHOW CREATE SEQUENCE の使用法の概要。
---

# 表示シーケンスの作成 {#show-create-sequence}

`SHOW CREATE SEQUENCE` `SHOW CREATE TABLE`と同様にシーケンスの詳細情報を表示します。

## 概要 {#synopsis}

```ebnf+diagram
ShowCreateSequenceStmt ::=
    "SHOW" "CREATE" "SEQUENCE" ( SchemaName "." )? TableName
```

## 例 {#examples}

```sql
CREATE SEQUENCE seq;
```

    Query OK, 0 rows affected (0.03 sec)

```sql
SHOW CREATE SEQUENCE seq;
```

    +-------+----------------------------------------------------------------------------------------------------------------------------+
    | Table | Create Table                                                                                                               |
    +-------+----------------------------------------------------------------------------------------------------------------------------+
    | seq   | CREATE SEQUENCE `seq` start with 1 minvalue 1 maxvalue 9223372036854775806 increment by 1 cache 1000 nocycle ENGINE=InnoDB |
    +-------+----------------------------------------------------------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## MySQL 互換性 {#mysql-compatibility}

このステートメントは TiDB の拡張機能です。実装は MariaDB で利用可能なシーケンスに基づいてモデル化されています。

## 参照 {#see-also}

-   [シーケンスを作成](/sql-statements/sql-statement-create-sequence.md)
-   [シーケンスの変更](/sql-statements/sql-statement-alter-sequence.md)
-   [ドロップシーケンス](/sql-statements/sql-statement-drop-sequence.md)
