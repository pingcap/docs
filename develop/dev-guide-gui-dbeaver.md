---
title: Connect to TiDB with DBeaver
summary: DBeaver Community を使用して TiDB に接続する方法を学習します。
---

# DBeaverでTiDBに接続する {#connect-to-tidb-with-dbeaver}

[DBeaverコミュニティ](https://dbeaver.io/download/)は MySQL 互換のデータベースであり、開発者、データベース管理者、アナリスト、およびデータを扱うすべての人にとって無料のクロスプラットフォーム データベース ツールです。

このチュートリアルでは、DBeaver Community を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [DBeaver コミュニティ**23.0.3**以上](https://dbeaver.io/download/) 。
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

    -   **接続タイプ**は`Public`に設定されています
    -   **ブランチ**は`main`に設定されています
    -   **接続先が**`DBeaver`に設定されています
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続」**ダイアログで、リストから**「TiDB」を**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

6.  TiDB Cloud接続ダイアログから接続文字列をコピーします。DBeaverで「**接続方法」**に**「URL」**を選択し、接続文字列を**URL**フィールドに貼り付けます。

7.  **「認証（データベースネイティブ）」**セクションで、**ユーザー名**と**パスワード**を入力します。例を以下に示します。

    ![Configure connection settings for TiDB Cloud Serverless](/media/develop/dbeaver-connection-settings-serverless.jpg)

8.  **「テスト接続」**をクリックして、 TiDB Cloud Serverless クラスターへの接続を検証します。

    **ドライバー ファイルのダウンロード**ダイアログが表示された場合は、 **[ダウンロード]**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のような**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

9.  **「完了」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続」**ダイアログで、リストから**「TiDB」を**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

5.  適切な接続文字列をコピーして、DBeaver 接続パネルに貼り付けます。DBeaver フィールドとTiDB Cloud Dedicated 接続文字列のマッピングは次のとおりです。

    | DBeaverフィールド | TiDB Cloud専用接続文字列 |
    | ------------ | ----------------- |
    | サーバーホスト      | `{host}`          |
    | ポート          | `{port}`          |
    | ユーザー名        | `{user}`          |
    | パスワード        | `{password}`      |

    次に例を示します。

    ![Configure connection settings for TiDB Cloud Dedicated](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6.  **「テスト接続」**をクリックして、 TiDB Cloud Dedicated クラスターへの接続を検証します。

    **ドライバー ファイルのダウンロード**ダイアログが表示された場合は、 **[ダウンロード]**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のような**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

7.  **「完了」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Managed">

1.  DBeaverを起動し、左上隅の**「新しいデータベース接続」**をクリックします。 **「データベースへの接続」**ダイアログで、リストから**「TiDB」を**選択し、 **「次へ」**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

2.  次の接続パラメータを構成します。

    -   **サーバー ホスト**: TiDB セルフマネージド クラスターの IP アドレスまたはドメイン名。
    -   **ポート**: TiDB セルフマネージド クラスターのポート番号。
    -   **ユーザー名**: TiDB セルフマネージド クラスターに接続するために使用するユーザー名。
    -   **パスワード**: ユーザー名のパスワード。

    次に例を示します。

    ![Configure connection settings for TiDB Self-Managed](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3.  **「テスト接続」**をクリックして、TiDB セルフマネージド クラスターへの接続を検証します。

    **ドライバー ファイルのダウンロード**ダイアログが表示された場合は、 **[ダウンロード]**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のような**接続テスト**ダイアログが表示されます。 **「OK」**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

4.  **「完了」**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   DBeaver の使い方を[DBeaverのドキュメント](https://github.com/dbeaver/dbeaver/wiki)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
