---
title: Identify Slow Queries
summary: スロークエリログを使用して、問題のあるSQL文を特定してください。
---

# 遅いクエリを特定する {#identify-slow-queries}

ユーザーが遅いクエリを特定し、SQL実行のパフォーマンスを分析および改善できるように、TiDBは実行時間が[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) （デフォルト値は300ミリ秒）を超えるステートメントを[スロークエリファイル](/tidb-configuration-file.md#slow-query-file)ファイル（デフォルト値は「tidb-slow.log」）に出力します。

TiDBはデフォルトでスロークエリログを有効にしています。システム変数[`tidb_enable_slow_log`](/system-variables.md#tidb_enable_slow_log)変更することで、この機能を有効または無効にできます。

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

遅いクエリの基本：

-   `Time` : ログの印刷時間。
-   `Query_time` : ステートメントの実行時間。
-   `Parse_time` : ステートメントの解析時間。
-   `Compile_time` : クエリ最適化の所要時間。
-   `Optimize_time` : 実行プランの最適化に要した時間。
-   `Wait_TS` : ステートメントがトランザクションのタイムスタンプを取得するまでの待機時間。
-   `Query` : SQL ステートメント。 `Query`はスローログには出力されませんが、対応するフィールドは、スローログがメモリテーブルにマッピングされた後に`Query`と呼ばれます。
-   `Digest` : SQL ステートメントのフィンガープリント。
-   `Txn_start_ts` : トランザクションの開始タイムスタンプと一意のID。この値を使用して、トランザクション関連のログを検索できます。
-   `Is_internal` : SQL ステートメントが TiDB 内部で実行されるかどうか。 `true`は、SQL ステートメントが TiDB 内部で実行されることを示し、 `false`は、SQL ステートメントがユーザーによって実行されることを示します。
-   `Index_names` : ステートメントで使用されるインデックス名。
-   `Stats` : このクエリ中に使用される統計情報の健全性状態、内部バージョン、総行数、変更された行数、およびロード状態。 `pseudo`統計情報が健全でないことを示します。オプティマイザが完全にロードされていない統計情報を使用しようとすると、内部状態も出力されます。たとえば、 `t1:439478225786634241[105000;5000][col1:allEvicted][idx1:allEvicted]`の意味は次のように理解できます。
    -   `t1` : テーブル`t1`の統計情報は、クエリ最適化中に使用されます。
    -   `439478225786634241` : 内部バージョン。
    -   `105000` : 統計情報における行の総数。
    -   `5000` : 前回の統計収集以降に変更された行数。
    -   `col1:allEvicted` : 列`col1`の統計情報が完全に読み込まれていません。
    -   `idx1:allEvicted` : インデックス`idx1`の統計情報が完全に読み込まれていません。
-   `Succ` : ステートメントが正常に実行されたかどうか。
-   `Backoff_time` : ステートメントが再試行を必要とするエラーに遭遇した場合の、再試行までの待機時間。このような一般的なエラーには、 `lock occurs` 、 `Region split` 、および`tikv server is busy`などがあります。
-   `Plan` : ステートメントの実行プラン。 `SELECT tidb_decode_plan('xxx...')`ステートメントを実行して、具体的な実行プランを解析します。
-   `Binary_plan` : バイナリエンコードされたステートメントの実行プラン。特定の実行プランを解析するには、 [`SELECT tidb_decode_binary_plan('xxx...')`](/functions-and-operators/tidb-functions.md#tidb_decode_binary_plan)ステートメントを実行します。 `Plan`および`Binary_plan`フィールドには同じ情報が含まれています。ただし、これら 2 つのフィールドから解析される実行プランの形式は異なります。
-   `Prepared` : このステートメントが`Prepare`または`Execute`の要求であるかどうか。
-   `Plan_from_cache` : このステートメントが実行プランキャッシュにヒットするかどうか。
-   `Plan_from_binding` : このステートメントがバインドされた実行プランを使用するかどうか。
-   `Has_more_results` : このステートメントには、ユーザーが取得できる結果がさらにあるかどうか。
-   `Rewrite_time` : このステートメントのクエリを書き換えるのに要した時間。
-   `Preproc_subqueries` : ステートメント内で事前に実行されるサブクエリの数。たとえば、 `where id in (select if from t)`サブクエリが事前に実行される場合があります。
-   `Preproc_subqueries_time` : このステートメントのサブクエリを事前に実行するために要した時間。
-   `Exec_retry_count` : このステートメントの再試行回数。このフィールドは通常、ロックが失敗した場合にステートメントが再試行される悲観的トランザクションに使用されます。
-   `Exec_retry_time` : このステートメントの実行再試行時間。たとえば、ステートメントが合計 3 回実行された場合 (最初の 2 回は失敗)、 `Exec_retry_time`最初の 2 回の実行の合計時間を意味します。最後の実行の時間は、 `Query_time`から`Exec_retry_time`引いた時間です。
-   `KV_total` : このステートメントによって、TiKV またはTiFlash上のすべての RPC リクエストに費やされた時間。
-   `PD_total` : このステートメントによる PD 上のすべての RPC リクエストに費やされた時間。
-   `Backoff_total` : このステートメントの実行中にすべてのバックオフに費やされた時間。
-   `Write_sql_response_total` : このステートメントによって結果をクライアントに送信するのに要した時間。
-   `Result_rows` : クエリ結果の行数。
-   `IsExplicitTxn` : このステートメントが明示的なトランザクションに含まれているかどうか。値が`false`の場合、トランザクションは`autocommit=1`となり、ステートメントは実行後に自動的にコミットされます。
-   `Warnings` : このステートメントの実行中に生成される JSON 形式の警告。これらの警告は、一般的に[`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md)ステートメントの出力と一致しますが、より詳細な診断情報を提供する追加の警告が含まれる場合があります。これらの追加の警告は`IsExtra: true`としてマークされます。

以下の項目はトランザクションの実行に関連しています。

-   `Prewrite_time` : 2 フェーズ トランザクション コミットの最初のフェーズ (プリライト) の期間。
-   `Commit_time` : 2 フェーズ トランザクション コミットの第 2 フェーズ (コミット) の期間。
-   `Get_commit_ts_time` : 2 フェーズ トランザクション コミットの第 2 フェーズ (コミット) で`commit_ts`取得するのに費やされた時間。
-   `Local_latch_wait_time` : TiDB が 2 相トランザクションコミットの第 2 相 (コミット) の前にロックを待機するのに費やす時間。
-   `Write_keys` : トランザクションが TiKV の Write CF に書き込むキーの数。
-   `Write_size` : トランザクションがコミットされたときに書き込まれるキーまたは値の合計サイズ。
-   `Prewrite_region` : 2フェーズトランザクションコミットの第1フェーズ（プリライト）に関与するTiKVリージョンの数。各リージョンはリモートプロシージャコールをトリガーします。
-   `Wait_prewrite_binlog_time` : トランザクションがコミットされたときにバイナリログを書き込むのに要した時間。v8.4.0以降、TiDB Binlogは削除され、このフィールドには値がありません。
-   `Resolve_lock_time` : トランザクションのコミット中にロックが発生した場合、ロックを解消するか、ロックの有効期限が切れるまで待機する時間。

メモリ使用量フィールド:

-   `Mem_max` : SQL ステートメントの実行期間中に使用される最大メモリ領域 (単位はバイト)。

ハードディスクの項目:

-   `Disk_max` : SQL ステートメントの実行期間中に使用される最大ディスク容量 (単位はバイト)。

ユーザーフィールド:

-   `User` : このステートメントを実行するユーザーの名前。
-   `Host` : このステートメントのホスト名。
-   `Conn_ID` : 接続ID（セッションID）。たとえば、キーワード`con:3`を使用して、セッションIDが`3`のログを検索できます。
-   `DB` : 現在のデータベース。

TiKVコプロセッサータスクフィールド：

-   `Request_count` : ステートメントが送信するコプロセッサー要求の数。
-   `Total_keys` :コプロセッサーがスキャンしたキーの数。
-   `Process_time` : TiKV における SQL ステートメントの合計処理時間。データは TiKV に同時送信されるため、この値は`Query_time`を超える場合があります。
-   `Wait_time` : TiKV におけるステートメントの合計待機時間。TiKV のコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが動作している場合、リクエストがキューに蓄積される可能性があります。キュー内のリクエストの処理に時間がかかると、後続のリクエストの待機時間が増加します。
-   `Process_keys` :コプロセッサーが処理したキーの数。 `total_keys`と比較すると、 `processed_keys`には MVCC の古いバージョンは含まれていません。 `processed_keys`と`total_keys`の間に大きな差があることから、多くの古いバージョンが存在することがわかります。
-   `Num_cop_tasks` : このステートメントによって送信されたコプロセッサータスクの数。
-   `Cop_proc_avg` : RocksDB のミューテックスなど、カウントできない待機時間を含む、cop-tasks の平均実行時間。
-   `Cop_proc_p90` : cop-tasks の P90 実行時間。
-   `Cop_proc_max` : cop-tasks の最大実行時間。
-   `Cop_proc_addr` : 実行時間が最も長いコップタスクのアドレス。
-   `Cop_wait_avg` : リクエストのキューイングとスナップショットの取得時間を含む、cop-tasks の平均待機時間。
-   `Cop_wait_p90` : 警官タスクの P90 待機時間。
-   `Cop_wait_max` : 警官タスクの最大待機時間。
-   `Cop_wait_addr` : 待ち時間が最も長い警官タスクのアドレス。
-   `Rocksdb_delete_skipped_count` : RocksDB がデータをスキャンする際に検出する削除済み (墓石) キーの数。
-   `Rocksdb_key_skipped_count` : RocksDB がデータをスキャンする際に遭遇するすべてのキーの数。
-   `Rocksdb_block_cache_hit_count` : RocksDB がブロックキャッシュからデータを読み取る回数。
-   `Rocksdb_block_read_count` : RocksDB がファイルシステムからデータを読み取る回数。
-   `Rocksdb_block_read_byte` : RocksDB がファイルシステムから読み取るデータ量。
-   `Rocksdb_block_read_time` : RocksDB がファイルシステムからデータを読み取るのにかかる時間。
-   `Cop_backoff_{backoff-type}_total_times` : エラーによって発生したバックオフの合計回数。
-   `Cop_backoff_{backoff-type}_total_time` : エラーによって発生したバックオフの合計時間。
-   `Cop_backoff_{backoff-type}_max_time` : エラーによって発生したバックオフの最長時間。
-   `Cop_backoff_{backoff-type}_max_addr` : エラーによって最も長いバックオフ時間が発生したコップタスクのアドレス。
-   `Cop_backoff_{backoff-type}_avg_time` : エラーによって発生するバックオフの平均時間。
-   `Cop_backoff_{backoff-type}_p90_time` : エラーによって発生した P90 パーセンタイルバックオフ時間。

`backoff-type`は、一般的に以下の種類が含まれます。

-   `tikvRPC` : TiKV への RPC リクエストの送信に失敗したために発生したバックオフ。
-   `tiflashRPC` : TiFlashへの RPC リクエストの送信に失敗したために発生したバックオフ。
-   `pdRPC` : PD への RPC リクエストの送信に失敗したために発生したバックオフ。
-   `txnLock` : ロックの競合によって発生するバックオフ。
-   `regionMiss` : リージョンが分割またはマージされた後に TiDBリージョンキャッシュ情報が古くなった場合に、リクエストの処理が失敗することによって発生するバックオフ。
-   `regionScheduling` : リージョンがスケジュールされていてLeaderが選択されていない場合、TiDB はリクエストを処理できないため、バックオフが発生します。
-   `tikvServerBusy` : TiKV の負荷が高すぎて新しいリクエストを処理できないために発生するバックオフ。
-   `tiflashServerBusy` : TiFlash の負荷が高すぎて新しいリクエストを処理できないために発生するバックオフ。
-   `tikvDiskFull` : TiKV ディスクがいっぱいになったことが原因で発生したバックオフ。
-   `txnLockFast` : データ読み取り中にロックが発生したことが原因で発生するバックオフ。

リソース制御に関連する分野：

-   `Resource_group` : ステートメントがバインドされているリソース グループ。
-   `Request_unit_read` : ステートメントによって消費された読み取り RU の合計。
-   `Request_unit_write` : ステートメントによって消費された書き込み RU の合計。
-   `Time_queued_by_rc` : ステートメントが利用可能なリソースを待機する合計時間。

storageエンジンに関連する分野：

-   `Storage_from_kv` : v8.5.5 で導入され、このステートメントが TiKV からデータを読み取ったかどうかを示します。
-   `Storage_from_mpp` : v8.5.5 で導入され、このステートメントがTiFlashからデータを読み取ったかどうかを示します。

## <code>tidb_slow_log_rules</code>を使用する {#use-code-tidb-slow-log-rules-code}

[`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules-new-in-v856)は、スロークエリログのトリガールールを定義するために使用され、多次元メトリックの組み合わせをサポートします。スローログの「ターゲットサンプリング」と「問題再現」に適しており、特定のメトリックの組み合わせに基づいて対象のステートメントをフィルタリングできます。

スロークエリログのトリガー動作は`tidb_slow_log_rules`の設定に依存します。

-   `tidb_slow_log_rules`が設定されていない場合、スロークエリログのトリガーは引き続き[`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) (ミリ秒単位) に依存します。
-   `tidb_slow_log_rules`が設定されている場合、設定済みのルールが優先され、 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)は無視されます。

各フィールドの意味、診断値、および背景情報の詳細については、[フィールドの説明](#fields-description)参照してください。

### 統一されたルール構文と型制約 {#unified-rule-syntax-and-type-constraints}

-   ルール容量と分離: `SESSION`と`GLOBAL`はそれぞれ最大 10 個のルールをサポートします。1 つのセッションで最大 20 個のアクティブなルールを持つことができます。ルールは`;`で分離されます。
-   条件の形式: 各条件は`field_name:value`の形式を使用します。単一のルール内の複数の条件は`,`で区切られます。
-   フィールドとスコープ: フィールド名は大文字と小文字を区別しません (アンダースコアやその他の文字は保持されます)。 `SESSION`ルールは`Conn_ID`をサポートしていません。 `GLOBAL`ルールのみが`Conn_ID`をサポートしています。
-   意味の一致：
    -   数値フィールドは`>=`を使用して照合されます。文字列フィールドとブール値フィールドは等価性 ( `=` ) を使用して照合されます。
    -   `DB`と`Resource_group`のマッチングは、大文字と小文字を区別しません。
    -   `>` 、 `<` 、 `!=`などの明示的な演算子はサポートされていません。

型制約は以下のとおりです。

-   数値型（ `int64` 、 `uint64` 、 `float64` ）は、いずれも`>= 0`を必要とします。負の値を指定すると、解析エラーが発生します。
    -   `int64` : 最大値は`2^63-1`です。
    -   `uint64` : 最大値は`2^64-1`です。
    -   `float64` : 一般的な上限はおおよそ`1.79e308`です。現在、解析は Go の`ParseFloat`を使用して行われています。 `NaN` / `Inf`は解析できますが、常に真または常に偽となるルールにつながる可能性があります。これらを使用することは推奨されません。
-   `bool` : `true` / `false` 、 `1` / `0` 、および`t` / `f`をサポートします (大文字小文字を区別しません)。
-   `string` : 現在`,` (条件区切り文字) または`;` (ルール区切り文字) を含む文字列は、引用符 (シングルクォートまたはダブルクォート) があってもサポートされていません。エスケープ処理もサポートされていません。
-   重複するフィールド：単一のルール内で同じフィールドが複数回指定されている場合、最後に指定されたフィールドが有効になります。

### サポートされているフィールド {#supported-fields}

フィールドの詳細な説明、診断の意味、背景情報については、 [`identify-slow-queries`のフィールド説明](/identify-slow-queries.md#fields-description)参照してください。

特に断りのない限り、次の表のフィールドは [統一されたルール構文と型制約](#unified-rule-syntax-and-type-constraints)型安定」で説明されている一般的な一致および型ルールに従います。この表には、現在サポートされているフィールド名、タイプ、単位、およびルール固有のいくつかの注意事項のみがリストされています。各フィールドの意味論的な意味を繰り返すことはありません。

| フィールド名                                       | タイプ      | ユニット | 注記                                 |
| -------------------------------------------- | -------- | ---- | ---------------------------------- |
| `Conn_ID`                                    | `uint`   | カウント | `GLOBAL`ルールでのみサポートされています。          |
| `Session_alias`                              | `string` | なし   | -                                  |
| `DB`                                         | `string` | なし   | マッチング時に大文字小文字を区別しない                |
| `Exec_retry_count`                           | `uint`   | カウント | -                                  |
| `Query_time`                                 | `float`  | 2番   | -                                  |
| `Parse_time`                                 | `float`  | 2番   | -                                  |
| `Compile_time`                               | `float`  | 2番   | -                                  |
| `Rewrite_time`                               | `float`  | 2番   | -                                  |
| `Optimize_time`                              | `float`  | 2番   | -                                  |
| `Wait_TS`                                    | `float`  | 2番   | -                                  |
| `Is_internal`                                | `bool`   | なし   | -                                  |
| `Digest`                                     | `string` | なし   | -                                  |
| `Plan_digest`                                | `string` | なし   | -                                  |
| `Num_cop_tasks`                              | `int`    | カウント | -                                  |
| `Mem_max`                                    | `int`    | バイト  | -                                  |
| `Disk_max`                                   | `int`    | バイト  | -                                  |
| `Write_sql_response_total`                   | `float`  | 2番   | -                                  |
| `Succ`                                       | `bool`   | なし   | -                                  |
| `Resource_group`                             | `string` | なし   | マッチング時に大文字小文字を区別しない                |
| `KV_total`                                   | `float`  | 2番   | -                                  |
| `PD_total`                                   | `float`  | 2番   | -                                  |
| `Unpacked_bytes_sent_tikv_total`             | `int`    | バイト  | -                                  |
| `Unpacked_bytes_received_tikv_total`         | `int`    | バイト  | -                                  |
| `Unpacked_bytes_sent_tikv_cross_zone`        | `int`    | バイト  | -                                  |
| `Unpacked_bytes_received_tikv_cross_zone`    | `int`    | バイト  | -                                  |
| `Unpacked_bytes_sent_tiflash_total`          | `int`    | バイト  | -                                  |
| `Unpacked_bytes_received_tiflash_total`      | `int`    | バイト  | -                                  |
| `Unpacked_bytes_sent_tiflash_cross_zone`     | `int`    | バイト  | -                                  |
| `Unpacked_bytes_received_tiflash_cross_zone` | `int`    | バイト  | -                                  |
| `Process_time`                               | `float`  | 2番   | -                                  |
| `Backoff_time`                               | `float`  | 2番   | -                                  |
| `Total_keys`                                 | `uint`   | カウント | -                                  |
| `Process_keys`                               | `uint`   | カウント | -                                  |
| `cop_mvcc_read_amplification`                | `float`  | 比率   | 比率値（ `Total_keys / Process_keys` ） |
| `Prewrite_time`                              | `float`  | 2番   | -                                  |
| `Commit_time`                                | `float`  | 2番   | -                                  |
| `Write_keys`                                 | `uint`   | カウント | -                                  |
| `Write_size`                                 | `uint`   | バイト  | -                                  |
| `Prewrite_region`                            | `uint`   | カウント | -                                  |

### 効果的な行動とマッチング順序 {#effective-behavior-and-matching-order}

-   ルール更新動作: `SET [SESSION|GLOBAL] tidb_slow_log_rules = '...'`の実行ごとに、既存のルールに追加するのではなく、そのスコープ内の既存のルールを上書きします。
-   ルールクリア動作: `SET [SESSION|GLOBAL] tidb_slow_log_rules = ''`対応するスコープ内のルールをクリアします。
-   現在のセッションに、 `tidb_slow_log_rules`ルール、現在の`SESSION`に対する`GLOBAL`ルール、または`Conn_ID`を含まない一般的なグローバルルールなど、適用可能な`Conn_ID`がある場合、スロークエリログの出力はルールのマッチング結果によって決定され、 `tidb_slow_log_threshold`は使用されなくなります。
-   現在のセッションに適用可能なルールがない場合、たとえば`SESSION`と`GLOBAL`両方のルールが空の場合、または現在の`GLOBAL`に一致しない`Conn_ID`ルールのみが構成されている場合、スロークエリのログ記録は`tidb_slow_log_threshold`に依存します。単位はミリ秒であることに注意してください。
-   スローログを書き込む条件としてSQL実行時間を使用したい場合は、ルール内で`Query_time`を使用し、単位が秒であることに注意してください。
-   ルールマッチングロジック：
    -   複数のルールは`OR`で結合され、単一のルール内の複数のフィールド条件は`AND`で結合されます。
    -   `SESSION`スコープのルールが最初に一致します。一致するルールがない場合、TiDB は現在の`GLOBAL`に対して`Conn_ID`ルールを一致させ、続いて`GLOBAL`を含まない一般的な`Conn_ID`ルールを一致させます。
-   `SHOW VARIABLES LIKE 'tidb_slow_log_rules'`と`SELECT @@SESSION.tidb_slow_log_rules`は`SESSION`ルールテキストを返します。設定されていない場合は空の文字列を返します。 `SELECT @@GLOBAL.tidb_slow_log_rules` `GLOBAL`ルールテキストを返します。

### 例 {#examples}

-   標準フォーマット（ `SESSION`範囲）：

    ```sql
    SET SESSION tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

-   無効な形式です（ `SESSION`スコープは`Conn_ID`をサポートしていません）：

    ```sql
    SET SESSION tidb_slow_log_rules = 'Conn_ID: 12, Query_time: 0.5, Is_internal: false';
    ```

-   グローバルルール（すべての接続に適用）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Query_time: 0.5, Is_internal: false';
    ```

-   特定の接続に対するグローバルルール（ `Conn_ID:11`と`Conn_ID:12` 2 つの接続にそれぞれ適用されます）：

    ```sql
    SET GLOBAL tidb_slow_log_rules = 'Conn_ID: 11, Query_time: 0.5, Is_internal: false; Conn_ID: 12, Query_time: 0.6, Process_time: 0.3, DB: db1';
    ```

### 推奨事項 {#recommendations}

-   `tidb_slow_log_rules`単一しきい値方式に代わるように設計されています。多次元メトリック条件の組み合わせをサポートし、低速クエリのログ記録をより柔軟かつきめ細かく制御できます。

-   TiDBノード1台（CPUコア16個、メモリ48GiB）とTiKVノード3台（それぞれCPUコア16個、メモリ48GiB）を備えた十分なリソースが確保されたテスト環境で、sysbenchテストを繰り返したところ、多次元スロークエリログルールによって30分以内に数百万件のスローログエントリが生成されても、パフォーマンスへの影響は小さいままであることが分かりました。しかし、ログの量が数千万件に達すると、TPSが大幅に低下し、レイテンシーが著しく増加します。そのため、業務ワークロードが高い場合や、CPUとメモリのリソースが限界に近い場合は、 `tidb_slow_log_rules`を慎重に設定して、ルールが広すぎるためにログが大量に発生するのを防いでください。ログ出力レートを制限する必要がある場合は、 [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec-new-in-v856)を使用してスロットリングを行い、業務パフォーマンスへの影響を軽減してください。

## 関連するシステム変数 {#related-system-variables}

-   [`tidb_slow_log_rules`](/system-variables.md#tidb_slow_log_rules-new-in-v856) : [`tidb_slow_log_rules`推奨事項](#recommendations)を参照

-   [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) : スロークエリログのしきい値を設定します。実行時間がこのしきい値を超える SQL ステートメントは、スロークエリログに記録されます。デフォルト値は`300ms` (ミリ秒) です。

    > **ヒント：**
    >
    > `tidb_slow_log_rules`の時間関連フィールド（ `Query_time`や`Process_time`など）は単位として秒を使用し、小数点を含むことができますが、 [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold)ミリ秒を使用します。

-   [`tidb_slow_log_max_per_sec`](/system-variables.md#tidb_slow_log_max_per_sec-new-in-v856) : 1 秒あたりに書き込めるスロークエリログエントリの最大数を設定します。デフォルト値は`0`です。この変数は v8.5.6 で導入されました。
    -   `0`という値は、1 秒あたりに書き込まれるスロークエリログエントリの数に制限がないことを意味します。
    -   `0`より大きい値を指定すると、TiDBは1秒あたりに指定された数のスロークエリログエントリを書き込みます。超過分のログエントリは破棄され、スロークエリログファイルには書き込まれません。
    -   ルールベースの低速クエリログが頻繁にトリガーされるのを防ぐため、 `tidb_slow_log_rules`を有効にした後にこの変数を設定することをお勧めします。

-   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len) : スロークエリログに記録されるSQLステートメントの最大長を設定します。デフォルト値は4096バイトです。

-   [`tidb_redact_log`](/system-variables.md#tidb_redact_log) : スロークエリログに記録される SQL ステートメント内のユーザーデータが編集され、 `?`に置き換えられるかどうかを制御します。デフォルト値は`0`で、この機能は無効になっています。

-   [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) : 実行プラン内の各オペレーターの物理実行情報を記録するかどうかを制御します。デフォルト値は`1`です。この機能はパフォーマンスに約 3% 影響します。この機能を有効にすると、 `Plan`の情報を次のように表示できます。

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

`Plan`フィールドの戻り値は、 `EXPLAIN`または`EXPLAIN ANALYZE`とほぼ同じ形式です。実行プランの詳細については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)参照してください。

詳細については、 [TiDB固有の変数と構文](/system-variables.md)参照してください。

## スローログのメモリマッピング {#memory-mapping-in-slow-log}

`INFORMATION_SCHEMA.SLOW_QUERY`テーブルをクエリすることで、スロークエリログの内容を照会できます。テーブル内の各列名は、スローログ内のフィールド名に対応しています。テーブル構造については、 [情報スキーマ](/information-schema/information-schema-slow-query.md)の`SLOW_QUERY`テーブルの概要を参照してください。

> **注記：**
>
> `SLOW_QUERY`テーブルに対してクエリを実行するたびに、TiDB は現在のスロークエリログを読み取って解析します。

TiDB 4.0 では、 `SLOW_QUERY`は、ローテーションされたスローログファイルを含む、任意の期間のスローログのクエリをサポートしています。解析する必要のあるスローログファイルを見つけるには`TIME`の範囲を指定する必要があります。 `TIME`の範囲を指定しない場合、TiDB は現在のスローログファイルのみを解析します。例:

-   時間範囲を指定しない場合、TiDB はスローログファイルに書き込むスロークエリデータのみを解析します。

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

-   例えば、 `2020-03-10 00:00:00`から`2020-03-11 00:00:00`までといった時間範囲を指定すると、TiDB はまず指定された時間範囲のスローログファイルを探し出し、次にスロークエリ情報を解析します。

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
> 指定された期間のスローログファイルが削除された場合、またはスロークエリが存在しない場合、クエリはNULLを返します。

TiDB 4.0 では、すべての TiDB ノードのスロー クエリ情報を照会するための[`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table)システム テーブルが追加されました。 `CLUSTER_SLOW_QUERY`テーブルのテーブル スキーマは`SLOW_QUERY`に`INSTANCE`列が追加されている点で`CLUSTER_SLOW_QUERY`テーブルのスキーマとは異なります。 `INSTANCE`列は、スロー クエリの行情報の TiDB ノード アドレスを表します。 `CLUSTER_SLOW_QUERY` 、 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)と同様に使用できます。

`CLUSTER_SLOW_QUERY`テーブルに対してクエリを実行すると、TiDB は他のノードからすべての低速クエリ情報を取得して 1 つの TiDB ノードで操作を実行するのではなく、計算と判断を他のノードにプッシュします。

## <code>SLOW_QUERY</code> / <code>CLUSTER_SLOW_QUERY</code>使用例 {#code-slow-query-code-code-cluster-slow-query-code-usage-examples}

### 上位N件の低速クエリ {#top-n-slow-queries}

ユーザーの遅いクエリ上位 2 件をクエリします。 `Is_internal=false` TiDB 内の遅いクエリを除外し、ユーザーの遅いクエリのみをクエリすることを意味します。

```sql
select query_time, query
from information_schema.slow_query
where is_internal = false
order by query_time desc
limit 2;
```

出力例：

    +--------------+------------------------------------------------------------------+
    | query_time   | query                                                            |
    +--------------+------------------------------------------------------------------+
    | 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
    |  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
    +--------------+------------------------------------------------------------------+

### <code>test</code>ユーザーの上位N件の遅いクエリを照会する {#query-the-top-n-slow-queries-of-the-code-test-code-user}

次の例では、 `test`ユーザーによって実行された低速クエリが照会され、最初の 2 つの結果が実行時間の逆順に表示されます。

```sql
select query_time, query, user
from information_schema.slow_query
where is_internal = false
  and user = "test"
order by query_time desc
limit 2;
```

出力例：

    +-------------+------------------------------------------------------------------+----------------+
    | Query_time  | query                                                            | user           |
    +-------------+------------------------------------------------------------------+----------------+
    | 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test           |
    +-------------+------------------------------------------------------------------+----------------+

### 同じSQLフィンガープリントを持つ類似の低速クエリを検索する {#query-similar-slow-queries-with-the-same-sql-fingerprints}

上位N個のSQL文を照会した後、同じフィンガープリントを使用して、同様の低速なクエリを引き続き照会します。

1.  処理速度の遅い上位N件のクエリと、それに対応するSQLフィンガープリントを取得します。

    ```sql
    select query_time, query, digest
    from information_schema.slow_query
    where is_internal = false
    order by query_time desc
    limit 1;
    ```

    出力例：

        +-------------+-----------------------------+------------------------------------------------------------------+
        | query_time  | query                       | digest                                                           |
        +-------------+-----------------------------+------------------------------------------------------------------+
        | 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
        +-------------+-----------------------------+------------------------------------------------------------------+

2.  同様の遅いクエリをフィンガープリントを使って照会する。

    ```sql
    select query, query_time
    from information_schema.slow_query
    where digest = "4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
    ```

    出力例：

        +-----------------------------+-------------+
        | query                       | query_time  |
        +-----------------------------+-------------+
        | select * from t1 where a=1; | 0.302558006 |
        | select * from t1 where a=2; | 0.401313532 |
        +-----------------------------+-------------+

## 擬似統計<code>stats</code>を使用して、遅いクエリをクエリする {#query-slow-queries-with-pseudo-code-stats-code}

```sql
select query, query_time, stats
from information_schema.slow_query
where is_internal = false
  and stats like '%pseudo%';
```

出力例：

    +-----------------------------+-------------+---------------------------------+
    | query                       | query_time  | stats                           |
    +-----------------------------+-------------+---------------------------------+
    | select * from t1 where a=1; | 0.302558006 | t1:pseudo                       |
    | select * from t1 where a=2; | 0.401313532 | t1:pseudo                       |
    | select * from t1 where a>2; | 0.602011247 | t1:pseudo                       |
    | select * from t1 where a>3; | 0.50077719  | t1:pseudo                       |
    | select * from t1 join t2;   | 0.931260518 | t1:407872303825682445,t2:pseudo |
    +-----------------------------+-------------+---------------------------------+

### 実行プランが変更された遅いクエリ {#query-slow-queries-whose-execution-plan-is-changed}

同じカテゴリのSQL文の実行プランを変更すると、統計情報が古くなっているか、実際のデータ分布を正確に反映していないため、実行速度が低下します。実行プランが異なるSQL文を照会するには、次のSQL文を使用できます。

```sql
select count(distinct plan_digest) as count,
       digest,
       min(query)
from cluster_slow_query
group by digest
having count > 1
limit 3\G
```

出力例：

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

そして、上記のクエリ結果に含まれるSQLフィンガープリントを使用して、さまざまなプランを照会できます。

```sql
select min(plan),
       plan_digest
from cluster_slow_query
where digest='17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94'
group by plan_digest\G
```

出力例：

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

### クラスタ内の各TiDBノードにおける低速クエリの数を照会する {#query-the-number-of-slow-queries-for-each-tidb-node-in-a-cluster}

```sql
select instance, count(*) from information_schema.cluster_slow_query where time >= "2020-03-06 00:00:00" and time < now() group by instance;
```

出力例：

    +---------------+----------+
    | instance      | count(*) |
    +---------------+----------+
    | 0.0.0.0:10081 | 124      |
    | 0.0.0.0:10080 | 119771   |
    +---------------+----------+

### クエリの遅延ログが異常な時間帯にのみ発生する {#query-slow-logs-occurring-only-in-abnormal-time-period}

`2020-03-10 13:24:00`から`2020-03-10 13:27:00`までの期間に QPS の低下やレイテンシーの増加などの問題が発生した場合、原因は大規模なクエリが発生している可能性があります。次の SQL ステートメントを実行して、異常な期間にのみ発生するスロー ログを照会します。 `2020-03-10 13:20:00`から`2020-03-10 13:23:00`までの期間は通常の期間を指します。

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

出力例：

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

### 他のTiDBスローログファイルを解析する {#parse-other-tidb-slow-log-files}

TiDB は`tidb_slow_query_file` `INFORMATION_SCHEMA.SLOW_QUERY`を使用します。セッション変数の値を変更することで、他のスロークエリログファイルの内容をクエリできます。

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

### <code>pt-query-digest</code>を使用してTiDBのスローログを解析する {#parse-tidb-slow-logs-with-code-pt-query-digest-code}

TiDB のスローログを解析するには、 `pt-query-digest`を使用します。

> **注記：**
>
> `pt-query-digest` 3.0.13以降のバージョンを使用することをお勧めします。

例えば：

```shell
pt-query-digest --report tidb-slow.log
```

出力例：

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

`SLOW_QUERY`ステートメントのすべてが問題となるわけではありません。 `process_time`の値が非常に大きいステートメントのみが、クラスター全体に負荷をかけます。

`wait_time`が非常に大きく、 `process_time`が非常に小さいステートメントは、通常は問題になりません。これは、そのステートメントが実際に問題のあるステートメントによってブロックされ、実行キューで待機する必要があるため、応答時間が大幅に長くなるためです。

### <code>ADMIN SHOW SLOW</code>コマンド {#code-admin-show-slow-code-command}

TiDBログファイルに加えて、 `ADMIN SHOW SLOW`コマンドを実行することで、遅いクエリを特定できます。

```sql
ADMIN SHOW SLOW recent N
ADMIN SHOW SLOW TOP [internal | all] N
```

`recent N`は、最近の N 件の低速クエリレコードを表示します。例:

```sql
ADMIN SHOW SLOW recent 10
```

`top N`は、最近 (数日以内) 実行されたクエリレコードのうち、最も実行速度の遅い N 件を表示します。 `internal`オプションが指定されている場合、返される結果はシステムによって実行された内部 SQL になります。 `all`オプションが指定されている場合、返される結果はユーザーの SQL と内部 SQL を組み合わせたものになります。それ以外の場合、このコマンドはユーザーの SQL から実行速度の遅いクエリレコードのみを返します。

```sql
ADMIN SHOW SLOW top 3
ADMIN SHOW SLOW top internal 3
ADMIN SHOW SLOW top all 5
```

TiDB はメモリが限られているため、低速クエリのレコードを限られた数しか保存しません。クエリ コマンドの`N`の値がレコード数より大きい場合、返されるレコード数は`N`より少なくなります。

以下の表は出力の詳細を示しています。

| カラム名        | 説明                                            |
| :---------- | :-------------------------------------------- |
| 始める         | SQL実行の開始時刻                                    |
| 間隔          | SQL実行の所要時間                                    |
| 詳細          | SQL実行の詳細                                      |
| う           | SQL文が正常に実行されたかどうかを示します。 `1`は成功、 `0`は失敗を意味します。 |
| conn_id     | セッションの接続ID                                    |
| トランザクション_ts | 取引の`start ts`                                 |
| ユーザー        | ステートメントを実行するためのユーザー名                          |
| db          | ステートメントの実行時に関係するデータベース                        |
| テーブルID      | SQL文の実行時に関係するテーブルのID                          |
| インデックスID    | SQL文の実行時に関係するインデックスのID                        |
| 内部          | これはTiDB内部のSQLステートメントです                        |
| ダイジェスト      | SQLステートメントの指紋                                 |
| SQL         | 実行中または既に実行されたSQLステートメント                       |
