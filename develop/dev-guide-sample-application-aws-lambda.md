---
title: Connect to TiDB with mysql2 in AWS Lambda Function
summary: この記事では、AWS Lambda FunctionsでTiDBとmysql2を使用してCRUDアプリケーションを構築する方法を説明し、簡単なサンプルコードを提供します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-aws-lambda/','/ja/tidb/dev/dev-guide-sample-application-aws-lambda/','/ja/tidbcloud/dev-guide-sample-application-aws-lambda/']
---

# AWS Lambda関数でmysql2を使用してTiDBに接続する {#connect-to-tidb-with-mysql2-in-aws-lambda-function}

TiDBはMySQL互換データベース、 [AWS Lambda関数](https://aws.amazon.com/lambda/)はコンピューティングサービス、 [mysql2](https://github.com/sidorares/node-mysql2)はNode.jsで人気のオープンソースドライバです。

このチュートリアルでは、AWS Lambda FunctionsでTiDBとmysql2を使用して以下のタスクを実行する方法を学びます。

-   環境をセットアップしてください。
-   mysql2を使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。
-   AWS Lambda関数をデプロイ。

> **注記**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。
-   管理者権限を持つ[AWSユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html)。
-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
-   [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

AWSアカウントまたはユーザーをお持ちでない場合は、 [Lambda入門](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)ガイドの手順に従って作成できます。

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

> **注記**
>
> 完全なコードスニペットと実行手順については、 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHubリポジトリを参照してください。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `mysql2`を含む）をインストールするには、次のコマンドを実行してください。

```bash
npm install
```

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>

<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **注記**
    >
    > Node.jsアプリケーションでは、SSL CA証明書を提供する必要はありません。Node.jsはTLS（SSL）接続を確立する際に、デフォルトで組み込みの[Mozilla CA証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用するためです。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを作成できます。

5.  対応する接続​​文字列をコピーして`env.json`に貼り付けてください。以下に例を示します。

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
        "TIDB_PORT": "4000",
        "TIDB_USER": "{prefix}.root",
        "TIDB_PASSWORD": "{password}",
        "TIDB_ENABLE_SSL": "true"
      }
    }
    ```

    `{}`内のプレースホルダーを、接続ダイアログで取得した値に置き換えてください。

</div>

<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  対応する接続​​文字列をコピーして`env.json`に貼り付けてください。以下に例を示します。

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{host}",
        "TIDB_PORT": "4000",
        "TIDB_USER": "root",
        "TIDB_PASSWORD": "{password}",
        "TIDB_ENABLE_SSL": "false"
      }
    }
    ```

    `{}`内のプレースホルダーを、接続ダイアログで取得した値に置き換えてください。

</div>

<div label="TiDB Self-Managed" value="tidb">

対応する接続​​文字列をコピーして`env.json`に貼り付けてください。以下に例を示します。

```json
{
  "Parameters": {
    "TIDB_HOST": "{tidb_server_host}",
    "TIDB_PORT": "4000",
    "TIDB_USER": "root",
    "TIDB_PASSWORD": "{password}",
    "TIDB_ENABLE_SSL": "false"
  }
}
```

`{}`内のプレースホルダーを、 **Connect**ウィンドウで取得した値に置き換えてください。

</div>

</SimpleTab>

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  （前提条件） [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)をインストールしてください。

2.  バンドルを作成する:

    ```bash
    npm run build
    ```

3.  サンプルLambda関数を呼び出します。

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4.  ターミナルの出力を確認してください。出力が以下の例と似ていれば、接続は成功しています。

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

接続が成功したことを確認したら、[次のセクション](#deploy-the-aws-lambda-function)セクションに従って AWS Lambda 関数をデプロイできます。

## AWS Lambda関数をデプロイ {#deploy-the-aws-lambda-function}

AWS Lambda関数は、 [SAM CLI](#sam-cli-deployment-recommended)または[AWS Lambdaコンソール](#web-console-deployment)プラグインのいずれかを使用してデプロイできます。

### SAM CLIの導入（推奨） {#sam-cli-deployment-recommended}

1.  ([前提条件](#prerequisites)) [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)をインストールします。

2.  バンドルを作成する:

    ```bash
    npm run build
    ```

3.  [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml)の環境変数を更新してください。

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4.  AWS 環境変数を設定します ( [短期資格](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)を参照)。

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5.  AWS Lambda関数をデプロイ：

    ```bash
    sam deploy --guided

    # Example:

    # Configuring SAM deploy
    # ======================

    #        Looking for config file [samconfig.toml] :  Not found

    #        Setting default arguments for 'sam deploy'
    #        =========================================
    #        Stack Name [sam-app]: tidb-aws-lambda-quickstart
    #        AWS Region [us-east-1]:
    #        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
    #        Confirm changes before deploy [y/N]:
    #        #SAM needs permission to be able to create roles to connect to the resources in your template
    #        Allow SAM CLI IAM role creation [Y/n]:
    #        #Preserves the state of previously provisioned resources when an operation fails
    #        Disable rollback [y/N]:
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        tidbHelloWorldFunction may not have authorization defined, Is this okay? [y/N]: y
    #        Save arguments to configuration file [Y/n]:
    #        SAM configuration file [samconfig.toml]:
    #        SAM configuration environment [default]:

    #        Looking for resources needed for deployment:
    #        Creating the required resources...
    #        Successfully created!
    ```

### Webコンソールの展開 {#web-console-deployment}

1.  バンドルを作成する:

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2.  [AWS Lambdaコンソール](https://console.aws.amazon.com/lambda/home#/functions)コンソールにアクセスしてください。

3.  [Lambda関数の作成](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html)の手順に従って、Node.js Lambda 関数を作成します。

4.  [Lambda デプロイメントパッケージ](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip)の手順に従って、 `dist/index.zip`ファイルをアップロードします。

5.  Lambda 関数で[対応する接続​​文字列をコピーして設定します。](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)

    1.  Lambda コンソールの[機能](https://console.aws.amazon.com/lambda/home#/functions)ページで、 **[コンフィグレーション]**タブを選択し、 **[環境変数]**を選択します。
    2.  **「編集」**を選択してください。
    3.  データベースへのアクセス資格情報を追加するには、以下の手順を実行してください。
        -   **「環境変数の追加」**を選択し、 **「キー」**に`TIDB_HOST`と入力し、 **「値」**にホスト名を入力します。
        -   **「環境変数の追加」**を選択し、 **「キー」**に`TIDB_PORT`と入力し、 **「値」**にポート番号を入力します（デフォルトは4000です）。
        -   **「環境変数の追加」**を選択し、 **「キー」**に`TIDB_USER`と入力し、 **「値」**にユーザー名を入力します。
        -   **「環境変数の追加」**を選択し、 **「キー」**に`TIDB_PASSWORD`と入力し、 **「値」**にデータベース作成時に選択したパスワードを入力します。
        -   **「保存」**を選択してください。

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

以下のコードは、環境変数で定義されたオプションを使用してTiDBへの接続を確立します。

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB password
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    } : null,
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
    enableKeepAlive: true,
  });
}

export function getPool(): mysql.Pool {
  if (!pool) {
    pool = connect();
  }
  return pool;
}
```

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `Player` `1` } レコードを返します。

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

以下のクエリは、 `50`の ID を持つ`50`に`Player`コインと`1`の商品を追加します。

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、IDが`Player`である`1`レコードを削除します。

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理することで、接続の頻繁な確立と切断によって発生するパフォーマンスのオーバーヘッドを削減できます。
-   SQL インジェクションを回避するには、 [準備された声明](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、[シークエライズ](https://sequelize.org/)、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)などの ORM フレームワークを使用すると、開発効率が大幅に向上します。
-   アプリケーション用の RESTful API を構築するには、 [AWS LambdaをAPI Gatewayで使用する](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)お勧めします。
-   TiDB Cloud Starterと AWS Lambda を使用した高性能アプリケーションの設計については、 [このブログ](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)を参照してください。

## 次のステップ {#next-steps}

-   AWS Lambda関数でTiDBを使用する方法の詳細については、 [TiDB-Lambda統合/aws-lambda-bookstoreデモ](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)ご覧ください。また、AWS API Gatewayを使用して、アプリケーション用のRESTful APIを構築することもできます。
-   `mysql2`の使用法について詳しくは、 [`mysql2`のドキュメント](https://sidorares.github.io/node-mysql2/docs/documentation)ご覧ください。
-   AWS Lambda の使用方法の詳細については[AWS `Lambda`の開発者ガイド](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)ご覧ください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
