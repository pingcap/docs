---
title: TiFlash Alert Rules
summary: Learn the alert rules of the TiFlash cluster.
---

# TiFlashアラート ルール {#tiflash-alert-rules}

このドキュメントでは、 TiFlashクラスターのアラート ルールを紹介します。

## <code>TiFlash_schema_error</code> {#code-tiflash-schema-error-code}

-   アラート ルール:

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

-   説明：

    スキーマ適用エラーが発生すると、アラートがトリガーされます。

-   解決：

    エラーは、間違ったロジックが原因である可能性があります。 PingCAP またはコミュニティから[支持を得ます](/support.md) 。

## <code>TiFlash_schema_apply_duration</code> {#code-tiflash-schema-apply-duration-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

-   説明：

    適用時間が 20 秒を超える確率が 99% を超えると、アラートがトリガーされます。

-   解決：

    これは、 TiFlashstorageエンジンの内部の問題が原因である可能性があります。 PingCAP またはコミュニティから[支持を得ます](/support.md) 。

## <code>TiFlash_raft_read_index_duration</code> {#code-tiflash-raft-read-index-duration-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

-   説明：

    読み取りインデックスの継続時間が 3 秒を超える確率が 99% を超えると、アラートがトリガーされます。

    > **ノート：**
    >
    > `read index`は、TiKV リーダーに送信される kvproto リクエストです。 TiKV リージョンの再試行、ビジー ストア、またはネットワークの問題により、要求時間が`read index`に長くなる可能性があります。

-   解決：

    頻繁な再試行は、TiKV クラスターの頻繁な分割または移行が原因である可能性があります。 TiKV クラスターのステータスをチェックして、再試行の理由を特定できます。

## <code>TiFlash_raft_wait_index_duration</code> {#code-tiflash-raft-wait-index-duration-code}

-   アラート ルール:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

-   説明：

    TiFlashのリージョン Raft Index の待ち時間が 2 秒を超える確率が 99% を超えると、アラートがトリガーされます。

-   解決：

    TiKV とプロキシ間の通信エラーが原因である可能性があります。 PingCAP またはコミュニティから[支持を得ます](/support.md) 。
