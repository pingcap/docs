---
title: Monitoring
summary: TiDB Cloudの監視の概念について学習します。
---

# 監視 {#monitoring}

TiDB Cloudのモニタリングでは、クラスターのパフォーマンスを監視し、アクティビティを追跡し、問題にタイムリーに対応できるようにするツールと統合が提供されます。

## 組み込みメトリック {#built-in-metrics}

組み込みメトリックとは、 TiDB Cloud が収集してメトリック ページに表示する、クラスターの標準メトリックの完全なセットを指します。これらのメトリックを使用すると、パフォーマンスの問題を簡単に特定し、現在のデータベース展開が要件を満たしているかどうかを判断できます。

詳細については[TiDB Cloud組み込みメトリック](/tidb-cloud/built-in-monitoring.md)参照してください。

## 組み込みアラート {#built-in-alerting}

組み込みアラートとは、クラスターの監視を支援するためにTiDB Cloud が提供するクラスター アラート メカニズムを指します。現在、 TiDB Cloud は次の 3 種類のアラートを提供しています。

-   リソース使用状況アラート

-   データ移行アラート

-   チェンジフィードアラート

TiDB Cloudコンソールの [アラート] ページでは、クラスターのアラートを表示したり、アラート ルールを編集したり、アラート通知メールをサブスクライブしたりできます。

詳細については[TiDB Cloud組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)参照してください。

## クラスタイベント {#cluster-events}

TiDB Cloudでは、イベントはTiDB Cloudクラスターの変更を示します。TiDB TiDB Cloud はクラスター レベルで履歴イベントを記録し、クラスターのアクティビティを追跡できるようにします。イベント タイプ、ステータス、メッセージ、トリガー時間、トリガー ユーザーなど、ログに記録されたイベントは、 **[イベント]**ページで確認できます。

詳細については[TiDB Cloudクラスタイベント](/tidb-cloud/tidb-cloud-events.md)参照してください。

## サードパーティの指標の統合（ベータ版） {#third-party-metrics-integrations-beta}

TiDB Cloud を使用すると、次のサードパーティ メトリック サービスを統合して、 TiDB Cloudアラートを受信し、TiDB クラスターのパフォーマンス メトリックを表示できます。

-   Datadog 統合

-   PrometheusとGrafanaの統合

-   New Relic 統合

現在、これらのサードパーティ メトリックの統合はベータ版です。

詳細については[サードパーティのメトリクス統合（ベータ版）](/tidb-cloud/third-party-monitoring-integrations.md)参照してください。
