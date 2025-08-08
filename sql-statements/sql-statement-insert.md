---
title: INSERT | TiDB SQL Statement Reference
summary: TiDB データベースでの INSERT の使用法の概要。
---

# 入れる {#insert}

このステートメントは、テーブルに新しい行を挿入します。

## 概要 {#synopsis}

```ebnf+diagram
InsertIntoStmt ::=
    'INSERT' TableOptimizerHints PriorityOpt IgnoreOptional IntoOpt TableName PartitionNameListOpt InsertValues OnDuplicateKeyUpdate

TableOptimizerHints ::=
    hintComment?

PriorityOpt ::=
    ( 'LOW_PRIORITY' | 'HIGH_PRIORITY' | 'DELAYED' )?

IgnoreOptional ::=
    'IGNORE'?

IntoOpt  ::= 'INTO'?

TableName ::=
    Identifier ( '.' Identifier )?

PartitionNameListOpt ::=
    ( 'PARTITION' '(' Identifier ( ',' Identifier )* ')' )?

InsertValues ::=
    '(' ( ColumnNameListOpt ')' ( ValueSym ValuesList | SelectStmt | '(' SelectStmt ')' | UnionStmt ) | SelectStmt ')' )
|   ValueSym ValuesList
|   SelectStmt
|   UnionStmt
|   'SET' ColumnSetValue? ( ',' ColumnSetValue )*

OnDuplicateKeyUpdate ::=
    ( 'ON' 'DUPLICATE' 'KEY' 'UPDATE' AssignmentList )?
```

> **注記：**
>
> TiDB v6.6.0以降、 [リソース管理](/tidb-resource-control-ru-groups.md)サポートします。この機能を使用すると、異なるリソースグループで異なる優先度のSQL文を実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、優先度の異なるSQL文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度（ `PriorityOpt` ）は無効になります。異なるSQL文のリソース使用量を管理するには、 [リソース管理](/tidb-resource-control-ru-groups.md)使用することをお勧めします。

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (a INT);
Query OK, 0 rows affected (0.11 sec)

mysql> CREATE TABLE t2 LIKE t1;
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO t1 (a) VALUES (1);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t2 SELECT * FROM t1;
Query OK, 2 rows affected (0.01 sec)
Records: 2  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+------+
| a    |
+------+
|    1 |
|    1 |
+------+
2 rows in set (0.00 sec)

mysql> SELECT * FROM t2;
+------+
| a    |
+------+
|    1 |
|    1 |
+------+
2 rows in set (0.00 sec)

mysql> INSERT INTO t2 VALUES (2),(3),(4);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t2;
+------+
| a    |
+------+
|    1 |
|    1 |
|    2 |
|    3 |
|    4 |
+------+
5 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBの`INSERT`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [消去](/sql-statements/sql-statement-delete.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
-   [交換する](/sql-statements/sql-statement-replace.md)
