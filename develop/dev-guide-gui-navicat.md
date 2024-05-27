---
title: Connect to TiDB with Navicat
summary: Navicat を使用して TiDB に接続する方法を学習します。
---

# NavicatでTiDBに接続する {#connect-to-tidb-with-navicat}

TiDB は MySQL 互換のデータベースで、 [ナビキャット](https://www.navicat.com)データベース ユーザー向けの GUI ツール セットです。このチュートリアルでは、 [MySQL 用 Navicat](https://www.navicat.com/en/products/navicat-for-mysql)ツールを使用して TiDB に接続します。

> **警告：**
>
> -   Navicat は MySQL と互換性があるため、TiDB に接続するために使用できますが、Navicat は TiDB を完全にサポートしていません。TiDB を MySQL として扱うため、使用中に問題が発生する可能性があります[Navicat ユーザー管理の互換性](https://github.com/pingcap/tidb/issues/45154)に関する既知の問題があります。Navicat と TiDB 間の互換性に関するその他の問題については、 [TiDB GitHub 問題ページ](https://github.com/pingcap/tidb/issues?q=is%3Aissue+navicat+is%3Aopen)を参照してください。
> -   [データグリップ](/develop/dev-guide-gui-datagrip.md) 、 [DBeaver](/develop/dev-guide-gui-dbeaver.md) 、 [VS コード SQL ツール](/develop/dev-guide-gui-vscode-sqltools.md)など、TiDB を公式にサポートする他の GUI ツールを使用することをお勧めします。TiDB で完全にサポートされている GUI ツールの完全なリストについては、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md#gui)を参照してください。

このチュートリアルでは、Navicat を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、TiDB Serverless、TiDB Dedicated、および TiDB Self-Hosted と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [MySQL 用 Navicat](https://www.navicat.com/en/download/navicat-for-mysql) **16.3.2**以降のバージョン。
-   Navicat for MySQL の有料アカウント。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレス クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレス クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## TiDBに接続する {#connect-to-tidb}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **エンドポイント タイプは**`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`Navicat`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  Navicat for MySQL を起動し、左上隅の**「接続」**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを設定します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: TiDB Serverless クラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-general.png)

7.  **[SSL]**タブをクリックし、 **[SSL の使用]** 、 **[認証の使用**]、 **[CA に対するサーバー証明書の検証]**チェックボックスをオンにします。次に、 TiDB Cloud接続ダイアログから`CA`ファイルを選択し、 **[CA 証明書]**フィールドに入力します。

    ![Navicat: configure connection SSL panel for TiDB Serverless](/media/develop/navicat-connection-config-serverless-ssl.png)

8.  **「テスト接続」**をクリックして、TiDB Serverless クラスターへの接続を検証します。

9.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を完了します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可] を**クリックします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  CA ファイルをダウンロードするには、 **「CA 証明書のダウンロード」を**クリックします。

5.  Navicat for MySQL を起動し、左上隅の**「接続」**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

6.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを設定します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: TiDB 専用クラスターのパスワードを入力します。

    ![Navicat: configure connection general panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-general.png)

7.  **[SSL]**タブをクリックし、 **[SSL の使用]** 、 **[認証の使用**]、 **[CA に対するサーバー証明書の検証]**チェックボックスをオンにします。次に、手順 4 でダウンロードした CA ファイルを**[CA 証明書]**フィールドに選択します。

    ![Navicat: configure connection SSL panel for TiDB Dedicated](/media/develop/navicat-connection-config-dedicated-ssl.jpg)

8.  TiDB 専用クラスターへの接続を検証するための**テスト接続**。

9.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を完了します。

</div>
<div label="TiDB Self-Hosted">

1.  Navicat for MySQL を起動し、左上隅の**「接続」**をクリックして、ドロップダウン リストから**MySQL**を選択します。

    ![Navicat: add new connection](/media/develop/navicat-add-new-connection.jpg)

2.  **[新しい接続 (MySQL)]**ダイアログで、次の接続パラメータを設定します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB に接続するために使用するユーザー名を入力します。
    -   **パスワード**: TiDB に接続するために使用するパスワードを入力します。

    ![Navicat: configure connection general panel for self-hosted TiDB](/media/develop/navicat-connection-config-self-hosted-general.png)

3.  **「テスト接続」**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

4.  接続テストが成功すると、 **「接続成功」**メッセージが表示されます。 **「保存」**をクリックして接続構成を完了します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/tidb-cloud/tidb-cloud-support.md)について質問します。

</CustomContent>
