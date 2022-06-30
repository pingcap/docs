---
title: TiDB Cluster Alert Rules
summary: Learn the alert rules in a TiDB cluster.
---

<!-- markdownlint-disable MD024 -->

# TiDBクラスターアラートルール {#tidb-cluster-alert-rules}

このドキュメントでは、TiDB、TiKV、PD、TiFlash、TiDB Binlog、TiCDC、Node_exporter、Blackbox_exporterのアラート項目のルールの説明と解決策を含め、TiDBクラスタのさまざまなコンポーネントのアラートルールについて説明します。

重大度レベルに応じて、アラートルールは、緊急レベル、クリティカルレベル、および警告レベルの3つのカテゴリ（高から低）に分類されます。この重大度レベルの区分は、以下の各コンポーネントのすべてのアラート項目に適用されます。

| 重大度レベル    | 説明                                                                                 |
| :-------- | :--------------------------------------------------------------------------------- |
| 緊急レベル     | サービスが利用できない最高の重大度レベル。緊急レベルのアラートは、多くの場合、サービスまたはノードの障害によって発生します。**すぐに手動による介入が必要です**。 |
| クリティカルレベル | サービスの可用性の低下。クリティカルレベルのアラートの場合、異常なメトリックを注意深く監視する必要があります。                            |
| 警告レベル     | 警告レベルのアラートは、問題またはエラーのリマインダーです。                                                     |

## TiDBアラートルール {#tidb-alert-rules}

このセクションでは、TiDBコンポーネントのアラートルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiDB_schema_error</code> {#code-tidb-schema-error-code}

-   アラートルール：

    `increase(tidb_session_schema_lease_error_total{type="outdated"}[15m]) > 0`

-   説明：

    最新のスキーマ情報は、1つのリース内でTiDBに再ロードされません。 TiDBがサービスの提供を継続できない場合、アラートがトリガーされます。

-   解決：

    多くの場合、使用できないリージョンまたはTiKVタイムアウトが原因です。 TiKV監視項目を確認して問題を特定する必要があります。

#### <code>TiDB_tikvclient_region_err_total</code> {#code-tidb-tikvclient-region-err-total-code}

-   アラートルール：

    `increase(tidb_tikvclient_region_err_total[10m]) > 6000`

-   説明：

    TiDBがTiKVにアクセスすると、リージョンエラーが発生します。エラーが10分間に6000回以上報告されると、アラートがトリガーされます。

-   解決：

    TiKVの監視ステータスを表示します。

#### <code>TiDB_domain_load_schema_total</code> {#code-tidb-domain-load-schema-total-code}

-   アラートルール：

    `increase(tidb_domain_load_schema_total{type="failed"}[10m]) > 10`

-   説明：

    TiDBに最新のスキーマ情報を再ロードできなかった合計数。リロードの失敗が10分間に10回以上発生すると、アラートがトリガーされます。

-   解決：

    [`TiDB_schema_error`](#tidb_schema_error)と同じ。

#### <code>TiDB_monitor_keep_alive</code> {#code-tidb-monitor-keep-alive-code}

-   アラートルール：

    `increase(tidb_monitor_keep_alive_total[10m]) < 100`

-   説明：

    TiDBプロセスがまだ存在するかどうかを示します。 `tidb_monitor_keep_alive_total`の回数が10分間に100回未満増加した場合、TiDBプロセスはすでに終了している可能性があり、アラートがトリガーされます。

-   解決：

    -   TiDBプロセスのメモリが不足していないか確認してください。
    -   本機が再起動したか確認してください。

### クリティカルレベルのアラート {#critical-level-alerts}

#### <code>TiDB_server_panic_total</code> {#code-tidb-server-panic-total-code}

-   アラートルール：

    `increase(tidb_server_panic_total[10m]) > 0`

-   説明：

    パニックに陥ったTiDBスレッドの数。パニックが発生すると、アラートがトリガーされます。スレッドは頻繁に回復されます。回復されない場合、TiDBは頻繁に再起動します。

-   解決：

    パニックログを収集して、問題を特定します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiDB_memory_abnormal</code> {#code-tidb-memory-abnormal-code}

-   アラートルール：

    `go_memstats_heap_inuse_bytes{job="tidb"} > 1e+10`

-   説明：

    TiDBメモリ使用量の監視。使用量が10Gを超えると、アラートがトリガーされます。

-   解決：

    HTTP APIを使用して、ゴルーチンリークの問題のトラブルシューティングを行います。

#### <code>TiDB_query_duration</code> {#code-tidb-query-duration-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket[1m])) BY (le, instance)) > 1`

-   説明：

    TiDBでリクエストを処理するまでのレイテンシ。 99パーセンタイル遅延が1秒を超えると、アラートがトリガーされます。

-   解決：

    TiDBログを表示し、 `SLOW_QUERY`と`TIME_COP_PROCESS`のキーワードを検索して、遅いSQLクエリを見つけます。

#### <code>TiDB_server_event_error</code> {#code-tidb-server-event-error-code}

-   アラートルール：

    `increase(tidb_server_event_total{type=~"server_start|server_hang"}[15m]) > 0`

-   説明：

    TiDBサービスで発生するイベントの数。次のイベントが発生すると、アラートがトリガーされます。

    1.  start：TiDBサービスが開始されます。
    2.  ハング：クリティカルレベルのイベント（現在、シナリオは1つだけです：TiDBはbinlogを書き込めません）が発生すると、TiDBは`hang`モードに入り、手動で強制終了されるのを待ちます。

-   解決：

    -   TiDBを再起動して、サービスを回復します。
    -   TiDBBinlogサービスが正常かどうかを確認します。

#### <code>TiDB_tikvclient_backoff_seconds_count</code> {#code-tidb-tikvclient-backoff-seconds-count-code}

-   アラートルール：

    `increase(tidb_tikvclient_backoff_seconds_count[10m]) > 10`

-   説明：

    TiDBがTiKVにアクセスできなかった場合の再試行回数。再試行時間が10分で10を超えると、アラートがトリガーされます。

-   解決：

    TiKVの監視ステータスを表示します。

#### <code>TiDB_monitor_time_jump_back_error</code> {#code-tidb-monitor-time-jump-back-error-code}

-   アラートルール：

    `increase(tidb_monitor_time_jump_back_total[10m]) > 0`

-   説明：

    TiDBを保持しているマシンの時刻が巻き戻されると、アラートがトリガーされます。

-   解決：

    NTP構成のトラブルシューティングを行います。

#### <code>TiDB_ddl_waiting_jobs</code> {#code-tidb-ddl-waiting-jobs-code}

-   アラートルール：

    `sum(tidb_ddl_waiting_jobs) > 5`

-   説明：

    TiDBで実行が保留されているDDLタスクの数が5を超えると、アラートがトリガーされます。

-   解決：

    `admin show ddl`を実行して実行されている時間のかかる`add index`操作があるかどうかを確認します。

## PDアラートルール {#pd-alert-rules}

このセクションでは、PDコンポーネントのアラートルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>PD_cluster_down_store_nums</code> {#code-pd-cluster-down-store-nums-code}

-   アラートルール：

    `(sum(pd_cluster_status{type="store_down_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PDはTiKV/TiFlashハートビートを長時間受信していません（デフォルト設定は30分です）。

-   解決：

    -   TiKV / TiFlashプロセスが正常であるか、ネットワークが分離されているか、または負荷が高すぎるかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV / TiFlashインスタンスを回復できない場合は、オフラインにすることができます。

### クリティカルレベルのアラート {#critical-level-alerts}

#### <code>PD_etcd_write_disk_latency</code> {#code-pd-etcd-write-disk-latency-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket[1m])) by (instance, job, le)) > 1`

-   説明：

    fsync操作の待ち時間が1秒を超える場合は、etcdが通常よりも低速でデータをディスクに書き込んでいることを示しています。 PDリーダーのタイムアウトが発生したり、TSOを時間内にディスクに保存できなかったりして、クラスタ全体のサービスがシャットダウンする可能性があります。

-   解決：

    -   書き込みが遅い原因を見つけます。システムに過負荷をかけるのは他のサービスである可能性があります。 PD自体が大量のCPUまたはI/Oリソースを占有しているかどうかを確認できます。
    -   PDを再起動するか、リーダーを別のPDに手動で転送して、サービスを回復してみてください。
    -   問題のあるPDインスタンスが環境要因のために回復できない場合は、オフラインにして交換します。

#### <code>PD_miss_peer_region_count</code> {#code-pd-miss-peer-region-count-code}

-   アラートルール：

    `(sum(pd_regions_status{type="miss_peer_region_count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    リージョンレプリカの数が`max-replicas`の値よりも少なくなっています。

-   解決：

    -   ダウンしているかオフラインになっているTiKVマシンがあるかどうかを確認して、問題の原因を特定します。
    -   地域のヘルスパネルを見て、 `miss_peer_region_count`が継続的に減少しているかどうかを確認します。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>PD_cluster_lost_connect_store_nums</code> {#code-pd-cluster-lost-connect-store-nums-code}

-   アラートルール：

    `(sum(pd_cluster_status{type="store_disconnected_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    PDは20秒以内にTiKV/TiFlashハートビートを受信しません。通常、TiKV/TiFlashハートビートは10秒ごとに発生します。

-   解決：

    -   TiKV/TiFlashインスタンスが再起動されているかどうかを確認します。
    -   TiKV / TiFlashプロセスが正常であり、ネットワークが分離されており、負荷が高すぎるかどうかを確認し、可能な限りサービスを回復します。
    -   TiKV / TiFlashインスタンスを復元できないことを確認した場合は、オフラインにすることができます。
    -   TiKV / TiFlashインスタンスを回復できるが、短期的には回復できないことを確認した場合は、 `max-down-time`の値を増やすことを検討できます。これにより、TiKV / TiFlashインスタンスが回復不能と見なされたり、データがTiKV/TiFlashから削除されたりするのを防ぐことができます。

#### <code>PD_cluster_low_space</code> {#code-pd-cluster-low-space-code}

-   アラートルール：

    `(sum(pd_cluster_status{type="store_low_space_count"}) by (instance) > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    TiKV/TiFlashノードに十分なスペースがないことを示します。

-   解決：

    -   クラスタのスペースが一般的に不十分であるかどうかを確認します。その場合は、容量を増やします。
    -   リージョンバランスのスケジューリングに問題がないかどうかを確認します。その場合、データの分散が不均一になります。
    -   ログ、スナップショット、コアダンプなど、大量のディスク容量を占めるファイルがないか確認してください。
    -   ノードのリージョンの重みを下げて、データ量を減らします。
    -   スペースを解放できない場合は、ノードを事前にオフラインにすることを検討してください。これにより、ダウンタイムにつながるディスク容量の不足を防ぎます。

#### <code>PD_etcd_network_peer_latency</code> {#code-pd-etcd-network-peer-latency-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(etcd_network_peer_round_trip_time_seconds_bucket[1m])) by (To, instance, job, le)) > 1`

-   説明：

    PDノード間のネットワーク遅延は高いです。リーダーのタイムアウトとTSOディスクストレージのタイムアウトが発生し、クラスタのサービスに影響を与える可能性があります。

-   解決：

    -   ネットワークとシステムの負荷状況を確認してください。
    -   問題のあるPDインスタンスが環境要因のために回復できない場合は、オフラインにして交換します。

#### <code>PD_tidb_handle_requests_duration</code> {#code-pd-tidb-handle-requests-duration-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(pd_client_request_handle_requests_duration_seconds_bucket{type="tso"}[1m])) by (instance, job, le)) > 0.1`

-   説明：

    PDがTSO要求を処理するのに時間がかかります。多くの場合、高負荷が原因です。

-   解決：

    -   サーバーのロードステータスを確認してください。
    -   pprofを使用して、PDのCPUプロファイルを分析します。
    -   PDリーダーを手動で切り替えます。
    -   問題のあるPDインスタンスが環境要因のために回復できない場合は、オフラインにして交換します。

#### <code>PD_down_peer_region_nums</code> {#code-pd-down-peer-region-nums-code}

-   アラートルール：

    `(sum(pd_regions_status{type="down-peer-region-count"}) by (instance)  > 0) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftリーダーによって報告された応答しないピアを持つリージョンの数。

-   解決：

    -   ダウンしている、または再起動したばかりの、またはビジー状態のTiKVがあるかどうかを確認します。
    -   地域のヘルスパネルを見て、 `down_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKVサーバー間のネットワークを確認してください。

#### <code>PD_pending_peer_region_count</code> {#code-pd-pending-peer-region-count-code}

-   アラートルール：

    `(sum(pd_regions_status{type="pending-peer-region-count"}) by (instance) > 100) and (sum(etcd_server_is_leader) by (instance) > 0)`

-   説明：

    Raftログが遅れているリージョンが多すぎます。スケジューリングによって保留中のピアの数が少なくなるのは通常のことですが、その数が多いままの場合は、問題が発生している可能性があります。

-   解決：

    -   地域のヘルスパネルを見て、 `pending_peer_region_count`が継続的に減少しているかどうかを確認します。
    -   TiKVサーバー間のネットワークを確認します。特に、十分な帯域幅があるかどうかを確認します。

#### <code>PD_leader_change</code> {#code-pd-leader-change-code}

-   アラートルール：

    `count(changes(pd_tso_events{type="save"}[10m]) > 0) >= 2`

-   説明：

    PDリーダーは最近切り替えられました。

-   解決：

    -   PDの再起動、リーダーの手動転送、リーダーの優先度の調整などの人的要因を除外します。
    -   ネットワークとシステムの負荷状況を確認してください。
    -   問題のあるPDインスタンスが環境要因のために回復できない場合は、オフラインにして交換します。

#### <code>TiKV_space_used_more_than_80%</code> {#code-tikv-space-used-more-than-80-code}

-   アラートルール：

    `sum(pd_cluster_status{type="storage_size"}) / sum(pd_cluster_status{type="storage_capacity"}) * 100 > 80`

-   説明：

    クラスタスペースの80％以上が占有されています。

-   解決：

    -   容量を増やす必要があるかどうかを確認します。
    -   ログ、スナップショット、コアダンプなど、大量のディスク容量を占めるファイルがないか確認してください。

#### <code>PD_system_time_slow</code> {#code-pd-system-time-slow-code}

-   アラートルール：

    `changes(pd_tso_events{type="system_time_slow"}[10m]) >= 1`

-   説明：

    システム時刻の巻き戻しが発生する可能性があります。

-   解決：

    システム時刻が正しく設定されているか確認してください。

#### <code>PD_no_store_for_making_replica</code> {#code-pd-no-store-for-making-replica-code}

-   アラートルール：

    `increase(pd_checker_event_count{type="replica_checker", name="no_target_store"}[1m]) > 0`

-   説明：

    追加のレプリカ用の適切なストアはありません。

-   解決：

    -   店舗に十分なスペースがあるかどうかを確認してください。
    -   ラベル構成が構成されている場合は、ラベル構成に従って追加のレプリカのストアがあるかどうかを確認します。

## TiKVアラートルール {#tikv-alert-rules}

このセクションでは、TiKVコンポーネントのアラートルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiKV_memory_used_too_fast</code> {#code-tikv-memory-used-too-fast-code}

-   アラートルール：

    `process_resident_memory_bytes{job=~"tikv",instance=~".*"} - (process_resident_memory_bytes{job=~"tikv",instance=~".*"} offset 5m) > 5*1024*1024*1024`

-   説明：

    現在、メモリに関するTiKV監視項目はありません。 Node_exporterを使用して、クラスタのマシンのメモリ使用量を監視できます。上記のルールは、メモリ使用量が5分以内に5 GBを超えると（TiKVではメモリの占有が速すぎる）、アラートがトリガーされることを示しています。

-   解決：

    `rockdb.defaultcf`と`rocksdb.writecf`の両方の`block-cache-size`の値を調整します。

#### <code>TiKV_GC_can_not_work</code> {#code-tikv-gc-can-not-work-code}

-   アラートルール：

    `sum(increase(tikv_gcworker_gc_tasks_vec{task="gc"}[1d])) < 1 and (sum(increase(tikv_gc_compaction_filter_perform[1d])) < 1 and sum(increase(tikv_engine_event_total{db="kv", cf="write", type="compaction"}[1d])) >= 1)`

-   説明：

    GCは24時間以内にTiKVインスタンスで正常に実行されません。これは、GCが正しく機能していないことを示しています。 GCが短期間で実行されなければ、それほど問題は発生しません。ただし、GCが停止し続けると、保持されるバージョンが増え、クエリの速度が低下します。

-   解決：

    1.  `SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME = "tikv_gc_leader_desc"`を実行して、GCリーダーに対応する`tidb-server`を見つけます。
    2.  `tidb-server`のログを表示し、grep gc_worker tidb.log;
    3.  この間にGCワーカーがロックを解決している（最後のログは「ロックの解決を開始」）か、範囲を削除している（最後のログは「{number}範囲を開始」）場合は、GCプロセスが実行中であることを意味します。通常は。それ以外の場合は、 [support@pingcap.com](mailto:support@pingcap.com)に連絡してこの問題を解決してください。

### クリティカルレベルのアラート {#critical-level-alerts}

#### <code>TiKV_server_report_failure_msg_total</code> {#code-tikv-server-report-failure-msg-total-code}

-   アラートルール：

    `sum(rate(tikv_server_report_failure_msg_total{type="unreachable"}[10m])) BY (store_id) > 10`

-   説明：

    リモートTiKVが接続できないことを示します。

-   解決：

    1.  ネットワークがクリアであるかどうかを確認します。
    2.  リモートTiKVがダウンしているかどうかを確認します。
    3.  リモートTiKVがダウンしていない場合は、圧力が高すぎるかどうかを確認してください。 [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_channel_full_total</code> {#code-tikv-channel-full-total-code}

-   アラートルール：

    `sum(rate(tikv_channel_full_total[10m])) BY (type, instance) > 0`

-   説明：

    この問題は、多くの場合、RaftstoreスレッドのスタックとTiKVへの高圧が原因で発生します。

-   解決：

    1.  Raft Proposeモニターを見て、アラートされたTiKVノードが他のTiKVノードよりもはるかに高いRaft提案を持っているかどうかを確認します。もしそうなら、それはこのTiKVに1つ以上のホットスポットがあることを意味します。ホットスポットのスケジューリングが正しく機能するかどうかを確認する必要があります。
    2.  Raft I / Oモニターを監視し、レイテンシーが増加するかどうかを確認します。待ち時間が長い場合は、ディスクにボトルネックが存在する可能性があることを意味します。実行可能であるが安全でない解決策の1つは、 `sync-log`を`false`に設定することです。
    3.  Raft Processモニターを監視し、ティック期間が長いかどうかを確認します。その場合、 `[raftstore]`構成の下に`raft-base-tick-interval = "2s"`を追加する必要があります。

#### <code>TiKV_write_stall</code> {#code-tikv-write-stall-code}

-   アラートルール：

    `delta(tikv_engine_write_stall[10m]) > 0`

-   説明：

    RocksDBへの書き込み圧力が高すぎるため、ストールが発生します。

-   解決：

    1.  ディスクモニターを表示し、ディスクの問題のトラブルシューティングを行います。
    2.  TiKVに書き込みホットスポットがあるかどうかを確認します。
    3.  `[rocksdb]`および`[raftdb]`構成では、 `max-sub-compactions`を大きい値に設定します。

#### <code>TiKV_raft_log_lag</code> {#code-tikv-raft-log-lag-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_log_lag_bucket[1m])) by (le, instance)) > 5000`

-   説明：

    この値が比較的大きい場合は、フォロワーがリーダーよりもはるかに遅れており、ラフトを正常に複製できないことを意味します。フォロワーが配置されているTiKVマシンがスタックしているか、ダウンしている可能性があります。

#### <code>TiKV_async_request_snapshot_duration_seconds</code> {#code-tikv-async-request-snapshot-duration-seconds-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="snapshot"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合は、Raftstoreの負荷圧力が高すぎることを意味し、すでにスタックしている可能性があります。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_async_request_write_duration_seconds</code> {#code-tikv-async-request-write-duration-seconds-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[1m])) by (le, instance, type)) > 1`

-   説明：

    この値が比較的大きい場合は、Raftの書き込みに時間がかかることを意味します。

-   解決：

    1.  Raftstoreの圧力を確認してください。 [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。
    2.  アプライワーカースレッドの圧力を確認してください。

#### <code>TiKV_coprocessor_request_wait_seconds</code> {#code-tikv-coprocessor-request-wait-seconds-code}

-   アラートルール：

    `histogram_quantile(0.9999, sum(rate(tikv_coprocessor_request_wait_seconds_bucket[1m])) by (le, instance, req)) > 10`

-   説明：

    この値が比較的大きい場合は、コプロセッサーワーカーへのプレッシャーが高いことを意味します。コプロセッサースレッドをスタックさせる遅いタスクがあるかもしれません。

-   解決：

    1.  TiDBログから低速クエリログを表示して、インデックスまたは全表スキャンがクエリで使用されているかどうか、または分析が必要かどうかを確認します。
    2.  ホットスポットがあるかどうかを確認します。
    3.  コプロセッサーモニターを表示し、 `coprocessor table/index scan`の`total`と`process`が一致するかどうかを確認します。それらが大きく異なる場合は、実行された無効なクエリが多すぎることを示しています。 `over seek bound`があるかどうかを確認できます。もしそうなら、GCが時間内に処理しないバージョンが多すぎます。次に、並列GCスレッドの数を増やす必要があります。

#### <code>TiKV_raftstore_thread_cpu_seconds_total</code> {#code-tikv-raftstore-thread-cpu-seconds-total-code}

-   アラートルール：

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"raftstore_.*"}[1m])) by (instance, name) > 1.6`

-   説明：

    Raftstoreスレッドへの圧力が高すぎます。

-   解決：

    [`TiKV_channel_full_total`](#tikv_channel_full_total)の解決策を参照してください。

#### <code>TiKV_raft_append_log_duration_secs</code> {#code-tikv-raft-append-log-duration-secs-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログを追加するための時間コストを示します。高い場合は、通常、I/Oがビジー状態であることを意味します。

#### <code>TiKV_raft_apply_log_duration_secs</code> {#code-tikv-raft-apply-log-duration-secs-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

-   説明：

    Raftログを適用するための時間コストを示します。高い場合は、通常、I/Oがビジー状態であることを意味します。

#### <code>TiKV_scheduler_latch_wait_duration_seconds</code> {#code-tikv-scheduler-latch-wait-duration-seconds-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_latch_wait_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

-   説明：

    書き込み操作がスケジューラのメモリロックを取得するまでの待機時間。これが高い場合、書き込みの競合が多く発生するか、競合につながる一部の操作が終了して同じロックを待機する他の操作をブロックするのに長い時間がかかる可能性があります。

-   解決：

    1.  Scheduler-Allモニターでスケジューラー・コマンドの期間を表示し、どのコマンドに最も時間がかかるかを確認します。
    2.  Scheduler-Allモニターでスケジューラースキャンの詳細を表示し、 `total`と`process`が一致するかどうかを確認します。それらが大きく異なる場合、多くの無効なスキャンがあります。 `over seek bound`があるかどうかも確認できます。多すぎる場合は、GCが時間内に機能しないことを示します。
    3.  ストレージモニターでストレージ非同期スナップショット/書き込み期間を表示し、ラフト操作が時間内に実行されているかどうかを確認します。

#### <code>TiKV_thread_apply_worker_cpu_seconds</code> {#code-tikv-thread-apply-worker-cpu-seconds-code}

-   アラートルール：

    `max(rate(tikv_thread_cpu_seconds_total{name=~"apply_.*"}[1m])) by (instance) > 0.9`

-   説明：

    アプライラフトログスレッドは大きな圧力を受けており、制限に近づいているか、制限を超えています。これは多くの場合、書き込みのバーストによって引き起こされます。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>TiKV_leader_drops</code> {#code-tikv-leader-drops-code}

-   アラートルール：

    `delta(tikv_pd_heartbeat_tick_total{type="leader"}[30s]) < -10`

-   説明：

    多くの場合、Raftstoreスレッドのスタックが原因です。

-   解決：

    1.  [`TiKV_channel_full_total`](#tikv_channel_full_total)を参照してください。
    2.  TiKVへの圧力が低い場合は、PDスケジューリングが頻繁すぎるかどうかを検討してください。 PDページでOperatorCreateパネルを表示し、PDスケジューリングのタイプと数を確認できます。

#### <code>TiKV_raft_process_ready_duration_secs</code> {#code-tikv-raft-process-ready-duration-secs-code}

-   アラートルール：

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type='ready'}[1m])) by (le, instance, type)) > 2`

-   説明：

    Raftの準備ができた状態で処理するための時間コストを示します。この値が大きい場合は、ログの追加タスクがスタックしていることが原因であることがよくあります。

#### <code>TiKV_raft_process_tick_duration_secs</code> {#code-tikv-raft-process-tick-duration-secs-code}

-   アラートルール：

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type=’tick’}[1m])) by (le, instance, type)) > 2`

-   説明：

    ラフトティックの処理にかかる時間コストを示します。この値が大きい場合は、多くの場合、リージョンが多すぎることが原因です。

-   解決：

    1.  `warn`や`error`などの高レベルのログの使用を検討してください。
    2.  `[raftstore]`構成の下に`raft-base-tick-interval = "2s"`を追加します。

#### <code>TiKV_scheduler_context_total</code> {#code-tikv-scheduler-context-total-code}

-   アラートルール：

    `abs(delta( tikv_scheduler_context_total[5m])) > 1000`

-   説明：

    スケジューラーによって実行されている書き込みコマンドの数。この値が大きい場合は、タスクがタイムリーに終了していないことを意味します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_scheduler_command_duration_seconds</code> {#code-tikv-scheduler-command-duration-seconds-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_command_duration_seconds_bucket[1m])) by (le, instance, type)  / 1000) > 1`

-   説明：

    スケジューラコマンドの実行にかかる時間コストを示します。

-   解決：

    [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv_scheduler_latch_wait_duration_seconds)を参照してください。

#### <code>TiKV_coprocessor_outdated_request_wait_seconds</code> {#code-tikv-coprocessor-outdated-request-wait-seconds-code}

-   アラートルール：

    `delta(tikv_coprocessor_outdated_request_wait_seconds_count[10m]) > 0`

-   説明：

    コプロセッサーによる期限切れの要求の待機時間。この値が大きい場合は、コプロセッサーに高い圧力がかかっていることを意味します。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_coprocessor_pending_request</code> {#code-tikv-coprocessor-pending-request-code}

-   アラートルール：

    `delta(tikv_coprocessor_pending_request[10m]) > 5000`

-   説明：

    コプロセッサーのキューイング要求。

-   解決：

    [`TiKV_coprocessor_request_wait_seconds`](#tikv_coprocessor_request_wait_seconds)を参照してください。

#### <code>TiKV_batch_request_snapshot_nums</code> {#code-tikv-batch-request-snapshot-nums-code}

-   アラートルール：

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[1m])) by (instance) / (count(tikv_thread_cpu_seconds_total{name=~"cop_.*"}) * 0.9) / count(count(tikv_thread_cpu_seconds_total) by (instance)) > 0`

-   説明：

    TiKVマシンのコプロセッサーCPU使用率が90％を超えています。

#### <code>TiKV_pending_task</code> {#code-tikv-pending-task-code}

-   アラートルール：

    `sum(tikv_worker_pending_task_total) BY (instance,name)  > 1000`

-   説明：

    TiKVの保留中のタスクの数。

-   解決：

    どの種類のタスクの方が価値が高いかを確認してください。通常、コプロセッサーの解決策を見つけて、他のメトリックからワーカータスクを適用できます。

#### <code>TiKV_low_space</code> {#code-tikv-low-space-code}

-   アラートルール：

    `sum(tikv_store_size_bytes{type="available"}) by (instance) / sum(tikv_store_size_bytes{type="capacity"}) by (instance) < 0.2`

-   説明：

    TiKVのデータ量が、構成されたノード容量またはマシンのディスク容量の80％を超えています。

-   解決：

    -   ノードスペースのバランス状態を確認してください。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスタノードを増やす計画を立てます。

#### <code>TiKV_approximate_region_size</code> {#code-tikv-approximate-region-size-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_region_size_bucket[1m])) by (le)) > 1073741824`

-   説明：

    TiKVスプリットチェッカーによってスキャンされるリージョンのおおよその最大サイズは、1分以内に1GBを超え続けます。

-   解決：

    リージョンの分割速度は、書き込み速度よりも遅くなります。この問題を軽減するには、TiDBをバッチ分割をサポートするバージョン（&gt; = 2.1.0-rc1）に更新することをお勧めします。一時的に更新できない場合は、 `pd-ctl operator add split-region <region_id> --policy=approximate`を使用してリージョンを手動で分割できます。

## TiFlashアラートルール {#tiflash-alert-rules}

TiFlashアラートルールの詳細については、 [TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)を参照してください。

## TiDBBinlogアラートルール {#tidb-binlog-alert-rules}

TiDB Binlogアラートルールの詳細については、 [TiDBBinlogモニタリングドキュメント](/tidb-binlog/monitor-tidb-binlog-cluster.md#alert-rules)を参照してください。

## TiCDCアラートルール {#ticdc-alert-rules}

TiCDCアラートルールの詳細については、 [TiCDCアラートルール](/ticdc/ticdc-alert-rules.md)を参照してください。

## Node_exporterホストアラートルール {#node-exporter-host-alert-rules}

このセクションでは、Node_exporterホストのアラートルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>NODE_disk_used_more_than_80%</code> {#code-node-disk-used-more-than-80-code}

-   アラートルール：

    `node_filesystem_avail_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} / node_filesystem_size_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} * 100 <= 20`

-   説明：

    本機のディスク容量が80％を超えています。

-   解決：

    -   マシンにログインし、 `df -h`コマンドを実行してディスク容量の使用状況を確認します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスタノードを増やす計画を立てます。

#### <code>NODE_disk_inode_more_than_80%</code> {#code-node-disk-inode-more-than-80-code}

-   アラートルール：

    `node_filesystem_files_free{fstype=~"(ext.|xfs)"} / node_filesystem_files{fstype=~"(ext.|xfs)"} * 100 < 20`

-   説明：

    マシン上のファイルシステムのiノード使用率が80％を超えています。

-   解決：

    -   マシンにログインし、 `df -i`コマンドを実行して、ファイルシステムのノード使用状況を表示します。
    -   さまざまな状況に応じて、ディスク容量を増やすか、一部のデータを削除するか、クラスタノードを増やす計画を立てます。

#### <code>NODE_disk_readonly</code> {#code-node-disk-readonly-code}

-   アラートルール：

    `node_filesystem_readonly{fstype=~"(ext.|xfs)"} == 1`

-   説明：

    ファイルシステムは読み取り専用であり、データを書き込むことはできません。多くの場合、ディスク障害またはファイルシステムの破損が原因です。

-   解決：

    -   マシンにログインし、ファイルを作成して、正常かどうかをテストします。
    -   ディスクLEDが正常か確認してください。そうでない場合は、ディスクを交換して、マシンのファイルシステムを修復します。

### クリティカルレベルのアラート {#critical-level-alerts}

#### <code>NODE_memory_used_more_than_80%</code> {#code-node-memory-used-more-than-80-code}

-   アラートルール：

    `(((node_memory_MemTotal_bytes-node_memory_MemFree_bytes-node_memory_Cached_bytes)/(node_memory_MemTotal_bytes)*100)) >= 80`

-   説明：

    本機のメモリー使用量が80％を超えています。

-   解決：

    -   Grafana Node Exporterダッシュボードでホストのメモリパネルを表示し、使用済みメモリが高すぎるか、使用可能メモリが低すぎるかを確認します。
    -   マシンにログインし、 `free -m`コマンドを実行してメモリ使用量を表示します。 `top`を実行して、メモリ使用量が多すぎる異常なプロセスがないかどうかを確認できます。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>NODE_node_overload</code> {#code-node-node-overload-code}

-   アラートルール：

    `(node_load5 / count without (cpu, mode) (node_cpu_seconds_total{mode="system"})) > 1`

-   説明：

    マシンのCPU負荷は比較的高いです。

-   解決：

    -   Grafana Node ExporterダッシュボードでホストのCPU使用率と負荷平均を表示して、それらが高すぎるかどうかを確認します。
    -   マシンにログインして`top`を実行し、負荷平均とCPU使用率を確認し、CPU使用率が高すぎる異常なプロセスがないかどうかを確認します。

#### <code>NODE_cpu_used_more_than_80%</code> {#code-node-cpu-used-more-than-80-code}

-   アラートルール：

    `avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance) * 100 <= 20`

-   説明：

    マシンのCPU使用率が80％を超えています。

-   解決：

    -   Grafana Node ExporterダッシュボードでホストのCPU使用率と負荷平均を表示して、それらが高すぎるかどうかを確認します。
    -   マシンにログインして`top`を実行し、負荷平均とCPU使用率を確認し、CPU使用率が高すぎる異常なプロセスがないかどうかを確認します。

#### <code>NODE_tcp_estab_num_more_than_50000</code> {#code-node-tcp-estab-num-more-than-50000-code}

-   アラートルール：

    `node_netstat_Tcp_CurrEstab > 50000`

-   説明：

    マシンの「確立」ステータスには50,000を超えるTCPリンクがあります。

-   解決：

    -   マシンにログインして`ss -s`を実行し、現在のシステムで「estab」ステータスのTCPリンクの数を確認します。
    -   `netstat`を実行して、異常なリンクがあるかどうかを確認します。

#### <code>NODE_disk_read_latency_more_than_32ms</code> {#code-node-disk-read-latency-more-than-32ms-code}

-   アラートルール：

    `((rate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_reads_completed_total{device=~".+"}[5m])) or (irate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_reads_completed_total{device=~".+"}[5m])) ) * 1000 > 32`

-   説明：

    ディスクの読み取り待ち時間が32ミリ秒を超えています。

-   解決：

    -   Grafana Disk Performanceダッシュボードを表示して、ディスクのステータスを確認します。
    -   [ディスクレイテンシ]パネルを表示して、ディスクの読み取りレイテンシを確認します。
    -   [ディスクI/O使用率]パネルを表示して、I/O使用量を確認します。

#### <code>NODE_disk_write_latency_more_than_16ms</code> {#code-node-disk-write-latency-more-than-16ms-code}

-   アラートルール：

    `((rate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_writes_completed_total{device=~".+"}[5m])) or (irate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_writes_completed_total{device=~".+"}[5m])))> 16`

-   説明：

    ディスクの書き込み待ち時間が16msを超えています。

-   解決：

    -   Grafana Disk Performanceダッシュボードを表示して、ディスクのステータスを確認します。
    -   [ディスクレイテンシ]パネルを表示して、ディスクの書き込みレイテンシを確認します。
    -   [ディスクI/O使用率]パネルを表示して、I/O使用量を確認します。

## Blackbox_exporter TCP、ICMP、およびHTTPアラートルール {#blackbox-exporter-tcp-icmp-and-http-alert-rules}

このセクションでは、Blackbox_exporter TCP、ICMP、およびHTTPのアラートルールを示します。

### 緊急レベルのアラート {#emergency-level-alerts}

#### <code>TiDB_server_is_down</code> {#code-tidb-server-is-down-code}

-   アラートルール：

    `probe_success{group="tidb"} == 0`

-   説明：

    TiDBサービスポートのプローブに失敗しました。

-   解決：

    -   TiDBサービスを提供するマシンがダウンしていないか確認してください。
    -   TiDBプロセスが存在するかどうかを確認します。
    -   監視マシンとTiDBマシン間のネットワークが正常か確認してください。

#### <code>TiFlash_server_is_down</code> {#code-tiflash-server-is-down-code}

-   アラートルール：

    `probe_success{group="tiflash"} == 0`

-   説明：

    TiFlashサービスポートのプローブに失敗しました。

-   解決：

    -   TiFlashサービスを提供するマシンがダウンしていないか確認してください。
    -   TiFlashプロセスが存在するかどうかを確認します。
    -   監視マシンとTiFlashマシン間のネットワークが正常かどうかを確認します。

#### <code>Pump_server_is_down</code> {#code-pump-server-is-down-code}

-   アラートルール：

    `probe_success{group="pump"} == 0`

-   説明：

    ポンプサービスポートのプローブに失敗しました。

-   解決：

    -   ポンプサービスを提供する機械がダウンしていないか確認してください。
    -   ポンププロセスが存在するかどうかを確認します。
    -   監視機とポンプ機のネットワークが正常か確認してください。

#### <code>Drainer_server_is_down</code> {#code-drainer-server-is-down-code}

-   アラートルール：

    `probe_success{group="drainer"} == 0`

-   説明：

    ドレイナーサービスポートのプローブに失敗しました。

-   解決：

    -   ドレイナーサービスを提供するマシンがダウンしていないか確認してください。
    -   ドレイナープロセスが存在するかどうかを確認します。
    -   監視機とドレイナー機のネットワークが正常か確認してください。

#### <code>TiKV_server_is_down</code> {#code-tikv-server-is-down-code}

-   アラートルール：

    `probe_success{group="tikv"} == 0`

-   説明：

    TiKVサービスポートのプローブに失敗しました。

-   解決：

    -   TiKVサービスを提供するマシンがダウンしていないか確認してください。
    -   TiKVプロセスが存在するかどうかを確認します。
    -   監視機とTiKV機のネットワークが正常か確認してください。

#### <code>PD_server_is_down</code> {#code-pd-server-is-down-code}

-   アラートルール：

    `probe_success{group="pd"} == 0`

-   説明：

    PDサービスポートのプローブに失敗しました。

-   解決：

    -   PDサービスを提供するマシンがダウンしていないか確認してください。
    -   PDプロセスが存在するかどうかを確認します。
    -   監視機とPD機間のネットワークが正常か確認してください。

#### <code>Node_exporter_server_is_down</code> {#code-node-exporter-server-is-down-code}

-   アラートルール：

    `probe_success{group="node_exporter"} == 0`

-   説明：

    Node_exporterサービスポートのプローブに失敗しました。

-   解決：

    -   Node_exporterサービスを提供するマシンがダウンしていないか確認してください。
    -   Node_exporterプロセスが存在するかどうかを確認します。
    -   監視マシンとNode_exporterマシン間のネットワークが正常かどうかを確認します。

#### <code>Blackbox_exporter_server_is_down</code> {#code-blackbox-exporter-server-is-down-code}

-   アラートルール：

    `probe_success{group="blackbox_exporter"} == 0`

-   説明：

    Blackbox_Exporterサービスポートのプローブに失敗しました。

-   解決：

    -   Blackbox_Exporterサービスを提供するマシンがダウンしていないか確認してください。
    -   Blackbox_Exporterプロセスが存在するかどうかを確認します。
    -   監視マシンとBlackbox_Exporterマシン間のネットワークが正常かどうかを確認します。

#### <code>Grafana_server_is_down</code> {#code-grafana-server-is-down-code}

-   アラートルール：

    `probe_success{group="grafana"} == 0`

-   説明：

    Grafanaサービスポートのプローブに失敗しました。

-   解決：

    -   Grafanaサービスを提供するマシンがダウンしていないかどうかを確認します。
    -   Grafanaプロセスが存在するかどうかを確認します。
    -   監視マシンとGrafanaマシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_server_is_down</code> {#code-pushgateway-server-is-down-code}

-   アラートルール：

    `probe_success{group="pushgateway"} == 0`

-   説明：

    Pushgatewayサービスポートのプローブに失敗しました。

-   解決：

    -   Pushgatewayサービスを提供するマシンがダウンしていないか確認してください。
    -   Pushgatewayプロセスが存在するかどうかを確認します。
    -   監視機とプッシュゲートウェイ機のネットワークが正常か確認してください。

#### <code>Kafka_exporter_is_down</code> {#code-kafka-exporter-is-down-code}

-   アラートルール：

    `probe_success{group="kafka_exporter"} == 0`

-   説明：

    Kafka_Exporterサービスポートのプローブに失敗しました。

-   解決：

    -   Kafka_Exporterサービスを提供するマシンがダウンしていないか確認してください。
    -   Kafka_Exporterプロセスが存在するかどうかを確認します。
    -   監視マシンとKafka_Exporterマシン間のネットワークが正常かどうかを確認します。

#### <code>Pushgateway_metrics_interface</code> {#code-pushgateway-metrics-interface-code}

-   アラートルール：

    `probe_success{job="blackbox_exporter_http"} == 0`

-   説明：

    Pushgatewayサービスのhttpインターフェイスのプローブに失敗しました。

-   解決：

    -   Pushgatewayサービスを提供するマシンがダウンしていないか確認してください。
    -   Pushgatewayプロセスが存在するかどうかを確認します。
    -   監視機とプッシュゲートウェイ機のネットワークが正常か確認してください。

### 警告レベルのアラート {#warning-level-alerts}

#### <code>BLACKER_ping_latency_more_than_1s</code> {#code-blacker-ping-latency-more-than-1s-code}

-   アラートルール：

    `max_over_time(probe_duration_seconds{job=~"blackbox_exporter.*_icmp"}[1m]) > 1`

-   説明：

    pingの待ち時間が1秒を超えています。

-   解決：

    -   Grafana Blackbox Exporterページで2つのノード間のpingレイテンシを表示して、高すぎるかどうかを確認します。
    -   Grafana Node ExporterページのTCPパネルをチェックして、パケット損失があるかどうかを確認します。
