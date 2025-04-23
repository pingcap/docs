---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: Prisma ORM でTiDB Cloudサーバーレス ドライバーを使用する方法を学習します。
---

# TiDB CloudサーバーレスDriverPrisma チュートリアル {#tidb-cloud-serverless-driver-prisma-tutorial}

[プリズマ](https://www.prisma.io/docs)はオープンソースの次世代 ORM（オブジェクトリレーショナルマッピング）であり、開発者がデータベースを直感的、効率的、かつ安全に操作できるようにします。TiDB TiDB Cloud は[@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)提供し、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)で HTTPS 経由で[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)使用できます。従来の TCP 方式と比較して、 [@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)は以下の利点があります。

-   サーバーレス環境での Prisma クライアントのパフォーマンスが向上
-   エッジ環境で Prisma Client を使用する機能

このチュートリアルでは、サーバーレス環境とエッジ環境で[@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)使用する方法について説明します。

## インストール {#install}

[@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)と[TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)両方をインストールする必要があります。5 またはお好みのパッケージマネージャーを使用し[npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)インストールできます。

npm を例にとると、インストールには次のコマンドを実行できます。

```shell
npm install @tidbcloud/prisma-adapter
npm install @tidbcloud/serverless
```

## <code>driverAdapters</code>を有効にする {#enable-code-driveradapters-code}

Prismaアダプタを使用するには、 `schema.prisma`ファイルの`driverAdapters`機能を有効にする必要があります。例：

```prisma
generator client {
  provider        = "prisma-client-js"
  previewFeatures = ["driverAdapters"]
}

datasource db {
  provider     = "mysql"
  url          = env("DATABASE_URL")
}
```

## Prismaクライアントを初期化する {#initialize-prisma-client}

Prisma Client を使用する前に、 `@tidbcloud/prisma-adapter`で初期化する必要があります。

v6.6.0 より前のバージョン`@tidbcloud/prisma-adapter`場合:

```js
import { connect } from '@tidbcloud/serverless';
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const connection = connect({ url: ${DATABASE_URL} });
const adapter = new PrismaTiDBCloud(connection);
const prisma = new PrismaClient({ adapter });
```

`@tidbcloud/prisma-adapter` v6.6.0 以降のバージョンの場合:

```js
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const adapter = new PrismaTiDBCloud({ url: ${DATABASE_URL} });
const prisma = new PrismaClient({ adapter });
```

その後、Prisma Client からのクエリをTiDB Cloudサーバーレス ドライバーに送信して処理することができます。

## Node.js環境でPrismaアダプターを使用する {#use-the-prisma-adapter-in-node-js-environments}

このセクションでは、Node.js 環境で`@tidbcloud/prisma-adapter`使用する方法の例を示します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Serverless クラスター。お持ちでない場合は、 [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)ご利用ください。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `prisma-example`という名前のプロジェクトを作成します。

        mkdir prisma-example
        cd prisma-example

2.  `@tidbcloud/prisma-adapter`ドライバー アダプター、 `@tidbcloud/serverless`サーバーレス ドライバー、および Prisma CLI をインストールします。

    以下のコマンドはパッケージマネージャーとしてnpmを使用します。1 `npm install @tidbcloud/serverless`実行すると、プロジェクトディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/prisma-adapter
        npm install @tidbcloud/serverless
        npm install prisma --save-dev

3.  `package.json`ファイルで、 `type: "module"`を追加して ES モジュールを指定します。

    ```json
    {
      "type": "module",
      "dependencies": {
        "@prisma/client": "^6.6.0",
        "@tidbcloud/prisma-adapter": "^6.6.0",
        "@tidbcloud/serverless": "^0.1.0"
      },
      "devDependencies": {
        "prisma": "^6.6.0"
      }
    }
    ```

### ステップ2. 環境を設定する {#step-2-set-the-environment}

1.  TiDB Cloud Serverlessクラスターの概要ページで、右上隅の**「接続」**をクリックし、表示されるダイアログからデータベースの接続文字列を取得します。接続文字列は以下のようになります。

        mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict

2.  プロジェクトのルート ディレクトリに`.env`という名前のファイルを作成し、次のように`DATABASE_URL`名前の環境変数を定義して、この変数内のプレースホルダー`[]`接続文字列内の対応するパラメーターに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict'
    ```

    > **注記：**
    >
    > `@tidbcloud/prisma-adapter` HTTPS 経由の Prisma Client の使用のみをサポートします。2 と[プリズママイグレーション](https://www.prisma.io/docs/concepts/components/prisma-migrate) [プリズマイントロスペクション](https://www.prisma.io/docs/concepts/components/introspection) 、従来の TCP 接続が引き続き使用されます。Prisma Client のみを使用する必要がある場合は、 `DATABASE_URL` `mysql://[username]:[password]@[host]/[database]`形式に簡略化できます。

3.  `.env`ファイルから環境変数を読み込むには`dotenv`インストールします。

        npm install dotenv

### ステップ3. スキーマを定義する {#step-3-define-your-schema}

1.  `schema.prisma`という名前のファイルを作成します。このファイルには、 `driverAdapters`プレビュー機能を組み込み、 `DATABASE_URL`環境変数を参照します。以下にファイルの例を示します。

        // schema.prisma
        generator client {
          provider        = "prisma-client-js"
          previewFeatures = ["driverAdapters"]
        }

        datasource db {
          provider     = "mysql"
          url          = env("DATABASE_URL")
        } 

2.  `schema.prisma`ファイルで、データベーステーブルのデータモデルを定義します。次の例では、 `user`名前のデータモデルが定義されています。

        // schema.prisma
        generator client {
          provider        = "prisma-client-js"
          previewFeatures = ["driverAdapters"]
        }

        datasource db {
          provider     = "mysql"
          url          = env("DATABASE_URL")
        } 

        // define a data model according to your database table
        model user {
          id    Int     @id @default(autoincrement())
          email String? @unique(map: "uniq_email") @db.VarChar(255)
          name  String? @db.VarChar(255)
        }

3.  データベースをPrismaスキーマと同期します。TiDB TiDB Cloud Serverlessクラスターにデータベーステーブルを手動で作成するか、Prisma CLIを使用して以下の手順で自動的に作成することもできます。

        npx prisma db push

    このコマンドは、 `@tidbcloud/prisma-adapter`使用したHTTPS接続ではなく、従来のTCP接続を介してTiDB Cloud Serverlessクラスターにテーブル`user`を作成します。これは、Prisma Migrateと同じエンジンを使用しているためです。このコマンドの詳細については、 [スキーマのプロトタイプを作成する](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)参照してください。

4.  Prisma クライアントを生成します:

        npx prisma generate

    このコマンドは、Prisma スキーマに基づいて Prisma クライアントを生成します。

### ステップ4. CRUD操作を実行する {#step-4-execute-crud-operations}

1.  `hello-word.js`という名前のファイルを作成し、次のコードを追加して Prisma Client を初期化します。

    ```js
    import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
    import { PrismaClient } from '@prisma/client';
    import dotenv from 'dotenv';

    // setup
    dotenv.config();
    const connectionString = `${process.env.DATABASE_URL}`;

    // Initialize Prisma Client
    const adapter = new PrismaTiDBCloud({ url: connectionString });
    const prisma = new PrismaClient({ adapter });
    ```

2.  Prisma ClientでCRUD操作を実行します。例:

    ```js
    // Insert
    const user = await prisma.user.create({
      data: {
        email: 'test@pingcap.com',
        name: 'test',
      },
    })
    console.log(user)

    // Query
    console.log(await prisma.user.findMany())

    // Delete
    await prisma.user.delete({
       where: {
          id: user.id,
       },
    })
    ```

3.  Prisma Clientでいくつかのトランザクション操作を実行します。例:

    ```js
    const createUser1 = prisma.user.create({
      data: {
        email: 'test1@pingcap.com',
        name: 'test1',
      },
    })
    const createUser2 = prisma.user.create({
      data: {
        email: 'test1@pingcap.com',
        name: 'test1',
      },
    })
    const createUser3 = prisma.user.create({
      data: {
        email: 'test2@pingcap.com',
        name: 'test2',
      },
    })

    try {
      await prisma.$transaction([createUser1, createUser2]) // Operations fail because the email address is duplicated
    } catch (e) {
      console.log(e)
    }

    try {
      await prisma.$transaction([createUser2, createUser3]) // Operations success because the email address is unique
    } catch (e) {
      console.log(e)
    }
    ```

## エッジ環境でPrismaアダプターを使用する {#use-the-prisma-adapter-in-edge-environments}

Vercel Edge FunctionsやCloudflare Workersなどのエッジ環境では、 `@tidbcloud/prisma-adapter` v5.11.0以降のバージョンをご利用いただけます。

-   [Vercel Edge Functionの例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-vercel-example)
-   [Cloudflare Workersの例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-cloudflare-worker-example)
