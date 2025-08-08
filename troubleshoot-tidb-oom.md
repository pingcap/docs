---
title: Troubleshoot TiDB OOM Issues
summary: TiDB OOM (メモリ不足) の問題を診断して解決する方法を学びます。
---

# TiDB OOM の問題のトラブルシューティング {#troubleshoot-tidb-oom-issues}

このドキュメントでは、現象、原因、解決策、診断情報など、TiDB OOM (メモリ不足) の問題をトラブルシューティングする方法について説明します。

## 典型的なOOM現象 {#typical-oom-phenomena}

以下に、典型的な OOM 現象をいくつか示します。

-   クライアント側で次のエラーが報告されます: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query` 。

-   Grafana ダッシュボードには次の内容が表示されます。
    -   **TiDB** &gt;**サーバー**&gt;**メモリ使用量で**は、 `process/heapInUse`メトリックが上昇し続け、しきい値に達した後、突然 0 に低下することが示されています。
    -   **TiDB** &gt;**サーバー**&gt;**稼働時間が**突然ゼロに低下します。
    -   **TiDB-Runtime** &gt;**メモリ使用量で**は、 `estimate-inuse`メトリックが上昇し続けていることがわかります。

-   `tidb.log`確認すると、次のログ エントリが見つかります。
    -   OOMに関するアラーム: `[WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"]` 。詳細については、 [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)参照してください。
    -   再起動に関するログエントリ: `[INFO] [printer.go:33] ["Welcome to TiDB."]` 。

## 全体的なトラブルシューティングプロセス {#overall-troubleshooting-process}

OOM の問題をトラブルシューティングする場合は、次のプロセスに従います。

1.  OOM の問題であるかどうかを確認します。

    以下のコマンドを実行して、オペレーティングシステムのログを確認します。問題が発生した時刻付近に`oom-killer`ログがある場合は、OOMの問題であることが確認できます。

    ```shell
    dmesg -T | grep tidb-server
    ```

    以下は`oom-killer`を含むログの例です。

    ```shell
    ......
    Mar 14 16:55:03 localhost kernel: tidb-server invoked oom-killer: gfp_mask=0x201da, order=0, oom_score_adj=0
    Mar 14 16:55:03 localhost kernel: tidb-server cpuset=/ mems_allowed=0
    Mar 14 16:55:03 localhost kernel: CPU: 14 PID: 21966 Comm: tidb-server Kdump: loaded Not tainted 3.10.0-1160.el7.x86_64 #1
    Mar 14 16:55:03 localhost kernel: Hardware name: QEMU Standard PC (i440FX + PIIX, 1996), BIOS rel-1.14.0-0-g155821a1990b-prebuilt.qemu.org 04/01/2014
    ......
    Mar 14 16:55:03 localhost kernel: Out of memory: Kill process 21945 (tidb-server) score 956 or sacrifice child
    Mar 14 16:55:03 localhost kernel: Killed process 21945 (tidb-server), UID 1000, total-vm:33027492kB, anon-rss:31303276kB, file-rss:0kB, shmem-rss:0kB
    Mar 14 16:55:07 localhost systemd: tidb-4000.service: main process exited, code=killed, status=9/KILL
    ......
    ```

2.  OOM の問題であることを確認した後、OOM の原因がデプロイメントによるものかデータベースによるものかをさらに調査できます。

    -   OOM が展開の問題によって発生した場合は、リソース構成とハイブリッド展開の影響を調査する必要があります。
    -   OOM がデータベースの問題によって発生した場合、次のような原因が考えられます。
        -   TiDB は、大規模なクエリ、大規模な書き込み、データのインポートなどの大規模なデータ トラフィックを処理します。
        -   TiDB は、複数の SQL ステートメントが同時にリソースを消費したり、オペレーターの同時実行性が高くなったりする、同時実行性の高いシナリオです。
        -   TiDB にメモリリークがあり、リソースが解放されません。

    具体的なトラブルシューティング方法については、次のセクションを参照してください。

## 一般的な原因と解決策 {#typical-causes-and-solutions}

OOM の問題は通常、次の原因で発生します。

-   [展開の問題](#deployment-issues)
-   [データベースの問題](#database-issues)
-   [クライアント側の問題](#client-side-issues)

### 展開の問題 {#deployment-issues}

不適切な展開による OOM の原因は次のとおりです。

-   オペレーティング システムのメモリ容量が小さすぎます。
-   TiUP構成[`resource_control`](/tiup/tiup-cluster-topology-reference.md#global)は適切ではありません。
-   ハイブリッド デプロイメント (つまり、TiDB と他のアプリケーションが同じサーバーにデプロイされている) の場合、リソース不足により、TiDB が`oom-killer`によって誤って強制終了されることがあります。

### データベースの問題 {#database-issues}

このセクションでは、データベースの問題によって発生する OOM の原因と解決策について説明します。

> **注記：**
>
> [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)設定した場合、エラーが発生します: `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]` 。これはデータベースのメモリ使用量制御の動作によるもので、正常な動作です。

#### SQL文を実行するとメモリ消費量が多すぎる {#executing-sql-statements-consumes-too-much-memory}

OOM 問題のさまざまな原因に応じて、SQL ステートメントのメモリ使用量を削減するために次の対策を講じることができます。

-   SQL実行プランが最適でない場合（適切なインデックスの欠如、古い統計情報、オプティマイザのバグなど）、誤ったSQL実行プランが選択される可能性があり、その結果、膨大な中間結果セットがメモリに蓄積されます。このような場合は、以下の対策を検討してください。
    -   適切なインデックスを追加します。
    -   実行演算子には[ディスクスピル](/configure-memory-usage.md#disk-spill)機能を使用します。
    -   テーブル間の JOIN 順序を調整します。
    -   ヒントを使用して SQL ステートメントを最適化します。

-   一部の演算子と関数はstorageレベルへのプッシュダウンがサポートされていないため、中間結果セットが大量に蓄積されます。このような場合は、SQL文を修正するか、ヒントを使用して最適化し、プッシュダウンをサポートする関数または演算子を使用する必要があります。

-   実行プランにはHashAgg演算子が含まれています。HashAggは複数のスレッドで同時に実行されるため、高速ですがメモリ消費量は多くなります。代わりに`STREAM_AGG()`使用することもできます。

-   同時実行数の増加によるメモリ問題を回避するには、同時に読み取る領域の数を減らすか、演算子の同時実行数を減らしてください。対応するシステム変数は次のとおりです。
    -   [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    -   [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    -   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)

-   問題発生時点付近では、セッションの同時実行性が高すぎます。この場合は、TiDBノードを追加してTiDBクラスターをスケールアウトすることを検討してください。

#### 大規模なトランザクションや大規模な書き込みはメモリを大量に消費します {#large-transactions-or-large-writes-consume-too-much-memory}

メモリ容量を計画する必要があります。トランザクションが実行されると、TiDBプロセスのメモリ使用量はトランザクションサイズに応じて増加し、最大でトランザクションサイズの2～3倍以上にまで達することがあります。

1 つの大きなトランザクションを複数の小さなトランザクションに分割できます。

#### 統計情報を収集して読み込むプロセスはメモリを大量に消費します {#the-process-of-collecting-and-loading-statistical-information-consumes-too-much-memory}

TiDBノードは起動後、統計情報をメモリに読み込む必要があります。TiDBは統計情報を収集する際にメモリを消費します。メモリ使用量は、以下の方法で制御できます。

-   サンプリング レートを指定し、特定の列の統計情報のみを収集し、同時実行性を`ANALYZE`減らします。
-   TiDB v6.1.0 以降では、システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)使用して統計情報のメモリ使用量を制御できます。
-   TiDB v6.1.0 以降では、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)使用して、TiDB が統計を更新するときに最大メモリ使用量を制御できます。

詳細については[統計入門](/statistics.md)参照してください。

#### 準備されたステートメントは使いすぎです {#prepared-statements-are-overused}

クライアント側はプリペアドステートメントを作成し続けますが、実行しません[`deallocate prepare stmt`](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) 。これによりメモリ消費量が増加し続け、最終的にはTiDB OOMが発生します。これは、プリペアドステートメントによって占有されたメモリがセッションが終了するまで解放されないためです。これは、長時間接続セッションにおいて特に重要です。

この問題を解決するには、次の対策を検討してください。

-   セッションのライフサイクルを調整します。
-   [接続プールの`wait_timeout`と`max_execution_time`](/develop/dev-guide-connection-parameters.md#timeout-related-parameters)を調整します。
-   システム変数[`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count)を使用して、セッションで準備されるステートメントの最大数を制御します。

#### <code>tidb_enable_rate_limit_action</code>が正しく設定されていません {#code-tidb-enable-rate-limit-action-code-is-not-configured-properly}

システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) 、SQL文がデータの読み取りのみを行う場合に、メモリ使用量を効果的に制御します。この変数が有効になっている場合、結合や集計などの計算処理が必要なときに、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)によって制御されない可能性があり、OOM（オーバーヘッドメモリ不足）のリスクが高まります。

このシステム変数を無効にすることをお勧めします。TiDB v6.3.0以降、このシステム変数はデフォルトで無効になっています。

### クライアント側の問題 {#client-side-issues}

クライアント側で OOM が発生した場合は、次の点を調査します。

-   **Grafana TiDB の「詳細」** &gt; **「サーバー」** &gt; **「クライアント データ トラフィック」**で傾向と速度を確認し、ネットワークのブロックがあるかどうかを確認します。
-   誤ったJDBC設定パラメータによってアプリケーションのOOMが発生していないか確認してください。例えば、ストリーミング読み取りのパラメータ`defaultFetchSize`が正しく設定されていない場合、クライアント側に大量のデータが蓄積される可能性があります。

## OOM の問題をトラブルシューティングするために収集される診断情報 {#diagnostic-information-to-be-collected-to-troubleshoot-oom-issues}

OOM 問題の根本原因を特定するには、次の情報を収集する必要があります。

-   オペレーティング システムのメモリ関連の構成を収集します。
    -   TiUP構成: `resource_control.memory_limit`
    -   オペレーティング システムの構成:
        -   メモリ情報: `cat /proc/meminfo`
        -   カーネルパラメータ: `vm.overcommit_memory`
    -   NUMA情報:
        -   `numactl --hardware`
        -   `numactl --show`

-   データベースのバージョン情報とメモリ関連の構成を収集します。
    -   TiDBバージョン
    -   `tidb_mem_quota_query`
    -   `memory-usage-alarm-ratio`
    -   `mem-quota-query`
    -   `oom-action`
    -   `tidb_enable_rate_limit_action`
    -   `tidb_server_memory_limit`
    -   `oom-use-tmp-storage`
    -   `tmp-storage-path`
    -   `tmp-storage-quota`
    -   `tidb_analyze_version`

-   Grafana ダッシュボードで TiDBメモリの毎日の使用量を確認します: **TiDB** &gt; **Server** &gt; **Memory Usage** 。

-   より多くのメモリを消費する SQL ステートメントを確認します。

    -   TiDB ダッシュボードで、SQL ステートメントの分析、遅いクエリ、メモリ使用量をビュー。
    -   `INFORMATION_SCHEMA`の`SLOW_QUERY`と`CLUSTER_SLOW_QUERY`確認してください。
    -   各 TiDB ノードで`tidb_slow_query.log`チェックします。
    -   `grep "expensive_query" tidb.log`実行して、対応するログ エントリを確認します。
    -   `EXPLAIN ANALYZE`実行して、演算子のメモリ使用量を確認します。
    -   `SELECT * FROM information_schema.processlist;`実行して`MEM`列の値を確認します。

-   メモリ使用量が多いときに TiDB プロファイル情報を収集するには、次のコマンドを実行します。

    ```shell
    curl -G "http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

-   `grep "tidb-server has the risk of OOM" tidb.log`実行して、TiDB サーバーによって収集されたアラートファイルのパスを確認します。出力例を以下に示します。

    ```shell
    ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

## 参照 {#see-also}

-   [TiDB メモリ制御](/configure-memory-usage.md)
-   [TiKVメモリパラメータのパフォーマンスを調整する](/tune-tikv-memory-performance.md)
