---
title: Migrate Datadog and New Relic Integrations
summary: DatadogとNew Relicにおける、従来のプロジェクトレベルのメトリクス統合から新しいクラスタレベルの統合への移行方法を学びましょう。
---

# DatadogとNew Relicの統合を移行する {#migrate-datadog-and-new-relic-integrations}

TiDB Cloudは、DatadogおよびNew Relicとの連携をクラスタレベルで管理するようになり、よりきめ細かな制御と設定が可能になりました。従来のプロジェクトレベルのDatadogおよびNew Relic連携は、2025年10月31日に廃止されます。組織でこれらの従来の連携をまだ使用している場合は、このガイドに従って新しいクラスタレベルの連携に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloudのサードパーティ メトリクス統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。

## 移行手順 {#migration-steps}

### ステップ1：従来のプロジェクトレベルのDatadogおよびNew Relic統合を削除します。 {#step-1-delete-the-legacy-project-level-datadog-and-new-relic-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションパネルで、 **「プロジェクト設定」**の下にある**「統合」**をクリックします。

4.  **統合**ページで、 **「Datadogとの統合」**または**「New Relicとの統合」の**横にある**「削除」を**クリックします。

5.  表示されたダイアログで、 `Delete`と入力して、従来の統合機能の削除を確認します。

### ステップ2. 各クラスターごとに新しいDatadogまたはNew Relic統合を作成します。 {#step-2-create-the-new-datadog-or-new-relic-integration-for-each-cluster}

プロジェクト内の各[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して、以下の手順を繰り返してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションパネルで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、必要に応じて新しい統合を作成します。詳細については、 [TiDB CloudとDatadogを統合する](/tidb-cloud/monitor-datadog-integration.md)および[TiDB CloudとNew Relicを統合する](/tidb-cloud/monitor-new-relic-integration.md)参照してください。

## インパクトステートメント {#impact-statement}

プロジェクトレベルの統合を削除すると、プロジェクト内のすべてのクラスターからのメトリクス送信が即座に停止します。これにより、下流データが一時的に失われ、新しいクラスターレベルの統合を作成するまで、統合関連のサービス（監視やアラートなど）が中断されます。

## サポートにお問い合わせください {#contact-support}

サポートが必要な場合は、 TiDB Cloudサポートまでお問い合わせください。<a href="mailto:support@pingcap.com"></a> [support@pi​​ngcap.com](mailto:support@pingcap.com)でお問い合わせいただくか、テクニカルアカウントマネージャー（TAM）までご連絡ください。
