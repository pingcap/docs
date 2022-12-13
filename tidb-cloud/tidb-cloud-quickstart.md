---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloudクイック スタート {#tidb-cloud-quick-start}

*推定完了時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始める簡単な方法について説明します。コンテンツには、クラスターを作成する方法、Playground を試す方法、データをロードする方法、およびTiDB Cloudコンソールで SQL ステートメントを実行する方法が含まれています。

## ステップ 1. TiDB クラスターを作成する {#step-1-create-a-tidb-cluster}

TiDB Cloud [サーバーレス層](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta) (ベータ) は、 TiDB Cloudを使い始める最良の方法です。無料の Serverless Tier クラスターを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/free-trial)クリックしてアカウントにサインアップします。

    Google または GitHub ユーザーの場合は、Google または GitHub アカウントでサインアップすることもできます。メールアドレスとパスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトではプラン選択ページが表示されます。

3.  プラン選択ページで、 **Serverless Tier**プランの<strong>[Get Started for Free]</strong>をクリックします。

4.  **[クラスタの作成]**ページでは、<strong>サーバーレス層が</strong>デフォルトで選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択します。

5.  **[作成]**をクリックします。

    TiDB Cloudクラスターは数分で作成されます。

6.  作成が完了したら、クラスターのセキュリティ設定を実行します。

    1.  クラスター領域の右上隅にある**[セキュリティ設定]**をクリックします。
    2.  **[セキュリティ設定]**ダイアログ ボックスで、クラスターに接続するためのルート パスワードを設定し、 <strong>[適用]</strong>をクリックします。 root パスワードを設定しないと、クラスターに接続できません。

## ステップ 2. Playground を試す {#step-2-try-playground}

TiDB Cloudクラスターが作成されたら、 TiDB Cloudにプリロードされたサンプル データを使用して、TiDB の実験をすぐに開始できます。

[**クラスター**](https://tidbcloud.com/console/clusters)ページで**Playground**をクリックして、 TiDB Cloudで即座にクエリを実行します。

## 手順 3. サンプル データを読み込む {#step-3-load-sample-data}

**Plaground**を試した後、サンプル データをTiDB Cloudクラスターにロードできます。データを簡単にインポートしてサンプル クエリを実行できるように、Capital Bikeshare のサンプル データを提供しています。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  新しく作成したクラスターの領域で、右上隅の**[...]**をクリックし、 <strong>[データのインポート]</strong>を選択します。 <strong>[データのインポート]</strong>ページが表示されます。

    > **ヒント：**
    >
    > または、 **[クラスター]**ページで新しく作成したクラスターの名前をクリックし、 <strong>[インポート]</strong>領域で<strong>[データのインポート]</strong>をクリックすることもできます。

3.  インポート パラメータを入力します。

    -   **データ形式**: <strong>SQL ファイル</strong>を選択
    -   **場所**: <strong>AWS</strong>を選択
    -   **バケット URI** : `s3://tidbcloud-samples/data-ingestion/`
    -   **ロールARN** ： `arn:aws:iam::385595570414:role/import-sample-access`

    バケットのリージョンがクラスターと異なる場合は、クロス リージョンのコンプライアンスを確認します。 **[次へ]**をクリックします。

4.  必要に応じてテーブル フィルター ルールを追加します。サンプル データの場合は、この手順を省略できます。 **[次へ]**をクリックします。

5.  **[プレビュー]**ページでインポートするデータを確認し、 <strong>[インポートの開始]</strong>をクリックします。

データのインポート プロセスには数分かかります。データ インポートの進行状況が**Finished**と表示されたら、サンプル データとデータベース スキーマがTiDB Cloudのデータベースに正常にインポートされました。

## ステップ 4. TiDB SQLエディター (ベータ) を試す {#step-4-try-tidb-sql-editor-beta}

クラスターにデータをロードした後、コンソールから直接 SQL ステートメントを実行してみることができます。

1.  左側のナビゲーション バーで**[SQL エディター]**をクリックします。 SQL エディタ ページが表示されます。

    SQL エディターでは、ターミナルを使用せずにクラスターに対して直接 SQL クエリを編集および実行できます。

    > **ノート：**
    >
    > SQL エディタは現在、SQL ステートメントのサポートが制限されています。 `CREATE TABLE`や`DROP TABLE`などの DDL はまだサポートされていません。

2.  エディターで、次の SQL ステートメントを入力します。

    ```sql
    SHOW databases;
    ```

    クエリを実行するには、 **Ctrl + Enter キー**を押すか、 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg><strong>実行します</strong>。ページの下部に、クエリ ログと結果がすぐに表示されます。

3.  `bikeshare`データベースのテーブルを表示するには、次の SQL ステートメントを入力します。

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

    2 つのクエリを順番に実行するには、次のいずれかを実行できます。

    -   **Control + Shift + Enter**を押します。
    -   カーソルで 2 つのクエリを選択し、 **[実行]**をクリックします。

    クエリ ログ パネルでは、2 つのクエリが 1 つずつ実行されていることがわかります。

    エディターに 2 つ以上のクエリがある場合、 **Ctrl + Enter を**押すか、 <strong>[実行] を</strong>クリックすると、エディターで強調表示されているクエリのみが実行されます。

4.  `trip`テーブルの構造を表示し、テーブルに含まれるレコード数をカウントするには、エディターで次の 2 つの SQL ステートメントを実行します。

    ```sql
    DESCRIBE trips;
    SELECT COUNT(*) FROM trips;
    ```

これで、 TiDB Cloudを使用してアプリケーションを構築する準備が整いました。

## 次は何ですか {#what-s-next}

-   SQL クライアント経由でクラスターに接続する方法については、 [TiDBクラスタに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。
-   TiDB SQL の使用方法の詳細については、 [TiDB で SQL を調べる](/basic-sql-operations.md)を参照してください。
-   クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番環境での使用については、 [TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照して Dedicated Tier クラスターを作成してください。
