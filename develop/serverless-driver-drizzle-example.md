---
title: TiDB Cloud Serverless Driver Drizzle Tutorial
summary: Drizzle でTiDB Cloudサーバーレス ドライバーを使用する方法を学びます。
aliases: ['/tidbcloud/serverless-driver-drizzle-example/']
---

# TiDB CloudサーバーレスDriverDrizzle チュートリアル {#tidb-cloud-serverless-driver-drizzle-tutorial}

[霧雨ORM](https://orm.drizzle.team/) 、開発者エクスペリエンス`drizzle-orm@0.31.2`重視した軽量で高性能な TypeScript ORM です。2 以降では[drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)サポートし、 [TiDB Cloudサーバーレス ドライバー](/develop/serverless-driver.md)では HTTPS 経由で Drizzle を利用できるようになります。

このチュートリアルでは、Node.js 環境およびエッジ環境で Drizzle とTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

> **ヒント：**
>
> このドキュメントの手順は、 TiDB Cloud Starter クラスターに加えて、 TiDB Cloud Essential クラスターでも機能します。

## Node.js環境でDrizzleとTiDB Cloudサーバーレスドライバーを使用する {#use-drizzle-and-tidb-cloud-serverless-driver-in-node-js-environments}

このセクションでは、Node.js 環境で Drizzle とTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Starter クラスター。まだお持ちでない場合は、 [TiDB Cloud Starterクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)実行できます。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `drizzle-node-example`という名前のプロジェクトを作成します。

    ```shell
    mkdir drizzle-node-example
    cd drizzle-node-example
    ```

2.  `drizzle-orm`と`@tidbcloud/serverless`パッケージをインストールします。

    ```shell
    npm install drizzle-orm @tidbcloud/serverless
    ```

3.  プロジェクトのルート ディレクトリで、 `package.json`ファイルを見つけ、ファイルに`"type": "module"`追加して ES モジュールを指定します。

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.1.1",
        "drizzle-orm": "^0.31.2"
      }
    }
    ```

4.  プロジェクトのルートディレクトリに、TypeScriptコンパイラオプションを定義するファイル`tsconfig.json`を追加します。以下にサンプルファイルを示します。

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

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter クラスターの名前をクリックして、その概要ページに移動します。

2.  概要ページで、右上隅の**[接続]**をクリックし、 **[接続**先] ドロップダウン リストで`Serverless Driver`を選択して、[**パスワードの生成] をクリックし、ランダム パスワード**を作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

    接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

3.  ローカル環境で環境変数`DATABASE_URL`を設定します。例えば、LinuxまたはmacOSでは、次のコマンドを実行できます。

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    ```

### ステップ3. Drizzleを使用してデータをクエリする {#step-3-use-drizzle-to-query-data}

1.  TiDB Cloud Starter クラスターにテーブルを作成します。

    [TiDB Cloudコンソールの SQL エディター](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query)使用するとSQL文を実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`users` (
     `id` BIGINT PRIMARY KEY auto_increment,
     `full_name` TEXT,
     `phone` VARCHAR(256)
    );
    ```

2.  プロジェクトのルート ディレクトリに`hello-world.ts`という名前のファイルを作成し、次のコードを追加します。

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

### ステップ4. Typescriptコードを実行する {#step-4-run-the-typescript-code}

1.  `ts-node`インストールして TypeScript を JavaScript に変換し、次に`@types/node`インストールして Node.js に TypeScript 型定義を提供します。

    ```shell
    npm install -g ts-node
    npm i --save-dev @types/node
    ```

2.  次のコマンドで Typescript コードを実行します。

    ```shell
    ts-node --esm hello-world.ts
    ```

## エッジ環境で Drizzle とTiDB Cloudサーバーレス ドライバーを使用する {#use-drizzle-and-tidb-cloud-serverless-driver-in-edge-environments}

このセクションでは、Vercel Edge Function を例に説明します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   エッジ環境を提供する[ヴェルセル](https://vercel.com/docs)アカウント。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Starter クラスター。まだお持ちでない場合は、 [TiDB Cloud Starterクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)実行できます。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  Vercel CLI をインストールします。

    ```shell
    npm i -g vercel@latest
    ```

2.  次のターミナル コマンドを使用して、 `drizzle-example`という[ネクスト.js](https://nextjs.org/)プロジェクトを作成します。

    ```shell
    npx create-next-app@latest drizzle-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
    ```

3.  `drizzle-example`ディレクトリに移動します。

    ```shell
    cd drizzle-example
    ```

4.  `drizzle-orm`と`@tidbcloud/serverless`パッケージをインストールします。

    ```shell
    npm install drizzle-orm @tidbcloud/serverless --force
    ```

### ステップ2. 環境を設定する {#step-2-set-the-environment}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットのTiDB Cloud Starter クラスターの名前をクリックして、その概要ページに移動します。

2.  概要ページで、右上隅の**[接続]**をクリックし、 **[接続**先] ドロップダウン リストで`Serverless Driver`を選択して、[**パスワードの生成] をクリックし、ランダム パスワード**を作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

    接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

### ステップ3. エッジ関数を作成する {#step-3-create-an-edge-function}

1.  TiDB Cloud Starter クラスターにテーブルを作成します。

    [TiDB Cloudコンソールの SQL エディター](https://docs.pingcap.com/tidbcloud/explore-data-with-chat2query.md)使用するとSQL文を実行できます。以下に例を示します。

    ```sql
    CREATE TABLE `test`.`users` (
     `id` BIGINT PRIMARY KEY auto_increment,
     `full_name` TEXT,
     `phone` VARCHAR(256)
    );
    ```

2.  プロジェクトの`app`ディレクトリにファイル`/api/edge-function-example/route.ts`を作成し、次のコードを追加します。

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

3.  コードをローカルでテストします。

    ```shell
    export DATABASE_URL='mysql://[username]:[password]@[host]/[database]'
    next dev
    ```

4.  ルートからの応答を取得するには、 `http://localhost:3000/api/edge-function-example`に移動します。

### ステップ4. コードをVercelにデプロイ {#step-4-deploy-your-code-to-vercel}

1.  `DATABASE_URL`環境変数を使用してコードを Vercel にデプロイ。

    ```shell
    vercel -e DATABASE_URL='mysql://[username]:[password]@[host]/[database]' --prod
    ```

    デプロイが完了すると、プロジェクトの URL が取得されます。

2.  ルートからの応答を取得するには、 `${Your-URL}/api/edge-function-example`ページに移動します。

## 次は何？ {#what-s-next}

-   [霧雨](https://orm.drizzle.team/docs/overview)と[drizzle-orm/tidb-serverless](https://orm.drizzle.team/docs/get-started-mysql#tidb-serverless)について詳しく説明します。
-   [TiDB CloudとVercelを統合する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-vercel)方法を学習します。
