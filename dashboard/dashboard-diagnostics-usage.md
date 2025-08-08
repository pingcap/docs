---
title: Locate Problems Using Diagnostic Report of TiDB Dashboard
summary: TiDBダッシュボードの診断レポートは、異なる時間範囲でのシステムパフォーマンスを比較することで、問題箇所の特定に役立ちます。QPSの低下、レイテンシーの増加、クエリの遅延といった問題を特定し、詳細な分析結果とSQL文を提供することで、さらなる調査に役立ちます。この比較レポートは、パフォーマンスの問題を迅速に特定し、対処するために不可欠です。
---

# TiDBダッシュボードの診断レポートを使用して問題を特定する {#locate-problems-using-diagnostic-report-of-tidb-dashboard}

このドキュメントでは、TiDB ダッシュボードの診断レポートを使用して問題を特定する方法を紹介します。

## 比較診断 {#comparison-diagnostics}

このセクションでは、比較診断機能を使用して、大規模なクエリや書き込みによって発生する QPS ジッターまたはレイテンシーの増加を診断する方法を説明します。

### 例1 {#example-1}

![QPS example](/media/dashboard/dashboard-diagnostics-usage1.png)

`go-ycsb` `2020-03-10 13:24:30`テストの結果は上の画像に示されています。3でQPSが急激に低下し始めたことがわかります。3分後、QPSは正常に戻り始めました。TiDBダッシュボードの診断レポートを使用して原因を特定できます。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-03-10 13:21:00` ～ `2020-03-10 13:23:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-03-10 13:24:30` ～ `2020-03-10 13:27:30` 。この範囲ではQPSが減少し始めました。

ジッタの影響範囲は3分であるため、上記の2つの時間範囲はどちらも3分です。診断時には監視された平均値を比較するため、範囲が長すぎると平均値の差が無視され、問題箇所を正確に特定できなくなります。

レポートが生成されると、**比較診断**ページでこのレポートを表示できます。

![Comparison diagnostics](/media/dashboard/dashboard-diagnostics-usage2.png)

上記の診断結果は、診断時間中に大きなクエリが存在する可能性があることを示しています。上記のレポートの各**「詳細」**は以下のように説明されています。

-   `tidb_qps` : QPSが0.93倍減少しました。
-   `tidb_query_duration` : P999 クエリのレイテンシーが1.54 倍増加しました。
-   `tidb_cop_duration` : P999 コプロセッサ要求の処理レイテンシーが 2.48 倍に増加しました。
-   `tidb_kv_write_num` : P999 TiDB トランザクションで書き込まれた KV の数は 7.61 倍に増加しました。
-   `tikv_cop_scan_keys_total_nun` : TiKVコプロセッサーによってスキャンされるキー/値の数が 3 つの TiKV インスタンスで大幅に改善されました。
-   `pd_operator_step_finish_total_count`では、転属リーダー数が2.45倍に増加しており、異常時間帯のスケジュールが正常時間帯のスケジュールよりも高くなっていることがわかります。
-   このレポートは、遅いクエリが存在する可能性があることを示しており、SQL文を使用して遅いクエリを照会できることを示しています。SQL文の実行結果は次のとおりです。

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

上記の結果から、 `13:24:30`から、バッチ削除の大規模な書き込みがあり、合計 196 回実行され、そのたびに 5,000 行のデータが削除され、合計所要時間は 46.8 秒であることがわかります。

### 例2 {#example-2}

大規模なクエリが実行されていない場合、そのクエリはスローログに記録されません。この状況でも、この大規模なクエリを診断することは可能です。次の例をご覧ください。

![QPS results](/media/dashboard/dashboard-diagnostics-usage3.png)

もう`go-ycsb`圧力テストの結果を上の`2020-03-08 01:46:30`に示します。3でQPSが急激に低下し始め、回復していないことがわかります。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-03-08 01:36:00` ～ `2020-03-08 01:41:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-03-08 01:46:30` ～ `2020-03-08 01:51:30` 。この範囲ではQPSが減少し始めました。

レポートが生成されると、**比較診断**ページでこのレポートを表示できます。

![Comparison diagnostics](/media/dashboard/dashboard-diagnostics-usage4.png)

診断結果は例1と同様です。上の画像の最後の行は、遅いクエリが存在する可能性があることを示しており、TiDBログ内の高負荷なクエリをSQL文で照会できることを示しています。SQL文の実行結果は次のとおりです。

```sql
> SELECT * FROM information_schema.cluster_log WHERE type='tidb' AND time >= '2020-03-08 01:46:30' AND time < '2020-03-08 01:51:30' AND level = 'warn' AND message LIKE '%expensive_query%'\G
TIME     | 2020/03/08 01:47:35.846
TYPE     | tidb
INSTANCE | 172.16.5.40:4009
LEVEL    | WARN
MESSAGE  | [expensivequery.go:167] [expensive_query] [cost_time=60.085949605s] [process_time=2.52s] [wait_time=2.52s] [request_count=9] [total_keys=996009] [process_keys=996000] [num_cop_tasks=9] [process_avg_time=0.28s] [process_p90_time=0.344s] [process_max_time=0.344s] [process_max_addr=172.16.5.40:20150] [wait_avg_time=0.000777777s] [wait_p90_time=0.003s] [wait_max_time=0.003s] [wait_max_addr=172.16.5.40:20150] [stats=t_wide:pseudo] [conn_id=19717] [user=root] [database=test] [table_ids="[80,80]"] [txn_start_ts=415132076148785201] [mem_max="23583169 Bytes (22.490662574768066 MB)"] [sql="select count(*) from t_wide as t1 join t_wide as t2 where t1.c0>t2.c1 and t1.c2>0"]
```

上記のクエリ結果は、このTiDBインスタンス`172.16.5.40:4009`の`2020/03/08 01:47:35.846`において、60秒間実行されている高負荷なクエリがまだ完了していないことを示しています。このクエリは、カルテシアン積の結合です。

## 比較診断レポートを使用して問題を特定する {#locate-problems-using-comparison-diagnostic-report}

診断結果が誤っている可能性があるため、比較レポートを使用すると、DBAが問題をより迅速に特定できる可能性があります。次の例をご覧ください。

![QPS results](/media/dashboard/dashboard-diagnostics-usage5.png)

`go-ycsb` `2020-05-22 22:14:00`テストの結果は上の画像に示されています。3でQPSが急激に低下し始めたことがわかります。3分後、QPSは正常に戻り始めました。TiDBダッシュボードの比較診断レポートを使用して、原因を特定できます。

次の 2 つの時間範囲でシステムを比較するレポートを生成します。

T1: `2020-05-22 22:11:00` ～ `2020-05-22 22:14:00` 。この範囲ではシステムは正常であり、基準範囲と呼ばれます。

T2: `2020-05-22 22:14:00` `2020-05-22 22:17:00`この範囲でQPSは減少し始めました。

比較レポートを生成したら、 **「最大差分項目**レポート」を確認してください。このレポートは、上記の2つの期間の監視項目を比較し、監視項目の差異に応じて並べ替えます。この表の結果は以下のとおりです。

![Comparison results](/media/dashboard/dashboard-diagnostics-usage6.png)

上記の結果から、T2のコプロセッサーリクエストがT1よりもはるかに多いことがわかります。T2で大規模なクエリがいくつか発生し、それが負荷の増加につながっている可能性があります。

実際、T1からT2までの全期間を通じて、 `go-ycsb`負荷テストが実行されています。その後、T2の間に`tpch`クエリが20回実行されています。つまり、多くのコプロセッサーリクエストを引き起こしているのは、この`tpch`クエリです。

実行時間がスローログのしきい値を超えるような大規模なクエリがスローログに記録されている場合、レポート`Slow Queries In Time Range t2`でスロークエリの有無を確認できます。ただし、T1のクエリの中には、T2では他の負荷によって実行速度が低下するため、T2でもスロークエリになるクエリが存在する可能性があります。
