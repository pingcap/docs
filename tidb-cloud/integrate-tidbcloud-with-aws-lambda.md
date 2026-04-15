---
title: Integrate TiDB Cloud Starter with Amazon Lambda Using AWS CloudFormation
summary: TiDB Cloud StarterをAmazon LambdaおよびCloudFormationと統合する方法を、手順を追って説明します。
---

# AWS CloudFormationを使用してTiDB Cloud StarterをAmazon Lambdaと統合する {#integrate-tidb-cloud-starter-with-amazon-lambda-using-aws-cloudformation}

このドキュメントでは、 [AWS CloudFormation](https://aws.amazon.com/cloudformation/)使用して、クラウドネイティブな分散 SQL データベースである[TiDB Cloud Starter](https://www.pingcap.com/tidb-cloud-starter/)と、サーバーレスでイベント駆動型のコンピューティング サービスである[AWS Lambda](https://aws.amazon.com/lambda/)を統合する手順を段階的に説明します。TiDB TiDB Cloud Starter をAmazon Lambda と統合することで、 TiDB Cloud Starterと AWS Lambda を通じてマイクロサービスの拡張性とコスト効率を活用できます。AWS CloudFormation は、Lambda関数、API Gateway、Secrets Manager などの AWS リソースの作成と管理を自動化します。

> **注記：**
>
> このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。

## ソリューションの概要 {#solution-overview}

このガイドでは、以下のコンポーネントを使用して、完全に機能するオンライン書店を作成します。

-   AWS Lambda関数：Sequelize ORMとFastify APIフレームワークを使用して、TiDB Cloud Starterインスタンスからのリクエストとクエリデータを処理します。
-   AWS Secrets Manager SDK: TiDB Cloud Starterインスタンスの接続構成を取得および管理します。
-   AWS API Gateway：HTTPリクエストのルーティングを処理します。
-   TiDB Cloud Starter：クラウドネイティブな分散型SQLデータベース。

AWS CloudFormationは、Secrets Manager、API Gateway、Lambda関数など、プロジェクトに必要なリソースを作成するために使用されます。

書店プロジェクトの構成は以下のとおりです。

![AWS Lambda structure overview](/media/develop/aws-lambda-structure-overview.png)

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   以下のAWSサービスにアクセスできるAWSアカウント：
    -   [AWS CloudFormation](https://aws.amazon.com/cloudformation/)
    -   [シークレットマネージャー](https://aws.amazon.com/secrets-manager/)
    -   [APIゲートウェイ](https://aws.amazon.com/api-gateway/)
    -   [Lambdaサービス](https://aws.amazon.com/lambda/)
    -   [S3](https://aws.amazon.com/s3/)
    -   [IAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)

-   [TiDB Cloud](https://tidbcloud.com)アカウントとTiDB Cloud Starterインスタンスが必要です。TiDB TiDB Cloud Starterインスタンスの接続情報を取得するには、以下の手順に従ってください。

    ![TiDB Cloud connection information](/media/develop/aws-lambda-tidbcloud-connection-info.png)

-   [郵便配達人](https://www.postman.com/)や[カール](https://curl.se/)などのAPIテストツール。このドキュメントのほとんどの例では cURL を使用します。 Windows ユーザーには Postman をお勧めします。

-   プロジェクトの[最新リリースのアセット](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest)ローカル マシンにダウンロードします。これには、 `cloudformation_template.yml`および`cloudformation_template.json`ファイルが含まれます。

> **注記：**
>
> -   AWS リソースを作成する際は、リージョンとして`us-east-1`を使用することをお勧めします。これは、このデモの Lambda 関数コードでリージョンが`us-east-1`とハードコーディングされており、コードバンドルが`us-east-1`リージョンに保存されるためです。
> -   別のリージョンを使用する場合は、以下の手順に従ってLambda関数のコードを変更し、再構築して、コードバンドルを独自のS3バケットにアップロードする必要があります。

<details><summary><code>us-east-1</code>以外のリージョンを使用する場合は、Lambda関数のコードを修正して再構築してください。</summary>

リージョンとして`us-east-1`を使用する場合は、このセクションをスキップして、 [ステップ1：AWS CloudFormationを使用してプロジェクトをセットアップする](#step-1-set-up-the-bookshop-project-using-aws-cloudformation)進みます。

AWS リソースを作成する際に`us-east-1`以外の別の AWS リージョンを使用する場合は、Lambda 関数のコードを変更し、再構築して、コード バンドルを独自の S3 バケットにアップロードする必要があります。

ローカル開発環境の問題を回避するため、 [Gitpod](https://www.gitpod.io/)などのクラウドネイティブ開発環境を使用することをお勧めします。

コードバンドルを再構築して独自のS3バケットにアップロードするには、次の手順を実行します。

1.  開発環境を初期化します。

    -   [Gitpod](https://gitpod.io/#/https://github.com/pingcap/TiDB-Lambda-integration)ワークスペースを開き、GitHubアカウントでログインしてください。

2.  ラムダ関数のコードを修正してください。

    1.  左側のサイドバーで`aws-lambda-cloudformation/src/secretManager.ts`ファイルを開きます。
    2.  22行目を見つけて、 `region`変数を自分の地域に合わせて変更してください。

3.  コードバンドルを再構築してください。

    1.  依存関係をインストールしてください。

        1.  Gitpodでターミナルを開きます。

        2.  作業ディレクトリを入力してください：

            ```shell
            cd aws-lambda-cloudformation
            ```

        3.  依存関係をインストールします。

            ```shell
            yarn
            ```

    2.  コードバンドルを再構築してください。

        1.  コードバンドルを作成します。

            ```shell
            yarn build
            ```

        2.  `aws-lambda-cloudformation/dist/index.zip`ファイルを確認してください。

        3.  `index.zip`ファイルを右クリックして、 **[ダウンロード]**を選択します。

4.  再構築したコードバンドルを、ご自身のS3バケットにアップロードしてください。

    1.  AWS マネジメントコンソールの[S3サービス](https://console.aws.amazon.com/s3)にアクセスします。
    2.  選択したリージョンに新しいバケットを作成します。
    3.  `index.zip`ファイルをバケットにアップロードします。
    4.  後で使用するため、S3バケット名とリージョンをメモしておいてください。

</details>

## ステップ1. AWS CloudFormationを使用して書店プロジェクトをセットアップします。 {#step-1-set-up-the-bookshop-project-using-aws-cloudformation}

AWS CloudFormation を使用して書店プロジェクトを設定するには、次の手順を実行します。

1.  AWS マネジメントコンソールに移動し、 [AWS CloudFormationサービス](https://console.aws.amazon.com/cloudformation)にアクセスします。
2.  **[スタックの作成]** &gt; **[新しいリソースを使用 (標準)]**をクリックします。
3.  「**スタックの作成」**ページで、スタックの作成プロセスを完了します。

    1.  **前提条件の**領域で、 **「既存のテンプレートを選択」**を選択します。

    2.  **テンプレート指定**領域で、 **[テンプレート ファイルをアップロード]**を選択し、 **[ファイルを選択]**をクリックしてテンプレート ファイル (YAML または JSON) をアップロードし、 **[次へ]**をクリックします。

        まだファイルをお持ちでない場合は、 [GitHub](https://github.com/pingcap/TiDB-Lambda-integration/releases/latest)からダウンロードしてください。このファイルには、プロジェクトに必要なリソースを作成するAWS CloudFormationテンプレートが含まれています。

        ![Create a stack](/media/develop/aws-lambda-cf-create-stack.png)

    3.  スタックの詳細を指定してください。

        -   地域として`us-east-1`を使用する場合は、次のスクリーンショットのようにフィールドに入力してください。

            ![Specify AWS Lambda stack details](/media/develop/aws-lambda-cf-stack-config.png)

            -   **スタック名**：スタック名を入力してください。
            -   **S3Bucket** ：zipファイルを保存しているS3バケットを入力してください。
            -   **S3Key** ：S3キーを入力してください。
            -   **TiDBDatabase** ： TiDB Cloud Starterインスタンス名を入力してください。
            -   **TiDBHost** : TiDB Cloudデータベースにアクセスするためのホスト URL を入力してください。 `localhost`を入力してください。
            -   **TiDBPassword** ： TiDB Cloudデータベースへのアクセスに使用するパスワードを入力してください。
            -   **TiDBPort** ： TiDB Cloudデータベースへのアクセスに使用するポート番号を入力してください。
            -   **TiDBUser** ： TiDB Cloudデータベースにアクセスするためのユーザー名を入力してください。

        -   `us-east-1`以外のAWSリージョンを使用する場合は、以下の手順に従ってください。

            1.  Lambda 関数のコードを変更して再構築し、 [`us-east-1`以外のリージョンを使用する場合は、Lambda関数のコードを修正して再構築してください。](#prerequisites)参照してください。
            2.  スタックの詳細フィールドでは、 `S3Bucket`および`S3Key`パラメーターに、ご自身の設定に応じて S3 バケット名とリージョンを指定してください。
            3.  前のスクリーンショットのように、他の項目も入力してください。

    4.  スタックオプションを設定してください。デフォルト設定を使用することもできます。

        ![Configure stack options](/media/develop/aws-lambda-cf-stack-config-option.png)

    5.  スタックを確認し、作成します。

        ![Review and create the stack](/media/develop/aws-lambda-cf-stack-config-review.png)

## ステップ2. 書店プロジェクトを使用する {#step-2-use-the-bookshop-project}

スタックが作成されたら、プロジェクトは次のように使用できます。

1.  AWS マネジメント コンソールで[APIゲートウェイサービス](https://console.aws.amazon.com/apigateway)サービスにアクセスし、 `TiDBCloudApiGatewayV2` API をクリックし、左側のペインで**API: TiDBCloudApiGatewayV2**をクリックします。

2.  **概要**ページから`Invoke URL`をコピーしてください。この URL が API エンドポイントとして機能します。

    ![API Gateway Invoke URL](/media/develop/aws-lambda-get-apigateway-invoke-url.png)

3.  APIをテストするには、PostmanやcURLなどのAPIテストツールを使用してください。

    -   模擬書籍の初期化:

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{"count":100}' https://<your-api-endpoint>/book/init
        ```

    -   すべての書籍を入手する：

        ```shell
        curl https://<your-api-endpoint>/book
        ```

    -   書籍IDで書籍を入手：

        ```shell
        curl https://<your-api-endpoint>/book/<book-id>
        ```

    -   本を作成する：

        ```shell
        curl -X POST -H "Content-Type: application/json" -d '{ "title": "Book Title", "type": "Test", "publishAt": "2022-12-15T21:01:49.000Z", "stock": 123, "price": 12.34, "authors": "Test Test" }' https://  <your-api-endpoint>/book
        ```

    -   本を更新する：

        ```shell
        curl -X PUT -H "Content-Type: application/json" -d '{ "title": "Book Title(updated)" }' https://<your-api-endpoint>/book/<book-id>
        ```

    -   本を削除する：

        ```shell
        curl -X DELETE https://<your-api-endpoint>/book/<book-id>
        ```

## ステップ3．リソースを整理する {#step-3-clean-up-resources}

不要な料金が発生しないように、作成されたすべてのリソースをクリーンアップしてください。

1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/cloudformation)コンソールにアクセスします。
2.  作成したAWS CloudFormationスタックを削除してください。
