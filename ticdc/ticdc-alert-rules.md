---
title: TiCDC Alert Rules
summary: Learn about TiCDC alert rules and how to handle the alerts.
---

# TiCDC アラート ルール {#ticdc-alert-rules}

この文書では、TiCDC アラート ルールと対応するソリューションについて説明します。重大度レベルは降順で、 **Critical** 、 **Warning**になります。

## 重大なアラート {#critical-alerts}

このセクションでは、重要なアラートと解決策を紹介します。

### <code>cdc_checkpoint_high_delay</code> {#code-cdc-checkpoint-high-delay-code}

重要なアラートの場合は、異常な監視メトリクスに細心の注意を払う必要があります。

-   アラート ルール:

    (time() - ticdc_owner_checkpoint_ts / 1000) &gt; 600

-   説明：

    レプリケーション タスクが 10 分以上遅延しています。

-   解決：

    [TiCDC ハンドル レプリケーションの中断](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

## <code>cdc_resolvedts_high_delay</code> {#code-cdc-resolvedts-high-delay-code}

-   アラート ルール:

    (time() - ticdc_owner_resolved_ts / 1000) &gt; 300

-   説明：

    レプリケーション タスクの解決された TS が 5 分以上遅れています。

-   解決：

    [TiCDC ハンドル レプリケーションの中断](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

### <code>ticdc_processor_exit_with_error_count</code> {#code-ticdc-processor-exit-with-error-count-code}

-   アラート ルール:

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

-   説明：

    レプリケーションタスクはエラーを報告して終了します。

-   解決：

    [TiCDC ハンドル レプリケーションの中断](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

## 警告アラート {#warning-alerts}

警告アラートは、問題またはエラーを通知するものです。

### <code>cdc_multiple_owners</code> {#code-cdc-multiple-owners-code}

-   アラート ルール:

    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

-   説明：

    TiCDC クラスターには複数の所有者がいます。

-   解決：

    TiCDC ログを収集して根本原因を特定します。

### <code>cdc_sink_flush_duration_time_more_than_10s</code> {#code-cdc-sink-flush-duration-time-more-than-10s-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(ticdc_sink_txn_worker_flush_duration[1m])) > 10`

-   説明：

    レプリケーション タスクでは、ダウンストリーム データベースにデータを書き込むのに 10 秒以上かかります。

-   解決：

    下流データベースに問題がないか確認してください。

### <code>cdc_processor_checkpoint_tso_no_change_for_1m</code> {#code-cdc-processor-checkpoint-tso-no-change-for-1m-code}

-   アラート ルール:

    `changes(ticdc_processor_checkpoint_ts[1m]) < 1`

-   説明：

    レプリケーション タスクが 1 分以上進んでいません。

-   解決：

    [TiCDC ハンドル レプリケーションの中断](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

### <code>ticdc_puller_entry_sorter_sort_bucket</code> {#code-ticdc-puller-entry-sorter-sort-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_sort_bucket{}[1m])) > 1`

-   説明：

    TiCDC プラー エントリ ソーターの遅延が長すぎます。

-   解決：

    TiCDC ログを収集して根本原因を特定します。

### <code>ticdc_puller_entry_sorter_merge_bucket</code> {#code-ticdc-puller-entry-sorter-merge-bucket-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_merge_bucket{}[1m])) > 1`

-   説明：

    TiCDC プラーのエントリー・ソーターのマージの遅延が長すぎます。

-   解決：

    TiCDC ログを収集して根本原因を特定します。

### <code>tikv_cdc_min_resolved_ts_no_change_for_1m</code> {#code-tikv-cdc-min-resolved-ts-no-change-for-1m-code}

-   アラート ルール:

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0`

-   説明：

    TiKV CDC の最小解決済み TS 1 は 1 分間進んでいません。

-   解決：

    TiKV ログを収集して根本原因を特定します。

### <code>tikv_cdc_scan_duration_seconds_more_than_10min</code> {#code-tikv-cdc-scan-duration-seconds-more-than-10min-code}

-   アラート ルール:

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

-   説明：

    TiKV CDC モジュールは、増分レプリケーションを 10 分以上スキャンしました。

-   解決：

    TiCDC モニタリング メトリックと TiKV ログを収集して、根本原因を特定します。

### <code>ticdc_sink_mysql_execution_error</code> {#code-ticdc-sink-mysql-execution-error-code}

-   アラート ルール:

    `changes(ticdc_sink_mysql_execution_error[1m]) > 0`

-   説明：

    レプリケーション タスクがダウンストリーム MySQL にデータを書き込むときにエラーが発生します。

-   解決：

    考えられる根本原因は多数あります。 [TiCDC のトラブルシューティング](/ticdc/troubleshoot-ticdc.md)を参照してください。

### <code>ticdc_memory_abnormal</code> {#code-ticdc-memory-abnormal-code}

-   アラート ルール:

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

-   説明：

    TiCDC ヒープメモリの使用量が 10 GiB を超えています。

-   解決：

    TiCDC ログを収集して根本原因を特定します。
