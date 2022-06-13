---
title: Identify Slow Queries
summary: Use the slow query log to identify problematic SQL statements.
---

# 遅いクエリを特定する {#identify-slow-queries}

ユーザーが遅いクエリを識別し、SQL実行のパフォーマンスを分析および改善できるように、TiDBは、実行時間が[遅いしきい値](/tidb-configuration-file.md#slow-threshold) （デフォルト値は300ミリ秒）から[遅いクエリファイル](/tidb-configuration-file.md#slow-query-file) （デフォルト値は &quot;tidb-slow.log&quot;）を超えるステートメントを出力します。

TiDBは、デフォルトで低速クエリログを有効にします。構成を変更することにより、機能を有効または無効にできます[`enable-slow-log`](/tidb-configuration-file.md#enable-slow-log) 。

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

> **ノート：**
>
> 低速クエリログの以下のすべての時間フィールドの単位は**「秒」**です。

遅いクエリの基本：

-   `Time` ：ログの印刷時間。
-   `Query_time` ：ステートメントの実行時間。
-   `Parse_time` ：ステートメントの解析時間。
-   `Compile_time` ：クエリ最適化の期間。
-   `Query` ：SQLステートメント。 `Query`はスローログに出力されませんが、スローログがメモリテーブルにマップされた後、対応するフィールドは`Query`と呼ばれます。
-   `Digest` ：SQLステートメントのフィンガープリント。
-   `Txn_start_ts` ：開始タイムスタンプとトランザクションの一意のID。この値を使用して、トランザクション関連のログを検索できます。
-   `Is_internal` ：SQLステートメントがTiDB内部であるかどうか。 `true`はSQLステートメントがTiDBの内部で実行されることを示し、 `false`はSQLステートメントがユーザーによって実行されることを示します。
-   `Index_ids` ：ステートメントに含まれるインデックスのID。
-   `Succ` ：ステートメントが正常に実行されたかどうか。
-   `Backoff_time` ：ステートメントで再試行が必要なエラーが発生した場合の再試行までの待機時間。一般的なエラーには、 `lock occurs` 、および`Region split`が含まれ`tikv server is busy` 。
-   `Plan` ：ステートメントの実行プラン。 `select tidb_decode_plan('xxx...')`ステートメントを使用して、特定の実行プランを解析します。
-   `Prepared` ：このステートメントが`Prepare`または`Execute`の要求であるかどうか。
-   `Plan_from_cache` ：このステートメントが実行プランのキャッシュにヒットするかどうか。
-   `Rewrite_time` ：このステートメントのクエリを書き換えるのにかかった時間。
-   `Preproc_subqueries` ：事前に実行された（ステートメント内の）サブクエリの数。たとえば、 `where id in (select if from t)`のサブクエリが事前に実行される場合があります。
-   `Preproc_subqueries_time` ：このステートメントのサブクエリを事前に実行するために費やされた時間。
-   `Exec_retry_count` ：このステートメントの再試行回数。このフィールドは通常、ロックが失敗したときにステートメントが再試行される悲観的なトランザクション用です。
-   `Exec_retry_time` ：このステートメントの実行再試行期間。たとえば、ステートメントが合計3回実行された（最初の2回失敗した）場合、 `Exec_retry_time`は最初の2回の実行の合計期間を意味します。最後の実行の期間は`Query_time`マイナス`Exec_retry_time`です。

次のフィールドは、トランザクションの実行に関連しています。

-   `Prewrite_time` ：2フェーズトランザクションコミットの最初のフェーズ（プリライト）の期間。
-   `Commit_time` ：2フェーズトランザクションコミットの2番目のフェーズ（コミット）の期間。
-   `Get_commit_ts_time` ：2フェーズトランザクションコミットの第2フェーズ（コミット）中に`commit_ts`を取得するために費やされた時間。
-   `Local_latch_wait_time` ：2フェーズトランザクションコミットの第2フェーズ（コミット）の前にTiDBがロックの待機に費やす時間。
-   `Write_keys` ：トランザクションがTiKVの書き込みCFに書き込むキーの数。
-   `Write_size` ：トランザクションがコミットするときに書き込まれるキーまたは値の合計サイズ。
-   `Prewrite_region` ：2フェーズトランザクションコミットの最初のフェーズ（プリライト）に関与するTiKVリージョンの数。各リージョンは、リモートプロシージャコールをトリガーします。

メモリ使用量フィールド：

-   `Mem_max` ：SQLステートメントの実行期間中に使用される最大メモリスペース（単位はバイト）。

ハードディスクフィールド：

-   `Disk_max` ：SQL文の実行中に使用される最大ディスク容量（単位はバイト）。

ユーザーフィールド：

-   `User` ：このステートメントを実行するユーザーの名前。
-   `Conn_ID` ：接続ID（セッションID）。たとえば、キーワード`con:3`を使用して、セッションIDが`3`のログを検索できます。
-   `DB` ：現在のデータベース。

TiKVコプロセッサータスクフィールド：

-   `Request_count` ：ステートメントが送信するコプロセッサー要求の数。
-   `Total_keys` ：コプロセッサーがスキャンしたキーの数。
-   `Process_time` ：TiKVでのSQLステートメントの合計処理時間。データは同時にTiKVに送信されるため、この値は`Query_time`を超える可能性があります。
-   `Wait_time` ：TiKVでのステートメントの合計待機時間。 TiKVのコプロセッサーは限られた数のスレッドを実行するため、コプロセッサーのすべてのスレッドが機能しているときに要求がキューに入れられる可能性があります。キュー内のリクエストの処理に時間がかかると、後続のリクエストの待機時間が長くなります。
-   `Process_keys` ：コプロセッサーが処理したキーの数。 `total_keys`と比較すると、 `processed_keys`には古いバージョンのMVCCが含まれていません。 `processed_keys`と`total_keys`の大きな違いは、多くの古いバージョンが存在することを示しています。
-   `Cop_proc_avg` ：RocksDBのミューテックスなど、カウントできない待機時間を含む、cop-tasksの平均実行時間。
-   `Cop_proc_p90` ：cop-tasksのP90実行時間。
-   `Cop_proc_max` ：cop-tasksの最大実行時間。
-   `Cop_proc_addr` ：実行時間が最も長いcop-taskのアドレス。
-   `Cop_wait_avg` ：リクエストのキューイングとスナップショットの取得の時間を含む、cop-tasksの平均待機時間。
-   `Cop_wait_p90` ：cop-tasksのP90待機時間。
-   `Cop_wait_max` ：cop-tasksの最大待機時間。
-   `Cop_wait_addr` ：待ち時間が最も長い警官タスクのアドレス。
-   `Cop_backoff_{backoff-type}_total_times` ：エラーによって発生したバックオフの合計時間。
-   `Cop_backoff_{backoff-type}_total_time` ：エラーによるバックオフの合計時間。
-   `Cop_backoff_{backoff-type}_max_time` ：エラーによるバックオフの最長時間。
-   `Cop_backoff_{backoff-type}_max_addr` ：エラーによるバックオフ時間が最も長いcop-taskのアドレス。
-   `Cop_backoff_{backoff-type}_avg_time` ：エラーによるバックオフの平均時間。
-   `Cop_backoff_{backoff-type}_p90_time` ：エラーによるP90パーセンタイルバックオフ時間。

## 関連するシステム変数 {#related-system-variables}

-   [`tidb_slow_log_threshold`](/system-variables.md#tidb_slow_log_threshold) ：低速ログのしきい値を設定します。実行時間がこのしきい値を超えるSQLステートメントは、低速ログに記録されます。デフォルト値は300（ms）です。
-   [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len) ：スローログに記録されるSQLステートメントの最大長を設定します。デフォルト値は4096（バイト）です。
-   [tidb_redact_log](/system-variables.md#tidb_redact_log) ：低速ログに記録されたSQLステートメントで`?`を使用してユーザーデータの感度を下げるかどうかを決定します。デフォルト値は`0`で、これは機能を無効にすることを意味します。
-   [`tidb_enable_collect_execution_info`](/system-variables.md#tidb_enable_collect_execution_info) ：各オペレーターの物理実行情報を実行計画に記録するかどうかを決定します。デフォルト値は`1`です。この機能は、パフォーマンスに約3％の影響を与えます。この機能を有効にすると、次の`Plan`の情報を表示できます。

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

パフォーマンステストを実施している場合は、オペレーターの実行情報を自動的に収集する機能を無効にすることができます。

{{< copyable "" >}}

```sql
set @@tidb_enable_collect_execution_info=0;
```

`Plan`フィールドの返される結果は、 `EXPLAIN`または`EXPLAIN ANALYZE`の結果とほぼ同じ形式になります。実行プランの詳細については、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)または[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)を参照してください。

詳細については、 [TiDB固有の変数と構文](/system-variables.md)を参照してください。

## 遅いログのメモリマッピング {#memory-mapping-in-slow-log}

`INFORMATION_SCHEMA.SLOW_QUERY`テーブルをクエリすることにより、低速クエリログの内容をクエリできます。表の各列名は、低速ログの1つのフィールド名に対応しています。テーブルの構造については、 [情報スキーマ](/information-schema/information-schema-slow-query.md)の`SLOW_QUERY`テーブルの概要を参照してください。

> **ノート：**
>
> `SLOW_QUERY`のテーブルをクエリするたびに、TiDBは現在の低速クエリログを読み取って解析します。

TiDB 4.0の場合、 `SLOW_QUERY`は、ローテーションされた低速ログファイルを含む、任意の期間の低速ログのクエリをサポートします。解析する必要のある低速ログファイルを見つけるには、 `TIME`の範囲を指定する必要があります。 `TIME`の範囲を指定しない場合、TiDBは現在の低速ログファイルのみを解析します。例えば：

-   時間範囲を指定しない場合、TiDBは、TiDBが低速ログファイルに書き込んでいる低速クエリデータのみを解析します。

    {{< copyable "" >}}

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query;
    ```

    ```
    +----------+----------------------------+----------------------------+
    | count(*) | min(time)                  | max(time)                  |
    +----------+----------------------------+----------------------------+
    | 122492   | 2020-03-11 23:35:20.908574 | 2020-03-25 19:16:38.229035 |
    +----------+----------------------------+----------------------------+
    ```

-   たとえば`2020-03-10 00:00:00`の時間範囲を指定すると、 `2020-03-11 00:00:00`は最初に指定された時間範囲の低速ログファイルを検索し、次に低速クエリ情報を解析します。

    {{< copyable "" >}}

    ```sql
    select count(*),
          min(time),
          max(time)
    from slow_query
    where time > '2020-03-10 00:00:00'
      and time < '2020-03-11 00:00:00';
    ```

    ```
    +----------+----------------------------+----------------------------+
    | count(*) | min(time)                  | max(time)                  |
    +----------+----------------------------+----------------------------+
    | 2618049  | 2020-03-10 00:00:00.427138 | 2020-03-10 23:00:22.716728 |
    +----------+----------------------------+----------------------------+
    ```

> **ノート：**
>
> 指定された時間範囲の低速ログファイルが削除された場合、または低速クエリがない場合、クエリはNULLを返します。

TiDB 4.0は、すべてのTiDBノードの低速クエリ情報をクエリするために[`CLUSTER_SLOW_QUERY`](/information-schema/information-schema-slow-query.md#cluster_slow_query-table)のシステムテーブルを追加します。 `CLUSTER_SLOW_QUERY`テーブルのテーブルスキーマは、 `INSTANCE`列が`CLUSTER_SLOW_QUERY`に追加されるという点で`SLOW_QUERY`テーブルのテーブルスキーマとは異なります。 `INSTANCE`列は、低速クエリの行情報のTiDBノードアドレスを表します。 [`SLOW_QUERY`](/information-schema/information-schema-slow-query.md)と同じように`CLUSTER_SLOW_QUERY`を使用できます。

`CLUSTER_SLOW_QUERY`テーブルをクエリすると、TiDBは、他のノードからすべての低速クエリ情報を取得して1つのTiDBノードで操作を実行するのではなく、計算と判断を他のノードにプッシュします。

## <code>SLOW_QUERY</code> / <code>CLUSTER_SLOW_QUERY</code>の使用例 {#code-slow-query-code-code-cluster-slow-query-code-usage-examples}

### トップNの遅いクエリ {#top-n-slow-queries}

ユーザーの上位2つの遅いクエリをクエリします。 `Is_internal=false`は、TiDB内の遅いクエリを除外し、ユーザーの遅いクエリのみをクエリすることを意味します。

{{< copyable "" >}}

```sql
select query_time, query
from information_schema.slow_query
where is_internal = false
order by query_time desc
limit 2;
```

出力例：

```
+--------------+------------------------------------------------------------------+
| query_time   | query                                                            |
+--------------+------------------------------------------------------------------+
| 12.77583857  | select * from t_slim, t_wide where t_slim.c0=t_wide.c0;          |
|  0.734982725 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c0; |
+--------------+------------------------------------------------------------------+
```

### <code>test</code>ユーザーの上位N個の低速クエリをクエリする {#query-the-top-n-slow-queries-of-the-code-test-code-user}

次の例では、 `test`人のユーザーによって実行された低速クエリが照会され、最初の2つの結果が実行時間の逆の順序で表示されます。

{{< copyable "" >}}

```sql
select query_time, query, user
from information_schema.slow_query
where is_internal = false
  and user = "test"
order by query_time desc
limit 2;
```

出力例：

```
+-------------+------------------------------------------------------------------+----------------+
| Query_time  | query                                                            | user           |
+-------------+------------------------------------------------------------------+----------------+
| 0.676408014 | select t0.c0, t1.c1 from t_slim t0, t_wide t1 where t0.c0=t1.c1; | test           |
+-------------+------------------------------------------------------------------+----------------+
```

### 同じSQLフィンガープリントを使用して同様の低速クエリをクエリする {#query-similar-slow-queries-with-the-same-sql-fingerprints}

Top-N SQLステートメントをクエリした後、同じフィンガープリントを使用して同様の遅いクエリをクエリし続けます。

1.  Top-Nの低速クエリと対応するSQLフィンガープリントを取得します。

    {{< copyable "" >}}

    ```sql
    select query_time, query, digest
    from information_schema.slow_query
    where is_internal = false
    order by query_time desc
    limit 1;
    ```

    出力例：

    ```
    +-------------+-----------------------------+------------------------------------------------------------------+
    | query_time  | query                       | digest                                                           |
    +-------------+-----------------------------+------------------------------------------------------------------+
    | 0.302558006 | select * from t1 where a=1; | 4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa |
    +-------------+-----------------------------+------------------------------------------------------------------+
    ```

2.  フィンガープリントを使用して、同様の低速クエリをクエリします。

    {{< copyable "" >}}

    ```sql
    select query, query_time
    from information_schema.slow_query
    where digest = "4751cb6008fda383e22dacb601fde85425dc8f8cf669338d55d944bafb46a6fa";
    ```

    出力例：

    ```
    +-----------------------------+-------------+
    | query                       | query_time  |
    +-----------------------------+-------------+
    | select * from t1 where a=1; | 0.302558006 |
    | select * from t1 where a=2; | 0.401313532 |
    +-----------------------------+-------------+
    ```

## 疑似<code>stats</code>を使用して低速クエリをクエリする {#query-slow-queries-with-pseudo-code-stats-code}

{{< copyable "" >}}

```sql
select query, query_time, stats
from information_schema.slow_query
where is_internal = false
  and stats like '%pseudo%';
```

出力例：

```
+-----------------------------+-------------+---------------------------------+
| query                       | query_time  | stats                           |
+-----------------------------+-------------+---------------------------------+
| select * from t1 where a=1; | 0.302558006 | t1:pseudo                       |
| select * from t1 where a=2; | 0.401313532 | t1:pseudo                       |
| select * from t1 where a>2; | 0.602011247 | t1:pseudo                       |
| select * from t1 where a>3; | 0.50077719  | t1:pseudo                       |
| select * from t1 join t2;   | 0.931260518 | t1:407872303825682445,t2:pseudo |
+-----------------------------+-------------+---------------------------------+
```

### 実行プランが変更された低速クエリをクエリする {#query-slow-queries-whose-execution-plan-is-changed}

同じカテゴリのSQLステートメントの実行プランが変更されると、統計が古くなっているか、統計が実際のデータ分布を反映するのに十分正確でないため、実行が遅くなります。次のSQLステートメントを使用して、さまざまな実行プランでSQLステートメントをクエリできます。

{{< copyable "" >}}

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

```
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
```

次に、上記のクエリ結果のSQLフィンガープリントを使用してさまざまなプランをクエリできます。

{{< copyable "" >}}

```sql
select min(plan),
       plan_digest
from cluster_slow_query
where digest='17b4518fde82e32021877878bec2bb309619d384fca944106fcaf9c93b536e94'
group by plan_digest\G
```

出力例：

```
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
```

### クラスタの各TiDBノードの低速クエリの数をクエリする {#query-the-number-of-slow-queries-for-each-tidb-node-in-a-cluster}

{{< copyable "" >}}

```sql
select instance, count(*) from information_schema.cluster_slow_query where time >= "2020-03-06 00:00:00" and time < now() group by instance;
```

出力例：

```
+---------------+----------+
| instance      | count(*) |
+---------------+----------+
| 0.0.0.0:10081 | 124      |
| 0.0.0.0:10080 | 119771   |
+---------------+----------+
```

### 異常な期間にのみ発生する低速ログのクエリ {#query-slow-logs-occurring-only-in-abnormal-time-period}

QPSの低下や`2020-03-10 13:24:00`から`2020-03-10 13:27:00`までの期間の遅延の増加などの問題が見つかった場合は、大きなクエリが発生することが原因である可能性があります。次のSQLステートメントを実行して、異常な期間にのみ発生する低速ログをクエリします。 `2020-03-10 13:20:00`の時間範囲は、通常の期間を指し`2020-03-10 13:23:00` 。

{{< copyable "" >}}

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

```
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
```

### 他のTiDB低速ログファイルを解析する {#parse-other-tidb-slow-log-files}

TiDBは、セッション変数`tidb_slow_query_file`を使用して、 `INFORMATION_SCHEMA.SLOW_QUERY`を照会するときに読み取られて解析されるファイルを制御します。セッション変数の値を変更することにより、他の低速クエリログファイルのコンテンツをクエリできます。

{{< copyable "" >}}

```sql
set tidb_slow_query_file = "/path-to-log/tidb-slow.log"
```

### <code>pt-query-digest</code>してTiDBの低速ログを解析します {#parse-tidb-slow-logs-with-code-pt-query-digest-code}

`pt-query-digest`を使用して、TiDBの低速ログを解析します。

> **ノート：**
>
> `pt-query-digest`以降のバージョンを使用することをお勧めします。

例えば：

{{< copyable "" >}}

```shell
pt-query-digest --report tidb-slow.log
```

出力例：

```
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
```

## 問題のあるSQLステートメントを特定する {#identify-problematic-sql-statements}

`SLOW_QUERY`のステートメントすべてに問題があるわけではありません。 `process_time`が非常に大きいものだけが、クラスタ全体の圧力を高めます。

`wait_time`が非常に大きく、 `process_time`が非常に小さいステートメントは、通常、問題ありません。これは、ステートメントが実際の問題のあるステートメントによってブロックされ、実行キューで待機する必要があるためです。これにより、応答時間が大幅に長くなります。

### <code>admin show slow</code>コマンド {#code-admin-show-slow-code-command}

TiDBログファイルに加えて、 `admin show slow`コマンドを実行することで遅いクエリを特定できます。

{{< copyable "" >}}

```sql
admin show slow recent N
admin show slow top [internal | all] N
```

`recent N`は、最近のN個の低速クエリレコードを示します。次に例を示します。

{{< copyable "" >}}

```sql
admin show slow recent 10
```

`top N`は、最近（数日以内）最も遅いN個のクエリレコードを示します。 `internal`オプションが指定されている場合、返される結果はシステムによって実行される内部SQLになります。 `all`オプションが指定されている場合、返される結果は、ユーザーのSQLと内部SQLの組み合わせになります。それ以外の場合、このコマンドはユーザーのSQLから遅いクエリレコードのみを返します。

{{< copyable "" >}}

```sql
admin show slow top 3
admin show slow top internal 3
admin show slow top all 5
```

TiDBは、メモリが限られているため、限られた数の低速クエリレコードのみを保存します。 queryコマンドの値`N`がレコード数よりも大きい場合、返されるレコードの数は`N`より少なくなります。

次の表に、出力の詳細を示します。

| 列名             | 説明                                                 |
| :------------- | :------------------------------------------------- |
| 始める            | SQL実行の開始時刻                                         |
| 間隔             | SQL実行の期間                                           |
| 詳細             | SQL実行の詳細                                           |
| サク             | SQLステートメントが正常に実行されたかどうか。 `1`は成功を意味し、 `0`は失敗を意味します。 |
| conn_id        | セッションの接続ID                                         |
| transcation_ts | トランザクションコミットの`commit ts`                           |
| ユーザー           | ステートメントを実行するためのユーザー名                               |
| db             | ステートメントの実行時に関係するデータベース                             |
| table_ids      | SQLステートメントの実行時に関係するテーブルのID                         |
| index_ids      | SQLステートメントの実行時に関係するインデックスのID                       |
| 内部             | これはTiDBの内部SQLステートメントです                             |
| ダイジェスト         | SQLステートメントのフィンガープリント                               |
| sql            | 実行中または実行されたSQLステートメント                              |
