---
title: Troubleshoot Lock Conflicts
summary: Learn to analyze and resolve lock conflicts in TiDB.
---

# ロックの競合のトラブルシューティング {#troubleshoot-lock-conflicts}

TiDB は完全な分散トランザクションをサポートします。 v3.0 以降、TiDB は楽観的トランザクション モードと悲観的トランザクション モードを提供します。このドキュメントでは、ロックビューを使用してロックの問題をトラブルシューティングする方法と、楽観的トランザクションと悲観的トランザクションにおける一般的なロック競合の問題に対処する方法について説明します。

## ロックビューを使用してロックの問題をトラブルシューティングする {#use-lock-view-to-troubleshoot-lock-issues}

v5.1 以降、TiDB はロックビュー機能をサポートしています。この機能には、ロックの競合とロックの待機に関する詳細情報を提供する`information_schema`のシステム テーブルが組み込まれています。

> **注記：**
>
> 現在、ロックビュー機能は、悲観的ロックの競合および待機情報のみを提供します。

これらのテーブルの詳細については、次のドキュメントを参照してください。

-   [`TIDB_TRX`および`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) : 現在の TiDB ノードまたはクラスター全体で実行中のすべてのトランザクションの情報を提供します。これには、トランザクションがロック待機状態にあるかどうか、ロック待機時間、トランザクションで実行されたステートメントのダイジェストが含まれます。
-   [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) : ブロッキングおよびブロックされたトランザクションの`start_ts` 、ブロックされた SQL ステートメントのダイジェスト、および待機が発生したキーを含む、TiKV の悲観的ロック待機情報を提供します。
-   [`DEADLOCKS`と`CLUSTER_DEADLOCKS`](/information-schema/information-schema-deadlocks.md) : 現在の TiDB ノードまたはクラスター全体で最近発生したいくつかのデッドロック イベントの情報を提供します。これには、デッドロック ループ内のトランザクション間の待機関係、トランザクションで現在実行されているステートメントのダイジェスト、およびキーが含まれます。待機が発生します。

> **注記：**
>
> ロック ビュー関連のシステム テーブルに表示される SQL ステートメントは、SQL ダイジェストに従って内部クエリによって取得される正規化された SQL ステートメント (つまり、形式と引数のない SQL ステートメント) であるため、テーブルは、形式と引数。 SQL ダイジェストと正規化された SQL ステートメントの詳細については、 [ステートメント概要テーブル](/statement-summary-tables.md)を参照してください。

次のセクションでは、これらの表を使用したいくつかの問題のトラブルシューティングの例を示します。

### デッドロックエラー {#deadlock-errors}

最近のデッドロック エラーの情報を取得するには、 `DEADLOCKS`または`CLUSTER_DEADLOCKS`テーブルをクエリします。

たとえば、 `DEADLOCKS`テーブルをクエリするには、次の SQL ステートメントを実行できます。

```sql
select * from information_schema.deadlocks;
```

以下は出力例です。

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

上記のクエリ結果は、デッドロックエラー時の複数トランザクション間の待ち関係、各トランザクションで実行中のSQL文の正規化形式（形式や引数のない文）、競合が発生しているキー、およびその情報を示しています。鍵。

たとえば、上記の例の最初の行は、ID が`426812829645406216`のトランザクションが``update `t` set `v` =? Where `id` =? ;``のようなステートメントを実行しているが、ID が`426812829645406217`の別のトランザクションによってブロックされていることを意味します。 ID `426812829645406217`のトランザクションも``update `t` set `v` =? Where `id` =? ;``の形式のステートメントを実行していますが、ID `426812829645406216`のトランザクションによってブロックされています。したがって、2 つのトランザクションはデッドロックを形成します。

### いくつかのホットキーによりキューロックが発生する {#a-few-hot-keys-cause-queueing-locks}

`DATA_LOCK_WAITS`システム テーブルは、TiKV ノード上のロック待機ステータスを提供します。このテーブルにクエリを実行すると、TiDB はすべての TiKV ノードからリアルタイムのロック待機情報を自動的に取得します。いくつかのホット キーが頻繁にロックされ、多くのトランザクションがブロックされている場合は、 `DATA_LOCK_WAITS`テーブルをクエリしてキーごとに結果を集計し、問題が頻繁に発生するキーを見つけることができます。

```sql
select `key`, count(*) as `count` from information_schema.data_lock_waits group by `key` order by `count` desc;
```

以下は出力例です。

```sql
+----------------------------------------+-------+
| key                                    | count |
+----------------------------------------+-------+
| 7480000000000000415F728000000000000001 |     2 |
| 7480000000000000415F728000000000000002 |     1 |
+----------------------------------------+-------+
```

不測の事態を避けるために、複数のクエリを作成する必要がある場合があります。

頻繁に問題が発生するキーがわかっている場合は、そのキーをロックしようとしているトランザクションの情報を`TIDB_TRX`または`CLUSTER_TIDB_TRX`テーブルから取得してみることができます。

表`TIDB_TRX`と`CLUSTER_TIDB_TRX`に表示される情報は、クエリの実行時に実行されているトランザクションの情報でもあることに注意してください。これらのテーブルには、完了したトランザクションの情報は表示されません。同時トランザクションが多数ある場合、クエリの結果セットも大きくなる可能性があります。 `limit`句または`where`句を使用して、ロック待機時間が長いトランザクションをフィルタリングできます。 Lock ビューで複数のテーブルを結合すると、異なるテーブルのデータが同時に取得されないため、異なるテーブルの情報に一貫性がなくなる可能性があることに注意してください。

たとえば、 `where`句を使用してロック待機時間が長いトランザクションをフィルタリングするには、次の SQL ステートメントを実行できます。

```sql
select trx.* from information_schema.data_lock_waits as l left join information_schema.tidb_trx as trx on l.trx_id = trx.id where l.key = "7480000000000000415F728000000000000001"\G
```

以下は出力例です。

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

### トランザクションが長期間ブロックされている {#a-transaction-is-blocked-for-a-long-time}

トランザクションが別のトランザクション (または複数のトランザクション) によってブロックされていることがわかっており、現在のトランザクションの`start_ts` (トランザクション ID) がわかっている場合は、次のメソッドを使用してブロックしているトランザクションの情報を取得できます。 Lock ビューで複数のテーブルを結合すると、異なるテーブルのデータが同時に取得されないため、異なるテーブルの情報に一貫性がなくなる可能性があることに注意してください。

```sql
select l.key, trx.*, tidb_decode_sql_digests(trx.all_sql_digests) as sqls from information_schema.data_lock_waits as l join information_schema.cluster_tidb_trx as trx on l.current_holding_trx_id = trx.id where l.trx_id = 426831965449355272\G
```

以下は出力例です。

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

上記のクエリでは、 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数が`CLUSTER_TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列で使用されています。この関数は、この列 (値は SQL ダイジェストのセット) を正規化された SQL ステートメントに変換しようとします。これにより、可読性が向上します。

現在のトランザクションの`start_ts`不明な場合は、 `TIDB_TRX` / `CLUSTER_TIDB_TRX`テーブルまたは[`PROCESSLIST` / `CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブルの情報からそれを見つけ出すことができます。

## 楽観的ロックの競合のトラブルシューティング {#troubleshoot-optimistic-lock-conflicts}

このセクションでは、楽観的トランザクション モードにおける一般的なロック競合の問題の解決策を提供します。

### 読み取り/書き込みの競合 {#read-write-conflicts}

TiDBサーバーはクライアントから読み取りリクエストを受信すると、現在のトランザクションの start_ts として物理時間でグローバルに一意で増加するタイムスタンプを取得します。トランザクションは、start_ts より前の最新のデータ、つまり start_ts より小さい最新の commit_ts のターゲット キーを読み取る必要があります。ターゲット キーが別のトランザクションによってロックされていることをトランザクションが検出し、他のトランザクションがどのフェーズにあるかを知ることができない場合、読み取り/書き込み競合が発生します。回路図は以下の通りです：

![read-write conflict](/media/troubleshooting-lock-pic-04.png)

Txn0 は事前書き込みフェーズを完了し、コミットフェーズに入ります。このとき、Txn1 は同じターゲット キーの読み取りを要求します。 Txn1 は、start_ts よりも小さい最新の commit_ts のターゲット キーを読み取る必要があります。 Txn1 の start_ts は Txn0 の lock_ts より大きいため、Txn1 はターゲット キーのロックがクリアされるまで待機する必要がありますが、まだ完了していません。その結果、Txn1 は Txn0 がコミットされたかどうかを確認できません。したがって、Txn1 と Txn0 の間で読み取り/書き込みの競合が発生します。

TiDB クラスター内の読み取り/書き込み競合は、次の方法で検出できます。

1.  TiDBサーバーのメトリクスとログのモニタリング

    -   Grafana を介したデータの監視

        TiDB ダッシュボードの`KV Errors`パネルでは、 `Lock Resolve OPS`の`not_expired` / `resolve`と`KV Backoff OPS`の`tikvLockFast`が、トランザクション内の読み取り/書き込み競合をチェックするために使用できるモニタリング メトリックです。すべてのメトリックの値が増加すると、読み取り/書き込みの競合が多数発生する可能性があります。 `not_expired`項目は、トランザクションのロックがタイムアウトしていないことを意味します。 `resolve`項目は、他のトランザクションがロックをクリーンアップしようとしていることを意味します。 `tikvLockFast`項目は、読み取り/書き込みの競合が発生することを意味します。

        ![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png) ![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png)

    -   TiDBサーバーのログ

        読み取り/書き込みの競合がある場合は、TiDB ログに次のメッセージが表示されます。

        ```log
        [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
        ```

        -   txnStartTS: 読み取りリクエストを送信しているトランザクションの start_ts。上記のログでは、 `416643508703592451`が start_ts です。
        -   backoff_types: 読み取り/書き込み競合が発生し、読み取りリクエストがバックオフと再試行を実行する場合、再試行のタイプは`TxnLockFast`です。
        -   backoff_ms: 読み取りリクエストがバックオフと再試行に費やした時間。単位はミリ秒です。上記のログでは、読み取りリクエストはバックオフと再試行に 255 ミリ秒を費やしています。
        -   region_id: 読み取りリクエストの対象キーに対応するリージョンID。

2.  TiKVサーバーのログ

    読み取り/書き込みの競合がある場合は、TiKV ログに次のメッセージが表示されます。

    ```log
    [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
    ```

    このメッセージは、TiDB で読み取り/書き込み競合が発生したことを示します。読み取りリクエストのターゲットキーは別のトランザクションによってロックされています。ロックは、コミットされていない楽観的トランザクションと、事前書き込みフェーズ後のコミットされていない悲観的トランザクションからのものです。

    -   Primary_lock: 対象キーがプライマリロックでロックされていることを示します。
    -   lock_version: ロックを所有するトランザクションの start_ts。
    -   key: ロックされているターゲットキー。
    -   lock_ttl: ロックの TTL (Time To Live)
    -   txn_size: ロックを所有するトランザクションのリージョン内にあるキーの数。

解決策:

-   読み取り/書き込みの競合が発生すると、自動バックオフと再試行がトリガーされます。上の例と同様に、Txn1 にはバックオフと再試行があります。初回のリトライは 10 ms、最長のリトライは 3000 ms、合計時間は最大 20000 ms です。

-   TiDB コントロールのサブコマンド[`decoder`](/tidb-control.md#the-decoder-command)を使用すると、指定したキーに対応する行のテーブル ID と ROWID を表示できます。

    ```sh
    ./tidb-ctl decoder "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    format: table_row
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

### KeyIsLocked エラー {#keyislocked-error}

トランザクションの Prewrite フェーズでは、TiDB は書き込みと書き込みの競合があるかどうかをチェックし、ターゲット キーが別のトランザクションによってロックされているかどうかをチェックします。キーがロックされている場合、TiKVサーバーは「KeyIsLocked」エラーを出力します。現時点では、TiDB および TiKV のログにはエラー メッセージは出力されません。読み取り/書き込み競合と同様に、「KeyIsLocked」が発生すると、TiDB は自動的にバックオフを実行し、トランザクションを再試行します。

Grafana の TiDB モニタリングで「KeyIsLocked」エラーがあるかどうかを確認できます。

TiDB ダッシュボードの`KV Errors`パネルには、トランザクションによって引き起こされる書き込みと書き込みの競合をチェックするために使用できる 2 つの監視メトリクス`Lock Resolve OPS`と`KV Backoff OPS`があります。 `Lock Resolve OPS`の下の`resolve`項目と`KV Backoff OPS`の下の`txnLock`項目が明確な上昇傾向にある場合、「KeyIsLocked」エラーが発生します。 `resolve`ロックをクリアしようとする操作を示し、 `txnLock`書き込み競合を表します。

![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png) ![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png)

解決策:

-   監視中に少量の txnLock が存在する場合は、あまり注意を払う必要はありません。バックオフと再試行はバックグラウンドで自動的に実行されます。最初の再試行時間は 100 ミリ秒、1 回の再試行の最大時間は 3000 ミリ秒です。
-   `KV Backoff OPS`内の「txnLock」操作が多すぎる場合は、アプリケーション側から書き込み競合の原因を分析することをお勧めします。
-   アプリケーションが書き込みと書き込みの競合シナリオである場合は、悲観的トランザクション モードを使用することを強くお勧めします。

### ロックノットファウンドエラー {#locknotfound-error}

「TxnLockNotFound」のエラー ログは、トランザクションのコミット時間が TTL 時間より長く、トランザクションがコミットしようとしたときに、そのロックが他のトランザクションによってロールバックされたことを意味します。 TiDBサーバーがトランザクションのコミット再試行を有効にしている場合、このトランザクションは[tidb_retry_limit](/system-variables.md#tidb_retry_limit)に従って再実行されます。 (明示的トランザクションと暗黙的トランザクションの違いに注意してください。)

「LockNotFound」エラーがあるかどうかは、次の方法で確認できます。

1.  TiDBサーバーのログをビュー

    「TxnLockNotFound」エラーが発生した場合、TiDB ログ メッセージは次のようになります。

    ```log
    [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
    ```

    -   start_ts: 他のトランザクションによってロックがロールバックされたために`TxnLockNotFound`エラーを出力したトランザクションの start_ts。上記のログでは、 `412720515987275779`が start_ts です。
    -   commit_ts: `TxnLockNotFound`エラーを出力したトランザクションの commit_ts。上記のログでは、 `412720519984971777`が commit_ts です。

2.  TiKVサーバーのログをビュー

    「TxnLockNotFound」エラーが発生した場合、TiKV ログ メッセージは次のようになります。

    ```log
    Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
    ```

解決策:

-   start_ts と commit_ts の時間間隔を確認することで、コミット時間が TTL 時間を超えているかどうかを確認できます。

    PD 制御ツールを使用して時間間隔を確認する:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd tso [start_ts]
    tiup ctl:v<CLUSTER_VERSION> pd tso [commit_ts]
    ```

-   書き込みパフォーマンスが遅いため、トランザクションコミットの効率が悪くなり、ロックが解除される可能性があるかどうかを確認することをお勧めします。

-   TiDB トランザクションのリトライを無効にする場合は、アプリケーション側で例外をキャッチして再試行する必要があります。

## 悲観的ロックの競合のトラブルシューティング {#troubleshoot-pessimistic-lock-conflicts}

このセクションでは、悲観的トランザクション モードにおける一般的なロック競合の問題の解決策を提供します。

> **注記：**
>
> 悲観的トランザクション モードが設定されている場合でも、自動コミット トランザクションは最初に楽観的モードを使用してコミットを試行します。競合が発生した場合、トランザクションは自動再試行中に悲観的トランザクション モードに切り替わります。

### 読み取り/書き込みの競合 {#read-write-conflicts}

エラー メッセージと解決策は、楽観的ロックの競合の[読み取り/書き込み競合](#read-write-conflicts)と同じです。

### 悲観的なロックの再試行制限に達しました {#pessimistic-lock-retry-limit-reached}

トランザクションの競合が非常に深刻な場合、または書き込み競合が発生した場合、楽観的トランザクションは直接終了され、悲観的トランザクションは書き込み競合がなくなるまでstorageからの最新データを使用してステートメントを再試行します。

TiDB のロック操作は書き込み操作であり、操作のプロセスは最初に読み取り、次に書き込みであるため、2 つの RPC リクエストが存在します。トランザクションの途中で書き込み競合が発生した場合、TiDB はターゲット キーのロックを再試行し、各再試行が TiDB ログに出力されます。再試行回数は[pessimistic-txn。max-retry-count](/tidb-configuration-file.md#max-retry-count)で決まります。

悲観的トランザクション モードでは、書き込み競合が発生し、再試行回数が上限に達すると、次のキーワードを含むエラー メッセージが TiDB ログに表示されます。

```log
err="pessimistic lock retry limit reached"
```

解決策:

-   上記エラーが頻繁に発生する場合は、アプリケーション側から調整することをお勧めします。
-   ビジネスに同じ行 (同じキー) に対する同時ロックが多く、頻繁に競合が発生する場合は、システム変数[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)を有効にしてみてください。この変数を有効にすると、ロック競合のあるトランザクションのスループット低下 (平均レイテンシーの増加) というコストが発生する可能性があることに注意してください。新しくデプロイされたクラスターの場合、この変数はデフォルトで有効 ( `ON` ) になります。

### ロック待機タイムアウトを超過しました {#lock-wait-timeout-exceeded}

悲観的トランザクション モードでは、トランザクションは相互のロックを待ちます。ロック待機のタイムアウトは、TiDB の[innodb_lock_wait_timeout](/pessimistic-transaction.md#behaviors)パラメータによって定義されます。これは、SQL ステートメント レベルでの最大待機ロック時間であり、SQL ステートメントのロックの予想値ですが、ロックは取得されていません。この時間が経過すると、TiDB は再度ロックを試行せず、対応するエラー メッセージをクライアントに返します。

待機ロックのタイムアウトが発生すると、次のエラー メッセージがクライアントに返されます。

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

解決策:

-   上記エラーが頻繁に発生する場合は、アプリケーションロジックを調整することをお勧めします。

### TTL マネージャーがタイムアウトしました {#ttl-manager-has-timed-out}

トランザクションの実行時間は GC 時間制限を超えることはできません。さらに、悲観的トランザクションの TTL 時間には上限があり、デフォルト値は 1 時間です。したがって、1 時間を超えて実行された悲観的トランザクションはコミットに失敗します。このタイムアウトしきい値は、TiDB パラメータ[`performance.max-txn-ttl`](https://github.com/pingcap/tidb/blob/release-7.5/pkg/config/config.toml.example)によって制御されます。

悲観的トランザクションの実行時間が TTL 時間を超えると、TiDB ログに次のエラー メッセージが表示されます。

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

解決策:

-   まず、アプリケーションロジックが最適化できるかどうかを確認します。たとえば、大規模なトランザクションは TiDB のトランザクション サイズ制限を引き起こす可能性があり、複数の小さなトランザクションに分割される可能性があります。
-   また、アプリケーションのトランザクション ロジックに合わせて関連パラメーターを適切に調整できます。

### ロックを取得しようとしたときにデッドロックが見つかりました {#deadlock-found-when-trying-to-get-lock}

2 つ以上のトランザクション間のリソース競合により、デッドロックが発生します。手動で処理しない場合、相互にブロックするトランザクションは正常に実行できず、相互に永遠に待機することになります。デッドロックを解決するには、トランザクションの 1 つを手動で終了して、他のトランザクション要求を再開する必要があります。

悲観的トランザクションにデッドロックが発生した場合、デッドロックを解除するにはトランザクションの 1 つを終了する必要があります。クライアントは、MySQL と同じ`Error 1213`エラーを返します。次に例を示します。

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```

解決策:

-   v5.1 以降のバージョンでデッドロックの原因を確認することが難しい場合は、システム テーブル`INFORMATION_SCHEMA.DEADLOCKS`または`INFORMATION_SCHEMA.CLUSTER_DEADLOCKS`にクエリを実行して、デッドロック待機チェーンの情報を取得することをお勧めします。詳細については、 [デッドロックエラー](#deadlock-errors)章および[`DEADLOCKS`テーブル](/information-schema/information-schema-deadlocks.md)ドキュメントを参照してください。
-   デッドロックが頻繁に発生する場合は、アプリケーションのトランザクション クエリ ロジックを調整して、デッドロックの発生を減らす必要があります。
