---
title: Subscribe via Slack
summary: Slack経由でアラート通知を受け取ることで、TiDBクラスタを監視する方法を学びましょう。
---

# Slack経由で購読する {#subscribe-via-slack}

TiDB Cloud、Slack、[メール](/tidb-cloud/monitor-alert-email.md)、[ズーム](/tidb-cloud/monitor-alert-zoom.md)、[フラッシュデューティ](/tidb-cloud/monitor-alert-flashduty.md)、 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)経由でアラート通知を購読する簡単な方法が提供されます。このドキュメントでは、Slack 経由でアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラート購読は、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンス、 [TiDB Cloudプレミアム](/tidb-cloud/select-cluster-tier.md#premium)インスタンス、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタで利用可能です。

## 前提条件 {#prerequisites}

-   Slack経由での購読機能は、**エンタープライズ**または**プレミアム**サポートプランに加入している組織のみが利用できます。

<CustomContent plan="essential,dedicated">

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

</CustomContent>

<CustomContent plan="premium">

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象のTiDB Cloud Premium インスタンスへの`Instance Manager`アクセス権が必要です。

</CustomContent>

## アラート通知を購読する {#subscribe-to-alert-notifications}

### ステップ1：SlackウェブフックURLを生成する {#step-1-generate-a-slack-webhook-url}

1.  まだお持ちでない場合は、 [Slackアプリを作成する](https://api.slack.com/apps/new)。 **[新しいアプリの作成]**をクリックし、 **[最初から]**を選択します。名前を入力し、アプリを関連付けるワークスペースを選択して、 **[アプリの作成] を**クリックします。
2.  アプリの設定ページに移動します。[アプリの管理ダッシュボード](https://api.slack.com/apps)から設定をロードできます。
3.  **「受信Webhook」**タブをクリックし、 **「受信Webhookを有効にする」**を**オン**に切り替えます。
4.  **「ワークスペースに新しいWebhookを追加」**をクリックします。
5.  アラート通知を受信するチャネルを選択し、 **「承認」**を選択してください。受信Webhookをプライベートチャネルに追加する必要がある場合は、まずそのチャネルに参加している必要があります。

**「ワークスペースの Webhook URL」**セクションに、次の形式で新しいエントリが表示されます: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX` 。

### ステップ2. TiDB Cloudから購読する {#step-2-subscribe-from-tidb-cloud}

アラート通知のサブスクリプションは[TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

TiDB Cloud Dedicatedクラスターのアラート通知を購読するには、以下の手順に従ってください。

> **ヒント：**
>
> TiDB Cloud Dedicatedの場合、アラートの購読は現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のTiDB Cloud Dedicatedクラスタがある場合でも、購読は一度だけで済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。

2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。

3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「アラート購読」**をクリックします。

4.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

5.  **購読者タイプの**ドロップダウンリストから**「Slack」**を選択してください。

6.  **「名前」**欄に名前を、「 **URL」**欄にSlackのWebhook URLを入力してください。

7.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

8.  購読を完了するには、 **「保存」**をクリックしてください。

または、対象のTiDB Cloud Dedicatedクラスタの**アラート**ページの右上にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

または、クラスターの**アラート**ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="essential">

> **ヒント：**
>
> TiDB Cloud Essentialの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のTiDB Cloud Essentialインスタンスをお持ちの場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**「Slack」**を選択してください。

5.  **「名前」**欄に名前を、「 **URL」**欄にSlackのWebhook URLを入力してください。

6.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

7.  購読を完了するには、 **「保存」**をクリックしてください。

または、対象のTiDB Cloud Essentialインスタンスの**アラート**ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="premium">

> **ヒント：**
>
> TiDB Cloud Premiumの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のTiDB Cloud Premiumインスタンスをお持ちの場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Premiumインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**「Slack」**を選択してください。

5.  **「名前」**欄に名前を、「 **URL」**欄にSlackのWebhook URLを入力してください。

6.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

7.  購読を完了するには、 **「保存」**をクリックしてください。

または、対象のTiDB Cloud Premiumインスタンスの**アラート**ページの右上にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

アラート条件が変化しない場合、アラートは3時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

アラート通知の受信を停止したい場合は、以下の手順に従ってください。手順は[TiDB Cloudプラン](/tidb-cloud/select-cluster-tier.md)によって異なります。

<CustomContent plan="dedicated">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、 **[プロジェクト ビュー]**タブをクリックします。
2.  プロジェクトビューで、対象のプロジェクトを見つけて、そのプロジェクトの<MDSvgIcon name="icon-project-settings" />をクリックします。
3.  左側のナビゲーションペインで、 **「プロジェクト設定」**の下にある**「アラート購読」**をクリックします。
4.  **アラート購読**ページで、削除する対象の購読者の行を見つけて、 **[...]** &gt; **[購読解除]**をクリックします。
5.  購読解除を確定するには、 **「購読解除」**をクリックしてください。

</CustomContent>

<CustomContent plan="essential">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。
3.  **アラート購読**ページで、削除する対象の購読者の行を見つけて、 **[...]** &gt; **[購読解除]**をクリックします。
4.  購読解除を確定するには、 **「購読解除」**をクリックしてください。

</CustomContent>

<CustomContent plan="premium">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Premiumインスタンスの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。
3.  **アラート購読**ページで、削除する対象の購読者の行を見つけて、 **[...]** &gt; **[購読解除]**をクリックします。
4.  購読解除を確定するには、 **「購読解除」**をクリックしてください。

</CustomContent>
