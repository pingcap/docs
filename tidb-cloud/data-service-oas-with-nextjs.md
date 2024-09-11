---
title: Use the OpenAPI Specification of a Data App with Next.js
summary: データ アプリの OpenAPI 仕様を使用してクライアント コードを生成し、Next.js アプリケーションを開発する方法を学習します。
---

# Next.js でデータ アプリの OpenAPI 仕様を使用する {#use-the-openapi-specification-of-a-data-app-with-next-js}

このドキュメントでは、 [データアプリ](/tidb-cloud/tidb-cloud-glossary.md#data-app)の OpenAPI 仕様を使用してクライアント コードを生成し、Next.js アプリケーションを開発する方法を紹介します。

## 始める前に {#before-you-begin}

Next.js で OpenAPI 仕様を使用する前に、次のものを用意してください。

-   TiDB クラスター。詳細については、 [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)または[TiDB Cloud専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。
-   [Node.js](https://nodejs.org/en/download)
-   [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
-   [糸](https://yarnpkg.com/getting-started/install)

このドキュメントでは、TiDB Cloud Serverless クラスターを例として使用します。

## ステップ1. データを準備する {#step-1-prepare-data}

まず、TiDB クラスターにテーブル`test.repository`を作成し、そこにサンプル データを挿入します。次の例では、デモ用のデータとして、PingCAP によって開発されたオープン ソース プロジェクトをいくつか挿入します。

SQL ステートメントを実行するには、 [TiDB Cloudコンソール](https://tidbcloud.com)の[SQL エディター](/tidb-cloud/explore-data-with-chat2query.md)使用できます。

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

データが挿入されたら、 [TiDB Cloudコンソール](https://tidbcloud.com)の[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。TiDB クラスターにリンクするデータ アプリを作成し、データ アプリの API キーを作成してから、データ アプリに`GET /repositories`エンドポイントを作成します。このエンドポイントに対応する SQL ステートメントは次のようになります。これは、 `test.repository`テーブルからすべての行を取得します。

```sql
SELECT * FROM test.repository;
```

詳細については[データサービスを始める](/tidb-cloud/data-service-get-started.md)参照してください。

## ステップ3. クライアントコードを生成する {#step-3-generate-client-code}

以下では、Next.js を例として使用し、データ アプリの OpenAPI 仕様を使用してクライアント コードを生成する方法を説明します。

1.  `hello-repos`という名前の Next.js プロジェクトを作成します。

    公式テンプレートを使用して Next.js プロジェクトを作成するには、次のコマンドを使用し、プロンプトが表示されたらすべてのデフォルト オプションをそのままにします。

    ```shell
    yarn create next-app hello-repos
    ```

    次のコマンドを使用して、新しく作成されたプロジェクトにディレクトリを変更します。

    ```shell
    cd hello-repos
    ```

2.  依存関係をインストールします。

    このドキュメントでは、 [OpenAPI ジェネレーター](https://github.com/OpenAPITools/openapi-generator)使用して、OpenAPI 仕様から API クライアント ライブラリを自動的に生成します。

    OpenAPI Generator を開発依存関係としてインストールするには、次のコマンドを実行します。

    ```shell
    yarn add @openapitools/openapi-generator-cli --dev
    ```

3.  OpenAPI 仕様をダウンロードし、 `oas/doc.json`として保存します。

    1.  TiDB Cloud [**データサービス**](https://tidbcloud.com/console/data-service)ページで、左側のペインにあるデータ アプリ名をクリックして、アプリ設定を表示します。
    2.  **API 仕様**領域で、 **「ダウンロード」を**クリックし、JSON 形式を選択して、プロンプトが表示されたら**「承認」を**クリックします。
    3.  ダウンロードしたファイルを`hello-repos`プロジェクトディレクトリに`oas/doc.json`として保存します。

    詳細については[OpenAPI仕様をダウンロードする](/tidb-cloud/data-service-manage-data-app.md#download-the-openapi-specification)参照してください。

    `oas/doc.json`ファイルの構造は次のとおりです。

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

4.  クライアント コードを生成します。

    ```shell
    yarn run openapi-generator-cli generate -i oas/doc.json --generator-name typescript-fetch -o gen/api
    ```

    このコマンドは、 `oas/doc.json`仕様を入力として使用してクライアント コードを生成し、クライアント コードを`gen/api`ディレクトリに出力します。

## ステップ4. Next.jsアプリケーションを開発する {#step-4-develop-your-next-js-application}

生成されたクライアント コードを使用して、Next.js アプリケーションを開発できます。

1.  `hello-repos`プロジェクト ディレクトリで、次の変数を含む`.env.local`ファイルを作成し、変数の値をデータ アプリの公開キーと秘密キーに設定します。

        TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY=YOUR_PUBLIC_KEY
        TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY=YOUR_PRIVATE_KEY

    データ アプリの API キーを作成するには、 [APIキーを作成する](/tidb-cloud/data-service-api-key.md#create-an-api-key)参照してください。

2.  `hello-repos`プロジェクト ディレクトリで、 `app/page.tsx`の内容を次のコードに置き換えます。このコードは、 `GET /repositories`エンドポイントからデータを取得してレンダリングします。

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
    > データ アプリのリンクされたクラスタが異なるリージョンでホストされている場合、ダウンロードした OpenAPI 仕様ファイルの`servers`セクションに複数の項目が表示されます。この場合、 `config`オブジェクトでエンドポイント パスを次のように構成する必要もあります。
    >
    > ```js
    > const config = new Configuration({
    >     username: process.env.TIDBCLOUD_DATA_SERVICE_PUBLIC_KEY,
    >     password: process.env.TIDBCLOUD_DATA_SERVICE_PRIVATE_KEY,
    >     basePath: "https://${YOUR_REGION}.data.dev.tidbcloud.com/api/v1beta/app/${YOUR_DATA_APP_ID}/endpoint"
    >   });
    > ```
    >
    > `basePath`データ アプリの実際のエンドポイント パスに置き換えてください。 `${YOUR_REGION}`と`{YOUR_DATA_APP_ID}`を取得するには、エンドポイントの**プロパティ**パネルで**エンドポイント URL**を確認します。

## ステップ5. Next.jsアプリケーションをプレビューする {#step-5-preview-your-next-js-application}

> **注記：**
>
> プレビューする前に、必要な依存関係がすべてインストールされ、正しく構成されていることを確認してください。

ローカル開発サーバーでアプリケーションをプレビューするには、次のコマンドを実行します。

```shell
yarn dev
```

その後、ブラウザで[http://ローカルホスト:3000](http://localhost:3000)開き、ページに表示される`test.repository`データベースのデータを確認できます。
