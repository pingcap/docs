---
title: Subscribe via Flashduty
summary: Flashduty 経由でアラート通知を取得して TiDB クラスターを監視する方法を学習します。
---

# Flashdutyで購読する {#subscribe-via-flashduty}

TiDB Cloudは、 [スラック](/tidb-cloud/monitor-alert-slack.md) 、 [メール](/tidb-cloud/monitor-alert-email.md) [ページャーデューティ](/tidb-cloud/monitor-alert-pagerduty.md)介してアラート通知を簡単に購読する方法を提供します。このドキュメントでは[ズーム](/tidb-cloud/monitor-alert-zoom.md) Flashdutyを介してアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラート サブスクリプションは[TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential)および[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで利用できます。

## 前提条件 {#prerequisites}

-   Flashduty 機能によるサブスクライブは、 **Enterprise**または**Premium** [サポートプラン](/tidb-cloud/connected-care-overview.md)にサブスクライブしている組織でのみ利用できます。

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

クラスターのアラート通知を受信するには、次の手順を実行します。

### ステップ1. Flashduty Webhook URLを生成する {#step-1-generate-a-flashduty-webhook-url}

1.  [Flashduty Prometheus 統合](https://docs.flashcat.cloud/en/flashduty/prometheus-integration-guide)の手順に従って、Webhook URL を生成します。
2.  次のステップで使用するために、生成された Webhook URL を保存します。

### ステップ2. TiDB Cloudからサブスクライブする {#step-2-subscribe-from-tidb-cloud}

アラート通知サブスクリプションはクラスター プランによって異なります。

<CustomContent plan="dedicated">

> **ヒント：**
>
> アラートのサブスクリプションは、現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のクラスターがある場合は、一度だけサブスクリプションすれば済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。

3.  **「アラート サブスクリプション」**ページで、右上隅の**「サブスクライバーの追加」**をクリックします。

4.  **「サブスクライバー タイプ」**ドロップダウン リストから**「Flashduty」**を選択します。

5.  **「名前」**フィールドに名前を入力し、 **「Webhook URL」**フィールドに Flashduty Webhook URL を入力します。

6.  **[接続テスト]**をクリックします。

    -   テストが成功すると、 **[保存]**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題を解決し、接続を再試行してください。

7.  **「保存」**をクリックしてサブスクリプションを完了します。

</CustomContent>

<CustomContent plan="essential">

> **ヒント：**
>
> アラートサブスクリプションは、現在のクラスター内のすべてのアラートに適用されます。複数のクラスターがある場合は、各クラスターを個別にサブスクライブする必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット クラスターに切り替えます。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[アラート サブスクリプション]**をクリックします。

3.  **「アラート サブスクリプション」**ページで、右上隅の**「サブスクライバーの追加」**をクリックします。

4.  **「サブスクライバー タイプ」**ドロップダウン リストから**「Flashduty」**を選択します。

5.  **「名前」**フィールドに名前を入力し、 **「Webhook URL」**フィールドに Flashduty Webhook URL を入力します。

6.  **[接続テスト]**をクリックします。

    -   テストが成功すると、 **[保存]**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従って問題を解決し、接続を再試行してください。

7.  **「保存」**をクリックしてサブスクリプションを完了します。

</CustomContent>

または、クラスターの**アラート**ページの右上隅にある**「サブスクライブ」**をクリックすることもできます。 **「アラートサブスクリプション」**ページに移動します。

アラート条件が変更されない場合、アラートは 3 時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

アラート通知の受信を停止したい場合は、以下の手順に従ってください。手順はクラスタープランによって異なります。

<CustomContent plan="dedicated">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。
3.  **[アラート サブスクリプション]**ページで、削除する対象のサブスクライバーの行を見つけて、 **[...]** &gt; **[サブスクリプション解除]**をクリックします。
4.  登録解除を確認するには、 **「登録解除」**をクリックします。

</CustomContent>

<CustomContent plan="essential">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット クラスターに切り替えます。
2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[アラート サブスクリプション]**をクリックします。
3.  **[アラート サブスクリプション]**ページで、削除する対象のサブスクライバーの行を見つけて、 **[...]** &gt; **[サブスクリプション解除]**をクリックします。
4.  登録解除を確認するには、 **「登録解除」**をクリックします。

</CustomContent>
