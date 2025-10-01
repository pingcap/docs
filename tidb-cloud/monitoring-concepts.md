---
title: Monitoring
summary: TiDB Cloudの監視の概念について学習します。
---

# 監視 {#monitoring}

TiDB Cloudのモニタリングでは、クラスターのパフォーマンスを監視し、アクティビティを追跡し、問題にタイムリーに対応できるようにするツールと統合が提供されます。

## 組み込みメトリック {#built-in-metrics}

組み込みメトリクスとは、 TiDB Cloudが収集し、**メトリクス**ページに表示される、クラスターの標準メトリクスの完全なセットを指します。これらのメトリクスを使用することで、パフォーマンスの問題を簡単に特定し、現在のデータベース環境が要件を満たしているかどうかを判断できます。

詳細については[TiDB Cloud組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)参照してください。

## 組み込みアラート {#built-in-alerting}

組み込みアラートとは、 TiDB Cloud がクラスターの監視を支援するために提供するクラスターアラートメカニズムを指します。現在、 TiDB Cloud は以下の3種類のアラートを提供しています。

-   リソース使用状況アラート

-   データ移行アラート

-   チェンジフィードアラート

TiDB Cloudコンソールの [アラート] ページでは、クラスターのアラートを表示したり、アラート ルールを編集したり、アラート通知メールをサブスクライブしたりできます。

詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)参照してください。

## クラスタイベント {#cluster-events}

TiDB Cloudでは、イベントはTiDB Cloudクラスターの変化を示します。TiDB TiDB Cloud はクラスターレベルで過去のイベントを記録し、クラスターのアクティビティを追跡できるようにします。記録されたイベントは、 **「イベント」**ページで確認できます。イベントの種類、ステータス、メッセージ、トリガー時刻、トリガーユーザーなどの情報が表示されます。

詳細については[TiDB Cloudクラスタイベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

## サードパーティの指標の統合 {#third-party-metrics-integrations}

TiDB Cloud を使用すると、次のいずれかのサードパーティ メトリック サービスを統合して、 TiDB Cloudアラートを受信し、TiDB クラスターのパフォーマンス メトリックを表示できます。

-   [Datadog統合](/tidb-cloud/monitor-datadog-integration.md)

-   [Prometheus と Grafana の統合 (ベータ版)](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

-   [New Relicとの統合](/tidb-cloud/monitor-new-relic-integration.md)
