---
title: Subscribe via Zoom
summary: Zoom 経由でアラート通知を受信して TiDB クラスターを監視する方法を学びます。
---

# Zoomで登録する {#subscribe-via-zoom}

TiDB Cloud、 [ズーム](https://www.zoom.com/) [メール](/tidb-cloud/monitor-alert-email.md)方法でアラート通知を簡単に購読できます。このドキュメントでは[スラック](/tidb-cloud/monitor-alert-slack.md) Zoom経由でアラート通知を購読する方法について説明します。

> **注記：**
>
> 現在、アラートサブスクリプションは[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対してのみ利用可能です。

## 前提条件 {#prerequisites}

-   Zoom 経由のサブスクリプション機能は、**エンタープライズ**または**プレミアム**サポート プランに加入している組織でのみご利用いただけます。

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

-   Zoom で Incoming Webhook チャットボットを追加して構成するには、Zoom アカウントの管理者権限が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

### ステップ1. Zoom Incoming Webhookアプリを追加する {#step-1-add-the-zoom-incoming-webhook-app}

1.  アカウント管理者として[Zoomアプリマーケットプレイス](https://marketplace.zoom.us/)にサインインします。
2.  Zoomアプリマーケットプレイスの[受信Webhookアプリ](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ)ページに移動し、 **「追加」**をクリックしてこのアプリを追加してください。アプリが事前承認されていない場合は、Zoom管理者に連絡して、アカウントへのアプリの承認を依頼してください。詳しくは[アプリの承認とアプリリクエストの管理](https://support.zoom.us/hc/en-us/articles/360027829671)ご覧ください。
3.  アプリに必要な権限を確認し、 **「承認」**をクリックして Incoming Webhook アプリを追加します。

### ステップ2. ZoomウェブフックURLを生成する {#step-2-generate-a-zoom-webhook-url}

1.  Zoom デスクトップ クライアントにサインインします。

2.  **チームチャット**タブをクリックします。

3.  **[アプリ]**の下で、 **[受信 Webhook]**を見つけて選択するか、メッセージを受信したいチャット チャネルを上から選択します。

4.  新しい接続を作成するには、以下のコマンドを入力します。1 `${connectionName}`希望の接続名（例： `tidbcloud-alerts` ）に置き換えてください。

    ```shell
    /inc connect ${connectionName}
    ```

5.  このコマンドは次の詳細を返します。

    -   **エンドポイント**。2 `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX`形式でWebhook URLが提供されます。
    -   **検証トークン**

### ステップ3. TiDB Cloudからサブスクライブする {#step-3-subscribe-from-tidb-cloud}

> **ヒント：**
>
> アラートサブスクリプションは、現在のプロジェクト内のすべてのアラートに適用されます。プロジェクト内に複数のクラスターがある場合は、一度だけサブスクリプションすれば済みます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。

2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。

3.  **アラート サブスクリプション**ページで、右上隅の**[サブスクライバーの追加]**をクリックします。

4.  **「サブスクライバータイプ」**ドロップダウンリストから**「Zoom」**を選択します。

5.  **「名前」**フィールドに名前、 **「URL」**フィールドに Zoom Webhook URL、 **「トークン」**フィールドに検証トークンを入力します。

6.  **[接続テスト]**をクリックします。

    -   テストが成功すると、 **[保存]**ボタンが表示されます。
    -   テストに失敗した場合は、エラーメッセージが表示されます。メッセージに従ってトラブルシューティングを行い、接続を再試行してください。

7.  **「保存」**をクリックしてサブスクリプションを完了します。

または、クラスターの**アラート**ページの右上隅にある**「サブスクライブ」**をクリックすることもできます。**アラートサブスクライバー**ページに移動します。

アラート条件が変更されない場合、アラートは 3 時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

プロジェクト内のクラスターのアラート通知を受信したくない場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用してターゲット プロジェクトに切り替えます。
2.  左側のナビゲーション ペインで、 **[プロジェクト設定]** &gt; **[アラート サブスクリプション]**をクリックします。
3.  **[アラート サブスクリプション]**ページで、削除する対象のサブスクライバーの行を見つけて、 **[...]** &gt; **[サブスクリプション解除]**をクリックします。
4.  登録解除を確認するには、 **「登録解除」を**クリックします。
