---
title: Connect to TiDB with DBeaver
summary: Learn how to connect to TiDB using DBeaver Community.
---

# DBeaverでTiDBに接続する {#connect-to-tidb-with-dbeaver}

TiDB は MySQL 互換のデータベースであり、開発者、データベース管理者、アナリスト、およびデータを扱うすべての人にとって無料のクロスプラットフォーム データベース[DBeaver コミュニティ](https://dbeaver.io/download/)です。

このチュートリアルでは、DBeaver Community を使用して TiDB クラスターに接続する方法を学習します。

> **注記：**
>
> このチュートリアルは、TiDB Serverless、TiDB Dedicated、および TiDB Self-Hosted と互換性があります。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [DBeaver コミュニティ**23.0.3**以上](https://dbeaver.io/download/) 。
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
    -   **接続先は**`DBeaver`に設定されています
    -   **オペレーティング システムは**環境に適合します。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  DBeaver を起動し、左上隅にある**[新しいデータベース接続]**をクリックします。 **[データベースへの接続**] ダイアログで、リストから**[TiDB]**を選択し、 **[次へ]**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

6.  TiDB Cloud接続ダイアログから接続文字列をコピーします。DBeaver で、 **[接続方法]**に**[URL]**を選択し、接続文字列を**[URL]**フィールドに貼り付けます。

7.  **認証 (データベース ネイティブ)**セクションで、**ユーザー名**と**パスワード**を入力します。例は次のとおりです。

    ![Configure connection settings for TiDB Serverless](/media/develop/dbeaver-connection-settings-serverless.jpg)

8.  **「テスト接続」**をクリックして、TiDB Serverless クラスターへの接続を検証します。

    **「ドライバー ファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のように**接続テスト**ダイアログが表示されます。 **[OK]**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

9.  **「完了」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[どこからでもアクセスを許可] を**クリックし、 **[CA 証明書のダウンロード]**をクリックして CA 証明書をダウンロードします。

    接続文字列を取得する方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  DBeaver を起動し、左上隅にある**[新しいデータベース接続]**をクリックします。 **[データベースへの接続**] ダイアログで、リストから**[TiDB]**を選択し、 **[次へ]**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

5.  適切な接続文字列をコピーして DBeaver 接続パネルに貼り付けます。DBeaver フィールドと TiDB 専用接続文字列間のマッピングは次のとおりです。

    | DBeaverフィールド | TiDB専用接続文字列  |
    | ------------ | ------------ |
    | サーバーホスト      | `{host}`     |
    | ポート          | `{port}`     |
    | ユーザー名        | `{user}`     |
    | パスワード        | `{password}` |

    例は以下のとおりです。

    ![Configure connection settings for TiDB Dedicated](/media/develop/dbeaver-connection-settings-dedicated.jpg)

6.  **「テスト接続」**をクリックして、TiDB 専用クラスターへの接続を検証します。

    **「ドライバー ファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のように**接続テスト**ダイアログが表示されます。 **[OK]**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

7.  **「完了」**をクリックして接続構成を保存します。

</div>
<div label="TiDB Self-Hosted">

1.  DBeaver を起動し、左上隅にある**[新しいデータベース接続]**をクリックします。 **[データベースへの接続**] ダイアログで、リストから**TiDB**を選択し、 **[次へ]**をクリックします。

    ![Select TiDB as the database in DBeaver](/media/develop/dbeaver-select-database.jpg)

2.  次の接続パラメータを構成します。

    -   **サーバー ホスト**: TiDB セルフホスト クラスターの IP アドレスまたはドメイン名。
    -   **ポート**: TiDB セルフホスト クラスターのポート番号。
    -   **ユーザー名**: TiDB セルフホスト クラスターに接続するために使用するユーザー名。
    -   **パスワード**: ユーザー名のパスワード。

    例は以下のとおりです。

    ![Configure connection settings for TiDB Self-Hosted](/media/develop/dbeaver-connection-settings-self-hosted.jpg)

3.  **「テスト接続」**をクリックして、TiDB セルフホスト クラスターへの接続を検証します。

    **「ドライバー ファイルのダウンロード」**ダイアログが表示されたら、 **「ダウンロード」**をクリックしてドライバー ファイルを取得します。

    ![Download driver files](/media/develop/dbeaver-download-driver.jpg)

    接続テストが成功すると、次のように**接続テスト**ダイアログが表示されます。 **[OK]**をクリックして閉じます。

    ![Connection test result](/media/develop/dbeaver-connection-test.jpg)

4.  **「完了」**をクリックして接続構成を保存します。

</div>
</SimpleTab>

## 次のステップ {#next-steps}

-   [DBeaverのドキュメント](https://github.com/dbeaver/dbeaver/wiki)から DBeaver の詳しい使い方を学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
