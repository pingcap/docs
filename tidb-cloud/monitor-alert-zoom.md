---
title: Subscribe via Zoom
summary: Zoom経由でアラート通知を受け取ることで、TiDBクラスタを監視する方法を学びましょう。
---

# Zoom経由で登録する {#subscribe-via-zoom}

TiDB Cloud は、Zoom、[スラック](/tidb-cloud/monitor-alert-slack.md)、[メール](/tidb-cloud/monitor-alert-email.md)、[フラッシュデューティ](/tidb-cloud/monitor-alert-flashduty.md)、 [PagerDuty](/tidb-cloud/monitor-alert-pagerduty.md)を介してアラート通知を購読する簡単な方法を提供します。このドキュメントでは、Zoom 経由でアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラート購読は、 [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)インスタンス、 [TiDB Cloudプレミアム](/tidb-cloud/select-cluster-tier.md#premium)インスタンス、および[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスタで利用可能です。

## 前提条件 {#prerequisites}

-   Zoom経由での登録機能は、**エンタープライズ**または**プレミアム**サポートプランに加入している組織のみが利用できます。

-   Zoomで受信Webhookチャットボットを追加および設定するには、Zoomアカウントの管理者権限が必要です。

<CustomContent plan="essential,dedicated">

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

</CustomContent>

<CustomContent plan="premium">

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権、またはTiDB Cloudの対象のTiDB Cloud Premium インスタンスへの`Instance Manager`アクセス権が必要です。

</CustomContent>

## アラート通知を購読する {#subscribe-to-alert-notifications}

### ステップ1. Zoom Incoming Webhookアプリを追加する {#step-1-add-the-zoom-incoming-webhook-app}

1.  [Zoomアプリマーケットプレイス](https://marketplace.zoom.us/)にアカウント管理者としてサインインします。
2.  Zoom App Marketplaceの[受信Webhookアプリ](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ)ページに移動し、 **「追加」**をクリックしてこのアプリを追加します。アプリが事前承認されていない場合は、Zoom 管理者に連絡して、アカウントに対してこのアプリを承認してもらいます。詳細については、 [アプリの承認とアプリリクエストの管理](https://support.zoom.us/hc/en-us/articles/360027829671)参照してください。
3.  アプリが必要とする権限を確認し、 **「承認」**をクリックして受信Webhookアプリを追加します。

### ステップ2. ZoomのWebhook URLを生成する {#step-2-generate-a-zoom-webhook-url}

1.  Zoomデスクトップクライアントにサインインしてください。

2.  **チームチャット**タブをクリックしてください。

3.  **「アプリ」**の下にある**「受信Webhook」**を見つけて選択するか、上記からメッセージを受信したいチャットチャネルを選択してください。

4.  新しい接続を作成するには、次のコマンドを入力してください。 `${connectionName}`部分を、接続したい名前（例： `tidbcloud-alerts`に置き換えてください。

    ```shell
    /inc connect ${connectionName}
    ```

5.  このコマンドを実行すると、以下の詳細情報が返されます。

    -   **エンドポイント**。次の形式のウェブフック URL が提供されます: `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX` 。
    -   **検証トークン**

### ステップ3. TiDB Cloudから購読する {#step-3-subscribe-from-tidb-cloud}

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

5.  **購読者タイプの**ドロップダウンリストから**Zoom**を選択してください。

6.  **「名前」**欄に名前を、 **「URL」**欄にZoomのWebhook URLを、 **「トークン」**欄に認証トークンを入力してください。

7.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、接続を再試行してください。

8.  購読を完了するには、 **「保存」**をクリックしてください。

または、対象のTiDB Cloud Dedicatedクラスタの**アラート**ページの右上にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

または、クラスターの**アラート**ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="essential">

TiDB Cloud Essentialインスタンスのアラート通知を購読するには、以下の手順を実行してください。

> **ヒント：**
>
> TiDB Cloud Essentialの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のTiDB Cloud Essentialインスタンスをお持ちの場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Essentialインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**Zoom**を選択してください。

5.  **「名前」**欄に名前を、 **「URL」**欄にZoomのWebhook URLを、 **「トークン」**欄に認証トークンを入力してください。

6.  **「接続テスト」**をクリックしてください。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラーメッセージが表示されます。メッセージの指示に従って問題を解決し、接続を再試行してください。

7.  購読を完了するには、 **「保存」**をクリックしてください。

または、対象のTiDB Cloud Essentialインスタンスの**アラート**ページの右上隅にある**「購読」を**クリックすることもできます。**アラート購読**ページに移動します。

</CustomContent>

<CustomContent plan="premium">

TiDB Cloud Premiumインスタンスのアラート通知を購読するには、以下の手順に従ってください。

> **ヒント：**
>
> TiDB Cloud Premiumの場合、アラートの購読は現在のインスタンス内のすべてのアラートに適用されます。複数のTiDB Cloud Premiumインスタンスをお持ちの場合は、各インスタンスごとに個別に購読する必要があります。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Premiumインスタンスの名前をクリックして、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[アラートの購読]**をクリックします。

3.  **アラート購読**ページで、右上隅にある**「購読者を追加」**をクリックします。

4.  **購読者タイプの**ドロップダウンリストから**Zoom**を選択してください。

5.  **「名前」**欄に名前を、 **「URL」**欄にZoomのWebhook URLを、 **「トークン」**欄に認証トークンを入力してください。

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
