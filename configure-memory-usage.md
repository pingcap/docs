---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
---

# TiDBメモリ制御 {#tidb-memory-control}

現在、TiDBは、単一のSQLクエリのメモリクォータを追跡し、メモリ使用量が特定のしきい値を超えたときにOOM（メモリ不足）を防止するか、OOMのトラブルシューティングを行うためのアクションを実行できます。 TiDB構成ファイルでは、メモリクォータがしきい値を超えたときのTiDBの動作を制御するために、以下のオプションを構成できます。

```
# Valid options: ["log", "cancel"]
oom-action = "cancel"
```

-   上記の構成アイテムが「ログ」を使用している場合、単一のSQLクエリのメモリクォータが`tidb_mem_quota_query`変数によって制御されるしきい値を超えると、TiDBはログのエントリを出力します。その後、SQLクエリは引き続き実行されます。 OOMが発生した場合、対応するSQLクエリをログで見つけることができます。
-   上記の構成項目で「キャンセル」を使用している場合、単一のSQLクエリのメモリクォータがしきい値を超えると、TiDBはSQLクエリの実行をすぐに停止し、クライアントにエラーを返します。エラー情報は、SQL実行プロセスで多くのメモリを消費する各物理実行演算子のメモリ使用量を明確に示しています。

## クエリのメモリクォータを構成する {#configure-the-memory-quota-of-a-query}

構成ファイルでは、クエリごとにデフォルトのメモリクォータを設定できます。次の例では、32GBに設定しています。

```
mem-quota-query = 34359738368
```

さらに、次のセッション変数を使用して、クエリのメモリクォータを制御できます。通常、構成する必要があるのは`tidb_mem_quota_query`だけです。他の変数は、ほとんどのユーザーが気にする必要のない高度な構成に使用されます。

| 変数名                              | 説明                                  | 単位  | デフォルト値              |
| -------------------------------- | ----------------------------------- | --- | ------------------- |
| tidb_mem_quota_query             | クエリのメモリクォータを制御する                    | バイト | 1 &lt;&lt; 30（1 GB） |
| tidb_mem_quota_hashjoin          | 「HashJoinExec」のメモリクォータを制御する         | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_mergejoin         | 「MergeJoinExec」のメモリクォータを制御する        | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_sort              | 「SortExec」のメモリクォータを制御する             | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_topn              | 「TopNExec」のメモリクォータを制御する             | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_indexlookupreader | 「IndexLookUpExecutor」のメモリクォータを制御します | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_indexlookupjoin   | 「IndexLookUpJoin」のメモリクォータを制御します     | バイト | 32 &lt;&lt; 30      |
| tidb_mem_quota_nestedloopapply   | 「NestedLoopApplyExec」のメモリクォータを制御します | バイト | 32 &lt;&lt; 30      |

いくつかの使用例：

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8GB:
set @@tidb_mem_quota_query = 8 << 30;
```

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8MB:
set @@tidb_mem_quota_query = 8 << 20;
```

{{< copyable "" >}}

```sql
-- Set the threshold value of memory quota for a single SQL query to 8KB:
set @@tidb_mem_quota_query = 8 << 10;
```

## tidb-serverインスタンスのメモリ使用量のしきい値を構成します {#configure-the-memory-usage-threshold-of-a-tidb-server-instance}

TiDB構成ファイルでは、 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)を構成することにより、tidb-serverインスタンスのメモリ使用量のしきい値を設定できます。

次の例では、tidb-serverインスタンスの合計メモリ使用量を32GBに設定します。

{{< copyable "" >}}

```toml
[performance]
server-memory-quota = 34359738368
```

この構成では、tidb-serverインスタンスのメモリ使用量が32 GBに達すると、メモリ使用量が32 GBを下回るまで、インスタンスは実行中のSQLステートメントをランダムに強制終了し始めます。強制終了するSQL操作は、クライアントに`Out Of Global Memory Limit!`エラーメッセージを返します。

> **警告：**
>
> -   `server-memory-quota`はまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。
> -   デフォルト値の`server-memory-quota`は`0`です。これは、メモリ制限がないことを意味します。

## 過度のメモリ使用量のアラームをトリガーします {#trigger-the-alarm-of-excessive-memory-usage}

デフォルトの構成では、マシンのメモリ使用量が合計メモリの80％に達すると、tidb-serverインスタンスはアラームログを出力し、関連するステータスファイルを記録します。 `memory-usage-alarm-ratio`を設定することにより、メモリ使用率のしきい値を設定できます。詳細なアラームルールについては、 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)の説明を参照してください。

アラームが1回トリガーされた後、メモリ使用率が10秒を超えてしきい値を下回り、再びしきい値に達した場合にのみ、アラームが再度トリガーされることに注意してください。さらに、アラームによって生成された過剰なステータスファイルの保存を回避するために、現在、TiDBは最近の5つのアラーム中に生成されたステータスファイルのみを保持します。

次の例では、アラームをトリガーするメモリを大量に消費するSQLステートメントを作成します。

1.  `memory-usage-alarm-ratio`から`0.8`に設定：

    {{< copyable "" >}}

    ```toml
    mem-quota-query = 34359738368  // Increases the memory limit of each query to construct SQL statements that take up larger memory.
    [performance]
    memory-usage-alarm-ratio = 0.8
    ```

2.  `CREATE TABLE t(a int);`を実行し、1000行のデータを挿入します。

3.  `select * from t t1 join t t2 join t t3 order by t1.a`を実行します。このSQLステートメントは10億レコードを出力しますが、これは大量のメモリを消費するため、アラームをトリガーします。

4.  合計システムメモリ、現在のシステムメモリ使用量、tidb-serverインスタンスのメモリ使用量、およびステータスファイルのディレクトリを記録する`tidb.log`のファイルを確認します。

    ```
    [2020/11/30 15:25:17.252 +08:00] [WARN] [memory_usage_alarm.go:141] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=33682427904] ["system memory usage"=27142864896] ["tidb-server memory usage"=22417922896] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

    上記のサンプルログファイルのフィールドは次のとおりです。

    -   `is server-memory-quota set`は、 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)が設定されているかどうかを示します。
    -   `system memory total`は、現在のシステムの合計メモリを示します。
    -   `system memory usage`は、現在のシステムメモリ使用量を示します。
    -   `tidb-server memory usage`は、tidb-serverインスタンスのメモリ使用量を示します。
    -   `memory-usage-alarm-ratio`は[`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)の値を示します。
    -   `record path`はステータスファイルのディレクトリを示します。

5.  ステータスファイルのディレクトリ（上記の例では、ディレクトリは`/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record` ）に、 `goroutinue` 、および`heap`を含む一連のファイルが表示され`running_sql` 。これらの3つのファイルには、ステータスファイルがログに記録される時刻の接尾辞が付いています。それぞれ、ゴルーチンスタック情報、ヒープメモリの使用状況、およびアラームがトリガーされたときの実行中のSQL情報を記録します。 `running_sql`のログコンテンツの形式については、 [`expensive-queries`](/identify-expensive-queries.md)を参照してください。

## tidb-serverの他のメモリ制御動作 {#other-memory-control-behaviors-of-tidb-server}

### フロー制御 {#flow-control}

-   TiDBは、データを読み取るオペレーターの動的メモリ制御をサポートしています。デフォルトでは、この演算子は[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)がデータの読み取りを許可するスレッドの最大数を使用します。 1回のSQL実行のメモリ使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターが1つのスレッドを停止します。

-   このフロー制御の動作は、システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)によって制御されます。

-   フロー制御動作がトリガーされると、TiDBはキーワード`memory exceeds quota, destroy one token now`を含むログを出力します。

### ディスクの流出 {#disk-spill}

TiDBは、実行オペレーターのディスクスピルをサポートします。 SQL実行のメモリ使用量がメモリクォータを超えると、tidb-serverは実行オペレータの中間データをディスクにスピルして、メモリの負荷を軽減できます。ディスクスピルをサポートするオペレーターには、Sort、MergeJoin、HashJoin、およびHashAggが含まれます。

-   ディスクの流出動作は、 [`mem-quota-query`](/tidb-configuration-file.md#mem-quota-query) 、および[`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path)のパラメーターによって共同で制御さ[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota) [`oom-use-tmp-storage`](/tidb-configuration-file.md#oom-use-tmp-storage) 。
-   ディスクスピルがトリガーされると、TiDBはキーワード`memory exceeds quota, spill to disk now`または`memory exceeds quota, set aggregate mode to spill-mode`を含むログを出力します。
-   Sort、MergeJoin、およびHashJoinオペレーターのディスクスピルはv4.0.0で導入されました。 HashAggオペレーターのディスクスピルはv5.2.0で導入されました。
-   Sort、MergeJoin、またはHashJoinを含むSQL実行によってOOMが発生すると、TiDBはデフォルトでディスクスピルをトリガーします。 HashAggを含むSQL実行がOOMを引き起こす場合、TiDBはデフォルトでディスクスピルをトリガーしません。 HashAggのディスクスピルをトリガーするようにシステム変数`tidb_executor_concurrency = 1`を構成できます。

> **ノート：**
>
> HashAggのディスクスピルは、 `DISTINCT`集約関数を含むSQL実行をサポートしていません。 `DISTINCT`集計関数を含むSQL実行が大量のメモリを使用する場合、ディスクスピルは適用されません。

次の例では、メモリを消費するSQLステートメントを使用して、HashAggのディスクスピル機能を示しています。

1.  SQLステートメントのメモリクォータを1GB（デフォルトでは1 GB）に構成します。

    {{< copyable "" >}}

    ```sql
    set tidb_mem_quota_query = 1 << 30;
    ```

2.  単一のテーブル`CREATE TABLE t(a int);`を作成し、256行の異なるデータを挿入します。

3.  次のSQLステートメントを実行します。

    {{< copyable "" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    このSQLステートメントを実行するとメモリを大量に消費するため、次の「メモリ不足クォータ」エラーメッセージが返されます。

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4.  システム変数`tidb_executor_concurrency`を1に構成します。この構成では、メモリが不足すると、HashAggは自動的にディスクスピルをトリガーしようとします。

    {{< copyable "" >}}

    ```sql
    set tidb_executor_concurrency = 1;
    ```

5.  同じSQLステートメントを実行します。今回は、ステートメントが正常に実行され、エラーメッセージが返されないことがわかります。次の詳細な実行プランから、HashAggが600MBのハードディスク領域を使用していることがわかります。

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
