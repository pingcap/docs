---
title: TiDB Cloud Serverless Driver Drizzle Tutorial
summary: TiDB CloudサーバーレスドライバーをDrizzleで使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-driver-drizzle-example/']
---

# TiDB Cloud Serverless Driver Drizzle チュートリアル {#tidb-cloud-serverless-driver-drizzle-tutorial}

[Drizzle ORM](https://orm.drizzle.team/) 、開発者エクスペリエンスを念頭に置いた軽量で高性能な TypeScript ORM です。 `drizzle-orm@0.31.2`以降、 [drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)をサポートしており、 [TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md).

このチュートリアルでは、Node.js環境およびエッジ環境でDrizzleとTiDB Cloudサーバーレスドライバーを使用する方法について説明します。

> **ヒント：**
>
> このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。

## Node.js環境でDrizzleとTiDB Cloudのサーバーレスドライバーを使用する {#use-drizzle-and-tidb-cloud-serverless-driver-in-node-js-environments}

このセクションでは、Node.js環境でDrizzleとTiDB Cloudサーバーレスドライバーを連携させる方法について説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、以下のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `drizzle-node-example`という名前のプロジェクトを作成します。

    ```shell
    mkdir drizzle-node-example
    cd drizzle-node-example
    ```

2.  `drizzle-orm`および`@tidbcloud/serverless`パッケージをインストールしてください。

    ```shell
    npm install drizzle-orm @tidbcloud/serverless
    ```

3.  プロジェクトのルートディレクトリで、 `package.json`ファイルを探し、そのファイルに`"type": "module"`を追加して ES モジュールを指定します。

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.1.1",
        "drizzle-orm": "^0.31.2"
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

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Starterインスタンスの名前をクリックして、その概要ページに移動します。

2.  概要ページで、右上隅の**「接続」**をクリックし、 **「接続先」**ドロップダウンリストから`Serverless Driver`を選択してから、 **「パスワードを生成」をクリックしてランダムなパスワード**を作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

    接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

3.  ローカル環境で環境変数`DATABASE_URL`を設定してください。例えば、Linux または macOS では、次のコマンドを実行できます。

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### ステップ3. Drizzleを使用してデータをクエリする {#step-3-use-drizzle-to-query-data}

1.  TiDB Cloud Starterインスタンスにテーブルを作成します。

    [TiDB CloudコンソールのSQLエディタ](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query)使用してSQL文を実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`users` (
     `id` BIGINT PRIMARY KEY auto_increment,
     `full_name` TEXT,
     `phone` VARCHAR(256)
    );
    ```

2.  プロジェクトのルートディレクトリに、 `hello-world.ts`という名前のファイルを作成し、以下のコードを追加してください。

    ```ts
    import { connect } from '@tidbcloud/serverless';
    import { drizzle } from 'drizzle-orm/tidb-serverless';
    import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';

    // Initialize
    const client = connect({ url: process.env.DATABASE_URL });
    const db = drizzle(client);

    // Define schema
    export const users = mysqlTable('users', {
      id: serial("id").primaryKey(),
      fullName: text('full_name'),
      phone: varchar('phone', { length: 256 }),
    });
    export type User = typeof users.$inferSelect; // return type when queried
    export type NewUser = typeof users.$inferInsert; // insert type

    // Insert and select data
    const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
    await db.insert(users).values(user)
    const result: User[] = await db.select().from(users);
    console.log(result);
    ```

### ステップ4．TypeScriptコードを実行する {#step-4-run-the-typescript-code}

1.  TypeScript を JavaScript に変換するには`ts-node`をインストールし、次に Node.js 用の TypeScript 型定義を提供するには`@types/node`をインストールします。

    ```shell
    npm install -g ts-node
    npm i --save-dev @types/node
    ```

2.  以下のコマンドでTypeScriptコードを実行してください。

    ```shell
    ts-node --esm hello-world.ts
    ```

## エッジ環境でDrizzleとTiDB Cloudのサーバーレスドライバーを使用する {#use-drizzle-and-tidb-cloud-serverless-driver-in-edge-environments}

このセクションでは、Vercel Edge関数を例として取り上げます。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、以下のものが必要です。

-   エッジ環境を提供する[ヴェルセル](https://vercel.com/docs)アカウント。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  Vercel CLIをインストールしてください。

    ```shell
    npm i -g vercel@latest
    ```

2.  以下のターミナルコマンドを使用して`drizzle-example`という名前の[Next.js](https://nextjs.org/)プロジェクトを作成します。

    ```shell
    npx create-next-app@latest drizzle-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
    ```

3.  `drizzle-example`ディレクトリに移動してください。

    ```shell
    cd drizzle-example
    ```

4.  `drizzle-orm`および`@tidbcloud/serverless`パッケージをインストールしてください。

    ```shell
    npm install drizzle-orm @tidbcloud/serverless --force
    ```

### ステップ2. 環境を設定する {#step-2-set-the-environment}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Starterインスタンスの名前をクリックして、その概要ページに移動します。

2.  概要ページで、右上隅の**「接続」**をクリックし、 **「接続先」**ドロップダウンリストから`Serverless Driver`を選択してから、 **「パスワードを生成」をクリックしてランダムなパスワード**を作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

    接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

### ステップ3. エッジ関数を作成する {#step-3-create-an-edge-function}

1.  TiDB Cloud Starterインスタンスにテーブルを作成します。

    [TiDB CloudコンソールのSQLエディタ](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query.md)使用してSQL文を実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`users` (
     `id` BIGINT PRIMARY KEY auto_increment,
     `full_name` TEXT,
     `phone` VARCHAR(256)
    );
    ```

2.  プロジェクトの`app`ディレクトリに、 `/api/edge-function-example/route.ts`ファイルを作成し、以下のコードを追加します。

    ```ts
    import { NextResponse } from 'next/server';
    import type { NextRequest } from 'next/server';
    import { connect } from '@tidbcloud/serverless';
    import { drizzle } from 'drizzle-orm/tidb-serverless';
    import { mysqlTable, serial, text, varchar } from 'drizzle-orm/mysql-core';
    export const runtime = 'edge';

    // Initialize
    const client = connect({ url: process.env.DATABASE_URL });
    const db = drizzle(client);

    // Define schema
    export const users = mysqlTable('users', {
      id: serial("id").primaryKey(),
      fullName: text('full_name'),
      phone: varchar('phone', { length: 256 }),
    });
    export type User = typeof users.$inferSelect; // return type when queried
    export type NewUser = typeof users.$inferInsert; // insert type

    export async function GET(request: NextRequest) {
      // Insert and select data
      const user: NewUser = { fullName: 'John Doe', phone: '123-456-7890' };
      await db.insert(users).values(user)
      const result: User[] = await db.select().from(users);
      return NextResponse.json(result);
    }
    ```

3.  コードをローカル環境でテストしてください。

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    next dev
    ```

4.  `http://localhost:3000/api/edge-function-example`に移動して、ルートからの応答を取得してください。

### ステップ4．Vercelにコードをデプロイ {#step-4-deploy-your-code-to-vercel}

1.  `DATABASE_URL`環境変数を使用して、Vercelにコードをデプロイ。

    ```shell
    vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod
    ```

    デプロイが完了すると、プロジェクトのURLが発行されます。

2.  `${Your-URL}/api/edge-function-example`ページに移動して、ルートからの応答を取得してください。

## 次は？ {#what-s-next}

-   [霧雨](https://orm.drizzle.team/docs/overview)と[drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)について詳しくはこちらをご覧ください。
-   [TiDB CloudとVercelを統合する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-vercel)方法を学びましょう。
