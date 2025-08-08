---
title: Identify Slow Queries
summary: 問題のある SQL ステートメントを識別するには、スロー クエリ ログを使用します。
---

# 遅いクエリを特定する {#identify-slow-queries}

ユーザーが遅いクエリを識別し、SQL 実行のパフォーマンスを分析および改善できるように、TiDB は実行時間が[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) (デフォルト値は 300 ミリ秒) ～ [遅いクエリファイル](/tidb-configuration-file.md#slow-query-file) (デフォルト値は「tidb-slow.log」) を超えるステートメントを出力します。

TiDBはデフォルトでスロークエリログを有効にします。この機能は、システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)変更することで有効または無効にできます。

## 使用例 {#usage-example}

```sql
# Time: 2019-08-14T09:26:59.487776265+08:00
# Txn_start_ts: 410450924122144769
# User@Host: root[root] @ localhost [127.0.0.1]
# Conn_ID: 3086
# Exec_retry_time: 5.1 Exec_retry_count: 3
# Query_time: 1.527627037
# Parse_time: 0.000054933
# Compile_time: 0.000129729
# Rewrite_time: 0.000000003 Preproc_subqueries: 2 Preproc_subqueries_time: 0.000000002
# Optimize_time: 0.00000001
# Wait_TS: 0.00001078
# Process_time: 0.07 Request_count: 1 Total_keys: 131073 Process_keys: 131072 Prewrite_time: 0.335415029 Commit_time: 0.032175429 Get_commit_ts_time: 0.000177098 Local_latch_wait_time: 0.106869448 Write_keys: 131072 Write_size: 3538944 Prewrite_region: 1
# DB: test
# Is_internal: false
# Digest: 50a2e32d2abbd6c1764b1b7f2058d428ef2712b029282b776beb9506a365c0f1
# Stats: t:pseudo
# Num_cop_tasks: 1
# Cop_proc_avg: 0.07 Cop_proc_p90: 0.07 Cop_proc_max: 0.07 Cop_proc_addr: 172.16.5.87:20171
# Cop_wait_avg: 0 Cop_wait_p90: 0 Cop_wait_max: 0 Cop_wait_addr: 172.16.5.87:20171
# Cop_backoff_regionMiss_total_times: 200 Cop_backoff_regionMiss_total_time: 0.2 Cop_backoff_regionMiss_max_time: 0.2 Cop_backoff_regionMiss_max_addr: 127.0.0.1 Cop_backoff_regionMiss_avg_time: 0.2 Cop_backoff_regionMiss_p90_time: 0.2
# Cop_backoff_rpcPD_total_times: 200 Cop_backoff_rpcPD_total_time: 0.2 Cop_backoff_rpcPD_max_time: 0.2 Cop_backoff_rpcPD_max_addr: 127.0.0.1 Cop_backoff_rpcPD_avg_time: 0.2 Cop_backoff_rpcPD_p90_time: 0.2
# Cop_backoff_rpcTiKV_total_times: 200 Cop_backoff_rpcTiKV_total_time: 0.2 Cop_backoff_rpcTiKV_max_time: 0.2 Cop_backoff_rpcTiKV_max_addr: 127.0.0.1 Cop_backoff_rpcTiKV_avg_time: 0.2 Cop_backoff_rpcTiKV_p90_time: 0.2
# Mem_max: 525211
# Disk_max: 65536
# Prepared: false
# Plan_from_cache: false
# Succ: true
# Plan: tidb_decode_plan('ZJAwCTMyXzcJMAkyMAlkYXRhOlRhYmxlU2Nhbl82CjEJMTBfNgkxAR0AdAEY1Dp0LCByYW5nZTpbLWluZiwraW5mXSwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCg==')
use test;
insert into t select * from t;
```

## フィールドの説明 {#fields-description}

> **注記：**
>
> スロー クエリ ログ内の次のすべての時間フィールドの単位は**「秒」**です。

スロークエリの基本:

-   `Time` : ログの印刷時刻。
-   `Query_time` : ステートメントの実行時間。
-   `Parse_time` : ステートメントの解析時間。
-   `Compile_time` : クエリ最適化の期間。
-   `Optimize_time` : 実行プランの最適化に費やされた時間。
-   `Wait_TS` : トランザクションのタイムスタンプを取得するためのステートメントの待機時間。
-   `Query` : SQL ステートメント。2 `Query`スロー ログに出力されませんが、スロー ログがメモリテーブルにマップされた後、対応するフィールドが`Query`呼ばれます。
-   `Digest` : SQL ステートメントのフィンガープリント。
-   `Txn_start_ts` : トランザクションの開始タイムスタンプと一意のID。この値を使用して、トランザクション関連のログを検索できます。
-   `Is_internal` : SQL 文が TiDB 内部であるかどうか。2 `true` SQL 文が TiDB 内部で実行されることを示し、 `false` SQL 文がユーザーによって実行されることを示します。
-   `Index_names` : ステートメントで使用されるインデックス名。
-   `Stats` : このクエリ中に使用される統計情報のヘルス状態、内部バージョン、合計行数、変更行数、およびロード状態。2 `pseudo` 、統計情報が正常でないことを示します。オプティマイザーが完全にロードされていない統計情報を使用しようとした場合、内部状態も出力されます。例えば、 `t1:439478225786634241[105000;5000][col1:allEvicted][idx1:allEvicted]`の意味は次のように理解できます。
    -   `t1` : クエリの最適化中にテーブル`t1`の統計が使用されます。
    -   `439478225786634241` : 内部バージョン。
    -   `105000` : 統計の合計行数。
    -   `5000` : 最後の統計収集以降に変更された行数。
    -   `col1:allEvicted` : 列`col1`の統計が完全にはロードされていません。
    -   `idx1:allEvicted` : インデックス`idx1`の統計が完全にロードされていません。
-   `Succ` : ステートメントが正常に実行されたかどうか。
-   `Backoff_time` : ステートメントで再試行を必要とするエラーが発生した場合の、再試行までの待機時間。一般的なエラーには、 `lock occurs` 、 `Region split` 、 `tikv server is busy`があります。
-   `Plan` : ステートメントの実行プラン。特定の実行プランを解析するには、 `SELECT tidb_decode_plan('xxx...')`ステートメントを実行します。
-   `Binary_plan` : バイナリエンコードされた文の実行計画。特定の実行計画を解析するには、 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)の文を実行します。4 `Plan`と`Binary_plan`フィールドには同じ情報が格納されます。ただし、2つのフィールドから解析される実行計画の形式は異なります。
-   `Prepared` : このステートメントが`Prepare`要求か`Execute`要求かを示します。
-   `Plan_from_cache` : このステートメントが実行プラン キャッシュにヒットするかどうか。
-   `Plan_from_binding` : このステートメントがバインドされた実行プランを使用するかどうか。
-   `Has_more_results` : このステートメントにユーザーが取得できる結果がさらにあるかどうか。
-   `Rewrite_time` : このステートメントのクエリの書き換えに要した時間。
-   `Preproc_subqueries` : ステートメント内の事前に実行されるサブクエリの数。例えば、 `where id in (select if from t)`サブクエリが事前に実行される可能性があります。
-   `Preproc_subqueries_time` : このステートメントのサブクエリを事前に実行するのに費やされた時間。
-   `Exec_retry_count` : このステートメントの再試行回数。このフィールドは通常、ロックが失敗した場合にステートメントが再試行される悲観的トランザクション用です。
-   `Exec_retry_time` : この文の実行再試行時間。例えば、文が合計3回実行された場合（最初の2回は失敗）、 `Exec_retry_time`最初の2回の実行の合計時間を意味します。最後の実行時間は`Query_time`から`Exec_retry_time`引いた値です。
-   `KV_total` : このステートメントによる TiKV またはTiFlash上のすべての RPC 要求に費やされた時間。
-   `PD_total` : このステートメントによって PD 上のすべての RPC 要求に費やされた時間。
-   `Backoff_total` : このステートメントの実行中にすべてのバックオフに費やされた時間。
-   `Write_sql_response_total` : このステートメントによって結果をクライアントに送り返すのに要した時間。
-   `Result_rows` : クエリ結果の行数。
-   `IsExplicitTxn` : この文が明示的なトランザクション内にあるかどうか。値が`false`の場合、トランザクションは`autocommit=1`であり、文は実行後に自動的にコミットされます。
-   `Warnings` : この文の実行中に生成されるJSON形式の警告。これらの警告は、 [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)文の出力と概ね一致しますが、より詳細な診断情報を提供する追加の警告が含まれる場合があります。これらの追加の警告は`IsExtra: true`としてマークされます。

次のフィールドはトランザクション実行に関連しています。

-   `Prewrite_time` : 2 フェーズ トランザクション コミットの最初のフェーズ (事前書き込み) の期間。
-   `Commit_time` : 2 フェーズ トランザクション コミットの 2 番目のフェーズ (コミット) の期間。
-   `Get_commit_ts_time` : 2 フェーズ トランザクション コミットの 2 番目のフェーズ (コミット) 中に`commit_ts`取得するのに費やされた時間。
-   `Local_latch_wait_time` : 2 フェーズ トランザクション コミットの 2 番目のフェーズ (コミット) の前に、TiDB がロックを待機するのにかかる時間。
-   `Write_keys` : トランザクションが TiKV 内の書き込み CF に書き込むキーの数。
-   `Write_size` : トランザクションがコミットされたときに書き込まれるキーまたは値の合計サイズ。
-   `Prewrite_region` ：2フェーズトランザクションコミットの最初のフェーズ（事前書き込み）に関与するTiKVリージョンの数。各リージョンはリモートプロシージャコールをトリガーします。
-   `Wait_prewrite_binlog_time` : トランザクションがコミットされた際にバイナリログを書き込むのにかかった時間。v8.4.0以降、TiDBBinlogは削除され、このフィールドには値が設定されません。
-   `Resolve_lock_time` : トランザクションのコミット中にロックが発生した後、ロックを解決するか期限が切れるまで待機する時間。

メモリ使用量フィールド:

-   `Mem_max` : SQL文の実行期間中に使用される最大メモリ空間(単位はバイト)。

ハードディスクのフィールド:

-   `Disk_max` : SQL 文の実行期間中に使用される最大ディスク容量 (単位はバイト)。

ユーザーフィールド:

-   `User` : このステートメントを実行するユーザーの名前。
-   `Host` : このステートメントのホスト名。
-   `Conn_ID` : 接続ID（セッションID）。例えば、キーワード`con:3`を使用すると、セッションIDが`3`ログを検索できます。
-   `DB` : 現在のデータベース。

TiKVコプロセッサータスク フィールド:

-   `Request_count` : ステートメントが送信するコプロセッサー要求の数。
-   `Total_keys` :コプロセッサーがスキャンしたキーの数。
-   `Process_time` : TiKVにおけるSQL文の合計処理時間。データはTiKVに同時に送信されるため、この値は`Query_time`超える場合があります。
-   `Wait_time` : TiKVにおけるステートメントの合計待機時間。TiKVのコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが動作している場合でも、リクエストがキューイングされる可能性があります。キュー内のリクエストの処理に時間がかかると、後続のリクエストの待機時間が増加します。
-   `Process_keys` :コプロセッサーが処理したキーの数。2 と比較すると、 `total_keys` `processed_keys`古いバージョンの MVCC は含まれません。6 と`processed_keys` `total_keys`差が大きいことから、古いバージョンが多数存在することがわかります。
-   `Num_cop_tasks` : このステートメントによって送信されたコプロセッサータスクの数。
-   `Cop_proc_avg` : RocksDB のミューテックスなど、カウントできない待機時間を含む、cop タスクの平均実行時間。
-   `Cop_proc_p90` : cop タスクの P90 実行時間。
-   `Cop_proc_max` : cop タスクの最大実行時間。
-   `Cop_proc_addr` : 実行時間が最も長い cop タスクのアドレス。
-   `Cop_wait_avg` : リクエストのキューイングとスナップショットの取得の時間を含む、cop タスクの平均待機時間。
-   `Cop_wait_p90` : copタスクのP90待機時間。
-   `Cop_wait_max` : cop タスクの最大待機時間。
-   `Cop_wait_addr` : 待機時間が最も長い cop-task のアドレス。
-   `Rocksdb_delete_skipped_count` : RocksDB がデータをスキャンするときに検出する削除された (tombstone) キーの数。
-   `Rocksdb_key_skipped_count` : RocksDB がデータをスキャンするときに検出するすべてのキーの数。
-   `Rocksdb_block_cache_hit_count` : RocksDB がブロックキャッシュからデータを読み取る回数。
-   `Rocksdb_block_read_count` : RocksDB がファイル システムからデータを読み取る回数。
-   `Rocksdb_block_read_byte` : RocksDB がファイル システムから読み取るデータの量。
-   `Rocksdb_block_read_time` : RocksDB がファイル システムからデータを読み取るのにかかる時間。
-   `Cop_backoff_{backoff-type}_total_times` : エラーによって発生したバックオフの合計回数。
-   `Cop_backoff_{backoff-type}_total_time` : エラーによって発生したバックオフの合計時間。
-   `Cop_backoff_{backoff-type}_max_time` : エラーによって発生したバックオフの最長時間。
-   `Cop_backoff_{backoff-type}_max_addr` : エラーによって発生したバックオフ時間が最も長い cop-task のアドレス。
-   `Cop_backoff_{backoff-type}_avg_time` : エラーによって発生したバックオフの平均時間。
-   `Cop_backoff_{backoff-type}_p90_time` : エラーによって発生した P90 パーセンタイル バックオフ時間。

`backoff-type`は、一般的に次のタイプが含まれます。

-   `tikvRPC` : RPC 要求を TiKV に送信できなかったために発生したバックオフ。
-   `tiflashRPC` : TiFlashへの RPC 要求の送信に失敗したために発生したバックオフ。
-   `pdRPC` : RPC 要求を PD に送信できなかったために発生したバックオフ。
-   `txnLock` : ロックの競合によって発生したバックオフ。
-   `regionMiss` : リージョンが分割または結合された後に TiDBリージョンキャッシュ情報が古くなると、その処理要求によって発生するバックオフは失敗します。
-   `regionScheduling` : リージョンがスケジュールされていてLeaderが選択されていない場合、TiDB がリクエストを処理できないために発生するバックオフ。
-   `tikvServerBusy` : TiKV 負荷が高すぎて新しいリクエストを処理できないために発生するバックオフ。
-   `tiflashServerBusy` : TiFlash の負荷が高すぎて新しい要求を処理できないために発生するバックオフ。
-   `tikvDiskFull` : TiKV ディスクがいっぱいであるために発生するバックオフ。
-   `txnLockFast` : データの読み取り中にロックが発生したために発生するバックオフ。

リソース制御に関連するフィールド:

-   `Resource_group` : ステートメントがバインドされているリソース グループ。
-   `Request_unit_read` : ステートメントによって消費された読み取り RU の合計。
-   `Request_unit_write` : ステートメントによって消費された書き込み RU の合計。
-   `Time_queued_by_rc` : ステートメントが利用可能なリソースを待機する合計時間。

## 関連するシステム変数 {#related-system-variables}

-   [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) : スローログの閾値を設定します。実行時間がこの閾値を超えたSQL文はスローログに記録されます。デフォルト値は300（ミリ秒）です。
-   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len) : スローログに記録されるSQL文の最大長を設定します。デフォルト値は4096（バイト）です。
-   [tidb_redact_log](/system-variables.md#tidb_redact_log) : スローログに記録されるSQL文で、 `?`使用してユーザーデータを非センシティブ化するかどうかを決定します。デフォルト値は`0`で、この機能は無効です。
-   [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) : 実行プランに各演算子の物理実行情報を記録するかどうかを指定します。デフォルト値は`1`です。この機能はパフォーマンスに約3%の影響を与えます。この機能を有効にすると、以下の`Plan`情報を表示できます。

    ```sql
    > select tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMgk1BWM2zwAAMRnIADcVyAAxHcEQNQlOL0EBBPBbCjMJMTNfMTYJMQkzMTI4MS44NTc4MTk5MDUyMTcJdGFibGU6dCwgaW5kZXg6aWR4KGEpLCByYW5nZTpbLWluZiw1MDAwMCksIGtlZXAgb3JkZXI6ZmFsc2UJMjUBrgnQVnsA');
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | tidb_decode_plan('jAOIMAk1XzE3CTAJMQlmdW5jczpjb3VudChDb2x1bW4jNyktPkMJC/BMNQkxCXRpbWU6MTAuOTMxNTA1bXMsIGxvb3BzOjIJMzcyIEJ5dGVzCU4vQQoxCTMyXzE4CTAJMQlpbmRleDpTdHJlYW1BZ2dfOQkxCXQRSAwyNzY4LkgALCwgcnBjIG51bTogMQkMEXMQODg0MzUFK0hwcm9jIGtleXM6MjUwMDcJMjA2HXsIMg |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    |     id                    task    estRows               operator info                                                  actRows    execution info                                                                  memory       disk                              |
    |     StreamAgg_17          root    1                     funcs:count(Column#7)->Column#5                                1          time:10.931505ms, loops:2                                                       372 Bytes    N/A                               |
    |     └─IndexReader_18      root    1                     index:StreamAgg_9                                              1          time:10.927685ms, loops:2, rpc num: 1, rpc time:10.884355ms, proc keys:25007    206 Bytes    N/A                               |
    |       └─StreamAgg_9       cop     1                     funcs:count(1)->Column#7                                       1          time:11ms, loops:25                                                             N/A          N/A                               |
    |         └─IndexScan_16    cop     31281.857819905217    table:t, index:idx(a), range:[-inf,50000), keep order:false    25007      time:11ms, loops:25                                                             N/A          N/A                               |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    ```

パフォーマンス テストを実施する場合は、オペレーターの実行情報を自動的に収集する機能を無効にすることができます。

```sql
set @@tidb_enable_collect_execution_info=0;
```

`Plan`フィールドに返される結果は、 `EXPLAIN`または`EXPLAIN ANALYZE`結果とほぼ同じ形式です。実行プランの詳細については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)参照してください。

詳細については[TiDB固有の変数と構文](/system-variables.md)参照してください。

## スローログのメモリマッピング {#memory-mapping-in-slow-log}

スロークエリログの内容は、 `INFORMATION_SCHEMA.SLOW_QUERY`テーブルをクエリすることで照会できます。テーブル内の各列名は、スローログ内の1つのフィールド名に対応しています。テーブル構造については、 [情報スキーマ](/information-schema/information-schema-slow-query.md)の`SLOW_QUERY`テーブルの概要を参照してください。

> **注記：**
>
> `SLOW_QUERY`テーブルをクエリするたびに、TiDB は現在のスロー クエリ ログを読み取って解析します。

TiDB 4.0では、 `SLOW_QUERY`ローテーションされたスローログファイルを含む任意の期間のスローログのクエリをサポートします。解析が必要なスローログファイルを特定するには、 `TIME`範囲を指定する必要があります。5 `TIME`範囲を指定しない場合、TiDBは現在のスローログファイルのみを解析します。例：

-   時間範囲を指定しない場合、TiDB はスロー ログ ファイルに書き込むスロー クエリ データのみを解析します。

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query;
    ```

        +----------+----------------------------+----------------------------+
        | count(*) | min(time)                  | max(time)                  |
        +----------+----------------------------+----------------------------+
        | 122492   | 2020-03-11 23:35:20.908574 | 2020-03-25 19:16:38.229035 |
        +----------+----------------------------+----------------------------+

-   たとえば、 `2020-03-10 00:00:00`から`2020-03-11 00:00:00`まで時間範囲を指定すると、TiDB は最初に指定された時間範囲のスロー ログ ファイルを見つけて、次にスロー クエリ情報を解析します。

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query
    where time > '2020-03-10 00:00:00'
      and time < '2020-03-11 00:00:00';
    ```

        +----------+----------------------------+----------------------------+
        | count(*) | min(time)                  | max(time)                  |
        +----------+----------------------------+----------------------------+
        | 2618049  | 2020-03-10 00:00:00.427138 | 2020-03-10 23:00:22.716728 |
        +----------+----------------------------+----------------------------+

> **注記：**
>
> 指定された時間範囲のスロー ログ ファイルが削除された場合、またはスロー クエリがない場合、クエリは NULL を返します。

TiDB 4.0では、すべてのTiDBノードのスロークエリ情報を照会するためのシステムテーブル[`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table)が追加されました。テーブル`CLUSTER_SLOW_QUERY`のスキーマは、テーブル`SLOW_QUERY`とは異なり、列`CLUSTER_SLOW_QUERY`に列`INSTANCE`が追加されています。列`INSTANCE`は、スロークエリの行情報のTiDBノードアドレスを表します。列`CLUSTER_SLOW_QUERY` 、 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)と同じように使用できます。

`CLUSTER_SLOW_QUERY`テーブルをクエリする場合、TiDB は、他のノードからすべての低速クエリ情報を取得して 1 つの TiDB ノードで操作を実行するのではなく、計算と判断を他のノードにプッシュします。

## <code>SLOW_QUERY</code> / <code>CLUSTER_SLOW_QUERY</code>の使用例 {#code-slow-query-code-code-cluster-slow-query-code-usage-examples}

### トップNの遅いクエリ {#top-n-slow-queries}

ユーザーの遅いクエリの上位 2 つをクエリします。1 `Is_internal=false` 、TiDB 内の遅いクエリを除外し、ユーザーの遅いクエリのみをクエリすることを意味します。

```sql
select query_time, query
from information_schema.slow_query
where is_internal = false
order by query_time desc
limit 2;
```

出力例:

    +--------------+------------------------------------------------------------------+
    | query_time   | query                                                            |
    +--------------+------------------------------------------------------------------+
    | 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
    |  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
    +--------------+------------------------------------------------------------------+

### <code>test</code>ユーザーの上位Nの遅いクエリを照会する {#query-the-top-n-slow-queries-of-the-code-test-code-user}

次の例では、 `test`ユーザーによって実行された遅いクエリが照会され、最初の 2 つの結果が実行時間の逆順に表示されます。

```sql
select query_time, query, user
from information_schema.slow_query
where is_internal = false
  and user = "test"
order by query_time desc
limit 2;
```

出力例:

    +-------------+------------------------------------------------------------------+----------------+
    | Query_time  | query                                                            | user           |
    +-------------+------------------------------------------------------------------+----------------+
    | 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test           |
    +-------------+------------------------------------------------------------------+----------------+

### 同じSQLフィンガープリントを持つ同様の低速クエリをクエリする {#query-similar-slow-queries-with-the-same-sql-fingerprints}

Top-N SQL ステートメントをクエリした後、同じフィンガープリントを使用して同様の低速クエリをクエリし続けます。

1.  上位 N 個の遅いクエリと対応する SQL フィンガープリントを取得します。

    ```sql
    select query_time, query, digest
    from information_schema.slow_query
    where is_internal = false
    order by query_time desc
    limit 1;
    ```

    出力例:

        +-------------+-----------------------------+------------------------------------------------------------------+
        | query_time  | query                       | digest                                                           |
        +-------------+-----------------------------+------------------------------------------------------------------+
        | 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
        +-------------+-----------------------------+------------------------------------------------------------------+

2.  指紋を使用して同様の遅いクエリをクエリします。

    ```sql
    select query, query_time
    from information_schema.slow_query
    where digest = "4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
    ```

    出力例:

        +-----------------------------+-------------+
        | query                       | query_time  |
        +-----------------------------+-------------+
        | select * from t1 where a=1; | 0.302558006 |
        | select * from t1 where a=2; | 0.401313532 |
        +-----------------------------+-------------+

## 疑似<code>stats</code>で遅いクエリをクエリする {#query-slow-queries-with-pseudo-code-stats-code}

```sql
select query, query_time, stats
from information_schema.slow_query
where is_internal = false
  and stats like '%pseudo%';
```

出力例:

    +-----------------------------+-------------+---------------------------------+
    | query                       | query_time  | stats                           |
    +-----------------------------+-------------+---------------------------------+
    | select * from t1 where a=1; | 0.302558006 | t1:pseudo                       |
    | select * from t1 where a=2; | 0.401313532 | t1:pseudo                       |
    | select * from t1 where a>2; | 0.602011247 | t1:pseudo                       |
    | select * from t1 where a>3; | 0.50077719  | t1:pseudo                       |
    | select * from t1 join t2;   | 0.931260518 | t1:407872303825682445,t2:pseudo |
    +-----------------------------+-------------+---------------------------------+

### 実行プランが変更された遅いクエリをクエリする {#query-slow-queries-whose-execution-plan-is-changed}

同じカテゴリのSQL文の実行プランが変更されると、統計情報が古くなっているか、統計情報が実際のデータ分布を反映するほど正確でないため、実行速度が低下します。次のSQL文を使用して、異なる実行プランを持つSQL文を照会できます。

```sql
select count(distinct plan_digest) as count,
       digest,
       min(query)
from cluster_slow_query
group by digest
having count > 1
limit 3\G
```

出力例:

    ***************************[ 1. row ]***************************
    count      | 2
    digest     | 17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94
    min(query) | SELECT DISTINCT c FROM sbtest25 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (291638, 291737)];
    ***************************[ 2. row ]***************************
    count      | 2
    digest     | 9337865f3e2ee71c1c2e740e773b6dd85f23ad00f8fa1f11a795e62e15fc9b23
    min(query) | SELECT DISTINCT c FROM sbtest22 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (215420, 215519)];
    ***************************[ 3. row ]***************************
    count      | 2
    digest     | db705c89ca2dfc1d39d10e0f30f285cbbadec7e24da4f15af461b148d8ffb020
    min(query) | SELECT DISTINCT c FROM sbtest11 WHERE id BETWEEN ? AND ? ORDER BY c [arguments: (303359, 303458)];

次に、上記のクエリ結果の SQL フィンガープリントを使用して、さまざまなプランをクエリできます。

```sql
select min(plan),
       plan_digest
from cluster_slow_query
where digest='17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94'
group by plan_digest\G
```

出力例:

    *************************** 1. row ***************************
      min(plan):    Sort_6                  root    100.00131380758702      sbtest.sbtest25.c:asc
            └─HashAgg_10            root    100.00131380758702      group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
              └─TableReader_15      root    100.00131380758702      data:TableRangeScan_14
                └─TableScan_14      cop     100.00131380758702      table:sbtest25, range:[502791,502890], keep order:false
    plan_digest: 6afbbd21f60ca6c6fdf3d3cd94f7c7a49dd93c00fcf8774646da492e50e204ee
    *************************** 2. row ***************************
      min(plan):    Sort_6                  root    1                       sbtest.sbtest25.c:asc
            └─HashAgg_12            root    1                       group by:sbtest.sbtest25.c, funcs:firstrow(sbtest.sbtest25.c)->sbtest.sbtest25.c
              └─TableReader_13      root    1                       data:HashAgg_8
                └─HashAgg_8         cop     1                       group by:sbtest.sbtest25.c,
                  └─TableScan_11    cop     1.2440069558121831      table:sbtest25, range:[472745,472844], keep order:false

### クラスター内の各 TiDB ノードの遅いクエリの数を照会する {#query-the-number-of-slow-queries-for-each-tidb-node-in-a-cluster}

```sql
select instance, count(*) from information_schema.cluster_slow_query where time >= "2020-03-06 00:00:00" and time < now() group by instance;
```

出力例:

    +---------------+----------+
    | instance      | count(*) |
    +---------------+----------+
    | 0.0.0.0:10081 | 124      |
    | 0.0.0.0:10080 | 119771   |
    +---------------+----------+

### 異常な時間帯にのみ発生するクエリスローログ {#query-slow-logs-occurring-only-in-abnormal-time-period}

`2020-03-10 13:24:00`から`2020-03-10 13:27:00`期間にQPSの低下やレイテンシーの増加などの問題が見られる場合、大規模なクエリの発生が原因の可能性があります。次のSQL文を実行して、異常な期間にのみ発生するスローログを検索してください。5から`2020-03-10 13:20:00` `2020-03-10 13:23:00`期間は通常の期間を指します。

```sql
SELECT * FROM
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ count(*),
         min(time),
         sum(query_time) AS sum_query_time,
         sum(Process_time) AS sum_process_time,
         sum(Wait_time) AS sum_wait_time,
         sum(Commit_time),
         sum(Request_count),
         sum(process_keys),
         sum(Write_keys),
         max(Cop_proc_max),
         min(query),min(prev_stmt),
         digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:24:00'
            AND time < '2020-03-10 13:27:00'
            AND Is_internal = false
    GROUP BY  digest) AS t1
WHERE t1.digest NOT IN
    (SELECT /*+ AGG_TO_COP(), HASH_AGG() */ digest
    FROM information_schema.CLUSTER_SLOW_QUERY
    WHERE time >= '2020-03-10 13:20:00'
            AND time < '2020-03-10 13:23:00'
    GROUP BY  digest)
ORDER BY  t1.sum_query_time DESC limit 10\G
```

出力例:

    ***************************[ 1. row ]***************************
    count(*)           | 200
    min(time)          | 2020-03-10 13:24:27.216186
    sum_query_time     | 50.114126194
    sum_process_time   | 268.351
    sum_wait_time      | 8.476
    sum(Commit_time)   | 1.044304306
    sum(Request_count) | 6077
    sum(process_keys)  | 202871950
    sum(Write_keys)    | 319500
    max(Cop_proc_max)  | 0.263
    min(query)         | delete from test.tcs2 limit 5000;
    min(prev_stmt)     |
    digest             | 24bd6d8a9b238086c9b8c3d240ad4ef32f79ce94cf5a468c0b8fe1eb5f8d03df

### 他の TiDB スローログファイルを解析する {#parse-other-tidb-slow-log-files}

TiDBは、セッション変数`tidb_slow_query_file`使用して、クエリ`INFORMATION_SCHEMA.SLOW_QUERY`実行する際に読み取りおよび解析するファイルを制御します。セッション変数の値を変更することで、他のスロークエリログファイルの内容をクエリできます。

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

### <code>pt-query-digest</code>で TiDB のスローログを解析する {#parse-tidb-slow-logs-with-code-pt-query-digest-code}

TiDB スロー ログを解析するには`pt-query-digest`使用します。

> **注記：**
>
> `pt-query-digest` 3.0.13 以降のバージョンを使用することをお勧めします。

例えば：

```shell
pt-query-digest --report tidb-slow.log
```

出力例:

    # 320ms user time, 20ms system time, 27.00M rss, 221.32M vsz
    # Current date: Mon Mar 18 13:18:51 2019
    # Hostname: localhost.localdomain
    # Files: tidb-slow.log
    # Overall: 1.02k total, 21 unique, 0 QPS, 0x concurrency _________________
    # Time range: 2019-03-18-12:22:16 to 2019-03-18-13:08:52
    # Attribute          total     min     max     avg     95%  stddev  median
    # ============     ======= ======= ======= ======= ======= ======= =======
    # Exec time           218s    10ms     13s   213ms    30ms      1s    19ms
    # Query size       175.37k       9   2.01k  175.89  158.58  122.36  158.58
    # Commit time         46ms     2ms     7ms     3ms     7ms     1ms     3ms
    # Conn ID               71       1      16    8.88   15.25    4.06    9.83
    # Process keys     581.87k       2 103.15k  596.43  400.73   3.91k  400.73
    # Process time         31s     1ms     10s    32ms    19ms   334ms    16ms
    # Request coun       1.97k       1      10    2.02    1.96    0.33    1.96
    # Total keys       636.43k       2 103.16k  652.35  793.42   3.97k  400.73
    # Txn start ts     374.38E       0  16.00E 375.48P   1.25P  89.05T   1.25P
    # Wait time          943ms     1ms    19ms     1ms     2ms     1ms   972us
    .
    .
    .

## 問題のあるSQL文を特定する {#identify-problematic-sql-statements}

`SLOW_QUERY`のすべてが問題となるわけではありません。3 `process_time`非常に大きいものだけが、クラスター全体への負荷を高めます。

`wait_time`が非常に大きく、 `process_time`が非常に小さいステートメントは、通常は問題になりません。これは、実際に問題のあるステートメントによってブロックされ、実行キューで待機する必要があるため、応答時間が大幅に長くなるためです。

### <code>ADMIN SHOW SLOW</code>コマンド {#code-admin-show-slow-code-command}

TiDB ログ ファイルに加えて、 `ADMIN SHOW SLOW`コマンドを実行して遅いクエリを特定できます。

```sql
ADMIN SHOW SLOW recent N
ADMIN SHOW SLOW TOP [internal | all] N
```

`recent N`最近の N 個の低速クエリ レコードを表示します。例:

```sql
ADMIN SHOW SLOW recent 10
```

`top N` 、最近（数日以内）の最も遅い N 件のクエリレコードを表示します。2 `internal`を指定した場合、返される結果はシステムによって実行された内部 SQL になります。4 オプション`all`指定した場合、返される結果はユーザーの SQL と内部 SQL を組み合わせたものになります。それ以外の場合、このコマンドはユーザーの SQL から取得した遅いクエリレコードのみを返します。

```sql
ADMIN SHOW SLOW top 3
ADMIN SHOW SLOW top internal 3
ADMIN SHOW SLOW top all 5
```

TiDBはメモリメモリが限られているため、低速クエリのレコードを限られた数だけしか保存しません。 `N`コマンドの値がレコード数よりも大きい場合、返されるレコード数は`N`未満になります。

次の表に出力の詳細を示します。

| カラム名       | 説明                                             |
| :--------- | :--------------------------------------------- |
| 始める        | SQL実行の開始時刻                                     |
| 間隔         | SQL実行の期間                                       |
| 詳細         | SQL実行の詳細                                       |
| 成功         | SQL ステートメントが正常に実行されたかどうか。1 `1`成功、 `0`失敗を意味します。 |
| 接続ID       | セッションの接続ID                                     |
| トランザクションts | 取引の`start ts`                                  |
| ユーザー       | ステートメントを実行するユーザー名                              |
| デシベル       | ステートメント実行時に関係するデータベース                          |
| テーブルID     | SQL文の実行時に関係するテーブルのID                           |
| インデックスID   | SQL文の実行時に関係するインデックスのID                         |
| 内部         | これはTiDBの内部SQL文です                               |
| ダイジェスト     | SQL文の指紋                                        |
| SQL        | 実行中または実行されたSQL文                                |
