---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: Kysely でTiDB Cloudサーバーレス ドライバーを使用する方法を学びます。
---

# TiDB CloudサーバーレスDriverKysely チュートリアル {#tidb-cloud-serverless-driver-kysely-tutorial}

[キセリ](https://kysely.dev/docs/intro) 、型安全で自動補完対応の TypeScript SQL クエリ ビルダーです。TiDB TiDB Cloud は[翻訳:](https://github.com/tidbcloud/kysely)提供し、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)を使用して HTTPS 経由で Kysely を使用できます。従来の TCP 方式と比較して、 [翻訳:](https://github.com/tidbcloud/kysely)は次の利点があります。

-   サーバーレス環境でのパフォーマンスが向上します。
-   エッジ環境で Kysely を使用する機能。

このチュートリアルでは、Node.js 環境とエッジ環境で Kysely とTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

## Node.js環境でTiDB Cloud Kysely方言を使用する {#use-tidb-cloud-kysely-dialect-in-node-js-environments}

このセクションでは、Node.js 環境で Kysely とTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Serverless クラスター。ない場合は、 [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)使用できます。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `kysely-node-example`という名前のプロジェクトを作成します。

        mkdir kysely-node-example
        cd kysely-node-example

2.  `kysely`パッケージ`@tidbcloud/kysely` `@tidbcloud/serverless`します。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

3.  プロジェクトのルート ディレクトリで、 `package.json`ファイルを見つけ、ファイルに`"type": "module"`追加して ES モジュールを指定します。

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

4.  プロジェクトのルート ディレクトリに、TypeScript コンパイラ オプションを定義する`tsconfig.json`ファイルを追加します。次にサンプル ファイルを示します。

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

1.  TiDB Cloud Serverless クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されるダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

2.  ローカル環境で環境変数`DATABASE_URL`設定します。たとえば、Linux または macOS では、次のコマンドを実行できます。

    ```bash
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### ステップ3. Kyselyを使用してデータをクエリする {#step-3-use-kysely-to-query-data}

1.  TiDB Cloud Serverless クラスターにテーブルを作成し、データを挿入します。

    [TiDB Cloudコンソールの SQL エディター](/tidb-cloud/explore-data-with-chat2query.md)使用して SQL ステートメントを実行できます。次に例を示します。

    ```sql
    CREATE TABLE `test`.`person`  (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(255) NULL DEFAULT NULL,
      `gender` enum('male','female') NULL DEFAULT NULL,
      PRIMARY KEY (`id`) USING BTREE
    );

    insert into test.person values (1,'pingcap','male')
    ```

2.  プロジェクトのルート ディレクトリに`hello-world.ts`という名前のファイルを作成し、次のコードを追加します。

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

### ステップ4. Typescriptコードを実行する {#step-4-run-the-typescript-code}

1.  `ts-node`インストールして TypeScript を JavaScript に変換し、次に`@types/node`インストールして Node.js に TypeScript 型定義を提供します。

        npm install -g ts-node
        npm i --save-dev @types/node

2.  次のコマンドで Typescript コードを実行します。

        ts-node --esm hello-world.ts

## エッジ環境でTiDB Cloud Kysely 方言を使用する {#use-tidb-cloud-kysely-dialect-in-edge-environments}

このセクションでは、Vercel Edge Function のTiDB Cloud Kysely 方言を例に説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   エッジ環境を提供する[ヴェルセル](https://vercel.com/docs)アカウント。
-   [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Serverless クラスター。ない場合は、 [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)使用できます。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  Vercel CLI をインストールします。

        npm i -g vercel@latest

2.  次のターミナル コマンドを使用して、 `kysely-example`という[次](https://nextjs.org/)プロジェクトを作成します。

        npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
        cd kysely-example

3.  `kysely`パッケージ`@tidbcloud/kysely` `@tidbcloud/serverless`します。

        npm install kysely @tidbcloud/kysely @tidbcloud/serverless

### ステップ2. 環境を設定する {#step-2-set-the-environment}

TiDB Cloud Serverless クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されるダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

    mysql://[username]:[password]@[host]/[database]

### ステップ3. エッジ関数を作成する {#step-3-create-an-edge-function}

1.  TiDB Cloud Serverless クラスターにテーブルを作成し、データを挿入します。

    [TiDB Cloudコンソールの SQL エディター](/tidb-cloud/explore-data-with-chat2query.md)使用して SQL ステートメントを実行できます。次に例を示します。

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

    上記のコードはクエリ パラメータ`query`を受け入れ、クエリの結果を返します。クエリ パラメータが指定されていない場合は、テーブル`person`内のすべてのレコードを返します。

3.  コードをローカルでテストします。

        export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
        next dev

4.  ルートからの応答を取得するには、 `http://localhost:3000/api/edge-function-example`に移動します。

### ステップ4. コードをVercelにデプロイ {#step-4-deploy-your-code-to-vercel}

1.  `DATABASE_URL`環境変数を使用してコードを Vercel にデプロイ。

        vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod

    デプロイが完了すると、プロジェクトの URL が取得されます。

2.  ルートからの応答を取得するには、 `${Your-URL}/api/edge-function-example`ページに移動します。

## 次は何か {#what-s-next}

-   [キセリ](https://kysely.dev/docs/intro)と[翻訳:](https://github.com/tidbcloud/kysely)について詳しく見る
-   方法を学ぶ[TiDB CloudとVercelを統合する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)
