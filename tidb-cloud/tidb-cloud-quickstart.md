---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDB Cloudクイックスタート {#tidb-cloud-quick-start}

*推定完了時間：20分*

このチュートリアルでは、 TiDB Cloudを簡単に使い始める方法について説明します。コンテンツには、クラスタの作成方法、クラスタへの接続方法、データのインポート方法、およびクエリの実行方法が含まれます。

## 手順1.TiDBクラスタを作成する {#step-1-create-a-tidb-cluster}

無料の[開発者層（開発層）](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスタまたは[専用層](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターを作成できます。

<SimpleTab>
<div label="Developer Tier">

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/free-trial)をクリックしてアカウントにサインアップしてください。

    -   Googleユーザーの場合、Googleにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **Googleにサインアップ**]をクリックします。メールアドレスとパスワードはGoogleによって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHubユーザーの場合は、GitHubにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **GitHubにサインアップ**]をクリックします。メールアドレスとパスワードはGitHubによって管理され、 TiDB Cloudコンソールを使用して変更することはできません。

2.  TiDB Cloudアカウントに[ログイン](https://tidbcloud.com/) 。

    プラン選択ページはデフォルトで表示されます。

3.  プランの選択ページで、**開発者層**プランの[<strong>無料で開始</strong>]をクリックします。

4.  [**クラスターの作成（開発層）]**ページで、必要に応じてデフォルトのクラスタ名を更新してから、クラスタを作成するリージョンを選択します。

5.  [**作成]**をクリックします。

    クラスタ作成プロセスが開始され、[**セキュリティクイックスタート**]ダイアログボックスが表示されます。

6.  [**セキュリティクイックスタート**]ダイアログボックスで、ルートパスワードと許可されたIPアドレスをクラスタに接続するように設定し、[<strong>適用</strong>]をクリックします。

    TiDB Cloudクラスタは約5〜15分で作成されます。

</div>

<div label="Dedicated Tier">

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

    -   Googleユーザーの場合、Googleにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **Googleにサインアップ**]をクリックします。メールアドレスとパスワードはGoogleによって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHubユーザーの場合は、GitHubにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **GitHubにサインアップ**]をクリックします。メールアドレスとパスワードはGitHubによって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   AWS Marketplaceユーザーの場合、AWSMarketplaceからサインアップすることもできます。これを行うには、 [AWSマーケットプレイス](https://aws.amazon.com/marketplace)分の`TiDB Cloud`を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントを設定します。

2.  TiDB Cloudアカウントに[ログイン](https://tidbcloud.com/) 。

    プラン選択ページはデフォルトで表示されます。

3.  プランの選択ページで、**専用階層**プランの[<strong>今すぐフルアクセスを取得</strong>]をクリックします。

    > **ノート：**
    >
    > 最初にTiDB Cloud Tierの14日間の無料試用版を入手したい場合は、 [TiDB Cloudで概念実証（PoC）を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。

4.  [**クラスターの作成**]ページで、必要に応じてデフォルトのクラスタ名とポート番号を更新し、クラウドプロバイダーとリージョンを選択して、[<strong>次へ</strong>]をクリックします。

5.  これが現在のプロジェクトの最初のクラスタであり、このプロジェクトに対してCIDRが構成されていない場合は、プロジェクトCIDRを設定してから、[**次へ**]をクリックする必要があります。<strong>プロジェクトのCIDR</strong>フィールドが表示されない場合は、CIDRがこのプロジェクト用に既に構成されていることを意味します。

    > **ノート：**
    >
    > プロジェクトCIDRを設定するときは、アプリケーションが配置されているVPCのCIDRとの競合を回避してください。プロジェクトのCIDRは、一度設定すると変更できません。

6.  TiDB、TiKV、およびTiFlash<sup>ベータ</sup>（オプション）にそれぞれ[クラスタサイズ](/tidb-cloud/size-your-cluster.md)を構成し、[**次へ**]をクリックします。

7.  中央の領域でクラスタ情報を確認し、右側のペインで請求情報も確認します。

8.  アカウントのクレジットカードを追加するには、右ペインの[**クレジットカードの追加]を**クリックします。

9.  [**作成]**をクリックします。

    クラスタ作成プロセスが開始され、[**セキュリティクイックスタート**]ダイアログボックスが表示されます。

10. [**セキュリティクイックスタート**]ダイアログボックスで、ルートパスワードと許可されたIPアドレスをクラスタに接続するように設定し、[<strong>適用</strong>]をクリックします。

    TiDB Cloudクラスタは約5〜15分で作成されます。

</div>
</SimpleTab>

## ステップ2.TiDBクラスタに接続します {#step-2-connect-to-your-tidb-cluster}

1.  [**アクティブクラスター**]ページで、新しく作成したクラスタの名前をクリックします。

    新しく作成したクラスタの概要ページが表示されます。

2.  [**接続]**をクリックします。 [ <strong>TiDBに接続</strong>]ダイアログボックスが表示されます。

3.  [**ステップ2：ダイアログボックスのSQLクライアントに接続**する]で、希望する接続方法のタブをクリックし、接続文字列を使用してクラスタに接続します。

    > **ヒント：**
    >
    > TiDB CloudはMySQLと互換性があるため、任意のMySQLクライアントツールを使用してクラスタに接続できます。 [mysql —MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または[mysql —MariaDBのMySQLコマンドラインクライアント](https://mariadb.com/kb/en/mysql-command-line-client/)の使用をお勧めします。

4.  TiDBクラスタにログインした後、次のSQLステートメントを使用して接続を検証できます。

    {{< copyable "" >}}

    ```sql
    SELECT TiDB_version();
    ```

    リリースバージョン情報が表示されたら、TiDBクラスタを使用する準備ができています。

## ステップ3.サンプルデータをインポートします {#step-3-import-the-sample-data}

Capital Bikeshareのサンプルデータを提供しているため、データを簡単にインポートしてサンプルクエリを実行できます。

1.  [**アクティブクラスター**]ページに移動し、新しく作成したクラスタの名前をクリックします。クラスタの概要ページが表示されます。

2.  左側のクラスタ情報ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。

3.  インポートパラメータを入力します。

    <SimpleTab>
     <div label="AWS">

    TiDBクラスタがAWSによってホストされている場合（デフォルトでは開発層はAWSによってホストされています）、次のパラメーターを入力します。

    -   **データソースタイプ**： `AWS S3` 。
    -   **バケットURL** ：サンプルデータ`s3://tidbcloud-samples/data-ingestion/`を入力します。
    -   **データ形式**： <strong>TiDBDumpling</strong>を選択します。
    -   **クレデンシャルの設定**：Role-ARNに`arn:aws:iam::385595570414:role/import-sample-access`を入力します。
    -   **ターゲットデータベース**：
        -   **ユーザー名**： `root` 。
        -   **パスワード**：rootパスワードを入力します。
    -   **DB /テーブルフィルター**：このフィールドは空白のままにします。

    </div>

    <div label="GCP">

    TiDBクラスタがGCPでホストされている場合は、次のパラメーターを入力します。

    -   **データソースタイプ**： `Google Cloud Stroage` 。
    -   **バケットURL** ：サンプルデータ`gcs://tidbcloud-samples-us-west1`を入力します。
    -   **データ形式**： <strong>TiDBDumpling</strong>を選択します。
    -   **ターゲットデータベース**：
        -   **ユーザー名**： `root` 。
        -   **パスワード**：rootパスワードを入力します。
    -   **DB /テーブルフィルター**：このフィールドは空白のままにします。

    </div>
     </SimpleTab>

4.  [**インポート]**をクリックします。

    データのインポートプロセスには5〜10分かかります。データインポートの進行状況バーに[**成功]**と表示されたら、サンプルデータとデータベーススキーマをデータベースに正常にインポートできます。

## ステップ4.データを照会する {#step-4-query-data}

データのインポートプロセスが完了すると、ターミナルでいくつかのクエリの実行を開始できます。

1.  `bikeshare`のデータベースとテーブルを使用します。

    {{< copyable "" >}}

    ```sql
    USE bikeshare;
    SHOW tables;
    ```

2.  `trip`のテーブルの構造を確認してください。

    {{< copyable "" >}}

    ```sql
    DESCRIBE trips;
    ```

3.  `trips`のテーブルにレコードがいくつ存在するかを確認します。

    {{< copyable "" >}}

    ```sql
    SELECT COUNT(*) FROM trips;
    ```

4.  スタートステーションが「8th＆D St NW」である、旅行履歴全体を確認します。

    {{< copyable "" >}}

    ```sql
    SELECT * FROM trips WHERE start_station_name = '8th & D St NW';
    ```

5.  ピックアップするのに最も人気のない自転車ステーションを10個表示します。

    {{< copyable "" >}}

    ```sql
    SELECT start_station_name, COUNT(ride_id) as count from `trips`
    GROUP BY start_station_name
    ORDER BY count ASC
    LIMIT 10;
    ```
