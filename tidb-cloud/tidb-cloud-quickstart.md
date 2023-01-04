---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloudクイック スタート {#tidb-cloud-quick-start}

*推定完了時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始める簡単な方法について説明します。このコンテンツには、クラスターを作成する方法、プレイグラウンドを試す方法、データをロードする方法、およびクラスターに接続する方法が含まれています。

## ステップ 1. TiDB クラスターを作成する {#step-1-create-a-tidb-cluster}

TiDB Cloud [サーバーレス層](/tidb-cloud/select-cluster-tier.md#serverless-tier)は、 TiDB Cloudを使い始めるための最良の方法です。無料の Serverless Tier クラスターを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップします。

    Google または GitHub ユーザーの場合は、Google または GitHub アカウントでサインアップすることもできます。メールアドレスとパスワードは Google または GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトではプラン選択ページが表示されます。

3.  プラン選択ページで、 **Serverless Tier**プランの [ <strong>Get Started for Free</strong> ] をクリックします。

4.  [**クラスタの作成**] ページでは、<strong>サーバーレス層</strong>がデフォルトで選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択します。

5.  [**作成]**をクリックします。

    TiDB Cloudクラスターは数分で作成されます。

6.  作成プロセス中に、クラスターのセキュリティ設定を実行します。

    1.  クラスター領域の右上隅にある [**セキュリティ設定]**をクリックします。
    2.  [**セキュリティ設定**] ダイアログ ボックスで、クラスターに接続するためのルート パスワードを設定し、 [<strong>適用</strong>] をクリックします。 root パスワードを設定しないと、クラスターに接続できません。

## ステップ 2. Playground を試す {#step-2-try-playground}

TiDB Cloudクラスターが作成されたら、TiDB TiDB Cloudにプリロードされたサンプル データを使用して、TiDB の実験をすぐに開始できます。

[**クラスター**] ページで [<strong>プレイグラウンド</strong>] をクリックして、 TiDB Cloudでクエリを即座に実行します。

## 手順 3. サンプル データを読み込む {#step-3-load-sample-data}

**Plaground**を試した後、サンプル データをTiDB Cloudクラスターにロードできます。データを簡単にインポートしてサンプル クエリを実行できるように、Capital Bikeshare のサンプル データを提供しています。

1.  [**クラスター]**ページに移動します。

2.  新しく作成したクラスターの領域で、右上隅の [ **...** ] をクリックし、[<strong>データのインポート</strong>] を選択します。 [<strong>データのインポート]</strong>ページが表示されます。

    > **ヒント：**
    >
    > または、[**クラスター**] ページで新しく作成したクラスターの名前をクリックし、[インポート] 領域で [<strong>データ</strong>の<strong>インポート</strong>] をクリックすることもできます。

3.  インポート パラメータを入力します。

    -   **データ形式**: <strong>SQL ファイル</strong>を選択
    -   **場所**: `AWS`
    -   **バケット URI** : `s3://tidbcloud-samples/data-ingestion/`
    -   **ロールARN** ： `arn:aws:iam::385595570414:role/import-sample-access`

    バケットのリージョンがクラスターと異なる場合は、クロス リージョンのコンプライアンスを確認します。 [**次へ**] をクリックします。

4.  必要に応じてテーブル フィルター ルールを追加します。サンプル データの場合は、この手順を省略できます。 [**次へ**] をクリックします。

5.  [**プレビュー**] ページでインポートするデータを確認し、[<strong>インポートの開始</strong>] をクリックします。

データのインポート プロセスには数分かかります。データ インポートの進行状況が**Finished**と表示されたら、サンプル データとデータベース スキーマがTiDB Cloudのデータベースに正常にインポートされました。

## ステップ 4. TiDB クラスターに接続する {#step-4-connect-to-your-tidb-cluster}

クラスターにデータをロードしたら、コマンドラインまたはプログラミング言語からクラスターに接続できます。

1.  [**クラスター]**ページに移動します。

2.  新しく作成したクラスターの領域で、右上隅にある [**接続**] をクリックします。接続ダイアログが表示されます。

3.  ダイアログの指示に従って、TiDB クラスターに接続します。

    1.  接続用のトラフィック フィルターを作成します。

    2.  SQL クライアントを使用してクラスターに接続します。希望する接続方法のタブをクリックし、接続文字列を使用してクラスターに接続します。

    > **ヒント：**
    >
    > TiDB Cloudは MySQL と互換性があるため、任意の MySQL クライアント ツールを使用してクラスターに接続できます。 [mysql — MySQL コマンドライン クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または[mysql — MariaDB の MySQL コマンドライン クライアント](https://mariadb.com/kb/en/mysql-command-line-client/)を使用することをお勧めします。

4.  TiDB クラスターにログインした後、次の SQL ステートメントを使用して接続を検証できます。

    {{< copyable "" >}}

    ```sql
    SELECT TiDB_version();
    ```

    リリース バージョン情報が表示されたら、TiDB クラスターを使用する準備ができています。

## ステップ 4. データのクエリ {#step-4-query-data}

TiDB クラスターに接続したら、ターミナルでいくつかのクエリを実行できます。

1.  `bikeshare`のデータベースとテーブルを使用します。

    {{< copyable "" >}}

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

2.  `trip`テーブルの構造を確認します。

    {{< copyable "" >}}

    ```sql
    DESCRIBE trips;
    ```

3.  `trips`のテーブルにいくつのレコードが存在するかを確認します。

    {{< copyable "" >}}

    ```sql
    SELECT COUNT(*) FROM trips;
    ```

4.  出発駅が「8th &amp; D St NW」であるすべての旅行履歴を確認します。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM trips WHERE start_station_name = '8th & D St NW';
    ```

5.  受け取りに人気の自転車ステーションを 10 個以上表示する:

    {{< copyable "" >}}

    ```sql
    SELECT start_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name
    ORDER BY count ASC
    LIMIT 10;
    ```

TiDB SQLの使用法の詳細については、 [TiDB で SQL を調べる](/basic-sql-operations.md)を参照してください。

クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた本番環境での使用については、 [TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してDedicated Tierクラスターを作成してください。
