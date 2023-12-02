---
title: ANALYZE | TiDB SQL Statement Reference
summary: An overview of the usage of ANALYZE for the TiDB database.
---

# 分析する {#analyze}

このステートメントは、TiDB がテーブルとインデックスに基づいて構築する統計を更新します。大規模なバッチ更新またはレコードのインポートを実行した後、またはクエリ実行プランが最適ではないことに気付いた場合は、 `ANALYZE`実行することをお勧めします。

TiDB はまた、統計が独自の推定値と矛盾していることを発見すると、時間の経過とともに自動的に統計を更新します。

現在、TiDB は`ANALYZE TABLE`ステートメントを使用して統計情報を完全なコレクションとして収集します。詳細については、 [統計学入門](/statistics.md)を参照してください。

## あらすじ {#synopsis}

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' ) | TableName ( 'INDEX' IndexNameList? | AnalyzeColumnOption | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList? | AnalyzeColumnOption )? )? ) | 'INCREMENTAL' 'TABLE' TableName ( 'PARTITION' PartitionNameList )? 'INDEX' IndexNameList? ) AnalyzeOptionListOpt

AnalyzeOptionListOpt ::=
( WITH AnalyzeOptionList )?

AnalyzeOptionList ::=
AnalyzeOption ( ',' AnalyzeOption )*

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
```

```sql
mysql> INSERT INTO t1 (c1) VALUES (1),(2),(3),(4),(5);
Query OK, 5 rows affected (0.03 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

```sql
mysql> ALTER TABLE t1 ADD INDEX (c1);
Query OK, 0 rows affected (0.30 sec)
```

```sql
mysql> EXPLAIN SELECT * FROM t1 WHERE c1 = 3;
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| id                     | estRows | task      | access object          | operator info                               |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
| IndexReader_6          | 10.00   | root      |                        | index:IndexRangeScan_5                      |
| └─IndexRangeScan_5     | 10.00   | cop[tikv] | table:t1, index:c1(c1) | range:[3,3], keep order:false, stats:pseudo |
+------------------------+---------+-----------+------------------------+---------------------------------------------+
2 rows in set (0.00 sec)
```

現在の統計のステータスは`pseudo`です。これは、統計が不正確であることを意味します。

```sql
mysql> ANALYZE TABLE t1;
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

統計が正しく更新され、ロードされるようになりました。

## MySQLの互換性 {#mysql-compatibility}

TiDB は、収集する統計とクエリ実行中の統計の利用方法の**両方**において MySQL とは異なります。このステートメントは構文的には MySQL と似ていますが、次のような違いがあります。

-   TiDB には、 `ANALYZE TABLE`の実行時に最近コミットされた変更が含まれていない可能性があります。行のバッチ更新後、統計の更新にこれらの変更を反映させるには、 `ANALYZE TABLE`実行する前に`sleep(1)`を実行する必要がある場合があります。 [#16570](https://github.com/pingcap/tidb/issues/16570)を参照してください。
-   `ANALYZE TABLE` TiDB での実行に MySQL よりも大幅に時間がかかります。

## こちらも参照 {#see-also}

-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [EXPLAINの説明](/sql-statements/sql-statement-explain-analyze.md)
