---
title: Analyze Slow Queries
summary: 遅いクエリを見つけて分析する方法を学びます。
---

# 遅いクエリを分析する {#analyze-slow-queries}

クエリの速度低下の問題を解決するには、次の 2 つの手順を実行する必要があります。

1.  多数のクエリの中で、どのタイプのクエリが遅いかを特定します。
2.  このタイプのクエリが遅い理由を分析します。

[スロークエリログ](/dashboard/dashboard-slow-query.md)と[ステートメント要約表](/statement-summary-tables.md)機能を使えば、ステップ1は簡単に実行できます。2つの機能を統合し、遅いクエリをブラウザに直接表示する[TiDBダッシュボード](/dashboard/dashboard-intro.md)ご利用をお勧めします。

このドキュメントでは、ステップ 2 (このタイプのクエリが遅い理由を分析する) の実行方法に焦点を当てます。

一般的に、クエリが遅くなる主な原因は次のとおりです。

-   間違ったインデックスが選択された、間違った結合タイプまたはシーケンスが選択されたなどのオプティマイザーの問題。
-   システムの問題。オプティマイザーが原因ではない問題はすべてシステムの問題です。例えば、TiKVインスタンスがビジー状態だとリクエストの処理が遅くなったり、リージョン情報が古くなるとクエリが遅くなったりします。

実際の状況では、オプティマイザの問題がシステムの問題を引き起こす可能性があります。例えば、特定の種類のクエリでは、オプティマイザはインデックスではなくフルテーブルスキャンを使用します。その結果、SQLクエリが多くのリソースを消費し、一部のTiKVインスタンスのCPU使用率が急上昇します。これはシステムの問題のように見えますが、実際にはオプティマイザの問題です。

システムの問題を特定するのは比較的簡単です。オプティマイザの問題を分析するには、実行プランが妥当かどうかを判断する必要があります。そのため、以下の手順に従って遅いクエリを分析することをお勧めします。

1.  クエリのパフォーマンスのボトルネック、つまりクエリ プロセスの中で時間のかかる部分を特定します。
2.  システムの問題を分析します。クエリのボトルネックとその時点の監視/ログ情報に基づいて、考えられる原因を分析します。
3.  オプティマイザーの問題を分析します。より優れた実行プランがあるかどうかを分析します。

上記の手順については、次のセクションで説明します。

## クエリのパフォーマンスボトルネックを特定する {#identify-the-performance-bottleneck-of-the-query}

まず、クエリプロセスの概要を理解する必要があります。TiDBにおけるクエリ実行プロセスの主要な段階を[TiDB パフォーマンス マップ](/media/performance-map.png)に示します。

次の方法を使用して期間情報を取得できます。

-   [スローログ](/identify-slow-queries.md) 。スローログは[TiDBダッシュボード](/dashboard/dashboard-overview.md)で表示することをお勧めします。
-   [`EXPLAIN ANALYZE`ステートメント](/sql-statements/sql-statement-explain-analyze.md) 。

上記の方法は、以下の点で異なります。

-   スロー ログには、解析から結果の返却まで、SQL 実行のほぼすべての段階の期間が記録され、比較的包括的です (TiDB ダッシュボードでスロー ログを直感的にクエリおよび分析できます)。
-   `EXPLAIN ANALYZE`実行すると、実際のSQL実行における各演算子の消費時間を知ることができます。結果には、実行時間に関するより詳細な統計情報が含まれます。

まとめると、スローログと`EXPLAIN ANALYZE`ステートメントは、SQLクエリの実行がどのコンポーネント（TiDBまたはTiKV）でどの段階で遅いのかを判断するのに役立ちます。これにより、クエリのパフォーマンスボトルネックを正確に特定できます。

さらに、v4.0.3以降では、スローログの`Plan`フィールドに、 `EXPLAIN ANALYZE`結果であるSQL実行情報も含まれるようになりました。そのため、スローログでSQL実行時間に関するすべての情報を確認できます。

## システムの問題を分析する {#analyze-system-issues}

システムの問題は、SQL ステートメントのさまざまな実行段階に応じて、次の種類に分類できます。

1.  TiKVはデータ処理が遅いです。例えば、TiKVコプロセッサはデータの処理が遅いです。
2.  TiDB は実行速度が遅いです。例えば、 `Join`演算子はデータの処理速度が遅くなります。
3.  その他の重要な段階は遅いです。例えば、タイムスタンプの取得に長い時間がかかります。

遅いクエリごとに、まずクエリがどのタイプに属するかを判断し、詳細に分析します。

### TiKVはデータ処理が遅い {#tikv-is-slow-in-data-processing}

TiKVによるデータ処理が遅い場合、 `EXPLAIN ANALYZE`の結果から簡単に特定できます。次の例では、 `StreamAgg_8`と`TableFullScan_15` 、つまり2つの`tikv-task`秒（ `task`列の`cop[tikv]`で示される）の実行に`170ms`かかります。15 `170ms`差し引くと、TiDB演算子の実行時間は全体の実行時間に占める割合が非常に小さくなります。これは、ボトルネックがTiKVにあることを示しています。

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

さらに、スローログのフィールド`Cop_process`と`Cop_wait`分析に役立ちます。次の例では、クエリの合計実行時間は約`180.85ms`で、最大の`coptask`の実行には`171ms`かかっています。これは、このクエリのボトルネックが TiKV 側にあることを示しています。

スロー ログの各フィールドの説明については、 [フィールドの説明](/identify-slow-queries.md#fields-description)参照してください。

```log
# Query_time: 0.18085
...
# Num_cop_tasks: 1
# Cop_process: Avg_time: 170ms P90_time: 170ms Max_time: 170ms Max_addr: 10.6.131.78
# Cop_wait: Avg_time: 1ms P90_time: 1ms Max_time: 1ms Max_Addr: 10.6.131.78
```

TiKV がボトルネックであると特定したら、次のセクションで説明するように原因を見つけることができます。

#### TiKVインスタンスはビジーです {#tikv-instance-is-busy}

SQL文の実行中に、TiDBは複数のTiKVインスタンスからデータを取得する場合があります。1つのTiKVインスタンスの応答が遅いと、SQL文全体の実行速度が低下します。

スロー ログの`Cop_wait`フィールドは、この原因を特定するのに役立ちます。

```log
# Cop_wait: Avg_time: 1ms P90_time: 2ms Max_time: 110ms Max_Addr: 10.6.131.78
```

上記のログは、インスタンス`10.6.131.78`に送信された`cop-task`実行されるまでに`110ms`待機していることを示しています。これは、このインスタンスがビジー状態であることを示しています。その時点のCPUモニタリングを確認することで、原因を確認できます。

#### 廃止されたMVCCバージョンと過剰なキー {#obsolete-mvcc-versions-and-excessive-keys}

TiKV上に古いMVCCバージョンが多すぎる場合、またはGCのMVCC履歴データの保持期間が長い場合、過剰なMVCCバージョンが蓄積される可能性があります。これらの不要なMVCCバージョンを処理すると、スキャンのパフォーマンスに影響する可能性があります。

`Total_keys`と`Processed_keys`確認してください。大きく異なる場合は、TiKVインスタンスに古いバージョンのキーが多すぎます。

    ...
    # Total_keys: 2215187529 Processed_keys: 1108056368
    ...

TiDB v8.5.0では、TiKV MVCCインメモリエンジン（IME）機能が導入され、このような低速クエリを高速化できます。詳細については、 [TiKV MVCC インメモリエンジン](/tikv-in-memory-engine.md)ご覧ください。

### 他の主要ステージは遅い {#other-key-stages-are-slow}

#### タイムスタンプの取得が遅い {#slow-in-getting-timestamps}

スローログで`Wait_TS`と`Query_time`比較できます。タイムスタンプはプリフェッチされるため、通常は`Wait_TS`値は低くなります。

    # Query_time: 0.0300000
    ...
    # Wait_TS: 0.02500000

#### 古いリージョン情報 {#outdated-region-information}

TiDB側のリージョン情報が古くなっている可能性があります。この場合、TiKVは`regionMiss`のエラーを返す可能性があります。その後、TiDBはPDからリージョン情報を再度取得し、 `Cop_backoff`情報に反映されます。障害発生回数と合計所要時間の両方が記録されます。

    # Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
    # Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2

#### サブクエリは事前に実行される {#subqueries-are-executed-in-advance}

非相関サブクエリを含む文の場合、サブクエリ部分は事前に実行される可能性があります。例えば、 `select * from t1 where a = (select max(a) from t2)`の場合、 `select max(a) from t2`部分は最適化段階で事前に実行される可能性があります。5 `EXPLAIN ANALYZE`結果は、このタイプのサブクエリの実行時間を示していません。

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

ただし、このタイプのサブクエリ実行はスロー ログで識別できます。

    # Query_time: 7.770634843
    ...
    # Rewrite_time: 7.765673663 Preproc_subqueries: 1 Preproc_subqueries_time: 7.765231874

上記のログ レコードから、サブクエリが事前に実行され、 `7.76s`かかることがわかります。

### TiDBは実行が遅い {#tidb-is-slow-in-execution}

TiDBの実行プランは正しいものの、実行速度が遅い場合を考えてみましょう。このような問題を解決するには、SQL文の`EXPLAIN ANALYZE`の結果に応じてパラメータを調整するか、ヒントを使用します。

実行プランが正しくない場合は、セクション[オプティマイザーの問題を分析する](#analyze-optimizer-issues)参照してください。

#### 同時実行性が低い {#low-concurrency}

ボトルネックが同時実行を伴う演算子にある場合は、同時実行性を調整して実行速度を上げます。例:

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

上記のように、 `HashJoin_14`と`Projection_24`実行時間の大部分を消費します。SQL変数を使用してこれらの同時実行性を高め、実行速度を向上させることを検討してください。

すべてのシステム変数は[システム変数](/system-variables.md)に記載されています。 `HashJoin_14`の同時実行性を高めるには、 `tidb_hash_join_concurrency`システム変数を変更します。

#### データがディスクに流出 {#data-is-spilled-to-disk}

実行速度が遅くなるもう一つの原因は、メモリ制限に達した場合に実行中に発生するディスクスピルです。この原因は、実行プランとスローログで確認できます。

```sql
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| id                      | estRows   | actRows | task      | access object | execution info               | operator info        | memory                | disk           |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
| Sort_4                  | 462144.00 | 462144  | root      |               | time:2.02848898s, loops:453  | test.t.a             | 149.68795776367188 MB | 219.3203125 MB |
| └─TableReader_8         | 462144.00 | 462144  | root      |               | time:616.211272ms, loops:453 | data:TableFullScan_7 | 197.49601364135742 MB | N/A            |
|   └─TableFullScan_7     | 462144.00 | -1      | cop[tikv] | table:t       | time:0s, loops:0             | keep order:false     | N/A                   | N/A            |
+-------------------------+-----------+---------+-----------+---------------+------------------------------+----------------------+-----------------------+----------------+
```

    ...
    # Disk_max: 229974016
    ...

#### 直積による結合演算 {#join-operations-with-cartesian-product}

デカルト積を用いた結合演算では、最大`left child row count * right child row count`という大きなデータ量が生成されます。これは非効率なので、避けるべきです。

このタイプの結合操作は、実行プランでは`CARTESIAN`マークされます。例:

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

オプティマイザの問題を分析するには、実行プランが妥当かどうかを判断する必要があります。最適化プロセスと各演算子についてある程度の理解が必要です。

次の例では、テーブル スキーマが`create table t (id int, a int, b int, c int, primary key(id), key(a), key(b, c))`であると想定します。

1.  `select * from t` : フィルター条件はなく、テーブル全体のスキャンが実行されます。そのため、データの読み取りには`TableFullScan`演算子が使用されます。
2.  `select a from t where a=2` : フィルター条件があり、インデックス列のみが読み取られるため、 `IndexReader`演算子を使用してデータを読み取ります。
3.  `select * from t where a=2` : `a`のフィルター条件がありますが、 `a`インデックスでは読み取るデータを完全にカバーできないため、 `IndexLookup`演算子が使用されます。
4.  `select b from t where c=3` : プレフィックス条件がないと、マルチカラムインデックスは使用できません。そのため、 `IndexFullScan`使用されます。
5.  ...

上記の例は、データ読み取りに使用される演算子です。その他の演算子については、 [TiDB実行プランを理解する](/explain-overview.md)参照してください。

さらに、 [SQLチューニングの概要](/sql-tuning-overview.md)読むことで、TiDB オプティマイザーをより深く理解し、実行プランが妥当かどうかを判断するのに役立ちます。

オプティマイザに関する問題のほとんどは[SQLチューニングの概要](/sql-tuning-overview.md)で説明されています。解決策については、以下のドキュメントを参照してください。

1.  [インデックス問題の解決方法](/wrong-index-solution.md)
2.  [結合順序が間違っています](/join-reorder.md)
3.  [式は押し下げられない](/blocklist-control-plan.md)
