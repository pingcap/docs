---
title: PostgreSQL 互換 TiDB Cloud Starter の組み込みメトリクス
summary: PostgreSQL 互換の TiDB Cloud Starter インスタンスで利用可能な組み込みメトリクスについて説明します。
---

# PostgreSQL 互換 TiDB Cloud Starter の組み込みメトリクス

TiDB Cloud は、TiDB リソースの標準メトリクス一式を収集し、Metrics ページに表示します。これらのメトリクスを確認することで、パフォーマンスの問題を簡単に特定し、現在のデータベースのデプロイが要件を満たしているかどうかを判断できます。

## Metrics ページを表示する {#view-the-metrics-page}

**Metrics** ページでメトリクスを表示するには、次の手順を実行します。

1. [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象のリソース名をクリックして、その概要ページに移動します。

    > **Tip:**
    >
    > 複数の組織に所属している場合は、まず左上隅のコンボボックスを使用して対象の組織に切り替えてください。

2. 左側のナビゲーションペインで、**Monitoring** > **Metrics** をクリックします。

## メトリクスの保持ポリシー {#metrics-retention-policy}

TiDB Cloud では、メトリクスデータは 7 日間保持されます。

## PostgreSQL 互換 {{{ .starter }}} インスタンスのメトリクス {#metrics-for-postgresql-compatible-starter-instances}

以下のセクションでは、PostgreSQL 互換の {{{ .starter }}} インスタンスの **Metrics** ページに表示されるメトリクスについて説明します。

| メトリクス名 | ラベル | 説明 |
| :------------| :------| :-------------------------------------------- |
| Used Storage Size | Row-based storage, Row-based standard storage, Columnar storage | 行ベースストレージ、行ベース標準ストレージ、およびカラムナー ストレージのサイズです。TiDB Cloud は、各ストレージタイプのサイズが 50 MiB 以上の場合にのみ、このメトリクスを表示します。**Row-based standard storage** は **Row-based storage** と同じ意味です。 |
| Query Per Second | All, {SQL type} | 1 秒あたりに実行される SQL 文の数です。`SELECT`、`INSERT`、`UPDATE` などの SQL タイプごとに収集されます。 |
| Query Duration | Avg, P99, P99-{SQL type} | クライアントから {{{ .starter }}} インスタンスがリクエストを受信してから、そのインスタンスがリクエストを実行し、結果をクライアントに返すまでの所要時間です。 |
| Total Connection | All | {{{ .starter }}} インスタンスへの接続数です。 |

## FAQ {#faq}

**1. このページで一部のペインが空なのはなぜですか？**

選択した時間範囲に、インスタンス上のアクティビティが含まれていることを確認してください。グラフが引き続き空のままの場合は、トラブルシューティングのために [PingCAP サポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。

**2. まれにメトリクスが不連続になるのはなぜですか？**

ごくまれに、メトリクスシステムに高い負荷がかかった場合などに、メトリクスが失われることがあります。

この問題が発生した場合は、トラブルシューティングのために [PingCAP サポート](/tidb-cloud/tidb-cloud-support.md) にお問い合わせください。