---
title: Troubleshoot TiDB OOM Issues
summary: Learn how to diagnose and resolve TiDB OOM (Out of Memory) issues.
---

# TiDB OOM の問題のトラブルシューティング {#troubleshoot-tidb-oom-issues}

このドキュメントでは、現象、原因、解決策、および診断情報を含む、TiDB OOM (メモリ不足) の問題をトラブルシューティングする方法について説明します。

## 典型的な OOM 現象 {#typical-oom-phenomena}

次に、いくつかの典型的な OOM 現象を示します。

-   クライアント側は次のエラーを報告します: `SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query` .

-   Grafana ダッシュボードには以下が表示されます。
    -   **TiDB** &gt;<strong>サーバー</strong>&gt;<strong>メモリ使用量</strong>は、 `process/heapInUse`メトリックが上昇し続け、しきい値に達すると突然ゼロに低下することを示しています。
    -   **TiDB** &gt;<strong>サーバー</strong>&gt;<strong>アップタイムが</strong>突然ゼロになりました。
    -   **TiDB-Runtime** &gt; <strong>Memory Usage は、</strong> `estimate-inuse`のメトリックが上昇し続けていることを示しています。

-   `tidb.log`を確認すると、次のログ エントリが見つかります。
    -   OOM に関するアラーム: `[WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]` 。詳細については、 [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)を参照してください。
    -   再起動に関するログ エントリ: `[INFO] [printer.go:33] ["Welcome to TiDB."]` .

## 全体的なトラブルシューティング プロセス {#overall-troubleshooting-process}

OOM の問題をトラブルシューティングするときは、次のプロセスに従います。

1.  OOM の問題かどうかを確認します。

    次のコマンドを実行して、オペレーティング システムのログを確認します。問題が発生した時刻付近に`oom-killer`ログがあれば、OOM の問題であることが確認できます。

    ```shell
    dmesg -T | grep tidb-server
    ```

    `oom-killer`を含むログの例を次に示します。

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

2.  それが OOM の問題であることを確認したら、OOM が配置またはデータベースによって引き起こされているかどうかをさらに調査できます。

    -   OOM の原因がデプロイの問題である場合は、リソースの構成とハイブリッド デプロイの影響を調査する必要があります。
    -   OOM の原因がデータベースの問題である場合、次のような原因が考えられます。
        -   TiDB は、大規模なクエリ、大規模な書き込み、データ インポートなどの大規模なデータ トラフィックを処理します。
        -   TiDB は、複数の SQL ステートメントが同時にリソースを消費するか、オペレーターの同時実行性が高い、高い同時実行性のシナリオにあります。
        -   TiDB にメモリリークがあり、リソースが解放されません。

    特定のトラブルシューティング方法については、次のセクションを参照してください。

## 典型的な原因と解決策 {#typical-causes-and-solutions}

通常、OOM の問題は次の原因で発生します。

-   [展開の問題](#deployment-issues)
-   [データベースの問題](#database-issues)
-   [クライアント側の問題](#client-side-issues)

### 展開の問題 {#deployment-issues}

以下は、不適切な展開による OOM のいくつかの原因です。

-   オペレーティング システムのメモリ容量が小さすぎます。
-   TiUP構成[`resource_control`](/tiup/tiup-cluster-topology-reference.md#global)は適切ではありません。
-   ハイブリッド展開 (TiDB と他のアプリケーションが同じサーバーに展開されていることを意味します) の場合、TiDB はリソース不足のために`oom-killer`て強制終了されます。

### データベースの問題 {#database-issues}

このセクションでは、データベースの問題によって引き起こされる OOM の原因と解決策について説明します。

> **ノート：**
>
> [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)を構成した場合、エラーが発生します: `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]` 。これは、データベースのメモリ使用量制御動作が原因です。これは正常な動作です。

#### SQL ステートメントを実行すると大量のメモリが消費される {#executing-sql-statements-consumes-too-much-memory}

OOM の問題のさまざまな原因に応じて、SQL ステートメントのメモリ使用量を減らすために次の手段を講じることができます。

-   たとえば、適切なインデックスがない、古い統計、またはオプティマイザのバグが原因で、SQL の実行計画が最適でない場合、SQL の間違った実行計画が選択される可能性があります。膨大な中間結果セットがメモリに蓄積されます。この場合、次の対策を検討してください。
    -   適切なインデックスを追加します。
    -   実行演算子には[ディスクこぼれ](/configure-memory-usage.md#disk-spill)機能を使用します。
    -   テーブル間の JOIN 順序を調整します。
    -   ヒントを使用して SQL ステートメントを最適化します。

-   一部の演算子と関数は、storageレベルへのプッシュ ダウンがサポートされていないため、中間結果セットが大量に蓄積されます。この場合、SQL ステートメントを改良するか、ヒントを使用して最適化し、プッシュ ダウンをサポートする関数または演算子を使用する必要があります。

-   実行計画には、演算子 HashAgg が含まれています。 HashAgg は複数のスレッドによって同時に実行されます。これは高速ですが、より多くのメモリを消費します。代わりに、 `STREAM_AGG()`を使用できます。

-   同時に読み取られるリージョンの数を減らすか、演算子の同時実行数を減らして、同時実行数が多いことによるメモリの問題を回避します。対応するシステム変数は次のとおりです。
    -   [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)
    -   [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    -   [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-new-in-v50)

-   問題が発生する時点に近づくと、セッションの同時実行性が高すぎます。この場合、TiDB ノードを追加して TiDB クラスターをスケールアウトすることを検討してください。

#### 大規模なトランザクションまたは大規模な書き込みが大量のメモリを消費する {#large-transactions-or-large-writes-consume-too-much-memory}

メモリ容量を計画する必要があります。トランザクションが実行されると、TiDB プロセスのメモリ使用量は、トランザクション サイズと比較して、最大でトランザクション サイズの 2 ～ 3 倍以上に拡大されます。

1 つの大きなトランザクションを複数の小さなトランザクションに分割できます。

#### 統計情報を収集してロードするプロセスで大量のメモリが消費される {#the-process-of-collecting-and-loading-statistical-information-consumes-too-much-memory}

TiDB ノードは、起動後に統計をメモリにロードする必要があります。 TiDB は、統計情報を収集するときにメモリを消費します。次の方法でメモリ使用量を制御できます。

-   サンプリング レートを指定し、特定の列の統計のみを収集し、同時実行数を`ANALYZE`減らします。
-   TiDB v6.1.0 以降、システム変数[`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)を使用して、統計情報のメモリ使用量を制御できます。
-   TiDB v6.1.0 以降、システム変数[`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)を使用して、TiDB が統計を更新するときの最大メモリ使用量を制御できます。

詳細については、 [統計入門](/statistics.md)を参照してください。

#### プリペアド ステートメントの使いすぎ {#prepared-statements-are-overused}

クライアント側は準備済みステートメントを作成し続けますが、実行しません[`deallocate prepare stmt`](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) 。これにより、メモリ消費が増加し続け、最終的に TiDB OOM がトリガーされます。その理由は、プリペアドステートメントによって占有されていたメモリが、セッションが閉じられるまで解放されないためです。これは、長時間の接続セッションでは特に重要です。

この問題を解決するには、次の対策を検討してください。

-   セッションのライフサイクルを調整します。
-   調整する[接続プールの`wait_timeout`と<code>max_execution_time</code>](/develop/dev-guide-connection-parameters.md#timeout-related-parameters) .
-   システム変数[`max_prepared_stmt_count`](/system-variables.md#max_prepared_stmt_count)を使用して、セッション内の準備済みステートメントの最大数を制御します。

#### <code>tidb_enable_rate_limit_action</code>が正しく構成されていません {#code-tidb-enable-rate-limit-action-code-is-not-configured-properly}

システム変数[`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)は、SQL ステートメントがデータの読み取りのみを行う場合に、メモリの使用を効果的に制御します。この変数が有効で、計算操作 (結合操作や集計操作など) が必要な場合、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)制御下にない可能性があり、OOM のリスクが高まります。

このシステム変数を無効にすることをお勧めします。 TiDB v6.3.0 以降、このシステム変数はデフォルトで無効になっています。

### クライアント側の問題 {#client-side-issues}

クライアント側で OOM が発生した場合は、次の点を調査してください。

-   **Grafana TiDB の [詳細]** &gt; <strong>[サーバー]</strong> &gt; <strong>[クライアント データ トラフィック]</strong>で傾向と速度を確認し、ネットワークがブロックされているかどうかを確認します。
-   間違った JDBC 構成パラメーターが原因でアプリケーション OOM が発生していないかどうかを確認してください。たとえば、ストリーミング読み取りの`defaultFetchSize`パラメータが正しく構成されていない場合、クライアント側にデータが大量に蓄積される可能性があります。

## OOM の問題をトラブルシューティングするために収集される診断情報 {#diagnostic-information-to-be-collected-to-troubleshoot-oom-issues}

OOM の問題の根本原因を突き止めるには、次の情報を収集する必要があります。

-   オペレーティング システムのメモリ関連の構成を収集します。
    -   TiUP構成: `resource_control.memory_limit`
    -   オペレーティング システムの構成:
        -   メモリー情報： `cat /proc/meminfo`
        -   カーネル パラメータ: `vm.overcommit_memory`
    -   NUMA 情報:
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

-   Grafana ダッシュボード ( **TiDB** &gt; <strong>Server</strong> &gt; <strong>Memory Usage )</strong>で TiDBメモリの毎日の使用量を確認します。

-   より多くのメモリを消費する SQL ステートメントを確認します。

    -   TiDB ダッシュボードで SQL ステートメント分析、スロー クエリ、およびメモリ使用量をビュー。
    -   `INFORMATION_SCHEMA`の`SLOW_QUERY`と`CLUSTER_SLOW_QUERY`確認してください。
    -   各 TiDB ノードで`tidb_slow_query.log`をチェックします。
    -   `grep "expensive_query" tidb.log`を実行して、対応するログ エントリを確認します。
    -   `EXPLAIN ANALYZE`を実行して、演算子のメモリ使用量を確認します。
    -   `SELECT * FROM information_schema.processlist;`を実行して、 `MEM`列の値を確認します。

-   メモリ使用量が多い場合は、次のコマンドを実行して TiDB プロファイル情報を収集します。

    ```shell
    curl -G http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

-   `grep "tidb-server has the risk of OOM" tidb.log`を実行して、TiDB サーバーによって収集されたアラート ファイルのパスを確認します。次に出力例を示します。

    ```shell
    ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]
    ```

## こちらもご覧ください {#see-also}

-   [TiDB メモリ制御](/configure-memory-usage.md)
-   [TiKV メモリ パラメータのパフォーマンスの調整](/tune-tikv-memory-performance.md)
