---
title: Connect to TiDB with MySQL Workbench
summary: MySQL Workbenchを使用してTiDBに接続する方法を学びます。MySQL WorkbenchはTiDBを完全にサポートしていませんが、TiDBをMySQLとして扱うことができます。TiDBを正式にサポートする他のGUIツールを使用することをお勧めします。接続方法にはTiDB Serverless、TiDB Dedicated、TiDB Self-Hostedのオプションがあります。接続タイムアウトエラーを処理する方法も学ぶことができます。MySQL Workbenchの詳細な使い方やTiDBアプリケーション開発の最適化プラクティスについても学ぶことができます。
---

# MySQL Workbench を使用して TiDB に接続する {#connect-to-tidb-with-mysql-workbench}

TiDB は MySQL と互換性のあるデータベースであり、 [MySQL ワークベンチ](https://www.mysql.com/products/workbench/)は MySQL データベース ユーザー向けの GUI ツール セットです。

> **警告：**
>
> -   MySQL との互換性により、MySQL Workbench を使用して TiDB に接続できますが、MySQL Workbench は TiDB を完全にはサポートしていません。 TiDB を MySQL として扱うため、使用中に問題が発生する可能性があります。
> -   TiDB を正式にサポートする他の GUI ツール ( [データグリップ](/develop/dev-guide-gui-datagrip.md) 、 [Dビーバー](/develop/dev-guide-gui-dbeaver.md) 、 [VS コード SQL ツール](/develop/dev-guide-gui-vscode-sqltools.md)など) を使用することをお勧めします。 TiDB で完全にサポートされている GUI ツールの完全なリストについては、 [TiDB がサポートするサードパーティ ツール](/develop/dev-guide-third-party-support.md#gui)を参照してください。

このチュートリアルでは、MySQL Workbench を使用して TiDB クラスターに接続する方法を学習できます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストと互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [MySQL ワークベンチ](https://dev.mysql.com/downloads/workbench/) **8.0.31**以降のバージョン。
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
    -   **ブランチは**`main`に設定されます。
    -   **[接続先] は**`MySQL Workbench`に設定されます。
    -   **オペレーティング システムが**環境に一致します。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  MySQL Workbench を起動し、 **MySQL Connections**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

6.  **[新しい接続のセットアップ] ダイアログ**で、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **[キーチェーンに保存 ...]**または**[ボールトに保存]**をクリックし、TiDB サーバーレス クラスターのパスワードを入力し、 **[OK]**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Serverless in keychain](/media/develop/mysql-workbench-store-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Serverless](/media/develop/mysql-workbench-connection-config-serverless-parameters.png)

7.  **「接続のテスト」**をクリックして、TiDB サーバーレスクラスターへの接続を検証します。

8.  接続テストが成功すると、 **「MySQL 接続が成功しました」**というメッセージが表示されます。 **「OK」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可する]**をクリックします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  MySQL Workbench を起動し、 **MySQL Connections**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

5.  **[新しい接続のセットアップ] ダイアログ**で、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB Cloud接続ダイアログから`HOST`パラメータを入力します。
    -   **ポート**: TiDB Cloud接続ダイアログから`PORT`パラメータを入力します。
    -   **ユーザー名**: TiDB Cloud接続ダイアログから`USERNAME`パラメータを入力します。
    -   **パスワード**: **[キーチェーンに保存...]**をクリックし、TiDB 専用クラスターのパスワードを入力し、 **[OK]**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Dedicated in keychain](/media/develop/mysql-workbench-store-dedicated-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Dedicated](/media/develop/mysql-workbench-connection-config-dedicated-parameters.png)

6.  **「接続のテスト」**をクリックして、TiDB 専用クラスターへの接続を検証します。

7.  接続テストが成功すると、 **「MySQL 接続が成功しました」**というメッセージが表示されます。 **「OK」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  MySQL Workbench を起動し、 **MySQL Connections**タイトルの近くにある**+**をクリックします。

    ![MySQL Workbench: add new connection](/media/develop/mysql-workbench-add-new-connection.png)

2.  **[新しい接続のセットアップ] ダイアログ**で、次の接続パラメータを構成します。

    -   **接続名**: この接続に意味のある名前を付けます。
    -   **ホスト名**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名を入力します。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号を入力します。
    -   **ユーザー名**: TiDB への接続に使用するユーザー名を入力します。
    -   **パスワード**: **[キーチェーンに保存...]**をクリックし、TiDB クラスターへの接続に使用するパスワードを入力し、 **[OK]**をクリックしてパスワードを保存します。

        ![MySQL Workbench: store the password of TiDB Self-Hosted in keychain](/media/develop/mysql-workbench-store-self-hosted-password-in-keychain.png)

    次の図は、接続パラメータの例を示しています。

    ![MySQL Workbench: configure connection settings for TiDB Self-Hosted](/media/develop/mysql-workbench-connection-config-self-hosted-parameters.png)

3.  **[接続のテスト]**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

4.  接続テストが成功すると、 **「MySQL 接続が成功しました」**というメッセージが表示されます。 **「OK」**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## よくある質問 {#faqs}

### 接続タイムアウト エラー「エラー コード: 2013。クエリ中に MySQLサーバーへの接続が失われました」を処理する方法は? {#how-to-handle-the-connection-timeout-error-error-code-2013-lost-connection-to-mysql-server-during-query}

このエラーは、クエリの実行時間がタイムアウト制限を超えたことを示します。この問題を解決するには、次の手順でタイムアウト設定を調整します。

1.  MySQL Workbench を起動し、 **Workbench の設定**ページに移動します。
2.  **[SQL エディター]** &gt; **[MySQL セッション]**セクションで、 **DBMS 接続読み取りタイムアウト間隔 (秒単位)**オプションを構成します。これは、MySQL Workbench がサーバーから切断されるまでのクエリにかかる最大時間 (秒単位) を設定します。

    ![MySQL Workbench: adjust timeout option in SQL Editor settings](/media/develop/mysql-workbench-adjust-sqleditor-read-timeout.jpg)

詳細については、 [MySQL Workbench に関するよくある質問](https://dev.mysql.com/doc/workbench/en/workbench-faq.html)を参照してください。

## 次のステップ {#next-steps}

-   MySQL Workbench の詳しい使い方を[MySQL Workbench のドキュメント](https://dev.mysql.com/doc/workbench/en/)から学びましょう。
-   TiDB アプリケーション開発の[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)プラクティスについて[トランザクション](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/tidb-cloud/tidb-cloud-support.md)について質問してください。

</CustomContent>
