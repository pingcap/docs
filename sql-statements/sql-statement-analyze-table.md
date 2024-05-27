---
title: ANALYZE | TiDB SQL Statement Reference
summary: TiDB データベースに対する ANALYZE の使用法の概要。
---

# 分析する {#analyze}

このステートメントは、TiDB がテーブルとインデックスに構築する統計を更新します。レコードの大規模なバッチ更新またはインポートを実行した後、またはクエリ実行プランが最適ではないことに気付いた場合は、 `ANALYZE`実行することをお勧めします。

TiDB は、統計が自身の推定値と一致しないことを発見すると、時間の経過とともに統計を自動的に更新します。

現在、TiDB は`ANALYZE TABLE`ステートメントを使用して完全なコレクションとして統計情報を収集します。詳細については、 [統計学入門](/statistics.md)を参照してください。

## 概要 {#synopsis}

```ebnf+diagram
AnalyzeTableStmt ::=
    'ANALYZE' ( 'TABLE' ( TableNameList ( 'ALL COLUMNS' | 'PREDICATE COLUMNS' ) | TableName ( 'INDEX' IndexNameList? | AnalyzeColumnOption | 'PARTITION' PartitionNameList ( 'INDEX' IndexNameList? | AnalyzeColumnOption )? )? ) 'INDEX' IndexNameList? ) AnalyzeOptionListOpt

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

統計が正しく更新され、読み込まれるようになりました。

## MySQL 互換性 {#mysql-compatibility}

TiDB は、収集する統計と、クエリ実行中に統計を利用する方法の**両方**において MySQL とは異なります。このステートメントは構文的には MySQL に似ていますが、次の違いがあります。

-   `ANALYZE TABLE`実行すると、TiDB は最近コミットされた変更を含まない場合があります。行のバッチ更新後、統計更新にこれらの変更を反映させるには、 `ANALYZE TABLE`実行する前に`sleep(1)`を実行する必要がある場合があります。7 [＃16570](https://github.com/pingcap/tidb/issues/16570)参照してください。
-   `ANALYZE TABLE` 、MySQL よりも TiDB で実行するのに大幅に時間がかかります。

## 参照 {#see-also}

-   [EXPLAIN](/sql-statements/sql-statement-explain.md)
-   [EXPLAIN分析](/sql-statements/sql-statement-explain-analyze.md)
