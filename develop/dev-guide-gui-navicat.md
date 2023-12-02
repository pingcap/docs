---
title: Connect to TiDB with Navicat
summary: Learn how to connect to TiDB using Navicat.
---

# Navicat を使用して TiDB に接続する {#connect-to-tidb-with-navicat}

TiDB は MySQL と互換性のあるデータベースであり、 [ナビキャット](https://www.navicat.com)はデータベース ユーザー向けの GUI ツール セットです。このチュートリアルでは、 [MySQL 用 Navicat](https://www.navicat.com/en/products/navicat-for-mysql)ツールを使用して TiDB に接続します。

> **警告：**
>
> -   Navicat は MySQL と互換性があるため、Navicat を使用して TiDB に接続できますが、Navicat は TiDB を完全にはサポートしません。 TiDB を MySQL として扱うため、使用中に問題が発生する可能性があります。 [Navicat ユーザー管理の互換性](https://github.com/pingcap/tidb/issues/45154)に関する既知の問題があります。 Navicat と TiDB の間の互換性の問題の詳細については、「 [TiDB GitHub の問題ページ](https://github.com/pingcap/tidb/issues?q=is%3Aissue+navicat+is%3Aopen)を参照してください。
> -   TiDB を正式にサポートする他の GUI ツール ( [データグリップ](/develop/dev-guide-gui-datagrip.md) 、 [Dビーバー](/develop/dev-guide-gui-dbeaver.md) 、 [VS コード SQL ツール](/develop/dev-guide-gui-vscode-sqltools.md)など) を使用することをお勧めします。 TiDB で完全にサポートされている GUI ツールの完全なリストについては、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md#gui)を参照してください。

このチュートリアルでは、Navicat を使用して TiDB クラスターに接続する方法を学習できます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストと互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [MySQL 用 Navicat](https://www.navicat.com/en/download/navicat-for-mysql) **16.3.2**以降のバージョン。
-   Navicat for MySQL の有料アカウント。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## TiDB に接続する {#connect-to-tidb}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。
    -   **[接続先] は**`General`に設定されます。
    -   **オペレーティング システムが**環境に一致します。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  Navicat for MySQL を起動し、左上隅の**[接続]**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`user`パラメータを入力します。
    -   **パスワード**: TiDB サーバーレスクラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-general.png)

7.  **[SSL]**タブをクリックし、 **[SSL を使用する]** 、 **[認証を使用する**] 、および**[CA に対してサーバー証明書を検証する**] チェックボックスを選択します。次に、 TiDB Cloud接続ダイアログから**CA 証明書**フィールドに`ssl_ca`ファイルを選択します。

    ![Navicat: configure connection SSL panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-ssl.png)

8.  **「接続のテスト」**をクリックして、TiDB サーバーレスクラスターへの接続を検証します。

9.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を終了します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可する]**をクリックします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  **[CA 証明書のダウンロード]**をクリックして CA ファイルをダウンロードします。

5.  Navicat for MySQL を起動し、左上隅の**[接続]**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`host`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`port`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`user`パラメータを入力します。
    -   **パスワード**: TiDB 専用クラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-general.png)

7.  **[SSL]**タブをクリックし、 **[SSL を使用する]** 、 **[認証を使用する**] 、および**[CA に対してサーバー証明書を検証する**] チェックボックスを選択します。次に、手順 4 でダウンロードした CA ファイルを**[CA 証明書]**フィールドに選択します。

    ![Navicat: configure connection SSL panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-ssl.jpg)

8.  **接続をテストして、** TiDB 専用クラスターへの接続を検証します。

9.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を終了します。

</div>
<div label="TiDB Self-Hosted">

1.  Navicat for MySQL を起動し、左上隅の**[接続]**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

2.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB への接続に使用するユーザー名を入力します。
    -   **パスワード**: TiDB への接続に使用するパスワードを入力します。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-connection-config-self-hosted-general.png)

3.  **[接続のテスト]**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

4.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を終了します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   TiDB アプリケーション開発の[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/tidb-cloud/tidb-cloud-support.md)について質問してください。

</CustomContent>
