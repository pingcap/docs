---
title: Migrate Prometheus Integrations
summary: 従来のプロジェクト レベルの Prometheus 統合から新しいクラスター レベルの Prometheus 統合に移行する方法を学習します。
---

# Prometheus統合の移行 {#migrate-prometheus-integrations}

TiDB Cloud は現在、 [Prometheusの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)クラスタレベルで管理し、よりきめ細かな制御と構成を提供しています。従来のプロジェクトレベルの Prometheus 統合（ベータ版）は、2026年1月9日に廃止されます。組織でこれらの従来の統合をまだ使用している場合は、このガイドに従って新しいクラスタレベルの Prometheus 統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloudのサードパーティ メトリック統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。

## 移行手順 {#migration-steps}

Prometheus 統合を移行するには、次の手順を実行します。

### ステップ 1. レガシー プロジェクト レベルの Prometheus 統合を削除する (ベータ版) {#step-1-delete-the-legacy-project-level-prometheus-integrations-beta}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、左上隅のコンボ ボックスを使用して対象プロジェクトに切り替えます。

2.  左側のナビゲーション パネルで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **統合**&gt; **Prometheus への統合 (ベータ版)**モジュールで、 **Scrape_config ファイル**を選択し、**削除**をクリックします。

4.  表示されたダイアログで`Delete`と入力して、レガシー統合の削除を確認します。

### ステップ2. 各クラスターに新しいクラスターレベルのPrometheus統合を作成する {#step-2-create-a-new-cluster-level-prometheus-integration-for-each-cluster}

プロジェクト内の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)ごとに次の手順を繰り返します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション パネルで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、新しいPrometheus統合を作成します。詳細については、 [TiDB Cloud をPrometheus および Grafana と統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)参照してください。

## プロジェクトレベルの Prometheus 統合の削除の影響 (ベータ版) {#impact-of-deleting-the-project-level-prometheus-integration-beta}

プロジェクトレベルの Prometheus 統合（ベータ版）を削除すると、プロジェクト内のすべてのクラスターから Prometheus エンドポイントへのメトリクスの公開が直ちに停止されます。これにより、下流のデータが一時的に失われ、新しいクラスターレベルの Prometheus 統合を設定するまで、統合関連サービス（モニタリングやアラートなど）が中断されます。

## サポートにお問い合わせください {#contact-support}

サポートが必要な場合は、 TiDB Cloudサポート<a href="mailto:support@pingcap.com">[support@pingcap.com](mailto:support@pingcap.com)</a>にお問い合わせいただくか、テクニカル アカウント マネージャー (TAM) にご連絡ください。
