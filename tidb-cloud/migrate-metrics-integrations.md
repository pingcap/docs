---
title: Migrate Datadog and New Relic Integrations
summary: 従来のプロジェクト レベルのメトリクス統合から、Datadog と New Relic の新しいクラスター レベルの統合に移行する方法を学習します。
---

# DatadogとNew Relicの統合の移行 {#migrate-datadog-and-new-relic-integrations}

TiDB Cloud は、Datadog と New Relic の統合をクラスターレベルで管理できるようになり、よりきめ細かな制御と構成が可能になりました。従来のプロジェクトレベルの Datadog と New Relic の統合は、2025 年 10 月 31 日をもって廃止されます。組織でこれらの従来の統合をまだご利用の場合は、このガイドに従って新しいクラスターレベルの統合に移行し、メトリクス関連サービスへの影響を最小限に抑えてください。

## 前提条件 {#prerequisites}

-   TiDB Cloudのサードパーティ メトリック統合を設定するには、 TiDB Cloudで`Organization Owner`または`Project Owner`アクセス権が必要です。

## 移行手順 {#migration-steps}

### ステップ1. レガシープロジェクトレベルのDatadogとNew Relicの統合を削除する {#step-1-delete-the-legacy-project-level-datadog-and-new-relic-integrations}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、左上隅のコンボ ボックスを使用して対象プロジェクトに切り替えます。

2.  左側のナビゲーション パネルで、 **[プロジェクト設定]** &gt; **[統合]**をクリックします。

3.  **[統合]**ページで、 **[Datadog への統合]**または**[New Relic への統合]**の横にある**[削除]**をクリックします。

4.  表示されたダイアログで`Delete`と入力して、レガシー統合の削除を確認します。

### ステップ2. 各クラスターに新しいDatadogまたはNew Relic統合を作成する {#step-2-create-the-new-datadog-or-new-relic-integration-for-each-cluster}

プロジェクト内の[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)ごとに次の手順を繰り返します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、左上隅のコンボ ボックスを使用してターゲット クラスターに切り替えます。

2.  左側のナビゲーション パネルで、 **[設定]** &gt; **[統合]**をクリックします。

3.  **「統合」**ページで、必要に応じて新しい統合を作成します。詳細については、 [TiDB CloudとDatadogの統合](/tidb-cloud/monitor-datadog-integration.md)と[TiDB CloudとNew Relicの統合](/tidb-cloud/monitor-new-relic-integration.md)参照してください。

## 影響声明 {#impact-statement}

プロジェクトレベルの統合を削除すると、プロジェクト内のすべてのクラスターからのメトリクスの送信が直ちに停止されます。これにより、下流のデータが一時的に失われ、新しいクラスターレベルの統合を作成するまで、統合関連サービス（モニタリングやアラートなど）が中断されます。

## サポートにお問い合わせください {#contact-support}

サポートが必要な場合は、 TiDB Cloudサポート<a href="mailto:support@pingcap.com">[support@pingcap.com](mailto:support@pingcap.com)</a>にお問い合わせいただくか、テクニカル アカウント マネージャー (TAM) にご連絡ください。
