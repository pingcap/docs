---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: TiDB CloudサーバーレスドライバーをPrisma ORMで使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-driver-prisma-example/']
---

# TiDB Cloud Serverless Driver Prisma チュートリアル {#tidb-cloud-serverless-driver-prisma-tutorial}

[プリズマ](https://www.prisma.io/docs)開発者が直感的、効率的、安全な方法でデータベースを操作できるようにするオープンソースの次世代 ORM (オブジェクト リレーショナル マッピング) です。 TiDB Cloudは[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)を提供しており、 [TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md)で HTTPS 経由で[Prismaクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)使用できるようにします。従来の TCP 方法と比較して、[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)は次の利点があります。

-   サーバーレス環境におけるPrisma Clientのパフォーマンス向上
-   エッジ環境でPrisma Clientを使用できる機能

このチュートリアルでは、サーバーレス環境およびエッジ環境で[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)使用する方法について説明します。

> **ヒント：**
>
> このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。

## インストール {#install}

[@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter)と[TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md)の両方をインストールする必要があります。 [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)または好みのパッケージ マネージャーを使用してインストールできます。

npmを例にとると、インストールするには以下のコマンドを実行します。

```shell
npm install @tidbcloud/prisma-adapter
npm install @tidbcloud/serverless
```

## <code>driverAdapters</code>を有効にする {#enable-code-driveradapters-code}

Prismaアダプタを使用するには、 `driverAdapters`ファイルで`schema.prisma` }機能を有効にする必要があります。例：

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

## Prismaクライアントを初期化します {#initialize-prisma-client}

Prisma Clientを使用する前に、 `@tidbcloud/prisma-adapter`を使用して初期化する必要があります。

`@tidbcloud/prisma-adapter`バージョン6.6.0より前のバージョンの場合：

```js
import { connect } from '@tidbcloud/serverless';
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const connection = connect({ url: ${DATABASE_URL} });
const adapter = new PrismaTiDBCloud(connection);
const prisma = new PrismaClient({ adapter });
```

`@tidbcloud/prisma-adapter` v6.6.0以降のバージョンの場合：

```js
import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
import { PrismaClient } from '@prisma/client';

// Initialize Prisma Client
const adapter = new PrismaTiDBCloud({ url: ${DATABASE_URL} });
const prisma = new PrismaClient({ adapter });
```

その後、Prisma Clientからのクエリは、処理のためにTiDB Cloudのサーバーレスドライバに送信されます。

## Node.js環境でPrismaアダプターを使用する {#use-the-prisma-adapter-in-node-js-environments}

このセクションでは、Node.js 環境で`@tidbcloud/prisma-adapter`使用する方法の例を示します。

### 始める前に {#before-you-begin}

このチュートリアルを完了するには、以下のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

### ステップ1. プロジェクトを作成する {#step-1-create-a-project}

1.  `prisma-example`という名前のプロジェクトを作成します。

        mkdir prisma-example
        cd prisma-example

2.  `@tidbcloud/prisma-adapter`ドライバーアダプター、 `@tidbcloud/serverless`サーバーレスドライバー、および Prisma CLI をインストールします。

    以下のコマンドはパッケージマネージャーとしてnpmを使用します。 `npm install @tidbcloud/serverless`を実行すると、プロジェクトディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

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

1.  TiDB Cloud Starterインスタンスの概要ページで、右上隅の**「接続」**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict

2.  プロジェクトのルートディレクトリに、 `.env`という名前のファイルを作成し、次のように`DATABASE_URL`という名前の環境変数を定義し、この変数内のプレースホルダー`[]`を接続文字列内の対応するパラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict'
    ```

    > **注記：**
    >
    > `@tidbcloud/prisma-adapter` 、HTTPS 経由の Prisma クライアントの使用のみをサポートします。 [プリズマ・マイグレート](https://www.prisma.io/docs/concepts/components/prisma-migrate)およびプリズマ・イントロ[プリズマ・イントロスペクション](https://www.prisma.io/docs/concepts/components/introspection)では、従来の TCP 接続が引き続き使用されます。 Prisma Client のみを使用する必要がある場合は、 `DATABASE_URL`を`mysql://[username]:[password]@[host]/[database]`形式に簡素化できます。

3.  `dotenv`ファイルから環境変数を読み込むには、 `.env` } をインストールしてください。

        npm install dotenv

### ステップ3．スキーマを定義する {#step-3-define-your-schema}

1.  `schema.prisma`という名前のファイルを作成します。このファイルに、 `driverAdapters`プレビュー機能を含め、 `DATABASE_URL`環境変数を参照します。以下にファイルの例を示します。

        // schema.prisma
        generator client {
          provider        = "prisma-client-js"
          previewFeatures = ["driverAdapters"]
        }

        datasource db {
          provider     = "mysql"
          url          = env("DATABASE_URL")
        } 

2.  `schema.prisma`ファイルで、データベーステーブルのデータモデルを定義します。次の例では、 `user`という名前のデータモデルが定義されています。

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

3.  データベースをPrismaスキーマと同期させます。TiDB Cloud Starterインスタンスでデータベーステーブルを手動で作成するか、Prisma CLIを使用して次のように自動的に作成することができます。

        npx prisma db push

    このコマンドは、 `user`を使用した HTTPS 接続ではなく、従来の TCP 接続を通じてTiDB Cloud Starterインスタンスに`@tidbcloud/prisma-adapter`します。これは、Prisma Migrate と同じエンジンを使用しているためです。このコマンドの詳細については、 [スキーマのプロトタイプを作成します](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)参照してください。

4.  Prismaクライアントを生成する：

        npx prisma generate

    このコマンドは、Prismaスキーマに基づいてPrismaクライアントを生成します。

### ステップ4．CRUD操作を実行する {#step-4-execute-crud-operations}

1.  `hello-word.js`という名前のファイルを作成し、以下のコードを追加してPrisma Clientを初期化します。

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

2.  Prisma Client を使用して、いくつかの CRUD 操作を実行します。例:

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

3.  Prisma Client を使用してトランザクション操作を実行します。例:

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

## エッジ環境ではPrismaアダプタを使用する {#use-the-prisma-adapter-in-edge-environments}

Vercel Edge FunctionsやCloudflare Workersなどのエッジ環境では`@tidbcloud/prisma-adapter` v5.11.0以降のバージョンを使用できます。

-   [Vercel Edge 関数の例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-vercel-example)
-   [Cloudflare Workersの例](https://github.com/tidbcloud/serverless-driver-example/tree/main/prisma/prisma-cloudflare-worker-example)
