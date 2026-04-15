---
title: Migrate Prometheus Integrations
summary: 従来のプロジェクトレベルのPrometheus統合から、新しいクラスタレベルのPrometheus統合への移行方法を学びましょう。
---

# Prometheus統合の移行 {#migrate-prometheus-integrations}

TiDB Cloud は、 [Prometheusとの統合](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)クラスタレベルで管理するようになり、よりきめ細かな制御と構成が可能になりました。従来のプロジェクトレベルの Prometheus 統合 (ベータ版) は、2026 年 1 月 9 日に廃止されます。組織でこれらの従来の統合をまだ使用している場合は、このガイドに従って新しいクラスタレベルの Prometheus 統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。

## 移行手順 {#migration-steps}

Prometheusとの連携を移行するには、以下の手順を実行してください。

### ステップ1. 従来のプロジェクトレベルのPrometheus統合を削除します（ベータ版） {#step-1-delete-the-legacy-project-level-prometheus-integrations-beta}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションパネルで、 **「プロジェクト設定」**の下にある**「統合」**をクリックします。

4.  **[統合]** &gt; **[Prometheus (BETA) との統合]**モジュールで、 **[Scrape_config Files]**を選択し、 **[削除]**をクリックします。

5.  表示されたダイアログで、 `Delete`と入力して、従来の統合機能の削除を確認します。

### ステップ2. 各クラスターに対して、新しいクラスターレベルのPrometheus統合を作成します。 {#step-2-create-a-new-cluster-level-prometheus-integration-for-each-cluster}

プロジェクト内の各[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して、以下の手順を繰り返してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションパネルで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、新しい Prometheus 統合を作成します。詳細については、 [TiDB CloudをPrometheusおよびGrafanaと統合する](/tidb-cloud/monitor-prometheus-and-grafana-integration.md)を参照してください。

## プロジェクトレベルのPrometheus統合を削除した場合の影響（ベータ版） {#impact-of-deleting-the-project-level-prometheus-integration-beta}

プロジェクトレベルのPrometheus統合（ベータ版）を削除すると、プロジェクト内のすべてのクラスターがPrometheusエンドポイントにメトリクスを公開しなくなります。これにより、下流データが一時的に失われ、新しいクラスターレベルのPrometheus統合を設定するまで、統合関連のサービス（監視やアラートなど）が中断されます。

## サポートにお問い合わせください {#contact-support}

サポートが必要な場合は、 TiDB Cloudサポートまでお問い合わせください。<a href="mailto:support@pingcap.com"></a> [support@pi​​ngcap.com](mailto:support@pingcap.com)でお問い合わせいただくか、テクニカルアカウントマネージャー（TAM）までご連絡ください。
