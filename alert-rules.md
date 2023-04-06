---
title: TiDB Cluster Alert Rules
summary: Learn the alert rules in a TiDB cluster.
---

<!-- markdownlint-disable MD024 -->

# TiDBクラスタアラート ルール {#tidb-cluster-alert-rules}

このドキュメントでは、TiDB、TiKV、PD、 TiFlash、TiDB Binlog、TiCDC、Node_exporter、および Blackbox_exporter のアラート項目のルールの説明と解決策を含む、TiDB クラスター内のさまざまなコンポーネントのアラート ルールについて説明します。

重大度レベルに応じて、アラート ルールは 3 つのカテゴリ (高から低) に分類されます: 緊急レベル、重大レベル、警告レベルです。この重大度レベルの区分は、以下の各コンポーネントのすべてのアラート項目に適用されます。

| 重大度       | 説明                                                                                 |
| :-------- | :--------------------------------------------------------------------------------- |
| 緊急レベル     | サービスが利用できない最高の重大度レベル。緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。**手動による介入がすぐに必要です**。 |
| クリティカルレベル | サービスの可用性の低下。重大レベルのアラートについては、異常なメトリックを注意深く監視する必要があります。                              |
| 警告レベル     | 警告レベルのアラートは、問題またはエラーのリマインダーです。                                                     |

## TiDB アラート ルール {#tidb-alert-rules}

このセクションでは、TiDBコンポーネントのアラート ルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiDB_schema_error</code> {#code-tidb-schema-error-code}

-   アラート ルール:

    `increase(tidb_session_schema_lease_error_total{type="outdated"}[15m]) > 0`

-   説明：

    1 つのリース内で最新のスキーマ情報が TiDB にリロードされません。 TiDB がサービスの提供を継続できない場合、アラートがトリガーされます。

-   解決：

    多くの場合、利用できないリージョンまたは TiKV タイムアウトが原因です。 TiKV 監視項目を確認して、問題を特定する必要があります。

#### <code>TiDB_tikvclient_region_err_total</code> {#code-tidb-tikvclient-region-err-total-code}

-   アラート ルール:

    `increase(tidb_tikvclient_region_err_total[10m]) > 6000`

-   説明：

    TiDB が TiKV にアクセスすると、 リージョンエラーが発生します。エラーが 10 分間に 6000 回以上報告されると、アラートがトリガーされます。

-   解決：

    TiKV の監視ステータスをビュー。

#### <code>TiDB_domain_load_schema_total</code> {#code-tidb-domain-load-schema-total-code}

-   アラート ルール:

    `increase(tidb_domain_load_schema_total{type="failed"}[10m]) > 10`

-   説明：

    TiDB で最新のスキーマ情報をリロードできなかった合計回数。リロードの失敗が 10 分間に 10 回以上発生すると、アラートがトリガーされます。

-   解決：

    [`TiDB_schema_error`](#tidb_schema_error)と同じ。

#### <code>TiDB_monitor_keep_alive</code> {#code-tidb-monitor-keep-alive-code}

-   アラート ルール:

    `increase(tidb_monitor_keep_alive_total[10m]) < 100`

-   説明：

    TiDB プロセスがまだ存在するかどうかを示します。 `tidb_monitor_keep_alive_total`の回数が 10 分間で 100 回未満に増加した場合、TiDB プロセスは既に終了している可能性があり、アラートがトリガーされます。

-   解決：

    -   TiDB プロセスがメモリ不足になっていないかどうかを確認します。
    -   マシンが再起動したかどうかを確認します。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>TiDB_server_panic_total</code> {#code-tidb-server-panic-total-code}

-   アラート ルール:

    `increase(tidb_server_panic_total[10m]) > 0`

-   説明：

    パニック状態の TiDB スレッドの数。panicが発生すると、アラートがトリガーされます。スレッドは頻繁に回復されます。そうしないと、TiDB が頻繁に再起動します。

-   解決：

    panicログを収集して問題を特定します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiDB_memory_abnormal</code> {#code-tidb-memory-abnormal-code}

-   アラート ルール:

    `go_memstats_heap_inuse_bytes{job="tidb"} > 1e+10`

-   説明：

    TiDBメモリ使用量の監視。使用量が 10 G を超えると、アラートがトリガーされます。

-   解決：

    HTTP API を使用して、ゴルーチン リークの問題をトラブルシューティングします。

#### <code>TiDB_query_duration</code> {#code-tidb-query-duration-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket[1m])) BY (le, instance)) > 1`

-   説明：

    TiDB でのリクエスト処理のレイテンシー。 99 パーセンタイルのレイテンシーが1 秒を超えると、アラートがトリガーされます。

-   解決：

    TiDB ログをビュー、 `SLOW_QUERY`と`TIME_COP_PROCESS`キーワードを検索して、遅い SQL クエリを見つけます。

#### <code>TiDB_server_event_error</code> {#code-tidb-server-event-error-code}

-   アラート ルール:

    `increase(tidb_server_event_total{type=~"server_start|server_hang"}[15m]) > 0`

-   説明：

    TiDB サービスで発生したイベントの数。次のイベントが発生すると、アラートがトリガーされます。

    1.  start: TiDB サービスが開始されます。
    2.  ハング: 重大レベルのイベント (現在のところ、TiDB が binlog を書き込めないシナリオは 1 つしかありません) が発生すると、TiDB は`hang`モードに入り、手動で強制終了されるのを待ちます。

-   解決：

    -   TiDB を再起動して、サービスを回復します。
    -   TiDB Binlogサービスが正常かどうかを確認します。

#### <code>TiDB_tikvclient_backoff_seconds_count</code> {#code-tidb-tikvclient-backoff-seconds-count-code}

-   アラート ルール:

    `increase(tidb_tikvclient_backoff_seconds_count[10m]) > 10`

-   説明：

    TiDB が TiKV へのアクセスに失敗した場合のリトライ回数。再試行回数が 10 分間で 10 回を超えると、アラートがトリガーされます。

-   解決：

    TiKV の監視ステータスをビュー。

#### <code>TiDB_monitor_time_jump_back_error</code> {#code-tidb-monitor-time-jump-back-error-code}

-   アラート ルール:

    `increase(tidb_monitor_time_jump_back_total[10m]) > 0`

-   説明：

    TiDB を保持するマシンの時間が巻き戻されると、アラートがトリガーされます。

-   解決：

    NTP 構成をトラブルシューティングします。

#### <code>TiDB_ddl_waiting_jobs</code> {#code-tidb-ddl-waiting-jobs-code}

-   アラート ルール:

    `sum(tidb_ddl_waiting_jobs) > 5`

-   説明：

    TiDB で実行待ちの DDL タスクの数が 5 を超えると、アラートがトリガーされます。

-   解決：

    `admin show ddl`を実行して実行中の`add index`時間のかかる操作がないかどうかを確認します。

## PD アラート ルール {#pd-alert-rules}

このセクションでは、PDコンポーネントのアラート ルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>PD_cluster_down_store_nums</code> {#code-pd-cluster-down-store-nums-code}

-   アラート ルール:

    `(sum(pd_cluster_status{type="store_down_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PD は長い間 TiKV/ TiFlashハートビートを受信していません (デフォルト設定は 30 分です)。

-   解決：

    -   TiKV/ TiFlashプロセスが正常であるか、ネットワークが分離されているか、負荷が高すぎるかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV/ TiFlashインスタンスを復旧できない場合は、オフラインにすることができます。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>PD_etcd_write_disk_latency</code> {#code-pd-etcd-write-disk-latency-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket[1m])) by (instance, job, le)) > 1`

-   説明：

    fsync 操作のレイテンシーが1 秒を超える場合は、etcd が通常より遅い速度でデータをディスクに書き込むことを示します。 PD リーダーがタイムアウトしたり、TSO を時間内にディスクに保存できなかったりして、クラスター全体のサービスがシャットダウンする可能性があります。

-   解決：

    -   遅い書き込みの原因を見つけます。システムに過負荷をかけているのは、他のサービスである可能性があります。 PD 自体が大量の CPU や I/O リソースを占有しているかどうかを確認できます。
    -   サービスを回復するには、PD を再起動するか、リーダーを別の PD に手動で転送してください。
    -   問題のある PD インスタンスが環境要因により回復できない場合は、オフラインにして置き換えます。

#### <code>PD_miss_peer_region_count</code> {#code-pd-miss-peer-region-count-code}

-   アラート ルール:

    `(sum(pd_regions_status{type="miss-peer-region-count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    リージョンレプリカの数が`max-replicas`の値よりも小さい。

-   解決：

    -   ダウンまたはオフラインになっている TiKV マシンがあるかどうかを確認して、問題の原因を見つけます。
    -   リージョンのヘルス パネルを見て、 `miss-peer-region-count`が継続的に減少しているかどうかを確認します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>PD_cluster_lost_connect_store_nums</code> {#code-pd-cluster-lost-connect-store-nums-code}

-   アラート ルール:

    `(sum(pd_cluster_status{type="store_disconnected_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PD は 20 秒以内に TiKV/ TiFlashハートビートを受信しません。通常、TiKV/ TiFlash のハートビートは10 秒ごとに送信されます。

-   解決：

    -   TiKV/ TiFlashインスタンスが再起動されているかどうかを確認します。
    -   TiKV/ TiFlashプロセスが正常であるか、ネットワークが分離されているか、負荷が高すぎるかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV/ TiFlashインスタンスが復旧できないことを確認したら、オフラインにすることができます。
    -   TiKV/ TiFlashインスタンスを回復できるが、短期的には回復できないことが確認された場合は、 `max-down-time`の値を増やすことを検討できます。これにより、TiKV/ TiFlashインスタンスが回復不能と見なされたり、データが TiKV/ TiFlashから削除されたりするのを防ぐことができます。

#### <code>PD_cluster_low_space</code> {#code-pd-cluster-low-space-code}

-   アラート ルール:

    `(sum(pd_cluster_status{type="store_low_space_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    TiKV/ TiFlashノードに十分なスペースがないことを示します。

-   解決：

    -   クラスター内のスペースが一般的に不足しているかどうかを確認します。その場合は、容量を増やしてください。
    -   リージョンバランス スケジューリングに問題があるかどうかを確認します。もしそうなら、それは不均一なデータ分布につながります。
    -   ログ、スナップショット、コアダンプなど、ディスク容量を多く占有するファイルがないか確認してください。
    -   ノードのリージョンの重みを下げて、データ量を減らします。
    -   スペースを解放できない場合は、積極的にノードをオフラインにすることを検討してください。これにより、ダウンタイムにつながるディスク容量の不足を防ぎます。

#### <code>PD_etcd_network_peer_latency</code> {#code-pd-etcd-network-peer-latency-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(etcd_network_peer_round_trip_time_seconds_bucket[1m])) by (To, instance, job, le)) > 1`

-   説明：

    PD ノード間のネットワークレイテンシーが大きい。これは、クラスターのサービスに影響を与えるリーダー タイムアウトおよび TSO ディスク ストレージ タイムアウトにつながる可能性があります。

-   解決：

    -   ネットワークとシステムの負荷状態を確認してください。
    -   問題のある PD インスタンスが環境要因により回復できない場合は、オフラインにして置き換えます。

#### <code>PD_tidb_handle_requests_duration</code> {#code-pd-tidb-handle-requests-duration-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(pd_client_request_handle_requests_duration_seconds_bucket{type="tso"}[1m])) by (instance, job, le)) > 0.1`

-   説明：

    PD が TSO 要求を処理するには、より長い時間がかかります。多くの場合、高負荷が原因です。

-   解決：

    -   サーバーの負荷状況を確認してください。
    -   pprof を使用して、PD の CPU プロファイルを分析します。
    -   PD リーダーを手動で切り替えます。
    -   問題のある PD インスタンスが環境要因により回復できない場合は、オフラインにして置き換えます。

#### <code>PD_down_peer_region_nums</code> {#code-pd-down-peer-region-nums-code}

-   アラート ルール:

    `(sum(pd_regions_status{type="down-peer-region-count"}) by (instance)  > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftリーダーによって報告された応答しないピアを持つリージョンの数。

-   解決：

    -   停止中、再起動したばかり、またはビジー状態の TiKV があるかどうかを確認します。
    -   リージョンのヘルス パネルを見て、 `down_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKV サーバー間のネットワークを確認します。

#### <code>PD_pending_peer_region_count</code> {#code-pd-pending-peer-region-count-code}

-   アラート ルール:

    `(sum(pd_regions_status{type="pending-peer-region-count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftログが遅れているリージョンが多すぎます。スケジューリングによって保留中のピアの数が少なくなるのは正常ですが、数が多いままである場合は、問題が発生している可能性があります。

-   解決：

    -   リージョンのヘルス パネルを見て、 `pending_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKV サーバー間のネットワーク、特に十分な帯域幅があるかどうかを確認してください。

#### <code>PD_leader_change</code> {#code-pd-leader-change-code}

-   アラート ルール:

    `count(changes(pd_tso_events{type="save"}[10m]) > 0) >= 2`

-   説明：

    最近 PD リーダーが交代しました。

-   解決：

    -   PD の再起動、リーダーの手動移動、リーダーの優先順位の調整などの人的要因を除外します。
    -   ネットワークとシステムの負荷状態を確認してください。
    -   問題のある PD インスタンスが環境要因により回復できない場合は、オフラインにして置き換えます。

#### <code>TiKV_space_used_more_than_80%</code> {#code-tikv-space-used-more-than-80-code}

-   アラート ルール:

    `sum(pd_cluster_status{type="storage_size"}) / sum(pd_cluster_status{type="storage_capacity"}) * 100 > 80`

-   説明：

    クラスタ領域の 80% 以上が占有されています。

-   解決：

    -   容量を増やす必要があるかどうかを確認します。
    -   ログ、スナップショット、コアダンプなど、ディスク容量を多く占有するファイルがないか確認してください。

#### <code>PD_system_time_slow</code> {#code-pd-system-time-slow-code}

-   アラート ルール:

    `changes(pd_tso_events{type="system_time_slow"}[10m]) >= 1`

-   説明：

    システム時間の巻き戻しが発生する可能性があります。

-   解決：

    システム時刻が正しく構成されているかどうかを確認します。

#### <code>PD_no_store_for_making_replica</code> {#code-pd-no-store-for-making-replica-code}

-   アラート ルール:

    `increase(pd_checker_event_count{type="replica_checker", name="no_target_store"}[1m]) > 0`

-   説明：

    追加のレプリカに適したストアがありません。

-   解決：

    -   店内に十分なスペースがあるかどうかを確認してください。
    -   ラベル構成が構成されている場合は、ラベル構成に従って、追加のレプリカ用のストアがあるかどうかを確認します。

#### <code>PD_cluster_slow_tikv_nums</code> {#code-pd-cluster-slow-tikv-nums-code}

-   アラート ルール:

    `sum(pd_cluster_status{type="store_slow_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0`

-   説明：

    遅い TiKV ノードがあります。 `raftstore.inspect-interval` TiKV 低速ノードの検出を制御します。詳細については、 [`raftstore.inspect-interval`](/tikv-configuration-file.md#inspect-interval)を参照してください。

-   解決：

    -   ストアのパフォーマンスが適切かどうかを確認します。
    -   `raftstore.inspect-interval`構成項目をより大きな値に設定して、レイテンシーのタイムアウト制限を増やします。

## TiKV アラート ルール {#tikv-alert-rules}

このセクションでは、TiKVコンポーネントのアラート ルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiKV_memory_used_too_fast</code> {#code-tikv-memory-used-too-fast-code}

-   アラート ルール:

    `process_resident_memory_bytes{job=~"tikv",instance=~".*"} - (process_resident_memory_bytes{job=~"tikv",instance=~".*"} offset 5m) > 5*1024*1024*1024`

-   説明：

    現在、メモリに関するTiKV監視項目はありません。 Node_exporter によって、クラスタ内のマシンのメモリ使用量を監視できます。上記のルールは、メモリ使用量が 5 分以内に 5 GB を超えた場合 (TiKV でメモリが急速に占有されている場合)、アラートがトリガーされることを示しています。

-   解決：

    `rockdb.defaultcf`と`rocksdb.writecf`の両方の`block-cache-size`値を調整します。

#### <code>TiKV_GC_can_not_work</code> {#code-tikv-gc-can-not-work-code}

-   アラート ルール:

    `sum(increase(tikv_gcworker_gc_tasks_vec{task="gc"}[1d])) < 1 and (sum(increase(tikv_gc_compaction_filter_perform[1d])) < 1 and sum(increase(tikv_engine_event_total{db="kv", cf="write", type="compaction"}[1d])) >= 1)`

-   説明：

    24 時間以内に TiKV インスタンスで GC が正常に実行されません。これは、GC が適切に機能していないことを示しています。 GC が短期間実行されなくても、大きな問題は発生しません。しかし、GC がダウンし続けると、ますます多くのバージョンが保持されるため、クエリが遅くなります。

-   解決：

    1.  `SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME = "tikv_gc_leader_desc"`を実行して、GC リーダーに対応する`tidb-server`見つけます。
    2.  `tidb-server`のログをビュー、grep gc_worker tidb.log;
    3.  この間に GC ワーカーがロックの解決 (最後のログは「ロックの解決開始」) または範囲の削除 (最後のログは「{番号} 範囲の削除の開始」) を行っていることがわかった場合は、GC プロセスが実行されていることを意味します。通常は。それ以外の場合は、 [support@pingcap.com](mailto:support@pingcap.com)に連絡してこの問題を解決してください。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>TiKV_server_report_failure_msg_total</code> {#code-tikv-server-report-failure-msg-total-code}

-   アラート ルール:

    `sum(rate(tikv_server_report_failure_msg_total{type="unreachable"}[10m])) BY (store_id) > 10`

-   説明：

    リモート TiKV が接続できないことを示します。

-   解決：

    1.  ネットワークがクリアかどうかを確認します。
    2.  リモート TiKV がダウンしているかどうかを確認します。
    3.  リモート TiKV がダウンしていない場合は、圧力が高すぎるかどうかを確認します。 [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_channel_full_total</code> {#code-tikv-channel-full-total-code}

-   アラート ルール:

    `sum(rate(tikv_channel_full_total[10m])) BY (type, instance) > 0`

-   説明：

    この問題は、スタックした Raftstore スレッドと TiKV への高圧が原因であることがよくあります。

-   解決：

    1.  Raft Propose モニターを監視し、アラートが発生した TiKV ノードのRaft提案が他の TiKV ノードよりもはるかに高いかどうかを確認します。その場合、この TiKV に 1 つ以上のホット スポットがあることを意味します。ホット スポット スケジューリングが適切に機能するかどうかを確認する必要があります。
    2.  Raft I/O モニターを監視し、レイテンシーが増加するかどうかを確認します。レイテンシーが高い場合は、ディスクにボトルネックが存在する可能性があることを意味します。実現可能だが安全でない解決策の 1 つは、 `sync-log`を`false`に設定することです。
    3.  Raftプロセス モニターを見て、ティックの持続時間が長いかどうかを確認します。その場合は、 `[raftstore]`構成の下に`raft-base-tick-interval = "2s"`を追加する必要があります。

#### <code>TiKV_write_stall</code> {#code-tikv-write-stall-code}

-   アラート ルール:

    `delta(tikv_engine_write_stall[10m]) > 0`

-   説明：

    RocksDB の書き込み圧力が高すぎて、ストールが発生します。

-   解決：

    1.  ディスク モニターをビュー、ディスクの問題をトラブルシューティングします。
    2.  TiKV に書き込みホット スポットがあるかどうかを確認します。
    3.  `[rocksdb]`と`[raftdb]`構成では、 `max-sub-compactions`をより大きな値に設定します。

#### <code>TiKV_raft_log_lag</code> {#code-tikv-raft-log-lag-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_log_lag_bucket[1m])) by (le, instance)) > 5000`

-   説明：

    この値が比較的大きい場合は、 Follower がLeaderに大きく遅れをとっており、 Raft を正常に複製できないことを意味します。Followerが配置されている TiKV マシンがスタックまたはダウンしていることが原因である可能性があります。

#### <code>TiKV_async_request_snapshot_duration_seconds</code> {#code-tikv-async-request-snapshot-duration-seconds-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="snapshot"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合は、Raftstore の負荷が高すぎることを意味し、すでにスタックしている可能性があります。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_async_request_write_duration_seconds</code> {#code-tikv-async-request-write-duration-seconds-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合、 Raft の書き込みに時間がかかることを意味します。

-   解決：

    1.  Raftstore の圧力を確認します。 [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。
    2.  適用ワーカー スレッドの圧力を確認します。

#### <code>TiKV_coprocessor_request_wait_seconds</code> {#code-tikv-coprocessor-request-wait-seconds-code}

-   アラート ルール:

    `histogram_quantile(0.9999, sum(rate(tikv_coprocessor_request_wait_seconds_bucket[1m])) by (le, instance, req)) > 10`

-   説明：

    この値が比較的大きい場合は、コプロセッサーワーカーへのプレッシャーが高いことを意味します。コプロセッサー・スレッドをスタックさせる遅いタスクがある可能性があります。

-   解決：

    1.  TiDB ログからスロー クエリ ログをビュー、クエリでインデックスまたはフル テーブル スキャンが使用されているかどうか、または分析に必要かどうかを確認します。
    2.  ホット スポットがあるかどうかを確認します。
    3.  コプロセッサーモニタをビュー、 `total`と`process` in `coprocessor table/index scan`が一致するかどうかを確認します。大きく異なる場合は、無効なクエリが多すぎることを示しています。 `over seek bound`があるかどうかがわかります。その場合、GC が時間内に処理できないバージョンが多すぎます。次に、並列 GC スレッドの数を増やす必要があります。

#### <code>TiKV_raftstore_thread_cpu_seconds_total</code> {#code-tikv-raftstore-thread-cpu-seconds-total-code}

-   アラート ルール:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"raftstore_.*"}[1m])) by (instance, name) > 1.6`

-   説明：

    Raftstore スレッドへの圧力が高すぎます。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_raft_append_log_duration_secs</code> {#code-tikv-raft-append-log-duration-secs-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログを追加する時間コストを示します。値が高い場合は、通常、I/O がビジー状態であることを意味します。

#### <code>TiKV_raft_apply_log_duration_secs</code> {#code-tikv-raft-apply-log-duration-secs-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログを適用する時間コストを示します。値が高い場合は、通常、I/O がビジー状態であることを意味します。

#### <code>TiKV_scheduler_latch_wait_duration_seconds</code> {#code-tikv-scheduler-latch-wait-duration-seconds-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_latch_wait_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

-   説明：

    書き込み操作がスケジューラでメモリロックを取得するまでの待機時間。値が高い場合は、多数の書き込み競合が発生している可能性があります。または、競合につながる一部の操作が完了するまでに時間がかかり、同じロックを待機する他の操作がブロックされている可能性があります。

-   解決：

    1.  Scheduler-All モニターでスケジューラ コマンドの所要時間をビュー、最も時間がかかるコマンドを確認します。
    2.  Scheduler-All モニターでスケジューラ スキャンの詳細をビュー、 `total`と`process`一致するかどうかを確認します。それらが大きく異なる場合、多くの無効なスキャンがあります。 `over seek bound`があるかどうかもわかります。多すぎる場合は、GC が間に合わないことを示しています。
    3.  Storage Monitor でストレージ非同期スナップショット/書き込み期間をビュー、 Raft操作が時間内に実行されているかどうかを確認します。

#### <code>TiKV_thread_apply_worker_cpu_seconds</code> {#code-tikv-thread-apply-worker-cpu-seconds-code}

-   アラート ルール:

    `max(rate(tikv_thread_cpu_seconds_total{name=~"apply_.*"}[1m])) by (instance) > 0.9`

-   説明：

    適用Raftログ スレッドは大きな負荷にさらされており、限界に近づいているか、限界を超えています。これは多くの場合、書き込みのバーストによって発生します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiKV_leader_drops</code> {#code-tikv-leader-drops-code}

-   アラート ルール:

    `delta(tikv_pd_heartbeat_tick_total{type="leader"}[30s]) < -10`

-   説明：

    多くの場合、Raftstore スレッドのスタックが原因です。

-   解決：

    1.  [`TiKV_channel_full_total`](#tikv_channel_full_total)を参照してください。
    2.  TiKV へのプレッシャーが少ない場合は、PD のスケジューリングが頻繁すぎるかどうかを検討してください。 PD ページの Operator Create パネルを表示し、PD スケジューリングのタイプと数を確認できます。

#### <code>TiKV_raft_process_ready_duration_secs</code> {#code-tikv-raft-process-ready-duration-secs-code}

-   アラート ルール:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type='ready'}[1m])) by (le, instance, type)) > 2`

-   説明：

    Raft Ready を処理するための時間コストを示します。この値が大きい場合は、多くの場合、ログ追加タスクのスタックが原因です。

#### <code>TiKV_raft_process_tick_duration_secs</code> {#code-tikv-raft-process-tick-duration-secs-code}

-   アラート ルール:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type=’tick’}[1m])) by (le, instance, type)) > 2`

-   説明：

    Raftティックを処理する時間コストを示します。この値が大きい場合は、リージョンが多すぎることが原因であることがよくあります。

-   解決：

    1.  `warn`や`error`などの上位レベルのログの使用を検討してください。
    2.  `[raftstore]`構成の下に`raft-base-tick-interval = "2s"`を追加します。

#### <code>TiKV_scheduler_context_total</code> {#code-tikv-scheduler-context-total-code}

-   アラート ルール:

    `abs(delta( tikv_scheduler_context_total[5m])) > 1000`

-   説明：

    スケジューラによって実行されている書き込みコマンドの数。この値が大きい場合、タスクがタイムリーに終了していないことを意味します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_scheduler_command_duration_seconds</code> {#code-tikv-scheduler-command-duration-seconds-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_command_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

-   説明：

    スケジューラ コマンドを実行する時間コストを示します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_coprocessor_outdated_request_wait_seconds</code> {#code-tikv-coprocessor-outdated-request-wait-seconds-code}

-   アラート ルール:

    `delta(tikv_coprocessor_outdated_request_wait_seconds_count[10m]) > 0`

-   説明：

    コプロセッサーによる期限切れの要求の待機時間。この値が大きい場合、 コプロセッサーに大きな負荷がかかっていることを意味します。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_coprocessor_pending_request</code> {#code-tikv-coprocessor-pending-request-code}

-   アラート ルール:

    `delta(tikv_coprocessor_pending_request[10m]) > 5000`

-   説明：

    コプロセッサーのキューイング要求。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_batch_request_snapshot_nums</code> {#code-tikv-batch-request-snapshot-nums-code}

-   アラート ルール:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[1m])) by (instance) / (count(tikv_thread_cpu_seconds_total{name=~"cop_.*"}) * 0.9) / count(count(tikv_thread_cpu_seconds_total) by (instance)) > 0`

-   説明：

    TiKV マシンのコプロセッサーCPU 使用率が 90% を超えています。

#### <code>TiKV_pending_task</code> {#code-tikv-pending-task-code}

-   アラート ルール:

    `sum(tikv_worker_pending_task_total) BY (instance,name)  > 1000`

-   説明：

    TiKV の保留中のタスクの数。

-   解決：

    どの種類のタスクがより高い値を持っているかを確認します。通常、コプロセッサーへのソリューションを見つけて、他のメトリックからワーカー タスクを適用できます。

#### <code>TiKV_low_space</code> {#code-tikv-low-space-code}

-   アラート ルール:

    `sum(tikv_store_size_bytes{type="available"}) by (instance) / sum(tikv_store_size_bytes{type="capacity"}) by (instance) < 0.2`

-   説明：

    TiKV のデータ量が、構成されているノード容量またはマシンのディスク容量の 80% を超えています。

-   解決：

    -   ノード空間のバランス状態を確認してください。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>TiKV_approximate_region_size</code> {#code-tikv-approximate-region-size-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_region_size_bucket[1m])) by (le)) > 1073741824`

-   説明：

    TiKV スプリット チェッカーによってスキャンされるリージョンの最大サイズは、1 分間で 1 GB を超え続けています。

-   解決：

    リージョンを分割する速度は、書き込み速度よりも遅くなります。この問題を軽減するには、TiDB をバッチ分割をサポートするバージョン (&gt;= 2.1.0-rc1) に更新することをお勧めします。一時的に更新できない場合は、 `pd-ctl operator add split-region <region_id> --policy=approximate`使用して手動でリージョンを分割できます。

## TiFlashアラート ルール {#tiflash-alert-rules}

TiFlashアラート ルールの詳細な説明については、 [TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## TiDB Binlogアラート ルール {#tidb-binlog-alert-rules}

TiDB Binlogアラート ルールの詳細な説明については、 [TiDB Binlog監視ドキュメント](/tidb-binlog/monitor-tidb-binlog-cluster.md#alert-rules)を参照してください。

## TiCDC アラート ルール {#ticdc-alert-rules}

TiCDC アラート ルールの詳細な説明については、 [TiCDC アラート ルール](/ticdc/ticdc-alert-rules.md)を参照してください。

## Node_exporter ホスト アラート ルール {#node-exporter-host-alert-rules}

このセクションでは、Node_exporter ホストのアラート ルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>NODE_disk_used_more_than_80%</code> {#code-node-disk-used-more-than-80-code}

-   アラート ルール:

    `node_filesystem_avail_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} / node_filesystem_size_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} * 100 <= 20`

-   説明：

    マシンのディスク容量使用率が 80% を超えています。

-   解決：

    -   マシンにログインし、 `df -h`コマンドを実行してディスク容量の使用状況を確認します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>NODE_disk_inode_more_than_80%</code> {#code-node-disk-inode-more-than-80-code}

-   アラート ルール:

    `node_filesystem_files_free{fstype=~"(ext.|xfs)"} / node_filesystem_files{fstype=~"(ext.|xfs)"} * 100 < 20`

-   説明：

    マシン上のファイル システムの inode 使用率が 80% を超えています。

-   解決：

    -   マシンにログインし、 `df -i`コマンドを実行して、ファイルシステムのノード使用状況を表示します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスター ノードを増やす計画を立てます。

#### <code>NODE_disk_readonly</code> {#code-node-disk-readonly-code}

-   アラート ルール:

    `node_filesystem_readonly{fstype=~"(ext.|xfs)"} == 1`

-   説明：

    ファイルシステムは読み取り専用であり、データを書き込むことはできません。多くの場合、ディスク障害またはファイルシステムの破損が原因です。

-   解決：

    -   マシンにログインし、正常かどうかをテストするためのファイルを作成します。
    -   ディスク LED が正常かどうかを確認します。そうでない場合は、ディスクを交換し、マシンのファイル システムを修復します。

### 重大レベルのアラート {#critical-level-alerts}

#### <code>NODE_memory_used_more_than_80%</code> {#code-node-memory-used-more-than-80-code}

-   アラート ルール:

    `(((node_memory_MemTotal_bytes-node_memory_MemFree_bytes-node_memory_Cached_bytes)/(node_memory_MemTotal_bytes)*100)) >= 80`

-   説明：

    マシンのメモリ使用量が 80% を超えています。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストの [メモリ] パネルをビュー、使用済みメモリが多すぎないか、使用可能なメモリが少なすぎないかを確認します。
    -   マシンにログインし、 `free -m`コマンドを実行してメモリ使用量を表示します。 `top`を実行して、メモリ使用量が過度に高い異常なプロセスがないかどうかを確認できます。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>NODE_node_overload</code> {#code-node-node-overload-code}

-   アラート ルール:

    `(node_load5 / count without (cpu, mode) (node_cpu_seconds_total{mode="system"})) > 1`

-   説明：

    マシンの CPU 負荷が比較的高い。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストの CPU 使用率と負荷平均をビュー、それらが高すぎるかどうかを確認します。
    -   マシンにログインして`top`を実行し、負荷平均と CPU 使用率を確認し、CPU 使用率が過度に高い異常なプロセスがないかどうかを確認します。

#### <code>NODE_cpu_used_more_than_80%</code> {#code-node-cpu-used-more-than-80-code}

-   アラート ルール:

    `avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance) * 100 <= 20`

-   説明：

    マシンの CPU 使用率が 80% を超えています。

-   解決：

    -   Grafana Node Exporter ダッシュボードでホストの CPU 使用率と負荷平均をビュー、それらが高すぎるかどうかを確認します。
    -   マシンにログインし、 `top`を実行して負荷平均と CPU 使用率を確認し、CPU 使用率が過度に高い異常なプロセスがないかどうかを確認します。

#### <code>NODE_tcp_estab_num_more_than_50000</code> {#code-node-tcp-estab-num-more-than-50000-code}

-   アラート ルール:

    `node_netstat_Tcp_CurrEstab > 50000`

-   説明：

    マシン上で「確立」ステータスの TCP リンクが 50,000 を超えています。

-   解決：

    -   マシンにログインして`ss -s`を実行し、現在のシステムで「estab」ステータスの TCP リンクの数を確認します。
    -   `netstat`を実行して、異常なリンクがないかどうかを確認します。

#### <code>NODE_disk_read_latency_more_than_32ms</code> {#code-node-disk-read-latency-more-than-32ms-code}

-   アラート ルール:

    `((rate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_reads_completed_total{device=~".+"}[5m])) or (irate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_reads_completed_total{device=~".+"}[5m])) ) * 1000 > 32`

-   説明：

    ディスクの読み取りレイテンシーが32 ミリ秒を超えています。

-   解決：

    -   Grafana Disk Performance ダッシュボードを表示して、ディスクのステータスを確認します。
    -   [ディスク レイテンシ] パネルを表示して、ディスクの読み取りレイテンシーを確認します。
    -   [ディスク I/O 使用率] パネルを表示して、I/O 使用率を確認します。

#### <code>NODE_disk_write_latency_more_than_16ms</code> {#code-node-disk-write-latency-more-than-16ms-code}

-   アラート ルール:

    `((rate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_writes_completed_total{device=~".+"}[5m])) or (irate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_writes_completed_total{device=~".+"}[5m])))> 16`

-   説明：

    ディスクの書き込みレイテンシーは16 ミリ秒を超えています。

-   解決：

    -   Grafana Disk Performance ダッシュボードを表示して、ディスクのステータスを確認します。
    -   [ディスク レイテンシ] パネルを表示して、ディスクの書き込みレイテンシーを確認します。
    -   [ディスク I/O 使用率] パネルを表示して、I/O 使用率を確認します。

## Blackbox_exporter TCP、ICMP、および HTTP アラート ルール {#blackbox-exporter-tcp-icmp-and-http-alert-rules}

このセクションでは、Blackbox_exporter TCP、ICMP、および HTTP のアラート ルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiDB_server_is_down</code> {#code-tidb-server-is-down-code}

-   アラート ルール:

    `probe_success{group="tidb"} == 0`

-   説明：

    TiDB サービス ポートのプローブに失敗しました。

-   解決：

    -   TiDB サービスを提供するマシンがダウンしているかどうかを確認します。
    -   TiDB プロセスが存在するかどうかを確認します。
    -   監視マシンと TiDB マシン間のネットワークが正常かどうかを確認します。

#### <code>TiFlash_server_is_down</code> {#code-tiflash-server-is-down-code}

-   アラート ルール:

    `probe_success{group="tiflash"} == 0`

-   説明：

    TiFlashサービス ポートのプローブに失敗しました。

-   解決：

    -   TiFlashサービスを提供するマシンがダウンしていないか確認してください。
    -   TiFlashプロセスが存在するかどうかを確認します。
    -   監視マシンとTiFlashマシン間のネットワークが正常か確認してください。

#### <code>Pump_server_is_down</code> {#code-pump-server-is-down-code}

-   アラート ルール:

    `probe_success{group="pump"} == 0`

-   説明：

    ポンプ サービス ポートのプローブの失敗。

-   解決：

    -   ポンプ サービスを提供するマシンがダウンしているかどうかを確認します。
    -   ポンプ プロセスが存在するかどうかを確認します。
    -   監視機とポンプ機間のネットワークが正常か確認してください。

#### <code>Drainer_server_is_down</code> {#code-drainer-server-is-down-code}

-   アラート ルール:

    `probe_success{group="drainer"} == 0`

-   説明：

    Drainerサービス ポートのプローブに失敗しました。

-   解決：

    -   Drainerサービスを提供するマシンがダウンしているかどうかを確認します。
    -   Drainerプロセスが存在するかどうかを確認します。
    -   監視マシンとDrainerマシン間のネットワークが正常か確認してください。

#### <code>TiKV_server_is_down</code> {#code-tikv-server-is-down-code}

-   アラート ルール:

    `probe_success{group="tikv"} == 0`

-   説明：

    TiKV サービス ポートのプローブに失敗しました。

-   解決：

    -   TiKV サービスを提供するマシンがダウンしていないか確認してください。
    -   TiKV プロセスが存在するかどうかを確認します。
    -   監視マシンとTiKVマシン間のネットワークが正常か確認してください。

#### <code>PD_server_is_down</code> {#code-pd-server-is-down-code}

-   アラート ルール:

    `probe_success{group="pd"} == 0`

-   説明：

    PD サービス ポートのプローブに失敗しました。

-   解決：

    -   PDサービスを提供するマシンがダウンしていないか確認してください。
    -   PD プロセスが存在するかどうかを確認します。
    -   監視マシンとPDマシン間のネットワークが正常か確認してください。

#### <code>Node_exporter_server_is_down</code> {#code-node-exporter-server-is-down-code}

-   アラート ルール:

    `probe_success{group="node_exporter"} == 0`

-   説明：

    Node_exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Node_exporter サービスを提供するマシンがダウンしているかどうかを確認します。
    -   Node_exporter プロセスが存在するかどうかを確認します。
    -   監視マシンとNode_exporterマシン間のネットワークが正常か確認してください。

#### <code>Blackbox_exporter_server_is_down</code> {#code-blackbox-exporter-server-is-down-code}

-   アラート ルール:

    `probe_success{group="blackbox_exporter"} == 0`

-   説明：

    Blackbox_Exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Blackbox_Exporter サービスを提供するマシンがダウンしているかどうかを確認します。
    -   Blackbox_Exporter プロセスが存在するかどうかを確認します。
    -   監視マシンと Blackbox_Exporter マシン間のネットワークが正常かどうかを確認します。

#### <code>Grafana_server_is_down</code> {#code-grafana-server-is-down-code}

-   アラート ルール:

    `probe_success{group="grafana"} == 0`

-   説明：

    Grafana サービス ポートのプローブに失敗しました。

-   解決：

    -   Grafana サービスを提供するマシンがダウンしているかどうかを確認します。
    -   Grafana プロセスが存在するかどうかを確認します。
    -   監視マシンと Grafana マシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_server_is_down</code> {#code-pushgateway-server-is-down-code}

-   アラート ルール:

    `probe_success{group="pushgateway"} == 0`

-   説明：

    Pushgateway サービス ポートのプローブに失敗しました。

-   解決：

    -   Pushgateway サービスを提供するマシンがダウンしていないか確認してください。
    -   Pushgateway プロセスが存在するかどうかを確認します。
    -   監視マシンとPushgatewayマシン間のネットワークが正常か確認してください。

#### <code>Kafka_exporter_is_down</code> {#code-kafka-exporter-is-down-code}

-   アラート ルール:

    `probe_success{group="kafka_exporter"} == 0`

-   説明：

    Kafka_Exporter サービス ポートのプローブに失敗しました。

-   解決：

    -   Kafka_Exporter サービスを提供するマシンがダウンしているかどうかを確認します。
    -   Kafka_Exporter プロセスが存在するかどうかを確認します。
    -   監視マシンと Kafka_Exporter マシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_metrics_interface</code> {#code-pushgateway-metrics-interface-code}

-   アラート ルール:

    `probe_success{job="blackbox_exporter_http"} == 0`

-   説明：

    Pushgateway サービスの http インターフェイスのプローブに失敗しました。

-   解決：

    -   Pushgateway サービスを提供するマシンがダウンしていないか確認してください。
    -   Pushgateway プロセスが存在するかどうかを確認します。
    -   監視マシンとPushgatewayマシン間のネットワークが正常か確認してください。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>BLACKER_ping_latency_more_than_1s</code> {#code-blacker-ping-latency-more-than-1s-code}

-   アラート ルール:

    `max_over_time(probe_duration_seconds{job=~"blackbox_exporter.*_icmp"}[1m]) > 1`

-   説明：

    ping のレイテンシーが1 秒を超えています。

-   解決：

    -   Grafana Blackbox Exporter ページで 2 つのノード間の pingレイテンシーをビュー、高すぎるかどうかを確認します。
    -   Grafana Node Exporter ページの TCP パネルをチェックして、パケット損失がないかどうかを確認します。
