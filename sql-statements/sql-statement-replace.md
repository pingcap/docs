---
title: REPLACE | TiDB SQL Statement Reference
summary: TiDB データベースでの REPLACE の使用法の概要。
---

# 交換する {#replace}

`REPLACE`ステートメントは意味的には`DELETE` + `INSERT`ステートメントを組み合わせたものです。これを使用して、アプリケーション コードを簡素化できます。

## 概要 {#synopsis}

```ebnf+diagram
ReplaceIntoStmt ::=
    'REPLACE' PriorityOpt IntoOpt TableName PartitionNameListOpt InsertValues

PriorityOpt ::=
    ( 'LOW_PRIORITY' | 'HIGH_PRIORITY' | 'DELAYED' )?

IntoOpt ::= 'INTO'?

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
```

> **注記：**
>
> v6.6.0 以降、TiDB は[リソース管理](/tidb-resource-control.md)サポートします。この機能を使用すると、異なるリソース グループで異なる優先度の SQL 文を実行できます。これらのリソース グループに適切なクォータと優先度を設定することで、異なる優先度の SQL 文のスケジュール制御を向上させることができます。リソース制御を有効にすると、文の優先度 ( `PriorityOpt` ) は無効になります。異なる SQL 文のリソース使用を管理するには、 [リソース管理](/tidb-resource-control.md)使用することをお勧めします。

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.12 sec)

mysql> INSERT INTO t1 (c1) VALUES (1), (2), (3);
Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 |  3 |
+----+----+
3 rows in set (0.00 sec)

mysql> REPLACE INTO t1 (id, c1) VALUES(3, 99);
Query OK, 2 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  1 |
|  2 |  2 |
|  3 | 99 |
+----+----+
3 rows in set (0.00 sec)
```

## MySQL 互換性 {#mysql-compatibility}

TiDB の`REPLACE`ステートメントは MySQL と完全に互換性があります。互換性の違いが見つかった場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support) 。

## 参照 {#see-also}

-   [消去](/sql-statements/sql-statement-delete.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
