---
title: Connect to TiDB with MySQL Workbench
summary: MySQL Workbench を使用して TiDB に接続する方法を学習します。
---

# MySQL Workbench で TiDB に接続する {#connect-to-tidb-with-mysql-workbench}

TiDB は MySQL 互換データベースであり、 [MySQL ワークベンチ](https://www.mysql.com/products/workbench/) MySQL データベース ユーザー向けの GUI ツール セットです。

> **警告：**
>
> -   MySQL との互換性があるため、MySQL Workbench を使用して TiDB に接続できますが、MySQL Workbench は TiDB を完全にはサポートしていません。TiDB を MySQL として扱うため、使用中に問題が発生する可能性があります。
> -   [データグリップ](/develop/dev-guide-gui-datagrip.md) 、 [DBeaver](/develop/dev-guide-gui-dbeaver.md) 、 [VS コード SQL ツール](/develop/dev-guide-gui-vscode-sqltools.md)など、TiDB を公式にサポートする他の GUI ツールを使用することをお勧めします。TiDB で完全にサポートされている GUI ツールの完全なリストについては、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md#gui)を参照してください。

このチュートリアルでは、MySQL Workbench を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、TiDB Serverless、TiDB Dedicated、および TiDB Self-Hosted と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [MySQL ワークベンチ](https://dev.mysql.com/downloads/workbench/) **8.0.31**以降のバージョン。
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
    -   **Connect With は**`MySQL Workbench`に設定されています。
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6.  **[新しい接続のセットアップ]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **「キーチェーンに保存...」**または**「ボールトに保存」を**クリックし、TiDB Serverless クラスターのパスワードを入力してから、 **「OK」**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Serverless in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Serverless](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7.  **「テスト接続」**をクリックして、TiDB Serverless クラスターへの接続を検証します。

8.  接続テストが成功すると、 **「MySQL 接続に成功しました」という**メッセージが表示されます。 **[OK]**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可] を**クリックします。

    接続文字列を取得する方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5.  **[新しい接続のセットアップ]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **「キーチェーンに保存...」**をクリックし、TiDB 専用クラスターのパスワードを入力して、 **「OK」**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6.  **「テスト接続」**をクリックして、TiDB 専用クラスターへの接続を検証します。

7.  接続テストが成功すると、 **「MySQL 接続に成功しました」という**メッセージが表示されます。 **[OK]**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  MySQL Workbench を起動し、 **MySQL 接続**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2.  **[新しい接続のセットアップ]**ダイアログで、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB に接続するために使用するユーザー名を入力します。
    -   **パスワード**: **「キーチェーンに保存...」**をクリックし、TiDB クラスターへの接続に使用するパスワードを入力して、 **「OK」**をクリックし、パスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Self-Hosted in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Self-Hosted](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3.  **「テスト接続」**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

4.  接続テストが成功すると、 **「MySQL 接続に成功しました」という**メッセージが表示されます。 **[OK]**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## よくある質問 {#faqs}

### 接続タイムアウト エラー「エラー コード: 2013。クエリ中に MySQLサーバーへの接続が失われました」を処理するにはどうすればよいですか? {#how-to-handle-the-connection-timeout-error-error-code-2013-lost-connection-to-mysql-server-during-query}

このエラーは、クエリの実行時間がタイムアウト制限を超えたことを示します。この問題を解決するには、次の手順でタイムアウト設定を調整します。

1.  MySQL Workbench を起動し、 **Workbench の設定**ページに移動します。
2.  **SQL エディタ**&gt; **MySQL セッション**セクションで、 **DBMS 接続読み取りタイムアウト間隔 (秒単位)**オプションを設定します。これにより、MySQL Workbench がサーバーから切断されるまでのクエリの最大時間 (秒単位) が設定されます。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

詳細については[MySQL Workbench よくある質問](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)参照してください。

## 次のステップ {#next-steps}

-   MySQL Workbench の使い方を[MySQL Workbenchのドキュメント](https://dev.mysql.com/doc/workbench/en/)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/tidb-cloud/tidb-cloud-support.md)について質問します。

</CustomContent>
