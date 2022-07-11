---
title: Analyze Slow Queries
summary: Learn how to locate and analyze slow queries.
---

# 遅いクエリを分析する {#analyze-slow-queries}

遅いクエリの問題に対処するには、次の2つの手順を実行する必要があります。

1.  多くのクエリの中から、どのタイプのクエリが遅いかを特定します。
2.  このタイプのクエリが遅い理由を分析します。

[遅いクエリログ](/dashboard/dashboard-slow-query.md)と[ステートメント要約表](/statement-summary-tables.md)の機能を使用して、ステップ1を簡単に実行できます。 2つの機能を統合し、ブラウザに遅いクエリを直接表示する[TiDBダッシュボード](/dashboard/dashboard-intro.md)を使用することをお勧めします。

このドキュメントでは、ステップ2の実行方法に焦点を当てています。このタイプのクエリが遅い理由を分析してください。

一般に、遅いクエリには次の主な原因があります。

-   間違ったインデックスが選択された、間違った結合タイプまたはシーケンスが選択されたなどのオプティマイザの問題。
-   システムの問題。オプティマイザが原因ではないすべての問題は、システムの問題です。たとえば、ビジー状態のTiKVインスタンスはリクエストをゆっくり処理します。古くなった地域情報により、クエリが遅くなります。

実際の状況では、オプティマイザの問題がシステムの問題を引き起こす可能性があります。たとえば、特定のタイプのクエリの場合、オプティマイザはインデックスの代わりに全表スキャンを使用します。その結果、SQLクエリは多くのリソースを消費し、一部のTiKVインスタンスのCPU使用率が急上昇します。これはシステムの問題のように見えますが、本質的にはオプティマイザの問題です。

システムの問題を特定するのは比較的簡単です。オプティマイザの問題を分析するには、実行プランが妥当かどうかを判断する必要があります。したがって、次の手順に従って、遅いクエリを分析することをお勧めします。

1.  クエリのパフォーマンスのボトルネック、つまりクエリプロセスの時間のかかる部分を特定します。
2.  システムの問題を分析します。クエリのボトルネックとその時点の監視/ログ情報に従って、考えられる原因を分析します。
3.  オプティマイザーの問題を分析します。より適切な実行プランがあるかどうかを分析します。

上記の手順については、次のセクションで説明します。

## クエリのパフォーマンスのボトルネックを特定する {#identify-the-performance-bottleneck-of-the-query}

まず、クエリプロセスの一般的な理解が必要です。 TiDBでのクエリ実行プロセスの主要な段階を[TiDBパフォーマンスマップ](/media/performance-map.png)に示します。

次の方法を使用して、期間情報を取得できます。

-   [遅いログ](/identify-slow-queries.md) 。 [TiDBダッシュボード](/dashboard/dashboard-overview.md)で遅いログインを表示することをお勧めします。
-   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md) 。

上記の方法は、次の点で異なります。

-   スローログは、解析から結果の返送まで、SQL実行のほぼすべての段階の期間を記録し、比較的包括的です（TiDBダッシュボードでスローログを直感的な方法でクエリおよび分析できます）。
-   `EXPLAIN ANALYZE`を実行することにより、実際のSQL実行における各演算子の消費時間を知ることができます。結果には、実行期間のより詳細な統計が含まれます。

要約すると、slow logおよび`EXPLAIN ANALYZE`ステートメントは、実行のどの段階でどのコンポーネント（TiDBまたはTiKV）でSQLクエリが遅いかを判断するのに役立ちます。したがって、クエリのパフォーマンスのボトルネックを正確に特定できます。

さらに、v4.0.3以降、低速ログの`Plan`フィールドには、 `EXPLAIN ANALYZE`の結果であるSQL実行情報も含まれています。したがって、SQL期間のすべての情報を低速ログで見つけることができます。

## システムの問題を分析する {#analyze-system-issues}

システムの問題は、SQLステートメントのさまざまな実行段階に応じて次のタイプに分類できます。

1.  TiKVはデータ処理が遅いです。たとえば、TiKVコプロセッサーはデータをゆっくりと処理します。
2.  TiDBの実行は遅いです。たとえば、 `Join`人のオペレーターはデータをゆっくりと処理します。
3.  他の重要な段階は遅いです。たとえば、タイムスタンプの取得には長い時間がかかります。

遅いクエリごとに、最初にクエリがどのタイプに属するかを判別してから、詳細に分析します。

### TiKVはデータ処理が遅い {#tikv-is-slow-in-data-processing}

TiKVのデータ処理が遅い場合は、 `EXPLAIN ANALYZE`の結果で簡単に識別できます。次の例では、 `StreamAgg_8`と`TableFullScan_15`つの`tikv-task` （ `task`列の`cop[tikv]`で示されている）は、実行に`170ms`を要します。 `170ms`を引いた後、TiDBオペレーターの実行時間は、合計実行時間のごくわずかな割合を占めます。これは、ボトルネックがTiKVにあることを示しています。

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

さらに、低速ログの`Cop_process`フィールドと`Cop_wait`フィールドも分析に役立ちます。次の例では、クエリの合計時間は約`180.85ms`で、最大の`coptask`は`171ms`になります。これは、このクエリのボトルネックがTiKV側にあることを示しています。

スローログの各フィールドの説明については、 [フィールドの説明](/identify-slow-queries.md#fields-description)を参照してください。

```log
# Query_time: 0.18085
...
# Num_cop_tasks: 1
# Cop_process: Avg_time: 170ms P90_time: 170ms Max_time: 170ms Max_addr: 10.6.131.78
# Cop_wait: Avg_time: 1ms P90_time: 1ms Max_time: 1ms Max_Addr: 10.6.131.78
```

TiKVがボトルネックであることを確認したら、次のセクションで説明するように原因を特定できます。

#### TiKVインスタンスがビジーです {#tikv-instance-is-busy}

SQLステートメントの実行中に、TiDBは複数のTiKVインスタンスからデータをフェッチする場合があります。 1つのTiKVインスタンスの応答が遅い場合、全体的なSQL実行速度が遅くなります。

遅いログの`Cop_wait`フィールドは、この原因を特定するのに役立ちます。

```log
# Cop_wait: Avg_time: 1ms P90_time: 2ms Max_time: 110ms Max_Addr: 10.6.131.78
```

上記のログは、 `10.6.131.78`のインスタンスに送信された`cop-task`が実行される前に`110ms`を待機していることを示しています。このインスタンスがビジーであることを示します。その時のCPU監視で原因を確認できます。

#### 古いキーが多すぎます {#too-many-outdated-keys}

TiKVインスタンスには多くの古いデータがあり、データスキャンのためにクリーンアップする必要があります。これは処理速度に影響します。

`Total_keys`と`Processed_keys`を確認してください。それらが大きく異なる場合、TiKVインスタンスには古いバージョンのキーが多すぎます。

```
...
# Total_keys: 2215187529 Processed_keys: 1108056368
...
```

### 他の重要な段階は遅い {#other-key-stages-are-slow}

#### タイムスタンプの取得が遅い {#slow-in-getting-timestamps}

遅いログで`Wait_TS`と`Query_time`を比較できます。タイムスタンプはプリフェッチされるため、通常は`Wait_TS`を低くする必要があります。

```
# Query_time: 0.0300000
...
# Wait_TS: 0.02500000
```

#### 古くなった地域情報 {#outdated-region-information}

TiDB側の地域情報が古くなっている可能性があります。この状況では、TiKVは`regionMiss`エラーを返す可能性があります。次に、TiDBはPDからリージョン情報を再度取得します。これは`Cop_backoff`の情報に反映されます。失敗した時間と合計期間の両方が記録されます。

```
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
```

#### サブクエリは事前に実行されます {#subqueries-are-executed-in-advance}

相関のないサブクエリを含むステートメントの場合、サブクエリ部分が事前に実行される場合があります。たとえば、 `select * from t1 where a = (select max(a) from t2)`では、最適化段階で`select max(a) from t2`の部分が事前に実行される場合があります。 `EXPLAIN ANALYZE`の結果は、このタイプのサブクエリの期間を示していません。

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

ただし、このタイプのサブクエリの実行は、低速ログで識別できます。

```
# Query_time: 7.770634843
...
# Rewrite_time: 7.765673663 Preproc_subqueries: 1 Preproc_subqueries_time: 7.765231874
```

上記のログレコードから、サブクエリが事前に実行され、 `7.76s`がかかることがわかります。

### TiDBの実行が遅い {#tidb-is-slow-in-execution}

TiDBの実行プランは正しいが、実行が遅いと仮定します。このタイプの問題を解決するには、SQLステートメントの`EXPLAIN ANALYZE`の結果に応じて、パラメーターを調整するか、ヒントを使用できます。

実行計画が正しくない場合は、 [オプティマイザの問題を分析する](#analyze-optimizer-issues)セクションを参照してください。

#### 同時実行性が低い {#low-concurrency}

同時実行性のある演算子にボトルネックがある場合は、同時実行性を調整して実行を高速化します。例えば：

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

上に示したように、 `HashJoin_14`と`Projection_24`は実行時間の多くを消費します。実行を高速化するために、SQL変数を使用して同時実行性を高めることを検討してください。

すべてのシステム変数は[システム変数](/system-variables.md)で文書化されています。 `HashJoin_14`の並行性を高めるために、 `tidb_hash_join_concurrency`システム変数を変更できます。

#### データがディスクに流出する {#data-is-spilled-to-disk}

実行速度が低下するもう1つの原因は、メモリ制限に達した場合に実行中に発生するディスクスピルです。この原因は、実行プランと遅いログで確認できます。

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

#### デカルト積で操作に参加する {#join-operations-with-cartesian-product}

デカルト積を使用した結合操作により、最大`left child row count * right child row count`のデータ量が生成されます。これは非効率的であり、避ける必要があります。

このタイプの結合操作は、実行プランで`CARTESIAN`とマークされています。例えば：

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

## オプティマイザの問題を分析する {#analyze-optimizer-issues}

オプティマイザの問題を分析するには、実行プランが妥当かどうかを判断する必要があります。最適化プロセスと各演算子についてある程度理解している必要があります。

次の例では、テーブルスキーマが`create table t (id int, a int, b int, c int, primary key(id), key(a), key(b, c))`であると想定しています。

1.  `select * from t` ：フィルター条件はなく、全表スキャンが実行されます。したがって、 `TableFullScan`演算子はデータの読み取りに使用されます。
2.  `select a from t where a=2` ：フィルター条件があり、インデックス列のみが読み取られるため、 `IndexReader`演算子を使用してデータを読み取ります。
3.  `select * from t where a=2` ： `a`のフィルター条件がありますが、 `a`インデックスは読み取るデータを完全にカバーできないため、 `IndexLookup`演算子が使用されます。
4.  `select b from t where c=3` ：プレフィックス条件がないと、複数列のインデックスは使用できません。したがって、 `IndexFullScan`が使用されます。
5.  ..。

上記の例は、データの読み取りに使用される演算子です。その他の演算子については、 [TiDB実行計画を理解する](/explain-overview.md)を参照してください。

さらに、 [SQLチューニングの概要](/sql-tuning-overview.md)を読むと、TiDBオプティマイザーをよりよく理解し、実行プランが妥当かどうかを判断するのに役立ちます。

ほとんどのオプティマイザの問題は[SQLチューニングの概要](/sql-tuning-overview.md)で説明されています。解決策については、次のドキュメントを参照してください。

1.  [インデックス問題の解決方法](/wrong-index-solution.md)
2.  [間違った参加順序](/join-reorder.md)
3.  [式はプッシュダウンされません](/blocklist-control-plan.md)
