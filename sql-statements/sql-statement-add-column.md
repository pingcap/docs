---
title: ADD COLUMN | TiDB SQL Statement Reference
summary: TiDB データベースの ADD COLUMN の使用法の概要。
---

# 列を追加 {#add-column}

`ALTER TABLE.. ADD COLUMN`文は既存のテーブルに列を追加します。この操作は TiDB ではオンラインで実行されるため、列の追加によってテーブルへの読み取りも書き込みもブロックされることはありません。

## 概要 {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddColumnSpec ( ',' AddColumnSpec )*

TableName ::=
    Identifier ('.' Identifier)?

AddColumnSpec
         ::= 'ADD' 'COLUMN' 'IF NOT EXISTS'? ColumnName ColumnType ColumnOption+ ( 'FIRST' | 'AFTER' ColumnName )?

ColumnType
         ::= NumericType
           | StringType
           | DateAndTimeType
           | 'SERIAL'

ColumnOption
         ::= 'NOT'? 'NULL'
           | 'AUTO_INCREMENT'
           | 'PRIMARY'? 'KEY' ( 'CLUSTERED' | 'NONCLUSTERED' )? ( 'GLOBAL' | 'LOCAL' )?
           | 'UNIQUE' 'KEY'? ( 'GLOBAL' | 'LOCAL' )?
           | 'DEFAULT' ( NowSymOptionFraction | SignedLiteral | NextValueForSequence )
           | 'SERIAL' 'DEFAULT' 'VALUE'
           | 'ON' 'UPDATE' NowSymOptionFraction
           | 'COMMENT' stringLit
           | ( 'CONSTRAINT' Identifier? )? 'CHECK' '(' Expression ')' ( 'NOT'? ( 'ENFORCED' | 'NULL' ) )?
           | 'GENERATED' 'ALWAYS' 'AS' '(' Expression ')' ( 'VIRTUAL' | 'STORED' )?
           | 'REFERENCES' TableName ( '(' IndexPartSpecificationList ')' )? Match? OnDeleteUpdateOpt
           | 'COLLATE' CollationName
           | 'COLUMN_FORMAT' ColumnFormat
           | 'STORAGE' StorageMedia
           | 'AUTO_RANDOM' ( '(' LengthNum ')' )?
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> SELECT * FROM t1;
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD COLUMN c1 INT NOT NULL;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+
| id | c1 |
+----+----+
|  1 |  0 |
+----+----+
1 row in set (0.00 sec)

mysql> ALTER TABLE t1 ADD c2 INT NOT NULL AFTER c1;
Query OK, 0 rows affected (0.28 sec)

mysql> SELECT * FROM t1;
+----+----+----+
| id | c1 | c2 |
+----+----+----+
|  1 |  0 |  0 |
+----+----+----+
1 row in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   新しい列を追加してそれを`PRIMARY KEY`に設定することはサポートされていません。
-   新しい列を追加して`AUTO_INCREMENT`に設定することはサポートされていません。
-   生成された列の追加には制限があります[生成された列の制限](/generated-columns.md#limitations)を参照してください。
-   新しい列を追加するときに`PRIMARY KEY`または`UNIQUE INDEX`を`GLOBAL`として指定して[グローバルインデックス](/global-indexes.md)設定することは、 [パーティションテーブル](/partitioned-table.md)の TiDB 拡張であり、MySQL と互換性がありません。

## 参照 {#see-also}

-   [インデックスを追加](/sql-statements/sql-statement-add-index.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
