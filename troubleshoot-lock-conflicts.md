---
title: Troubleshoot Lock Conflicts
summary: Learn to analyze and resolve lock conflicts in TiDB.
---

# ロックの競合のトラブルシューティング {#troubleshoot-lock-conflicts}

TiDBは、完全な分散トランザクションをサポートしています。 v3.0以降、TiDBは楽観的トランザクションモードと悲観的トランザクションモードを提供します。このドキュメントでは、TiDBでのロックの競合をトラブルシューティングして解決する方法を紹介します。

## 楽観的なトランザクションモード {#optimistic-transaction-mode}

TiDBのトランザクションは、プリライトフェーズとコミットフェーズを含む2フェーズコミット（2PC）を使用します。手順は次のとおりです。

![two-phase commit in the optimistic transaction mode](/media/troubleshooting-lock-pic-01.png)

PercolatorおよびTiDBのトランザクションのアルゴリズムの詳細については、 [Googleのパーコレーター](https://ai.google/research/pubs/pub36726)を参照してください。

### 事前書き込みフェーズ（楽観的） {#prewrite-phase-optimistic}

事前書き込みフェーズでは、TiDBはターゲットキーにプライマリロックとセカンダリロックを追加します。同じターゲットキーにロックを追加する要求が多数ある場合、TiDBは書き込みの競合や`keyislocked`などのエラーをログに出力し、クライアントに報告します。具体的には、ロックに関連する次のエラーが事前書き込みフェーズで発生する可能性があります。

#### 読み取りと書き込みの競合（楽観的） {#read-write-conflict-optimistic}

TiDBサーバーは、クライアントから読み取り要求を受信すると、現在のトランザクションのstart_tsとして、物理的な時間にグローバルに一意で増加するタイムスタンプを取得します。トランザクションは、start_tsの前に最新のデータ、つまり、start_tsよりも小さい最新のcommit_tsのターゲットキーを読み取る必要があります。トランザクションがターゲットキーが別のトランザクションによってロックされていることを検出し、他のトランザクションがどのフェーズにあるかを知ることができない場合、読み取りと書き込みの競合が発生します。回路図は以下の通りです：

![read-write conflict](/media/troubleshooting-lock-pic-04.png)

Txn0はプリライトフェーズを完了し、コミットフェーズに入ります。このとき、Txn1は同じターゲットキーの読み取りを要求します。 Txn1は、start_tsよりも小さい最新のcommit_tsのターゲットキーを読み取る必要があります。 Txn1のstart_tsはTxn0のlock_tsよりも大きいため、Txn1はターゲットキーのロックがクリアされるのを待つ必要がありますが、まだ実行されていません。その結果、Txn1はTxn0がコミットされているかどうかを確認できません。したがって、Txn1とTxn0の間で読み取りと書き込みの競合が発生します。

次の方法で、TiDBクラスタの読み取り/書き込みの競合を検出できます。

1.  TiDBサーバーのメトリックとログの監視

    -   Grafanaを介したデータの監視

        TiDBダッシュボードの`KV Errors`のパネルには、トランザクションでの読み取りと書き込みの競合をチェックするために使用できる2つの監視メトリック`Lock Resolve OPS`と`KV Backoff OPS`があります。 `Lock Resolve OPS`未満の`not_expired`と`resolve`の両方の値が増加すると、多くの読み取り/書き込みの競合が発生する可能性があります。 `not_expired`項目は、トランザクションのロックがタイムアウトしていないことを意味します。 `resolve`項目は、他のトランザクションがロックをクリーンアップしようとすることを意味します。 `KV Backoff OPS`未満の別の`txnLockFast`項目の値が増加すると、読み取りと書き込みの競合も発生する可能性があります。

        ![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png) ![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png)

    -   TiDBサーバーのログ

        読み取りと書き込みの競合がある場合は、TiDBログに次のメッセージが表示されます。

        ```log
        [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
        ```

        -   txnStartTS：読み取り要求を送信しているトランザクションのstart_ts。上記のログでは、 `416643508703592451`はstart_tsです。
        -   backoff_types：読み取りと書き込みの競合が発生し、読み取り要求がバックオフと再試行を実行する場合、再試行のタイプは`TxnLockFast`です。
        -   backoff_ms：読み取り要求がバックオフと再試行に費やす時間。単位はミリ秒です。上記のログでは、読み取り要求はバックオフと再試行に255ミリ秒を費やしています。
        -   region_id：読み取り要求のターゲットキーに対応するリージョンID。

2.  TiKVサーバーのログ

    読み取りと書き込みの競合がある場合は、TiKVログに次のメッセージが表示されます。

    ```log
    [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
    ```

    このメッセージは、TiDBで読み取りと書き込みの競合が発生していることを示しています。読み取り要求のターゲットキーが別のトランザクションによってロックされています。ロックは、コミットされていない楽観的なトランザクションと、事前書き込みフェーズ後のコミットされていない悲観的なトランザクションからのものです。

    -   primary_lock：ターゲットキーがプライマリロックによってロックされていることを示します。
    -   lock_version：ロックを所有するトランザクションのstart_ts。
    -   key：ロックされているターゲットキー。
    -   lock_ttl：ロックのTTL（Time To Live）
    -   txn_size：ロックを所有するトランザクションのリージョンにあるキーの数。

ソリューション：

-   読み取りと書き込みの競合により、自動バックオフと再試行がトリガーされます。上記の例のように、Txn1にはバックオフと再試行があります。最初の再試行は10ミリ秒、最長の再試行は3000ミリ秒、合計時間は最大で20000ミリ秒です。

-   TiDB Controlのサブコマンド[`decoder`](/tidb-control.md#the-decoder-command)を使用して、指定されたキーに対応する行のテーブルIDとROWIDを表示できます。

    ```sh
    ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"

    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

#### KeyIsLockedエラー {#keyislocked-error}

トランザクションの事前書き込みフェーズでは、TiDBは書き込みと書き込みの競合があるかどうかを確認し、次にターゲットキーが別のトランザクションによってロックされているかどうかを確認します。キーがロックされている場合、TiKVサーバーは「KeyIsLocked」エラーを出力します。現在、エラーメッセージはTiDBとTiKVのログに出力されません。読み取りと書き込みの競合と同じように、「KeyIsLocked」が発生すると、TiDBは自動的にバックオフを実行し、トランザクションを再試行します。

GrafanaのTiDBモニタリングに「KeyIsLocked」エラーがあるかどうかを確認できます。

TiDBダッシュボードの`KV Errors`のパネルには、トランザクションによって引き起こされた書き込みと書き込みの競合をチェックするために使用できる2つの監視メトリック`Lock Resolve OPS`と`KV Backoff OPS`があります。 `Lock Resolve OPS`未満の`resolve`アイテムと`KV Backoff OPS`未満の`txnLock`アイテムに明確な上昇傾向がある場合、「KeyIsLocked」エラーが発生します。 `resolve`はロックをクリアしようとする操作を示し、 `txnLock`は書き込みの競合を表します。

![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png) ![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png)

ソリューション：

-   監視に少量のtxnLockがある場合は、あまり注意を払う必要はありません。バックオフと再試行はバックグラウンドで自動的に実行されます。 1回の再試行の初回は100ミリ秒で、最大時間は3000ミリ秒です。
-   `KV Backoff OPS`に「txnLock」操作が多すぎる場合は、アプリケーション側から書き込みの競合の理由を分析することをお勧めします。
-   アプリケーションが書き込みと書き込みの競合シナリオである場合は、ペシミスティックトランザクションモードを使用することを強くお勧めします。

### コミットフェーズ（楽観的） {#commit-phase-optimistic}

事前書き込みフェーズが完了した後、クライアントはcommit_tsを取得し、トランザクションは2PCの次のフェーズであるコミットフェーズに進みます。

#### LockNotFoundエラー {#locknotfound-error}

「TxnLockNotFound」のエラーログは、トランザクションのコミット時間がTTL時間よりも長く、トランザクションがコミットしようとしているときに、そのロックが他のトランザクションによってロールバックされたことを意味します。 TiDBサーバーがトランザクションコミットの再試行を有効にしている場合、このトランザクションは[tidb_retry_limit](/system-variables.md#tidb_retry_limit)に従って再実行されます。 （明示的トランザクションと暗黙的トランザクションの違いに注意してください。）

次の方法で、「LockNotFound」エラーがあるかどうかを確認できます。

1.  TiDBサーバーのログをビューする

    「TxnLockNotFound」エラーが発生した場合、TiDBログメッセージは次のようになります。

    ```log
    [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
    ```

    -   start_ts：ロックが他のトランザクションによってロールバックされたために`TxnLockNotFound`エラーを出力するトランザクションのstart_ts。上記のログでは、 `412720515987275779`がstart_tsです。
    -   commit_ts： `TxnLockNotFound`エラーを出力するトランザクションのcommit_ts。上記のログでは、 `412720519984971777`はcommit_tsです。

2.  TiKVサーバーのログをビューする

    「TxnLockNotFound」エラーが発生した場合、TiKVログメッセージは次のようになります。

    ```log
    Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
    ```

ソリューション：

-   start_tsとcommit_tsの時間間隔を確認することで、コミット時間がTTL時間を超えているかどうかを確認できます。

    PD制御ツールを使用して時間間隔を確認します。

    ```shell
    tiup ctl pd tso [start_ts]
    tiup ctl pd tso [commit_ts]
    ```

-   書き込みパフォーマンスが遅いかどうかを確認することをお勧めします。これにより、トランザクションコミットの効率が低下し、ロックが解除される可能性があります。

-   TiDBトランザクションの再試行を無効にする場合は、アプリケーション側で例外をキャッチして再試行する必要があります。

## 悲観的なトランザクションモード {#pessimistic-transaction-mode}

v3.0.8より前では、TiDBはデフォルトでオプティミスティックトランザクションモードを使用していました。このモードでは、トランザクションの競合がある場合、最新のトランザクションはコミットに失敗します。したがって、アプリケーションはトランザクションの再試行をサポートする必要があります。悲観的なトランザクションモードはこの問題を解決し、アプリケーションは回避策のためにロジックを変更する必要はありません。

TiDBのペシミスティックトランザクションモードとオプティミスティックトランザクションモードのコミットフェーズは同じロジックであり、両方のコミットは2PCモードです。悲観的なトランザクションの重要な適応は、DMLの実行です。

![TiDB pessimistic transaction commit logic](/media/troubleshooting-lock-pic-05.png)

悲観的なトランザクションは、2PCの前に`Acquire Pessimistic Lock`フェーズを追加します。このフェーズには、次の手順が含まれます。

1.  （楽観的なトランザクションモードと同じ）クライアントから`begin`の要求を受信し、現在のタイムスタンプはこのトランザクションのstart_tsです。
2.  TiDBサーバーがクライアントから`update`要求を受信すると、TiDBサーバーはTiKVサーバーへの悲観的なロック要求を開始し、ロックはTiKVサーバーに保持されます。
3.  （楽観的トランザクションモードと同じ）クライアントがコミット要求を送信すると、TiDBは楽観的トランザクションモードと同様に2PCの実行を開始します。

![Pessimistic transactions in TiDB](/media/troubleshooting-lock-pic-06.png)

詳細については、 [悲観的なトランザクションモード](/pessimistic-transaction.md)を参照してください。

### 事前書き込みフェーズ（悲観的） {#prewrite-phase-pessimistic}

トランザクションペシミスティックモードでは、コミットフェーズは2PCと同じです。したがって、楽観的なトランザクションモードの場合と同様に、読み取りと書き込みの競合も存在します。

#### 読み取りと書き込みの競合（悲観的） {#read-write-conflict-pessimistic}

[読み取りと書き込みの競合（楽観的）](#read-write-conflict-optimistic)と同じ。

### コミットフェーズ（悲観的） {#commit-phase-pessimistic}

悲観的トランザクションモードでは、 `TxnLockNotFound`のエラーは発生しません。代わりに、ペシミスティックロックはトランザクションのTTLを`txnheartbeat`まで自動的に更新して、2番目のトランザクションが最初のトランザクションのロックをクリアしないようにします。

### ロックに関連するその他のエラー {#other-errors-related-to-locks}

#### 悲観的なロックの再試行制限に達しました {#pessimistic-lock-retry-limit-reached}

トランザクションの競合が非常に深刻な場合、または書き込みの競合が発生した場合、オプティミスティックトランザクションは直接終了し、ペシミスティックトランザクションは、書き込みの競合がなくなるまで、ストレージからの最新データを使用してステートメントを再試行します。

TiDBのロック操作は書き込み操作であり、操作のプロセスは最初に読み取り、次に書き込みであるため、2つのRPC要求があります。トランザクションの途中で書き込みの競合が発生した場合、TiDBはターゲットキーのロックを再試行し、再試行するたびにTiDBログに出力されます。再試行の回数は[pessimistic-txn.max-retry-count](/tidb-configuration-file.md#max-retry-count)によって決定されます。

ペシミスティックトランザクションモードでは、書き込みの競合が発生し、再試行回数が上限に達すると、次のキーワードを含むエラーメッセージがTiDBログに表示されます。

```log
err="pessimistic lock retry limit reached"
```

ソリューション：

-   上記のエラーが頻繁に発生する場合は、アプリケーション側から調整することをお勧めします。

#### ロック待機タイムアウトを超えました {#lock-wait-timeout-exceeded}

悲観的トランザクションモードでは、トランザクションは相互のロックを待機します。ロックを待機するためのタイムアウトは、TiDBの[innodb_lock_wait_timeout](/pessimistic-transaction.md#behaviors)パラメーターによって定義されます。これは、SQLステートメントのロックの予想であるSQLステートメントレベルでの最大待機ロック時間ですが、ロックが取得されたことはありません。この後、TiDBは再度ロックを試みず、対応するエラーメッセージをクライアントに返します。

待機ロックのタイムアウトが発生すると、次のエラーメッセージがクライアントに返されます。

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

ソリューション：

-   上記のエラーが頻繁に発生する場合は、アプリケーションロジックを調整することをお勧めします。

#### TTLマネージャーがタイムアウトしました {#ttl-manager-has-timed-out}

トランザクションの実行時間は、GCの制限時間を超えることはできません。さらに、ペシミスティックトランザクションのTTL時間には上限があり、デフォルト値は1時間です。したがって、1時間以上実行された悲観的なトランザクションは、コミットに失敗します。このタイムアウトしきい値は、TiDBパラメーター[performance.max-txn-ttl](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)によって制御されます。

ペシミスティックトランザクションの実行時間がTTL時間を超えると、TiDBログに次のエラーメッセージが表示されます。

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

ソリューション：

-   まず、アプリケーションロジックを最適化できるかどうかを確認します。たとえば、大きなトランザクションはTiDBのトランザクションサイズ制限をトリガーする可能性があり、これは複数の小さなトランザクションに分割できます。
-   また、アプリケーションのトランザクションロジックに合わせて、関連するパラメータを適切に調整できます。

#### ロックを取得しようとしたときにデッドロックが見つかりました {#deadlock-found-when-trying-to-get-lock}

2つ以上のトランザクション間のリソース競合により、デッドロックが発生します。手動で処理しないと、相互にブロックし合うトランザクションを正常に実行できず、永久に相互に待機します。デッドロックを解決するには、トランザクションの1つを手動で終了して、他のトランザクション要求を再開する必要があります。

悲観的トランザクションにデッドロックがある場合、デッドロックのロックを解除するには、トランザクションの1つを終了する必要があります。クライアントは、MySQLと同じ`Error 1213`のエラーを返します。次に例を示します。

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```

ソリューション：

-   デッドロックの原因を確認するのが難しい場合、v5.1以降のバージョンでは、デッドロック待機チェーンの情報を取得するために`INFORMATION_SCHEMA.DEADLOCKS`または`INFORMATION_SCHEMA.CLUSTER_DEADLOCKS`システムテーブルを照会することをお勧めします。詳細については、 [デッドロックエラー](#deadlock-errors)セクションおよび[`DEADLOCKS`テーブル](/information-schema/information-schema-deadlocks.md)ドキュメントを参照してください。
-   デッドロックが頻繁に発生する場合は、アプリケーションのトランザクションクエリロジックを調整して、そのような発生を減らす必要があります。

### ロックビューを使用して、悲観的なロックに関連する問題のトラブルシューティングを行います {#use-lock-view-to-troubleshoot-issues-related-to-pessimistic-locks}

v5.1以降、TiDBはロックビュー機能をサポートしています。この機能には、ペシミスティックロックの競合とペシミスティックロックの待機に関する詳細情報を提供するいくつかのシステムテーブルが組み込まれてい`information_schema` 。これらの表の詳細な紹介については、次のドキュメントを参照してください。

-   [`TIDB_TRX`および<code>CLUSTER_TIDB_TRX</code>](/information-schema/information-schema-tidb-trx.md) ：トランザクションがロック待機状態にあるかどうか、ロック待機時間、トランザクションで実行されたステートメントのダイジェストなど、現在のTiDBノードまたはクラスタ全体で実行中のすべてのトランザクションの情報を提供します。
-   [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) ：ブロックおよびブロックされたトランザクションの`start_ts` 、ブロックされたSQLステートメントのダイジェスト、および待機が発生するキーを含む、TiKVの悲観的なロック待機情報を提供します。
-   [`DEADLOCKS`および<code>CLUSTER_DEADLOCKS</code>](/information-schema/information-schema-deadlocks.md) ：現在のTiDBノードまたはクラスタ全体で最近発生したいくつかのデッドロックイベントの情報を提供します。これには、デッドロックループ内のトランザクション間の待機関係、トランザクションで現在実行されているステートメントのダイジェスト、およびキーが含まれます。待機が発生する場所。

> **ノート：**
>
> ロックビュー関連のシステムテーブルに表示されるSQLステートメントは正規化されたSQLステートメント（つまり、フォーマットと引数のないSQLステートメント）であり、SQLダイジェストに従った内部クエリによって取得されるため、テーブルは、フォーマットと引数。 SQLダイジェストと正規化されたSQLステートメントの詳細については、 [ステートメント要約表](/statement-summary-tables.md)を参照してください。

次のセクションでは、これらの表を使用していくつかの問題をトラブルシューティングする例を示します。

#### デッドロックエラー {#deadlock-errors}

最近のデッドロックエラーの情報を取得するには、 `DEADLOCKS`または`CLUSTER_DEADLOCKS`のテーブルを照会できます。例えば：

{{< copyable "" >}}

```sql
select * from information_schema.deadlocks;
```

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

上記のクエリ結果は、デッドロックエラーでの複数のトランザクション間の待機関係、各トランザクションで現在実行されているSQLステートメントの正規化された形式（形式と引数のないステートメント）、競合が発生するキー、および鍵。

たとえば、上記の例では、最初の行は、IDが`426812829645406216`のトランザクションが``update `t` set `v` =? Where `id` =? ;``のようなステートメントを実行しているが、IDが`426812829645406217`の別のトランザクションによってブロックされていることを意味します。 IDが`426812829645406217`のトランザクションも、 ``update `t` set `v` =? Where `id` =? ;``の形式のステートメントを実行していますが、IDが`426812829645406216`のトランザクションによってブロックされています。したがって、2つのトランザクションはデッドロックを形成します。

#### いくつかのホットキーはキューイングロックを引き起こします {#a-few-hot-keys-cause-queueing-locks}

`DATA_LOCK_WAITS`システムテーブルは、TiKVノードのロック待機ステータスを提供します。このテーブルを照会すると、TiDBはすべてのTiKVノードからリアルタイムのロック待機情報を自動的に取得します。いくつかのホットキーが頻繁にロックされ、多くのトランザクションがブロックされる場合は、 `DATA_LOCK_WAITS`のテーブルをクエリし、キーごとに結果を集計して、問題が頻繁に発生するキーを見つけようとします。

{{< copyable "" >}}

```sql
select `key`, count(*) as `count` from information_schema.data_lock_waits group by `key` order by `count` desc;
```

```sql
+----------------------------------------+-------+
| key                                    | count |
+----------------------------------------+-------+
| 7480000000000000415F728000000000000001 |     2 |
| 7480000000000000415F728000000000000002 |     1 |
+----------------------------------------+-------+
```

不測の事態を回避するために、複数のクエリを実行する必要がある場合があります。

問題が頻繁に発生するキーがわかっている場合は、 `TIDB_TRX`または`CLUSTER_TIDB_TRX`のテーブルからキーをロックしようとするトランザクションの情報を取得してみてください。

`TIDB_TRX`と`CLUSTER_TIDB_TRX`の表に表示される情報は、クエリの実行時に実行されているトランザクションの情報でもあることに注意してください。これらのテーブルには、完了したトランザクションの情報は表示されません。同時トランザクションが多数ある場合、クエリの結果セットも大きくなる可能性があります。 `limit`句または`where`句を使用して、ロック待機時間が長いトランザクションを除外できます。 Lock ビューで複数のテーブルを結合すると、異なるテーブルのデータが同時に取得されない可能性があるため、異なるテーブルの情報に一貫性がない可能性があることに注意してください。

{{< copyable "" >}}

```sql
select trx.* from information_schema.data_lock_waits as l left join information_schema.tidb_trx as trx on l.trx_id = trx.id where l.key = "7480000000000000415F728000000000000001"\G
```

```sql
*************************** 1. row ***************************
                     ID: 426831815660273668
             START_TIME: 2021-08-06 07:16:00.081000
     CURRENT_SQL_DIGEST: 06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ? ;
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-06 07:16:00.087720
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 77
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["0fdc781f19da1c6078c9de7eadef8a307889c001e05f107847bee4cfc8f3cdf3","06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7"]
*************************** 2. row ***************************
                     ID: 426831818019569665
             START_TIME: 2021-08-06 07:16:09.081000
     CURRENT_SQL_DIGEST: 06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ? ;
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-06 07:16:09.290271
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 75
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["0fdc781f19da1c6078c9de7eadef8a307889c001e05f107847bee4cfc8f3cdf3","06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7"]
2 rows in set (0.00 sec)
```

#### トランザクションが長期間ブロックされている {#a-transaction-is-blocked-for-a-long-time}

トランザクションが別のトランザクション（または複数のトランザクション）によってブロックされていることがわかっていて、現在のトランザクションの`start_ts` （トランザクションID）がわかっている場合は、次の方法を使用して、ブロックしているトランザクションの情報を取得できます。 Lock ビューで複数のテーブルを結合すると、異なるテーブルのデータが同時に取得されない可能性があるため、異なるテーブルの情報に一貫性がない可能性があることに注意してください。

{{< copyable "" >}}

```sql
select l.key, trx.*, tidb_decode_sql_digests(trx.all_sql_digests) as sqls from information_schema.data_lock_waits as l join information_schema.cluster_tidb_trx as trx on l.current_holding_trx_id = trx.id where l.trx_id = 426831965449355272\G
```

```sql
*************************** 1. row ***************************
                    key: 74800000000000004D5F728000000000000001
               INSTANCE: 127.0.0.1:10080
                     ID: 426832040186609668
             START_TIME: 2021-08-06 07:30:16.581000
     CURRENT_SQL_DIGEST: 06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ? ;
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-06 07:30:16.592763
        MEM_BUFFER_KEYS: 1
       MEM_BUFFER_BYTES: 19
             SESSION_ID: 113
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["0fdc781f19da1c6078c9de7eadef8a307889c001e05f107847bee4cfc8f3cdf3","a4e28cc182bdd18288e2a34180499b9404cd0ba07e3cc34b6b3be7b7c2de7fe9","06da614b93e62713bd282d4685fc5b88d688337f36e88fe55871726ce0eb80d7"]
                   sqls: ["begin ;","select * from `t` where `id` = ? for update ;","update `t` set `v` = `v` + ? where `id` = ? ;"]
1 row in set (0.01 sec)
```

上記のクエリでは、 `CLUSTER_TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列で[`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数が使用されています。この関数は、この列（値はSQLダイジェストのセット）を正規化されたSQLステートメントに変換しようとします。これにより、読みやすさが向上します。

現在のトランザクションの`start_ts`が不明な場合は、 `TIDB_TRX` / `CLUSTER_TIDB_TRX`テーブルまたは[`PROCESSLIST` / <code>CLUSTER_PROCESSLIST</code>](/information-schema/information-schema-processlist.md)テーブルの情報からそれを見つけることができます。
