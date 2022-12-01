---
title: TiDB Memory Control
summary: Learn how to configure the memory quota of a query and avoid OOM (out of memory).
---

# TiDB メモリ制御 {#tidb-memory-control}

現在、TiDB は単一の SQL クエリのメモリ クォータを追跡し、メモリ使用量が特定のしきい値を超えたときに OOM (メモリ不足) を防止したり、OOM のトラブルシューティングを行ったりするためのアクションを実行できます。システム変数[`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)は、クエリがメモリ制限に達したときに実行するアクションを指定します。

-   `LOG`の値は、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制限に達したときにクエリが引き続き実行されることを意味しますが、TiDB はログにエントリを出力します。
-   値`CANCEL`は、TiDB が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制限に達した直後に SQL クエリの実行を停止し、クライアントにエラーを返すことを意味します。エラー情報には、SQL 実行プロセスでメモリを消費する各物理実行演算子のメモリ使用量が明確に示されます。

## クエリのメモリ クォータを構成する {#configure-the-memory-quota-of-a-query}

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

TiDB 構成ファイルで、 [`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)を構成することにより、tidb-server インスタンスのメモリ使用量のしきい値を設定できます。

次の例では、tidb-server インスタンスの合計メモリ使用量を 32 GB に設定します。

{{< copyable "" >}}

```toml
[performance]
server-memory-quota = 34359738368
```

この構成では、tidb-server インスタンスのメモリ使用量が 32 GB に達すると、メモリ使用量が 32 GB を下回るまで、インスタンスは実行中の SQL ステートメントをランダムに強制終了し始めます。強制終了された SQL 操作は、クライアントに`Out Of Global Memory Limit!`エラー メッセージを返します。

> **警告：**
>
> -   `server-memory-quota`はまだ実験的機能です。実稼働環境で使用することはお勧めし**ません**。
> -   `server-memory-quota`のデフォルト値は`0`で、これはメモリ制限がないことを意味します。

## 過剰なメモリ使用量のアラームをトリガーする {#trigger-the-alarm-of-excessive-memory-usage}

デフォルトの構成では、マシンのメモリ使用量が合計メモリの 80% に達すると、tidb-server インスタンスはアラーム ログを出力し、関連するステータス ファイルを記録します。 `memory-usage-alarm-ratio`を構成することで、メモリ使用率のしきい値を設定できます。詳細なアラーム ルールについては、 [`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)の説明を参照してください。

アラームが一度トリガーされた後、メモリ使用率が 10 秒以上しきい値を下回り、再びしきい値に達した場合にのみ、アラームが再度トリガーされることに注意してください。さらに、アラームによって生成された過剰なステータス ファイルを保存しないように、現在、TiDB は最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。

次の例では、アラームをトリガーするメモリ集約型の SQL ステートメントを作成します。

1.  `memory-usage-alarm-ratio` ～ `0.8`を設定:

    {{< copyable "" >}}

    ```toml
    [performance]
    memory-usage-alarm-ratio = 0.8
    ```

2.  `CREATE TABLE t(a int);`を実行し、1000 行のデータを挿入します。

3.  `select * from t t1 join t t2 join t t3 order by t1.a`を実行します。この SQL ステートメントは 10 億件のレコードを出力します。これは大量のメモリを消費するため、アラームがトリガーされます。

4.  合計システム メモリ、現在のシステム メモリ使用量、tidb-server インスタンスのメモリ使用量、およびステータス ファイルのディレクトリを記録する`tidb.log`のファイルを確認します。

    ```
    [2020/11/30 15:25:17.252 +08:00] [WARN] [memory_usage_alarm.go:141] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=33682427904] ["system memory usage"=27142864896] ["tidb-server memory usage"=22417922896] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

    上記のログ ファイルの例のフィールドは、次のように説明されています。

    -   `is server-memory-quota set`は[`server-memory-quota`](/tidb-configuration-file.md#server-memory-quota-new-in-v409)が設定されているかどうかを示します。
    -   `system memory total`は、現在のシステムの合計メモリを示します。
    -   `system memory usage`は、現在のシステム メモリ使用量を示します。
    -   `tidb-server memory usage`は、tidb-server インスタンスのメモリ使用量を示します。
    -   `memory-usage-alarm-ratio`は[`memory-usage-alarm-ratio`](/tidb-configuration-file.md#memory-usage-alarm-ratio-new-in-v409)の値を示します。
    -   `record path`は、ステータス ファイルのディレクトリを示します。

5.  ステータス ファイルのディレクトリ (上記の例では、ディレクトリは`/tmp/1000_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record`です) に、 `goroutinue` 、 `heap` 、および`running_sql`を含む一連のファイルが表示されます。これら 3 つのファイルの末尾には、ステータス ファイルがログに記録された時刻が付けられます。アラームがトリガーされたときに、ゴルーチン スタック情報、ヒープ メモリの使用状況、および実行中の SQL 情報をそれぞれ記録します。 `running_sql`のログ内容の形式については、 [`expensive-queries`](/identify-expensive-queries.md)を参照してください。

## tidb-server のその他のメモリ制御動作 {#other-memory-control-behaviors-of-tidb-server}

### フロー制御 {#flow-control}

-   TiDB は、データを読み取るオペレーターの動的メモリー制御をサポートしています。デフォルトでは、このオペレーターは、データの読み取りを許可するスレッドの最大数を使用し[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 。 1 回の SQL 実行のメモリー使用量が毎回[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を超えると、データを読み取るオペレーターは 1 つのスレッドを停止します。

-   このフロー制御動作は、システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)によって制御されます。この変数はデフォルトで有効になっているため、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制御下にない場合があります。したがって、値を`tidb_enable_rate_limit_action` ～ `OFF`に設定することをお勧めします。

-   フロー制御動作がトリガーされると、TiDB はキーワード`memory exceeds quota, destroy one token now`を含むログを出力します。

### ディスクこぼれ {#disk-spill}

TiDB は、実行オペレーターのディスクスピルをサポートしています。 SQL 実行のメモリ使用量がメモリ クォータを超えると、tidb-server は実行オペレータの中間データをディスクにスピルして、メモリの負荷を軽減できます。ディスク スピルをサポートする演算子には、Sort、MergeJoin、HashJoin、HashAgg などがあります。

-   ディスク スピルの動作は、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 、 [`oom-use-tmp-storage`](/tidb-configuration-file.md#oom-use-tmp-storage) 、 [`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path) 、および[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota)パラメータによって共同で制御されます。
-   ディスク スピルがトリガーされると、TiDB はキーワード`memory exceeds quota, spill to disk now`または`memory exceeds quota, set aggregate mode to spill-mode`を含むログを出力します。
-   Sort、MergeJoin、および HashJoin オペレーターのディスク スピルは v4.0.0 で導入されました。 HashAgg オペレーターのディスク スピルは v5.2.0 で導入されました。
-   Sort、MergeJoin、または HashJoin を含む SQL 実行によって OOM が発生すると、TiDB はデフォルトでディスク スピルをトリガーします。 HashAgg を含む SQL 実行によって OOM が発生した場合、TiDB はデフォルトでディスク スピルをトリガーしません。システム変数`tidb_executor_concurrency = 1`を構成して、HashAgg のディスク スピルをトリガーできます。

> **ノート：**
>
> HashAgg のディスク スピルは、 `DISTINCT`の集計関数を含む SQL 実行をサポートしていません。 `DISTINCT`の集計関数を含む SQL 実行でメモリが大量に使用される場合、ディスク スピルは適用されません。

次の例では、メモリを消費する SQL ステートメントを使用して、HashAgg のディスク スピル機能を示します。

1.  SQL ステートメントのメモリ クォータを 1 GB (既定では 1 GB) に構成します。

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

4.  システム変数を`tidb_executor_concurrency`対 1 で構成します。この構成では、メモリが不足すると、HashAgg は自動的にディスク スピルをトリガーしようとします。

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
