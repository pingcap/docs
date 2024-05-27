---
title: Identify Expensive Queries
summary: TiDB は、実行時間またはメモリ使用量のしきい値を超えるステートメントに関する情報を出力して、コストの高いクエリを識別するのに役立ちます。これにより、SQL パフォーマンスの診断と改善が可能になります。コストの高いクエリ ログには、実行時間、メモリ使用量、ユーザー、データベース、TiKVコプロセッサータスク情報などの詳細が含まれます。このログは、ステートメントがリソースしきい値を超えるとすぐに情報を出力ため、低速クエリ ログとは異なります。
---

# コストの高いクエリを特定する {#identify-expensive-queries}

TiDB を使用すると、SQL 実行中にコストの高いクエリを識別できるため、SQL 実行のパフォーマンスを診断して改善できます。具体的には、TiDB は、実行時間が[`tidb_expensive_query_time_threshold`](/system-variables.md#tidb_expensive_query_time_threshold) (デフォルトでは 60 秒) を超えるか、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) (デフォルトでは 1 GB) を超えるステートメントに関する情報を[tidb-server ログファイル](/tidb-configuration-file.md#logfile) (デフォルトでは &quot;tidb.log&quot;) に出力します。

> **注記：**
>
> 高価なクエリ ログは、次の点で[スロークエリログ](/identify-slow-queries.md)と異なります。TiDB は、ステートメントがリソース使用量 (実行時間またはメモリ使用量) のしきい値を超える**とすぐに**ステートメント情報を高価なクエリ ログに出力。一方、TiDB は、ステートメントの実行**後に**ステートメント情報を低速クエリ ログに出力。

## 高価なクエリログの例 {#expensive-query-log-example}

```sql
[2020/02/05 15:32:25.096 +08:00] [WARN] [expensivequery.go:167] [expensive_query] [cost_time=60.008338935s] [wait_time=0s] [request_count=1] [total_keys=70] [process_keys=65] [num_cop_tasks=1] [process_avg_time=0s] [process_p90_time=0s] [process_max_time=0s] [process_max_addr=10.0.1.9:20160] [wait_avg_time=0.002s] [wait_p90_time=0.002s] [wait_max_time=0.002s] [wait_max_addr=10.0.1.9:20160] [stats=t:pseudo] [conn_id=60026] [user=root] [database=test] [table_ids="[122]"] [txn_start_ts=414420273735139329] [mem_max="1035 Bytes (1.0107421875 KB)"] [sql="insert into t select sleep(1) from t"]
```

## フィールドの説明 {#fields-description}

基本フィールド:

-   `cost_time` : ログが印刷されるときのステートメントの実行時間。
-   `stats` : ステートメントに関係するテーブルまたはインデックスによって使用される統計のバージョン。値が`pseudo`の場合、使用可能な統計がないことを意味します。この場合、テーブルまたはインデックスを分析する必要があります。
-   `table_ids` : ステートメントに関係するテーブルの ID。
-   `txn_start_ts` : トランザクションの開始タイムスタンプと一意の ID。この値を使用して、トランザクション関連のログを検索できます。
-   `sql` : SQL ステートメント。

メモリ使用量関連のフィールド:

-   `mem_max` : ログが印刷されるときのステートメントのメモリ使用量。このフィールドには、メモリ使用量を測定するための 2 種類の単位があります。バイトと、その他の読み取り可能で適応可能な単位 (MB や GB など) です。

ユーザー関連フィールド:

-   `user` : ステートメントを実行するユーザーの名前。
-   `conn_id` : 接続 ID (セッション ID)。たとえば、キーワード`con:60026`を使用して、セッション ID が`60026`のログを検索できます。
-   `database` : ステートメントが実行されるデータベース。

TiKVコプロセッサー関連フィールド:

-   `wait_time` : TiKV 内のステートメントのすべてのコプロセッサー要求の合計待機時間。TiKV のコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが動作しているときに要求がキューに入れられることがあります。キュー内の要求の処理に時間がかかる場合、後続の要求の待機時間が長くなります。
-   `request_count` : ステートメントが送信するコプロセッサー要求の数。
-   `total_keys` :コプロセッサーがスキャンしたキーの数。
-   `processed_keys` :コプロセッサーが処理したキーの数。 `total_keys`と比較すると、 `processed_keys` MVCC の古いバージョンは含まれません。 `processed_keys`と`total_keys`の大きな差は、多くの古いバージョンが存在することを示しています。
-   `num_cop_tasks` : ステートメントが送信するコプロセッサー要求の数。
-   `process_avg_time` :コプロセッサータスクの平均実行時間。
-   `process_p90_time` :コプロセッサータスクの P90 実行時間。
-   `process_max_time` :コプロセッサータスクの最大実行時間。
-   `process_max_addr` : 実行時間が最も長いコプロセッサータスクのアドレス。
-   `wait_avg_time` :コプロセッサータスクの平均待機時間。
-   `wait_p90_time` :コプロセッサータスクの P90 待機時間。
-   `wait_max_time` :コプロセッサータスクの最大待機時間。
-   `wait_max_addr` : 待機時間が最も長いコプロセッサータスクのアドレス。
