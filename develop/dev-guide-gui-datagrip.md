---
title: Connect to TiDB with JetBrains DataGrip
summary: Learn how to connect to TiDB using JetBrains DataGrip. This tutorial also applies to the Database Tools and SQL plugin available in other JetBrains IDEs, such as IntelliJ, PhpStorm, and PyCharm.
---

# JetBrains DataGrip を使用して TiDB に接続する {#connect-to-tidb-with-jetbrains-datagrip}

TiDB は MySQL と互換性のあるデータベースであり、データベースと SQL のための強力な統合開発環境 ( [JetBrains データグリップ](https://www.jetbrains.com/help/datagrip/getting-started.html) ) です。このチュートリアルでは、DataGrip を使用して TiDB クラスターに接続するプロセスを説明します。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストと互換性があります。

DataGrip は 2 つの方法で使用できます。

-   [データグリップIDE](https://www.jetbrains.com/datagrip/download)スタンドアロン ツールとして。
-   IntelliJ、PhpStorm、PyCharm などの JetBrains IDE の[データベースツールとSQLプラグイン](https://www.jetbrains.com/help/idea/relational-databases.html)として。

このチュートリアルでは主にスタンドアロンの DataGrip IDE に焦点を当てます。 JetBrains データベース ツールと JetBrains IDE の SQL プラグインを使用して TiDB に接続する手順は似ています。 JetBrains IDE から TiDB に接続する場合は、参考としてこのドキュメントの手順に従うこともできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [DataGrip **2023.2.1**以降](https://www.jetbrains.com/datagrip/download/)または非コミュニティ エディション[ジェットブレインズ](https://www.jetbrains.com/) IDE。
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

    -   **エンドポイント タイプは**`Public`に設定されます
    -   **[接続先] は**`JDBC`に設定されています
    -   **オペレーティング システムが**環境に一致します。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6.  新しく作成したプロジェクトで、 **[データベース エクスプローラー]**パネルの左上隅にある**[+]**をクリックし、 **[データ ソース]** &gt; **[その他]** &gt; **[TiDB]**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7.  TiDB Cloud接続ダイアログから JDBC 文字列をコピーし、 `<your_password>`実際のパスワードに置き換えます。次に、それを**URL**フィールドに貼り付けると、残りのパラメータが自動入力されます。結果の例は次のとおりです。

    ![Configure the URL field for TiDB Serverless](/media/develop/datagrip-url-paste.jpg)

    **「不足しているドライバー ファイルをダウンロードする」**という警告が表示された場合は、 **「ダウンロード」を**クリックしてドライバー ファイルを取得します。

8.  **「接続のテスト」**をクリックして、TiDB サーバーレスクラスターへの接続を検証します。

    ![Test the connection to a TiDB Serverless clustser](/media/develop/datagrip-test-connection.jpg)

9.  **「OK」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **「どこからでもアクセスを許可」**をクリックし、 **「TiDB クラスター CA のダウンロード」**をクリックして CA 証明書をダウンロードします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

5.  新しく作成したプロジェクトで、 **[データベース エクスプローラー]**パネルの左上隅にある**[+]**をクリックし、 **[データ ソース]** &gt; **[その他]** &gt; **[TiDB]**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

6.  適切な接続文字列をコピーして、DataGrip の**[データ ソースとドライバー]**ウィンドウに貼り付けます。 DataGrip フィールドと TiDB 専用接続文字列間のマッピングは次のとおりです。

    | データグリップフィールド | TiDB 専用接続文字列 |
    | ------------ | ------------ |
    | ホスト          | `{host}`     |
    | ポート          | `{port}`     |
    | ユーザー         | `{user}`     |
    | パスワード        | `{password}` |

    例は次のとおりです。

    ![Configure the connection parameters for TiDB Dedicated](/media/develop/datagrip-dedicated-connect.jpg)

7.  **[SSH/SSL]**タブをクリックし、 **[SSL を使用]**チェックボックスを選択して、CA 証明書のパスを**[CA ファイル]**フィールドに入力します。

    ![Configure the CA for TiDB Dedicated](/media/develop/datagrip-dedicated-ssl.jpg)

    **「不足しているドライバー ファイルをダウンロードする」**という警告が表示された場合は、 **「ダウンロード」を**クリックしてドライバー ファイルを取得します。

8.  **「詳細」**タブをクリックし、スクロールして**「enabledTLSProtocols」**パラメータを見つけ、その値を`TLSv1.2,TLSv1.3`に設定します。

    ![Configure the TLS for TiDB Dedicated](/media/develop/datagrip-dedicated-advanced.jpg)

9.  **「接続のテスト」**をクリックして、TiDB 専用クラスターへの接続を検証します。

    ![Test the connection to a TiDB Dedicated cluster](/media/develop/datagrip-dedicated-test-connection.jpg)

10. **「OK」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

2.  新しく作成したプロジェクトで、 **[データベース エクスプローラー]**パネルの左上隅にある**[+]**をクリックし、 **[データ ソース]** &gt; **[その他]** &gt; **[TiDB]**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

3.  次の接続パラメータを構成します。

    -   **ホスト**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名。
    -   **Port** : TiDB セルフホスト クラスターのポート番号。
    -   **User** : TiDB セルフホスト クラスターへの接続に使用するユーザー名。
    -   **パスワード**: ユーザー名のパスワード。

    例は次のとおりです。

    ![Configure the connection parameters for TiDB Self-Hosted](/media/develop/datagrip-self-hosted-connect.jpg)

    **「不足しているドライバー ファイルをダウンロードする」**という警告が表示された場合は、 **「ダウンロード」を**クリックしてドライバー ファイルを取得します。

4.  **[接続のテスト]**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

    ![Test the connection to a TiDB Self-Hosted cluster](/media/develop/datagrip-self-hosted-test-connection.jpg)

5.  **「OK」**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   DataGrip の詳しい使い方を[DataGrip のドキュメント](https://www.jetbrains.com/help/datagrip/getting-started.html)から学びましょう。
-   TiDB アプリケーション開発[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>
