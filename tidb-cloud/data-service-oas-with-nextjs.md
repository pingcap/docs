---
title: Use the OpenAPI Specification of a Data App with Next.js
summary: データアプリのOpenAPI仕様を使用してクライアントコードを生成し、Next.jsアプリケーションを開発する方法を学びます。
---

# Next.jsでデータアプリのOpenAPI仕様を使用する {#use-the-openapi-specification-of-a-data-app-with-next-js}

このドキュメントでは[データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の OpenAPI 仕様を使用してクライアント コードを生成し、Next.js アプリケーションを開発する方法を紹介します。

## 始める前に {#before-you-begin}

Next.jsでOpenAPI Specificationを使用する前に、以下のものが用意されていることを確認してください。

-   [TiDB Cloud Starterインスタンス](/tidb-cloud/create-tidb-cluster-serverless.md)または[TiDB Cloud Dedicatedクラスター](/tidb-cloud/create-tidb-cluster.md)クラスター。
-   [Node.js](https://nodejs.org/en/download)
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
-   [糸](https://yarnpkg.com/getting-started/install)

このドキュメントでは、例としてTiDB Cloud Starterインスタンスを使用します。

## ステップ1. データの準備 {#step-1-prepare-data}

まず、 TiDB Cloud StarterインスタンスまたはTiDB Cloud Dedicatedクラスターにテーブル`test.repository`を作成し、サンプルデータを挿入します。以下の例では、デモンストレーション用のデータとして、PingCAP が開発したオープンソースプロジェクトをいくつか挿入します。

SQL ステートメントを実行するには、 [TiDB Cloudコンソール](https://tidbcloud.com)の[SQLエディタ](/tidb-cloud/explore-data-with-chat2query.md)使用できます。

```sql
-- Select the database
USE test;

-- Create the table
CREATE TABLE repository (
        id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
        name varchar(64) NOT NULL,
        url varchar(256) NOT NULL
);

-- Insert some sample data into the table
INSERT INTO repository (name, url)
VALUES ('tidb', 'https://github.com/pingcap/tidb'),
        ('tikv', 'https://github.com/tikv/tikv'),
        ('pd', 'https://github.com/tikv/pd'),
        ('tiflash', 'https://github.com/pingcap/tiflash');
```

## ステップ2. データアプリを作成する {#step-2-create-a-data-app}

データ挿入後、 [TiDB Cloudコンソール](https://tidbcloud.com)のデータ[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。 TiDB Cloud StarterインスタンスまたはTiDB Cloud Dedicatedクラスターにリンクするデータ アプリを作成し、データ アプリの API キーを作成してから、データ アプリに`GET /repositories`エンドポイントを作成します。このエンドポイントに対応する SQL ステートメントは次のとおりです。これは`test.repository`テーブルからすべての行を取得します。

```sql
SELECT * FROM test.repository;
```

詳細については、[データサービスの利用開始](/tidb-cloud/data-service-get-started.md)をご覧ください。

## ステップ3．クライアントコードを生成する {#step-3-generate-client-code}

以下では、Next.jsを例として、データアプリのOpenAPI仕様を使用してクライアントコードを生成する方法を説明します。

1.  `hello-repos`という名前の Next.js プロジェクトを作成します。

    公式テンプレートを使用してNext.jsプロジェクトを作成するには、次のコマンドを使用し、プロンプトが表示されたらすべてのデフォルトオプションをそのまま使用してください。

    ```shell
    yarn create next-app hello-repos
    ```

    以下のコマンドを使用して、新しく作成したプロジェクトのディレクトリに移動します。

    ```shell
    cd hello-repos
    ```

2.  依存関係をインストールします。

    このドキュメントでは[OpenAPIジェネレーター](https://github.com/OpenAPITools/openapi-generator)を使用して、OpenAPI 仕様から API クライアント ライブラリを自動的に生成します。

    OpenAPI Generatorを開発依存関係としてインストールするには、次のコマンドを実行します。

    ```shell
    yarn add @openapitools/openapi-generator-cli --dev
    ```

3.  OpenAPI仕様をダウンロードして、 `oas/doc.json`として保存してください。

    1.  TiDB Cloud[**データサービス**](https://tidbcloud.com/project/data-service)ページで、左側のペインにあるデータアプリ名をクリックすると、アプリの設定が表示されます。
    2.  **API仕様**エリアで**「ダウンロード」**をクリックし、JSON形式を選択して、プロンプトが表示されたら**「承認」**をクリックします。
    3.  ダウンロードしたファイルを`oas/doc.json`プロジェクトディレクトリに`hello-repos` }という名前で保存してください。

    詳細については、 [OpenAPI仕様書をダウンロードする](/tidb-cloud/data-service-manage-data-app.md#download-the-openapi-specification)参照してください。

    `oas/doc.json`ファイルの構造は以下のとおりです。

    ```json
    {
      "openapi": "3.0.3",
      "components": {
        "schemas": {
          "getRepositoriesResponse": {
            "properties": {
              "data": {
                "properties": {
                  "columns": { ... },
                  "result": { ... },
                  "rows": {
                    "items": {
                      "properties": {
                        "id": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "url": {
                          "type": "string"
                        }
    ...
      "paths": {
        "/repositories": {
          "get": {
            "operationId": "getRepositories",
            "responses": {
              "200": {
                "content": {
                  "application/json": {
                    "schema": {
                      "$ref": "#/components/schemas/getRepositoriesResponse"
                    }
                  }
                },
                "description": "OK"
              },
    ...
    ```

4.  クライアントコードを生成する：

    ```shell
    yarn run openapi-generator-cli generate -i oas/doc.json --generator-name typescript-fetch -o gen/api
    ```

    このコマンドは`oas/doc.json`仕様を入力として使用してクライアントコードを生成し、 `gen/api`ディレクトリに出力します。

## ステップ4．Next.jsアプリケーションを開発する {#step-4-develop-your-next-js-application}

生成されたクライアントコードを使用して、Next.jsアプリケーションを開発できます。

1.  `hello-repos`プロジェクトディレクトリに、次の変数を含む`.env.local`ファイルを作成し、変数の値をデータアプリの公開鍵と秘密鍵に設定します。

        TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY=YOUR_PUBLIC_KEY
        TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY=YOUR_PRIVATE_KEY

    データ アプリの API キーを作成するには、 [APIキーを作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)参照してください。

2.  `hello-repos`プロジェクトディレクトリで、 `app/page.tsx`の内容を、 `GET /repositories`エンドポイントからデータを取得して表示する以下のコードに置き換えてください。

    ```js
    import {DefaultApi, Configuration} from "../gen/api"

    export default async function Home() {
      const config = new Configuration({
        username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
        password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
      });
      const apiClient = new DefaultApi(config);
      const resp = await apiClient.getRepositories();
      return (
        <main className="flex min-h-screen flex-col items-center justify-between p-24">
          <ul className="font-mono text-2xl">
            {resp.data.rows.map((repo) => (
              <a href={repo.url}>
                <li key={repo.id}>{repo.name}</li>
              </a>
            ))}
          </ul>
        </main>
      )
    }
    ```

    > **注記：**
    >
    > データアプリにリンクされているTiDB Cloud StarterインスタンスまたはTiDB Cloud Dedicatedクラスターが異なるリージョンでホストされている場合、ダウンロードした OpenAPI 仕様ファイルの`servers`セクションに複数の項目が表示されます。この場合、 `config`オブジェクトのエンドポイント パスを次のように構成する必要があります。
    >
    > ```js
    > const config = new Configuration({
    >     username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
    >     password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
    >     basePath: "https://${YOUR_REGION}.data.dev.tidbcloud.com/api/v1beta/app/${YOUR_DATA_APP_ID}/endpoint"
    >   });
    > ```
    >
    > `basePath`データアプリの実際のエンドポイントパスに置き換えてください。 `${YOUR_REGION}`と`{YOUR_DATA_APP_ID}`を取得するには、エンドポイントの**プロパティ**パネルで**エンドポイント URL を**確認してください。

## ステップ5．Next.jsアプリケーションをプレビューする {#step-5-preview-your-next-js-application}

> **注記：**
>
> プレビューを実行する前に、必要な依存関係がすべてインストールされ、正しく設定されていることを確認してください。

ローカル開発サーバーでアプリケーションをプレビューするには、次のコマンドを実行します。

```shell
yarn dev
```

その後、ブラウザで[http://localhost:3000](http://localhost:3000)を開くと、 `test.repository`データベースのデータがページに表示されます。
