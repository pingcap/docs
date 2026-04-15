---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: TiDB CloudサーバーレスドライバーをKyselyで使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-driver-kysely-example/']
---

# TiDB Cloud Serverless Driver Kysely チュートリアル {#tidb-cloud-serverless-driver-kysely-tutorial}

[キセリー](https://kysely.dev/docs/intro)、タイプセーフでオートコンプリートに適した TypeScript SQL クエリ ビルダーです。 TiDB Cloudは[@tidbcloud/kysely](https://github.com/tidbcloud/kysely)を提供しており、 [TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md)を使用して HTTPS 経由で Kysely を使用できるようにします。従来の TCP 方式と比較して、 [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)は次の利点があります。

-   サーバーレス環境におけるパフォーマンスの向上。
-   Kyselyをエッジ環境で使用できる機能。

このチュートリアルでは、Node.js環境およびエッジ環境で、 TiDB CloudサーバーレスドライバーをKyselyと組み合わせて使用​​する方法について説明します。

## Node.js環境でTiDB Cloud Kysely方言を使用する {#use-tidb-cloud-kysely-dialect-in-node-js-environments}

このセクションでは、Node.js環境でKyselyとTiDB Cloudサーバーレスドライバーを連携させる方法について説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、以下のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `kysely-node-example`という名前のプロジェクトを作成します。

        mkdir kysely-node-example
        cd kysely-node-example

2.  `kysely` 、 `@tidbcloud/kysely` 、および`@tidbcloud/serverless`パッケージをインストールしてください。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

3.  プロジェクトのルートディレクトリで、 `package.json`ファイルを探し、そのファイルに`"type": "module"`を追加して ES モジュールを指定します。

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/kysely": "^0.0.4",
        "@tidbcloud/serverless": "^0.0.7",
        "kysely": "^0.26.3",
      }
    }
    ```

4.  プロジェクトのルートディレクトリに、TypeScriptコンパイラオプションを定義する`tsconfig.json`ファイルを追加します。以下にファイルの例を示します。

    ```json
    {
      "compilerOptions": {
        "module": "ES2022",
        "target": "ES2022",
        "moduleResolution": "node",
        "strict": false,
        "declaration": true,
        "outDir": "dist",
        "removeComments": true,
        "allowJs": true,
        "esModuleInterop": true,
        "resolveJsonModule": true
      }
    }
    ```

### ステップ2. 環境を設定する {#step-2-set-the-environment}

1.  TiDB Cloud Starterインスタンスの概要ページで、右上隅の**「接続」**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

2.  ローカル環境で環境変数`DATABASE_URL`を設定してください。例えば、Linux または macOS では、次のコマンドを実行できます。

    ```bash
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### ステップ3. Kyselyを使用してデータをクエリする {#step-3-use-kysely-to-query-data}

1.  TiDB Cloud Starterインスタンスにテーブルを作成し、データを挿入してください。

    [TiDB CloudコンソールのSQLエディタ](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query)使用してSQLステートメントを実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`person`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NULL DEFAULT NULL,
      `gender` enum('male','female') NULL DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    );

    insert into test.person values (1,'pingcap','male')
    ```

2.  プロジェクトのルートディレクトリに、 `hello-world.ts`という名前のファイルを作成し、以下のコードを追加してください。

    ```ts
    import { Kysely,GeneratedAlways,Selectable } from 'kysely'
    import { TiDBServerlessDialect } from '@tidbcloud/kysely'

    // Types
    interface Database {
      person: PersonTable
    }

    interface PersonTable {
      id: GeneratedAlways<number>
      name: string
      gender: "male" | "female"
    }

    // Dialect
    const db = new Kysely<Database>({
      dialect: new TiDBServerlessDialect({
        url: process.env.DATABASE_URL
      }),
    })

    // Simple Querying
    type Person = Selectable<PersonTable>
    export async function findPeople(criteria: Partial<Person> = {}) {
      let query = db.selectFrom('person')

      if (criteria.name){
        query = query.where('name', '=', criteria.name)
      }

      return await query.selectAll().execute()
    }

    console.log(await findPeople())
    ```

### ステップ4．TypeScriptコードを実行する {#step-4-run-the-typescript-code}

1.  TypeScript を JavaScript に変換するには`ts-node`をインストールし、次に Node.js 用の TypeScript 型定義を提供するには`@types/node`をインストールします。

        npm install -g ts-node
        npm i --save-dev @types/node

2.  以下のコマンドでTypeScriptコードを実行してください。

        ts-node --esm hello-world.ts

## エッジ環境では、 TiDB Cloud Kysely 方言を使用する {#use-tidb-cloud-kysely-dialect-in-edge-environments}

このセクションでは、Vercel Edge Function のTiDB Cloud Kysely 方言を例として取り上げます。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、以下のものが必要です。

-   エッジ環境を提供する[ヴェルセル](https://vercel.com/docs)アカウント。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  Vercel CLIをインストールしてください。

        npm i -g vercel@latest

2.  以下のターミナルコマンドを使用して`kysely-example`という名前の[Next.js](https://nextjs.org/)プロジェクトを作成します。

        npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
        cd kysely-example

3.  `kysely` 、 `@tidbcloud/kysely` 、および`@tidbcloud/serverless`パッケージをインストールしてください。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

### ステップ2. 環境を設定する {#step-2-set-the-environment}

TiDB Cloud Starterインスタンスの概要ページで、右上隅の**「接続」**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

    mysql://[username]:[password]@[host]/[database]

### ステップ3. エッジ関数を作成する {#step-3-create-an-edge-function}

1.  TiDB Cloud Starterインスタンスにテーブルを作成し、データを挿入してください。

    [TiDB CloudコンソールのSQLエディタ](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query)使用してSQL文を実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`person`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NULL DEFAULT NULL,
      `gender` enum('male','female') NULL DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    );

    insert into test.person values (1,'pingcap','male')
    ```

2.  プロジェクトの`app`ディレクトリに、 `/api/edge-function-example/route.ts`ファイルを作成し、以下のコードを追加します。

    ```ts
    import { NextResponse } from 'next/server';
    import type { NextRequest } from 'next/server';
    import { Kysely,GeneratedAlways,Selectable } from 'kysely'
    import { TiDBServerlessDialect } from '@tidbcloud/kysely'

    export const runtime = 'edge';

    // Types
    interface Database {
      person: PersonTable
    }

    interface PersonTable {
      id: GeneratedAlways<number>
      name: string
      gender: "male" | "female" | "other"
    }

    // Dialect
    const db = new Kysely<Database>({
      dialect: new TiDBServerlessDialect({
        url: process.env.DATABASE_URL
      }),
    })

    // Query
    type Person = Selectable<PersonTable>
    async function findPeople(criteria: Partial<Person> = {}) {
      let query = db.selectFrom('person')

      if (criteria.name){
        query = query.where('name', '=', criteria.name)
      }

      return await query.selectAll().execute()
    }

    export async function GET(request: NextRequest) {

      const searchParams = request.nextUrl.searchParams
      const query = searchParams.get('query')

      let response = null;
      if (query) {
        response = await findPeople({name: query})
      } else {
        response = await findPeople()
      }

      return NextResponse.json(response);
    }
    ```

    上記のコードは、クエリパラメータ`query`を受け取り、クエリの結果を返します。クエリパラメータが指定されていない場合は、 `person`テーブル内のすべてのレコードを返します。

3.  コードをローカル環境でテストしてください。

        export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
        next dev

4.  `http://localhost:3000/api/edge-function-example`に移動して、ルートからの応答を取得してください。

### ステップ4．Vercelにコードをデプロイ {#step-4-deploy-your-code-to-vercel}

1.  `DATABASE_URL`環境変数を使用して、Vercelにコードをデプロイ。

        vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod

    デプロイが完了すると、プロジェクトのURLが発行されます。

2.  `${Your-URL}/api/edge-function-example`ページに移動して、ルートからの応答を取得してください。

## 次は？ {#what-s-next}

-   [キセリー](https://kysely.dev/docs/intro)と[@tidbcloud/kysely](https://github.com/tidbcloud/kysely)についてもっと詳しく知りたい方はこちらをご覧ください。
-   [TiDB CloudとVercelを統合する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-vercel)方法を学ぶ
