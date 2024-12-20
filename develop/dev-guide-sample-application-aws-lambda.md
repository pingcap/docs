---
title: Connect to TiDB with mysql2 in AWS Lambda Function
summary: この記事では、AWS Lambda 関数で TiDB と mysql2 を使用して CRUD アプリケーションを構築する方法について説明し、簡単なサンプル コード スニペットを示します。
---

# AWS Lambda 関数で mysql2 を使用して TiDB に接続する {#connect-to-tidb-with-mysql2-in-aws-lambda-function}

TiDB は MySQL 互換のデータベース、 [AWS Lambda 関数](https://aws.amazon.com/lambda/)はコンピューティング サービス、 [マイSQL2](https://github.com/sidorares/node-mysql2) Node.js 用の人気のあるオープン ソース ドライバーです。

このチュートリアルでは、AWS Lambda 関数で TiDB と mysql2 を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることができます。
-   AWS Lambda 関数をデプロイ。

> **注記**
>
> このチュートリアルは、 TiDB Cloud Serverless および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。
-   管理者権限を持つ[AWS ユーザー](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html) 。
-   [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
-   [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

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

AWS アカウントまたはユーザーがない場合は、ガイド[Lambda を使い始める](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)の手順に従って作成できます。

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

> **注記**
>
> 完全なコード スニペットと実行手順については、 [tidb サンプル/tidb-aws-lambda クイックスタート](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub リポジトリを参照してください。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`を含む) をインストールします。

```bash
npm install
```

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>

<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」を**クリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチは**`main`に設定されています

    -   **接続先は**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **注記**
    >
    > Node.js アプリケーションでは、TLS (SSL) 接続を確立するときに Node.js がデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)使用するため、SSL CA 証明書を提供する必要はありません。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」**をクリックします。

    > **ヒント**
    >
    > 以前にパスワードを生成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  対応する接続文字列をコピーして`env.json`に貼り付けます。次に例を示します。

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

    `{}`のプレースホルダーを接続ダイアログで取得した値に置き換えます。

</div>

<div label="TiDB Self-Managed">

対応する接続文字列をコピーして`env.json`に貼り付けます。次に例を示します。

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

`{}`のプレースホルダーを、**接続**ウィンドウで取得した値に置き換えます。

</div>

</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  (前提条件) [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)インストールします。

2.  バンドルをビルドします。

    ```bash
    npm run build
    ```

3.  サンプル Lambda 関数を呼び出します。

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

4.  ターミナルの出力を確認します。出力が次のようになる場合、接続は成功しています。

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

接続が成功したことを確認したら、 [次のセクション](#deploy-the-aws-lambda-function)に従って AWS Lambda 関数をデプロイします。

## AWS Lambda関数をデプロイ {#deploy-the-aws-lambda-function}

AWS Lambda 関数は、 [SAM CLI](#sam-cli-deployment-recommended)または[AWS Lambda コンソール](#web-console-deployment)いずれかを使用してデプロイできます。

### SAM CLI の展開 (推奨) {#sam-cli-deployment-recommended}

1.  （ [前提条件](#prerequisites) ） [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)をインストールします。

2.  バンドルをビルドします。

    ```bash
    npm run build
    ```

3.  [`template.yml`](https://github.com/tidb-samples/tidb-aws-lambda-quickstart/blob/main/template.yml)の環境変数を更新します:

    ```yaml
    Environment:
      Variables:
        TIDB_HOST: {tidb_server_host}
        TIDB_PORT: 4000
        TIDB_USER: {prefix}.root
        TIDB_PASSWORD: {password}
    ```

4.  AWS環境変数を設定します（ [短期資格](https://docs.aws.amazon.com/cli/latest/userguide/cli-authentication-short-term.html)を参照）。

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

### Webコンソールの展開 {#web-console-deployment}

1.  バンドルをビルドします。

    ```bash
    npm run build

    # Bundle for AWS Lambda
    # =====================
    # dist/index.zip
    ```

2.  [AWS Lambda コンソール](https://console.aws.amazon.com/lambda/home#/functions)ご覧ください。

3.  [Lambda関数の作成](https://docs.aws.amazon.com/lambda/latest/dg/lambda-nodejs.html)の手順に従って、Node.js Lambda 関数を作成します。

4.  [Lambda デプロイメント パッケージ](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html#gettingstarted-package-zip)の手順に従って`dist/index.zip`ファイルをアップロードします。

5.  Lambda 関数では[対応する接続文字列をコピーして設定します](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) 。

    1.  Lambda コンソールの[機能](https://console.aws.amazon.com/lambda/home#/functions)ページで、 **[コンフィグレーション]**タブを選択し、 **[環境変数]**を選択します。
    2.  **編集を**選択します。
    3.  データベース アクセス資格情報を追加するには、次の手順を実行します。
        -   **[環境変数の追加]**を選択し、**キー**に`TIDB_HOST`入力し、**値**にホスト名を入力します。
        -   **[環境変数の追加]**を選択し、**キー**に`TIDB_PORT`入力し、**値**にポートを入力します (デフォルトは 4000)。
        -   **[環境変数の追加]**を選択し、**キー**に`TIDB_USER`入力し、**値**にユーザー名を入力します。
        -   **[環境変数の追加]**を選択し、**キー**に`TIDB_PASSWORD`入力し、**値**にデータベースの作成時に選択したパスワードを入力します。
        -   **[保存]**を選択します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb サンプル/tidb-aws-lambda クイックスタート](https://github.com/tidb-samples/tidb-aws-lambda-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

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

### データを挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```typescript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、 ID `1`の単一の`Player`レコードを返します。

```typescript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは、 ID `1`の`Player`にコイン`50`枚と商品`50`を追加します。

```typescript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `1`の`Player`のレコードを削除します。

```typescript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役に立つメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)使用してデータベース接続を管理すると、接続の確立と破棄を頻繁に行うことによって発生するパフォーマンスのオーバーヘッドを削減できます。
-   SQL インジェクションを回避するには、 [準備されたステートメント](https://github.com/sidorares/node-mysql2#using-prepared-statements)使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、 [続編](https://sequelize.org/) 、 [タイプORM](https://typeorm.io/) 、 [プリズマ](https://www.prisma.io/)などの ORM フレームワークを使用すると、開発効率が大幅に向上します。
-   アプリケーション用の RESTful API を構築するには、 [API GatewayでAWS Lambdaを使用する](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html)をお勧めします。
-   TiDB Cloud Serverless と AWS Lambda を使用して高性能アプリケーションを設計するには、 [このブログ](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/)を参照してください。

## 次のステップ {#next-steps}

-   AWS Lambda 関数で TiDB を使用する方法の詳細については、 [TiDB-Lambda-integration/aws-lambda-bookstore デモ](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md)参照してください。また、AWS API Gateway を使用して、アプリケーション用の RESTful API を構築することもできます。
-   [`mysql2`のドキュメント](https://sidorares.github.io/node-mysql2/docs/documentation)から`mysql2`の使用法について詳しく学びます。
-   [`Lambda`のAWS開発者ガイド](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)から AWS Lambda の使用方法について詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>
