---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
---

# TiDB メモリ制御 {#tidb-memory-control}

現在、TiDB は単一の SQL クエリのメモリクォータを追跡し、メモリ使用量が特定のしきい値を超えた場合に OOM (メモリ不足) を防止したり、OOM のトラブルシューティングを行ったりするためのアクションを実行できます。システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)は、クエリがメモリ制限に達したときに実行するアクションを指定します。

-   `LOG`の値は、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達したときにクエリが引き続き実行されることを意味しますが、TiDB はログにエントリを出力します。
-   値`CANCEL`は、TiDB が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達した直後に SQL クエリの実行を停止し、クライアントにエラーを返すことを意味します。エラー情報には、SQL 実行プロセスでメモリを消費する各物理実行演算子のメモリ使用量が明確に示されます。

## クエリのメモリクォータを構成する {#configure-the-memory-quota-of-a-query}

システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)は、クエリの制限をバイト単位で設定します。いくつかの使用例:

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8GB:
SET tidb_mem_quota_query = 8 << 30;
```

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8MB:
SET tidb_mem_quota_query = 8 << 20;
```

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8KB:
SET tidb_mem_quota_query = 8 << 10;
```

## tidb-server インスタンスのメモリ使用量のしきい値を構成する {#configure-the-memory-usage-threshold-of-a-tidb-server-instance}

v6.5.0 以降、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用して、tidb-server インスタンスのメモリ使用量のしきい値を設定できます。

たとえば、tidb-server インスタンスの合計メモリ使用量を 32 GB に設定します。

```sql
SET GLOBAL tidb_server_memory_limit = "32GB";
```

この変数を設定した後、tidb-server インスタンスのメモリ使用量が 32 GB に達すると、TiDB は、インスタンスのメモリ使用量が 32 GB を下回るまで、実行中のすべての SQL 操作の中でメモリ使用量が最大の SQL 操作を順番に終了します。 .強制終了した SQL 操作は、クライアントに`Out Of Memory Quota!`エラーを返します。

現在、 `tidb_server_memory_limit`で設定されたメモリ制限は、次の SQL 操作を終了**しません**。

-   DDL 操作
-   INSERT、UPDATE、および DELETE 操作
-   ウィンドウ関数と共通テーブル式を含む SQL 操作

> **警告：**
>
> -   起動プロセス中、TiDB は[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)制限が適用されることを保証しません。オペレーティング システムの空きメモリが不十分な場合でも、TiDB で OOM が発生する可能性があります。 TiDB インスタンスに十分な利用可能なメモリがあることを確認する必要があります。
> -   メモリ制御の過程で、TiDB の合計メモリ使用量が`tidb_server_memory_limit`で設定された制限をわずかに超える場合があります。
> -   v6.5.0 以降、設定項目`server-memory-quota`は廃止されました。互換性を確保するために、クラスターを v6.5.0 以降のバージョンにアップグレードした後、 `tidb_server_memory_limit` `server-memory-quota`の値を継承します。アップグレード前に`server-memory-quota`を設定していない場合、デフォルト値の`tidb_server_memory_limit`が使用されます。これは`80%`です。

tidb-server インスタンスのメモリ使用量が総メモリの特定の割合に達すると (割合はシステム変数[`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)によって制御されます)、tidb-server はGolang GC をトリガーしてメモリストレスを軽減しようとします。インスタンスのメモリがしきい値付近で変動するためにパフォーマンスの問題を引き起こす頻繁な GC を回避するために、この GC メソッドは GC を最大でも 1 分に 1 回トリガーします。

## INFORMATION_SCHEMA システム テーブルを使用して、現在の tidb-server インスタンスのメモリ使用量をビュー。 {#view-the-memory-usage-of-the-current-tidb-server-instance-using-the-information-schema-system-table}

現在のインスタンスまたはクラスターのメモリ使用量を表示するには、システム テーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)にクエリを実行できます。

現在のインスタンスまたはクラスターのメモリ関連の操作と実行ベースを表示するには、システム テーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)にクエリを実行できます。インスタンスごとに、このテーブルには最新の 50 レコードが保持されます。

## 過剰なメモリ使用量のアラームをトリガーする {#trigger-the-alarm-of-excessive-memory-usage}

tidb-server インスタンスのメモリ使用量がメモリのしきい値 (デフォルトでは総メモリの 70%) を超え、次の条件のいずれかが満たされると、TiDB は関連するステータス ファイルを記録し、アラーム ログを出力。

-   メモリ使用量がメモリのしきい値を超えるのは初めてです。
-   メモリ使用量がメモリのしきい値を超えており、最後のアラームから 60 秒以上経過しています。
-   メモリ使用量がメモリしきい値および`(Current memory usage - Memory usage at the last alarm) / Total memory > 10%`を超えています。

システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)を介してメモリ使用率を変更することにより、アラームをトリガーするメモリしきい値を制御できます。

過剰なメモリ使用量のアラームがトリガーされると、TiDB は次のアクションを実行します。

-   TiDB は、TiDB ログ ファイル[`filename`](/tidb-configuration-file.md#filename)があるディレクトリに次の情報を記録します。

    -   現在実行されているすべての SQL ステートメントの中で、メモリ使用量が最も多い上位 10 個の SQL ステートメントと、実行時間が最も長い上位 10 個の SQL ステートメントに関する情報
    -   ゴルーチンスタック情報
    -   ヒープメモリの使用状況

-   TiDB は、キーワード`tidb-server has the risk of OOM`と次のメモリ関連のシステム変数の値を含むアラーム ログを出力。

    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)
    -   [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)
    -   [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)

アラーム用のステータス ファイルが蓄積しすぎるのを避けるために、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この数は、システム変数[`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)を構成することで調整できます。

次の例では、アラームをトリガーするメモリ集約型の SQL ステートメントを作成します。

1.  `tidb_memory_usage_alarm_ratio` ～ `0.85`を設定:

    {{< copyable "" >}}

    ```sql
    SET GLOBAL tidb_memory_usage_alarm_ratio = 0.85;
    ```

2.  `CREATE TABLE t(a int);`を実行し、1000 行のデータを挿入します。

3.  `select * from t t1 join t t2 join t t3 order by t1.a`を実行します。この SQL ステートメントは 10 億件のレコードを出力します。これは大量のメモリを消費するため、アラームがトリガーされます。

4.  合計システムメモリ、現在のシステムメモリ使用量、tidb-server インスタンスのメモリ使用量、およびステータス ファイルのディレクトリを記録する`tidb.log`ファイルを確認します。

    ```
    [2022/10/11 16:39:02.281 +08:00] [WARN] [memoryusagealarm.go:212] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=33682427904] ["system memory usage"=22120655360] ["tidb-server memory usage"=21468556992] [memory-usage-alarm-ratio=0.85] ["record path"=/tiup/deploy/tidb-4000/log/oom_record]
    ```

    上記のログ ファイルの例のフィールドは、次のように説明されています。

    -   `is tidb_server_memory_limit set` [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)設定されているかどうかを示します。
    -   `system memory total`現在のシステムの合計メモリを示します。
    -   `system memory usage`現在のシステムメモリ使用量を示します。
    -   `tidb-server memory usage` tidb-server インスタンスのメモリ使用量を示します。
    -   `memory-usage-alarm-ratio`システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)の値を示します。
    -   `record path`ステータス ファイルのディレクトリを示します。

5.  ステータス ファイルのディレクトリを確認すると (前の例では、ディレクトリは`/tiup/deploy/tidb-4000/log/oom_record`です)、対応するタイムスタンプ (たとえば、 `record2022-10-09T17:18:38+08:00` ) を持つレコード ディレクトリを確認できます。レコード ディレクトリには、 `goroutinue` 、 `heap` 、および`running_sql`の 3 つのファイルが含まれます。これら 3 つのファイルの末尾には、ステータス ファイルがログに記録された時刻が付けられます。これらは、アラームがトリガーされたときに、ゴルーチン スタック情報、ヒープメモリの使用状況、および実行中の SQL 情報をそれぞれ記録します。 `running_sql`の内容は[`expensive-queries`](/identify-expensive-queries.md)を参照。

## tidb-server のその他のメモリ制御動作 {#other-memory-control-behaviors-of-tidb-server}

### フロー制御 {#flow-control}

-   TiDB は、データを読み取るオペレーターの動的メモリ制御をサポートしています。デフォルトでは、このオペレーターは、データの読み取りを許可する[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の最大数を使用します。 1 回の SQL 実行のメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターは 1 つのスレッドを停止します。

-   このフロー制御動作は、システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)によって制御されます。

-   フロー制御動作がトリガーされると、TiDB はキーワード`memory exceeds quota, destroy one token now`を含むログを出力します。

### ディスクこぼれ {#disk-spill}

TiDB は、実行オペレーターのディスクスピルをサポートしています。 SQL 実行のメモリ使用量がメモリクォータを超えると、tidb-server は実行オペレータの中間データをディスクにスピルして、メモリの負荷を軽減することができます。ディスク スピルをサポートする演算子には、Sort、MergeJoin、HashJoin、HashAgg などがあります。

-   ディスク スピルの動作は、パラメータ[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) 、 [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path) 、および[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota)によって共同で制御されます。
-   ディスク スピルがトリガーされると、TiDB はキーワード`memory exceeds quota, spill to disk now`または`memory exceeds quota, set aggregate mode to spill-mode`を含むログを出力します。
-   Sort、MergeJoin、および HashJoin オペレーターのディスク スピルは v4.0.0 で導入されました。 HashAgg オペレーターのディスク スピルは v5.2.0 で導入されました。
-   Sort、MergeJoin、または HashJoin を含む SQL 実行によって OOM が発生すると、TiDB はデフォルトでディスク スピルをトリガーします。 HashAgg を含む SQL 実行によって OOM が発生した場合、TiDB はデフォルトでディスク スピルをトリガーしません。システム変数`tidb_executor_concurrency = 1`を構成して、HashAgg のディスク スピルをトリガーできます。

> **ノート：**
>
> HashAgg のディスク スピルは、 `DISTINCT`集計関数を含む SQL 実行をサポートしていません。 `DISTINCT`集計関数を含む SQL の実行で大量のメモリが使用される場合、ディスク スピルは適用されません。

次の例では、メモリを消費する SQL ステートメントを使用して、HashAgg のディスク スピル機能を示します。

1.  SQL ステートメントのメモリクォータを 1 GB (既定では 1 GB) に構成します。

    {{< copyable "" >}}

    ```sql
    SET tidb_mem_quota_query = 1 << 30;
    ```

2.  1 つのテーブル`CREATE TABLE t(a int);`を作成し、256 行の異なるデータを挿入します。

3.  次の SQL ステートメントを実行します。

    {{< copyable "" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    この SQL ステートメントを実行すると大量のメモリが占有されるため、次の「メモリ クォータが不足しています」というエラー メッセージが返されます。

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4.  システム変数を`tidb_executor_concurrency`から 1 に構成します。この構成では、メモリ不足になると、HashAgg は自動的にディスク スピルをトリガーしようとします。

    {{< copyable "" >}}

    ```sql
    SET tidb_executor_concurrency = 1;
    ```

5.  同じ SQL ステートメントを実行します。今回は、ステートメントが正常に実行され、エラー メッセージが返されていないことがわかります。次の詳細な実行計画から、HashAgg が 600 MB のハード ディスク領域を使用したことがわかります。

    {{< copyable "" >}}

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

### <code>GOMEMLIMIT</code>を構成して OOM の問題を軽減する {#mitigate-oom-issues-by-configuring-code-gomemlimit-code}

GO 1.19 では、GC をトリガーするメモリ制限を設定する環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)が導入されています。

v6.1.3 &lt;= TiDB &lt; v6.5.0 の場合、手動で`GOMEMLIMIT`を設定することにより、OOM の問題の典型的なカテゴリを軽減できます。 OOM の問題の典型的なカテゴリは次のとおりです。次の図に示すように、OOM が発生する前に、Grafana で使用中の推定メモリがメモリ全体の半分しか占めていません (TiDB ランタイム &gt; メモリ使用量 &gt; 推定使用中)。

![normal OOM case example](/media/configure-memory-usage-oom-example.png)

`GOMEMLIMIT`のパフォーマンスを検証するために、特定のメモリ使用量を構成ありと`GOMEMLIMIT`なしで比較するテストが実行されます。

-   TiDB v6.1.2 では、シミュレートされたワークロードが数分間実行された後、TiDBサーバーで OOM (システムメモリ: 約 48 GiB) が発生します。

    ![v6.1.2 workload oom](/media/configure-memory-usage-612-oom.png)

-   TiDB v6.1.3 では、 `GOMEMLIMIT`は 40000 MiB に設定されます。シミュレートされたワークロードは長時間安定して動作し、TiDBサーバーで OOM は発生せず、プロセスの最大メモリ使用量は約 40.8 GiB で安定していることがわかりました。

    ![v6.1.3 workload no oom with GOMEMLIMIT](/media/configure-memory-usage-613-no-oom.png)
