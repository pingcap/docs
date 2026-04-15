---
title: Connect to TiDB with Navicat
summary: Navicatを使用してTiDBに接続する方法を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-gui-navicat/','/ja/tidb/dev/dev-guide-gui-navicat/','/ja/tidbcloud/dev-guide-gui-navicat/']
---

# Navicatを使用してTiDBに接続する {#connect-to-tidb-with-navicat}

TiDBはMySQL互換データベースであり、[ナビキャット](https://www.navicat.com)データベースユーザー向けのGUIツールセットです。このチュートリアルでは、 [Navicat Premium](https://www.navicat.com/en/products/navicat-premium)ツールを使用してTiDBに接続します。

このチュートリアルでは、Navicatを使用してTiDBに接続する方法を学ぶことができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Navicat Premium](https://www.navicat.com) **17.1.6**以降のバージョン。
-   Navicat Premiumの有料アカウント。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続する {#connect-to-tidb}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`Navicat`に設定されています。
    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  Navicat Premiumを起動し、左上隅の**「接続」**をクリックし、**ベンダーフィルタ**リストから**PingCAP**を選択し、右側のパネルで**TiDBを**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6.  「**新規接続（TiDB）」**ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワード**：手順4で作成したパスワードを入力してください。

    ![Navicat: configure connection general panel for TiDB Cloud Starter](/media/develop/navicat-premium-connection-config-serverless-general.png)

7.  **SSL**タブをクリックし、 **「SSLを使用」** 、 **「認証を使用」** 、 **「CAに対してサーバー証明書を検証する」**のチェックボックスを選択します。次に、 TiDB Cloud接続ダイアログから`CA`ファイルを選択し、 **CA証明書**フィールドに貼り付けます。

    ![Navicat: configure connection SSL panel for TiDB Cloud Starter](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8.  **「接続テスト」**をクリックして、対象のTiDB Cloud StarterまたはEssentialインスタンスへの接続を検証してください。

9.  接続テストが成功すると、 **「接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  **CA証明書をダウンロードするには、「CA証明書**」をクリックしてください。

5.  Navicat Premiumを起動し、左上隅の**「接続」**をクリックし、**ベンダーフィルタ**リストから**PingCAP**を選択し、右側のパネルで**TiDBを**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6.  「**新規接続（TiDB）」**ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**： TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力してください。
    -   **パスワード**： TiDB Cloud Dedicatedクラスタのパスワードを入力してください。

    ![Navicat: configure connection general panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7.  **「SSL」**タブをクリックし、 **「SSLを使用する」** 、 **「認証を使用する**」、 **「CAに対してサーバー証明書を検証する」の**チェックボックスをオンにします。次に、手順4でダウンロードしたCAファイルを**「CA証明書」**フィールドに選択します。

    ![Navicat: configure connection SSL panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8.  TiDB Cloud Dedicatedクラスターへの接続を検証するために、**接続テストを実行します**。

9.  接続テストが成功すると、 **「接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  Navicat Premiumを起動し、左上隅の**「接続」**をクリックし、**ベンダーフィルタ**リストから**PingCAP**を選択し、右側のパネルで**TiDBを**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

2.  「**新規接続（TiDB）」**ダイアログで、以下の接続パラメータを設定します。

    -   **接続名**：この接続に分かりやすい名前を付けてください。
    -   **ホスト**：TiDBセルフマネージドクラスタのIPアドレスまたはドメイン名を入力してください。
    -   **ポート**：TiDBセルフマネージドクラスタのポート番号を入力してください。
    -   **ユーザー名**：TiDBに接続するために使用するユーザー名を入力してください。
    -   **パスワード**：TiDBに接続するために使用するパスワードを入力してください。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3.  **「接続テスト」**をクリックして、TiDBセルフマネージドクラスタへの接続を検証してください。

4.  接続テストが成功すると、 **「接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
