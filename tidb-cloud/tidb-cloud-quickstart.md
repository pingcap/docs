---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
aliases: ['/tidbcloud/beta/tidb-cloud-quickstart']
---

# TiDBクラウドクイックスタート {#tidb-cloud-quick-start}

*推定完了時間：20分*

このチュートリアルでは、TiDBクラウドを簡単に使い始める方法について説明します。コンテンツには、クラスタの作成方法、クラスタへの接続方法、データのインポート方法、およびクエリの実行方法が含まれます。

## 手順1.TiDBクラスタを作成する {#step-1-create-a-tidb-cluster}

無料の[開発者層（開発層）](/tidb-cloud/select-cluster-tier.md#developer-tier)クラスタまたは[専用層](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスターを作成できます。

<SimpleTab>
<div label="Developer Tier">

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

    -   Googleユーザーの場合、Googleにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **Googleにサインアップ**]をクリックします。メールアドレスとパスワードはGoogleによって管理され、TiDBクラウドコンソールを使用して変更することはできません。
    -   GitHubユーザーの場合は、GitHubにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **GitHubにサインアップ**]をクリックします。メールアドレスとパスワードはGitHubによって管理され、TiDBクラウドコンソールを使用して変更することはできません。

2.  TiDBCloudアカウントに[ログイン](https://tidbcloud.com/) 。

    デフォルトでは、プラン選択ページが表示されます。

3.  プランの選択ページで、**開発者層**プランの[<strong>無料で開始</strong>]をクリックします。

4.  [**クラスターの作成（開発層）]**ページで、クラスタ名とルートパスワードを設定します。

5.  開発者層のクラウドプロバイダーはAWSであることに注意してください。次に、クラスタを作成するリージョンを選択します。

6.  開発者層のクラスタサイズを表示し、[**作成**]をクリックします。

TiDB Cloudクラスタは、約5〜15分で作成されます。

</div>

<div label="Dedicated Tier">

1.  TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

    -   Googleユーザーの場合、Googleにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **Googleにサインアップ**]をクリックします。メールアドレスとパスワードはGoogleによって管理され、TiDBクラウドコンソールを使用して変更することはできません。
    -   GitHubユーザーの場合は、GitHubにサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページの[ **GitHubにサインアップ**]をクリックします。メールアドレスとパスワードはGitHubによって管理され、TiDBクラウドコンソールを使用して変更することはできません。
    -   AWS Marketplaceユーザーの場合、AWSMarketplaceからサインアップすることもできます。これを行うには、 [AWSマーケットプレイス](https://aws.amazon.com/marketplace)分の`TiDB Cloud`を検索し、TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDBCloudアカウントを設定します。

2.  TiDBCloudアカウントに[ログイン](https://tidbcloud.com/) 。

    デフォルトでは、プラン選択ページが表示されます。

3.  プランの選択ページで、**オンデマンド**プランの[<strong>今すぐフルアクセスを取得</strong>]をクリックします。

    > **ノート：**
    >
    > 最初にTiDBCloudの14日間の無料トライアルを取得する場合は**、概念実証**プランの[ <strong>PoCトライアルの申請</strong>]をクリックし、申請フォームに記入して、[ <strong>OK</strong> ]をクリックします。 PingCAPサポートチームは48時間以内にご連絡いたします。詳細については、 [TiDB Cloudで概念実証（PoC）を実行する](/tidb-cloud/tidb-cloud-poc.md)を参照してください。

4.  [クラスターの**作成]**ページで、クラスタ名とルートパスワードを設定し、接続に`4000`を使用できない場合は、デフォルトのポート番号`4000`を更新します。

5.  クラウドプロバイダーとリージョンを選択し、[**次へ**]をクリックします。

6.  これが現在のプロジェクトの最初のクラスタであり、このプロジェクトに対してCIDRが構成されていない場合は、プロジェクトCIDRを設定してから、[**次へ**]をクリックする必要があります。<strong>プロジェクトのCIDR</strong>フィールドが表示されない場合は、CIDRがこのプロジェクト用に既に構成されていることを意味します。

    > **ノート：**
    >
    > プロジェクトCIDRを設定するときは、アプリケーションが配置されているVPCのCIDRとの競合を回避してください。プロジェクトのCIDRは、一度設定すると変更できません。

7.  TiDB、TiKV、およびTiFlash<sup>ベータ</sup>（オプション）にそれぞれ[クラスタサイズ](/tidb-cloud/size-your-cluster.md)を構成し、[**次へ**]をクリックします。

8.  中央の領域でクラスタ情報を確認し、右側のペインで請求情報も確認します。

9.  アカウントのクレジットカードを追加するには、右ペインの[**クレジットカードの追加]を**クリックします。

10. [**作成]**をクリックします。

TiDB Cloudクラスタは、約5〜15分で作成されます。

</div>
</SimpleTab>

## ステップ2.TiDBクラスタに接続します {#step-2-connect-to-your-tidb-cluster}

1.  [TiDBクラスター]ページに移動し、新しく作成したクラスタの名前をクリックします。

    新しく作成したクラスタの概要ページが表示されます。

2.  [**接続]**をクリックします。 [ <strong>TiDBに接続</strong>]ダイアログボックスが表示されます。

3.  **手順1：トラフィックフィルターの作成**で、[<strong>現在のIPアドレスの追加</strong>]をクリックし、[<strong>フィルターの作成</strong>]をクリックします。

    この手順の目的は、トラフィックフィルターを設定することです。これにより、クラスタが信頼できるIPアドレスからの接続のみを受け入れるようになります。

4.  **手順2：** SQLクライアントに接続するで、SQLクライアントを使用してクラスタに接続します。

    TiDB CloudはMySQLと互換性があるため、任意のMySQLクライアントツールを使用してクラスタに接続できます。 [mysql —MySQLコマンドラインクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または[mysql —MariaDBのMySQLコマンドラインクライアント](https://mariadb.com/kb/en/mysql-command-line-client/)の使用をお勧めします。

5.  [ **TiDBに接続**]ダイアログボックスで、[<strong>手順2：SQLクライアントに接続</strong>する]で提供されているコマンドをコピーして、ターミナルインターフェイスに貼り付けます。

    コマンドラインの形式は次のとおりですが、エンドポイントをカスタマイズする必要があります。

    {{< copyable "" >}}

    ```shell
    mysql -u root -h <endpoint> -P <port number> -p
    ```

6.  クラスタの作成時に使用したrootパスワードを入力します。

7.  MySQLクライアントで接続を検証します。

    {{< copyable "" >}}

    ```sql
    SELECT TiDB_version();
    ```

    リリースバージョン情報が表示されたら、TiDBクラウドクラスタでMySQLクライアントを試す準備ができています。

## ステップ3.サンプルデータをインポートします {#step-3-import-the-sample-data}

Capital Bikeshareのサンプルデータを提供しているため、データを簡単にインポートしてサンプルクエリを実行できます。

1.  [TiDBクラスター]ページに移動し、新しく作成したクラスタの名前をクリックします。クラスタの概要ページが表示されます。

2.  左側のクラスタ情報ペインで、[**インポート**]をクリックします。 [<strong>データインポートタスク]</strong>ページが表示されます。

3.  TiDBクラスタがホストされている場所に応じて、次のいずれかを実行します。

    -   TiDBクラスタがAWSによってホストされている場合（デフォルトでは開発層はAWSによってホストされています）、データソースタイプとして**AWS S3**を選択し、サンプルデータのバケットURLを入力して、バケットリージョンを選択します。

        **バケットのURLとリージョンは、ターゲットデータベースのリージョンに対応している必要があります。**たとえば、US-West-2（オレゴン）でクラスタを作成する場合は、次のリストからUS-West-2（オレゴン）のバケット領域のサンプルデータURLを選択する必要があります。

        -   US-West-2（オレゴン）： `s3://tidbcloud-samples-us-west-2/data-ingestion/`
        -   US-East-1（バージニア）： `s3://tidbcloud-samples-us-east-1/data-ingestion/`
        -   AP-北東-1（東京）： `s3://tidbcloud-samples-ap-northeast-1/data-ingestion/`
        -   AP-南東1（シンガポール）： `s3://tidbcloud-samples-ap-southeast-1/data-ingestion/`

    -   TiDBクラスタがGCPでホストされている場合は、[**データソースの種類**]に[ <strong>Google Cloud Storage</strong> ]を選択し、[<strong>バケットURL</strong> ]フィールドにサンプルデータのURL `gcs://tidbcloud-samples-us-west1`を入力して、[<strong>バケットリージョン</strong>]に[ <strong>US-West1（オレゴン）]</strong>を選択します。サンプルデータバケットは、GCPのUS-West1（オレゴン）でホストされています。

4.  他のインポートパラメータを入力します。

    -   データ形式： **TiDBDumpling**を選択します。
    -   クレデンシャルの設定：Role-ARNに`arn:aws:iam::385595570414:role/import-sample-access`を入力します。
    -   ターゲットデータベース：
        -   ユーザー名： `root` 。
        -   パスワード：rootパスワードを入力します。
    -   DB /テーブルフィルター：このフィールドは空白のままにします。

5.  [**インポート]**をクリックします。

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
