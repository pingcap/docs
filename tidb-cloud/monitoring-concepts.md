---
title: Monitoring
summary: TiDB Cloudの監視に関する概念について学びましょう。
---

# 監視 {#monitoring}

TiDB Cloudのモニタリング機能は、TiDBのパフォーマンスを監視し、アクティビティを追跡し、問題に迅速に対応するためのツールと統合機能を提供します。

## 組み込みの指標 {#built-in-metrics}

組み込みメトリクスとは<CustomContent plan="dedicated">クラスタ</CustomContent>TiDB Cloudが収集し、<CustomContent plan="starter,essential,premium">実例</CustomContent>レベルの**メトリクス**ページに表示する一連の標準メトリクスを指します。これらのメトリクスを使用することで、パフォーマンスの問題を容易に特定し、現在のデータベース展開が要件を満たしているかどうかを判断できます。

<CustomContent plan="starter,essential,dedicated">

詳細については、 [TiDB Cloud の組み込みメトリクス](/tidb-cloud/built-in-monitoring.md)を参照してください。

</CustomContent>
<CustomContent plan="premium">

詳細については、 [TiDB Cloud Premium の組み込みメトリクス](/tidb-cloud/premium/built-in-monitoring-premium.md)を参照してください。

</CustomContent>

## 内蔵アラート機能 {#built-in-alerting}

組み込みアラートとは、 TiDB Cloud EssentialインスタンスおよびTiDB Cloud Dedicatedクラスタの監視を支援するためにTiDB Cloudが提供するアラートメカニズムのことです。現在、 TiDB Cloudは以下の3種類のアラートを提供しています。

-   リソース使用状況アラート

-   データ移行に関する警告

-   変更フィードアラート

TiDB Cloudコンソールの「アラート」ページでは、 TiDB Cloud EssentialインスタンスまたはTiDB Cloud Dedicatedクラスタのアラートを表示したり、アラートルールを編集したり、アラート通知メールを購読したりできます。

詳細については、 [TiDB Cloudの組み込みアラート機能](/tidb-cloud/monitor-built-in-alerting.md)を参照してください。

## イベント {#events}

TiDB Cloudでは、イベントはTiDB Cloudリソースの変更を示します。

-   TiDB Cloud StarterおよびEssentialインスタンスの場合、 TiDB Cloudはインスタンスレベルで履歴イベントをログに記録します。
-   TiDB Cloud Dedicatedクラスタの場合、 TiDB Cloudはクラスタレベルで履歴イベントをログに記録します。

**イベント**ページでは、イベントの種類、ステータス、メッセージ、トリガー時刻、トリガーユーザーなど、記録されたイベントを確認できます。

詳細については、[イベント](/tidb-cloud/tidb-cloud-events.md)を参照してください。

## サードパーティ製メトリクスの統合 {#third-party-metrics-integrations}

TiDB Cloud、以下のサードパーティ製メトリクスサービスのいずれかを統合して、 TiDB Cloudアラートを受信したり、 TiDB Cloud Dedicatedクラスタのパフォーマンスメトリクスを表示したりできます。

-   [Datadogとの連携](/tidb-cloud/monitor-datadog-integration.md)

-   [PrometheusとGrafanaの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)

-   [New Relicとの連携](/tidb-cloud/monitor-new-relic-integration.md)
