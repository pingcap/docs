---
title: Identify Expensive Queries
---

# 高価なクエリを特定する {#identify-expensive-queries}

TiDBを使用すると、SQL実行中にコストのかかるクエリを識別できるため、SQL実行の診断とパフォーマンスの向上を実現できます。具体的には、TiDBは、実行時間が[`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold) （デフォルトでは60秒）を超える、またはメモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) （デフォルトでは1 GB）を超えるステートメントに関する情報を[tidb-serverログファイル](/tidb-configuration-file.md#logfile) （デフォルトでは「tidb.log」）に出力します。

> **ノート：**
>
> 高価なクエリログは、次の点で[遅いクエリログ](/identify-slow-queries.md)とは異なります。TiDBは、ステートメントがリソース使用量のしきい値（実行時間またはメモリ使用量）を超える**とすぐに**、ステートメント情報を高価なクエリログに出力します。一方、TiDBは、ステートメントの実行<strong>後</strong>にステートメント情報を低速クエリログに出力します。

## 高価なクエリログの例 {#expensive-query-log-example}

```sql
[2020/02/05 15:32:25.096 +08:00] [WARN] [expensivequery.go:167] [expensive_query] [cost_time=60.008338935s] [wait_time=0s] [request_count=1] [total_keys=70] [process_keys=65] [num_cop_tasks=1] [process_avg_time=0s] [process_p90_time=0s] [process_max_time=0s] [process_max_addr=10.0.1.9:20160] [wait_avg_time=0.002s] [wait_p90_time=0.002s] [wait_max_time=0.002s] [wait_max_addr=10.0.1.9:20160] [stats=t:pseudo] [conn_id=60026] [user=root] [database=test] [table_ids="[122]"] [txn_start_ts=414420273735139329] [mem_max="1035 Bytes (1.0107421875 KB)"] [sql="insert into t select sleep(1) from t"]
```

## フィールドの説明 {#fields-description}

基本フィールド：

-   `cost_time` ：ログを出力するときのステートメントの実行時間。
-   `stats` ：ステートメントに含まれるテーブルまたはインデックスによって使用される統計のバージョン。値が`pseudo`の場合、使用可能な統計がないことを意味します。この場合、テーブルまたはインデックスを分析する必要があります。
-   `table_ids` ：ステートメントに含まれるテーブルのID。
-   `txn_start_ts` ：開始タイムスタンプとトランザクションの一意のID。この値を使用して、トランザクション関連のログを検索できます。
-   `sql` ：sqlステートメント。

メモリ使用量関連フィールド：

-   `mem_max` ：ログ印刷時のステートメントのメモリ使用量。このフィールドには、メモリ使用量を測定するための2種類の単位があります。バイトとその他の読み取り可能で適応可能な単位（MBやGBなど）です。

ユーザー関連フィールド：

-   `user` ：ステートメントを実行するユーザーの名前。
-   `conn_id` ：接続ID（セッションID）。たとえば、キーワード`con:60026`を使用して、セッションIDが`60026`のログを検索できます。
-   `database` ：ステートメントが実行されるデータベース。

TiKVコプロセッサーのタスク関連フィールド：

-   `wait_time` ：TiKVのステートメントのすべてのコプロセッサー要求の合計待機時間。 TiKVのコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが機能しているときに要求がキューに入れられる可能性があります。キュー内のリクエストの処理に時間がかかると、後続のリクエストの待機時間が長くなります。
-   `request_count` ：ステートメントが送信するコプロセッサー要求の数。
-   `total_keys` ：コプロセッサーがスキャンしたキーの数。
-   `processed_keys` ：コプロセッサーが処理したキーの数。 `total_keys`と比較すると、 `processed_keys`には古いバージョンのMVCCが含まれていません。 `processed_keys`と`total_keys`の大きな違いは、多くの古いバージョンが存在することを示しています。
-   `num_cop_tasks` ：ステートメントが送信するコプロセッサー要求の数。
-   `process_avg_time` ：コプロセッサータスクの平均実行時間。
-   `process_p90_time` ：コプロセッサータスクのP90実行時間。
-   `process_max_time` ：コプロセッサータスクの最大実行時間。
-   `process_max_addr` ：実行時間が最も長いコプロセッサータスクのアドレス。
-   `wait_avg_time` ：コプロセッサータスクの平均待機時間。
-   `wait_p90_time` ：コプロセッサータスクのP90待機時間。
-   `wait_max_time` ：コプロセッサータスクの最大待機時間。
-   `wait_max_addr` ：待機時間が最も長いコプロセッサータスクのアドレス。
