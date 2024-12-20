---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: Prisma ORM でTiDB Cloudサーバーレス ドライバーを使用する方法を学習します。
---

# TiDB CloudサーバーレスDriverPrisma チュートリアル {#tidb-cloud-serverless-driver-prisma-tutorial}

[プリズマ](https://www.prisma.io/docs)はオープンソースの次世代 ORM (オブジェクト リレーショナル マッピング) であり、開発者が直感的、効率的、かつ安全な方法でデータベースを操作できるようにします。TiDB TiDB Cloud は[@tidbcloud/プリズマアダプタ](https://github.com/tidbcloud/prisma-adapter)提供し、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)で HTTPS 経由で[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)使用できます。従来の TCP 方式と比較して、 [@tidbcloud/プリズマアダプタ](https://github.com/tidbcloud/prisma-adapter)は次の利点があります。

-   サーバーレス環境での Prisma Client のパフォーマンスが向上
-   エッジ環境で Prisma Client を使用する機能

このチュートリアルでは、サーバーレス環境とエッジ環境で[@tidbcloud/プリズマアダプタ](https://github.com/tidbcloud/prisma-adapter)使用する方法について説明します。

## インストール {#install}

[@tidbcloud/プリズマアダプタ](https://github.com/tidbcloud/prisma-adapter)と[TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)両方をインストールする必要があります。 [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用してインストールできます。

npm を例にとると、インストールには次のコマンドを実行できます。

```shell
npm install @tidbcloud/prisma-adapter
npm install @tidbcloud/serverless
```

## <code>driverAdapters</code>有効にする {#enable-code-driveradapters-code}

Prisma アダプターを使用するには、 `schema.prisma`ファイルの`driverAdapters`機能を有効にする必要があります。例:

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

Prisma Client を使用する前に、 `@tidbcloud/prisma-adapter`で初期化する必要があります。例:

```js
import { connect } from '@tidbcloud/serverless';
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const connection = connect({ url: ${DATABASE_URL} });
const adapter = new PrismaTiDBCloud(connection);
const prisma = new PrismaClient({ adapter });
```

その後、Prisma Client からのクエリをTiDB Cloudサーバーレス ドライバーに送信して処理することができます。

## Node.js環境でPrismaアダプターを使用する {#use-the-prisma-adapter-in-node-js-environments}

このセクションでは、Node.js 環境で`@tidbcloud/prisma-adapter`使用する方法の例を示します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Serverless クラスター。ない場合は、 [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)使用できます。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `prisma-example`という名前のプロジェクトを作成します。

        mkdir prisma-example
        cd prisma-example

2.  `@tidbcloud/prisma-adapter`ドライバー アダプター、 `@tidbcloud/serverless`サーバーレス ドライバー、および Prisma CLI をインストールします。

    次のコマンドは、パッケージ マネージャーとして npm を使用します。1 `npm install @tidbcloud/serverless`実行すると、プロジェクト ディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/prisma-adapter
        npm install @tidbcloud/serverless
        npm install prisma --save-dev

3.  `package.json`ファイルで、 `type: "module"`を追加して ES モジュールを指定します。

    ```json
    {
      "type": "module",
      "dependencies": {
        "@prisma/client": "^5.5.2",
        "@tidbcloud/prisma-adapter": "^5.5.2",
        "@tidbcloud/serverless": "^0.0.7"
      },
      "devDependencies": {
        "prisma": "^5.5.2"
      }
    }
    ```

### ステップ2. 環境を設定する {#step-2-set-the-environment}

1.  TiDB Cloud Serverless クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されるダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict

2.  プロジェクトのルート ディレクトリに`.env`という名前のファイルを作成し、次のように`DATABASE_URL`という名前の環境変数を定義して、この変数内のプレースホルダー`[]`接続文字列内の対応するパラメーターに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict'
    ```

    > **注記：**
    >
    > `@tidbcloud/prisma-adapter` HTTPS 経由の Prisma Client の使用のみをサポートします。 [プリズマ移行](https://www.prisma.io/docs/concepts/components/prisma-migrate)および[プリズマ イントロスペクション](https://www.prisma.io/docs/concepts/components/introspection)では、従来の TCP 接続が引き続き使用されます。 Prisma Client のみを使用する必要がある場合は、 `DATABASE_URL` `mysql://[username]:[password]@[host]/[database]`形式に簡略化できます。

3.  `.env`ファイルから環境変数を読み込むには`dotenv`インストールします。

        npm install dotenv

### ステップ3. スキーマを定義する {#step-3-define-your-schema}

1.  `schema.prisma`という名前のファイルを作成します。このファイルには、 `driverAdapters`プレビュー機能を含め、 `DATABASE_URL`環境変数を参照します。次にファイルの例を示します。

        // schema.prisma
        generator client {
          provider        = "prisma-client-js"
          previewFeatures = ["driverAdapters"]
        }

        datasource db {
          provider     = "mysql"
          url          = env("DATABASE_URL")
        } 

2.  `schema.prisma`ファイルで、データベース テーブルのデータ モデルを定義します。次の例では、 `user`という名前のデータ モデルが定義されています。

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

3.  データベースを Prisma スキーマと同期します。TiDB TiDB Cloud Serverless クラスターにデータベース テーブルを手動で作成することも、次のように Prisma CLI を使用して自動的に作成することもできます。

        npx prisma db push

    このコマンドは、 `@tidbcloud/prisma-adapter`使用した HTTPS 接続ではなく、従来の TCP 接続を介してTiDB Cloud Serverless クラスターに`user`テーブルを作成します。これは、Prisma Migrate と同じエンジンを使用するためです。このコマンドの詳細については、 [スキーマのプロトタイプを作成する](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)参照してください。

4.  Prisma クライアントを生成します:

        npx prisma generate

    このコマンドは、Prisma スキーマに基づいて Prisma クライアントを生成します。

### ステップ4. CRUD操作を実行する {#step-4-execute-crud-operations}

1.  `hello-word.js`という名前のファイルを作成し、次のコードを追加して Prisma Client を初期化します。

    ```js
    import { connect } from '@tidbcloud/serverless';
    import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
    import { PrismaClient } from '@prisma/client';
    import dotenv from 'dotenv';

    // setup
    dotenv.config();
    const connectionString = `${process.env.DATABASE_URL}`;

    // Initialize Prisma Client
    const connection = connect({ url: connectionString });
    const adapter = new PrismaTiDBCloud(connection);
    const prisma = new PrismaClient({ adapter });
    ```

2.  Prisma Client を使用していくつかの CRUD 操作を実行します。例:

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

3.  Prisma Client を使用していくつかのトランザクション操作を実行します。例:

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

Vercel Edge FunctionsやCloudflare Workersなどのエッジ環境では、 `@tidbcloud/prisma-adapter` v5.11.0以降のバージョンを使用できます。

-   [Vercel エッジ関数の例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-vercel-example)
-   [Cloudflare Workersの例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-cloudflare-worker-example)
