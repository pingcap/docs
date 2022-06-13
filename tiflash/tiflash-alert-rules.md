---
title: TiFlash Alert Rules
summary: Learn the alert rules of the TiFlash cluster.
---

# TiFlashアラートルール {#tiflash-alert-rules}

このドキュメントでは、TiFlashクラスタのアラートルールを紹介します。

## <code>TiFlash_schema_error</code> {#code-tiflash-schema-error-code}

-   アラートルール：

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

-   説明：

    スキーマ適用エラーが発生すると、アラートがトリガーされます。

-   解決：

    エラーは、いくつかの間違ったロジックが原因である可能性があります。サポートについては[TiFlash R＆D](mailto:support@pingcap.com)にお問い合わせください。

## <code>TiFlash_schema_apply_duration</code> {#code-tiflash-schema-apply-duration-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

-   説明：

    適用期間が20秒を超える確率が99％を超えると、アラートがトリガーされます。

-   解決：

    TiFlashストレージエンジンの内部の問題が原因である可能性があります。サポートについては[TiFlash R＆D](mailto:support@pingcap.com)にお問い合わせください。

## <code>TiFlash_raft_read_index_duration</code> {#code-tiflash-raft-read-index-duration-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

-   説明：

    読み取りインデックス期間が3秒を超える確率が99％を超えると、アラートがトリガーされます。

    > **ノート：**
    >
    > `read index`は、TiKVリーダーに送信されるkvprotoリクエストです。 TiKVリージョンの再試行、ビジーストア、またはネットワークの問題により、要求時間が`read index`に長くなる可能性があります。

-   解決：

    頻繁な再試行は、TiKVクラスタの頻繁な分割または移行が原因である可能性があります。 TiKVクラスタのステータスを確認して、再試行の理由を特定できます。

## <code>TiFlash_raft_wait_index_duration</code> {#code-tiflash-raft-wait-index-duration-code}

-   アラートルール：

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

-   説明：

    TiFlashのRegionRaftIndexの待機時間が2秒を超える確率が99％を超えると、アラートがトリガーされます。

-   解決：

    TiKVとプロキシ間の通信エラーが原因である可能性があります。サポートについては[TiFlash R＆D](mailto:support@pingcap.com)にお問い合わせください。
