---
title: Index Advisor
summary: TiDB Index Advisorを使用してクエリパフォーマンスを最適化する方法を学びましょう。
---

# インデックスアドバイザー {#index-advisor}

TiDB v8.5.0では、クエリパフォーマンスを向上させるインデックスを推奨することでワークロードを最適化するインデックスアドバイザー機能が導入されました。新しいSQLステートメント`RECOMMEND INDEX`を使用すると、単一のクエリまたはワークロード全体に対してインデックスの推奨事項を生成できます。評価のために物理的にインデックスを作成するというリソース集約型のプロセスを回避するために、TiDBは[仮説的な指標](#hypothetical-indexes)サポートしており、これは具体化されていない論理インデックスです。

> **注記：**
>
> 現在、この機能は[TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

インデックス アドバイザーは、クエリを分析して、 `WHERE` 、 `GROUP BY` 、 `ORDER BY`などの句からインデックス可能な列を特定します。次に、インデックス候補を生成し、仮想インデックスを使用してパフォーマンス上のメリットを推定します。TiDB は、遺伝的探索アルゴリズムを使用して最適なインデックスセットを選択します。まず単一列のインデックスから始め、複数列のインデックスを反復的に探索し、「What-If」分析を活用して、オプティマイザ プランのコストへの影響に基づいて潜在的なインデックスを評価します。アドバイザーは、インデックスを使用せずにクエリを実行する場合と比較して、インデックスによって全体のコストが削減される場合に、インデックスを推奨します。

[新しい指標を推奨する](#recommend-indexes-using-the-recommend-index-statement)ことに加えて、インデックスアドバイザーは効率的なインデックス管理を確保するために[非アクティブなインデックスの削除](#remove-unused-indexes)も提案します。

## <code>RECOMMEND INDEX</code>ステートメントを使用してインデックスを推奨します。 {#recommend-indexes-using-the-code-recommend-index-code-statement}

TiDB では、インデックス アドバイザ タスク用の`RECOMMEND INDEX` SQL ステートメントが導入されました。 `RUN`サブコマンドは、過去のワークロードを分析し、推奨事項をシステム テーブルに保存します。 `FOR`オプションを使用すると、以前に実行されていない特定の SQL ステートメントを対象にすることができます。さらに、[オプション](#recommend-index-options)の を使用して高度な制御を行うこともできます。構文は次のとおりです。

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>] 
```

### 単一クエリに対する推奨インデックス {#recommend-indexes-for-a-single-query}

次の例は、5,000 行を含むテーブル`t`に対するクエリのインデックス推奨を生成する方法を示しています。簡潔にするため、 `INSERT`ステートメントは省略されています。

```sql
CREATE TABLE t (a INT, b INT, c INT);
RECOMMEND INDEX RUN for "SELECT a, b FROM t WHERE a = 1 AND b = 1"\G
*************************** 1. row ***************************
              database: test
                 table: t
            index_name: idx_a_b
         index_columns: a,b
        est_index_size: 0
                reason: Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t` where `a` = ? and `b` = ?
    top_impacted_query: [{"Query":"SELECT `a`,`b` FROM `test`.`t` WHERE `a` = 1 AND `b` = 1","Improvement":0.999994}]
create_index_statement: CREATE INDEX idx_a_b ON t(a,b);
```

インデックスアドバイザーは`a`と`b`の単一列インデックスを個別に評価し、最終的に最適なパフォーマンスを実現するためにそれらを単一のインデックスに統合します。

以下の`EXPLAIN`の結果は、インデックスなしの場合と、推奨される 2 列の仮想インデックスを使用した場合のクエリ実行を比較したものです。インデックス アドバイザーは、両方のケースを内部的に評価し、コストが最小となるオプションを選択します。インデックス アドバイザーは`a`および`b`上の単一列の仮想インデックスも検討しますが、これらは 2 列のインデックスを組み合わせた場合よりも優れたパフォーマンスを提供しません。簡潔にするため、実行プランは省略しています。

```sql
EXPLAIN FORMAT='VERBOSE' SELECT a, b FROM t WHERE a=1 AND b=1;

+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| id                      | estRows | estCost    | task      | access object | operator info                    |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01    | 196066.71  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01    | 2941000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 5000.00 | 2442000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+---------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='VERBOSE' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.05    | 1.10    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.05    | 10.18   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

### ワークロードに適したインデックスを推奨する {#recommend-indexes-for-a-workload}

次の例は、ワークロード全体に対するインデックス推奨事項を生成する方法を示しています。テーブル`t1`と`t2`にはそれぞれ 5,000 行のデータが含まれていると仮定します。

```sql
CREATE TABLE t1 (a INT, b INT, c INT, d INT);
CREATE TABLE t2 (a INT, b INT, c INT, d INT);

-- Run some queries in this workload.
SELECT a, b FROM t1 WHERE a=1 AND b<=5;
SELECT d FROM t1 ORDER BY d LIMIT 10;
SELECT * FROM t1, t2 WHERE t1.a=1 AND t1.d=t2.d;

RECOMMEND INDEX RUN;
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| database | table | index_name | index_columns | est_index_size | reason                                                                                                                                                                | top_impacted_query                                                                                                                                                                                                              | create_index_statement           |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
| test     | t1    | idx_a_b    | a,b           | 19872      | Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?                                    | [{"Query":"SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` \u003c= 5","Improvement":0.998214},{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.336837}] | CREATE INDEX idx_a_b ON t1(a,b); |
| test     | t1    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?                                                  | [{"Query":"SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10","Improvement":0.999433}]                                                                                                                                          | CREATE INDEX idx_d ON t1(d);     |
| test     | t2    | idx_d      | d             | 9936       | Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d` | [{"Query":"SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`","Improvement":0.638567}]                                                                                                    | CREATE INDEX idx_d ON t2(d);     |
+----------+-------+------------+---------------+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------+
```

この場合、インデックスアドバイザーは、単一のクエリではなく、ワークロード全体に対して最適なインデックスを特定します。ワークロードクエリは、TiDBシステムテーブル`INFORMATION_SCHEMA.STATEMENTS_SUMMARY`から取得されます。

このテーブルには数万から数十万ものクエリが含まれる可能性があり、インデックスアドバイザーのパフォーマンスに影響を与える可能性があります。この問題を解決するため、インデックスアドバイザーは実行頻度の高いクエリを優先します。これらのクエリはワークロード全体のパフォーマンスに大きな影響を与えるためです。デフォルトでは、インデックスアドバイザーは上位1,000件のクエリを選択します。この値は、 [`max_num_query`](#recommend-index-options)パラメーターを使用して調整できます。

`RECOMMEND INDEX`ステートメントの結果は`mysql.index_advisor_results`テーブルに格納されます。このテーブルをクエリして、推奨インデックスを表示できます。次の例は、前の 2 つの`RECOMMEND INDEX`ステートメントの実行後のこのシステム テーブルの内容を示しています。

```sql
SELECT * FROM mysql.index_advisor_results;
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
| id | created_at          | updated_at          | schema_name | table_name | index_name | index_columns | index_details                                                                                                                                                                                       | top_impacted_queries                                                                                                                                                                                                              | workload_impact                   | extra |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
|  1 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_a_b    | a,b           | {"IndexSize": 0, "Reason": "Column [a b] appear in Equal or Range Predicate clause(s) in query: select `a` , `b` from `test` . `t1` where `a` = ? and `b` <= ?"}                                    | [{"Improvement": 0.998214, "Query": "SELECT `a`,`b` FROM `test`.`t1` WHERE `a` = 1 AND `b` <= 5"}, {"Improvement": 0.337273, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}] | {"WorkloadImprovement": 0.395235} | NULL  |
|  2 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t1         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select `d` from `test` . `t1` order by `d` limit ?"}                                                  | [{"Improvement": 0.999715, "Query": "SELECT `d` FROM `test`.`t1` ORDER BY `d` LIMIT 10"}]                                                                                                                                         | {"WorkloadImprovement": 0.225116} | NULL  |
|  3 | 2024-12-10 11:44:45 | 2024-12-10 11:44:45 | test        | t2         | idx_d      | d             | {"IndexSize": 0, "Reason": "Column [d] appear in Equal or Range Predicate clause(s) in query: select * from ( `test` . `t1` ) join `test` . `t2` where `t1` . `a` = ? and `t1` . `d` = `t2` . `d`"} | [{"Improvement": 0.639393, "Query": "SELECT * FROM (`test`.`t1`) JOIN `test`.`t2` WHERE `t1`.`a` = 1 AND `t1`.`d` = `t2`.`d`"}]                                                                                                   | {"WorkloadImprovement": 0.365871} | NULL  |
+----+---------------------+---------------------+-------------+------------+------------+---------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------+-------+
```

### <code>RECOMMEND INDEX</code>オプションの推奨 {#code-recommend-index-code-options}

`RECOMMEND INDEX`ステートメントのオプションを設定および表示して、ワークロードに合わせて動作を微調整するには、次のようにします。

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

以下のオプションが利用可能です。

-   `timeout` : `RECOMMEND INDEX`コマンドの実行に許容される最大時間を指定します。
-   `max_num_index` : `RECOMMEND INDEX`の結果に含めるインデックスの最大数を指定します。
-   `max_index_columns` : 結果の複数列インデックスで許可される最大列数を指定します。
-   `max_num_query` : ステートメントサマリーワークロードから選択するクエリの最大数を指定します。

現在のオプション設定を確認するには、 `RECOMMEND INDEX SHOW OPTION`ステートメントを実行してください。

```sql
RECOMMEND INDEX SHOW OPTION;
+-------------------+-------+---------------------------------------------------------+
| option            | value | description                                             |
+-------------------+-------+---------------------------------------------------------+
| max_num_index     | 5     | The maximum number of indexes to recommend.             |
| max_index_columns | 3     | The maximum number of columns in an index.              |
| max_num_query     | 1000  | The maximum number of queries to recommend indexes.     |
| timeout           | 30s   | The timeout of index advisor.                           |
+-------------------+-------+---------------------------------------------------------+
4 rows in set (0.00 sec)
```

オプションを変更するには、 `RECOMMEND INDEX SET`ステートメントを使用します。たとえば、 `timeout`オプションを変更するには、次のように記述します。

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### 制限事項 {#limitations}

インデックス推奨機能には、以下の制限事項があります。

-   現在、[準備された声明](/develop/dev-guide-prepared-statement.md)ステートメントはサポートされていません。 `RECOMMEND INDEX RUN`ステートメントは`Prepare`および`Execute`プロトコルを介して実行されるクエリに対してインデックスを推奨することはできません。
-   現時点では、インデックスの削除に関する推奨事項は提供されていません。
-   現在、インデックスアドバイザーのユーザーインターフェース（UI）はまだ提供されていません。

## 使用されていないインデックスを削除する {#remove-unused-indexes}

バージョン8.0.0以降では、 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)と[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)を使用して、ワークロード内の非アクティブなインデックスを特定できます。これらのインデックスを削除することで、storage容量を節約し、オーバーヘッドを削減できます。本番環境では、対象のインデックスを完全に削除する前に、まず非表示にして、1回の業務サイクルにわたって影響を確認することを強くお勧めします。

### <code>sys.schema_unused_indexes</code>を使用します {#use-code-sys-schema-unused-indexes-code}

[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)ビューは、すべての TiDB インスタンスの最後の起動以降に使用されていないインデックスを識別します。このビューは、スキーマ、テーブル、および列情報を含むシステム テーブルに基づいており、スキーマ、テーブル、およびインデックス名を含む、各インデックスの完全な仕様を提供します。このビューを照会することで、どのインデックスを非表示にするか、または削除するかを決定できます。

> **警告：**
>
> `sys.schema_unused_indexes`ビューは、すべての TiDB インスタンスの最後の起動以降に使用されていないインデックスを表示するため、TiDB インスタンスが十分な時間稼働していることを確認してください。そうでない場合、特定のワークロードがまだ実行されていないと、ビューに誤った候補が表示される可能性があります。すべての TiDB インスタンスの稼働時間を確認するには、次の SQL クエリを使用してください。
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### <code>INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE</code>を使用してください。 {#use-code-information-schema-cluster-tidb-index-usage-code}

[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)テーブルには、選択バケット、最終アクセス時刻、アクセスされた行数などのメトリックが格納されています。以下の例は、このテーブルに基づいて未使用または非効率なインデックスを特定するクエリを示しています。

```sql
-- Find indexes that have not been accessed in the last 30 days.
SELECT table_schema, table_name, index_name, last_access_time
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NULL
  OR last_access_time < NOW() - INTERVAL 30 DAY;

-- Find indexes that are consistently scanned with over 50% of total records.
SELECT table_schema, table_name, index_name,
       query_total, rows_access_total,
       percentage_access_0 as full_table_scans
FROM information_schema.cluster_tidb_index_usage
WHERE last_access_time IS NOT NULL AND percentage_access_0 + percentage_access_0_1 + percentage_access_1_10 + percentage_access_10_20 + percentage_access_20_50 = 0;
```

> **注記：**
>
> `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`のデータは最大 5 分遅延する可能性があり、TiDB ノードが再起動されるたびに使用状況データはリセットされます。また、インデックスの使用状況は、テーブルに有効な統計情報がある場合にのみ記録されます。

## 仮説的な指標 {#hypothetical-indexes}

仮説インデックス（Hypo Indexes）は、 `CREATE INDEX`ステートメントではなく、 のような SQL コメントを使用して作成されます。この方法により[クエリヒント](/optimizer-hints.md)インデックスを物理的に作成するオーバーヘッドなしに、軽量なインデックス実験が可能になります。

例えば、 `/*+ HYPO_INDEX(t, idx_ab, a, b) */`コメントは、クエリ プランナーに対し、 `idx_ab`テーブル上に、 `t`に対して、 `a` `b`名前の仮想インデックスを作成するように指示します。プランナーはインデックスのメタデータを生成しますが、物理的にインデックスを作成することはありません。該当する場合、プランナーはインデックス作成に伴うコストを発生させることなく、クエリ最適化中にこの仮想インデックスを考慮します。

`RECOMMEND INDEX`アドバイザーは、仮説的なインデックスを使用して「もしも」分析を行い、さまざまなインデックスの潜在的なメリットを評価します。また、仮説的なインデックスを直接使用して、インデックスを作成する前にインデックス設計を試すこともできます。

次の例は、架空のインデックスを使用したクエリを示しています。

```sql
CREATE TABLE t(a INT, b INT, c INT);
Query OK, 0 rows affected (0.02 sec)

EXPLAIN FORMAT='verbose' SELECT a, b FROM t WHERE a=1 AND b=1;
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| id                      | estRows  | estCost    | task      | access object | operator info                    |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+
| TableReader_7           | 0.01     | 392133.42  | root      |               | data:Selection_6                 |
| └─Selection_6           | 0.01     | 5882000.00 | cop[tikv] |               | eq(test.t.a, 1), eq(test.t.b, 1) |
|   └─TableFullScan_5     | 10000.00 | 4884000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo   |
+-------------------------+----------+------------+-----------+---------------+----------------------------------+

EXPLAIN FORMAT='verbose' SELECT /*+ HYPO_INDEX(t, idx_ab, a, b) */ a, b FROM t WHERE a=1 AND b=1;
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| id                     | estRows | estCost | task      | access object               | operator info                                   |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
| IndexReader_6          | 0.10    | 2.20    | root      |                             | index:IndexRangeScan_5                          |
| └─IndexRangeScan_5     | 0.10    | 20.35   | cop[tikv] | table:t, index:idx_ab(a, b) | range:[1 1,1 1], keep order:false, stats:pseudo |
+------------------------+---------+---------+-----------+-----------------------------+-------------------------------------------------+
```

この例では、 `HYPO_INDEX`コメントで、仮想的なインデックスが指定されています。このインデックスを使用すると、テーブル全体のスキャン ({ `2.20` `392133.42`の代わりにインデックス範囲スキャン ( `IndexRangeScan` } から`TableFullScan` } に削減されます。

TiDBは、ワークロード内のクエリに基づいて、ワークロードにメリットをもたらす可能性のあるインデックス候補を自動的に生成します。仮想インデックスを使用して潜在的なメリットを推定し、最も効果的なインデックスを推奨します。
