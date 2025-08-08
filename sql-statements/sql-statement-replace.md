---
title: REPLACE | TiDB SQL Statement Reference
summary: TiDB データベースでの REPLACE の使用法の概要。
---

# 交換する {#replace}

`REPLACE`文は意味的には`DELETE`文と`INSERT`文を組み合わせたものになります。これにより、アプリケーションコードを簡素化できます。

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
> TiDB v6.6.0以降、 [リソース管理](/tidb-resource-control-ru-groups.md)サポートします。この機能を使用すると、異なるリソースグループで異なる優先度のSQL文を実行できます。これらのリソースグループに適切なクォータと優先度を設定することで、優先度の異なるSQL文のスケジュールをより適切に制御できます。リソース制御を有効にすると、文の優先度（ `PriorityOpt` ）は無効になります。異なるSQL文のリソース使用量を管理するには、 [リソース管理](/tidb-resource-control-ru-groups.md)使用することをお勧めします。

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

## MySQLの互換性 {#mysql-compatibility}

TiDBの`REPLACE`文はMySQLと完全に互換性があります。互換性に違いがある場合は、 [バグを報告する](https://docs.pingcap.com/tidb/stable/support)参照してください。

## 参照 {#see-also}

-   [消去](/sql-statements/sql-statement-delete.md)
-   [入れる](/sql-statements/sql-statement-insert.md)
-   [選択](/sql-statements/sql-statement-select.md)
-   [アップデート](/sql-statements/sql-statement-update.md)
