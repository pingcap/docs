---
title: Troubleshoot TiDB OOM Issues
summary: TiDB OOM (メモリ不足) の問題を診断して解決する方法を学びます。
---

# TiDB OOM の問題のトラブルシューティング {#troubleshoot-tidb-oom-issues}

このドキュメントでは、現象、原因、解決策、診断情報など、TiDB OOM (メモリ不足) の問題のトラブルシューティング方法について説明します。

## 典型的なOOM現象 {#typical-oom-phenomena}

以下に、典型的な OOM 現象をいくつか示します。

-   クライアント側から次のエラーが報告されます: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query` 。

-   Grafana ダッシュボードには以下が表示されます:
    -   **TiDB** &gt;**サーバー**&gt;**メモリ使用量では、** `process/heapInUse`メトリックが上昇し続け、しきい値に達した後突然ゼロに低下することが示されています。
    -   **TiDB** &gt;**サーバー**&gt;**稼働時間**が突然ゼロに低下します。
    -   **TiDB-Runtime** &gt;**メモリ使用量では**、 `estimate-inuse`メトリックが上昇し続けていることがわかります。

-   `tidb.log`確認すると、次のログ エントリが見つかります。
    -   OOM に関する警告: `[WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"]` 。詳細については、 [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)参照してください。
    -   再起動に関するログエントリ: `[INFO] [printer.go:33] ["Welcome to TiDB."]` 。

## 全体的なトラブルシューティングプロセス {#overall-troubleshooting-process}

OOM の問題をトラブルシューティングする場合は、次のプロセスに従います。

1.  OOM の問題かどうかを確認します。

    以下のコマンドを実行して、オペレーティングシステムのログを確認します。問題が発生した時間の近くに`oom-killer`ログがある場合は、OOM の問題であることが確認できます。

    ```shell
    dmesg -T | grep tidb-server
    ```

    以下は`oom-killer`含むログの例です。

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

    -   OOM がデプロイメントの問題によって発生した場合は、リソース構成とハイブリッド デプロイメントの影響を調査する必要があります。
    -   OOM がデータベースの問題によって発生した場合、次のような原因が考えられます。
        -   TiDB は、大規模なクエリ、大規模な書き込み、データのインポートなどの大規模なデータ トラフィックを処理します。
        -   TiDB は、複数の SQL ステートメントが同時にリソースを消費したり、演算子の同時実行性が高くなったりする、同時実行性の高いシナリオにあります。
        -   TiDB にメモリリークがあり、リソースが解放されません。

    具体的なトラブルシューティング方法については、次のセクションを参照してください。

## 一般的な原因と解決策 {#typical-causes-and-solutions}

OOM の問題は通常、次の原因で発生します。

-   [展開の問題](#deployment-issues)
-   [データベースの問題](#database-issues)
-   [クライアント側の問題](#client-side-issues)

### 展開の問題 {#deployment-issues}

不適切なデプロイメントによる OOM の原因は次のとおりです。

-   オペレーティング システムのメモリ容量が小さすぎます。
-   TiUP構成[`resource_control`](/tiup/tiup-cluster-topology-reference.md#global)は適切ではありません。
-   ハイブリッド デプロイメント (TiDB と他のアプリケーションが同じサーバーにデプロイされていることを意味します) の場合、リソース不足のため、TiDB が`oom-killer`によって誤って強制終了されます。

### データベースの問題 {#database-issues}

このセクションでは、データベースの問題によって発生する OOM の原因と解決策について説明します。

> **注記：**
>
> [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)設定した場合、エラーが発生します: `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]` 。これは、データベースのメモリ使用量制御動作によって発生します。これは正常な動作です。

#### SQL文を実行するとメモリが大量に消費される {#executing-sql-statements-consumes-too-much-memory}

OOM 問題のさまざまな原因に応じて、SQL ステートメントのメモリ使用量を削減するために次の対策を講じることができます。

-   適切なインデックスがない、統計が古い、オプティマイザのバグなどにより、SQL の実行プランが最適でない場合は、間違った SQL の実行プランが選択されることがあります。その場合、膨大な中間結果セットがメモリに蓄積されます。このような場合は、次の対策を検討してください。
    -   適切なインデックスを追加します。
    -   実行演算子には[ディスクスピル](/configure-memory-usage.md#disk-spill)機能を使用します。
    -   テーブル間の JOIN 順序を調整します。
    -   ヒントを使用して SQL ステートメントを最適化します。

-   一部の演算子と関数はstorageレベルへのプッシュダウンがサポートされていないため、中間結果セットが大量に蓄積されます。この場合、SQL ステートメントを改良するか、ヒントを使用して最適化し、プッシュダウンをサポートする関数または演算子を使用する必要があります。

-   実行プランには演算子 HashAgg が含まれています。HashAgg は複数のスレッドによって同時に実行されるため、高速になりますが、より多くのメモリを消費します。代わりに、 `STREAM_AGG()`使用できます。

-   同時に読み取る領域の数を減らすか、演算子の同時実行性を減らして、同時実行性が高いために発生するメモリの問題を回避します。対応するシステム変数は次のとおりです。
    -   [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    -   [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    -   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)

-   問題が発生した時点付近では、セッションの同時実行性が高すぎます。この場合、TiDB ノードを追加して TiDB クラスターをスケールアウトすることを検討してください。

#### 大規模なトランザクションや大規模な書き込みはメモリを大量に消費します {#large-transactions-or-large-writes-consume-too-much-memory}

メモリ容量を計画する必要があります。トランザクションが実行されると、TiDB プロセスのメモリ使用量はトランザクション サイズと比較して増加し、最大でトランザクション サイズの 2 ～ 3 倍以上にまで増加します。

1 つの大きなトランザクションを複数の小さなトランザクションに分割できます。

#### 統計情報を収集して読み込むプロセスでメモリが大量に消費される {#the-process-of-collecting-and-loading-statistical-information-consumes-too-much-memory}

TiDB ノードは起動後に統計をメモリにロードする必要があります。TiDB は統計情報を収集するときにメモリを消費します。メモリ使用量は、次の方法で制御できます。

-   サンプリング レートを指定し、特定の列の統計情報のみを収集し、同時実行性を`ANALYZE`減らします。
-   TiDB v6.1.0 以降では、システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)使用して統計情報のメモリ使用量を制御できます。
-   TiDB v6.1.0 以降では、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)使用して、TiDB が統計を更新するときに最大メモリ使用量を制御できます。

詳細については[統計入門](/statistics.md)参照してください。

#### 準備されたステートメントは使いすぎです {#prepared-statements-are-overused}

クライアント側は準備​​済みステートメントを作成し続けますが、実行しません[`deallocate prepare stmt`](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) 。これにより、メモリ消費量が増加し続け、最終的に TiDB OOM が発生します。その理由は、プリペアドステートメントによって占有されたメモリは、セッションが終了するまで解放されないためです。これは、長時間の接続セッションでは特に重要です。

この問題を解決するには、次の対策を検討してください。

-   セッションのライフサイクルを調整します。
-   [接続プールの`wait_timeout`と`max_execution_time`](/develop/dev-guide-connection-parameters.md#timeout-related-parameters)調整します。
-   システム変数[`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count)使用して、セッションで準備されたステートメントの最大数を制御します。

#### <code>tidb_enable_rate_limit_action</code>が正しく設定されていません {#code-tidb-enable-rate-limit-action-code-is-not-configured-properly}

システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)は、SQL 文がデータを読み取るだけの場合に、メモリ使用量を効果的に制御します。この変数が有効になっていて、計算操作 (結合操作や集計操作など) が必要な場合、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)によって制御されない可能性があり、OOM のリスクが高まります。

このシステム変数を無効にすることをお勧めします。TiDB v6.3.0 以降、このシステム変数はデフォルトで無効になっています。

### クライアント側の問題 {#client-side-issues}

クライアント側で OOM が発生した場合は、次の点を調査します。

-   **Grafana TiDB の「詳細」** &gt; **「サーバー」** &gt; **「クライアント データ トラフィック」**で傾向と速度を確認し、ネットワークのブロックがあるかどうかを確認します。
-   間違った JDBC 構成パラメータによってアプリケーション OOM が発生していないかどうかを確認します。たとえば、ストリーミング読み取りの`defaultFetchSize`パラメータが誤って構成されていると、クライアント側に大量のデータが蓄積される可能性があります。

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
    -   TiDB バージョン
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

    -   TiDB ダッシュボードで、SQL ステートメント分析、低速クエリ、メモリ使用量をビュー。
    -   `INFORMATION_SCHEMA`の`SLOW_QUERY`と`CLUSTER_SLOW_QUERY`確認してください。
    -   各 TiDB ノードで`tidb_slow_query.log`チェックします。
    -   `grep "expensive_query" tidb.log`実行して、対応するログ エントリを確認します。
    -   `EXPLAIN ANALYZE`実行して、演算子のメモリ使用量を確認します。
    -   `SELECT * FROM information_schema.processlist;`実行して`MEM`列の値を確認します。

-   メモリ使用量が高い場合に TiDB プロファイル情報を収集するには、次のコマンドを実行します。

    ```shell
    curl -G "http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

-   `grep "tidb-server has the risk of OOM" tidb.log`実行して、TiDB サーバーによって収集されたアラート ファイルのパスを確認します。出力例を次に示します。

    ```shell
    ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

## 参照 {#see-also}

-   [TiDB メモリ制御](/configure-memory-usage.md)
-   [TiKV メモリ パラメータのパフォーマンスを調整する](/tune-tikv-memory-performance.md)
