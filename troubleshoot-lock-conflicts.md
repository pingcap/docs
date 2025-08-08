---
title: Troubleshoot Lock Conflicts
summary: TiDB でのロック競合を分析して解決する方法を学びます。
---

# ロックの競合のトラブルシューティング {#troubleshoot-lock-conflicts}

TiDBは完全な分散トランザクションをサポートしています。v3.0以降、TiDBは楽観的トランザクションモードと悲観的トランザクションモードを提供します。このドキュメントでは、ロックビューを使用してロックの問題をトラブルシューティングする方法と、楽観的と悲観的トランザクションにおける一般的なロック競合の問題に対処する方法について説明します。

## ロックビューを使用してロックの問題をトラブルシューティングする {#use-lock-view-to-troubleshoot-lock-issues}

TiDBはバージョン5.1以降、ロックビュー機能をサポートしています。この機能には、ロック競合やロック待機に関する詳細情報を提供する複数のシステムテーブルがバージョン`information_schema`に組み込まれています。

> **注記：**
>
> 現在、ロックビュー機能は、悲観的ロックの競合と待機情報のみを提供します。

これらのテーブルの詳細な紹介については、次のドキュメントを参照してください。

-   [`TIDB_TRX`および`CLUSTER_TIDB_TRX`](/information-schema/information-schema-tidb-trx.md) : 現在の TiDB ノードまたはクラスター全体で実行中のすべてのトランザクションの情報 (トランザクションがロック待機状態にあるかどうか、ロック待機時間、トランザクションで実行されたステートメントのダイジェストなど) を提供します。
-   [`DATA_LOCK_WAITS`](/information-schema/information-schema-data-lock-waits.md) : ブロックしているトランザクションとブロックされたトランザクションの`start_ts` 、ブロックされた SQL ステートメントのダイジェスト、待機が発生したキーなど、悲観的ロック待機情報を TiKV で提供します。
-   [`DEADLOCKS`と`CLUSTER_DEADLOCKS`](/information-schema/information-schema-deadlocks.md) : デッドロック ループ内のトランザクション間の待機関係、トランザクションで現在実行されているステートメントのダイジェスト、待機が発生しているキーなど、現在の TiDB ノードまたはクラスター全体で最近発生したいくつかのデッドロック イベントの情報を提供します。

> **注記：**
>
> ロックビュー関連のシステムテーブルに表示されるSQL文は、SQLダイジェストに基づく内部クエリによって取得された正規化されたSQL文（つまり、書式と引数のないSQL文）であるため、書式と引数を含む完全なSQL文を取得することはできません。SQLダイジェストと正規化されたSQL文の詳細については、 [明細書概要表](/statement-summary-tables.md)参照してください。

次のセクションでは、これらの表を使用していくつかの問題をトラブルシューティングする例を示します。

### デッドロックエラー {#deadlock-errors}

最近のデッドロック エラーの情報を取得するには、テーブル`DEADLOCKS`または`CLUSTER_DEADLOCKS`クエリできます。

たとえば、テーブル`DEADLOCKS`クエリするには、次の SQL ステートメントを実行できます。

```sql
select * from information_schema.deadlocks;
```

出力例は次のとおりです。

```sql
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
| DEADLOCK_ID | OCCUR_TIME                 | RETRYABLE | TRY_LOCK_TRX_ID    | CURRENT_SQL_DIGEST                                               | CURRENT_SQL_DIGEST_TEXT                 | KEY                                    | KEY_INFO                                                                                           | TRX_HOLDING_LOCK   |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406216 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000002 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"2"} | 426812829645406217 |
|           1 | 2021-08-05 11:09:03.230341 |         0 | 426812829645406217 | 22230766411edb40f27a68dadefc63c6c6970d5827f1e5e22fc97be2c4d8350d | update `t` set `v` = ? where `id` = ? ; | 7480000000000000355F728000000000000001 | {"db_id":1,"db_name":"test","table_id":53,"table_name":"t","handle_type":"int","handle_value":"1"} | 426812829645406216 |
+-------------+----------------------------+-----------+--------------------+------------------------------------------------------------------+-----------------------------------------+----------------------------------------+----------------------------------------------------------------------------------------------------+--------------------+
```

上記のクエリ結果には、デッドロックエラーが発生した複数のトランザクション間の待機関係、各トランザクションで現在実行中の SQL 文の正規化された形式 (形式や引数のない文)、競合が発生しているキー、およびそのキーの情報が表示されます。

例えば、上記の例では、最初の行は、IDが`426812829645406216`のトランザクションが``update `t` set `v` =? Where `id` =? ;``ような文を実行しているが、IDが`426812829645406217`の別のトランザクションによってブロックされていることを意味します。IDが`426812829645406217`のトランザクションも``update `t` set `v` =? Where `id` =? ;``のような文を実行していますが、IDが`426812829645406216`のトランザクションによってブロックされています。このように、2つのトランザクションはデッドロックを形成しています。

### いくつかのホットキーはキューロックを引き起こす {#a-few-hot-keys-cause-queueing-locks}

`DATA_LOCK_WAITS`システムテーブルは、TiKVノードのロック待機状態を提供します。このテーブルにクエリを実行すると、TiDBはすべてのTiKVノードからリアルタイムのロック待機情報を自動的に取得します。一部のホットキーが頻繁にロックされ、多くのトランザクションをブロックしている場合は、 `DATA_LOCK_WAITS`テーブルにクエリを実行し、結果をキーごとに集計することで、問題が頻繁に発生するキーを特定できます。

```sql
select `key`, count(*) as `count` from information_schema.data_lock_waits group by `key` order by `count` desc;
```

出力例は次のとおりです。

```sql
+----------------------------------------+-------+
| key                                    | count |
+----------------------------------------+-------+
| 7480000000000000415F728000000000000001 |     2 |
| 7480000000000000415F728000000000000002 |     1 |
+----------------------------------------+-------+
```

不測の事態を回避するために、複数のクエリを実行する必要がある場合があります。

頻繁に問題が発生しているキーがわかっている場合は、 `TIDB_TRX`または`CLUSTER_TIDB_TRX`テーブルからキーをロックしようとしたトランザクションの情報を取得してみることができます。

`TIDB_TRX`と`CLUSTER_TIDB_TRX`テーブルに表示される情報は、クエリ実行時に実行中のトランザクションの情報でもあることに注意してください。これらのテーブルには、完了したトランザクションの情報は表示されません。同時実行トランザクションの数が多い場合、クエリの結果セットも大きくなる可能性があります。5 句または`where`句`limit`使用すると、ロック待機時間が長いトランザクションをフィルタリングできます。Lock ビューで複数のテーブルを結合する場合、異なるテーブルのデータが同時に取得されない可能性があり、異なるテーブルの情報が一致しない可能性があることに注意してください。

たとえば、 `where`句を使用してロック待機時間が長いトランザクションをフィルタリングするには、次の SQL ステートメントを実行します。

```sql
select trx.* from information_schema.data_lock_waits as l left join information_schema.cluster_tidb_trx as trx on l.trx_id = trx.id where l.key = "7480000000000000415F728000000000000001"\G
```

出力例は次のとおりです。

```sql
*************************** 1. row ***************************
               INSTANCE: 127.0.0.1:10080
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
               INSTANCE: 127.0.0.1:10080
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

### トランザクションが長時間ブロックされている {#a-transaction-is-blocked-for-a-long-time}

あるトランザクションが別のトランザクション（または複数のトランザクション）によってブロックされていることが分かっており、かつ現在のトランザクションの`start_ts` （トランザクションID）が分かっている場合、以下の方法でブロックしているトランザクションの情報を取得できます。ただし、Lock ビューで複数のテーブルを結合する場合、異なるテーブルのデータが同時に取得されない可能性があり、異なるテーブルの情報が一致しない可能性があることに注意してください。

```sql
select l.key, trx.*, tidb_decode_sql_digests(trx.all_sql_digests) as sqls from information_schema.data_lock_waits as l join information_schema.cluster_tidb_trx as trx on l.current_holding_trx_id = trx.id where l.trx_id = 426831965449355272\G
```

出力例は次のとおりです。

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

上記のクエリでは、 `CLUSTER_TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列目に[`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数が使用されています。この関数は、この列（値は SQL ダイジェストのセット）を正規化された SQL 文に変換することで、可読性を向上させます。

現在のトランザクションの`start_ts`不明な場合は、 `TIDB_TRX` / `CLUSTER_TIDB_TRX`テーブルまたは[`PROCESSLIST` / `CLUSTER_PROCESSLIST`](/information-schema/information-schema-processlist.md)テーブルの情報から調べることができます。

### メタデータロック {#metadata-locks}

セッションがスキーマの変更を待機している場合、メタデータ ロックが原因である可能性があります。

詳細については[メタデータロック](/metadata-lock.md)参照してください。

## 楽観的ロックの競合のトラブルシューティング {#troubleshoot-optimistic-lock-conflicts}

このセクションでは、楽観的トランザクション モードでの一般的なロック競合の問題の解決策を示します。

### 読み書き競合 {#read-write-conflicts}

TiDBサーバーはクライアントからの読み取り要求を受信すると、物理時刻におけるグローバルに一意で増加するタイムスタンプを現在のトランザクションのstart_tsとして取得します。トランザクションはstart_tsより前の最新のデータ、つまりstart_tsより小さい最新のcommit_tsのターゲットキーを読み取る必要があります。トランザクションがターゲットキーが別のトランザクションによってロックされていることに気づき、そのトランザクションがどのフェーズにあるかを把握できない場合、読み取り/書き込み競合が発生します。図を以下に示します。

![read-write conflict](/media/troubleshooting-lock-pic-04.png)

Txn0はPrewriteフェーズを完了し、Commitフェーズに入ります。この時、Txn1は同じターゲットキーの読み取りを要求します。Txn1は、自身のstart_tsよりも小さい最新のcommit_tsのターゲットキーを読み取る必要があります。Txn1のstart_tsはTxn0のlock_tsよりも大きいため、Txn1はターゲットキーのロックが解除されるまで待機する必要がありますが、まだ解除されていません。その結果、Txn1はTxn0がコミットされたかどうかを確認できません。こうして、Txn1とTxn0の間で読み取り/書き込み競合が発生します。

TiDB クラスター内の読み取り/書き込み競合は、次の方法で検出できます。

1.  TiDBサーバーのメトリックとログの監視

    -   Grafanaによるデータの監視

        TiDBダッシュボードの`KV Errors`パネル目では、 `Lock Resolve OPS`の`not_expired`と`KV Backoff OPS`の`tikvLockFast` `resolve`トランザクションにおける読み取り/書き込み競合を確認するために使用できる監視メトリックです。すべてのメトリックの値が上昇している場合、読み取り/書き込み競合が多数発生している可能性があります。13 `not_expired`項目は、トランザクションのロックがタイムアウトしていないことを意味します。15 `resolve`項目は、他のトランザクションがロックのクリーンアップを試みていることを意味します。17 `tikvLockFast`項目は、読み取り/書き込み競合が発生していることを意味します。

        ![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png) ![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png)

    -   TiDBサーバーのログ

        読み取り/書き込みの競合がある場合は、TiDB ログに次のメッセージが表示されます。

        ```log
        [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
        ```

        -   txnStartTS: 読み取り要求を送信しているトランザクションのstart_ts。上記のログでは、 `416643508703592451`がstart_tsです。
        -   backoff_types: 読み取り/書き込み競合が発生し、読み取り要求がバックオフと再試行を実行する場合、再試行のタイプは`TxnLockFast`なります。
        -   backoff_ms: 読み取りリクエストがバックオフとリトライに要した時間。単位はミリ秒です。上記のログでは、読み取りリクエストはバックオフとリトライに255ミリ秒を費やしています。
        -   region_id: 読み取り要求のターゲット キーに対応するリージョンID。

2.  TiKVサーバーのログ

    読み取り/書き込みの競合がある場合は、TiKV ログに次のメッセージが表示されます。

    ```log
    [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
    ```

    このメッセージは、TiDBで読み取り/書き込み競合が発生したことを示しています。読み取り要求のターゲットキーは別のトランザクションによってロックされています。ロックは、コミットされていない楽観的トランザクションと、プリライトフェーズ後のコミットされていない悲観的トランザクションによって発生しています。

    -   primary_lock: ターゲット キーがプライマリ ロックによってロックされていることを示します。
    -   lock_version: ロックを所有するトランザクションの start_ts。
    -   key: ロックされる対象キー。
    -   lock_ttl: ロックの TTL (Time To Live)
    -   txn_size: ロックを所有するトランザクションのリージョン内にあるキーの数。

解決策:

-   読み取り/書き込み競合が発生すると、自動的にバックオフと再試行が実行されます。上記の例のように、Txn1 にはバックオフと再試行が適用されます。再試行の初回時間は10ミリ秒、最長は3000ミリ秒、合計時間は最大20000ミリ秒です。

-   TiDB コントロールのサブコマンド[`decoder`](/tidb-control.md#the-decoder-command)を使用して、指定したキーに対応する行のテーブル ID と行 ID を表示できます。

    ```sh
    ./tidb-ctl decoder "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    format: table_row
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

### KeyIsLockedエラー {#keyislocked-error}

トランザクションのPrewriteフェーズでは、TiDBは書き込み競合の有無を確認し、対象キーが他のトランザクションによってロックされているかどうかを確認します。キーがロックされている場合、TiKVサーバーは「KeyIsLocked」エラーを出力します。現在、このエラーメッセージはTiDBとTiKVのログには出力されません。読み取り競合と同様に、「KeyIsLocked」エラーが発生した場合、TiDBは自動的にトランザクションのバックオフと再試行を実行します。

Grafana の TiDB モニタリングで「KeyIsLocked」エラーがあるかどうかを確認できます。

TiDBダッシュボードの`KV Errors`パネルには、トランザクションによって発生した書き込み競合を確認するための2つの監視メトリック`Lock Resolve OPS`と`KV Backoff OPS`あります。9 `Lock Resolve OPS` `resolve`番目の項目と`KV Backoff OPS`の`txnLock`番目の項目に明らかな上昇傾向が見られる場合、「KeyIsLocked」エラーが発生します。15 `resolve`ロックを解除しようとする操作を指し、 `txnLock`書き込み競合を表します。

![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png) ![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png)

解決策:

-   監視中にtxnLockが少量発生しても、あまり気にする必要はありません。バックオフとリトライはバックグラウンドで自動的に実行されます。リトライの初回は100ミリ秒、最大1回のリトライ時間は3000ミリ秒です。
-   `KV Backoff OPS`に「txnLock」操作が多すぎる場合は、アプリケーション側から書き込み競合の原因を分析することをお勧めします。
-   アプリケーションで書き込み-書き込み競合が発生するシナリオの場合は、悲観的トランザクション モードを使用することを強くお勧めします。

### LockNotFoundエラー {#locknotfound-error}

「TxnLockNotFound」というエラーログは、トランザクションのコミット時間がTTL時間よりも長く、トランザクションをコミットしようとした際に、そのロックが他のトランザクションによってロールバックされたことを意味します。TiDBサーバーがトランザクションコミットの再試行を有効にしている場合、このトランザクションは[tidb_retry_limit](/system-variables.md#tidb_retry_limit)に従って再実行されます。（明示的トランザクションと暗黙的トランザクションの違いに注意してください。）

「LockNotFound」エラーがあるかどうかは、次の方法で確認できます。

1.  TiDBサーバーのログをビュー

    「TxnLockNotFound」エラーが発生した場合、TiDB ログ メッセージは次のようになります。

    ```log
    [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
    ```

    -   start_ts: 他のトランザクションによってロックがロールバックされたためにエラー`TxnLockNotFound`出力したトランザクションのstart_ts。上記のログでは、 `412720515987275779`がstart_tsです。
    -   commit_ts: エラー`TxnLockNotFound`を出力したトランザクションのcommit_ts。上記のログでは、 `412720519984971777`がcommit_tsです。

2.  TiKVサーバーのログをビュー

    「TxnLockNotFound」エラーが発生した場合、TiKV ログ メッセージは次のようになります。

    ```log
    Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
    ```

解決策:

-   start_ts と commit_ts 間の時間間隔を確認することで、コミット時間が TTL 時間を超えているかどうかを確認できます。

    PD 制御ツールを使用して時間間隔を確認します。

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd tso [start_ts]
    tiup ctl:v<CLUSTER_VERSION> pd tso [commit_ts]
    ```

-   書き込みパフォーマンスが遅いかどうかをチェックすることをお勧めします。書き込みパフォーマンスが遅いと、トランザクションのコミットの効率が低下し、ロックがクリアされる可能性があります。

-   TiDB トランザクションの再試行を無効にする場合は、アプリケーション側で例外をキャッチして再試行する必要があります。

## 悲観的ロックの競合のトラブルシューティング {#troubleshoot-pessimistic-lock-conflicts}

このセクションでは、悲観的トランザクション モードでの一般的なロック競合の問題の解決策を示します。

> **注記：**
>
> 悲観的・トランザクション・モードが設定されている場合でも、自動コミット・トランザクションはまず楽観的・モードでコミットを試行します。競合が発生した場合、自動再試行中にトランザクションは悲観的・トランザクション・モードに切り替わります。

### 読み書き競合 {#read-write-conflicts}

エラー メッセージと解決策は、楽観的ロックの競合の[読み取り書き込み競合](#read-write-conflicts)と同じです。

### 悲観的ロック再試行制限に達しました {#pessimistic-lock-retry-limit-reached}

トランザクションの競合が非常に深刻な場合、または書き込みの競合が発生した場合、楽観的トランザクションは直接終了され、悲観的トランザクションは書き込みの競合がなくなるまでstorageからの最新のデータを使用してステートメントを再試行します。

TiDBのロック操作は書き込み操作であり、そのプロセスはまず読み取り、次に書き込みであるため、RPCリクエストは2つあります。トランザクションの途中で書き込み競合が発生した場合、TiDBは対象キーのロックを再度試行し、各再試行はTiDBログに出力されます。再試行回数は[pessimistic-txn。max-retry-count](/tidb-configuration-file.md#max-retry-count)です。

悲観的トランザクション モードでは、書き込み競合が発生し、再試行回数が上限に達すると、次のキーワードを含むエラー メッセージが TiDB ログに表示されます。

```log
err="pessimistic lock retry limit reached"
```

解決策:

-   上記エラーが頻繁に発生する場合は、アプリケーション側からの調整をお勧めします。
-   同一行（同一キー）への同時ロックが多く、頻繁に競合が発生する業務の場合は、システム変数[`tidb_pessimistic_txn_fair_locking`](/system-variables.md#tidb_pessimistic_txn_fair_locking-new-in-v700)有効化を検討してください。ただし、この変数を有効にすると、ロック競合が発生するトランザクションのスループット低下（平均レイテンシーの増加）が多少発生する可能性がある点にご注意ください。新規に導入されたクラスターでは、この変数はデフォルトで有効化（ `ON` ）されています。

### ロック待機タイムアウトを超えました {#lock-wait-timeout-exceeded}

悲観的トランザクションモードでは、トランザクションは互いのロックを待機します。ロック待機のタイムアウトは、TiDBのパラメータ[innodb_lock_wait_timeout](/pessimistic-transaction.md#behaviors)によって定義されます。これは、SQL文レベルでの最大ロック待機時間であり、SQL文がロックを要求したがロックが取得されなかった場合に想定される時間です。この時間が経過すると、TiDBは再びロックを試行せず、対応するエラーメッセージをクライアントに返します。

待機ロックのタイムアウトが発生すると、次のエラー メッセージがクライアントに返されます。

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```

解決策:

-   上記のエラーが頻繁に発生する場合は、アプリケーションロジックを調整することをお勧めします。

### TTLマネージャがタイムアウトしました {#ttl-manager-has-timed-out}

トランザクションの実行時間はGCのタイムリミットを超えることはできません。また、悲観的トランザクションのTTL時間には上限があり、デフォルト値は1時間です。そのため、1時間を超えて実行された悲観的トランザクションはコミットに失敗します。このタイムアウトしきい値は、TiDBパラメータ[`performance.max-txn-ttl`](https://github.com/pingcap/tidb/blob/release-8.5/pkg/config/config.toml.example)によって制御されます。

悲観的トランザクションの実行時間が TTL 時間を超えると、TiDB ログに次のエラー メッセージが表示されます。

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

解決策:

-   まず、アプリケーションロジックを最適化できるかどうかを確認します。例えば、大規模なトランザクションはTiDBのトランザクションサイズ制限に達する可能性があり、それを複数の小さなトランザクションに分割できます。
-   また、アプリケーションのトランザクション ロジックに合わせて関連パラメータを適切に調整することもできます。

### ロックを取得しようとしたときにデッドロックが見つかりました {#deadlock-found-when-trying-to-get-lock}

2つ以上のトランザクション間でリソースの競合が発生すると、デッドロックが発生します。手動で対処しないと、互いにブロックし合うトランザクションは正常に実行されず、永遠に待機状態になります。デッドロックを解決するには、いずれかのトランザクションを手動で終了し、他のトランザクション要求を再開する必要があります。

悲観的トランザクションでデッドロックが発生した場合、デッドロックを解除するには、いずれかのトランザクションを終了させる必要があります。クライアントはMySQLと同じ`Error 1213`エラーを返します。例：

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```

解決策:

-   デッドロックの原因を確認するのが難しい場合は、v5.1以降のバージョンでは、 `INFORMATION_SCHEMA.DEADLOCKS`または`INFORMATION_SCHEMA.CLUSTER_DEADLOCKS`システムテーブルをクエリして、デッドロック待機チェーンの情報を取得することをお勧めします。詳細については、 [デッドロックエラー](#deadlock-errors)セクションと[`DEADLOCKS`テーブル](/information-schema/information-schema-deadlocks.md)ドキュメントを参照してください。
-   デッドロックが頻繁に発生する場合は、そのような発生を減らすために、アプリケーション内のトランザクション クエリ ロジックを調整する必要があります。
