---
title: ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of ANALYZE for the TiDB database.
---

# 分析する {#analyze}

このステートメントは、TiDB がテーブルとインデックスで構築する統計を更新します。大規模なバッチ更新またはレコードのインポートを実行した後、またはクエリ実行プランが最適ではないことに気付いた場合は、 `ANALYZE`実行することをお勧めします。

また、TiDB は、統計が独自の見積もりと矛盾していることを発見すると、時間の経過とともに統計を自動的に更新します。

現在、TiDB は 2 つの方法で統計情報を収集します。完全収集 ( `ANALYZE TABLE`ステートメントを使用して実装) と増分収集 ( `ANALYZE INCREMENTAL TABLE`ステートメントを使用して実装) です。これら 2 つのステートメントの詳細な使用方法については、 [統計入門](/statistics.md)を参照してください。

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

## MySQL の互換性 {#mysql-compatibility}

TiDB は、収集する統計と、クエリ実行中に統計を利用する方法の**両方**で、MySQL とは異なります。このステートメントは構文的に MySQL と似ていますが、次の違いがあります。

1.  TiDB は、実行時に最近コミットされた変更を含まない場合があります`ANALYZE TABLE` 。行のバッチ更新の後、これらの変更を統計の更新に反映させるために、 `ANALYZE TABLE`実行する前に`sleep(1)`が必要になる場合があります。 [#16570](https://github.com/pingcap/tidb/issues/16570) .
2.  `ANALYZE TABLE` MySQL よりも TiDB での実行にかなり時間がかかります。このパフォーマンスの違いは、 `SET GLOBAL tidb_enable_fast_analyze=1`で高速分析を有効にすることで部分的に軽減できます。高速分析ではサンプリングが使用されるため、統計の精度が低下します。その使用法はまだ実験的と考えられています。

MySQL は`ANALYZE INCREMENTAL TABLE`ステートメントをサポートしていません。 TiDB は、統計の増分収集をサポートしています。詳しい使い方は[増分コレクション](/statistics.md#incremental-collection)を参照してください。

## こちらもご覧ください {#see-also}

-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [EXPLAIN分析する](/sql-statements/sql-statement-explain-analyze.md)
