---
title: Troubleshoot TiDB OOM Issues
summary: Learn how to diagnose and resolve TiDB OOM (Out of Memory) issues.
---

# TiDB OOM の問題のトラブルシューティング {#troubleshoot-tidb-oom-issues}

このドキュメントでは、現象、原因、解決策、診断情報など、TiDB OOM (メモリ不足) 問題のトラブルシューティング方法について説明します。

## 典型的な OOM 現象 {#typical-oom-phenomena}

以下に、典型的な OOM 現象をいくつか示します。

-   クライアント側は次のエラーを報告します: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query` 。

-   Grafana ダッシュボードには以下が表示されます。
    -   **[TiDB]** &gt; **[サーバー]** &gt; **[メモリ使用量]**では、 `process/heapInUse`メトリックが増加し続け、しきい値に達すると突然ゼロに低下することがわかります。
    -   **TiDB** &gt;**サーバー**&gt;**稼働時間が**突然ゼロに低下します。
    -   **[TiDB-Runtime]** &gt; **[メモリ使用量]**では、 `estimate-inuse`メトリクスが上昇し続けていることがわかります。

-   `tidb.log`を確認すると、次のログ エントリが見つかります。
    -   OOM に関するアラーム: `[WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]` 。詳細については、 [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)を参照してください。
    -   再起動に関するログ エントリ: `[INFO] [printer.go:33] ["Welcome to TiDB."]` 。

## 全体的なトラブルシューティングのプロセス {#overall-troubleshooting-process}

OOM の問題をトラブルシューティングする場合は、次のプロセスに従ってください。

1.  OOM の問題かどうかを確認します。

    次のコマンドを実行して、オペレーティング システムのログを確認します。問題が発生した時刻に近いログが`oom-killer`件あれば、OOM の問題であることを確認できます。

    ```shell
    dmesg -T | grep tidb-server
    ```

    以下は、 `oom-killer`を含むログの例です。

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

2.  OOM の問題であることを確認したら、OOM の原因がデプロイメントによるものかデータベースによるものかをさらに調査できます。

    -   OOM がデプロイメントの問題によって引き起こされている場合は、リソース構成とハイブリッド デプロイメントの影響を調査する必要があります。
    -   OOM がデータベースの問題によって引き起こされている場合は、次のような原因が考えられます。
        -   TiDB は、大規模なクエリ、大規模な書き込み、データ インポートなどの大規模なデータ トラフィックを処理します。
        -   TiDB は、複数の SQL ステートメントがリソースを同時に消費するか、オペレーターの同時実行性が高い、同時実行性の高いシナリオにあります。
        -   TiDB にメモリリークがあり、リソースが解放されません。

    具体的なトラブルシューティング方法については、次のセクションを参照してください。

## 一般的な原因と解決策 {#typical-causes-and-solutions}

OOM の問題は通常、次のことが原因で発生します。

-   [導入の問題](#deployment-issues)
-   [データベースの問題](#database-issues)
-   [クライアント側の問題](#client-side-issues)

### 導入の問題 {#deployment-issues}

不適切なデプロイメントによる OOM の原因には、次のようなものがあります。

-   オペレーティング システムのメモリ容量が少なすぎます。
-   TiUP構成[`resource_control`](/tiup/tiup-cluster-topology-reference.md#global)は適切ではありません。
-   ハイブリッド デプロイメント (TiDB と他のアプリケーションが同じサーバーにデプロイされることを意味します) の場合、リソース不足により TiDB が`oom-killer`て強制終了されます。

### データベースの問題 {#database-issues}

このセクションでは、データベースの問題による OOM の原因と解決策について説明します。

> **注記：**
>
> [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を設定した場合、次のエラーが発生します。 `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]` 。これは、データベースのメモリ使用量制御動作が原因で発生します。それは正常な動作です。

#### SQL ステートメントを実行すると大量のメモリが消費されます {#executing-sql-statements-consumes-too-much-memory}

OOM 問題のさまざまな原因に応じて、次の措置を講じて SQL ステートメントのメモリ使用量を削減できます。

-   たとえば、適切なインデックスの欠如、古い統計、オプティマイザのバグなどが原因で SQL の実行計画が最適でない場合、間違った SQL の実行計画が選択される可能性があります。巨大な中間結果セットがメモリに蓄積されます。この場合は、次のような対策を検討してください。
    -   適切なインデックスを追加します。
    -   実行演算子には[ディスク流出](/configure-memory-usage.md#disk-spill)機能を使用します。
    -   テーブル間の JOIN 順序を調整します。
    -   ヒントを使用して SQL ステートメントを最適化します。

-   一部の演算子と関数はstorageレベルへのプッシュダウンがサポートされていないため、中間結果セットが膨大に蓄積されます。この場合、SQL ステートメントを調整するかヒントを使用して最適化し、プッシュダウンをサポートする関数または演算子を使用する必要があります。

-   実行プランには演算子 HashAgg が含まれています。 HashAgg は複数のスレッドによって同時に実行されるため、高速になりますが、より多くのメモリを消費します。代わりに`STREAM_AGG()`を使用できます。

-   同時に読み取られるリージョンの数を減らすか、オペレーターの同時実行数を減らして、同時実行性の高さによって引き起こされるメモリの問題を回避します。対応するシステム変数には次のものがあります。
    -   [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    -   [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    -   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)

-   問題が発生する時点近くでは、セッションの同時実行性が高すぎます。この場合、TiDB ノードを追加して TiDB クラスターをスケールアウトすることを検討してください。

#### 大規模なトランザクションまたは大規模な書き込みはメモリを大量に消費します {#large-transactions-or-large-writes-consume-too-much-memory}

メモリ容量を計画する必要があります。トランザクションが実行されると、TiDB プロセスのメモリ使用量はトランザクション サイズに比べて増加し、最大で 2 ～ 3 倍以上になります。

1 つの大きなトランザクションを複数の小さなトランザクションに分割できます。

#### 統計情報の収集とロードのプロセスで大量のメモリが消費されます {#the-process-of-collecting-and-loading-statistical-information-consumes-too-much-memory}

TiDB ノードは、起動後に統計をメモリにロードする必要があります。 TiDB は統計情報を収集するときにメモリを消費します。次の方法でメモリ使用量を制御できます。

-   サンプリング レートを指定し、特定の列の統計のみを収集し、同時実行数を`ANALYZE`減らします。
-   TiDB v6.1.0 以降、システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)を使用して統計情報のメモリ使用量を制御できます。
-   TiDB v6.1.0 以降、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDB が統計を更新するときに最大メモリ使用量を制御できます。

詳細については、 [統計入門](/statistics.md)を参照してください。

#### プリペアドステートメントが多用されている {#prepared-statements-are-overused}

クライアント側はプリペアド ステートメントを作成し続けますが、 [`deallocate prepare stmt`](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement)実行しないため、メモリ消費量が増加し続け、最終的に TiDB OOM がトリガーされます。その理由は、プリペアドステートメントによって占有されているメモリは、セッションが閉じられるまで解放されないためです。これは、長時間の接続セッションでは特に重要です。

この問題を解決するには、次の対策を検討してください。

-   セッションのライフサイクルを調整します。
-   [接続プールの`wait_timeout`と`max_execution_time`](/develop/dev-guide-connection-parameters.md#timeout-related-parameters)を調整します。
-   システム変数[`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count)を使用して、セッション内の準備済みステートメントの最大数を制御します。

#### <code>tidb_enable_rate_limit_action</code>が正しく構成されていません {#code-tidb-enable-rate-limit-action-code-is-not-configured-properly}

システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) 、SQL ステートメントがデータの読み取りのみを行う場合のメモリ使用量を効果的に制御します。この変数が有効で、計算操作 (結合操作や集計操作など) が必要な場合、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制御下にない可能性があり、OOM のリスクが増加します。

このシステム変数を無効にすることをお勧めします。 TiDB v6.3.0 以降、このシステム変数はデフォルトで無効になっています。

### クライアント側の問題 {#client-side-issues}

OOM がクライアント側で発生する場合は、次の点を調査してください。

-   **[Grafana TiDB の詳細]** &gt; **[サーバー]** &gt; **[クライアント データ トラフィック]**で傾向と速度を確認し、ネットワークの障害がないか確認します。
-   間違った JDBC 構成パラメーターが原因でアプリケーション OOM が発生していないかどうかを確認してください。たとえば、ストリーミング読み取りの`defaultFetchSize`パラメータが正しく構成されていない場合、クライアント側にデータが大量に蓄積される可能性があります。

## OOM の問題をトラブルシューティングするために収集される診断情報 {#diagnostic-information-to-be-collected-to-troubleshoot-oom-issues}

OOM 問題の根本原因を特定するには、次の情報を収集する必要があります。

-   オペレーティング システムのメモリ関連の構成を収集します。
    -   TiUP構成： `resource_control.memory_limit`
    -   オペレーティング システムの構成:
        -   メモリ情報： `cat /proc/meminfo`
        -   カーネルパラメータ: `vm.overcommit_memory`
    -   NUMA 情報:
        -   `numactl --hardware`
        -   `numactl --show`

-   データベースのバージョン情報とメモリ関連の構成を収集します。
    -   TiDBのバージョン
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

-   Grafana ダッシュボードで TiDBメモリの毎日の使用量を確認します: **TiDB** &gt;**サーバー**&gt;**メモリ使用量**。

-   より多くのメモリを消費する SQL ステートメントを確認します。

    -   TiDB ダッシュボードで SQL ステートメント分析、遅いクエリ、メモリ使用量をビュー。
    -   `INFORMATION_SCHEMA`の`SLOW_QUERY`と`CLUSTER_SLOW_QUERY`確認します。
    -   各 TiDB ノードで`tidb_slow_query.log`をチェックします。
    -   `grep "expensive_query" tidb.log`を実行して、対応するログ エントリを確認します。
    -   `EXPLAIN ANALYZE`を実行して、演算子のメモリ使用量を確認します。
    -   `SELECT * FROM information_schema.processlist;`を実行して`MEM`列の値を確認します。

-   メモリ使用量が多い場合は、次のコマンドを実行して TiDB プロファイル情報を収集します。

    ```shell
    curl -G http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

-   `grep "tidb-server has the risk of OOM" tidb.log`を実行して、TiDB サーバーによって収集されたアラート ファイルのパスを確認します。以下は出力例です。

    ```shell
    ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

## こちらも参照 {#see-also}

-   [TiDB メモリ制御](/configure-memory-usage.md)
-   [TiKV メモリ パラメータのパフォーマンスを調整する](/tune-tikv-memory-performance.md)
