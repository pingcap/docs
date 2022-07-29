---
title: TiCDC Alert Rules
summary: Learn about TiCDC alert rules and how to handle the alerts.
---

# TiCDCアラートルール {#ticdc-alert-rules}

このドキュメントでは、TiCDCアラートルールと対応するソリューションについて説明します。降順で、重大度レベルは次のとおりです。**重大**、<strong>警告</strong>。

## 重要なアラート {#critical-alerts}

このセクションでは、重要なアラートとソリューションを紹介します。

### <code>cdc_checkpoint_high_delay</code> {#code-cdc-checkpoint-high-delay-code}

重要なアラートの場合、異常な監視メトリックに細心の注意を払う必要があります。

-   アラートルール：

    （time（）-ticdc_processor_checkpoint_ts / 1000）&gt; 600

-   説明：

    レプリケーションタスクが10分以上遅れています。

-   解決：

    [TiCDCはレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

## <code>cdc_resolvedts_high_delay</code> {#code-cdc-resolvedts-high-delay-code}

-   アラートルール：

    （time（）-ticdc_processor_resolved_ts / 1000）&gt; 300

-   説明：

    レプリケーションタスクの解決済みTSが10分以上遅れています。

-   解決：

    [TiCDCはレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

### <code>ticdc_processor_exit_with_error_count</code> {#code-ticdc-processor-exit-with-error-count-code}

-   アラートルール：

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

-   説明：

    レプリケーションタスクはエラーを報告して終了します。

-   解決：

    [TiCDCはレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

## 警告アラート {#warning-alerts}

警告アラートは、問題またはエラーのリマインダーです。

### <code>cdc_multiple_owners</code> {#code-cdc-multiple-owners-code}

-   アラートルール：

    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

-   説明：

    TiCDCクラスタには複数の所有者がいます。

-   解決：

    TiCDCログを収集して、根本原因を特定します。

### <code>ticdc_mounter_unmarshal_and_mount_time_more_than_1s</code> {#code-ticdc-mounter-unmarshal-and-mount-time-more-than-1s-code}

-   アラートルール：

`histogram_quantile(0.9, rate(ticdc_mounter_unmarshal_and_mount_bucket[1m])) * 1000 > 1000`

-   説明：

    データ変更のマーシャリングを解除するには、レプリケーションタスクに1秒以上かかります。

-   解決：

    TiCDCログを収集して、根本原因を特定します。

### <code>cdc_sink_execute_duration_time_more_than_10s</code> {#code-cdc-sink-execute-duration-time-more-than-10s-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(ticdc_sink_txn_exec_duration_bucket[1m])) > 10`

-   説明：

    ダウンストリームデータベースにデータを書き込むには、レプリケーションタスクに10秒以上かかります。

-   解決：

    ダウンストリームデータベースに問題があるかどうかを確認します。

### <code>cdc_processor_checkpoint_tso_no_change_for_1m</code> {#code-cdc-processor-checkpoint-tso-no-change-for-1m-code}

-   アラートルール：

    `changes(ticdc_processor_checkpoint_ts[1m]) < 1`

-   説明：

    レプリケーションタスクが1分以上進行していません。

-   解決：

    [TiCDCはレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

### <code>ticdc_puller_entry_sorter_sort_bucket</code> {#code-ticdc-puller-entry-sorter-sort-bucket-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_sort_bucket{}[1m])) > 1`

-   説明：

    TiCDCプラーエントリーソーターの遅延が長すぎます。

-   解決：

    TiCDCログを収集して、根本原因を特定します。

### <code>ticdc_puller_entry_sorter_merge_bucket</code> {#code-ticdc-puller-entry-sorter-merge-bucket-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_merge_bucket{}[1m])) > 1`

-   説明：

    TiCDCプラーエントリソーターマージの遅延が長すぎます。

-   解決：

    TiCDCログを収集して、根本原因を特定します。

### <code>tikv_cdc_min_resolved_ts_no_change_for_1m</code> {#code-tikv-cdc-min-resolved-ts-no-change-for-1m-code}

-   アラートルール：

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0`

-   説明：

    TiKVCDCの最小解決済みTS1が1分間進んでいません。

-   解決：

    TiKVログを収集して、根本原因を特定します。

### <code>tikv_cdc_scan_duration_seconds_more_than_10min</code> {#code-tikv-cdc-scan-duration-seconds-more-than-10min-code}

-   アラートルール：

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

-   説明：

    TiKV CDCモジュールは、10分を超えて増分レプリケーションをスキャンしました。

-   解決：

    TiCDCモニタリングメトリックとTiKVログを収集して、根本原因を特定します。

### <code>ticdc_sink_mysql_execution_error</code> {#code-ticdc-sink-mysql-execution-error-code}

-   アラートルール：

    `changes(ticdc_sink_mysql_execution_error[1m]) > 0`

-   説明：

    レプリケーションタスクがダウンストリームのMySQLにデータを書き込むときにエラーが発生します。

-   解決：

    考えられる根本的な原因はたくさんあります。 [TiCDCのトラブルシューティング](/ticdc/troubleshoot-ticdc.md)を参照してください。

### <code>ticdc_memory_abnormal</code> {#code-ticdc-memory-abnormal-code}

-   アラートルール：

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

-   説明：

    TiCDCヒープメモリ使用量が10GiBを超えています。

-   解決：

    TiCDCログを収集して、根本原因を特定します。
