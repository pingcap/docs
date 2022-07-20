---
title: ADD INDEX | TiDB SQL Statement Reference
summary: An overview of the usage of ADD INDEX for the TiDB database.
---

# インデックスを追加 {#add-index}

`ALTER TABLE.. ADD INDEX`ステートメントは、既存のテーブルにインデックスを追加します。この操作はTiDBでオンラインです。つまり、インデックスを追加しても、テーブルへの読み取りも書き込みもブロックされません。

> **警告：**
>
> -   DDLステートメントがクラスタで実行されているときは**TiDB**クラスタをアップグレードしないでください（通常、 `ADD INDEX`などの時間のかかるDDLステートメントや列タイプの変更の場合）。
> -   アップグレードする前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDBクラスタに進行中のDDLジョブがあるかどうかを確認することをお勧めします。クラスタにDDLジョブがある場合、クラスタをアップグレードするには、DDLの実行が終了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用してDDLジョブをキャンセルしてからクラスタをアップグレードします。
> -   さらに、クラスタのアップグレード中は、DDLステートメントを実行し**ない**でください。そうしないと、未定義動作の問題が発生する可能性があります。

## あらすじ {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'

IndexType
         ::= 'BTREE'
           | 'HASH'
           | 'RTREE'
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+-------------------------+----------+-----------+---------------+--------------------------------+
| id                      | estRows  | task      | access object | operator info                  |
+-------------------------+----------+-----------+---------------+--------------------------------+
| TableReader_7           | 10.00    | root      |               | data:Selection_6               |
| └─Selection_6           | 10.00    | cop[tikv] |               | eq(test.t1.c1, 3)              |
|   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo |
+-------------------------+----------+-----------+---------------+--------------------------------+
3 rows in set (0.00 sec)

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 0.01    | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 0.01    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

-   `FULLTEXT` 、および`HASH`のインデックスはサポートさ`SPATIAL`ていません。
-   降順インデックスはサポートされていません（ MySQL 5.7と同様）。
-   現在、複数のインデックスを同時に追加することはサポートされていません。
-   `CLUSTERED`タイプの主キーをテーブルに追加することはサポートされていません。 `CLUSTERED`タイプの主キーの詳細については、 [クラスター化されたインデックス](/clustered-indexes.md)を参照してください。

## も参照してください {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
-   [ドロップインデックス](/sql-statements/sql-statement-drop-index.md)
-   [インデックスの名前を変更](/sql-statements/sql-statement-rename-index.md)
-   [ALTER INDEX](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
