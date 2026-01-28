---
title: Subscribe via PagerDuty
summary: PagerDuty 経由でアラート通知を取得して TiDB クラスターを監視する方法を学習します。
---

# PagerDuty経由で購読する {#subscribe-via-pagerduty}

TiDB Cloudは、 [スラック](/tidb-cloud/monitor-alert-slack.md) 、 [メール](/tidb-cloud/monitor-alert-email.md) [フラッシュデューティ](/tidb-cloud/monitor-alert-flashduty.md)介してアラート通知を簡単に購読する方法を提供します。このドキュメントでは[ズーム](/tidb-cloud/monitor-alert-zoom.md) PagerDutyを介してアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラート サブスクリプションは[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対してのみ利用可能です。

## 前提条件 {#prerequisites}

-   PagerDuty 経由のサブスクライブ機能は、 **Enterprise**または**Premium** [サポートプラン](/tidb-cloud/connected-care-overview.md)にサブスクライブしている組織でのみ利用できます。

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

プロジェクト内のクラスターのアラート通知を受信するには、次の手順を実行します。

### ステップ1. PagerDuty統合キーを生成する {#step-1-generate-a-pagerduty-integration-key}

1.  [PagerDuty イベント API v2 の概要](https://developer.pagerduty.com/docs/events-api-v2-overview#getting-started)の手順に従って、 **Events API v2**タイプの統合キーを生成します。
2.  生成された統合キーを保存して、次の手順で使用します。

### ステップ2. TiDB Cloudからサブスクライブする {#step-2-subscribe-from-tidb-cloud}

> **ヒント：**
>
> アラートのサブスクリプションは、現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のクラスターがある場合は、一度だけサブスクリプションすれば済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。

3.  **「アラート サブスクリプション」**ページで、右上隅の**「サブスクライバーの追加」**をクリックします。

4.  **「サブスクライバー タイプ」**ドロップダウン リストから**PagerDuty を**選択します。

5.  「**名前」**フィールドに名前を入力し、 **「統合キー」**フィールドに PagerDuty 統合キーを入力します。

6.  **[接続テスト]**をクリックします。

    -   テストが成功すると、 **[保存]**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題を解決し、接続を再試行してください。

7.  **「保存」**をクリックしてサブスクリプションを完了します。

または、クラスターの**アラート**ページの右上隅にある**「サブスクライブ」**をクリックすることもできます。**アラートサブスクライバー**ページに移動します。

アラート条件が変更されない場合、アラートは 3 時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

プロジェクト内のクラスターのアラート通知を受信したくない場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。
3.  **[アラート サブスクリプション]**ページで、削除する対象のサブスクライバーの行を見つけて、 **[...]** &gt; **[サブスクリプション解除]**をクリックします。
4.  登録解除を確認するには、 **「登録解除」**をクリックします。
