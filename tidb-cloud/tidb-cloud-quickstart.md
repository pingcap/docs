---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
---

# TiDB Cloudクイック スタート {#tidb-cloud-quick-start}

*推定完了時間: 20 分*

このチュートリアルでは、 TiDB Cloudを使い始める簡単な方法について説明します。コンテンツには、クラスターの作成方法、クラスターへの接続方法、データのインポート方法、およびクエリの実行方法が含まれています。

## ステップ 1. TiDB クラスターを作成する {#step-1-create-a-tidb-cluster}

無料の[開発者層](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスターまたは[専用ティア](/tidb-cloud/select-cluster-tier.md#dedicated-tier)のいずれかを作成できます。

<SimpleTab>
<div label="Developer Tier">

無料の Developer Tier クラスターを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップします。

    -   Google ユーザーの場合は、Google でサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Google にサインアップ**] をクリックします。メールアドレスとパスワードは Google によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHub ユーザーの場合は、GitHub にサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Sign up with GitHub** ] をクリックします。メールアドレスとパスワードは GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトではプラン選択ページが表示されます。

3.  プラン選択ページで、 **Developer Tier**プランの [ <strong>Get Started for Free</strong> ] をクリックします。

4.  [**クラスタの作成]**ページでは、デフォルトで [<strong>開発者層]</strong>が選択されています。必要に応じてデフォルトのクラスター名を更新し、クラスターを作成するリージョンを選択します。

5.  [**作成]**をクリックします。

    クラスターの作成プロセスが開始され、 **[セキュリティの設定**] ダイアログ ボックスが表示されます。

6.  [**セキュリティ設定**] ダイアログ ボックスで、ルート パスワードと許可された IP アドレスを設定してクラスターに接続し、[<strong>適用</strong>] をクリックします。

    TiDB Cloudクラスターは、約 5 ～ 15 分で作成されます。

</div>

<div label="Dedicated Tier">

Dedicated Tier クラスターを作成するには、次の手順を実行します。

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップします。

    -   Google ユーザーの場合は、Google でサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Google にサインアップ**] をクリックします。メールアドレスとパスワードは Google によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHub ユーザーの場合は、GitHub にサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Sign up with GitHub** ] をクリックします。メールアドレスとパスワードは GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   AWS Marketplace ユーザーは、AWS Marketplace からサインアップすることもできます。これを行うには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントをセットアップします。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

    デフォルトではプラン選択ページが表示されます。

3.  プラン選択ページで、 **Dedicated Tier**プランの [ <strong>Get Full Access Today</strong> ] をクリックします。

4.  [**クラスタの作成]**ページでは、 <strong>Dedicated Tier</strong>がデフォルトで選択されています。必要に応じて既定のクラスター名とポート番号を更新し、クラウド プロバイダーとリージョンを選択して、 [<strong>次へ</strong>] をクリックします。

    > **ノート：**
    >
    > 最初にTiDB Cloud Dedicated Tier の 14 日間無料試用版を取得する場合は、 [TiDB Cloudで概念実証 (PoC) を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。

5.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに対して CIDR が構成されていない場合は、プロジェクトの CIDR を設定し、[**次へ**] をクリックする必要があります。<strong>プロジェクトの CIDR</strong>フィールドが表示されない場合は、このプロジェクトに対して CIDR が既に構成されていることを意味します。

    > **ノート：**
    >
    > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR と競合しないようにしてください。プロジェクトの CIDR は、一度設定すると変更できません。

6.  TiDB、TiKV、および TiFlash (オプション) にそれぞれ[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を構成し、[**次へ**] をクリックします。

7.  ページのクラスター情報と、左下隅の課金情報を確認します。

8.  右下隅にある [**クレジット カードを追加] を**クリックして、アカウントにクレジット カードを追加します。

9.  [**作成]**をクリックします。

    クラスターの作成プロセスが開始され、 **[セキュリティの設定**] ダイアログ ボックスが表示されます。

10. [**セキュリティ設定**] ダイアログ ボックスで、ルート パスワードと許可された IP アドレスを設定してクラスターに接続し、[<strong>適用</strong>] をクリックします。

    TiDB Cloudクラスターは、約 5 ～ 15 分で作成されます。

</div>
</SimpleTab>

## ステップ 2. TiDB クラスターに接続する {#step-2-connect-to-your-tidb-cluster}

1.  [**アクティブなクラスター]**ページに移動します。

2.  新しく作成したクラスターの領域で、右上隅にある [**接続**] をクリックします。接続ダイアログボックスが表示されます。

    > **ヒント：**
    >
    > または、[**アクティブなクラスター**] ページで新しく作成したクラスターの名前をクリックし、右上隅にある [<strong>接続</strong>] をクリックすることもできます。

3.  ダイアログ ボックスの [**ステップ 2: SQL クライアントに接続**する] で、希望する接続方法のタブをクリックし、接続文字列を使用してクラスターに接続します。

    > **ノート：**
    >
    > -   [開発者層のクラスター](/tidb-cloud/select-cluster-tier.md#developer-tier)の場合、クラスターに接続するときに、ユーザー名にクラスターのプレフィックスを含め、名前を引用符で囲む必要があります。詳細については、 [ユーザー名のプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を参照してください。
    > -   TiDB Cloudは MySQL と互換性があるため、任意の MySQL クライアント ツールを使用してクラスターに接続できます。 [mysql — MySQL コマンドライン クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または[mysql — MariaDB の MySQL コマンドライン クライアント](https://mariadb.com/kb/en/mysql-command-line-client/)を使用することをお勧めします。

4.  TiDB クラスターにログインした後、次の SQL ステートメントを使用して接続を検証できます。

    {{< copyable "" >}}

    ```sql
    SELECT TiDB_version();
    ```

    リリース バージョン情報が表示されたら、TiDB クラスターを使用する準備ができています。

## ステップ 3. サンプル データをインポートする {#step-3-import-the-sample-data}

データを簡単にインポートしてサンプル クエリを実行できるように、Capital Bikeshare のサンプル データを提供しています。

1.  [**アクティブなクラスター]**ページに移動します。

2.  新しく作成したクラスターの領域で、右上隅にある [**データのインポート**] をクリックします。 [<strong>データ インポート タスク]</strong>ページが表示されます。

    > **ヒント：**
    >
    > または、[**アクティブなクラスター**] ページで新しく作成したクラスターの名前をクリックし、右上隅にある [<strong>データのインポート</strong>] をクリックすることもできます。

3.  インポート パラメータを入力します。

    <SimpleTab>
     <div label="AWS">

    TiDB クラスターが AWS によってホストされている場合 (Developer Tier はデフォルトで AWS によってホストされています)、次のパラメーターを入力します。

    -   **データ ソースの種類**: `AWS S3` 。
    -   **バケット URL** : サンプル データの URL を入力します。 `s3://tidbcloud-samples/data-ingestion/` .
    -   **データ形式**: <strong>TiDB Dumpling</strong>を選択します。
    -   **資格情報のセットアップ**: Role-ARN に`arn:aws:iam::385595570414:role/import-sample-access`を入力します。
    -   **ターゲットクラスタ**: <strong>[ユーザー名]</strong>および [<strong>パスワード</strong>] フィールドに入力します。
    -   **DB/Tables Filter** : このフィールドは空白のままにします。

    </div>

    <div label="GCP">

    TiDB クラスターが GCP によってホストされている場合は、次のパラメーターを入力します。

    -   **データ ソースの種類**: `Google Cloud Stroage` 。
    -   **バケット URL** : サンプル データの URL を入力します。 `gcs://tidbcloud-samples-us-west1` .
    -   **データ形式**: <strong>TiDB Dumpling</strong>を選択します。
    -   **ターゲットクラスタ**: <strong>[ユーザー名]</strong>および [<strong>パスワード</strong>] フィールドに入力します。
    -   **DB/Tables Filter** : このフィールドは空白のままにします。

    </div>
     </SimpleTab>

4.  [**インポート]**をクリックします。

    データベース リソースの消費に関する警告メッセージが表示されます。新しく作成されたクラスターの場合、警告メッセージは無視できます。

5.  [**確認]**をクリックします。

    TiDB Cloudは、指定されたバケット URL のサンプル データにアクセスできるかどうかの検証を開始します。検証が完了して成功すると、インポート タスクが自動的に開始されます。

データのインポート プロセスには 5 ～ 10 分かかります。データ インポート プログレス バーに**Success**と表示されたら、サンプル データとデータベース スキーマがデータベースに正常にインポートされています。

## ステップ 4. データのクエリ {#step-4-query-data}

データのインポート プロセスが完了したら、ターミナルでいくつかのクエリの実行を開始できます。

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
