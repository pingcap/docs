---
title: Latency Breakdown
summary: TiDB のレイテンシーと、実際の使用例でレイテンシーを分析する方法について詳しく紹介します。
---

# レイテンシーの内訳 {#latency-breakdown}

このドキュメントでは、レイテンシーをメトリックに分解し、次の側面からユーザーの観点から分析します。

-   [一般的なSQLレイヤー](#general-sql-layer)
-   [クエリを読む](#read-queries)
-   [クエリを書く](#write-queries)
-   [バッチクライアント](#batch-client)
-   [TiKVスナップショット](#tikv-snapshot)
-   [非同期書き込み](#async-write)

これらの分析により、 TiDB SQLクエリの実行時間コストに関する詳細な情報が得られます。これは、TiDBのクリティカルパス診断のガイドです。さらに、第[診断のユースケース](#diagnosis-use-cases)セクションでは、実際のユースケースにおけるレイテンシーの分析方法を紹介します。

このドキュメントを読む前に、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md)お読みください。レイテンシーをメトリクスに分解する際、特定の遅いクエリではなく、実行時間またはレイテンシーの平均値を計算することに注意してください。多くのメトリクスは、実行時間またはレイテンシーの分布を示すヒストグラムとして表示されます。平均レイテンシーを計算するには、以下の合計とカウントのカウンタを使用する必要があります。

    avg = ${metric_name}_sum / ${metric_name}_count

このドキュメントで説明されているメトリックは、TiDB の Prometheus ダッシュボードから直接読み取ることができます。

## 一般的なSQLレイヤー {#general-sql-layer}

この一般的なSQLレイヤーのレイテンシーはTiDBの最上位レベルに存在し、すべてのSQLクエリで共有されます。以下は、一般的なSQLレイヤーの操作にかかる時間コストのグラフです。

```railroad+diagram
Diagram(
    NonTerminal("Token wait duration"),
    Choice(
        0,
        Comment("Prepared statement"),
        NonTerminal("Parse duration"),
    ),
    OneOrMore(
        Sequence(
        Choice(
            0,
            NonTerminal("Optimize prepared plan duration"),
            Sequence(
            Comment("Plan cache miss"),
            NonTerminal("Compile duration"),
            ),
        ),
        NonTerminal("TSO wait duration"),
        NonTerminal("Execution duration"),
        ),
        Comment("Retry"),
    ),
)
```

一般的な SQLレイヤーのレイテンシーは`e2e duration`メトリックとして観察され、次のように計算されます。

```text
e2e duration =
    tidb_server_get_token_duration_seconds +
    tidb_session_parse_duration_seconds +
    tidb_session_compile_duration_seconds +
    tidb_session_execute_duration_seconds{type="general"}
```

-   `tidb_server_get_token_duration_seconds`トークンの待機時間を記録します。これは通常1ミリ秒未満であり、無視できるほど小さい値です。
-   `tidb_session_parse_duration_seconds` SQL クエリを抽象構文ツリー (AST) に解析する時間を記録します。これは[`PREPARE/EXECUTE`ステートメント](/develop/dev-guide-optimize-sql-best-practices.md#use-prepare)でスキップできます。
-   `tidb_session_compile_duration_seconds` AST を実行プランにコンパイルする時間を記録し、これは[SQL 準備済み実行プランキャッシュ](/sql-prepared-plan-cache.md)でスキップできます。
-   `tidb_session_execute_duration_seconds{type="general"}`実行時間を記録しますが、これにはあらゆる種類のユーザークエリが混在します。パフォーマンスの問題やボトルネックを分析するには、これを細分化した期間に分割する必要があります。

一般的に、OLTP（オンライントランザクション処理）ワークロードは、重要なコードを共有する読み取りクエリと書き込みクエリに分けられます。以下のセクションでは、実行方法が異なる[読み取りクエリ](#read-queries)と[クエリを書く](#write-queries)のレイテンシーについて説明します。

## クエリを読む {#read-queries}

読み取りクエリにはプロセス フォームが 1 つだけあります。

### ポイントゲット {#point-get}

以下は[ポイントゲット](/glossary.md#point-get)操作の時間コスト図です。

```railroad+diagram
Diagram(
    Choice(
        0,
        NonTerminal("Resolve TSO"),
        Comment("Read by clustered PK in auto-commit-txn mode or snapshot read"),
    ),
    Choice(
        0,
        NonTerminal("Read handle by index key"),
        Comment("Read by clustered PK, encode handle by key"),
    ),
    NonTerminal("Read value by handle"),
)
```

ポイント獲得中、 `tidb_session_execute_duration_seconds{type="general"}`期間は次のように計算されます。

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handle duration +
    read value duration
```

`pd_client_cmd_handle_cmds_duration_seconds{type="wait"}` PDから[TSO (タイムスタンプ オラクル)](/tso.md)取得するのに要した時間を記録します。クラスター化プライマリインデックスを使用した自動コミットトランザクションモード、またはスナップショットからの読み取りの場合、値は0になります。

`read handle duration`と`read value duration`次のように計算されます。

```text
read handle duration = read value duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="Get"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

`tidb_tikvclient_request_seconds{type="Get"}` 、バッチ処理された gRPC ラッパーを介して TiKV に直接送信される GET リクエストの継続時間を記録します`tidb_tikvclient_batch_wait_duration` 、 `tidb_tikvclient_batch_send_latency` 、 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`などの先行するバッチクライアントの継続時間の詳細については、 [バッチクライアント](#batch-client)セクションを参照してください。

`tikv_grpc_msg_duration_seconds{type="kv_get"}`期間は次のように計算されます。

```text
tikv_grpc_msg_duration_seconds{type="kv_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    tikv_engine_seek_micro_seconds{type="seek_average"} +
    read value duration +
    read value duration(non-short value)
```

この時点で、リクエストはTiKVに格納されます。TiKVは、1回のシークと1回または2回の読み取りアクションでリクエストを処理します（短い値は書き込みカラムファミリーにエンコードされており、一度読み取れば十分です）。TiKVは、読み取りリクエストを処理する前にスナップショットを取得します。TiKVスナップショットの持続時間の詳細については、セクション[TiKVスナップショット](#tikv-snapshot)を参照してください。

`read value duration(from disk)`は次のように計算されます。

```text
read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="get/batch_get_command"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="get/batch_get_command"}))
```

TiKVはstorageエンジンとしてRocksDBを使用します。必要な値がブロックキャッシュに存在しない場合、TiKVはディスクから値をロードする必要があります。1 `tikv_storage_rocksdb_perf`場合、getリクエストは`get`または`batch_get_command`いずれかになります。

### バッチポイント取得 {#batch-point-get}

以下はバッチ ポイント取得操作の時間コスト図です。

```railroad+diagram
Diagram(
  NonTerminal("Resolve TSO"),
  Choice(
    0,
    NonTerminal("Read all handles by index keys"),
    Comment("Read by clustered PK, encode handle by keys"),
  ),
  NonTerminal("Read values by handles"),
)
```

バッチポイント取得中、 `tidb_session_execute_duration_seconds{type="general"}`次のように計算されます。

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handles duration +
    read values duration
```

バッチ ポイント取得のプロセスは、バッチ ポイント取得が複数の値を同時に読み取る点を除いて、 [ポイントゲット](#point-get)とほぼ同じです。

`read handles duration`と`read values duration`次のように計算されます。

```text
read handles duration = read values duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="BatchGet"} =
    tidb_tikvclient_batch_wait_duration(transaction) +
    tidb_tikvclient_batch_send_latency(transaction) +
    tikv_grpc_msg_duration_seconds{type="kv_batch_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}(transaction)
```

`tidb_tikvclient_batch_wait_duration(transaction)` 、 `tidb_tikvclient_batch_send_latency(transaction)` 、 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}(transaction)`などの前述のバッチ クライアント期間の詳細については、 [バッチクライアント](#batch-client)セクションを参照してください。

`tikv_grpc_msg_duration_seconds{type="kv_batch_get"}`期間は次のように計算されます。

```text
tikv_grpc_msg_duration_seconds{type="kv_batch_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    n * (
        tikv_engine_seek_micro_seconds{type="seek_max"} +
        read value duration +
        read value duration(non-short value)
    )

read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="batch_get"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="batch_get"}))
```

スナップショットを取得した後、TiKVは同じスナップショットから複数の値を読み取ります。読み取り時間は[ポイントゲット](#point-get)と同じです。TiKVがディスクからデータを読み込む場合の平均時間は、 `tikv_storage_rocksdb_perf`と`req="batch_get"`で計算できます。

### テーブルスキャンとインデックススキャン {#table-scan-x26-index-scan}

以下は、テーブルスキャンとインデックススキャン操作の時間コスト図です。

```railroad+diagram
Diagram(
    Stack(
        NonTerminal("Resolve TSO"),
        NonTerminal("Load region cache for related table/index ranges"),
        OneOrMore(
            NonTerminal("Wait for result"),
            Comment("Next loop: drain the result"),
        ),
    ),
)
```

テーブル スキャンおよびインデックス スキャン中、 `tidb_session_execute_duration_seconds{type="general"}`期間は次のように計算されます。

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )
    tidb_distsql_handle_query_duration_seconds{sql_type="general"} <= send request duration
```

テーブルスキャンとインデックススキャンは同じように処理されます。1 `req_per_copr`分散タスク数です。コプロセッサの実行とクライアントへのデータ応答は異なるスレッドで行われるため、待機時間は`tidb_distsql_handle_query_duration_seconds{sql_type="general"}`となり、 `send request duration`よりも短くなります。

`send request duration`と`req_per_copr`次のように計算されます。

```text
send request duration =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="coprocessor"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tikv_grpc_msg_duration_seconds{type="coprocessor"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} +
    tikv_coprocessor_request_wait_seconds{type="schedule"} +
    tikv_coprocessor_request_handler_build_seconds{type="index/select"} +
    tikv_coprocessor_request_handle_seconds{type="index/select"}

req_per_copr = rate(tidb_distsql_handle_query_duration_seconds_count) / rate(tidb_distsql_scan_keys_partial_num_count)
```

TiKVでは、テーブルスキャンタイプは`select` 、インデックススキャンタイプは`index`です。5と`select` `index`タイプの所要時間の詳細は同じです。

### インデックス検索 {#index-look-up}

以下は、インデックス検索操作の時間コスト図です。

```railroad+diagram
Diagram(
    Stack(
        NonTerminal("Resolve TSO"),
        NonTerminal("Load region cache for related index ranges"),
        OneOrMore(
            Sequence(
                NonTerminal("Wait for index scan result"),
                NonTerminal("Wait for table scan result"),
            ),
        Comment("Next loop: drain the result"),
        ),
    ),
)
```

インデックス検索中、 `tidb_session_execute_duration_seconds{type="general"}`期間は次のように計算されます。

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    ) +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )

req_per_copr = rate(tidb_distsql_handle_query_duration_seconds_count) / rate(tidb_distsql_scan_keys_partial_num_count)
```

インデックス ルックアップは、パイプラインで処理されるインデックス スキャンとテーブル スキャンを組み合わせたものです。

## クエリを書く {#write-queries}

書き込みクエリは読み取りクエリよりもはるかに複雑です。書き込みクエリにはいくつかのバリエーションがあります。以下は、書き込みクエリ操作の時間コストのグラフです。

```railroad+diagram
Diagram(
    NonTerminal("Execute write query"),
    Choice(
        0,
        NonTerminal("Pessimistic lock keys"),
        Comment("bypass in optimistic transaction"),
    ),
    Choice(
        0,
        NonTerminal("Auto Commit Transaction"),
        Comment("bypass in non-auto-commit or explicit transaction"),
    ),
)
```

|         | 悲観的な取引          | 楽観的な取引    |
| ------- | --------------- | --------- |
| 自動コミット  | 実行 + ロック + コミット | 実行 + コミット |
| 非自動コミット | 実行 + ロック        | 実行する      |

書き込みクエリは次の 3 つのフェーズに分かれています。

-   実行フェーズ: 変更を実行し、TiDB のメモリに書き込みます。
-   ロックフェーズ: 実行結果に対して悲観的ロックを取得します。
-   コミット フェーズ: 2 フェーズ コミット プロトコル (2PC) を使用してトランザクションをコミットします。

実行フェーズでは、TiDBはメモリ内のデータを操作します。主なレイテンシーは必要なデータの読み取りに起因します。更新クエリと削除クエリの場合、TiDBはまずTiKVからデータを読み取り、次にメモリ内の行を更新または削除します。

例外はポイントゲットとバッチポイントゲットによるロックタイム読み取り操作（ `SELECT FOR UPDATE` ）で、これは1回のリモートプロシージャコール（RPC）で読み取りとロックを実行します。

### ロックタイムポイント取得 {#lock-time-point-get}

以下は、ロックタイムポイント取得操作の時間コスト図です。

```railroad+diagram
Diagram(
    Choice(
        0,
        Sequence(
            NonTerminal("Read handle key by index key"),
            NonTerminal("Lock index key"),
        ),
        Comment("Clustered index"),
    ),
    NonTerminal("Lock handle key"),
    NonTerminal("Read value from pessimistic lock cache"),
)
```

ロックタイムポイントの取得中、 `execution(clustered PK)`と`execution(non-clustered PK or UK)`期間は次のように計算されます。

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    2 * tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

ロックタイムポイント取得はキーをロックし、その値を返します。実行後のロックフェーズと比較すると、1ラウンドトリップを節約できます。ロックタイムポイント取得の実行時間は[ロック期間](#lock)として扱うことができます。

### ロックタイムバッチポイント取得 {#lock-time-batch-point-get}

以下は、ロックタイム バッチ ポイント取得操作の時間コスト図です。

```railroad+diagram
Diagram(
    Choice(
        0,
        NonTerminal("Read handle keys by index keys"),
        Comment("Clustered index"),
    ),
    NonTerminal("Lock index and handle keys"),
    NonTerminal("Read values from pessimistic lock cache"),
)
```

ロックタイム バッチ ポイント取得中、 `execution(clustered PK)`と`execution(non-clustered PK or UK)`期間は次のように計算されます。

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} +
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

ロックタイムバッチポイント取得の実行は、1回のRPCで複数の値を読み取る点を除けば、 [ロックタイムポイント取得](#lock-time-point-get)と同様です。3 `tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"}`所要時間の詳細については、 [バッチポイント取得](#batch-point-get)セクションを参照してください。

### ロック {#lock}

このセクションでは、ロック期間について説明します。

```text
round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_pessimistic_lock"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_pessimistic_lock"})) /
    committer-concurrency
)

lock = tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"} =
    round * tidb_tikvclient_request_seconds{type="PessimisticLock"}
```

ロックは、フロー制御機構を備えた2PC構造を通じて取得されます。フロー制御は、同時オンザフライリクエスト数を`committer-concurrency`に制限します（デフォルト値は`128` ）。簡略化のため、フロー制御はリクエストレイテンシーの増幅（ `round` ）として扱うことができます。

`tidb_tikvclient_request_seconds{type="PessimisticLock"}`は次のように計算されます。

```text
tidb_tikvclient_request_seconds{type="PessimisticLock"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

`tidb_tikvclient_batch_wait_duration` 、 `tidb_tikvclient_batch_send_latency` 、 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`などの前述のバッチ クライアント期間の詳細については、 [バッチクライアント](#batch-client)セクションを参照してください。

`tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"}`期間は次のように計算されます。

```text
tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} =
    tikv_scheduler_latch_wait_duration_seconds{type="acquire_pessimistic_lock"} +
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    (lock in-mem key count + lock on-disk key count) * lock read duration +
    lock on-disk key count / (lock in-mem key count + lock on-disk key count) *
    lock write duration
```

-   TiDB v6.0以降、TiKVはデフォルトで[メモリ内悲観的ロック](/pessimistic-transaction.md#in-memory-pessimistic-lock)使用します。メモリ内悲観的ロックは非同期書き込みプロセスをバイパスします。

-   `tikv_storage_engine_async_request_duration_seconds{type="snapshot"}`はスナップショットタイプの期間です。詳細については、 [TiKVスナップショット](#tikv-snapshot)セクションを参照してください。

-   `lock in-mem key count`と`lock on-disk key count`次のように計算されます。

    ```text
    lock in-mem key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="success"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))

    lock on-disk key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="full"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))
    ```

    メモリ内およびディスク上のロックされたキーの数は、メモリ内ロックカウンタによって計算できます。TiKVはロックを取得する前にキーの値を読み取り、読み取り時間はRocksDBパフォーマンスコンテキストによって計算できます。

    ```text
    lock read duration(from disk) =
        sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="acquire_pessimistic_lock"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="acquire_pessimistic_lock"}))
    ```

-   `lock write duration`はディスク上の書き込みロックの持続時間です。詳細については、 [非同期書き込み](#async-write)セクションを参照してください。

### 専念 {#commit}

このセクションではコミットの所要時間について説明します。以下はコミット操作の時間コストのグラフです。

```railroad+diagram
Diagram(
    Stack(
        Sequence(
            Choice(
                0,
                Comment("use 2pc or causal consistency"),
                NonTerminal("Get min-commit-ts"),
            ),
            Optional("Async prewrite binlog"),
            NonTerminal("Prewrite mutations"),
            Optional("Wait prewrite binlog result"),
        ),
        Sequence(
            Choice(
                1,
                Comment("1pc"),
                Sequence(
                    Comment("2pc"),
                    NonTerminal("Get commit-ts"),
                    NonTerminal("Check schema"),
                    NonTerminal("Commit PK mutation"),
                ),
                Sequence(
                    Comment("async-commit"),
                    NonTerminal("Commit mutations asynchronously"),
                ),
            ),
            Choice(
                0,
                Comment("committed"),
                NonTerminal("Async cleanup"),
            ),
            Optional("Commit binlog"),
        ),
    ),
)
```

コミット フェーズの期間は次のように計算されます。

```text
commit =
    Get_latest_ts_time +
    Prewrite_time +
    Get_commit_ts_time +
    Commit_time

Get_latest_ts_time = Get_commit_ts_time =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"}

prewrite_round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_prewrite"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_prewrite"})) /
    committer-concurrency
)

commit_round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_commit"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_commit"})) /
    committer-concurrency
)

Prewrite_time =
    prewrite_round * tidb_tikvclient_request_seconds{type="Prewrite"}

Commit_time =
    commit_round * tidb_tikvclient_request_seconds{type="Commit"}
```

コミット期間は、次の 4 つの指標に分類できます。

-   `Get_latest_ts_time` 、非同期コミットまたはシングル フェーズ コミット (1PC) トランザクションで最新の TSO を取得するのにかかる時間を記録します。
-   `Prewrite_time`事前書き込みフェーズの期間を記録します。
-   `Get_commit_ts_time` 、一般的な 2PC トランザクションの期間を記録します。
-   `Commit_time`コミットフェーズの所要時間を記録します。非同期コミットまたは1PCトランザクションにはこのフェーズはありません。

悲観的ロックと同様に、フロー制御はレイテンシー(前の式の`prewrite_round`と`commit_round` ) の増幅として機能します。

`tidb_tikvclient_request_seconds{type="Prewrite"}`と`tidb_tikvclient_request_seconds{type="Commit"}`期間は次のように計算されます。

```text
tidb_tikvclient_request_seconds{type="Prewrite"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_prewrite"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tidb_tikvclient_request_seconds{type="Commit"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_commit"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

`tidb_tikvclient_batch_wait_duration` 、 `tidb_tikvclient_batch_send_latency` 、 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`などの前述のバッチ クライアント期間の詳細については、 [バッチクライアント](#batch-client)セクションを参照してください。

`tikv_grpc_msg_duration_seconds{type="kv_prewrite"}`は次のように計算されます。

```text
tikv_grpc_msg_duration_seconds{type="kv_prewrite"} =
    prewrite key count * prewrite read duration +
    prewrite write duration

prewrite key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="prewrite"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="prewrite"}))

prewrite read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="prewrite"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="prewrite"}))
```

TiKVのロックと同様に、事前書き込みは読み取りフェーズと書き込みフェーズで処理されます。読み取り時間はRocksDBパフォーマンスコンテキストから計算できます。書き込み時間の詳細については、セクション[非同期書き込み](#async-write)を参照してください。

`tikv_grpc_msg_duration_seconds{type="kv_commit"}`は次のように計算されます。

```text
tikv_grpc_msg_duration_seconds{type="kv_commit"} =
    commit key count * commit read duration +
    commit write duration

commit key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="commit"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="commit"}))

commit read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="commit"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="commit"})) (storage)
```

`kv_commit`の所要時間は`kv_prewrite`とほぼ同じです。書き込み所要時間の詳細については、 [非同期書き込み](#async-write)セクションを参照してください。

## バッチクライアント {#batch-client}

以下はバッチ クライアントの時間コスト図です。

```railroad+diagram
Diagram(
    NonTerminal("Get conn pool to the target store"),
    Choice(
        0,
        Sequence(
            Comment("Batch enabled"),
                NonTerminal("Push request to channel"),
                NonTerminal("Wait response"),
            ),
            Sequence(
            NonTerminal("Get conn from pool"),
            NonTerminal("Call RPC"),
            Choice(
                0,
                Comment("Unary call"),
                NonTerminal("Recv first"),
            ),
        ),
    ),
)
```

-   リクエストの送信にかかる全体的な所要時間は`tidb_tikvclient_request_seconds`と測定されます。
-   RPC クライアントは各ストアへの接続プール (ConnArray という名前) を維持し、各プールにはバッチ要求 (送信) チャネルを持つ BatchConn があります。
-   ストアが TiKV であり、バッチ サイズが正の場合、バッチが有効になります。これはほとんどの場合に当てはまります。
-   バッチ要求チャネルのサイズは[`tikv-client.max-batch-size`](/tidb-configuration-file.md#max-batch-size) (デフォルトは`128` ) で、エンキューの期間は`tidb_tikvclient_batch_wait_duration`として観測されます。
-   ストリーム要求には`CmdBatchCop` 、 `CmdCopStream` 、 `CmdMPPConn` 3 種類があり、ストリームから最初の応答を取得するために追加の`recv()`呼び出しが必要になります。

まだいくらかのレイテンシーが観測されていますが、 `tidb_tikvclient_request_seconds`次のように概算できます。

```text
tidb_tikvclient_request_seconds{type="?"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_?"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

-   `tidb_tikvclient_batch_wait_duration`バッチ システムでの待機期間を記録します。
-   `tidb_tikvclient_batch_send_latency`バッチ システムでのエンコード期間を記録します。
-   `tikv_grpc_msg_duration_seconds{type="kv_?"}`は TiKV 処理期間です。
-   `tidb_tikvclient_rpc_net_latency_seconds`ネットワークレイテンシーを記録します。

## TiKVスナップショット {#tikv-snapshot}

以下は、TiKV スナップショット操作の時間コスト図です。

```railroad+diagram
Diagram(
    Choice(
        0,
        Comment("Local Read"),
        Sequence(
            NonTerminal("Propose Wait"),
            NonTerminal("Read index Read Wait"),
        ),
    ),
    NonTerminal("Fetch A Snapshot From KV Engine"),
)
```

TiKV スナップショットの全体的な継続時間は`tikv_storage_engine_async_request_duration_seconds{type="snapshot"}`として観測され、次のように計算されます。

```text
tikv_storage_engine_async_request_duration_seconds{type="snapshot"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} =
    tikv_raftstore_request_wait_time_duration_secs +
    tikv_raftstore_commit_log_duration_seconds +
    get snapshot from rocksdb duration
```

リーダー リースの有効期限が切れると、TiKV は RocksDB からスナップショットを取得する前に読み取りインデックス コマンドを提案します`tikv_raftstore_request_wait_time_duration_secs`と`tikv_raftstore_commit_log_duration_seconds`読み取りインデックス コマンドをコミットする期間です。

RocksDB からスナップショットを取得する操作は通常は高速なので、 `get snapshot from rocksdb duration`無視されます。

## 非同期書き込み {#async-write}

非同期書き込みは、TiKV がコールバックを使用して Raft ベースの複製されたステート マシンに非同期的にデータを書き込むプロセスです。

-   以下は、非同期 IO が無効になっている場合の非同期書き込み操作の時間コスト図です。

    ```railroad+diagram
    Diagram(
        NonTerminal("Propose Wait"),
        NonTerminal("Process Command"),
        Choice(
            0,
            Sequence(
                NonTerminal("Wait Current Batch"),
                NonTerminal("Write to Log Engine"),
            ),
            Sequence(
                NonTerminal("RaftMsg Send Wait"),
                NonTerminal("Commit Log Wait"),
            ),
        ),
        NonTerminal("Apply Wait"),
        NonTerminal("Apply Log"),
    )
    ```

-   以下は、非同期 IO が有効な場合の非同期書き込み操作の時間コスト図です。

    ```railroad+diagram
    Diagram(
        NonTerminal("Propose Wait"),
        NonTerminal("Process Command"),
        Choice(
            0,
            NonTerminal("Wait Until Persisted by Write Worker"),
            Sequence(
                NonTerminal("RaftMsg Send Wait"),
                NonTerminal("Commit Log Wait"),
            ),
        ),
        NonTerminal("Apply Wait"),
        NonTerminal("Apply Log"),
    )
    ```

非同期書き込み時間は次のように計算されます。

```text
async write duration(async io disabled) =
    propose +
    async io disabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds

async write duration(async io enabled) =
    propose +
    async io enabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds
```

非同期書き込みは次の 3 つのフェーズに分けられます。

-   提案する
-   専念
-   適用：上記の式に`tikv_raftstore_apply_wait_time_duration_secs + tikv_raftstore_apply_log_duration_seconds`代入する

提案フェーズの期間は次のように計算されます。

```text
propose =
    propose wait duration +
    propose duration

propose wait duration =
    tikv_raftstore_store_wf_batch_wait_duration_seconds

propose duration =
    tikv_raftstore_store_wf_send_to_queue_duration_seconds -
    tikv_raftstore_store_wf_batch_wait_duration_seconds
```

Raftプロセスはウォーターフォール方式で記録されます。そのため、提案された所要時間は2つのメトリックの差から計算されます。

コミット フェーズの期間は次のように計算されます。

```text
async io disabled commit = max(
    persist log locally duration,
    replicate log duration
)

async io enabled commit = max(
    wait by write worker duration,
    replicate log duration
)
```

v5.3.0以降、TiKVはAsync IO Raft （StoreWriterスレッドプールによるRaftログの書き込み）をサポートしています。Async IO Raftは、 [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530)正の値に設定されている場合にのみ有効になり、コミットプロセスが変更されます。3と`persist log locally duration` `wait by write worker duration`以下のように計算されます。

```text
persist log locally duration =
    batch wait duration +
    write to raft db duration

batch wait duration =
    tikv_raftstore_store_wf_before_write_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

write to raft db duration =
    tikv_raftstore_store_wf_write_end_duration_seconds -
    tikv_raftstore_store_wf_before_write_duration_seconds

wait by write worker duration =
    tikv_raftstore_store_wf_persist_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds
```

非同期IOの有無の違いは、ログがローカルに保持される期間です。非同期IOを使用する場合、ログがローカルに保持される期間は、ウォーターフォールメトリックから直接計算できます（バッチ待機時間は考慮されません）。

レプリケートログ期間は、クォーラムピアに保持されたログの期間を記録します。これには、RPC期間と過半数に保持されたログの期間が含まれます。1は`replicate log duration`のように計算されます。

```text
replicate log duration =
    raftmsg send wait duration +
    commit log wait duration

raftmsg send wait duration =
    tikv_raftstore_store_wf_send_proposal_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

commit log wait duration =
    tikv_raftstore_store_wf_commit_log_duration -
    tikv_raftstore_store_wf_send_proposal_duration_seconds
```

### RaftDB {#raft-db}

以下は、 Raft DB 操作の時間コスト図です。

```railroad+diagram
Diagram(
    NonTerminal("Wait for Writer Leader"),
    NonTerminal("Write and Sync Log"),
    NonTerminal("Apply Log to Memtable"),
)
```

```text
write to raft db duration = raft db write duration
commit log wait duration >= raft db write duration

raft db write duration(raft engine enabled) =
    raft_engine_write_preprocess_duration_seconds +
    raft_engine_write_leader_duration_seconds +
    raft_engine_write_apply_duration_seconds

raft db write duration(raft engine disabled) =
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_memtable_time"}
```

クォーラム ピアの最長期間は`commit log wait duration`であるため、 `raft db write duration`よりも大きくなる可能性があります。

v6.1.0 以降、TiKV はデフォルトのログstorageエンジンとして[Raft Engine](/glossary.md#raft-engine)使用するようになり、ログの書き込みプロセスが変更されました。

### KV DB {#kv-db}

以下は、KV DB 操作の時間コスト図です。

```railroad+diagram
Diagram(
    NonTerminal("Wait for Writer Leader"),
    NonTerminal("Preprocess"),
    Choice(
        0,
        Comment("No Need to Switch"),
        NonTerminal("Switch WAL or Memtable"),
    ),
    NonTerminal("Write and Sync WAL"),
    NonTerminal("Apply to Memtable"),
)
```

```text
tikv_raftstore_apply_log_duration_seconds =
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_memtable_time"}
```

非同期書き込みプロセスでは、コミットされたログをKV DBに適用する必要があります。適用時間はRocksDBのパフォーマンスコンテキストから計算できます。

## 診断のユースケース {#diagnosis-use-cases}

前のセクションでは、クエリ実行時の時間コスト指標について詳細に説明しました。このセクションでは、読み取りまたは書き込みクエリが遅い場合に指標を分析するための一般的な手順を紹介します。すべての指標は、 [パフォーマンス概要ダッシュボード](/grafana-performance-overview-dashboard.md)の「データベース時間」パネルで確認できます。

### 遅い読み取りクエリ {#slow-read-queries}

`SELECT`ステートメントがデータベース時間の大部分を占める場合、TiDB の読み取りクエリが遅いと想定できます。

遅いクエリの実行プランは、TiDBダッシュボードの[Top SQL文](/dashboard/dashboard-overview.md#top-sql-statements)パネルに表示されます。遅い読み取りクエリの時間コストを調査するには、前述の説明に従って[ポイントゲット](#point-get) 、および[シンプルなコプロセッサクエリ](#table-scan--index-scan) [バッチポイント取得](#batch-point-get)できます。

### 書き込みクエリが遅い {#slow-write-queries}

書き込み速度が遅い原因を調査する前に、 `tikv_scheduler_latch_wait_duration_seconds_sum{type="acquire_pessimistic_lock"} by (instance)`を確認して競合の原因をトラブルシューティングする必要があります。

-   特定の TiKV インスタンスでこのメトリックが高い場合、ホットなリージョンで競合が発生している可能性があります。
-   このメトリックがすべてのインスタンスにわたって高い場合、アプリケーションに競合が発生している可能性があります。

アプリケーションからの競合の原因を確認した後、 [ロック](#lock)と[専念](#commit)期間を分析することで、書き込みが遅いクエリを調査できます。
