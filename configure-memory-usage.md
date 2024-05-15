---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
---

# TiDB メモリ制御 {#tidb-memory-control}

現在、TiDB は単一の SQL クエリのメモリクォータを追跡し、メモリ使用量が特定のしきい値を超えた場合に OOM (メモリ不足) を防止したり、OOM のトラブルシューティングを行うためのアクションを実行できます。システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) 、クエリがメモリ制限に達したときに実行するアクションを指定します。

-   値が`LOG`の場合、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達したときにクエリは引き続き実行されますが、TiDB はログにエントリを出力します。
-   値が`CANCEL`の場合、TiDB は[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達するとすぐに SQL クエリの実行を停止し、クライアントにエラーを返します。エラー情報には、SQL 実行プロセスでメモリを消費する各物理実行演算子のメモリ使用量が明確に表示されます。

## クエリのメモリクォータを設定する {#configure-the-memory-quota-of-a-query}

システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)クエリの制限をバイト単位で設定します。使用例をいくつか示します。

```sql
-- Set the threshold value of memory quota for a single SQL query to 8GB:
SET tidb_mem_quota_query = 8 << 30;
```

```sql
-- Set the threshold value of memory quota for a single SQL query to 8MB:
SET tidb_mem_quota_query = 8 << 20;
```

```sql
-- Set the threshold value of memory quota for a single SQL query to 8KB:
SET tidb_mem_quota_query = 8 << 10;
```

## tidb-serverインスタンスのメモリ使用量しきい値を設定する {#configure-the-memory-usage-threshold-of-a-tidb-server-instance}

v6.5.0 以降では、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用して、tidb-server インスタンスのメモリ使用量のしきい値を設定できます。

たとえば、tidb-server インスタンスの合計メモリ使用量を 32 GB に設定します。

```sql
SET GLOBAL tidb_server_memory_limit = "32GB";
```

この変数を設定すると、tidb-server インスタンスのメモリ使用量が 32 GB に達すると、TiDB は、インスタンスのメモリ使用量が 32 GB を下回るまで、実行中のすべての SQL 操作の中でメモリ使用量が最も大きい SQL 操作を順番に終了します。強制終了された SQL 操作は、クライアントに`Out Of Memory Quota!`エラーを返します。

現在、 `tidb_server_memory_limit`で設定されたメモリ制限では、次の SQL 操作は終了し**ません**。

-   DDL操作
-   ウィンドウ関数と共通テーブル式を含むSQL操作

> **警告：**
>
> -   起動プロセス中、TiDB は[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)制限が適用されることを保証しません。オペレーティング システムの空きメモリが不足している場合、TiDB は依然として OOM に遭遇する可能性があります。TiDB インスタンスに十分な使用可能メモリがあることを確認する必要があります。
> -   メモリ制御の過程で、TiDB の合計メモリ使用量が`tidb_server_memory_limit`で設定された制限をわずかに超える場合があります。
> -   v6.5.0 以降、構成項目`server-memory-quota`は非推奨です。互換性を確保するために、クラスターを v6.5.0 以降のバージョンにアップグレードすると、 `tidb_server_memory_limit` `server-memory-quota`の値を継承します。アップグレード前に`server-memory-quota`構成していない場合は、デフォルト値`tidb_server_memory_limit` 、つまり`80%`が使用されます。

tidb-server インスタンスのメモリ使用量が総メモリの特定の割合 (割合はシステム変数[`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)によって制御されます) に達すると、tidb-server はメモリのストレスを軽減するためにGolang GC をトリガーしようとします。インスタンスメモリがしきい値付近で変動することでパフォーマンスの問題を引き起こす頻繁な GC を回避するために、この GC メソッドは最大で 1 分に 1 回 GC をトリガーします。

> **注記：**
>
> ハイブリッド展開シナリオでは、物理マシン全体の合計メモリしきい値ではなく、単一の tidb-server インスタンスのメモリ使用量しきい値が`tidb_server_memory_limit`なります。

## INFORMATION_SCHEMA システム テーブルを使用して、現在の tidb-server インスタンスのメモリ使用量をビュー。 {#view-the-memory-usage-of-the-current-tidb-server-instance-using-the-information-schema-system-table}

現在のインスタンスまたはクラスターのメモリ使用量を表示するには、システム テーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)をクエリします。

現在のインスタンスまたはクラスターのメモリ関連の操作と実行基準を表示するには、システム テーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)をクエリします。このテーブルには、インスタンスごとに最新の 50 件のレコードが保持されます。

## 過剰なメモリ使用量の警告を発する {#trigger-the-alarm-of-excessive-memory-usage}

tidb-server インスタンスのメモリ使用量がメモリしきい値 (デフォルトでは合計メモリの 70%) を超え、次のいずれかの条件が満たされると、TiDB は関連するステータス ファイルを記録し、アラーム ログを出力。

-   メモリ使用量がメモリしきい値を超えるのは初めてです。
-   メモリ使用量がメモリしきい値を超えており、前回のアラームから 60 秒以上経過しています。
-   メモリ使用量がメモリしきい値を超え、 `(Current memory usage - Memory usage at the last alarm) / Total memory > 10%` 。

システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)を介してメモリ使用率を変更することで、アラームをトリガーするメモリしきい値を制御できます。

過剰なメモリ使用量のアラームがトリガーされると、TiDB は次のアクションを実行します。

-   TiDB は、TiDB ログ ファイル[`filename`](/tidb-configuration-file.md#filename)が配置されているディレクトリに次の情報を記録します。

    -   現在実行中のすべてのSQL文のうち、メモリ使用量が最も多い上位10個のSQL文と実行時間が最も長い上位10個のSQL文に関する情報
    -   ゴルーチンスタック情報
    -   ヒープメモリの使用状況

-   TiDB は、キーワード`tidb-server has the risk of OOM`と次のメモリ関連のシステム変数の値を含むアラーム ログを出力。

    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)
    -   [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)
    -   [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)

アラームのステータス ファイルが蓄積されすぎないようにするため、TiDB はデフォルトで、最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この数は、システム変数[`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)を構成することで調整できます。

次の例では、アラームをトリガーするメモリを大量に消費する SQL ステートメントを構築します。

1.  セット`tidb_memory_usage_alarm_ratio` ～ `0.85` :

    ```sql
    SET GLOBAL tidb_memory_usage_alarm_ratio = 0.85;
    ```

2.  `CREATE TABLE t(a int);`を実行し、1000 行のデータを挿入します。

3.  `select * from t t1 join t t2 join t t3 order by t1.a`実行します。この SQL ステートメントは 10 億件のレコードを出力し、大量のメモリを消費するため、アラームがトリガーされます。

4.  システムメモリの合計、現在のシステムメモリ使用量、tidb-server インスタンスのメモリ使用量、およびステータス ファイルのディレクトリを記録する`tidb.log`ファイルを確認します。

        [2022/10/11 16:39:02.281 +08:00] [WARN] [memoryusagealarm.go:212] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=33682427904] ["system memory usage"=22120655360] ["tidb-server memory usage"=21468556992] [memory-usage-alarm-ratio=0.85] ["record path"=/tiup/deploy/tidb-4000/log/oom_record]

    上記のサンプル ログ ファイルのフィールドは次のように説明されています。

    -   `is tidb_server_memory_limit set` [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)が設定されているかどうかを示します。
    -   `system memory total`現在のシステムの合計メモリを示します。
    -   `system memory usage`現在のシステムメモリ使用量を示します。
    -   `tidb-server memory usage` tidb-server インスタンスのメモリ使用量を示します。
    -   `memory-usage-alarm-ratio`システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)の値を示します。
    -   `record path`ステータス ファイルのディレクトリを示します。

5.  ステータス ファイルのディレクトリを確認すると (上記の例ではディレクトリは`/tiup/deploy/tidb-4000/log/oom_record` )、対応するタイムスタンプ (たとえば`record2022-10-09T17:18:38+08:00` ) を持つレコード ディレクトリが表示されます。レコード ディレクトリには、 `goroutinue` 、 `heap` 、 `running_sql` 3 つのファイルが含まれています。これらの 3 つのファイルには、ステータス ファイルが記録された時刻が末尾に付けられています。それぞれ、ゴルーチン スタック情報、ヒープメモリの使用状況、アラームがトリガーされたときに実行されている SQL 情報が記録されます。 `running_sql`の内容については、 [`expensive-queries`](/identify-expensive-queries.md)を参照してください。

## tidb-server のその他のメモリ制御動作 {#other-memory-control-behaviors-of-tidb-server}

### フロー制御 {#flow-control}

-   TiDB は、データを読み取る演算子の動的メモリ制御をサポートしています。デフォルトでは、この演算子は、データの読み取りに許可される最大数のスレッドを使用します。1 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の SQL 実行のメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取る演算子は 1 つのスレッドを停止します。

-   このフロー制御動作はシステム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)によって制御されます。

-   フロー制御動作がトリガーされると、TiDB はキーワード`memory exceeds quota, destroy one token now`含むログを出力します。

### ディスク流出 {#disk-spill}

TiDB は、実行演算子のディスク スピルをサポートしています。SQL 実行のメモリ使用量がメモリクォータを超えると、tidb-server は実行演算子の中間データをディスクにスピルして、メモリ負荷を軽減できます。ディスク スピルをサポートする演算子には、Sort、MergeJoin、HashJoin、および HashAgg があります。

-   ディスクスピル動作は、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) 、 [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path) 、および[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota)のパラメータによって共同で制御されます。
-   ディスク スピルがトリガーされると、TiDB はキーワード`memory exceeds quota, spill to disk now`または`memory exceeds quota, set aggregate mode to spill-mode`を含むログを出力します。
-   Sort、MergeJoin、および HashJoin 演算子のディスク スピルは v4.0.0 で導入され、HashAgg 演算子のディスク スピルは v5.2.0 で導入されました。
-   Sort、MergeJoin、または HashJoin を含む SQL 実行によって OOM が発生すると、TiDB はデフォルトでディスク スピルをトリガーします。HashAgg を含む SQL 実行によって OOM が発生すると、TiDB はデフォルトでディスク スピルをトリガーしません。システム変数`tidb_executor_concurrency = 1`を設定すると、HashAgg のディスク スピルをトリガーできます。

> **注記：**
>
> HashAgg のディスク スピルは、 `DISTINCT`集計関数を含む SQL 実行をサポートしていません。3 `DISTINCT`集計関数を含む SQL 実行でメモリが多すぎる場合、ディスク スピルは適用されません。

次の例では、メモリを消費する SQL ステートメントを使用して、HashAgg のディスク スピル機能を示します。

1.  SQL ステートメントのメモリクォータを 1 GB (デフォルトは 1 GB) に設定します。

    ```sql
    SET tidb_mem_quota_query = 1 << 30;
    ```

2.  単一のテーブル`CREATE TABLE t(a int);`を作成し、256 行の異なるデータを挿入します。

3.  次の SQL ステートメントを実行します。

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    この SQL ステートメントを実行するとメモリが大量に消費されるため、次の「メモリ クォータ不足」エラー メッセージが返されます。

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4.  システム変数`tidb_executor_concurrency`を 1 に設定します。この設定では、メモリ不足になると、HashAgg は自動的にディスク スピルをトリガーしようとします。

    ```sql
    SET tidb_executor_concurrency = 1;
    ```

5.  同じ SQL ステートメントを実行します。今回はステートメントが正常に実行され、エラー メッセージは返されないことがわかります。次の詳細な実行プランから、HashAgg が 600 MB のハード ディスク領域を使用したことがわかります。

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    ```sql
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | id                              | estRows     | actRows  | task      | access object | execution info                                                                                                                                                      | operator info                                                   | memory    | disk     |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | HashAgg_11                      | 204.80      | 16777216 | root      |               | time:1m37.4s, loops:16385                                                                                                                                           | group by:test.t.a, test.t.a, test.t.a, funcs:count(1)->Column#7 | 1.13 GB   | 600.0 MB |
    | └─HashJoin_12                   | 16777216.00 | 16777216 | root      |               | time:21.5s, loops:16385, build_hash_table:{total:267.2µs, fetch:228.9µs, build:38.2µs}, probe:{concurrency:1, total:35s, max:35s, probe:35s, fetch:962.2µs}         | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |   ├─TableReader_21(Build)       | 256.00      | 256      | root      |               | time:87.2µs, loops:2, cop_task: {num: 1, max: 150µs, proc_keys: 0, rpc_num: 1, rpc_time: 145.1µs, copr_cache_hit_ratio: 0.00}                                       | data:TableFullScan_20                                           | 885 Bytes | N/A      |
    |   │ └─TableFullScan_20          | 256.00      | 256      | cop[tikv] | table:t3      | tikv_task:{time:23.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |   └─HashJoin_14(Probe)          | 65536.00    | 65536    | root      |               | time:728.1µs, loops:65, build_hash_table:{total:307.5µs, fetch:277.6µs, build:29.9µs}, probe:{concurrency:1, total:34.3s, max:34.3s, probe:34.3s, fetch:278µs}      | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |     ├─TableReader_19(Build)     | 256.00      | 256      | root      |               | time:126.2µs, loops:2, cop_task: {num: 1, max: 308.4µs, proc_keys: 0, rpc_num: 1, rpc_time: 295.3µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_18                                           | 885 Bytes | N/A      |
    |     │ └─TableFullScan_18        | 256.00      | 256      | cop[tikv] | table:t2      | tikv_task:{time:79.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |     └─TableReader_17(Probe)     | 256.00      | 256      | root      |               | time:211.1µs, loops:2, cop_task: {num: 1, max: 295.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 279.7µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_16                                           | 885 Bytes | N/A      |
    |       └─TableFullScan_16        | 256.00      | 256      | cop[tikv] | table:t1      | tikv_task:{time:71.4µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    9 rows in set (1 min 37.428 sec)
    ```

## その他 {#others}

### <code>GOMEMLIMIT</code>を設定してOOMの問題を軽減する {#mitigate-oom-issues-by-configuring-code-gomemlimit-code}

GO 1.19 では、GC をトリガーするメモリ制限を設定するための環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入されています。

v6.1.3 &lt;= TiDB &lt; v6.5.0 の場合、手動で`GOMEMLIMIT`を設定することで、OOM 問題の一般的なカテゴリを軽減できます。OOM 問題の一般的なカテゴリは、OOM が発生する前に、Grafana で使用されていると推定されるメモリがメモリ全体の半分しか占めないことです (TiDB-Runtime &gt; Memory Usage &gt; Estimation-inuse)。次の図を参照してください。

![normal OOM case example](/media/configure-memory-usage-oom-example.png)

`GOMEMLIMIT`のパフォーマンスを確認するために、 `GOMEMLIMIT`構成の有無による特定のメモリ使用量を比較するテストを実行します。

-   TiDB v6.1.2 では、シミュレートされたワークロードが数分間実行された後、TiDBサーバーはOOM (システムメモリ: 約 48 GiB) に遭遇します。

    ![v6.1.2 workload oom](/media/configure-memory-usage-612-oom.png)

-   TiDB v6.1.3 では、 `GOMEMLIMIT` 40000 MiB に設定されています。シミュレートされたワークロードは長時間安定して実行され、TiDBサーバーで OOM は発生せず、プロセスの最大メモリ使用量は 40.8 GiB 前後で安定していることがわかります。

    ![v6.1.3 workload no oom with GOMEMLIMIT](/media/configure-memory-usage-613-no-oom.png)
