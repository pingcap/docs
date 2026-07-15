---
title: TiCDC Alert Rules
summary: TiCDC アラート ルールとアラートの処理方法について学習します。
---

# TiCDCアラートルール {#ticdc-alert-rules}

このドキュメントでは、TiCDC のアラートルールとそれに対応するソリューションについて説明します。重大度は、降順に、**重大**、**警告の**順になります。

## 重大なアラート {#critical-alerts}

このセクションでは、重要なアラートと解決策について説明します。

### `cdc_checkpoint_high_delay` {#cdc-checkpoint-high-delay}

重大なアラートの場合、異常な監視メトリックに細心の注意を払う必要があります。

-   アラートルール:

    `ticdc_owner_checkpoint_ts_lag > 600`

-   説明：

    レプリケーション タスクが 10 分以上遅延します。

-   解決：

    [TiCDC はレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)参照。

### `cdc_resolvedts_high_delay` {#cdc-resolvedts-high-delay}

-   アラートルール:

    `ticdc_owner_resolved_ts_lag > 300`

-   説明：

    レプリケーション タスクの解決された TS が 5 分以上遅延します。

-   解決：

    [TiCDC はレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)参照。

### `ticdc_changefeed_failed` {#ticdc-changefeed-failed}

-   アラートルール:

    `(max_over_time(ticdc_owner_status[1m]) == 2) > 0`

-   説明：

    レプリケーション タスクで回復不可能なエラーが発生し、失敗状態になります。

-   解決：

    このアラートはレプリケーションの中断に似ています。1 [TiCDC はレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)を参照してください。

## 警告アラート {#warning-alerts}

警告アラートは、問題またはエラーを通知するものです。

### `cdc_multiple_owners` {#cdc-multiple-owners}

-   アラートルール:

    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

-   説明：

    TiCDC クラスターには複数の所有者が存在します。

-   解決：

    根本原因を特定するには、TiCDC ログを収集します。

### `cdc_no_owner` {#cdc-no-owner}

-   アラートルール:

    `sum(rate(ticdc_owner_ownership_counter[240s])) < 0.5`

-   説明：

    TiCDC クラスターに 10 分以上所有者が存在しません。

-   解決：

    根本原因を特定するために TiCDC ログを収集します。

### `ticdc_changefeed_meet_error` {#ticdc-changefeed-meet-error}

-   アラートルール:

    `(max_over_time(ticdc_owner_status[1m]) == 1 or max_over_time(ticdc_owner_status[1m]) == 6) > 0`

-   説明：

    レプリケーション タスクでエラーが発生しました。

-   解決：

    [TiCDC はレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)参照。

### `ticdc_processor_exit_with_error_count` {#ticdc-processor-exit-with-error-count}

-   アラートルール:

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

-   説明：

    レプリケーション タスクはエラーを報告して終了します。

-   解決：

    [TiCDC はレプリケーションの中断を処理します](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions)参照。

### `tikv_cdc_min_resolved_ts_no_change_for_1m` {#tikv-cdc-min-resolved-ts-no-change-for-1m}

-   アラートルール:

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0 and ON (instance) tikv_cdc_captured_region_total > 0`

-   説明：

    TiKV CDC の最小解決 TS 1 は 1 分間進んでいません。

-   解決：

    根本原因を特定するには、TiKV ログを収集します。

### `tikv_cdc_scan_duration_seconds_more_than_10min` {#tikv-cdc-scan-duration-seconds-more-than-10min}

-   アラートルール:

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

-   説明：

    TiKV CDC モジュールは、増分レプリケーションを 10 分以上スキャンしました。

-   解決：

    根本原因を特定するには、TiCDC 監視メトリックと TiKV ログを収集します。

### `ticdc_sink_execution_error` {#ticdc-sink-execution-error}

-   アラートルール:

    `changes(ticdc_sink_execution_error[1m]) > 0`

-   説明：

    レプリケーション タスクがダウンストリームにデータを書き込むときにエラーが発生します。

-   解決：

    考えられる根本原因は多数あります。1 [TiCDC のトラブルシューティング](/ticdc/troubleshoot-ticdc.md)を参照してください。

### `ticdc_memory_abnormal` {#ticdc-memory-abnormal}

-   アラートルール:

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

-   説明：

    TiCDC ヒープメモリ使用量が 10 GiB を超えています。

-   解決：

    根本原因を特定するには、TiCDC ログを収集します。
