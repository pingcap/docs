---
title: Connect to TiDB with Navicat
summary: Navicat を使用して TiDB に接続する方法を学びます。
---

# NavicatでTiDBに接続する {#connect-to-tidb-with-navicat}

TiDBはMySQL互換データベースで、 [ナビキャット](https://www.navicat.com)データベースユーザー向けのGUIツールセットです。このチュートリアルでは、 [ナビキャット プレミアム](https://www.navicat.com/en/products/navicat-premium)ツールを使用してTiDBに接続します。

このチュートリアルでは、Navicat を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [ナビキャット プレミアム](https://www.navicat.com) **17.1.6**以降のバージョン。
-   Navicat Premium の有料アカウント。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## TiDBに接続する {#connect-to-tidb}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With が**`Navicat`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  Navicat Premium を起動し、左上隅の**「接続」**をクリックし、**ベンダー フィルター**リストから**PingCAP**を選択して、右側のパネルで**TiDB を**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6.  [**新しい接続 (TiDB)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: TiDB Cloud Serverless クラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Cloud Serverless](/media/develop/navicat-premium-connection-config-serverless-general.png)

7.  **「SSL」**タブをクリックし、 **「SSLを使用する」** 、 **「認証を使用する**」、 **「CA証明サーバーを検証する」の**チェックボックスをオンにします。次に、 TiDB Cloud接続ダイアログから`CA`ファイルを選択し、 **「CA証明書」**フィールドに入力します。

    ![Navicat: configure connection SSL panel for TiDB Cloud Serverless](/media/develop/navicat-premium-connection-config-serverless-ssl.png)

8.  **「テスト接続」**をクリックして、 TiDB Cloud Serverless クラスターへの接続を検証します。

9.  接続テストが成功すると、「**接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択します。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  **CA 証明書をダウンロードするには、CA 証明**書をクリックします。

5.  Navicat Premium を起動し、左上隅の**「接続」**をクリックし、**ベンダー フィルター**リストから**PingCAP**を選択して、右側のパネルで**TiDB を**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

6.  [**新しい接続 (TiDB)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: TiDB Cloud Dedicated クラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-general.png)

7.  **「SSL」**タブをクリックし、 **「SSLを使用する」** 、 **「認証を使用する**」、 **「CAサーバー書を検証する」の**チェックボックスをオンにします。次に、 **「CA証明書」**フィールドで、手順4でダウンロードしたCAファイルを選択します。

    ![Navicat: configure connection SSL panel for TiDB Cloud Dedicated](/media/develop/navicat-premium-connection-config-dedicated-ssl.png)

8.  TiDB Cloud Dedicated クラスターへの接続を検証するための**テスト接続**。

9.  接続テストが成功すると、「**接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
<div label="TiDB Self-Managed">

1.  Navicat Premium を起動し、左上隅の**「接続」**をクリックし、**ベンダー フィルター**リストから**PingCAP**を選択して、右側のパネルで**TiDB を**ダブルクリックします。

    ![Navicat: add new connection](/media/develop/navicat-premium-add-new-connection.png)

2.  [**新しい接続 (TiDB)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB セルフマネージド クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフマネージド クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB に接続するために使用するユーザー名を入力します。
    -   **パスワード**: TiDB に接続するために使用するパスワードを入力します。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-premium-connection-config-self-hosted-general.png)

3.  **「テスト接続」**をクリックして、TiDB セルフマネージド クラスターへの接続を検証します。

4.  接続テストが成功すると、「**接続成功」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を完了してください。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
