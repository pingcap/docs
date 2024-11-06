---
title: TiDB Cluster Alert Rules
summary: TiDB クラスターのアラート ルールについて学習します。
---

<!-- markdownlint-disable MD024 -->

# TiDBクラスタアラートルール {#tidb-cluster-alert-rules}

このドキュメントでは、TiDB、TiKV、PD、 TiFlash、TiDB Binlog、TiCDC、Node_exporter、Blackbox_exporter のアラート項目のルールの説明と解決策を含む、TiDB クラスター内のさまざまなコンポーネントのアラート ルールについて説明します。

重大度に応じて、アラート ルールは、緊急レベル、重大レベル、警告レベルの 3 つのカテゴリ (高から低の順) に分類されます。この重大度の区分は、以下の各コンポーネントのすべてのアラート項目に適用されます。

| 重大度レベル    | 説明                                                                                    |
| :-------- | :------------------------------------------------------------------------------------ |
| 緊急レベル     | サービスが利用できなくなる最も高い重大度レベル。緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。**すぐに手動による介入が必要です**。 |
| クリティカルレベル | サービスの可用性が低下します。重大レベルのアラートの場合、異常なメトリックを注意深く監視する必要があります。                                |
| 警告レベル     | 警告レベルのアラートは、問題またはエラーを通知するものです。                                                        |

## TiDBアラートルール {#tidb-alert-rules}

このセクションでは、TiDBコンポーネントのアラート ルールについて説明します。

### 緊急レベルの警報 {#emergency-level-alerts}

#### <code>TiDB_schema_error</code> {#code-tidb-schema-error-code}

-   アラートルール:

    `increase(tidb_session_schema_lease_error_total{type="outdated"}[15m]) > 0`

-   説明：

    最新のスキーマ情報は、1 つのリース内では TiDB に再ロードされません。TiDB がサービスの提供を継続できない場合、アラートがトリガーされます。

-   解決：

    これは、利用できないリージョンまたは TiKV タイムアウトによって発生することがよくあります。TiKV 監視項目を確認して問題を特定する必要があります。

#### <code>TiDB_tikvclient_region_err_total</code> {#code-tidb-tikvclient-region-err-total-code}

-   アラートルール:

    `increase(tidb_tikvclient_region_err_total[10m]) > 6000`

-   説明：

    TiDBサーバーは、自身のキャッシュ情報に従って TiKV のリージョンリーダーにアクセスします。リージョンリーダーが変更された場合、または現在の TiKVリージョン情報が TiDB キャッシュ内の情報と一致していない場合、リージョンキャッシュ エラーが発生します。エラーが 10 分間に 6000 回以上報告されると、アラートがトリガーされます。

-   解決：

    リーダーのバランスが取れているかどうかを確認するには、ビュー[**TiKV-詳細**&gt;**クラスタ**ダッシュボード](/grafana-tikv-dashboard.md#cluster)ビュー。

#### <code>TiDB_domain_load_schema_total</code> {#code-tidb-domain-load-schema-total-code}

-   アラートルール:

    `increase(tidb_domain_load_schema_total{type="failed"}[10m]) > 10`

-   説明：

    TiDB の最新のスキーマ情報を再ロードできなかった合計回数。再ロードの失敗が 10 分間に 10 回以上発生すると、アラートがトリガーされます。

-   解決：

    [`TiDB_schema_error`](#tidb_schema_error)と同じです。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>TiDB_server_panic_total</code> {#code-tidb-server-panic-total-code}

-   アラートルール:

    `increase(tidb_server_panic_total[10m]) > 0`

-   説明：

    パニックになった TiDB スレッドの数。panicが発生すると、アラートがトリガーされます。スレッドは頻繁に回復されますが、そうでない場合は、TiDB が頻繁に再起動されます。

-   解決：

    panicログを収集して問題を特定します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiDB_memory_abnormal</code> {#code-tidb-memory-abnormal-code}

-   アラートルール:

    `go_memstats_heap_inuse_bytes{job="tidb"} > 1e+10`

-   説明：

    TiDBメモリ使用量の監視。使用量が 10 G を超えると、アラートがトリガーされます。

-   解決：

    HTTP API を使用して、goroutine リークの問題をトラブルシューティングします。

#### <code>TiDB_query_duration</code> {#code-tidb-query-duration-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket[1m])) BY (le, instance)) > 1`

-   説明：

    TiDB でリクエストを処理する際のレイテンシー。リクエストの 99% の応答時間は 1 秒以内である必要があります。それ以外の場合は、アラートがトリガーされます。

-   解決：

    TiDB ログをビュー、キーワード`SLOW_QUERY`と`TIME_COP_PROCESS`を検索して、遅い SQL クエリを見つけます。

#### <code>TiDB_server_event_error</code> {#code-tidb-server-event-error-code}

-   アラートルール:

    `increase(tidb_server_event_total{type=~"server_start|server_hang"}[15m]) > 0`

-   説明：

    TiDB サービスで発生したイベントの数。次のイベントが発生するとアラートがトリガーされます。

    1.  start: TiDB サービスが開始されます。
    2.  ハング: 重大なレベルのイベント (現在、シナリオは 1 つだけ: TiDB がbinlogに書き込めない) が発生すると、TiDB は`hang`モードに入り、手動で強制終了されるのを待機します。

-   解決：

    -   サービスを回復するには、TiDB を再起動します。
    -   TiDB Binlogサービスが正常かどうかを確認します。

#### <code>TiDB_tikvclient_backoff_seconds_count</code> {#code-tidb-tikvclient-backoff-seconds-count-code}

-   アラートルール:

    `increase(tidb_tikvclient_backoff_seconds_count[10m]) > 10`

-   説明：

    TiDB が TiKV へのアクセスに失敗した場合の再試行回数。再試行回数が 10 分間に 10 回を超えると、アラートがトリガーされます。

-   解決：

    TiKV の監視ステータスをビュー。

#### <code>TiDB_monitor_time_jump_back_error</code> {#code-tidb-monitor-time-jump-back-error-code}

-   アラートルール:

    `increase(tidb_monitor_time_jump_back_total[10m]) > 0`

-   説明：

    TiDB を保持しているマシンの時間が巻き戻ると、アラートがトリガーされます。

-   解決：

    NTP 構成のトラブルシューティングを行います。

#### <code>TiDB_ddl_waiting_jobs</code> {#code-tidb-ddl-waiting-jobs-code}

-   アラートルール:

    `sum(tidb_ddl_waiting_jobs) > 5`

-   説明：

    TiDB で実行が保留中の DDL タスクの数が 5 を超えると、アラートがトリガーされます。

-   解決：

    `admin show ddl`実行して、時間のかかる`add index`操作が実行されているかどうかを確認します。

## PDアラートルール {#pd-alert-rules}

このセクションでは、PDコンポーネントのアラート ルールについて説明します。

### 緊急レベルの警報 {#emergency-level-alerts}

#### <code>PD_cluster_down_store_nums</code> {#code-pd-cluster-down-store-nums-code}

-   アラートルール:

    `(sum(pd_cluster_status{type="store_down_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PD は TiKV/ TiFlashハートビートを長時間受信していません (デフォルト設定は 30 分です)。

-   解決：

    -   TiKV/ TiFlashプロセスが正常かどうか、ネットワークが分離されているか、負荷が高すぎるかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV/ TiFlashインスタンスを回復できない場合は、オフラインにすることができます。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>PD_etcd_write_disk_latency</code> {#code-pd-etcd-write-disk-latency-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket[1m])) by (instance, job, le)) > 1`

-   説明：

    fsync 操作のレイテンシーが1 秒を超える場合、etcd が通常よりも遅い速度でディスクにデータを書き込んでいることを示します。PD リーダーのタイムアウトが発生したり、TSO を時間内にディスクに保存できなかったりして、クラスター全体のサービスがシャットダウンする可能性があります。

-   解決：

    -   書き込み速度が遅い原因を見つけます。システムに過負荷をかけているのは他のサービスである可能性があります。PD 自体が大量の CPU または I/O リソースを占有しているかどうかを確認できます。
    -   サービスを回復するには、PD を再起動するか、リーダーを手動で別の PD に転送してください。
    -   環境要因により問題のある PD インスタンスを回復できない場合は、オフラインにして交換してください。

#### <code>PD_miss_peer_region_count</code> {#code-pd-miss-peer-region-count-code}

-   アラートルール:

    `(sum(pd_regions_status{type="miss-peer-region-count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    リージョンレプリカの数が`max-replicas`より小さくなっています。

-   解決：

    -   ダウンしている、またはオフラインになっている TiKV マシンがあるかどうかを確認して、問題の原因を見つけます。
    -   リージョンのヘルスパネルを監視し、 `miss-peer-region-count`が継続的に減少しているかどうかを確認します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>PD_cluster_lost_connect_store_nums</code> {#code-pd-cluster-lost-connect-store-nums-code}

-   アラートルール:

    `(sum(pd_cluster_status{type="store_disconnected_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PD は 20 秒以内に TiKV/ TiFlashハートビートを受信しません。通常、TiKV/ TiFlashハートビートは 10 秒ごとに受信されます。

-   解決：

    -   TiKV/ TiFlashインスタンスが再起動されているかどうかを確認します。
    -   TiKV/ TiFlashプロセスが正常かどうか、ネットワークが分離されているかどうか、負荷が高すぎないかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV/ TiFlashインスタンスが回復できないことが確認できた場合は、オフラインにすることができます。
    -   TiKV/ TiFlashインスタンスを回復できるが、短期的には回復できないことが確認された場合は、 `max-down-time`の値を増やすことを検討できます。これにより、 TiKV/ TiFlashインスタンスが回復不能とみなされ、データが TiKV/ TiFlashから削除されることがなくなります。

#### <code>PD_cluster_unhealthy_tikv_nums</code> {#code-pd-cluster-unhealthy-tikv-nums-code}

-   アラートルール:

    `(sum(pd_cluster_status{type="store_unhealth_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    不健全なストアがあることを示します。この状況がしばらく続くと ( [`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)に設定され、デフォルトは`30m` )、ストアは`Offline`状態に変わり、 [`PD_cluster_down_store_nums`](#pd_cluster_down_store_nums)アラートがトリガーされる可能性が高くなります。

-   解決：

    TiKV ストアの状態を確認します。

#### <code>PD_cluster_low_space</code> {#code-pd-cluster-low-space-code}

-   アラートルール:

    `(sum(pd_cluster_status{type="store_low_space_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    TiKV/ TiFlashノードに十分なスペースがないことを示します。

-   解決：

    -   クラスター内のスペースが全体的に不足していないかどうかを確認します。不足している場合は、容量を増やします。
    -   リージョンバランスのスケジュールに問題がないか確認してください。問題がある場合は、データの分散が不均一になります。
    -   ログ、スナップショット、コアダンプなど、大量のディスク領域を占有するファイルがあるかどうかを確認します。
    -   データ量を減らすには、ノードのリージョンの重みを下げます。
    -   スペースを解放できない場合は、事前にノードをオフラインにすることを検討してください。これにより、ダウンタイムにつながるディスク容量不足を防止できます。

#### <code>PD_etcd_network_peer_latency</code> {#code-pd-etcd-network-peer-latency-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(etcd_network_peer_round_trip_time_seconds_bucket[1m])) by (To, instance, job, le)) > 1`

-   説明：

    PD ノード間のネットワークレイテンシーが高くなっています。リーダー タイムアウトと TSO ディスクstorageタイムアウトが発生し、クラスターのサービスに影響する可能性があります。

-   解決：

    -   ネットワークとシステムの負荷状態を確認します。
    -   環境要因により問題のある PD インスタンスを回復できない場合は、オフラインにして交換してください。

#### <code>PD_tidb_handle_requests_duration</code> {#code-pd-tidb-handle-requests-duration-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(pd_client_request_handle_requests_duration_seconds_bucket{type="tso"}[1m])) by (instance, job, le)) > 0.1`

-   説明：

    PD が TSO 要求を処理するのに時間がかかります。これは多くの場合、高負荷によって発生します。

-   解決：

    -   サーバーの負荷状況を確認してください。
    -   pprof を使用して PD の CPU プロファイルを分析します。
    -   PD リーダーを手動で切り替えます。
    -   環境要因により問題のある PD インスタンスを回復できない場合は、オフラインにして交換してください。

#### <code>PD_down_peer_region_nums</code> {#code-pd-down-peer-region-nums-code}

-   アラートルール:

    `(sum(pd_regions_status{type="down-peer-region-count"}) by (instance)  > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftリーダーによって報告された、応答しないピアがあるリージョンの数。

-   解決：

    -   ダウンしている TiKV、再起動したばかりの TiKV、またはビジー状態の TiKV があるかどうかを確認します。
    -   リージョンのヘルスパネルを監視し、 `down_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKV サーバー間のネットワークを確認します。

#### <code>PD_pending_peer_region_count</code> {#code-pd-pending-peer-region-count-code}

-   アラートルール:

    `(sum(pd_regions_status{type="pending-peer-region-count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftログが遅れているリージョンが多すぎます。スケジュールによって保留中のピアの数が少なくなるのは正常ですが、その数が多い場合は問題がある可能性があります。

-   解決：

    -   リージョンのヘルスパネルを監視し、 `pending_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKV サーバー間のネットワーク、特に十分な帯域幅があるかどうかを確認します。

#### <code>PD_leader_change</code> {#code-pd-leader-change-code}

-   アラートルール:

    `count(changes(pd_tso_events{type="save"}[10m]) > 0) >= 2`

-   説明：

    最近PDリーダーが交代しました。

-   解決：

    -   PD の再起動、リーダーの手動転送、リーダーの優先順位の調整などの人的要因を除外します。
    -   ネットワークとシステムの負荷状態を確認します。
    -   環境要因により問題のある PD インスタンスを回復できない場合は、オフラインにして交換してください。

#### <code>TiKV_space_used_more_than_80%</code> {#code-tikv-space-used-more-than-80-code}

-   アラートルール:

    `sum(pd_cluster_status{type="storage_size"}) / sum(pd_cluster_status{type="storage_capacity"}) * 100 > 80`

-   説明：

    クラスタースペースの 80% 以上が使用されています。

-   解決：

    -   容量を増やす必要があるかどうかを確認します。
    -   ログ、スナップショット、コアダンプなど、大量のディスク領域を占有するファイルがあるかどうかを確認します。

#### <code>PD_system_time_slow</code> {#code-pd-system-time-slow-code}

-   アラートルール:

    `changes(pd_tso_events{type="system_time_slow"}[10m]) >= 1`

-   説明：

    システム時間の巻き戻しが発生する可能性があります。

-   解決：

    システム時刻が正しく設定されているかどうかを確認します。

#### <code>PD_no_store_for_making_replica</code> {#code-pd-no-store-for-making-replica-code}

-   アラートルール:

    `increase(pd_checker_event_count{type="replica_checker", name="no_target_store"}[1m]) > 0`

-   説明：

    追加のレプリカを保存する適切なストアがありません。

-   解決：

    -   店内に十分なスペースがあるかどうかを確認してください。
    -   ラベル構成が設定されている場合は、それに応じて追加のレプリカ用のストアがあるかどうかを確認します。

#### <code>PD_cluster_slow_tikv_nums</code> {#code-pd-cluster-slow-tikv-nums-code}

-   アラートルール:

    `sum(pd_cluster_status{type="store_slow_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0`

-   説明：

    遅い TiKV ノードがあります`raftstore.inspect-interval`は、遅い TiKV ノードの検出を制御します。詳細については、 [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)参照してください。

-   解決：

    -   [**TiKV詳細**&gt; **PD**ダッシュボード](/grafana-tikv-dashboard.md#pd)を監視し、Store Slow Score メトリックを確認します。メトリック値が 80 を超えるノードを特定します。このノードは低速ノードとして検出されます。
    -   [**TiKV-詳細**&gt; **Raft IO**ダッシュボード](/grafana-tikv-dashboard.md#raft-io)を監視して、レイテンシーが増加するかどうかを確認します。レイテンシーが高い場合は、ディスクにボトルネックが存在する可能性があることを意味します。
    -   レイテンシーのタイムアウト制限を増やすには、 [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)構成項目をより大きな値に設定します。
    -   アラートされた TiKV ノードのパフォーマンスの問題とチューニング方法の詳細な分析については、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md#storage-async-write-duration-store-duration-and-apply-duration)参照してください。

## TiKVアラートルール {#tikv-alert-rules}

このセクションでは、TiKVコンポーネントのアラート ルールについて説明します。

### 緊急レベルの警報 {#emergency-level-alerts}

#### <code>TiKV_memory_used_too_fast</code> {#code-tikv-memory-used-too-fast-code}

-   アラートルール:

    `process_resident_memory_bytes{job=~"tikv",instance=~".*"} - (process_resident_memory_bytes{job=~"tikv",instance=~".*"} offset 5m) > 5*1024*1024*1024`

-   説明：

    現在、メモリに関する TiKV 監視項目はありません。Node_exporter を使用すると、クラスター内のマシンのメモリ使用量を監視できます。上記のルールは、メモリ使用量が 5 分以内に 5 GB を超えると (TiKV でメモリが占​​有される速度が速すぎる)、アラートがトリガーされることを示しています。

-   解決：

    `rocksdb.defaultcf`と`rocksdb.writecf`両方の`block-cache-size`値を調整します。

#### <code>TiKV_GC_can_not_work</code> {#code-tikv-gc-can-not-work-code}

-   アラートルール:

    `sum(increase(tikv_gcworker_gc_tasks_vec{task="gc"}[1d])) < 1 and (sum(increase(tikv_gc_compaction_filter_perform[1d])) < 1 and sum(increase(tikv_engine_event_total{db="kv", cf="write", type="compaction"}[1d])) >= 1)`

-   説明：

    GC が 24 時間以内に TiKV インスタンスで正常に実行されない場合、GC が正常に動作していないことを示します。GC が短期間で実行されなければ、それほど問題は発生しませんが、GC が停止し続けると、保持されるバージョンが増え続け、クエリの速度が低下します。

-   解決：

    1.  `SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME = "tikv_gc_leader_desc"`実行して、GC リーダーに対応する`tidb-server`見つけます。
    2.  `tidb-server`のログをビュー、grep gc_worker tidb.log;
    3.  この間に GC ワーカーがロックを解決していた (最後のログは「start resolve locks」) か、範囲を削除していた (最後のログは「start delete {number} ranges」) ことがわかった場合、GC プロセスは正常に実行されていることを意味します。それ以外の場合は、PingCAP またはコミュニティから[サポートを受ける](/support.md)返されます。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>TiKV_server_report_failure_msg_total</code> {#code-tikv-server-report-failure-msg-total-code}

-   アラートルール:

    `sum(rate(tikv_server_report_failure_msg_total{type="unreachable"}[10m])) BY (store_id) > 10`

-   説明：

    リモート TiKV に接続できないことを示します。

-   解決：

    1.  ネットワークがクリアかどうかを確認してください。
    2.  リモート TiKV がダウンしていないかどうかを確認します。
    3.  リモート TiKV がダウンしていない場合は、圧力が高すぎないかどうかを確認してください。 [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_channel_full_total</code> {#code-tikv-channel-full-total-code}

-   アラートルール:

    `sum(rate(tikv_channel_full_total[10m])) BY (type, instance) > 0`

-   説明：

    この問題は、多くの場合、 Raftstoreスレッドがスタックし、TiKV に高い圧力がかかっていることが原因で発生します。

-   解決：

    1.  [**TiKV-詳細**&gt; **Raft Propose**ダッシュボード](/grafana-tikv-dashboard.md#raft-propose)を見て、アラートされた TiKV ノードのRaft提案が他の TiKV ノードよりもはるかに高いかどうかを確認します。そうである場合、この TiKV に 1 つ以上のホット スポットがあることを意味します。ホット スポットのスケジューリングが適切に機能するかどうかを確認する必要があります。
    2.  [**TiKV-詳細**&gt; **Raft IO**ダッシュボード](/grafana-tikv-dashboard.md#raft-io)を見て、レイテンシーが増加するかどうかを確認します。レイテンシーが高い場合は、ディスクにボトルネックが存在する可能性があることを意味します。
    3.  [**TiKV-詳細**&gt;**Raftプロセス**ダッシュボード](/grafana-tikv-dashboard.md#raft-process)を見て、 `tick duration`が高いかどうかを確認します。高い場合は、 [`raftstore.raft-base-tick-interval`](/tikv-configuration-file.md#raft-base-tick-interval) `"2s"`に設定する必要があります。

#### <code>TiKV_write_stall</code> {#code-tikv-write-stall-code}

-   アラートルール:

    `delta(tikv_engine_write_stall[10m]) > 0`

-   説明：

    RocksDB への書き込み圧力が高すぎるため、停止が発生します。

-   解決：

    1.  ディスク モニターをビュー、ディスクの問題をトラブルシューティングします。
    2.  TiKV に書き込みホットスポットがあるかどうかを確認します。
    3.  `[rocksdb]`および`[raftdb]`構成では、 `max-sub-compactions`より大きな値に設定します。

#### <code>TiKV_raft_log_lag</code> {#code-tikv-raft-log-lag-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_log_lag_bucket[1m])) by (le, instance)) > 5000`

-   説明：

    この値が比較的大きい場合、 Follower がLeaderより大幅に遅れており、 Raft を正常に複製できないことを意味します。Followerが配置されている TiKV マシンがスタックしているかダウンしている可能性があります。

#### <code>TiKV_async_request_snapshot_duration_seconds</code> {#code-tikv-async-request-snapshot-duration-seconds-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="snapshot"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合、 Raftstoreの負荷圧力が高すぎることを意味し、すでにスタックしている可能性があります。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_async_request_write_duration_seconds</code> {#code-tikv-async-request-write-duration-seconds-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合、 Raft の書き込みに長い時間がかかることを意味します。

-   解決：

    1.  [**TiKV-詳細**&gt; **Raft提案**ダッシュボード](/grafana-tikv-dashboard.md#raft-propose)を監視し、アラートされた TiKV ノードの**サーバーあたりの 99% 提案待機期間**メトリックが他の TiKV ノードよりも大幅に高いかどうかを確認します。そうである場合、この TiKV ノードにホットスポットが存在することを示し、ホットスポットのスケジュールが適切に機能しているかどうかを確認する必要があります。
    2.  [**TiKV-詳細**&gt; **Raft IO**ダッシュボード](/grafana-tikv-dashboard.md#raft-io)を監視して、レイテンシーが増加するかどうかを確認します。レイテンシーが高い場合は、ディスクにボトルネックが存在する可能性があることを意味します。
    3.  アラートされた TiKV ノードのパフォーマンスの問題とチューニング方法の詳細な分析については、 [パフォーマンス分析とチューニング](/performance-tuning-methods.md#storage-async-write-duration-store-duration-and-apply-duration)参照してください。

#### <code>TiKV_coprocessor_request_wait_seconds</code> {#code-tikv-coprocessor-request-wait-seconds-code}

-   アラートルール:

    `histogram_quantile(0.9999, sum(rate(tikv_coprocessor_request_wait_seconds_bucket[1m])) by (le, instance, req)) > 10`

-   説明：

    この値が比較的大きい場合、コプロセッサーワーカーへの負荷が高いことを意味します。コプロセッサースレッドがスタックするほど遅いタスクがある可能性があります。

-   解決：

    1.  TiDB ログからスロー クエリ ログをビュー、クエリでインデックスまたは完全なテーブル スキャンが使用されているかどうか、または分析に必要かどうかを確認します。
    2.  ホットスポットがあるかどうかを確認します。
    3.  コプロセッサーモニターをビュー、 `coprocessor table/index scan`の`total`と`process`一致するかどうかを確認します。大きく異なる場合は、無効なクエリが多すぎることを示しています。7 `over seek bound`あるかどうかを確認できます。そうであれば、GC が時間内に処理できないバージョンが多すぎます。その場合は、並列 GC スレッドの数を増やす必要があります。

#### <code>TiKV_raftstore_thread_cpu_seconds_total</code> {#code-tikv-raftstore-thread-cpu-seconds-total-code}

-   アラートルール:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"raftstore_.*"}[1m])) by (instance) > 1.6`

-   説明：

    このルールは、Raftstoreによる CPU 使用率を監視します。値が高い場合、 Raftstoreスレッドへの負荷が大きいことを示します。

    アラートしきい値は[`raftstore.store-pool-size`](/tikv-configuration-file.md#store-pool-size)値の 80% です。3 `raftstore.store-pool-size`デフォルトで 2 なので、アラートしきい値は 1.6 になります。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_raft_append_log_duration_secs</code> {#code-tikv-raft-append-log-duration-secs-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログの追加にかかる時間コストを示します。この値が高い場合、通常は I/O がビジー状態であることを意味します。

#### <code>TiKV_raft_apply_log_duration_secs</code> {#code-tikv-raft-apply-log-duration-secs-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログの適用にかかる時間コストを示します。この値が高い場合、通常は I/O がビジー状態であることを意味します。

#### <code>TiKV_scheduler_latch_wait_duration_seconds</code> {#code-tikv-scheduler-latch-wait-duration-seconds-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_latch_wait_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

-   説明：

    書き込み操作がスケジューラでメモリロックを取得するまでの待機時間。この値が高い場合、書き込みの競合が多く発生している可能性があります。または、競合の原因となる一部の操作が完了するまでに長い時間がかかり、同じロックを待機している他の操作がブロックされている可能性があります。

-   解決：

    1.  Scheduler-All モニターでスケジューラ コマンドの実行時間をビュー、どのコマンドが最も時間がかかっているかを確認します。
    2.  Scheduler-All モニターでスケジューラ スキャンの詳細をビュー、 `total`と`process`一致するかどうかを確認します。大きく異なる場合は、無効なスキャンが多数あります。 `over seek bound`があるかどうかも確認できます。多すぎる場合は、GC が時間どおりに動作していないことを示します。
    3.  ストレージ モニターでstorageの非同期スナップショット/書き込み期間をビュー、 Raft操作が時間内に実行されているかどうかを確認します。

#### <code>TiKV_thread_apply_worker_cpu_seconds</code> {#code-tikv-thread-apply-worker-cpu-seconds-code}

-   アラートルール:

    `max(rate(tikv_thread_cpu_seconds_total{name=~"apply_.*"}[1m])) by (instance) > 0.9`

-   説明：

    適用Raftログ スレッドに大きな負荷がかかっており、制限に近づいているか、制限を超えています。これは、書き込みのバーストによって発生することがよくあります。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiKV_leader_drops</code> {#code-tikv-leader-drops-code}

-   アラートルール:

    `delta(tikv_pd_heartbeat_tick_total{type="leader"}[30s]) < -10`

-   説明：

    これは多くの場合、 Raftstoreスレッドがスタックしていることが原因で発生します。

-   解決：

    1.  [`TiKV_channel_full_total`](#tikv_channel_full_total)を参照してください。
    2.  TiKV の負荷が低い場合は、PD スケジューリングが頻繁すぎないか検討してください。PD ページの Operator Create パネルを表示して、PD スケジューリングのタイプと数を確認できます。

#### <code>TiKV_raft_process_ready_duration_secs</code> {#code-tikv-raft-process-ready-duration-secs-code}

-   アラートルール:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type='ready'}[1m])) by (le, instance, type)) > 2`

-   説明：

    Raft の準備の処理にかかる時間コストを示します。この値が大きい場合は、ログ追加タスクが停止していることが原因であることがほとんどです。

#### <code>TiKV_raft_process_tick_duration_secs</code> {#code-tikv-raft-process-tick-duration-secs-code}

-   アラートルール:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type='tick'}[1m])) by (le, instance, type)) > 2`

-   説明：

    Raftティックの処理にかかる時間コストを示します。この値が大きい場合は、多くの場合、領域が多すぎることが原因です。

-   解決：

    1.  `warn`や`error`などの上位レベルのログの使用を検討してください。
    2.  `[raftstore]`構成の下に`raft-base-tick-interval = "2s"`追加します。

#### <code>TiKV_scheduler_context_total</code> {#code-tikv-scheduler-context-total-code}

-   アラートルール:

    `abs(delta( tikv_scheduler_context_total[5m])) > 1000`

-   説明：

    スケジューラによって実行されている書き込みコマンドの数。この値が大きい場合、タスクが時間どおりに終了していないことを意味します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_scheduler_command_duration_seconds</code> {#code-tikv-scheduler-command-duration-seconds-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_command_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

-   説明：

    スケジューラ コマンドの実行にかかる時間コストを示します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_coprocessor_outdated_request_wait_seconds</code> {#code-tikv-coprocessor-outdated-request-wait-seconds-code}

-   アラートルール:

    `delta(tikv_coprocessor_outdated_request_wait_seconds_count[10m]) > 0`

-   説明：

    コプロセッサーによる期限切れのリクエストの待機時間。この値が大きい場合、コプロセッサーに高い負荷がかかっていることを意味します。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_coprocessor_pending_request</code> {#code-tikv-coprocessor-pending-request-code}

-   アラートルール:

    `delta(tikv_coprocessor_pending_request[10m]) > 5000`

-   説明：

    コプロセッサーのキューイング要求。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_batch_request_snapshot_nums</code> {#code-tikv-batch-request-snapshot-nums-code}

-   アラートルール:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[1m])) by (instance) / (count(tikv_thread_cpu_seconds_total{name=~"cop_.*"}) * 0.9) / count(count(tikv_thread_cpu_seconds_total) by (instance)) > 0`

-   説明：

    TiKV マシンのコプロセッサーCPU 使用率が 90% を超えています。

#### <code>TiKV_pending_task</code> {#code-tikv-pending-task-code}

-   アラートルール:

    `sum(tikv_worker_pending_task_total) BY (instance,name)  > 1000`

-   説明：

    TiKV の保留中のタスクの数。

-   解決：

    [**TiKV-詳細**&gt;**タスク**ダッシュボード](/grafana-tikv-dashboard.md#task)の`Worker pending tasks`番目のメトリックからどの種類のタスクの値が高いかを確認します。

#### <code>TiKV_low_space</code> {#code-tikv-low-space-code}

-   アラートルール:

    `sum(tikv_store_size_bytes{type="available"}) by (instance) / sum(tikv_store_size_bytes{type="capacity"}) by (instance) < 0.2`

-   説明：

    TiKV のデータ量が、構成されたノード容量またはマシンのディスク容量の 80% を超えています。

-   解決：

    -   ノードスペースのバランス状態を確認します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>TiKV_approximate_region_size</code> {#code-tikv-approximate-region-size-code}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_region_size_bucket[1m])) by (le)) > 1073741824`

-   説明：

    TiKV 分割チェッカーによってスキャンされるリージョンの最大おおよそのサイズは、1 分以内に継続的に 1 GB を超えます。

-   解決：

    リージョン分割の速度は書き込み速度よりも遅くなります。この問題を軽減するには、TiDB をバッチ分割をサポートするバージョン (&gt;= 2.1.0-rc1) に更新することをお勧めします。一時的に更新できない場合は、 `pd-ctl operator add split-region <region_id> --policy=approximate`使用してリージョンを手動で分割できます。

## TiFlashアラートルール {#tiflash-alert-rules}

TiFlashアラートルールの詳細な説明については、 [TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)参照してください。

## TiDBBinlogアラートルール {#tidb-binlog-alert-rules}

TiDB Binlogアラート ルールの詳細な説明については、 [TiDBBinlog監視ドキュメント](/tidb-binlog/monitor-tidb-binlog-cluster.md#alert-rules)参照してください。

## TiCDCアラートルール {#ticdc-alert-rules}

TiCDCアラートルールの詳細な説明については、 [TiCDCアラートルール](/ticdc/ticdc-alert-rules.md)参照してください。

## Node_exporter ホストアラートルール {#node-exporter-host-alert-rules}

このセクションでは、Node_exporter ホストのアラート ルールを示します。

### 緊急レベルの警報 {#emergency-level-alerts}

#### <code>NODE_disk_used_more_than_80%</code> {#code-node-disk-used-more-than-80-code}

-   アラートルール:

    `node_filesystem_avail_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} / node_filesystem_size_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} * 100 <= 20`

-   説明：

    マシンのディスク領域の使用率が 80% を超えています。

-   解決：

    -   マシンにログインし、コマンド`df -h`を実行してディスク領域の使用量を確認します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>NODE_disk_inode_more_than_80%</code> {#code-node-disk-inode-more-than-80-code}

-   アラートルール:

    `node_filesystem_files_free{fstype=~"(ext.|xfs)"} / node_filesystem_files{fstype=~"(ext.|xfs)"} * 100 < 20`

-   説明：

    マシン上のファイルシステムの inode 使用率が 80% を超えています。

-   解決：

    -   マシンにログインし、 `df -i`コマンドを実行してファイルシステムのノード使用状況を表示します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>NODE_disk_readonly</code> {#code-node-disk-readonly-code}

-   アラートルール:

    `node_filesystem_readonly{fstype=~"(ext.|xfs)"} == 1`

-   説明：

    ファイルシステムは読み取り専用であり、データを書き込むことはできません。これは、ディスク障害またはファイルシステムの破損によって発生することがよくあります。

-   解決：

    -   マシンにログインし、正常かどうかをテストするためのファイルを作成します。
    -   ディスク LED が正常かどうかを確認します。正常でない場合は、ディスクを交換し、マシンのファイルシステムを修復します。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>NODE_memory_used_more_than_80%</code> {#code-node-memory-used-more-than-80-code}

-   アラートルール:

    `(((node_memory_MemTotal_bytes-node_memory_MemFree_bytes-node_memory_Cached_bytes)/(node_memory_MemTotal_bytes)*100)) >= 80`

-   説明：

    マシンのメモリ使用量が80%を超えています。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストのメモリ パネルをビュー、使用済みメモリが高すぎるかどうか、使用可能なメモリが低すぎるかどうかを確認します。
    -   マシンにログインし、コマンド`free -m`を実行してメモリ使用量を表示します。コマンド`top`実行すると、メモリ使用量が過度に高い異常なプロセスがあるかどうかを確認できます。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>NODE_node_overload</code> {#code-node-node-overload-code}

-   アラートルール:

    `(node_load5 / count without (cpu, mode) (node_cpu_seconds_total{mode="system"})) > 1`

-   説明：

    マシンの CPU 負荷は比較的高いです。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストの CPU 使用率と負荷平均をビュー、それらが高すぎないかどうかを確認します。
    -   マシンにログインして`top`実行し、負荷平均と CPU 使用率をチェックして、CPU 使用率が過度に高い異常なプロセスがないか確認します。

#### <code>NODE_cpu_used_more_than_80%</code> {#code-node-cpu-used-more-than-80-code}

-   アラートルール:

    `avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance) * 100 <= 20`

-   説明：

    マシンのCPU使用率が80%を超えています。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストの CPU 使用率と負荷平均をビュー、それらが高すぎないかどうかを確認します。
    -   マシンにログインして`top`実行し、負荷平均と CPU 使用率をチェックして、CPU 使用率が過度に高い異常なプロセスがないか確認します。

#### <code>NODE_tcp_estab_num_more_than_50000</code> {#code-node-tcp-estab-num-more-than-50000-code}

-   アラートルール:

    `node_netstat_Tcp_CurrEstab > 50000`

-   説明：

    マシン上には「確立」ステータスの TCP リンクが 50,000 個以上あります。

-   解決：

    -   マシンにログインし、 `ss -s`実行して、現在のシステムで「estab」ステータスにある TCP リンクの数を確認します。
    -   `netstat`実行して、異常なリンクがないか確認します。

#### <code>NODE_disk_read_latency_more_than_32ms</code> {#code-node-disk-read-latency-more-than-32ms-code}

-   アラートルール:

    `((rate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_reads_completed_total{device=~".+"}[5m])) or (irate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_reads_completed_total{device=~".+"}[5m])) ) * 1000 > 32`

-   説明：

    ディスクの読み取りレイテンシーが 32 ミリ秒を超えています。

-   解決：

    -   Grafana ディスク パフォーマンス ダッシュボードを表示して、ディスクの状態を確認します。
    -   ディスク レイテンシ パネルを表示して、ディスクの読み取りレイテンシーを確認します。
    -   ディスク I/O 使用率パネルを表示して、I/O 使用率を確認します。

#### <code>NODE_disk_write_latency_more_than_16ms</code> {#code-node-disk-write-latency-more-than-16ms-code}

-   アラートルール:

    `((rate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_writes_completed_total{device=~".+"}[5m])) or (irate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_writes_completed_total{device=~".+"}[5m])))> 16`

-   説明：

    ディスクの書き込みレイテンシーが 16 ミリ秒を超えています。

-   解決：

    -   Grafana ディスク パフォーマンス ダッシュボードを表示して、ディスクの状態を確認します。
    -   ディスク レイテンシ パネルを表示して、ディスクの書き込みレイテンシーを確認します。
    -   ディスク I/O 使用率パネルを表示して、I/O 使用率を確認します。

## Blackbox_exporter TCP、ICMP、HTTP アラートルール {#blackbox-exporter-tcp-icmp-and-http-alert-rules}

このセクションでは、Blackbox_exporter TCP、ICMP、および HTTP のアラート ルールを示します。

### 緊急レベルの警報 {#emergency-level-alerts}

#### <code>TiDB_server_is_down</code> {#code-tidb-server-is-down-code}

-   アラートルール:

    `probe_success{group="tidb"} == 0`

-   説明：

    TiDB サービス ポートのプローブに失敗しました。

-   解決：

    -   TiDB サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   TiDB プロセスが存在するかどうかを確認します。
    -   監視マシンと TiDB マシン間のネットワークが正常かどうかを確認します。

#### <code>TiFlash_server_is_down</code> {#code-tiflash-server-is-down-code}

-   アラートルール:

    `probe_success{group="tiflash"} == 0`

-   説明：

    TiFlashサービス ポートのプローブに失敗しました。

-   解決：

    -   TiFlashサービスを提供するマシンがダウンしていないかどうかを確認します。
    -   TiFlashプロセスが存在するかどうかを確認します。
    -   監視マシンとTiFlashマシン間のネットワークが正常かどうかを確認します。

#### <code>Pump_server_is_down</code> {#code-pump-server-is-down-code}

-   アラートルール:

    `probe_success{group="pump"} == 0`

-   説明：

    ポンプのサービス ポートのプローブに失敗しました。

-   解決：

    -   ポンプサービスを提供するマシンがダウンしていないかどうかを確認します。
    -   ポンププロセスが存在するかどうかを確認します。
    -   監視機とポンプ機間のネットワークが正常かどうかを確認します。

#### <code>Drainer_server_is_down</code> {#code-drainer-server-is-down-code}

-   アラートルール:

    `probe_success{group="drainer"} == 0`

-   説明：

    Drainerサービス ポートのプローブに失敗しました。

-   解決：

    -   Drainerサービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Drainerプロセスが存在するかどうかを確認します。
    -   監視マシンとDrainerマシン間のネットワークが正常かどうかを確認します。

#### <code>TiKV_server_is_down</code> {#code-tikv-server-is-down-code}

-   アラートルール:

    `probe_success{group="tikv"} == 0`

-   説明：

    TiKV サービス ポートのプローブに失敗しました。

-   解決：

    -   TiKV サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   TiKV プロセスが存在するかどうかを確認します。
    -   監視マシンと TiKV マシン間のネットワークが正常かどうかを確認します。

#### <code>PD_server_is_down</code> {#code-pd-server-is-down-code}

-   アラートルール:

    `probe_success{group="pd"} == 0`

-   説明：

    PD サービス ポートのプローブに失敗しました。

-   解決：

    -   PD サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   PD プロセスが存在するかどうかを確認します。
    -   監視マシンとPDマシン間のネットワークが正常かどうかを確認します。

#### <code>Node_exporter_server_is_down</code> {#code-node-exporter-server-is-down-code}

-   アラートルール:

    `probe_success{group="node_exporter"} == 0`

-   説明：

    Node_exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Node_exporter サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Node_exporter プロセスが存在するかどうかを確認します。
    -   監視マシンとNode_exporterマシン間のネットワークが正常かどうかを確認します。

#### <code>Blackbox_exporter_server_is_down</code> {#code-blackbox-exporter-server-is-down-code}

-   アラートルール:

    `probe_success{group="blackbox_exporter"} == 0`

-   説明：

    Blackbox_Exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Blackbox_Exporter サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Blackbox_Exporter プロセスが存在するかどうかを確認します。
    -   監視マシンと Blackbox_Exporter マシン間のネットワークが正常かどうかを確認します。

#### <code>Grafana_server_is_down</code> {#code-grafana-server-is-down-code}

-   アラートルール:

    `probe_success{group="grafana"} == 0`

-   説明：

    Grafana サービス ポートのプローブに失敗しました。

-   解決：

    -   Grafana サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Grafana プロセスが存在するかどうかを確認します。
    -   監視マシンと Grafana マシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_server_is_down</code> {#code-pushgateway-server-is-down-code}

-   アラートルール:

    `probe_success{group="pushgateway"} == 0`

-   説明：

    Pushgateway サービス ポートのプローブに失敗しました。

-   解決：

    -   Pushgateway サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Pushgateway プロセスが存在するかどうかを確認します。
    -   監視マシンと Pushgateway マシン間のネットワークが正常かどうかを確認します。

#### <code>Kafka_exporter_is_down</code> {#code-kafka-exporter-is-down-code}

-   アラートルール:

    `probe_success{group="kafka_exporter"} == 0`

-   説明：

    Kafka_Exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Kafka_Exporter サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Kafka_Exporter プロセスが存在するかどうかを確認します。
    -   監視マシンと Kafka_Exporter マシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_metrics_interface</code> {#code-pushgateway-metrics-interface-code}

-   アラートルール:

    `probe_success{job="blackbox_exporter_http"} == 0`

-   説明：

    Pushgateway サービスの http インターフェースのプローブに失敗しました。

-   解決：

    -   Pushgateway サービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Pushgateway プロセスが存在するかどうかを確認します。
    -   監視マシンと Pushgateway マシン間のネットワークが正常かどうかを確認します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>BLACKER_ping_latency_more_than_1s</code> {#code-blacker-ping-latency-more-than-1s-code}

-   アラートルール:

    `max_over_time(probe_duration_seconds{job=~"blackbox_exporter.*_icmp"}[1m]) > 1`

-   説明：

    ping のレイテンシーが1 秒を超えています。

-   解決：

    -   Grafana Blackbox Exporter ページで 2 つのノード間の pingレイテンシーをビュー、遅延が高すぎないかどうかを確認します。
    -   Grafana Node Exporter ページの TCP パネルをチェックして、パケット損失があるかどうかを確認します。
