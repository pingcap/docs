---
title: Analyze Slow Queries
summary: Learn how to locate and analyze slow queries.
---

# 遅いクエリを分析する {#analyze-slow-queries}

遅いクエリの問題に対処するには、次の 2 つの手順を実行する必要があります。

1.  多くのクエリの中で、どのタイプのクエリが遅いかを特定します。
2.  このタイプのクエリが遅い理由を分析します。

[遅いクエリ ログ](/dashboard/dashboard-slow-query.md)と[ステートメント要約表](/statement-summary-tables.md)機能を使用して、ステップ 1 を簡単に実行できます。 [TiDB ダッシュボード](/dashboard/dashboard-intro.md)を使用することをお勧めします。これは、2 つの機能を統合し、ブラウザーにスロー クエリを直接表示します。

このドキュメントでは、ステップ 2 を実行する方法に焦点を当てます - このタイプのクエリが遅い理由を分析します。

一般に、遅いクエリには次の主な原因があります。

-   間違ったインデックスが選択されている、間違った結合タイプまたはシーケンスが選択されているなどのオプティマイザーの問題。
-   システムの問題。オプティマイザが原因ではないすべての問題は、システムの問題です。たとえば、ビジー状態の TiKV インスタンスはリクエストの処理に時間がかかります。リージョン情報が古いと、クエリが遅くなります。

実際の状況では、オプティマイザーの問題がシステムの問題を引き起こす可能性があります。たとえば、特定のタイプのクエリの場合、オプティマイザーはインデックスではなくフル テーブル スキャンを使用します。その結果、SQL クエリは多くのリソースを消費し、一部の TiKV インスタンスの CPU 使用率が急増します。これはシステムの問題のように見えますが、本質的にはオプティマイザの問題です。

システムの問題を特定するのは比較的簡単です。オプティマイザの問題を分析するには、実行計画が妥当かどうかを判断する必要があります。したがって、次の手順に従ってスロー クエリを分析することをお勧めします。

1.  クエリのパフォーマンスのボトルネック、つまり、クエリ プロセスの時間のかかる部分を特定します。
2.  システムの問題を分析する: クエリのボトルネックとその時の監視/ログ情報に従って、考えられる原因を分析します。
3.  オプティマイザーの問題を分析します。より良い実行計画があるかどうかを分析します。

上記の手順については、次のセクションで説明します。

## クエリのパフォーマンスのボトルネックを特定する {#identify-the-performance-bottleneck-of-the-query}

まず、クエリ プロセスの一般的な理解が必要です。 TiDB でのクエリ実行プロセスの主要な段階を[TiDB パフォーマンス マップ](/media/performance-map.png)に示します。

次のメソッドを使用して期間情報を取得できます。

-   [スローログ](/identify-slow-queries.md) . [TiDB ダッシュボード](/dashboard/dashboard-overview.md)でスローログを表示することをお勧めします。
-   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md) .

上記の方法は、次の点で異なります。

-   スローログは、解析から結果を返すまでの SQL 実行のほぼすべての段階の期間を記録し、比較的包括的です (TiDB ダッシュボードで直感的な方法でスローログを照会および分析できます)。
-   `EXPLAIN ANALYZE`を実行することで、実際の SQL 実行における各演算子の消費時間を知ることができます。結果には、実行時間のより詳細な統計が含まれます。

要約すると、slow log と`EXPLAIN ANALYZE`ステートメントは、実行のどの段階で、どのコンポーネント(TiDB または TiKV) で SQL クエリが遅いかを判断するのに役立ちます。したがって、クエリのパフォーマンスのボトルネックを正確に特定できます。

さらに、v4.0.3 以降、スローログの`Plan`フィールドには、 `EXPLAIN ANALYZE`の結果である SQL 実行情報も含まれます。そのため、SQL の実行時間に関するすべての情報をスロー ログで見つけることができます。

## システムの問題を分析する {#analyze-system-issues}

システムの問題は、SQL ステートメントのさまざまな実行段階に応じて、次のタイプに分類できます。

1.  TiKV はデータ処理が遅いです。たとえば、TiKV コプロセッサはデータの処理に時間がかかります。
2.  TiDB は実行が遅いです。たとえば、 `Join`演算子はデータの処理に時間がかかります。
3.  他の重要な段階は遅いです。たとえば、タイムスタンプの取得には時間がかかります。

遅いクエリごとに、まずクエリがどのタイプに属しているかを判断し、詳細に分析します。

### TiKV はデータ処理が遅い {#tikv-is-slow-in-data-processing}

TiKV のデータ処理が遅い場合は、 `EXPLAIN ANALYZE`の結果で簡単に識別できます。次の例では、 `StreamAgg_8`と`TableFullScan_15` 、2 つの`tikv-task` ( `task`列の`cop[tikv]`で示されている) を実行するには`170ms`必要です。 `170ms`を引いた後、TiDB オペレーターの実行時間は、合計実行時間のごく一部を占めます。これは、ボトルネックが TiKV にあることを示しています。

```sql
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| id                         | estRows | actRows | task      | access object | execution info                                                               | operator info                   | memory    | disk |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| StreamAgg_16               | 1.00    | 1       | root      |               | time:170.08572ms, loops:2                                                     | funcs:count(Column#5)->Column#3 | 372 Bytes | N/A  |
| └─TableReader_17           | 1.00    | 1       | root      |               | time:170.080369ms, loops:2, rpc num: 1, rpc time:17.023347ms, proc keys:28672 | data:StreamAgg_8                | 202 Bytes | N/A  |
|   └─StreamAgg_8            | 1.00    | 1       | cop[tikv] |               | time:170ms, loops:29                                                          | funcs:count(1)->Column#5        | N/A       | N/A  |
|     └─TableFullScan_15     | 7.00    | 28672   | cop[tikv] | table:t       | time:170ms, loops:29                                                          | keep order:false, stats:pseudo  | N/A       | N/A  |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------
```

さらに、スロー ログの`Cop_process`フィールドと`Cop_wait`フィールドも分析に役立ちます。次の例では、クエリの合計所要時間は約`180.85ms`で、最大の`coptask`で`171ms`かかります。これは、このクエリのボトルネックが TiKV 側にあることを示しています。

スロー ログの各フィールドの説明については、 [フィールドの説明](/identify-slow-queries.md#fields-description)を参照してください。

```log
# Query_time: 0.18085
...
# Num_cop_tasks: 1
# Cop_process: Avg_time: 170ms P90_time: 170ms Max_time: 170ms Max_addr: 10.6.131.78
# Cop_wait: Avg_time: 1ms P90_time: 1ms Max_time: 1ms Max_Addr: 10.6.131.78
```

TiKV がボトルネックであることを特定したら、次のセクションで説明するように原因を突き止めることができます。

#### TiKV インスタンスがビジーです {#tikv-instance-is-busy}

SQL ステートメントの実行中に、TiDB は複数の TiKV インスタンスからデータをフェッチする場合があります。 1 つの TiKV インスタンスの応答が遅い場合、全体的な SQL 実行速度が遅くなります。

スロー ログの`Cop_wait`フィールドは、この原因を特定するのに役立ちます。

```log
# Cop_wait: Avg_time: 1ms P90_time: 2ms Max_time: 110ms Max_Addr: 10.6.131.78
```

上記のログは、 `10.6.131.78`インスタンスに送信された`cop-task`が実行される前に`110ms`待機することを示しています。このインスタンスがビジーであることを示します。その時のCPU監視で原因を確認できます。

#### 古いキーが多すぎる {#too-many-outdated-keys}

TiKV インスタンスには多くの古いデータが含まれており、データ スキャンのためにクリーンアップする必要があります。これは処理速度に影響します。

`Total_keys`と`Processed_keys`を確認してください。それらが大きく異なる場合、TiKV インスタンスには古いバージョンのキーが多すぎます。

```
...
# Total_keys: 2215187529 Processed_keys: 1108056368
...
```

### 他の重要な段階は遅い {#other-key-stages-are-slow}

#### タイムスタンプの取得が遅い {#slow-in-getting-timestamps}

スローログで`Wait_TS`と`Query_time`を比較できます。タイムスタンプはプリフェッチされるため、通常は`Wait_TS`が低くなります。

```
# Query_time: 0.0300000
...
# Wait_TS: 0.02500000
```

#### 古いリージョン情報 {#outdated-region-information}

TiDB 側のリージョン情報が古い可能性があります。この場合、TiKV は`regionMiss`エラーを返すことがあります。その後、TiDB は再び PD からリージョン情報を取得し、 `Cop_backoff`の情報に反映されます。失敗した時間と合計期間の両方が記録されます。

```
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
```

#### サブクエリは事前に実行されます {#subqueries-are-executed-in-advance}

非相関サブクエリを含むステートメントの場合、サブクエリ部分が事前に実行される場合があります。たとえば、 `select * from t1 where a = (select max(a) from t2)`では、 `select max(a) from t2`部分が最適化段階で事前に実行される場合があります。 `EXPLAIN ANALYZE`の結果は、このタイプのサブクエリの期間を示しません。

```sql
mysql> explain analyze select count(*) from t where a=(select max(t1.a) from t t1, t t2 where t1.a=t2.a);
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
| id                           | estRows  | actRows | task      | access object | execution info           | operator info                    | memory    | disk |
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
| StreamAgg_59                 | 1.00     | 1       | root      |               | time:4.69267ms, loops:2  | funcs:count(Column#10)->Column#8 | 372 Bytes | N/A  |
| └─TableReader_60             | 1.00     | 1       | root      |               | time:4.690428ms, loops:2 | data:StreamAgg_48                | 141 Bytes | N/A  |
|   └─StreamAgg_48             | 1.00     |         | cop[tikv] |               | time:0ns, loops:0        | funcs:count(1)->Column#10        | N/A       | N/A  |
|     └─Selection_58           | 16384.00 |         | cop[tikv] |               | time:0ns, loops:0        | eq(test.t.a, 1)                  | N/A       | N/A  |
|       └─TableFullScan_57     | 16384.00 | -1      | cop[tikv] | table:t       | time:0s, loops:0         | keep order:false                 | N/A       | N/A  |
+------------------------------+----------+---------+-----------+---------------+--------------------------+----------------------------------+-----------+------+
5 rows in set (7.77 sec)
```

ただし、このタイプのサブクエリの実行は、スロー ログで識別できます。

```
# Query_time: 7.770634843
...
# Rewrite_time: 7.765673663 Preproc_subqueries: 1 Preproc_subqueries_time: 7.765231874
```

上記のログ レコードから、サブクエリが事前に実行され、 `7.76s`かかることがわかります。

### TiDB の実行が遅い {#tidb-is-slow-in-execution}

TiDB の実行計画は正しいが、実行が遅いと仮定します。この種の問題を解決するには、パラメーターを調整するか、SQL ステートメントの`EXPLAIN ANALYZE`の結果に従ってヒントを使用します。

実行計画が正しくない場合は、 [オプティマイザーの問題を分析する](#analyze-optimizer-issues)セクションを参照してください。

#### 同時実行性が低い {#low-concurrency}

ボトルネックが並行性を持つオペレーターにある場合は、並行性を調整して実行を高速化します。例えば：

```sql
mysql> explain analyze select sum(t1.a) from t t1, t t2 where t1.a=t2.a;
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
| id                               | estRows      | actRows   | task      | access object | execution info                                                                      | operator info                                  | memory           | disk    |
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
| HashAgg_11                       | 1.00         | 1         | root      |               | time:9.666832189s, loops:2, PartialConcurrency:4, FinalConcurrency:4                | funcs:sum(Column#6)->Column#5                  | 322.125 KB       | N/A     |
| └─Projection_24                  | 268435456.00 | 268435456 | root      |               | time:9.098644711s, loops:262145, Concurrency:4                                      | cast(test.t.a, decimal(65,0) BINARY)->Column#6 | 199 KB           | N/A     |
|   └─HashJoin_14                  | 268435456.00 | 268435456 | root      |               | time:6.616773501s, loops:262145, Concurrency:5, probe collision:0, build:881.404µs  | inner join, equal:[eq(test.t.a, test.t.a)]     | 131.75 KB        | 0 Bytes |
|     ├─TableReader_21(Build)      | 16384.00     | 16384     | root      |               | time:6.553717ms, loops:17                                                           | data:Selection_20                              | 33.6318359375 KB | N/A     |
|     │ └─Selection_20             | 16384.00     |           | cop[tikv] |               | time:0ns, loops:0                                                                   | not(isnull(test.t.a))                          | N/A              | N/A     |
|     │   └─TableFullScan_19       | 16384.00     | -1        | cop[tikv] | table:t2      | time:0s, loops:0                                                                    | keep order:false                               | N/A              | N/A     |
|     └─TableReader_18(Probe)      | 16384.00     | 16384     | root      |               | time:6.880923ms, loops:17                                                           | data:Selection_17                              | 33.6318359375 KB | N/A     |
|       └─Selection_17             | 16384.00     |           | cop[tikv] |               | time:0ns, loops:0                                                                   | not(isnull(test.t.a))                          | N/A              | N/A     |
|         └─TableFullScan_16       | 16384.00     | -1        | cop[tikv] | table:t1      | time:0s, loops:0                                                                    | keep order:false                               | N/A              | N/A     |
+----------------------------------+--------------+-----------+-----------+---------------+-------------------------------------------------------------------------------------+------------------------------------------------+------------------+---------+
9 rows in set (9.67 sec)
```

上記のように、 `HashJoin_14`と`Projection_24`実行時間の多くを消費します。実行を高速化するために、SQL 変数を使用して同時実行数を増やすことを検討してください。

すべてのシステム変数は[システム変数](/system-variables.md)に記載されています。 `HashJoin_14`の同時実行性を高めるには、システム変数`tidb_hash_join_concurrency`を変更します。

#### データがディスクにこぼれる {#data-is-spilled-to-disk}

実行が遅くなるもう 1 つの原因は、メモリの制限に達した場合に実行中に発生するディスクのスピルです。この原因は、実行計画とスロー ログで確認できます。

```sql
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| id                      | estRows   | actRows | task      | access object | execution info               | operator info        | memory                | disk           |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| Sort_4                  | 462144.00 | 462144  | root      |               | time:2.02848898s, loops:453  | test.t.a             | 149.68795776367188 MB | 219.3203125 MB |
| └─TableReader_8         | 462144.00 | 462144  | root      |               | time:616.211272ms, loops:453 | data:TableFullScan_7 | 197.49601364135742 MB | N/A            |
|   └─TableFullScan_7     | 462144.00 | -1      | cop[tikv] | table:t       | time:0s, loops:0             | keep order:false     | N/A                   | N/A            |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
```

```
...
# Disk_max: 229974016
...
```

#### デカルト積で演算を結合 {#join-operations-with-cartesian-product}

デカルト積を使用した結合操作では、 `left child row count * right child row count`ものデータ ボリュームが生成されます。これは非効率的であり、避ける必要があります。

このタイプの結合操作は、実行計画で`CARTESIAN`とマークされます。例えば：

```sql
mysql> explain select * from t t1, t t2 where t1.a>t2.a;
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
| id                           | estRows     | task      | access object | operator info                                           |
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
| HashJoin_8                   | 99800100.00 | root      |               | CARTESIAN inner join, other cond:gt(test.t.a, test.t.a) |
| ├─TableReader_15(Build)      | 9990.00     | root      |               | data:Selection_14                                       |
| │ └─Selection_14             | 9990.00     | cop[tikv] |               | not(isnull(test.t.a))                                   |
| │   └─TableFullScan_13       | 10000.00    | cop[tikv] | table:t2      | keep order:false, stats:pseudo                          |
| └─TableReader_12(Probe)      | 9990.00     | root      |               | data:Selection_11                                       |
|   └─Selection_11             | 9990.00     | cop[tikv] |               | not(isnull(test.t.a))                                   |
|     └─TableFullScan_10       | 10000.00    | cop[tikv] | table:t1      | keep order:false, stats:pseudo                          |
+------------------------------+-------------+-----------+---------------+---------------------------------------------------------+
```

## オプティマイザーの問題を分析する {#analyze-optimizer-issues}

オプティマイザの問題を分析するには、実行計画が妥当かどうかを判断する必要があります。最適化プロセスと各演算子についてある程度理解する必要があります。

次の例では、テーブル スキーマが`create table t (id int, a int, b int, c int, primary key(id), key(a), key(b, c))`であると想定しています。

1.  `select * from t` : フィルター条件はなく、テーブル全体のスキャンが実行されます。したがって、データの読み取りには`TableFullScan`演算子が使用されます。
2.  `select a from t where a=2` : フィルター条件があり、インデックス列のみが読み取られるため、データの読み取りには`IndexReader`演算子が使用されます。
3.  `select * from t where a=2` : `a`のフィルター条件がありますが、 `a`インデックスでは読み取るデータを完全にカバーできないため、 `IndexLookup`演算子が使用されます。
4.  `select b from t where c=3` : プレフィクス条件がない場合、複数列インデクスは使用できません。したがって、 `IndexFullScan`が使用されます。
5.  ...

上記の例は、データの読み取りに使用される演算子です。その他の演算子については、 [TiDB 実行計画を理解する](/explain-overview.md)を参照してください。

さらに、 [SQL チューニングの概要](/sql-tuning-overview.md)を読むことで、TiDB オプティマイザーをよりよく理解し、実行計画が妥当かどうかを判断するのに役立ちます。

ほとんどのオプティマイザの問題は[SQL チューニングの概要](/sql-tuning-overview.md)で説明されています。解決策については、次のドキュメントを参照してください。

1.  [インデックス問題の解決方法](/wrong-index-solution.md)
2.  [参加順序が間違っている](/join-reorder.md)
3.  [式は押し下げられません](/blocklist-control-plan.md)
