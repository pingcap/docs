---
title: Index Advisor
summary: TiDB Index Advisor を使用してクエリ パフォーマンスを最適化する方法を学習します。
---

# インデックスアドバイザー {#index-advisor}

TiDB v8.5.0では、クエリパフォーマンスを向上させるインデックスを推奨することでワークロードの最適化を支援するIndex Advisor機能が導入されました。新しいSQL文`RECOMMEND INDEX`を使用すると、単一のクエリまたはワークロード全体に対してインデックスの推奨を生成できます。評価のためにインデックスを物理的に作成するというリソースを大量に消費するプロセスを回避するため、TiDBはマテリアライズされない論理インデックスである[仮想インデックス](#hypothetical-indexes)サポートしています。

> **注記：**
>
> 現在、この機能は[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)クラスターでは利用できません。

インデックスアドバイザーはクエリを分析し、 `WHERE` 、 `GROUP BY` 、 `ORDER BY`などの句からインデックス可能な列を特定します。次に、インデックス候補を生成し、仮想インデックスを使用してパフォーマンスの向上を推定します。TiDBは遺伝的探索アルゴリズムを使用して最適なインデックスセットを選択します。まず、単一列インデックスから始めて複数列インデックスを反復的に探索し、「What-If」分析を活用して、オプティマイザプランのコストへの影響に基づいて潜在的なインデックスを評価します。アドバイザーは、インデックスなしでクエリを実行する場合と比較して全体的なコストが削減される場合に、インデックスを推奨します。

効率的なインデックス管理を確実にするために、Index Advisor は[新しいインデックスの推奨](#recommend-indexes-using-the-recommend-index-statement)に加えて[非アクティブなインデックスの削除](#remove-unused-indexes)提案します。

## <code>RECOMMEND INDEX</code>ステートメントを使用してインデックスを推奨する {#recommend-indexes-using-the-code-recommend-index-code-statement}

TiDBでは、インデックスアドバイザータスク用のSQL文`RECOMMEND INDEX`が導入されています。サブコマンド`RUN`は、過去のワークロードを分析し、推奨事項をシステムテーブルに保存します。オプション`FOR`を使用すると、過去に実行されていないSQL文であっても、特定のSQL文をターゲットにすることができます。また、高度な制御のためにオプション[オプション](#recommend-index-options)追加することもできます。構文は次のとおりです。

```sql
RECOMMEND INDEX RUN [ FOR <SQL> ] [<Options>] 
```

### 単一のクエリに対してインデックスを推奨する {#recommend-indexes-for-a-single-query}

次の例は、5,000行を含むテーブル`t`に対するクエリに対して、インデックス推奨を生成する方法を示しています。簡潔にするために、 `INSERT`ステートメントは省略されています。

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

インデックス アドバイザーは、 `a`と`b`単一列インデックスを個別に評価し、最終的にそれらを 1 つのインデックスに結合して、最適なパフォーマンスを実現します。

以下の`EXPLAIN`の結果は、インデックスなしの場合と、推奨される2列の仮想インデックスを使用した場合のクエリ実行を比較したものです。Index Advisorは内部的に両方のケースを評価し、コストが最小となるオプションを選択します。Index Advisorは`a`と`b`についても1列の仮想インデックスを検討しますが、これらは2列の結合インデックスよりも優れたパフォーマンスを提供しません。簡潔にするため、実行プランは省略しています。

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

### ワークロードのインデックスを推奨する {#recommend-indexes-for-a-workload}

次の例は、ワークロード全体に対してインデックスの推奨事項を生成する方法を示しています。テーブル`t1`と`t2`はそれぞれ5,000行が含まれていると仮定します。

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

この場合、インデックスアドバイザーは単一のクエリではなく、ワークロード全体に最適なインデックスを特定します。ワークロードクエリはTiDBシステムテーブル`INFORMATION_SCHEMA.STATEMENTS_SUMMARY`から取得されます。

このテーブルには数万から数十万のクエリが含まれる場合があり、インデックスアドバイザーのパフォーマンスに影響を与える可能性があります。この問題に対処するため、インデックスアドバイザーは、ワークロード全体のパフォーマンスに大きな影響を与える、最も頻繁に実行されるクエリを優先します。デフォルトでは、インデックスアドバイザーは上位1,000件のクエリを選択します。この値は、 [`max_num_query`](#recommend-index-options)パラメータを使用して調整できます。

`RECOMMEND INDEX`のステートメントの結果は`mysql.index_advisor_results`テーブルに保存されます。このテーブルをクエリすることで、推奨されるインデックスを確認できます。次の例は、前の 2 つの`RECOMMEND INDEX`ステートメントを実行した後のこのシステムテーブルの内容を示しています。

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

### <code>RECOMMEND INDEX</code>オプション {#code-recommend-index-code-options}

次のように、 `RECOMMEND INDEX`ステートメントのオプションを設定および表示して、ワークロードに合わせてその動作を微調整できます。

```sql
RECOMMEND INDEX SET <option> = <value>;
RECOMMEND INDEX SHOW OPTION;
```

利用可能なオプションは次のとおりです。

-   `timeout` : `RECOMMEND INDEX`コマンドの実行に許可される最大時間を指定します。
-   `max_num_index` : `RECOMMEND INDEX`の結果に含めるインデックスの最大数を指定します。
-   `max_index_columns` : 結果内の複数列インデックスで許可される列の最大数を指定します。
-   `max_num_query` : ステートメント サマリー ワークロードから選択するクエリの最大数を指定します。

現在のオプション設定を確認するには、 `RECOMMEND INDEX SHOW OPTION`ステートメントを実行します。

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

オプションを変更するには、 `RECOMMEND INDEX SET`ステートメントを使用します。例えば、 `timeout`オプションを変更するには次のようにします。

```sql
RECOMMEND INDEX SET timeout='20s';
Query OK, 1 row affected (0.00 sec)
```

### 制限事項 {#limitations}

インデックス推奨機能には次の制限があります。

-   現在、 [準備された文](/develop/dev-guide-prepared-statement.md)サポートされていません。 `RECOMMEND INDEX RUN`ステートメントは、 `Prepare`および`Execute`プロトコルを介して実行されたクエリのインデックスを推奨できません。
-   現在、インデックスを削除するための推奨事項は提供されていません。
-   現在、Index Advisor のユーザー インターフェイス (UI) はまだ利用できません。

## 未使用のインデックスを削除する {#remove-unused-indexes}

v8.0.0以降のバージョンでは、 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)と[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)使用してワークロード内の非アクティブなインデックスを特定できます。これらのインデックスを削除すると、storage容量を節約し、オーバーヘッドを削減できます。本番環境では、対象のインデックスをまず非表示にし、1つのビジネスサイクル全体にわたって影響を観察した後に、完全に削除することを強くお勧めします。

### <code>sys.schema_unused_indexes</code>を使用する {#use-code-sys-schema-unused-indexes-code}

[`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md)ビューは、すべての TiDB インスタンスの前回の起動以降に使用されていないインデックスを特定します。このビューは、スキーマ、テーブル、列情報を含むシステムテーブルに基づいており、スキーマ、テーブル、インデックス名を含む各インデックスの完全な仕様を提供します。このビューをクエリすることで、どのインデックスを非表示にするか、または削除するかを決定できます。

> **警告：**
>
> `sys.schema_unused_indexes`ビューには、すべての TiDB インスタンスの前回の起動以降に使用されていないインデックスが表示されるため、TiDB インスタンスが十分な時間実行されていることを確認してください。そうでない場合、特定のワークロードがまだ実行されていない場合、ビューに誤った候補が表示される可能性があります。すべての TiDB インスタンスの稼働時間を確認するには、次の SQL クエリを使用してください。
>
> ```sql
> SELECT START_TIME,UPTIME FROM INFORMATION_SCHEMA.CLUSTER_INFO WHERE TYPE='tidb';
> ```

### <code>INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE</code>を使用する {#use-code-information-schema-cluster-tidb-index-usage-code}

[`INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)テーブルは、選択性バケット、最終アクセス時刻、アクセスされた行数などの指標を提供します。次の例は、このテーブルに基づいて未使用または非効率的なインデックスを特定するクエリを示しています。

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
> `INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE`のデータは最大 5 分遅延する可能性があり、使用状況データは TiDB ノードが再起動するたびにリセットされます。また、インデックスの使用状況は、テーブルに有効な統計情報がある場合にのみ記録されます。

## 仮説指標 {#hypothetical-indexes}

仮説インデックス（Hypo Indexes）は、 `CREATE INDEX`ステートメントではなく、 [クエリヒント](/optimizer-hints.md)と同様のSQLコメントを使用して作成されます。このアプローチにより、インデックスを物理的にマテリアライズするオーバーヘッドなしに、軽量な実験が可能になります。

例えば、 `/*+ HYPO_INDEX(t, idx_ab, a, b) */`のコメントは、クエリプランナーに、テーブル`t`列`a`と`b`に`idx_ab`という仮想インデックスを作成するよう指示します。プランナーはインデックスのメタデータを生成しますが、物理的には実現しません。該当する場合、プランナーはクエリの最適化時にこの仮想インデックスを考慮しますが、インデックス作成に伴うコストは発生しません。

`RECOMMEND INDEX`アドバイザーは、仮想インデックスを用いて「What-If」分析を行い、様々なインデックスの潜在的なメリットを評価します。また、仮想インデックスを直接使用して、インデックスの作成に進む前に様々な設計を試すこともできます。

次の例は、仮想インデックスを使用したクエリを示しています。

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

この例では、 `HYPO_INDEX`のコメントは仮想インデックスを指定しています。このインデックスを使用すると、フルテーブルスキャン（ `TableFullScan` ）の代わりにインデックス範囲スキャン（ `IndexRangeScan` ）が有効になり、推定コストが`392133.42`から`2.20`に削減されます。

TiDBは、ワークロード内のクエリに基づいて、ワークロードにメリットをもたらす可能性のあるインデックス候補を自動的に生成します。仮想インデックスを使用して潜在的なメリットを推定し、最も効果的なインデックスを推奨します。
