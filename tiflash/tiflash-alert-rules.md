---
title: TiFlash Alert Rules
summary: TiFlashクラスターのアラート ルールについて学習します。
---

# TiFlashアラートルール {#tiflash-alert-rules}

このドキュメントでは、 TiFlashクラスターのアラート ルールについて説明します。

## `TiFlash_schema_error` {#tiflash-schema-error}

-   アラートルール:

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

-   説明：

    スキーマ適用エラーが発生すると、アラートがトリガーされます。

-   解決：

    このエラーは、何らかの間違ったロジックによって発生した可能性があります。1 [サポートを受ける](/support.md)またはコミュニティから。

## `TiFlash_schema_apply_duration` {#tiflash-schema-apply-duration}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

-   説明：

    適用期間が 20 秒を超える確率が 99% を超えると、アラートがトリガーされます。

-   解決：

    これは、 TiFlashストレージエンジンの内部的な問題が原因である可能性があります。1 [サポートを受ける](/support.md) PingCAP またはコミュニティから提供されました。

## `TiFlash_raft_read_index_duration` {#tiflash-raft-read-index-duration}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

-   説明：

    読み取りインデックスの継続時間が 3 秒を超える確率が 99% を超えると、アラートがトリガーされます。

    > **Note:**
    >
    > `read index`は TiKV リーダーに送信される kvproto リクエストです。TiKV リージョンの再試行、ストアのビジー状態、またはネットワークの問題により、リクエスト時間が`read index`と長くなる可能性があります。

-   解決：

    頻繁な再試行は、TiKV クラスターの頻繁な分割または移行が原因である可能性があります。再試行の理由を特定するには、TiKV クラスターのステータスを確認してください。

## `TiFlash_raft_wait_index_duration` {#tiflash-raft-wait-index-duration}

-   アラートルール:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

-   説明：

    TiFlashのリージョン Raft Index の待機時間が 2 秒を超える確率が 99% を超えると、アラートがトリガーされます。

-   解決：

    これは、TiKV とプロキシ間の通信エラーが原因である可能性があります。1 [サポートを受ける](/support.md) PingCAP またはコミュニティから提供されました。
