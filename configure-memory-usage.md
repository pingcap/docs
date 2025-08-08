---
title: TiDB Memory Control
summary: クエリのメモリクォータを構成して OOM (メモリ不足) を回避する方法を学習します。
---

# TiDB メモリ制御 {#tidb-memory-control}

現在、TiDBは単一のSQLクエリのメモリクォータを追跡し、メモリ使用量が特定のしきい値を超えた場合に、OOM（メモリ不足）を防止したり、OOMのトラブルシューティングを行うためのアクションを実行できます。システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610) 、クエリがメモリ制限に達した場合に実行するアクションを指定します。

-   値が`LOG`の場合、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達したときにクエリは引き続き実行されますが、TiDB はログにエントリを出力します。
-   値が`CANCEL`の場合、TiDBは[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達した直後にSQLクエリの実行を停止し、クライアントにエラーを返します。エラー情報には、SQL実行プロセスでメモリを消費する各物理実行演算子のメモリ使用量が明確に表示されます。

## クエリのメモリクォータを設定する {#configure-the-memory-quota-of-a-query}

システム変数[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、クエリの制限をバイト単位で設定します。使用例：

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

## tidb-server インスタンスのメモリ使用量しきい値を構成する {#configure-the-memory-usage-threshold-of-a-tidb-server-instance}

v6.5.0 以降では、システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用して、tidb-server インスタンスのメモリ使用量のしきい値を設定できます。

たとえば、tidb-server インスタンスの合計メモリ使用量を 32 GB に設定します。

```sql
SET GLOBAL tidb_server_memory_limit = "32GB";
```

この変数を設定すると、tidb-server インスタンスのメモリ使用量が 32 GB に達すると、TiDB は実行中のすべての SQL 操作のうち、メモリ使用量が最も大きい SQL 操作を順に終了し、インスタンスのメモリ使用量が 32 GB を下回るまで実行を続けます。強制終了された SQL 操作は、クライアントにエラー`Out Of Memory Quota!`を返します。

現在、 `tidb_server_memory_limit`で設定されたメモリ制限では、次の SQL 操作は終了し**ません**。

-   DDL操作
-   ウィンドウ関数と共通テーブル式を含むSQL操作

> **警告：**
>
> -   TiDBは起動プロセス中に[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)制限が確実に適用されるとは保証しません。オペレーティングシステムの空きメモリが不足している場合、TiDBは依然としてOOMが発生する可能性があります。TiDBインスタンスに十分な空きメモリがあることを確認する必要があります。
> -   メモリ制御の過程で、TiDB の合計メモリ使用量が`tidb_server_memory_limit`で設定された制限をわずかに超える場合があります。
> -   バージョン6.5.0以降、設定項目`server-memory-quota`非推奨となりました。互換性を確保するため、クラスターをバージョン6.5.0以降にアップグレードすると、 `tidb_server_memory_limit` `server-memory-quota`の値を継承します。アップグレード前に`server-memory-quota`を設定していない場合は、デフォルト値`tidb_server_memory_limit` （ `80%`が使用されます。

tidb-server インスタンスのメモリ使用量が総メモリの一定割合（割合はシステム変数[`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)によって制御されます）に達すると、tidb-server はメモリ負荷を軽減するためにGolang GC をトリガーしようとします。インスタンスメモリがしきい値付近で変動することで頻繁な GC が発生し、パフォーマンスに問題が生じるのを防ぐため、この GC 方式では GC は最大で 1 分に 1 回しかトリガーされません。

> **注記：**
>
> ハイブリッド展開シナリオでは、物理マシン全体の合計メモリしきい値ではなく、単一の tidb-server インスタンスのメモリ使用量しきい値は`tidb_server_memory_limit`なります。

## INFORMATION_SCHEMA システム テーブルを使用して、現在の tidb-server インスタンスのメモリ使用量をビュー。 {#view-the-memory-usage-of-the-current-tidb-server-instance-using-the-information-schema-system-table}

現在のインスタンスまたはクラスターのメモリ使用量を表示するには、システム テーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)クエリします。

現在のインスタンスまたはクラスターのメモリ関連の操作と実行基準を確認するには、システムテーブル[`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)クエリします。このテーブルには、インスタンスごとに最新の50件のレコードが保持されます。

## 過剰なメモリ使用量のアラームをトリガーする {#trigger-the-alarm-of-excessive-memory-usage}

tidb-server インスタンスのメモリ使用量がメモリしきい値 (デフォルトでは合計メモリの 70%) を超え、次のいずれかの条件が満たされると、TiDB は関連するステータス ファイルを記録し、アラーム ログを出力。

-   メモリ使用量がメモリしきい値を超えるのは初めてです。
-   メモリ使用量がメモリしきい値を超えており、前回のアラームから 60 秒以上経過しています。
-   メモリ使用量がメモリしきい値を超え、 `(Current memory usage - Memory usage at the last alarm) / Total memory > 10%` 。

システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)を使用してメモリ使用率を変更することで、アラームをトリガーするメモリしきい値を制御できます。

過剰なメモリ使用量のアラームがトリガーされると、TiDB は次のアクションを実行します。

-   TiDB は、TiDB ログ ファイル[`filename`](/tidb-configuration-file.md#filename)が配置されているディレクトリに次の情報を記録します。

    -   現在実行中のすべてのSQL文の中で、メモリ使用量が最も多い上位10個のSQL文と実行時間が最も長い上位10個のSQL文に関する情報
    -   ゴルーチンスタック情報
    -   ヒープメモリの使用状況

-   TiDB は、キーワード`tidb-server has the risk of OOM`と次のメモリ関連のシステム変数の値を含むアラーム ログを出力。

    -   [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)
    -   [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    -   [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)
    -   [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-new-in-v510)
    -   [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)

アラームのステータスファイルが過度に蓄積されるのを防ぐため、TiDBはデフォルトで、直近5回のアラーム中に生成されたステータスファイルのみを保持します。この数は、システム変数[`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)設定することで調整できます。

次の例では、アラームをトリガーするメモリを大量に消費する SQL ステートメントを構築します。

1.  セット`tidb_memory_usage_alarm_ratio` ～ `0.85` :

    ```sql
    SET GLOBAL tidb_memory_usage_alarm_ratio = 0.85;
    ```

2.  `CREATE TABLE t(a int);`を実行し、1000 行のデータを挿入します。

3.  `select * from t t1 join t t2 join t t3 order by t1.a`実行します。この SQL 文は 10 億件のレコードを出力し、大量のメモリを消費するため、アラームがトリガーされます。

4.  システムメモリの合計、現在のシステムメモリ使用量、tidb-server インスタンスのメモリ使用量、およびステータス ファイルのディレクトリを記録する`tidb.log`ファイルを確認します。

        [2022/10/11 16:39:02.281 +08:00] [WARN] [memoryusagealarm.go:212] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=33682427904] ["system memory usage"=22120655360] ["tidb-server memory usage"=21468556992] [memory-usage-alarm-ratio=0.85] ["record path"=/tiup/deploy/tidb-4000/log/oom_record]

    上記のサンプル ログ ファイルのフィールドは次のように説明されています。

    -   `is tidb_server_memory_limit set` [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)が設定されているかどうかを示します。
    -   `system memory total`現在のシステムの合計メモリを示します。
    -   `system memory usage`現在のシステムメモリ使用量を示します。
    -   `tidb-server memory usage` 、tidb-server インスタンスのメモリ使用量を示します。
    -   `memory-usage-alarm-ratio`システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)の値を示します。
    -   `record path`ステータス ファイルのディレクトリを示します。

5.  ステータスファイルのディレクトリ（上記の例ではディレクトリ`/tiup/deploy/tidb-4000/log/oom_record` ）を確認すると、対応するタイムスタンプ（例： `record2022-10-09T17:18:38+08:00` ）を持つレコードディレクトリが表示されます。レコードディレクトリには、 `goroutinue` 、 `heap` 、 `running_sql`の3つのファイルが含まれています。これらの3つのファイルには、ステータスファイルが記録された時刻が末尾に付加されます。これらのファイルには、それぞれ、ゴルーチンのスタック情報、ヒープメモリの使用状況、アラーム発生時の実行SQL情報が記録されています。 `running_sql`の内容については、 [`expensive-queries`](/identify-expensive-queries.md)を参照してください。

## tidb-server の書き込みトランザクションのメモリ使用量を削減します {#reduce-the-memory-usage-for-write-transactions-in-tidb-server}

TiDBが使用するトランザクションモデルでは、トランザクションのすべての書き込み操作はコミットされる前にメモリにキャッシュされる必要があります。TiDBが大規模なトランザクションを書き込む場合、メモリ使用量が増加し、ボトルネックになる可能性があります。様々な制約下で大規模トランザクションによるメモリ使用量の増加を軽減または回避するには、システム変数[`tidb_dml_type`](/system-variables.md#tidb_dml_type-new-in-v800) `"bulk"`に調整するか、 [非トランザクションDMLステートメント](/non-transactional-dml.md)使用します。

## tidb-serverのその他のメモリ制御動作 {#other-memory-control-behaviors-of-tidb-server}

### フロー制御 {#flow-control}

-   TiDBは、データ読み取り演算子の動的メモリ制御をサポートしています。デフォルトでは、この演算子はデータ読み取りに使用できる最大スレッド数を使用します。1 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)のSQL実行でメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)超えると、データ読み取り演算子は1つのスレッドを停止します。

-   このフロー制御動作は、システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)によって制御されます。

-   フロー制御動作がトリガーされると、TiDB はキーワード`memory exceeds quota, destroy one token now`を含むログを出力します。

### ディスクスピル {#disk-spill}

TiDBは、実行演算子のディスクへの書き込みをサポートしています。SQL実行のメモリ使用量がメモリクォータを超えた場合、tidb-serverは実行演算子の中間データをディスクに書き出すことで、メモリ負荷を軽減します。ディスクへの書き込みをサポートする演算子には、Sort、MergeJoin、HashJoin、HashAggなどがあります。

-   ディスクスピル動作は、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、 [`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom) 、 [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path) 、および[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota)パラメータによって共同で制御されます。
-   ディスク スピルがトリガーされると、TiDB はキーワード`memory exceeds quota, spill to disk now`または`memory exceeds quota, set aggregate mode to spill-mode`含むログを出力します。
-   Sort、MergeJoin、およびHashJoin演算子のディスクスピルはv4.0.0で導入されました。HashAgg演算子の非並列アルゴリズムのディスクスピルはv5.2.0で導入されました。HashAgg演算子の並列アルゴリズムのディスクスピルはv8.0.0で実験的機能として導入され、v8.2.0で一般提供（GA）されました。TopN演算子のディスクスピルはv8.3.0で導入されました。
-   [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-new-in-v800)システム変数を使用して、ディスクスピルをサポートする並列HashAggアルゴリズムを有効にするかどうかを制御できます。この変数は将来のリリースで廃止される予定です。
-   Sort、MergeJoin、HashJoin、HashAgg、または TopN を含む SQL 実行によって OOM が発生すると、TiDB はデフォルトでディスク スピルをトリガーします。

> **注記：**
>
> HashAgg のディスクスピルは、 `DISTINCT`集計関数を含む SQL 実行をサポートしていません。3 `DISTINCT`集計関数を含む SQL 実行でメモリ使用量が多すぎる場合、ディスクスピルは適用されません。

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

4.  同じSQL文を実行します。今回は文が正常に実行され、エラーメッセージは返されません。以下の詳細な実行プランから、HashAggが600MBのハードディスク容量を使用していることがわかります。

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

### <code>GOMEMLIMIT</code>を設定して OOM の問題を軽減する {#mitigate-oom-issues-by-configuring-code-gomemlimit-code}

GO 1.19 では、GC をトリガーするメモリ制限を設定するための環境変数[`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables)導入されています。

v6.1.3 &lt;= TiDB &lt; v6.5.0 の場合、手動で`GOMEMLIMIT`設定することで、OOM 問題の典型的なカテゴリを軽減できます。OOM 問題の典型的なカテゴリは、OOM が発生する前に、Grafana で推定される使用メモリが全体のメモリの半分しか占めていないというものです (TiDB-Runtime &gt; Memory Usage &gt; estimate-inuse)。次の図に示されています。

![normal OOM case example](/media/configure-memory-usage-oom-example.png)

`GOMEMLIMIT`のパフォーマンスを確認するために、 `GOMEMLIMIT`構成の有無での特定のメモリ使用量を比較するテストを実行します。

-   TiDB v6.1.2 では、シミュレートされたワークロードが数分間実行された後、TiDBサーバーはOOM (システムメモリ: 約 48 GiB) に遭遇します。

    ![v6.1.2 workload oom](/media/configure-memory-usage-612-oom.png)

-   TiDB v6.1.3では、 `GOMEMLIMIT` 40000MiBに設定されています。シミュレーションされたワークロードは長時間安定して動作し、TiDBサーバーでOOMは発生せず、プロセスの最大メモリ使用量は40.8GiB前後で安定していることがわかりました。

    ![v6.1.3 workload no oom with GOMEMLIMIT](/media/configure-memory-usage-613-no-oom.png)
