---
title: Connect to TiDB with JetBrains DataGrip
summary: JetBrains DataGrip を使用して TiDB に接続する方法を学びます。このチュートリアルは、IntelliJ、PhpStorm、PyCharm などの他の JetBrains IDE で利用可能なデータベース ツールと SQL プラグインにも適用されます。
---

# JetBrains DataGrip で TiDB に接続する {#connect-to-tidb-with-jetbrains-datagrip}

TiDB は MySQL 互換のデータベースであり、 [ジェットブレインズ データグリップ](https://www.jetbrains.com/help/datagrip/getting-started.html)データベースと SQL 用の強力な統合開発環境 (IDE) です。このチュートリアルでは、DataGrip を使用して TiDB クラスターに接続するプロセスについて説明します。

> **注記：**
>
> このチュートリアルは、TiDB Serverless、TiDB Dedicated、および TiDB Self-Hosted と互換性があります。

DataGrip は次の 2 つの方法で使用できます。

-   [データグリップIDE](https://www.jetbrains.com/datagrip/download)スタンドアロン ツールとして。
-   IntelliJ、PhpStorm、PyCharm などの JetBrains IDE の[データベースツールとSQLプラグイン](https://www.jetbrains.com/help/idea/relational-databases.html)として。

このチュートリアルでは、主にスタンドアロンの DataGrip IDE に焦点を当てています。JetBrains IDE の JetBrains データベース ツールと SQL プラグインを使用して TiDB に接続する手順は同様です。また、任意の JetBrains IDE から TiDB に接続する場合は、このドキュメントの手順を参考にすることもできます。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [DataGrip **2023.2.1**以降](https://www.jetbrains.com/datagrip/download/)または非コミュニティ エディション[ジェットブレインズ](https://www.jetbrains.com/) IDE。
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

    -   **エンドポイントタイプは**`Public`に設定されています
    -   **ブランチ**は`main`に設定されています
    -   **接続先は**`DataGrip`に設定されています
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

6.  新しく作成したプロジェクトで、**データベース エクスプローラー**パネルの左上隅にある**+**をクリックし、**データ ソース**&gt;**その他**&gt; **TiDB**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

7.  TiDB Cloud接続ダイアログから接続文字列をコピーします。次に、それを**URL**フィールドに貼り付けると、残りのパラメータが自動的に入力されます。結果の例は次のとおりです。

    ![Configure the URL field for TiDB Serverless](/media/develop/datagrip-url-paste.jpg)

    **「不足しているドライバー ファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

8.  **「テスト接続」**をクリックして、TiDB Serverless クラスターへの接続を検証します。

    ![Test the connection to a TiDB Serverless clustser](/media/develop/datagrip-test-connection.jpg)

9.  **[OK]**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **「どこからでもアクセスを許可」**をクリックし、 **「CA 証明書のダウンロード」**をクリックして CA 証明書をダウンロードします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

5.  新しく作成したプロジェクトで、**データベース エクスプローラー**パネルの左上隅にある**+**をクリックし、**データ ソース**&gt;**その他**&gt; **TiDB**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

6.  適切な接続文字列をコピーして、DataGrip の**[データ ソースとドライバー]**ウィンドウに貼り付けます。DataGrip フィールドと TiDB 専用接続文字列間のマッピングは次のとおりです。

    | DataGrip フィールド | TiDB専用接続文字列  |
    | -------------- | ------------ |
    | ホスト            | `{host}`     |
    | ポート            | `{port}`     |
    | ユーザー           | `{user}`     |
    | パスワード          | `{password}` |

    例は以下のとおりです。

    ![Configure the connection parameters for TiDB Dedicated](/media/develop/datagrip-dedicated-connect.jpg)

7.  **SSH/SSL**タブをクリックし、 **SSL を使用する**チェックボックスをオンにして、 **CA ファイル**フィールドに CA 証明書のパスを入力します。

    ![Configure the CA for TiDB Dedicated](/media/develop/datagrip-dedicated-ssl.jpg)

    **「不足しているドライバー ファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

8.  **[詳細設定]**タブをクリックし、スクロールして**enabledTLSProtocols**パラメータを見つけ、その値を`TLSv1.2,TLSv1.3`に設定します。

    ![Configure the TLS for TiDB Dedicated](/media/develop/datagrip-dedicated-advanced.jpg)

9.  **「テスト接続」**をクリックして、TiDB 専用クラスターへの接続を検証します。

    ![Test the connection to a TiDB Dedicated cluster](/media/develop/datagrip-dedicated-test-connection.jpg)

10. **[OK]**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  DataGrip を起動し、接続を管理するためのプロジェクトを作成します。

    ![Create a project in DataGrip](/media/develop/datagrip-create-project.jpg)

2.  新しく作成したプロジェクトで、**データベース エクスプローラー**パネルの左上隅にある**+**をクリックし、**データ ソース**&gt;**その他**&gt; **TiDB**を選択します。

    ![Select a data source in DataGrip](/media/develop/datagrip-data-source-select.jpg)

3.  次の接続パラメータを構成します。

    -   **ホスト**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号。
    -   **ユーザー**: TiDB セルフホスト クラスターに接続するために使用するユーザー名。
    -   **パスワード**: ユーザー名のパスワード。

    例は以下のとおりです。

    ![Configure the connection parameters for TiDB Self-Hosted](/media/develop/datagrip-self-hosted-connect.jpg)

    **「不足しているドライバー ファイルをダウンロードしてください」**という警告が表示された場合は、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

4.  **「テスト接続」**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

    ![Test the connection to a TiDB Self-Hosted cluster](/media/develop/datagrip-self-hosted-test-connection.jpg)

5.  **[OK]**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   [DataGripのドキュメント](https://www.jetbrains.com/help/datagrip/getting-started.html)から DataGrip の使い方を詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
