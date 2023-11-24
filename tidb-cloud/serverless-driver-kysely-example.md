---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Kysely.
---

# TiDB CloudサーバーレスDriverKysely チュートリアル {#tidb-cloud-serverless-driver-kysely-tutorial}

[キセリー](https://kysely.dev/docs/intro)は、タイプ セーフでオートコンプリートに適した TypeScript SQL クエリ ビルダーです。 TiDB Cloudは[@tidbcloud/kysely](https://github.com/tidbcloud/kysely)を提供し、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)で HTTPS 経由で Kysely を使用できるようにします。従来の TCP 方式と比較して、 [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)には次の利点があります。

-   サーバーレス環境でのパフォーマンスの向上。
-   エッジ環境で Kysely を使用する機能。

このチュートリアルでは、Node.js 環境およびエッジ環境でTiDB Cloudサーバーレス ドライバーを Kysely とともに使用する方法について説明します。

## Node.js 環境でTiDB Cloud Kysely 言語を使用する {#use-tidb-cloud-kysely-dialect-in-node-js-environments}

このセクションでは、Node.js 環境でTiDB Cloudサーバーレス ドライバーを Kysely で使用する方法について説明します。

### あなたが始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)または好みのパッケージ マネージャー。
-   TiDB サーバーレス クラスター。何も持っていない場合は、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)を実行できます。

### ステップ 1. プロジェクトを作成する {#step-1-create-a-project}

1.  `kysely-node-example`という名前のプロジェクトを作成します。

        mkdir kysely-node-example
        cd kysely-node-example

2.  `kysely` 、 `@tidbcloud/kysely` 、および`@tidbcloud/serverless`パッケージをインストールします。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

3.  プロジェクトのルート ディレクトリで`package.json`ファイルを見つけ、そのファイルに`type: "module"`追加して ES モジュールを指定します。

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

4.  プロジェクトのルート ディレクトリに、TypeScript コンパイラ オプションを定義する`tsconfig.json`ファイルを追加します。ファイルの例を次に示します。

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

### ステップ 2. 環境を設定する {#step-2-set-the-environment}

1.  TiDB サーバーレス クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

2.  ローカル環境で環境変数`DATABASE_URL`を設定します。たとえば、Linux または macOS では、次のコマンドを実行できます。

    ```bash
    export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
    ```

### ステップ 3. Kysely を使用してデータをクエリする {#step-3-use-kysely-to-query-data}

1.  TiDB サーバーレス クラスターにテーブルを作成し、データを挿入します。

    [TiDB Cloudコンソールの Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)を使用すると SQL ステートメントを実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`person`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NULL DEFAULT NULL,
      `gender` enum('male','female') NULL DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    );

    insert into test.person values (1,'pingcap','male')
    ```

2.  プロジェクトのルート ディレクトリに`hello-word.ts`という名前のファイルを作成し、次のコードを追加します。

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

### ステップ 4. Typescript コードを実行する {#step-4-run-the-typescript-code}

1.  `ts-node`をインストールして TypeScript を JavaScript に変換し、次に`@types/node`をインストールして Node.js の TypeScript 型定義を提供します。

        npm install -g ts-node
        npm i --save-dev @types/node

2.  次のコマンドを使用して Typescript コードを実行します。

        ts-node --esm hello-world.ts

## エッジ環境でTiDB Cloud Kysely 言語を使用する {#use-tidb-cloud-kysely-dialect-in-edge-environments}

このセクションでは、Vercel Edge Function のTiDB Cloud Kysely 言語を例として取り上げます。

### あなたが始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   エッジ環境を提供する[ヴェルセル](https://vercel.com/docs)アカウント。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)または好みのパッケージ マネージャー。
-   TiDB サーバーレス クラスター。何も持っていない場合は、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)を実行できます。

### ステップ 1. プロジェクトを作成する {#step-1-create-a-project}

1.  Vercel CLI をインストールします。

        npm i -g vercel@latest

2.  次のターミナル コマンドを使用して、 `kysely-example`という名前の[Next.js](https://nextjs.org/)プロジェクトを作成します。

        npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
        cd kysely-example

3.  `kysely` 、 `@tidbcloud/kysely` 、および`@tidbcloud/serverless`パッケージをインストールします。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

### ステップ 2. 環境を設定する {#step-2-set-the-environment}

TiDB サーバーレス クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

    mysql://[username]:[password]@[host]/[database]

### ステップ 3. エッジ関数を作成する {#step-3-create-an-edge-function}

1.  TiDB サーバーレス クラスターにテーブルを作成し、データを挿入します。

    [TiDB Cloudコンソールの Chat2Query](/tidb-cloud/explore-data-with-chat2query.md)を使用すると SQL ステートメントを実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`person`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NULL DEFAULT NULL,
      `gender` enum('male','female') NULL DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    );

    insert into test.person values (1,'pingcap','male')
    ```

2.  プロジェクトの`app`ディレクトリにファイル`/api/edge-function-example/route.ts`を作成し、次のコードを追加します。

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

    前述のコードはクエリ パラメータ`query`を受け入れ、クエリの結果を返します。クエリ パラメータが指定されていない場合は、テーブル`person`内のすべてのレコードが返されます。

3.  コードをローカルでテストします。

        export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
        next dev

4.  `http://localhost:3000/api/edge-function-example`に移動して、ルートからの応答を取得します。

### ステップ 4. コードを Vercel にデプロイ {#step-4-deploy-your-code-to-vercel}

1.  `DATABASE_URL`環境変数を使用してコードを Vercel にデプロイ。

        vercel -e DATABASE_URL=mysql://[username]:[password]@[host]/[database] --prod

    デプロイメントが完了すると、プロジェクトの URL が取得されます。

2.  `${Your-URL}/api/edge-function-example`ページに移動して、ルートからの応答を取得します。

## 次は何ですか {#what-s-next}

-   [キセリー](https://kysely.dev/docs/intro)と[@tidbcloud/kysely](https://github.com/tidbcloud/kysely)について詳しく見る
-   方法を学ぶ[TiDB Cloudと Vercel を統合する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)
