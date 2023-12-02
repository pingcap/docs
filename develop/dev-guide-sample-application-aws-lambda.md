---
title: Connect to TiDB with mysql2 in AWS Lambda Function
summary: This article describes how to build a CRUD application using TiDB and mysql2 in AWS Lambda Function and provides a simple example code snippet.
---

# AWS Lambda 関数の mysql2 を使用して TiDB に接続する {#connect-to-tidb-with-mysql2-in-aws-lambda-function}

TiDB は MySQL 互換データベース、 [AWSラムダ関数](https://aws.amazon.com/lambda/)はコンピューティング サービス、 [mysql2](https://github.com/sidorares/node-mysql2)は Node.js 用の一般的なオープンソース ドライバーです。

このチュートリアルでは、AWS Lambda 関数で TiDB と mysql2 を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。
-   AWS Lambda 関数をデプロイ。

> **注記**
>
> このチュートリアルは、TiDB サーバーレスおよび TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。
-   管理者権限を持つ[AWSユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) 。
-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
-   [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

AWS アカウントまたはユーザーをお持ちでない場合は、 [Lambda の入門](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)ガイドの手順に従って作成できます。

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

> **注記**
>
> 完全なコード スニペットと実行手順については、 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub リポジトリを参照してください。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`を含む) をインストールします。

```bash
npm install
```

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>

<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **注記**
    >
    > Node.js アプリケーションでは、TLS (SSL) 接続を確立するときにデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用するため、SSL CA 証明書を提供する必要はありません。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント**
    >
    > 以前にパスワードを生成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  対応する接続​​文字列をコピーして`env.json`に貼り付けます。以下は例です。

    ```json
    {
      "Parameters": {
        "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
        "TIDB_PORT": "4000",
        "TIDB_USER": "{prefix}.root",
        "TIDB_PASSWORD": "{password}"
      }
    }
    ```

    `{}`のプレースホルダーを、接続ダイアログで取得した値に置き換えます。

</div>

<div label="TiDB Self-Hosted">

対応する接続​​文字列をコピーして`env.json`に貼り付けます。以下は例です。

```json
{
  "Parameters": {
    "TIDB_HOST": "{tidb_server_host}",
    "TIDB_PORT": "4000",
    "TIDB_USER": "root",
    "TIDB_PASSWORD": "{password}"
  }
}
```

`{}`のプレースホルダーを、 **「接続」**ウィンドウで取得した値に置き換えます。

</div>

</SimpleTab>

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  (前提条件) [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)をインストールします。

2.  バンドルをビルドします。

    ```bash
    npm run build
    ```

3.  サンプルの Lambda 関数を呼び出します。

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4.  端末の出力を確認します。出力が次のような場合、接続は成功しています。

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

接続が成功したことを確認したら、 [次のセクション](#deploy-the-aws-lambda-function)に従って AWS Lambda 関数をデプロイします。

## AWS Lambda 関数をデプロイ {#deploy-the-aws-lambda-function}

[サム・クリ](#sam-cli-deployment-recommended)または[AWS Lambda コンソール](#web-console-deployment)いずれかを使用して AWS Lambda 関数をデプロイできます。

### SAM CLI の導入 (推奨) {#sam-cli-deployment-recommended}

1.  ( [前提条件](#prerequisites) ) [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)を取り付けます。

2.  バンドルをビルドします。

    ```bash
    npm run build
    ```

3.  [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml)で環境変数を更新します。

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4.  AWS 環境変数を設定します ( [短期資格情報](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)を参照)。

    ```bash
    export AWS_ACCESS_KEY_ID={your_access_key_id}
    export AWS_SECRET_ACCESS_KEY={your_secret_access_key}
    export AWS_SESSION_TOKEN={your_session_token}
    ```

5.  AWS Lambda 関数をデプロイ。

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

### Web コンソールの展開 {#web-console-deployment}

1.  バンドルをビルドします。

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2.  [AWS Lambda コンソール](https://console.aws.amazon.com/lambda/home#/functions)にアクセスしてください。

3.  [Lambda 関数の作成](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html)の手順に従って、Node.js Lambda 関数を作成します。

4.  [Lambdaデプロイメントパッケージ](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip)の手順に従って、 `dist/index.zip`ファイルをアップロードします。

5.  Lambda 関数では[対応する接続​​文字列をコピーして構成します](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) 。

    1.  Lambda コンソールの[機能](https://console.aws.amazon.com/lambda/home#/functions)ページで、 **[コンフィグレーション]**タブを選択し、 **[環境変数]**を選択します。
    2.  **[編集]**を選択します。
    3.  データベース アクセス資格情報を追加するには、次の手順を実行します。
        -   **[環境変数の追加]**を選択し、 **[キー]**に`TIDB_HOST`を入力し、[**値]**にホスト名を入力します。
        -   **[環境変数の追加]**を選択し、 **[キー]**に`TIDB_PORT`を入力し、 **[値]**にポートを入力します (デフォルトは 4000)。
        -   **[環境変数の追加]**を選択し、 **[キー]**に`TIDB_USER`を入力し、[**値]**にユーザー名を入力します。
        -   **[環境変数の追加]**を選択し、 **[キー]**に`TIDB_PASSWORD`を入力し、[**値]**にデータベースの作成時に選択したパスワードを入力します。
        -   **[保存]**を選択します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

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
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
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

### データの挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `1`による単一の`Player`レコードを返します。

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `1`の`Player`に`50`コインと`50`グッズを追加します。

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、ID `1`の`Player`レコードを削除します。

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 便利なメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理すると、接続の頻繁な確立と破棄によって生じるパフォーマンスのオーバーヘッドを軽減できます。
-   SQL インジェクションを回避するには、 [準備されたステートメント](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、 [続編](https://sequelize.org/) 、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)のような ORM フレームワークを使用すると、開発効率が大幅に向上します。
-   アプリケーションの RESTful API を構築するには、 [APIゲートウェイでAWS Lambdaを使用する](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)をお勧めします。
-   TiDB Serverless と AWS Lambda を使用した高性能アプリケーションの設計については、 [このブログ](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)を参照してください。

## 次のステップ {#next-steps}

-   AWS Lambda 関数で TiDB を使用する方法の詳細については、 [TiDB-Lambda-integration/aws-lambda-bookstore デモ](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)を参照してください。 AWS API Gateway を使用して、アプリケーション用の RESTful API を構築することもできます。
-   `mysql2`から[`mysql2`のドキュメント](https://github.com/sidorares/node-mysql2/tree/master/documentation/en)の使用法をさらに学習します。
-   AWS Lambdaの使い方を[`Lambda`の AWS 開発者ガイド](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)から詳しく学びましょう。
-   TiDB アプリケーション開発の[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>
