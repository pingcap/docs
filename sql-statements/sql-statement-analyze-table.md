---
title: ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of ANALYZE for the TiDB database.
---

# 分析する {#analyze}

このステートメントは、TiDBがテーブルとインデックスに基づいて構築する統計を更新します。大規模なバッチ更新またはレコードのインポートを実行した後、またはクエリ実行計画が最適ではないことに気付いた場合は、 `ANALYZE`を実行することをお勧めします。

TiDBはまた、統計が自身の推定値と矛盾していることを発見すると、時間の経過とともに統計を自動的に更新します。

現在、TiDBは、完全収集（ `ANALYZE TABLE`ステートメントを使用して実装）と増分収集（ `ANALYZE INCREMENTAL TABLE`ステートメントを使用して実装）の2つの方法で統計情報を収集します。これら2つのステートメントの詳細な使用法については、 [統計入門](/statistics.md)を参照してください。

## あらすじ {#synopsis}

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' ) | TableName ( 'INDEX' IndexNameList? | AnalyzeColumnOption | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList? | AnalyzeColumnOption )? )? ) | 'INCREMENTAL' 'TABLE' TableName ( 'PARTITION' PartitionNameList )? 'INDEX' IndexNameList? ) AnalyzeOptionListOpt

AnalyzeOptionListOpt ::=
( WITH AnalyzeOptionList )?

AnalyzeOptionList ::=
AnalyzeOption ( ',' AnlyzeOption )*

AnalyzeOption ::=
( NUM ( 'BUCKETS' | 'TOPN' | ( 'CMSKETCH' ( 'DEPTH' | 'WIDTH' ) ) | 'SAMPLES' ) ) | ( FLOATNUM 'SAMPLERATE' )

AnalyzeColumnOption ::=
( 'ALL COLUMNS' | 'PREDICATE COLUMNS' | 'COLUMNS' ColumnNameList )

TableNameList ::=
    TableName (',' TableName)*

TableName ::=
    Identifier ( '.' Identifier )?

ColumnNameList ::=
    Identifier ( ',' Identifier )*

IndexNameList ::=
    Identifier ( ',' Identifier )*

PartitionNameList ::=
    Identifier ( ',' Identifier )*
```

## 例 {#examples}

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, c1 INT NOT NULL);
Query OK, 0 rows affected (0.11 sec)

mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)

mysql> analyze table t1;
Query OK, 0 rows affected (0.13 sec)

mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+-------------------------------+
| id                     | estRows | task      | access object          | operator info                 |
+------------------------+---------+-----------+------------------------+-------------------------------+
| IndexReader_6          | 1.00    | root      |                        | index:IndexRangeScan_5        |
| └─IndexRangeScan_5     | 1.00    | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false |
+------------------------+---------+-----------+------------------------+-------------------------------+
2 rows in set (0.00 sec)
```

## MySQLの互換性 {#mysql-compatibility}

TiDBは、収集する統計とクエリ実行中に統計を利用する方法の**両方**でMySQLとは異なります。このステートメントは構文的にMySQLに似ていますが、次の違いが適用されます。

1.  TiDBは、 `ANALYZE TABLE`を実行しているときに、ごく最近コミットされた変更を含まない場合があります。行のバッチ更新後、統計更新にこれらの変更を反映させるために、 `ANALYZE TABLE`を実行する前に`sleep(1)`を実行する必要がある場合があります。 [＃16570](https://github.com/pingcap/tidb/issues/16570) 。
2.  `ANALYZE TABLE`は、MySQLよりもTiDBでの実行にかなり長い時間がかかります。このパフォーマンスの違いは、 `SET GLOBAL tidb_enable_fast_analyze=1`で高速分析を有効にすることで部分的に軽減できます。高速分析はサンプリングを利用するため、統計の精度が低下します。その使用法はまだ実験的と見なされます。

MySQLは`ANALYZE INCREMENTAL TABLE`ステートメントをサポートしていません。 TiDBは、統計の増分収集をサポートしています。詳細な使用法については、 [インクリメンタルコレクション](/statistics.md#incremental-collection)を参照してください。

## も参照してください {#see-also}

-   [説明](/sql-statements/sql-statement-explain.md)
-   [説明分析](/sql-statements/sql-statement-explain-analyze.md)
