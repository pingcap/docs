---
title: Identify Slow Queries
summary: 遅いクエリを特定し、SQL実行のパフォーマンスを分析して改善できるために、TiDBは実行時間が300ミリ秒を超えるステートメントを出力します。デフォルトで低速クエリログを有効にし、システム変数を変更することで機能を制御できます。遅いクエリの基本情報には、ログの出力時刻、ステートメントの実行時間、解析時間、クエリ最適化の期間などが含まれます。また、トランザクションの実行に関連する情報も提供されます。TiDBは`ADMIN SHOW SLOW`コマンドを使用して遅いクエリを特定できます。
---

# 遅いクエリを特定する {#identify-slow-queries}

ユーザーが遅いクエリを特定し、SQL 実行のパフォーマンスを分析して改善できるようにするために、TiDB は実行時間が[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) (デフォルト値は 300 ミリ秒) から[スロークエリファイル](/tidb-configuration-file.md#slow-query-file) (デフォルト値は「tidb-slow.log」) を超えるステートメントを出力します。

TiDB はデフォルトで低速クエリ ログを有効にします。システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)を変更することで、この機能を有効または無効にできます。

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
> スロークエリログ内の以下のすべての時間フィールドの単位は**「秒」**です。

遅いクエリの基本:

-   `Time` : ログの出力時刻。
-   `Query_time` : ステートメントの実行時間。
-   `Parse_time` : ステートメントの解析時間。
-   `Compile_time` : クエリ最適化の期間。
-   `Optimize_time` : 実行計画の最適化にかかる時間。
-   `Wait_TS` : トランザクションのタイムスタンプを取得するためのステートメントの待ち時間。
-   `Query` : SQL ステートメント。 `Query`はスロー ログには出力されませんが、スロー ログがメモリテーブルにマップされた後、対応するフィールドは`Query`と呼ばれます。
-   `Digest` : SQL ステートメントのフィンガープリント。
-   `Txn_start_ts` : トランザクションの開始タイムスタンプと一意の ID。この値を使用して、トランザクション関連のログを検索できます。
-   `Is_internal` : SQL ステートメントが TiDB 内部であるかどうか。 `true` SQL ステートメントが TiDB の内部で実行されることを示し、 `false`は SQL ステートメントがユーザーによって実行されることを示します。
-   `Index_names` : ステートメントで使用されるインデックス名。
-   `Stats` : このクエリ中に使用される統計のヘルス状態、内部バージョン、合計行数、変更された行数、およびロード状態。 `pseudo` 、統計情報が異常であることを示します。オプティマイザが完全にロードされていない統計を使用しようとすると、内部状態も出力されます。たとえば、 `t1:439478225786634241[105000;5000][col1:allEvicted][idx1:allEvicted]`の意味は次のように理解できます。
    -   `t1` : テーブル`t1`の統計はクエリの最適化中に使用されます。
    -   `439478225786634241` : 内部バージョン。
    -   `105000` : 統計の合計行数。
    -   `5000` : 最後の統計収集以降に変更された行の数。
    -   `col1:allEvicted` : 列`col1`の統計は完全にはロードされていません。
    -   `idx1:allEvicted` : インデックス`idx1`の統計は完全にはロードされていません。
-   `Succ` : ステートメントが正常に実行されたかどうか。
-   `Backoff_time` : ステートメントで再試行が必要なエラーが発生した場合の、再試行までの待ち時間。一般的なエラーには、 `lock occurs` 、 `Region split` 、および`tikv server is busy`が含まれます。
-   `Plan` : ステートメントの実行計画。 `SELECT tidb_decode_plan('xxx...')`ステートメントを実行して、特定の実行プランを解析します。
-   `Binary_plan` : バイナリエンコードされたステートメントの実行計画。 `SELECT tidb_decode_binary_plan('xxx...')`ステートメントを実行して、特定の実行プランを解析します。 `Plan`フィールドと`Binary_plan`フィールドには同じ情報が含まれます。ただし、2 つのフィールドから解析された実行プランの形式は異なります。
-   `Prepared` : このステートメントが`Prepare`または`Execute`リクエストであるかどうか。
-   `Plan_from_cache` : このステートメントが実行プラン キャッシュにヒットするかどうか。
-   `Plan_from_binding` : このステートメントがバインドされた実行プランを使用するかどうか。
-   `Has_more_results` : このステートメントにユーザーが取得する結果がさらにあるかどうか。
-   `Rewrite_time` : このステートメントのクエリを書き換えるのに費やした時間。
-   `Preproc_subqueries` : 事前に実行される (ステートメント内の) サブクエリの数。たとえば、 `where id in (select if from t)`サブクエリは事前に実行される可能性があります。
-   `Preproc_subqueries_time` : この文のサブクエリを事前に実行するために費やした時間。
-   `Exec_retry_count` : このステートメントの再試行回数。このフィールドは通常、ロックが失敗したときにステートメントが再試行される悲観的トランザクション用です。
-   `Exec_retry_time` : このステートメントの実行再試行期間。たとえば、ステートメントが合計 3 回実行された (最初の 2 回は失敗した) 場合、 `Exec_retry_time`最初の 2 回の実行の合計時間を意味します。最後の実行の期間は`Query_time`マイナス`Exec_retry_time`です。
-   `KV_total` : このステートメントによって TiKV またはTiFlash上のすべての RPC リクエストに費やされた時間。
-   `PD_total` : このステートメントによって PD 上のすべての RPC リクエストに費やされた時間。
-   `Backoff_total` : このステートメントの実行中にすべてのバックオフに費やされた時間。
-   `Write_sql_response_total` : このステートメントによって結果をクライアントに送信するために費やされた時間。
-   `Result_rows` : クエリ結果の行数。
-   `IsExplicitTxn` : このステートメントが明示的なトランザクション内にあるかどうか。値が`false`の場合、トランザクションは`autocommit=1`であり、ステートメントは実行後に自動的にコミットされます。
-   `Warnings` : このステートメントの実行中に生成される JSON 形式の警告。これらの警告は通常、 [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)ステートメントの出力と一致しますが、より多くの診断情報を提供する追加の警告が含まれる場合があります。これらの追加の警告は`IsExtra: true`としてマークされます。

次のフィールドはトランザクションの実行に関連します。

-   `Prewrite_time` : 2 フェーズ トランザクション コミットの最初のフェーズ (事前書き込み) の期間。
-   `Commit_time` : 2 フェーズ トランザクション コミットの第 2 フェーズ (コミット) の期間。
-   `Get_commit_ts_time` : 2 フェーズ トランザクション コミットの第 2 フェーズ (コミット) で`commit_ts`取得するのに費やした時間。
-   `Local_latch_wait_time` : 2 フェーズ トランザクション コミットの第 2 フェーズ (コミット) の前に、TiDB がロックの待機に費やす時間。
-   `Write_keys` : トランザクションが TiKV の Write CF に書き込むキーの数。
-   `Write_size` : トランザクションのコミット時に書き込まれるキーまたは値の合計サイズ。
-   `Prewrite_region` : 2 フェーズ トランザクション コミットの最初のフェーズ (事前書き込み) に関与する TiKV リージョンの数。各リージョンはリモート プロシージャ コールをトリガーします。
-   `Wait_prewrite_binlog_time` : トランザクションがコミットされたときにバイナリログを書き込むのに使用される時間。
-   `Resolve_lock_time` : トランザクションのコミット中にロックが発生した後、解決するか、ロックが期限切れになるまで待機する時間。

メモリ使用量フィールド:

-   `Mem_max` : SQL文の実行中に使用される最大メモリ空間(単位はバイト)。

ハードディスクのフィールド:

-   `Disk_max` : SQL文の実行中に使用される最大ディスク容量(単位はバイト)。

ユーザーフィールド:

-   `User` : このステートメントを実行するユーザーの名前。
-   `Host` : このステートメントのホスト名。
-   `Conn_ID` : 接続 ID (セッション ID)。たとえば、キーワード`con:3`使用して、セッション ID が`3`のログを検索できます。
-   `DB` : 現在のデータベース。

TiKVコプロセッサータスク フィールド:

-   `Request_count` : ステートメントが送信するコプロセッサー要求の数。
-   `Total_keys` :コプロセッサーがスキャンしたキーの数。
-   `Process_time` : TiKV での SQL ステートメントの合計処理時間。データは TiKV に同時に送信されるため、この値は`Query_time`を超える可能性があります。
-   `Wait_time` : TiKV のステートメントの合計待機時間。 TiKV のコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが動作しているときにリクエストがキューに入る可能性があります。キュー内のリクエストの処理に時間がかかると、後続のリクエストの待ち時間が長くなります。
-   `Process_keys` :コプロセッサーが処理したキーの数。 `total_keys`と比較して、 `processed_keys`は古いバージョンの MVCC が含まれていません。 `processed_keys`と`total_keys`の大きな違いは、古いバージョンが多数存在することを示しています。
-   `Num_cop_tasks` : このステートメントによって送信されたコプロセッサータスクの数。
-   `Cop_proc_avg` : RocksDB のミューテックスなど、カウントできない待機時間を含む、cop タスクの平均実行時間。
-   `Cop_proc_p90` : cop タスクの P90 実行時間。
-   `Cop_proc_max` : cop タスクの最大実行時間。
-   `Cop_proc_addr` : 実行時間が最も長いcopタスクのアドレス。
-   `Cop_wait_avg` : リクエストのキューイングとスナップショットの取得の時間を含む、cop タスクの平均待機時間。
-   `Cop_wait_p90` : 警官タスクの P90 待機時間。
-   `Cop_wait_max` : cop タスクの最大待機時間。
-   `Cop_wait_addr` : 待機時間が最も長いcopタスクのアドレス。
-   `Rocksdb_delete_skipped_count` : RocksDB 読み取り中の削除されたキーのスキャン数。
-   `Rocksdb_key_skipped_count` : データのスキャン時に RocksDB が検出した削除された (廃棄された) キーの数。
-   `Rocksdb_block_cache_hit_count` : RocksDB がブロックキャッシュからデータを読み取る回数。
-   `Rocksdb_block_read_count` : RocksDB がファイル システムからデータを読み取る回数。
-   `Rocksdb_block_read_byte` : RocksDB がファイル システムから読み取るデータの量。
-   `Rocksdb_block_read_time` : RocksDB がファイル システムからデータを読み取るのにかかる時間。
-   `Cop_backoff_{backoff-type}_total_times` : エラーによるバックオフの合計回数。
-   `Cop_backoff_{backoff-type}_total_time` : エラーによるバックオフの合計時間。
-   `Cop_backoff_{backoff-type}_max_time` : エラーによるバックオフの最長時間。
-   `Cop_backoff_{backoff-type}_max_addr` : エラーによるバックオフ時間が最も長いcopタスクのアドレス。
-   `Cop_backoff_{backoff-type}_avg_time` : エラーによるバックオフの平均時間。
-   `Cop_backoff_{backoff-type}_p90_time` : エラーによって発生した P90 パーセンタイル バックオフ時間。

`backoff-type`は通常、次のタイプが含まれます。

-   `tikvRPC` : TiKV への RPC リクエストの送信失敗によって発生するバックオフ。
-   `tiflashRPC` : TiFlashへの RPC リクエストの送信に失敗したことによって発生するバックオフ。
-   `pdRPC` : RPC リクエストを PD に送信できなかったことによって発生するバックオフ。
-   `txnLock` : ロックの競合によって発生するバックオフ。
-   `regionMiss` : リージョンの分割またはマージ後に TiDBリージョンキャッシュ情報が古くなると、リクエストの処理によって引き起こされるバックオフは失敗します。
-   `regionScheduling` : リージョンがスケジュールされており、Leaderが選択されていない場合、TiDB によって発生するバックオフはリクエストを処理できません。
-   `tikvServerBusy` : TiKV 負荷が高すぎて新しいリクエストを処理できないことによって引き起こされるバックオフ。
-   `tiflashServerBusy` : TiFlash の負荷が高すぎて新しいリクエストを処理できないことによって発生するバックオフ。
-   `tikvDiskFull` : TiKV ディスクがいっぱいであることによって発生するバックオフ。
-   `txnLockFast` : データ読み取り中にロックによって発生するバックオフが発生します。

リソース制御に関連するフィールド:

-   `Resource_group` : ステートメントがバインドされているリソース グループ。
-   `Request_unit_read` : ステートメントによって消費される読み取り RU の合計。
-   `Request_unit_write` : ステートメントによって消費される合計書き込み RU。
-   `Time_queued_by_rc` : ステートメントが使用可能なリソースを待機する合計時間。

## 関連するシステム変数 {#related-system-variables}

-   [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) : スローログのしきい値を設定します。実行時間がこのしきい値を超えたSQL文はスローログに記録されます。デフォルト値は 300 (ミリ秒) です。
-   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len) : スローログに記録されるSQL文の最大長を設定します。デフォルト値は 4096 (バイト) です。
-   [tidb_redact_log](/system-variables.md#tidb_redact_log) : スローログに記録される SQL ステートメント`?`を使用してユーザーデータを非感作するかどうかを決定します。デフォルト値は`0`で、これは機能を無効にすることを意味します。
-   [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) : 各オペレーターの物理的な実行情報を実行計画に記録するかどうかを決定します。デフォルト値は`1`です。この機能はパフォーマンスに約 3% 影響します。この機能を有効にすると、次のように`Plan`情報を表示できます。

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

パフォーマンス テストを実施している場合は、オペレーターの実行情報を自動的に収集する機能を無効にすることができます。

```sql
set @@tidb_enable_collect_execution_info=0;
```

`Plan`フィールドの返される結果の形式は、 `EXPLAIN`または`EXPLAIN ANALYZE`の形式とほぼ同じです。実行計画の詳細については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を参照してください。

詳細については、 [TiDB 固有の変数と構文](/system-variables.md)を参照してください。

## 遅いログのメモリマッピング {#memory-mapping-in-slow-log}

`INFORMATION_SCHEMA.SLOW_QUERY`テーブルをクエリすることで、スロー クエリ ログの内容をクエリできます。テーブル内の各列名は、スロー ログ内の 1 つのフィールド名に対応します。テーブルの構造については、 [情報スキーマ](/information-schema/information-schema-slow-query.md)の`SLOW_QUERY`テーブルの概要を参照してください。

> **注記：**
>
> `SLOW_QUERY`テーブルをクエリするたびに、TiDB は現在のスロー クエリ ログを読み取って解析します。

TiDB 4.0 の場合、 `SLOW_QUERY` 、ローテーションされたスロー ログ ファイルを含む、任意の期間のスロー ログのクエリをサポートします。解析する必要がある低速ログ ファイルを見つけるには、 `TIME`の範囲を指定する必要があります。 `TIME`範囲を指定しない場合、TiDB は現在の低速ログ ファイルのみを解析します。例えば：

-   時間範囲を指定しない場合、TiDB は TiDB がスロー ログ ファイルに書き込んでいるスロー クエリ データのみを解析します。

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

-   たとえば、 `2020-03-10 00:00:00`から`2020-03-11 00:00:00`までの時間範囲を指定すると、TiDB はまず指定された時間範囲のスロー ログ ファイルを見つけてから、スロー クエリ情報を解析します。

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
> 指定した時間範囲のスロー ログ ファイルが削除されている場合、またはスロー クエリがない場合、クエリは NULL を返します。

TiDB 4.0 では、すべての TiDB ノードのスロー クエリ情報をクエリするための[`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table)システム テーブルが追加されています。 `CLUSTER_SLOW_QUERY`テーブルのテーブル スキーマは、 `CLUSTER_SLOW_QUERY`に`INSTANCE`列が追加されるという点で`SLOW_QUERY`テーブルのテーブル スキーマとは異なります。 `INSTANCE`列は、スロー クエリの行情報の TiDB ノード アドレスを表します。 `CLUSTER_SLOW_QUERY` [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)と同じように使用できます。

`CLUSTER_SLOW_QUERY`テーブルにクエリを実行すると、TiDB は他のノードからすべての低速クエリ情報を取得して 1 つの TiDB ノードで操作を実行するのではなく、計算と判断を他のノードにプッシュします。

## <code>SLOW_QUERY</code> / <code>CLUSTER_SLOW_QUERY</code>の使用例 {#code-slow-query-code-code-cluster-slow-query-code-usage-examples}

### トップ N の遅いクエリ {#top-n-slow-queries}

ユーザーの上位 2 つの遅いクエリをクエリします。 `Is_internal=false` TiDB 内の低速クエリを除外し、ユーザーの低速クエリのみをクエリすることを意味します。

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

### <code>test</code>ユーザーの上位 N の低速クエリをクエリします。 {#query-the-top-n-slow-queries-of-the-code-test-code-user}

次の例では、 `test`人のユーザーによって実行されたスロー クエリがクエリされ、最初の 2 つの結果が実行時間の逆順に表示されます。

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

### 同じ SQL フィンガープリントを使用して、同様の遅いクエリをクエリします。 {#query-similar-slow-queries-with-the-same-sql-fingerprints}

上位 N SQL ステートメントをクエリした後、同じフィンガープリントを使用して同様の低速クエリをクエリし続けます。

1.  トップ N の遅いクエリと対応する SQL フィンガープリントを取得します。

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

2.  フィンガープリントを使用して、同様の遅いクエリを実行します。

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

## 疑似<code>stats</code>を使用して遅いクエリをクエリする {#query-slow-queries-with-pseudo-code-stats-code}

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

### 実行計画が変更された低速クエリのクエリ {#query-slow-queries-whose-execution-plan-is-changed}

同じカテゴリの SQL ステートメントの実行計画が変更されると、統計が古いか、統計が実際のデータ分布を反映できるほど正確ではないため、実行が遅くなります。次の SQL ステートメントを使用して、さまざまな実行プランで SQL ステートメントをクエリできます。

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

### クラスター内の各 TiDB ノードの低速クエリの数を照会します。 {#query-the-number-of-slow-queries-for-each-tidb-node-in-a-cluster}

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

### 異常な時間帯にのみ発生する遅いログをクエリする {#query-slow-logs-occurring-only-in-abnormal-time-period}

`2020-03-10 13:24:00`から`2020-03-10 13:27:00`までの期間で QPS の低下やレイテンシーの増加などの問題が見つかった場合、その理由は大規模なクエリが発生した可能性があります。次の SQL ステートメントを実行して、異常な期間にのみ発生する遅いログをクエリします。 `2020-03-10 13:20:00`から`2020-03-10 13:23:00`までの時間帯は通常の時間帯を指します。

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

### 他の TiDB 低速ログ ファイルを解析する {#parse-other-tidb-slow-log-files}

TiDB はセッション変数`tidb_slow_query_file`を使用して、クエリ時に読み取られ解析されるファイルを制御します`INFORMATION_SCHEMA.SLOW_QUERY` 。セッション変数の値を変更することで、他のスロー クエリ ログ ファイルの内容をクエリできます。

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

### <code>pt-query-digest</code>を使用して TiDB の遅いログを解析する {#parse-tidb-slow-logs-with-code-pt-query-digest-code}

TiDB の遅いログを解析するには`pt-query-digest`を使用します。

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

## 問題のある SQL ステートメントを特定する {#identify-problematic-sql-statements}

`SLOW_QUERY`ステートメントのすべてに問題があるわけではありません。 `process_time`が非常に大きいものだけがクラスター全体への圧力を高めます。

`wait_time`が非常に大きく、 `process_time`が非常に小さいステートメントは、通常は問題になりません。これは、ステートメントが実際に問題のあるステートメントによってブロックされ、実行キューで待機する必要があるため、応答時間が大幅に長くなるからです。

### <code>ADMIN SHOW SLOW</code>コマンド {#code-admin-show-slow-code-command}

TiDB ログ ファイルに加えて、 `ADMIN SHOW SLOW`コマンドを実行して遅いクエリを特定できます。

```sql
ADMIN SHOW SLOW recent N
ADMIN SHOW SLOW TOP [internal | all] N
```

`recent N` 、最近の N 個の低速クエリ レコードを示します。次に例を示します。

```sql
ADMIN SHOW SLOW recent 10
```

`top N`最近 (数日以内) 最も遅い N クエリ レコードを示します。 `internal`オプションが指定された場合、返される結果はシステムによって実行された内部 SQL になります。 `all`オプションが指定された場合、返される結果は、ユーザーの SQL と内部 SQL を組み合わせたものになります。それ以外の場合、このコマンドはユーザーの SQL からスロー クエリ レコードのみを返します。

```sql
ADMIN SHOW SLOW top 3
ADMIN SHOW SLOW top internal 3
ADMIN SHOW SLOW top all 5
```

メモリが限られているため、TiDB は限られた数のスロー クエリ レコードのみを保存します。クエリ コマンドの値`N`レコード数より大きい場合、返されるレコードの数は`N`より小さくなります。

次の表に出力の詳細を示します。

| カラム名        | 説明                                                |
| :---------- | :------------------------------------------------ |
| 始める         | SQL実行の開始時刻                                        |
| 間隔          | SQLの実行時間                                          |
| 詳細          | SQL実行の詳細                                          |
| 成功しました      | SQL ステートメントが正常に実行されたかどうか。 `1`成功を意味し、 `0`失敗を意味します。 |
| conn_id     | セッションの接続ID                                        |
| トランザクション_ts | 取引の`start ts`                                     |
| ユーザー        | ステートメントを実行するユーザー名                                 |
| データベース      | ステートメントの実行時に関与するデータベース                            |
| テーブルID      | SQL ステートメントの実行時に関係するテーブルの ID                      |
| インデックスID    | SQL ステートメントの実行時に使用されるインデックスの ID                   |
| 内部          | これは TiDB 内部 SQL ステートメントです                         |
| ダイジェスト      | SQL ステートメントのフィンガープリント                             |
| SQL         | 実行中または実行されたSQL文                                   |
