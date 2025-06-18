---
title: Connect to TiDB with MySQL Workbench
summary: MySQL Workbench を使用して TiDB に接続する方法を学習します。
---

# MySQL Workbench で TiDB に接続する {#connect-to-tidb-with-mysql-workbench}

TiDB は MySQL 互換のデータベースであり、 [MySQLワークベンチ](https://www.mysql.com/products/workbench/) MySQL データベース ユーザー向けの GUI ツール セットです。

> **警告：**
>
> -   MySQL WorkbenchはMySQLとの互換性があるため、TiDBに接続できますが、MySQL WorkbenchはTiDBを完全にサポートしているわけではありません。TiDBをMySQLとして扱うため、使用中に問題が発生する可能性があります。
> -   TiDB [VS Code SQLツール](/develop/dev-guide-gui-vscode-sqltools.md)公式にサポートしている他のGUIツール（ [データグリップ](/develop/dev-guide-gui-datagrip.md)など[DBeaver](/develop/dev-guide-gui-dbeaver.md)の使用をお勧めします。TiDBで完全にサポートされているGUIツールの完全なリストについては、 [TiDB でサポートされているサードパーティ ツール](/develop/dev-guide-third-party-support.md#gui)参照してください。

このチュートリアルでは、MySQL Workbench を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [MySQLワークベンチ](https://dev.mysql.com/downloads/workbench/) **8.0.31**以降のバージョン。
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
    -   **Connect With が**`MySQL Workbench`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6.  **[新しい接続のセットアップ**] ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **「キーチェーンに保存...」**または**「ボールトに保存」**をクリックし、 TiDB Cloud Serverless クラスターのパスワードを入力してから、 **「OK」**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Cloud Serverless in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    次の図は接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Cloud Serverless](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7.  **「テスト接続」**をクリックして、 TiDB Cloud Serverless クラスターへの接続を検証します。

8.  接続テストが成功すると、 **「MySQL接続に成功しました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5.  **[新しい接続のセットアップ**] ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **「キーチェーンに保存...」**をクリックし、 TiDB Cloud Dedicated クラスターのパスワードを入力して、 **「OK」**をクリックし、パスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Cloud Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    次の図は接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Cloud Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6.  **「テスト接続」**をクリックして、 TiDB Cloud Dedicated クラスターへの接続を検証します。

7.  接続テストが成功すると、 **「MySQL接続に成功しました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存します。

</div>
<div label="TiDB Self-Managed">

1.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2.  **[新しい接続のセットアップ**] ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB セルフマネージド クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフマネージド クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB に接続するために使用するユーザー名を入力します。
    -   **パスワード**: **「キーチェーンに保存...」**をクリックし、TiDB クラスターへの接続に使用するパスワードを入力し、 **「OK」**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Self-Managed in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    次の図は接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Self-Managed](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3.  **「テスト接続」**をクリックして、TiDB セルフマネージド クラスターへの接続を検証します。

4.  接続テストが成功すると、 **「MySQL接続に成功しました」という**メッセージが表示されます。 **「OK」**をクリックして接続設定を保存します。

</div>
</SimpleTab>

## よくある質問 {#faqs}

### 接続タイムアウト エラー「エラー コード: 2013。クエリ中に MySQLサーバーへの接続が失われました」を処理するにはどうすればよいですか? {#how-to-handle-the-connection-timeout-error-error-code-2013-lost-connection-to-mysql-server-during-query}

このエラーは、クエリ実行時間がタイムアウト制限を超えたことを示します。この問題を解決するには、以下の手順でタイムアウト設定を調整してください。

1.  MySQL Workbench を起動し、 **Workbench の設定**ページに移動します。
2.  **SQLエディタ**&gt; **MySQLセッション**セクションで、「 **DBMS接続読み取りタイムアウト間隔（秒）」**オプションを設定します。これは、MySQL Workbenchがサーバーから切断されるまでのクエリの最大所要時間（秒）を設定します。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

詳細については[MySQL Workbench のよくある質問](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)参照してください。

## 次のステップ {#next-steps}

-   MySQL Workbench の使い方を[MySQL Workbenchのドキュメント](https://dev.mysql.com/doc/workbench/en/)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
