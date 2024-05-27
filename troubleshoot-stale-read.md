---
title: Understanding Stale Read and safe-ts in TiKV
summary: TiKV のステイル読み取りと safe-ts の原理を紹介し、 ステイル読み取りに関連する一般的な問題を診断するためのトラブルシューティングのヒントと例を示します。
---

# TiKV のステイル読み取りと safe-ts を理解する {#understanding-stale-read-and-safe-ts-in-tikv}

このガイドでは、TiKV のステイル読み取りと safe-ts について、またステイル読み取りに関連する一般的な問題を診断する方法について説明します。

## ステイル読み取りと safe-ts の概要 {#overview-of-stale-read-and-safe-ts}

[ステイル読み取り](/stale-read.md) 、TiDB が TiDB に保存されているデータの履歴バージョンを読み取るために適用するメカニズムです。TiKV では、 ステイル読み取り は[セーフティー](/#what-is-safe-ts)に依存します。リージョンピアの読み取り要求のタイムスタンプ (ts) がリージョンの safe-ts 以下である場合、TiDB はピアからデータを安全に読み取ることができます。TiKV は、safe-ts が常に[resolved-ts](#what-is-resolved-ts)以下であることを保証することで、この安全性の保証を実装します。

## safe-tsとresolved-tsを理解する {#understand-safe-ts-and-resolved-ts}

このセクションでは、 safe-ts とresolved-tsの概念とメンテナンスについて説明します。

### safe-tsとは何ですか? {#what-is-safe-ts}

safe-ts は、リージョン内の各ピアが維持するタイムスタンプです。これにより、タイムスタンプがこの値より小さいすべてのトランザクションがローカルに適用され、ローカルのステイル読み取りが有効になります。

### resolved-tsとは何ですか? {#what-is-resolved-ts}

resolved-ts は、タイムスタンプがこの値より小さいすべてのトランザクションがリーダーによって適用されていることを保証するタイムスタンプです。ピア コンセプトである safe-ts とは異なり、resolved-tsはリージョンリーダーによってのみ管理されます。フォロワーの適用インデックスはリーダーよりも小さい可能性があるため、フォロワーではresolved-ts を直接 safe-ts として扱うことはできません。

### セーフティーの維持 {#the-maintenance-of-safe-ts}

`RegionReadProgress`モジュールは safe-ts を維持します。リージョンリーダーは、 resolved-tsを維持し、そのresolved-ts、このresolved-tsを検証する最低限必要な適用インデックス、およびリージョン自体を、CheckLeader RPC を介してすべてのレプリカの`RegionReadProgerss`モジュールに定期的に送信します。

ピアがデータを適用すると、適用インデックスが更新され、保留中のresolved-tsが新しい safe-ts になるかどうかがチェックされます。

### resolved-tsのメンテナンス {#the-maintenance-of-resolved-ts}

リージョンリーダーは、resolved-tsを管理するためにリゾルバを使用します。このリゾルバは、 Raftが適用されたときに変更ログを受信することで、LOCK CF (カラムファミリ) 内のロックを追跡します。初期化されると、リゾルバはリージョン全体をスキャンしてロックを追跡します。

## ステイル読み取りの問題を診断する {#diagnose-stale-read-issues}

このセクションでは、Grafana、 `tikv-ctl` 、およびログを使用してステイル読み取り の問題を診断する方法を紹介します。

### 問題を特定する {#identify-issues}

[Grafana &gt; TiDBダッシュボード &gt; **KVリクエスト**ダッシュボード](/grafana-tidb-dashboard.md#kv-request)では、次のパネルにステイル読み取りのヒット率、OPS、トラフィックが表示されます。

![Stale Read Hit/Miss OPS](/media/stale-read/metrics-hit-miss.png)

![Stale Read Req OPS](/media/stale-read/metrics-ops.png)

![Stale Read Req Traffic](/media/stale-read/traffic.png)

上記のメトリックの詳細については、 [TiDB 監視メトリクス](/grafana-tidb-dashboard.md#kv-request)参照してください。

ステイル読み取り の問題が発生すると、前述のメトリックの変化に気付く場合があります。最も直接的な指標は、TiDB からの WARN ログで、リージョンID が`DataIsNotReady`で、検出された`safe-ts`が報告されます。

### 一般的な原因 {#common-causes}

ステイル読み取りの有効性に影響を与える最も一般的な原因は次のとおりです。

-   コミットに長い時間を要するトランザクション。
-   トランザクションはコミットされるまでに時間がかかりすぎます。
-   CheckLeader の情報をリーダーからフォロワーにプッシュする際の遅延。

### Grafanaを使用して診断する {#use-grafana-to-diagnose}

[**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)では、各 TiKV のresolved-tsと safe-ts が最も小さいリージョンを特定できます。これらのタイムスタンプがリアルタイムより大幅に遅れている場合は、 `tikv-ctl`使用してこれらのリージョンの詳細を確認する必要があります。

### <code>tikv-ctl</code>使用して診断する {#use-code-tikv-ctl-code-to-diagnose}

`tikv-ctl`リゾルバの最新の詳細情報を提供し、 `RegionReadProgress` 。詳細については[リージョンの`RegionReadProgress`の状態を取得する](/tikv-control.md#get-the-state-of-a-regions-regionreadprogress)を参照してください。

次に例を示します。

```bash
./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 14 --log --min-start-ts 0
```

出力は次のようになります。

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

上記の出力は、次のことを判断するのに役立ちます。

-   ロックがresolved-ts をブロックしているかどうか。
-   適用インデックスが safe-ts を更新するには小さすぎるかどうか。
-   フォロワー ピアが存在する場合に、リーダーが十分に更新されたresolved-tsを送信しているかどうか。

### ログを使用して診断する {#use-logs-to-diagnose}

TiKV は 10 秒ごとに次のメトリックをチェックします。

-   resolved-tsが最小であるリージョンリーダー
-   セーフティーが最小であるリージョンフォロワー
-   resolved-tsが最小であるリージョンフォロワー

これらのタイムスタンプのいずれかが異常に小さい場合、TiKV はログを出力。

これらのログは、現在は存在しない過去の問題を診断する場合に特に役立ちます。

ログの例を以下に示します。

```log
[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:505] ["the max gap of leader resolved-ts is large"] [last_resolve_attempt="Some(LastAttempt { success: false, ts: TimeStamp(443888082736381953), reason: \"lock\", lock: Some(7480000000000000625F728000000002512B5C) })"] [duration_to_last_update_safe_ts=10648ms] [min_memory_lock=None] [txn_num=0] [lock_num=0] [min_lock=None] [safe_ts=443888117326544897] [gap=110705ms] [region_id=291]

[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:526] ["the max gap of follower safe-ts is large"] [oldest_candidate=None] [latest_candidate=None] [applied_index=3276] [duration_to_last_consume_leader=11460ms] [resolved_ts=443888117117353985] [safe_ts=443888117117353985] [gap=111503ms] [region_id=273]

[2023/08/29 16:48:18.118 +08:00] [INFO] [endpoint.rs:547] ["the max gap of follower resolved-ts is large; it's the same region that has the min safe-ts"]
```

## トラブルシューティングのヒント {#troubleshooting-tips}

### 遅いトランザクションコミットを処理する {#handle-slow-transaction-commit}

コミットに長い時間がかかるトランザクションは、多くの場合、大規模なトランザクションです。この低速トランザクションの事前書き込みフェーズでは、いくつかのロックが残りますが、コミット フェーズでロックが消去されるまでに時間がかかりすぎます。この問題のトラブルシューティングを行うには、ロックが属するトランザクションを特定し、ログを使用するなどして、ロックが存在する理由を正確に突き止めます。

実行できるアクションをいくつか次に示します。

-   `tikv-ctl`コマンドで`--log`オプションを指定し、TiKV ログをチェックして、start_ts を持つ特定のロックを見つけます。

-   トランザクションの問題を特定するには、TiDB ログと TiKV ログの両方で start_ts を検索します。

    クエリに 60 秒以上かかる場合は、SQL ステートメントとともに`expensive_query`ログが出力されます。start_ts 値を使用してログを一致させることができます。次に例を示します。

    ```log
    [2023/07/17 19:32:09.403 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.025022732s] [cop_time=0.00346666s] [process_time=8.358409508s] [wait_time=0.013582596s] [request_count=278] [total_keys=9943616] [process_keys=9943360] [num_cop_tasks=278] [process_avg_time=0.030066221s] [process_p90_time=0.045296042s] [process_max_time=0.052828934s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000048858s] [wait_p90_time=0.00006057s] [wait_max_time=0.00040991s] [wait_max_addr=192.168.31.244:20160] [stats=t:442916666913587201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[100]"] [**txn_start_ts**=442916790435840001] [mem_max="2514229289 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]
    ```

-   ログからロックに関する十分な情報を取得できない場合は、 [`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md#cluster_tidb_trx)テーブルを使用してアクティブなトランザクションを見つけます。

-   [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)を実行すると、同じ TiDBサーバーに接続されている現在のセッションと、現在のステートメントに費やされた時間が表示されます。ただし、start_ts は表示されません。

進行中の大規模トランザクションが原因でロックが存在する場合は、これらのロックによって解決の進行が妨げられる可能性があるため、アプリケーション ロジックを変更することを検討してください。

ロックが進行中のトランザクションに属していない場合は、コーディネーター (TiDB) がロックを事前書き込みした後にクラッシュしたことが原因の可能性があります。この場合、TiDB は自動的にロックを解決します。問題が解決しない限り、アクションは必要ありません。

### 長期トランザクションを処理する {#handle-long-lived-transactions}

長時間アクティブなままのトランザクションは、最終的にすぐにコミットされるとしても、 resolved-tsの進行をブロックする可能性があります。これは、 resolved-tsの計算に使用されるのは、これらの長時間存続するトランザクションの start-ts であるためです。

この問題に対処するには:

-   トランザクションを識別する: まず、ロックに関連するトランザクションを特定します。ロックが存在する理由を理解することが重要です。ログを活用すると特に役立ちます。

-   アプリケーション ロジックを調べる: トランザクションの所要時間が長くなっている原因がアプリケーションのロジックにある場合は、そのような事態が発生しないようにロジックを修正することを検討してください。

-   遅いクエリに対処する: 遅いクエリが原因でトランザクションの期間が長くなる場合は、これらのクエリの解決を優先して問題を軽減します。

### CheckLeaderの問題に対処する {#address-checkleader-issues}

CheckLeader の問題に対処するには、 [**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)でネットワークと**Check Leader Duration**メトリックを確認します。

## 例 {#example}

次のように、 **ステイル読み取り OPS**のミス率が増加していることがわかります。

![Example: Stale Read OPS](/media/stale-read/example-ops.png)

まず、次の[**TiKV-詳細**&gt;**解決済み-TS**ダッシュボード](/grafana-tikv-dashboard.md#resolved-ts)の**最大解決 TS ギャップ**と**最小解決 TSリージョン**メトリックを確認できます。

![Example: Max Resolved TS gap](/media/stale-read/example-ts-gap.png)

上記のメトリックから、リージョン`3121`と他のいくつかのリージョンが、 resolved-ts を時間内に更新していないことがわかります。

リージョン`3121`の状態に関する詳細情報を取得するには、次のコマンドを実行します。

```bash
./tikv-ctl --host 127.0.0.1:20160 get-region-read-progress -r 3121 --log
```

出力は次のようになります。

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

ここで注目すべき点は、リゾルバの`applied_index` `tracked index`に等しいことです。したがって、リゾルバがこの問題の根本原因であると思われます。また、このリージョンに 480000 のロックを残すトランザクションが 1 つあることもわかります。これが原因である可能性があります。

正確なトランザクションと一部のロックのキーを取得するには、TiKV ログをチェックして grep `locks with`を実行します。出力は次のようになります。

```log
[2023/07/17 21:16:44.257 +08:00] [INFO] [resolver.rs:213] ["locks with the minimum start_ts in resolver"] [keys="[74800000000000006A5F7280000000000405F6, ... , 74800000000000006A5F72800000000000EFF6, 74800000000000006A5F7280000000000721D9, 74800000000000006A5F72800000000002F691]"] [start_ts=442918429687808001] [region_id=3121]
```

TiKV ログから、トランザクションの start_ts (つまり`442918429687808001`を取得できます。ステートメントとトランザクションに関する詳細情報を取得するには、TiDB ログでこのタイムスタンプを grep します。出力は次のようになります。

```log
[2023/07/17 21:16:18.287 +08:00] [INFO] [2pc.go:685] ["[BIG_TXN]"] [session=2826881778407440457] ["key sample"=74800000000000006a5f728000000000000000] [size=319967171] [keys=10000000] [puts=10000000] [dels=0] [locks=0] [checks=0] [txnStartTS=442918429687808001]

[2023/07/17 21:16:22.703 +08:00] [WARN] [expensivequery.go:145] [expensive_query] [cost_time=60.047172498s] [cop_time=0.004575113s] [process_time=15.356963423s] [wait_time=0.017093811s] [request_count=397] [total_keys=20000398] [process_keys=10000000] [num_cop_tasks=397] [process_avg_time=0.038682527s] [process_p90_time=0.082608262s] [process_max_time=0.116321331s] [process_max_addr=192.168.31.244:20160] [wait_avg_time=0.000043057s] [wait_p90_time=0.00004007s] [wait_max_time=0.00075014s] [wait_max_addr=192.168.31.244:20160] [stats=t:442918428521267201] [conn=2826881778407440457] [user=root] [database=test] [table_ids="[106]"] [txn_start_ts=442918429687808001] [mem_max="2513773983 Bytes (2.34 GB)"] [sql="update t set b = b + 1"]
```

次に、基本的に問題の原因となったステートメントを見つけることができます。さらに確認するには、 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md)ステートメントを実行します。出力は次のようになります。

```sql
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| Id                  | User | Host                | db     | Command | Time | State      | Info                      |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
| 2826881778407440457 | root | 192.168.31.43:58641 | test   | Query   | 48   | autocommit | update t set b = b + 1    |
| 2826881778407440613 | root | 127.0.0.1:45952     | test   | Execute | 0    | autocommit | select * from t where a=? |
| 2826881778407440619 | root | 192.168.31.43:60428 | <null> | Query   | 0    | autocommit | show processlist          |
+---------------------+------+---------------------+--------+---------+------+------------+---------------------------+
```

出力は、誰かが予期しない`UPDATE`ステートメント ( `update t set b = b + 1` ) を実行していることを示しています。これにより、トランザクションが大きくなり、 ステイル読み取りが妨げられます。

この問題を解決するには、この`UPDATE`ステートメントを実行しているアプリケーションを停止します。
