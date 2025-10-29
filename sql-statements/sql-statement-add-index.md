---
title: ADD INDEX | TiDB SQL Statement Reference
summary: TiDB データベースの ADD INDEX の使用法の概要。
---

# インデックスを追加 {#add-index}

`ALTER TABLE.. ADD INDEX`文は既存のテーブルにインデックスを追加します。この操作は TiDB ではオンラインで実行されるため、インデックスの追加によってテーブルへの読み取りも書き込みもブロックされることはありません。

> **ヒント：**
>
> [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)使用すると、このステートメントの操作を高速化できます。

<CustomContent platform="tidb-cloud">

> **注記：**
>
> 4つのvCPUを搭載したクラスタ[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)の場合、インデックス作成時にリソース制限がクラスタの安定性に影響を与えないように、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)手動で無効にすることをお勧めします。この設定を無効にすると、トランザクションを使用してインデックスを作成できるようになり、クラスタ全体への影響が軽減されます。

</CustomContent>

<CustomContent platform="tidb">

> **警告：**
>
> -   クラスター内で DDL ステートメントが実行されているときは、TiDB クラスターをアップグレードし**ないでください**(通常は、 `ADD INDEX`や列タイプの変更などの時間のかかる DDL ステートメントの場合)。
> -   アップグレード前に、 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-admin-show-ddl.md)コマンドを使用して、TiDB クラスターで実行中の DDL ジョブがあるかどうかを確認することをお勧めします。クラスターに DDL ジョブがある場合は、クラスターをアップグレードする前に、DDL の実行が完了するまで待つか、 [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md)コマンドを使用して DDL ジョブをキャンセルしてください。
> -   また、クラスタのアップグレード中は、DDL文を実行し**ないでください**。そうしないと、未定義の動作が発生する可能性があります。
>
> TiDBをv7.1.0からそれ以降のバージョンにアップグレードする場合、上記の制限は無視できます。詳細については、 [TiDBスムーズアップグレードの制限](/smooth-upgrade-tidb.md)参照してください。

</CustomContent>

## 概要 {#synopsis}

```ebnf+diagram
AlterTableStmt
         ::= 'ALTER' 'IGNORE'? 'TABLE' TableName AddIndexSpec ( ',' AddIndexSpec )*

AddIndexSpec
         ::= 'ADD' ( ( 'PRIMARY' 'KEY' | ( 'KEY' | 'INDEX' ) 'IF NOT EXISTS'? | 'UNIQUE' ( 'KEY' | 'INDEX' )? ) ( ( Identifier? 'USING' | Identifier 'TYPE' ) IndexType )? | 'FULLTEXT' ( 'KEY' | 'INDEX' )? IndexName ) '(' IndexPartSpecification ( ',' IndexPartSpecification )* ')' IndexOption*

IndexPartSpecification
         ::= ( ColumnName ( '(' LengthNum ')' )? | '(' Expression ')' ) ( 'ASC' | 'DESC' )

IndexOption
         ::= 'KEY_BLOCK_SIZE' '='? LengthNum
           | 'USING' IndexType
           | 'WITH' 'PARSER' Identifier
           | 'COMMENT' stringLit
           | 'VISIBLE'
           | 'INVISIBLE'
           | 'GLOBAL'
           | 'LOCAL'

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

-   TiDB は`RTREE` `BTREE` `HASH`インデックス タイプを受け入れますが、それらを無視します。

-   `SPATIAL`インデックスはサポートされていません。

-   TiDB Self-Managed およびTiDB Cloud Dedicated は、 `FULLTEXT`構文の解析をサポートしますが、 `FULLTEXT`インデックスの使用はサポートしません。

    > **注記：**
    >
    > 現在、特定の AWS リージョンの {{{ .starter }} および {{{ .essential }}} クラスターのみが[`FULLTEXT`構文とインデックス](https://docs.pingcap.com/tidbcloud/vector-search-full-text-search-sql)サポートしています。

-   降順インデックスはサポートされていません ( MySQL 5.7と同様)。

-   `CLUSTERED`型の主キーをテーブルに追加することはサポートされていません。3 型の主キーの詳細については、 `CLUSTERED` [クラスター化インデックス](/clustered-indexes.md)参照してください。

-   `GLOBAL`インデックス オプションを使用して`PRIMARY KEY`または`UNIQUE INDEX` [グローバルインデックス](/partitioned-table.md#global-indexes)として設定することは、 [パーティションテーブル](/partitioned-table.md)の TiDB 拡張であり、MySQL とは互換性がありません。

## 参照 {#see-also}

-   [インデックスの選択](/choose-index.md)
-   [インデックス問題の解決方法](/wrong-index-solution.md)
-   [インデックスの作成](/sql-statements/sql-statement-create-index.md)
-   [インデックスを削除](/sql-statements/sql-statement-drop-index.md)
-   [インデックス名の変更](/sql-statements/sql-statement-rename-index.md)
-   [インデックスの変更](/sql-statements/sql-statement-alter-index.md)
-   [列を追加](/sql-statements/sql-statement-add-column.md)
-   [テーブルの作成](/sql-statements/sql-statement-create-table.md)
-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [TiDB 分散実行フレームワーク (DXF)](/tidb-distributed-execution-framework.md)
