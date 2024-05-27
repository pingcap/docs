---
title: Locate Problems Using Diagnostic Report of TiDB Dashboard
summary: TiDB ダッシュボードの診断レポートは、さまざまな時間範囲でのシステム パフォーマンスを比較することで、問題を特定するのに役立ちます。QPS の低下、レイテンシーの増加、クエリの低速化などの問題を特定し、詳細な分析と SQL ステートメントを提供して、さらに調査できるようにします。この比較レポートは、パフォーマンスの問題を迅速に特定して対処するために不可欠です。
---

# TiDBダッシュボードの診断レポートを使用して問題を特定する {#locate-problems-using-diagnostic-report-of-tidb-dashboard}

このドキュメントでは、TiDB ダッシュボードの診断レポートを使用して問題を特定する方法について説明します。

## 比較診断 {#comparison-diagnostics}

このセクションでは、比較診断機能を使用して、大規模なクエリや書き込みによって発生する QPS ジッターやレイテンシーの増加を診断する方法を説明します。

### 例1 {#example-1}

![QPS example](/media/dashboard/dashboard-diagnostics-usage1.png)

`go-ycsb`圧力テストの結果が上の画像に示されています。3 で QPS が突然減少し始めたことがわかります。3 `2020-03-10 13:24:30`後、QPS は正常に戻り始めました。TiDB ダッシュボードの診断レポートを使用して原因を見つけることができます。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-03-10 13:21:00` ～ `2020-03-10 13:23:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-03-10 13:24:30` ～ `2020-03-10 13:27:30` 。この範囲では、QPS が減少し始めました。

ジッターの影響範囲は 3 分であるため、上記の 2 つの時間範囲は両方とも 3 分です。診断中に比較するために監視された平均値がいくつか使用されるため、範囲が長すぎると平均値の差が重要でなくなり、問題を正確に特定できなくなります。

レポートが生成されると、**比較診断**ページでこのレポートを表示できます。

![Comparison diagnostics](/media/dashboard/dashboard-diagnostics-usage2.png)

上記の診断結果は、診断時間中に大きなクエリが存在する可能性があることを示しています。上記のレポートの各**詳細**は、次のように説明されています。

-   `tidb_qps` : QPSが0.93倍減少しました。
-   `tidb_query_duration` : P999 クエリのレイテンシーが1.54 倍に増加しました。
-   `tidb_cop_duration` : P999 コプロセッサ要求の処理レイテンシーが2.48 倍に増加しました。
-   `tidb_kv_write_num` : P999 TiDB トランザクションで書き込まれた KV の数は 7.61 倍に増加しました。
-   `tikv_cop_scan_keys_total_nun` : TiKVコプロセッサーによってスキャンされるキー/値の数は、3 つの TiKV インスタンスで大幅に改善されました。
-   `pd_operator_step_finish_total_count`では、転勤リーダー数が2.45倍に増加しており、これは異常時間帯のスケジュールが正常時間帯のスケジュールよりも高いことを意味します。
-   このレポートは、遅いクエリが存在する可能性があることを示しており、遅いクエリを照会するには SQL ステートメントを使用できることを示しています。SQL ステートメントの実行結果は次のとおりです。

```sql
SELECT * FROM (SELECT count(*), min(time), sum(query_time) AS sum_query_time, sum(Process_time) AS sum_process_time, sum(Wait_time) AS sum_wait_time, sum(Commit_time), sum(Request_count), sum(process_keys), sum(Write_keys), max(Cop_proc_max), min(query),min(prev_stmt), digest FROM information_schema.CLUSTER_SLOW_QUERY WHERE time >= '2020-03-10 13:24:30' AND time < '2020-03-10 13:27:30' AND Is_internal = false GROUP BY digest) AS t1 WHERE t1.digest NOT IN (SELECT digest FROM information_schema.CLUSTER_SLOW_QUERY WHERE time >= '2020-03-10 13:21:00' AND time < '2020-03-10 13:24:00' GROUP BY digest) ORDER BY t1.sum_query_time DESC limit 10\G
***************************[ 1. row ]***************************
count(*)           | 196
min(time)          | 2020-03-10 13:24:30.204326
sum_query_time     | 46.878509117
sum_process_time   | 265.924
sum_wait_time      | 8.308
sum(Commit_time)   | 0.926820886
sum(Request_count) | 6035
sum(process_keys)  | 201453000
sum(Write_keys)    | 274500
max(Cop_proc_max)  | 0.263
min(query)         | delete from test.tcs2 limit 5000;
min(prev_stmt)     |
digest             | 24bd6d8a9b238086c9b8c3d240ad4ef32f79ce94cf5a468c0b8fe1eb5f8d03df
```

上記の結果から、 `13:24:30`からバッチ削除の大規模な書き込みがあり、合計 196 回実行され、そのたびに 5,000 行のデータが削除され、合計所要時間は 46.8 秒であることがわかります。

### 例2 {#example-2}

大きなクエリが実行されていない場合、そのクエリはスロー ログに記録されません。この状況でも、この大きなクエリを診断することは可能です。次の例を参照してください。

![QPS results](/media/dashboard/dashboard-diagnostics-usage3.png)

もう一つの`go-ycsb`回の圧力テストの結果が上の画像に示されています。3 `2020-03-08 01:46:30` QPS が突然低下し始め、回復していないことがわかります。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-03-08 01:36:00` ～ `2020-03-08 01:41:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-03-08 01:46:30` ～ `2020-03-08 01:51:30` 。この範囲では、QPS が減少し始めました。

レポートが生成されると、**比較診断**ページでこのレポートを表示できます。

![Comparison diagnostics](/media/dashboard/dashboard-diagnostics-usage4.png)

診断結果は例 1 と同様です。上の画像の最後の行は、クエリが遅い可能性があることを示しており、SQL ステートメントを使用して TiDB ログ内のコストのかかるクエリを照会できることを示しています。SQL ステートメントの実行結果は次のとおりです。

```sql
> SELECT * FROM information_schema.cluster_log WHERE type='tidb' AND time >= '2020-03-08 01:46:30' AND time < '2020-03-08 01:51:30' AND level = 'warn' AND message LIKE '%expensive_query%'\G
TIME     | 2020/03/08 01:47:35.846
TYPE     | tidb
INSTANCE | 172.16.5.40:4009
LEVEL    | WARN
MESSAGE  | [expensivequery.go:167] [expensive_query] [cost_time=60.085949605s] [process_time=2.52s] [wait_time=2.52s] [request_count=9] [total_keys=996009] [process_keys=996000] [num_cop_tasks=9] [process_avg_time=0.28s] [process_p90_time=0.344s] [process_max_time=0.344s] [process_max_addr=172.16.5.40:20150] [wait_avg_time=0.000777777s] [wait_p90_time=0.003s] [wait_max_time=0.003s] [wait_max_addr=172.16.5.40:20150] [stats=t_wide:pseudo] [conn_id=19717] [user=root] [database=test] [table_ids="[80,80]"] [txn_start_ts=415132076148785201] [mem_max="23583169 Bytes (22.490662574768066 MB)"] [sql="select count(*) from t_wide as t1 join t_wide as t2 where t1.c0>t2.c1 and t1.c2>0"]
```

上記のクエリ結果は、この`172.16.5.40:4009` TiDB インスタンスの`2020/03/08 01:47:35.846`に、60 秒間実行されたがまだ実行が完了していない高価なクエリがあることを示しています。このクエリは、デカルト積の結合です。

## 比較診断レポートを使用して問題を特定する {#locate-problems-using-comparison-diagnostic-report}

診断結果が間違っている可能性があるため、比較レポートを使用すると DBA が問題をより迅速に特定できるようになります。次の例を参照してください。

![QPS results](/media/dashboard/dashboard-diagnostics-usage5.png)

`go-ycsb`圧力テストの結果が上の画像に示されています。3 で QPS が突然減少し始めたことがわかります。3 `2020-05-22 22:14:00`後、QPS は正常に戻り始めました。TiDB ダッシュボードの比較診断レポートを使用して原因を見つけることができます。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-05-22 22:11:00` ～ `2020-05-22 22:14:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-05-22 22:14:00` `2020-05-22 22:17:00`この範囲では、QPSが減少し始めました。

比較レポートを生成したら、**最大差分項目**レポートを確認します。このレポートは、上記の 2 つの時間範囲の監視項目を比較し、監視項目の差異に従って並べ替えます。この表の結果は次のようになります。

![Comparison results](/media/dashboard/dashboard-diagnostics-usage6.png)

上記の結果から、T2 のコプロセッサーリクエストが T1 よりもはるかに多いことがわかります。T2 にいくつかの大きなクエリが発生し、負荷が増大している可能性があります。

実際、T1 から T2 までの全時間範囲で、 `go-ycsb`圧力テストが実行されています。その後、T2 中に 20 個の`tpch`クエリが実行されます。したがって、多くのコプロセッサー要求を引き起こすのは`tpch`クエリです。

実行時間がスロー ログのしきい値を超えるような大規模なクエリがスロー ログに記録されている場合、 `Slow Queries In Time Range t2`レポートをチェックして、スロー クエリがあるかどうかを確認できます。ただし、T2 では他の負荷によって実行速度が低下するため、T1 の一部のクエリが T2 でもスロー クエリになる可能性があります。
