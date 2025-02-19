---
title: Subscribe via Zoom
summary: Zoom 経由でアラート通知を受信して TiDB クラスターを監視する方法を学習します。
---

# Zoomで登録する {#subscribe-via-zoom}

TiDB Cloud、 [ズーム](https://www.zoom.com/) 、 [スラック](/tidb-cloud/monitor-alert-slack.md) 、 [メール](/tidb-cloud/monitor-alert-email.md)を介してアラート通知を購読する簡単な方法が提供されています。このドキュメントでは、Zoom 経由でアラート通知を購読する方法について説明します。

## 前提条件 {#prerequisites}

-   Zoom 経由のサブスクリプション機能は、**エンタープライズ**または**プレミアム**サポート プランに加入している組織でのみ利用できます。

-   TiDB Cloudのアラート通知を購読するには、組織への`Organization Owner`アクセス権またはTiDB Cloudの対象プロジェクトへの`Project Owner`アクセス権が必要です。

-   Zoom で Incoming Webhook チャットボットを追加して構成するには、Zoom アカウントの管理者権限が必要です。

## アラート通知を購読する {#subscribe-to-alert-notifications}

### ステップ1. Zoom Incoming Webhookアプリを追加する {#step-1-add-the-zoom-incoming-webhook-app}

1.  アカウント管理者として[Zoom アプリマーケットプレイス](https://marketplace.zoom.us/)にサインインします。
2.  Zoom アプリマーケットプレイスの[受信Webhookアプリ](https://marketplace.zoom.us/apps/eH_dLuquRd-VYcOsNGy-hQ)ページに移動し、 **[追加]**をクリックしてこのアプリを追加します。アプリが事前に承認されていない場合は、Zoom 管理者に連絡して、アカウントでこのアプリを承認してもらってください。詳細については、 [アプリの承認とアプリリクエストの管理](https://support.zoom.us/hc/en-us/articles/360027829671)参照してください。
3.  アプリに必要な権限を確認し、 **「承認」**をクリックして Incoming Webhook アプリを追加します。

### ステップ2. ZoomウェブフックURLを生成する {#step-2-generate-a-zoom-webhook-url}

1.  Zoom デスクトップ クライアントにサインインします。

2.  **チームチャット**タブをクリックします。

3.  **[アプリ]**の下で、 **[受信 Webhook]**を見つけて選択するか、メッセージを受信したいチャット チャネルを上から選択します。

4.  新しい接続を作成するには、次のコマンドを入力します。 `${connectionName}`希望の接続名に置き換える必要があります (例: `tidbcloud-alerts` )。

    ```shell
    /inc connect ${connectionName}
    ```

5.  このコマンドは次の詳細を返します。

    -   **エンドポイント**。次の形式で Webhook URL が提供されます: `https://integrations.zoom.us/chat/webhooks/incomingwebhook/XXXXXXXXXXXXXXXXXXXXXXXX` 。
    -   **検証トークン**

### ステップ3. TiDB Cloudからサブスクライブする {#step-3-subscribe-from-tidb-cloud}

> **ヒント：**
>
> アラートのサブスクリプションは、現在のプロジェクト内のすべてのアラートを対象としています。プロジェクト内に複数のクラスターがある場合は、一度だけサブスクライブする必要があります。

1.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定] を**クリックします。</mdsvgicon>

2.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「アラート サブスクリプション」**をクリックします。

3.  **購読者を追加を**クリック

4.  **「サブスクライバータイプ」**ドロップダウンリストから**「Zoom」**を選択します。

5.  **「名前」**フィールドに名前を入力し、 **「URL」**フィールドに Zoom Webhook URL を入力し、 **「トークン」**フィールドに検証トークンを入力します。

6.  **[接続テスト]**をクリックします。

    -   テストが成功すると、「**保存」**ボタンが表示されます。
    -   テストが失敗した場合は、エラー メッセージが表示されます。メッセージに従ってトラブルシューティングを行い、接続を再試行してください。

7.  **「保存」**をクリックしてサブスクリプションを完了します。

または、クラスターの**アラート**ページの右上隅にある [**サブスクライブ]**をクリックすることもできます。**アラート サブスクライバー**ページに移動します。

アラート条件が変更されない場合、アラートは 3 時間ごとに通知を送信します。

## アラート通知の購読を解除する {#unsubscribe-from-alert-notifications}

プロジェクト内のクラスターのアラート通知を受信したくない場合は、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定] を**クリックします。</mdsvgicon>
3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「アラート サブスクリプション」**をクリックします。
4.  削除する対象の加入者の行で、 **...**をクリックします。
5.  **「購読解除」**をクリックすると、ポップアップ ウィンドウで購読解除が確定します。
