---
title: Understanding Stale Read and safe-ts in TiKV
summary: Introduce the principles of Stale Read and safe-ts in TiKV and provide troubleshooting tips and examples for diagnosing common issues related to Stale Read.
---

# TiKV のステイル読み取りとsafe-tsを理解する {#understanding-stale-read-and-safe-ts-in-tikv}

このガイドでは、TiKV のステイル読み取りとsafe-ts について、またステイル読み取りに関連する一般的な問題を診断する方法について学習できます。

## ステイル読み取りとsafe-tsの概要 {#overview-of-stale-read-and-safe-ts}

[ステイル読み取り](/stale-read.md)は、TiDB に保存されているデータの履歴バージョンを読み取るために TiDB が適用するメカニズムです。 TiKV では、 ステイル読み取り は[セーフ-TS](/#what-is-safe-ts)に依存します。リージョンピア上の読み取りリクエストのタイムスタンプ (ts) がリージョンのsafe-ts 以下である場合、TiDB はピアからデータを安全に読み取ることができます。 TiKV は、safe-ts が常に[resolved-ts](#what-is-resolved-ts)以下であることを保証することで、この安全性保証を実装します。

## 安全なTSとresolved-tsを理解する {#understand-safe-ts-and-resolved-ts}

このセクションでは、safe-ts とresolved-tsの概念とメンテナンスについて説明します。

### セーフTSとは何ですか？ {#what-is-safe-ts}

safe-ts は、リージョン内の各ピアが維持するタイムスタンプです。この値より小さいタイムスタンプを持つすべてのトランザクションがローカルに適用されていることを確認し、ローカルのステイル読み取りを有効にします。

### resolved-tsとは何ですか? {#what-is-resolved-ts}

resolved-ts は、この値より小さいタイムスタンプを持つすべてのトランザクションがリーダーによって適用されていることを保証するタイムスタンプです。ピアの概念であるsafe-tsとは異なり、 resolved-tsはリージョンリーダーによってのみ維持されます。フォロワーはリーダーよりも適用インデックスが小さい可能性があるため、resolved-ts をフォロワー内で安全な t として直接扱うことはできません。

### 安全なTSのメンテナンス {#the-maintenance-of-safe-ts}

`RegionReadProgress`モジュールは安全性を維持します。リージョンリーダーは、 resolved-tsを維持し、そのresolved-ts、最小限必要な適用インデックス (このresolved-ts を検証する)、およびリージョン自体を CheckLeader RPC 経由ですべてのレプリカの`RegionReadProgerss`のモジュールに定期的に送信します。

ピアがデータを適用すると、適用インデックスが更新され、保留中のresolved-ts が新しい安全 T になり得るかどうかがチェックされます。

### resolved-tsのメンテナンス {#the-maintenance-of-resolved-ts}

リージョンリーダーは、リゾルバーを使用して、 resolved-tsを管理します。このリゾルバーは、 Raft が適用されるときに変更ログを受信することによって、LOCK CF (カラムファミリー) のロックを追跡します。初期化されると、リゾルバはリージョン全体をスキャンしてロックを追跡します。

## ステイル読み取りの問題を診断する {#diagnose-stale-read-issues}

このセクションでは、Grafana、 `tikv-ctl` 、およびログを使用してステイル読み取りの問題を診断する方法を紹介します。

### 問題を特定する {#identify-issues}

[Grafana &gt; TiDB ダッシュボード &gt; **KV リクエスト**ダッシュボード](/grafana-tidb-dashboard.md#kv-request)では、次のパネルにステイル読み取りのヒット率、OPS、トラフィックが表示されます。

![Stale Read Hit/Miss OPS](/media/stale-read/metrics-hit-miss.png)

![Stale Read Req OPS](/media/stale-read/metrics-ops.png)

![Stale Read Req Traffic](/media/stale-read/traffic.png)

前述のメトリクスの詳細については、 [TiDB モニタリングメトリクス](/grafana-tidb-dashboard.md#kv-request)を参照してください。

ステイル読み取りの問題が発生すると、前述のメトリックの変化に気づく場合があります。最も直接的な指標は TiDB からの WARN ログで、リージョンID を含む`DataIsNotReady`と、検出された`safe-ts`報告します。

### よくある原因 {#common-causes}

ステイル読み取りの有効性に影響を与える可能性のある最も一般的な原因は次のとおりです。

-   コミットに長時間かかるトランザクション。
-   トランザクションがコミットされるまでの期間が長すぎます。
-   CheckLeader の情報をリーダーからフォロワーにプッシュする際の遅延。

### Grafana を使用して診断する {#use-grafana-to-diagnose}

[**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)では、各 TiKV の最小のresolved-tsと安全な ts を持つリージョンを識別できます。これらのタイムスタンプがリアルタイムより大幅に遅れている場合は、 `tikv-ctl`使用してこれらのリージョンの詳細を確認する必要があります。

### <code>tikv-ctl</code>使用して診断する {#use-code-tikv-ctl-code-to-diagnose}

`tikv-ctl`リゾルバーの最新の詳細を提供し、 `RegionReadProgress`リゾルバーの最新の詳細を提供します。詳細については、 [リージョンの`RegionReadProgress`の状態を取得する](/tikv-control.md#get-the-state-of-a-regions-regionreadprogress)を参照してください。

以下は例です。

```bash
./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 14 --log --min-start-ts 0
```

出力は次のとおりです。

```log
Region read progress:
    exist: true,
    safe_ts: 0,
    applied_index: 92,
    pending front item (oldest) ts: 0,
    pending front item (oldest) applied index: 0,
    pending back item (latest) ts: 0,
    pending back item (latest) applied index: 0,
    paused: false,
Resolver:
    exist: true,
    resolved_ts: 0,
    tracked index: 92,
    number of locks: 0,
    number of transactions: 0,
    stopped: false,
```

前述の出力は、以下を判断するのに役立ちます。

-   ロックがresolved-tsをブロックしているかどうか。
-   適用インデックスが小さすぎて、safe-ts を更新できないかどうか。
-   フォロワーピアが存在する場合、リーダーが十分に更新されたresolved-tsを送信しているかどうか。

### ログを使用して診断する {#use-logs-to-diagnose}

TiKV は 10 秒ごとに次のメトリクスをチェックします。

-   resolved-tsが最小であるリージョンリーダー
-   safety-ts が最小であるリージョンフォロワー
-   resolved-tsが最小であるリージョンフォロワー

これらのタイムスタンプのいずれかが異常に小さい場合、TiKV はログを出力。

これらのログは、現在は存在しない過去の問題を診断する場合に特に役立ちます。

以下にログの例を示します。

```log
[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:505] ["the max gap of leader resolved-ts is large"] [last_resolve_attempt="Some(LastAttempt { success: false, ts: TimeStamp(443888082736381953), reason: \"lock\", lock: Some(7480000000000000625F728000000002512B5C) })"] [duration_to_last_update_safe_ts=10648ms] [min_memory_lock=None] [txn_num=0] [lock_num=0] [min_lock=None] [safe_ts=443888117326544897] [gap=110705ms] [region_id=291]

[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:526] ["the max gap of follower safe-ts is large"] [oldest_candidate=None] [latest_candidate=None] [applied_index=3276] [duration_to_last_consume_leader=11460ms] [resolved_ts=443888117117353985] [safe_ts=443888117117353985] [gap=111503ms] [region_id=273]

[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:547] ["the max gap of follower resolved-ts is large; it's the same region that has the min safe-ts"]
```

## トラブルシューティングのヒント {#troubleshooting-tips}

### 遅いトランザクションのコミットを処理する {#handle-slow-transaction-commit}

コミットに時間がかかるトランザクションは、多くの場合、大規模なトランザクションです。この遅いトランザクションの事前書き込みフェーズではいくつかのロックが残りますが、コミットフェーズでロックが消去されるまでに時間がかかりすぎます。この問題をトラブルシューティングするには、ログを使用するなどして、ロックが属しているトランザクションを特定し、ロックが存在する理由を正確に特定することを試みることができます。

以下に、実行できるアクションをいくつかリストします。

-   `tikv-ctl`コマンドで`--log`オプションを指定し、TiKV ログをチェックして、start_ts を持つ特定のロックを見つけます。

-   TiDB ログと TiKV ログの両方で start_ts を検索して、トランザクションの問題を特定します。

    クエリに 60 秒以上かかる場合、SQL ステートメントとともに`expensive_query`ログが出力されます。 start_ts 値を使用してログと一致させることができます。以下は例です。

    ```log
    [2023/07/17 19:32:09.403 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.025022732s] [cop_time=0.00346666s] [process_time=8.358409508s] [wait_time=0.013582596s] [request_count=278] [total_keys=9943616] [process_keys=9943360] [num_cop_tasks=278] [process_avg_time=0.030066221s] [process_p90_time=0.045296042s] [process_max_time=0.052828934s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000048858s] [wait_p90_time=0.00006057s] [wait_max_time=0.00040991s] [wait_max_addr=192.168.31.244:20160] [stats=t:442916666913587201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[100]"] [**txn_start_ts**=442916790435840001] [mem_max="2514229289 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]
    ```

-   ログからロックに関する十分な情報を取得できない場合は、 [`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md#cluster_tidb_trx)テーブルを使用してアクティブなトランザクションを見つけます。

-   [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)を実行すると、同じ TiDBサーバーに接続されている現在のセッションと、現在のステートメントに費やされた時間が表示されます。しかし、start_ts は表示されません。

進行中の大規模なトランザクションによってロックが存在する場合は、これらのロックがresolve-tsの進行を妨げる可能性があるため、アプリケーションロジックを変更することを検討してください。

ロックが進行中のトランザクションに属していない場合は、ロックを事前に書き込んだ後にコーディネーター (TiDB) がクラッシュしたことが原因である可能性があります。この場合、TiDB は自動的にロックを解決します。問題が解決しない限り、対処の必要はありません。

### 存続期間の長いトランザクションを処理する {#handle-long-lived-transactions}

トランザクションが長期間アクティブのままであると、たとえ最終的にはすぐにコミットされたとしても、 resolved-tsの進行がブロックされる可能性があります。これは、 resolved-tsの計算に使用されるのは、これらの長期トランザクションの start-ts であるためです。

この問題に対処するには:

-   トランザクションを特定する : まず、ロックに関連付けられているトランザクションを特定することから始めます。それらの存在の背後にある理由を理解することが重要です。ログの活用は特に役立ちます。

-   アプリケーション ロジックを調査する: トランザクション期間の延長がアプリケーションのロジックの結果である場合は、そのような事態が発生しないようにアプリケーション ロジックを修正することを検討してください。

-   遅いクエリに対処する: 遅いクエリが原因でトランザクションの時間が延長される場合は、問題を軽減するためにこれらのクエリの解決を優先します。

### CheckLeader の問題に対処する {#address-checkleader-issues}

CheckLeader の問題に対処するには、 [**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)でネットワークと**チェックLeader期間**メトリックを確認します。

## 例 {#example}

次のように、 **ステイル読み取り OPS**のミス率が増加していることが観察された場合:

![Example: Stale Read OPS](/media/stale-read/example-ops.png)

まず、 [**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)で**最大解決 TS ギャップ**と**最小解決 TSリージョン**メトリクスを確認できます。

![Example: Max Resolved TS gap](/media/stale-read/example-ts-gap.png)

前述のメトリクスから、リージョン`3121`と他の一部のリージョンがresolved-ts を時間内に更新していないことがわかります。

リージョン`3121`の状態に関する詳細を取得するには、次のコマンドを実行します。

```bash
./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 3121 --log
```

出力は次のとおりです。

```log
Region read progress:
    exist: true,
    safe_ts: 442918444145049601,
    applied_index: 2477,
    read_state.ts: 442918444145049601,
    read_state.apply_index: 1532,
    pending front item (oldest) ts: 0,
    pending front item (oldest) applied index: 0,
    pending back item (latest) ts: 0,
    pending back item (latest) applied index: 0,
    paused: false,
    discarding: false,
Resolver:
    exist: true,
    resolved_ts: 442918444145049601,
    tracked index: 2477,
    number of locks: 480000,
    number of transactions: 1,
    stopped: false,
```

ここで注目すべき点は、リゾルバでは`applied_index` `tracked index`に等しいということです。したがって、リゾルバーがこの問題の根本であると考えられます。また、このリージョンに 480000 個のロックを残すトランザクションが 1 つあることもわかります。これが原因である可能性があります。

正確なトランザクションと一部のロックのキーを取得するには、TiKV ログを確認し、 grep `locks with`を実行します。出力は次のとおりです。

```log
[2023/07/17 21:16:44.257 +08:00] [INFO] [resolver.rs:213] ["locks with the minimum start_ts in resolver"] [keys="[74800000000000006A5F7280000000000405F6, ... , 74800000000000006A5F72800000000000EFF6, 74800000000000006A5F7280000000000721D9, 74800000000000006A5F72800000000002F691]"] [start_ts=442918429687808001] [region_id=3121]
```

TiKV ログから、トランザクションの start_ts `442918429687808001`を取得できます。ステートメントとトランザクションに関する詳細情報を取得するには、TiDB ログ内のこのタイムスタンプを grep します。出力は次のとおりです。

```log
[2023/07/17 21:16:18.287 +08:00] [INFO] [2pc.go:685] ["[BIG_TXN]"] [session=2826881778407440457] ["key sample"=74800000000000006a5f728000000000000000] [size=319967171] [keys=10000000] [puts=10000000] [dels=0] [locks=0] [checks=0] [txnStartTS=442918429687808001]

[2023/07/17 21:16:22.703 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.047172498s] [cop_time=0.004575113s] [process_time=15.356963423s] [wait_time=0.017093811s] [request_count=397] [total_keys=20000398] [process_keys=10000000] [num_cop_tasks=397] [process_avg_time=0.038682527s] [process_p90_time=0.082608262s] [process_max_time=0.116321331s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000043057s] [wait_p90_time=0.00004007s] [wait_max_time=0.00075014s] [wait_max_addr=192.168.31.244:20160] [stats=t:442918428521267201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[106]"] [txn_start_ts=442918429687808001] [mem_max="2513773983 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]
```

その後、基本的に、問題の原因となったステートメントを特定できます。さらに詳しく確認するには、 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)ステートメントを実行します。出力は次のとおりです。

```sql
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| Id                  | User | Host                | db     | Command | Time | State      | Info                      |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| 2826881778407440457 | root | 192.168.31.43:58641 | test   | Query   | 48   | autocommit | update t set b = b + 1    |
| 2826881778407440613 | root | 127.0.0.1:45952     | test   | Execute | 0    | autocommit | select * from t where a=? |
| 2826881778407440619 | root | 192.168.31.43:60428 | <null> | Query   | 0    | autocommit | show processlist          |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
```

出力は、誰かが予期しない`UPDATE`ステートメント ( `update t set b = b + 1` ) を実行していることを示しています。これにより、大規模なトランザクションが発生し、 ステイル読み取りが妨げられます。

この問題を解決するには、この`UPDATE`ステートメントを実行しているアプリケーションを停止します。
