---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Prisma ORM.
---

# TiDB CloudサーバーレスDriverPrisma チュートリアル {#tidb-cloud-serverless-driver-prisma-tutorial}

[プリズマ](https://www.prisma.io/docs)は、開発者が直観的、効率的、安全な方法でデータベースを操作できるようにするオープンソースの次世代 ORM (オブジェクト リレーショナル マッピング) です。 TiDB Cloudは[@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)を提供し、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)で[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client) HTTPS 経由で使用できるようにします。従来の TCP 方式と比較して、 [@tidbcloud/プリズマアダプター](https://github.com/tidbcloud/prisma-adapter)には次の利点があります。

-   サーバーレス環境でのパフォーマンスの向上
-   エッジ環境で Prisma クライアントを使用できる可能性 (詳細については[#21394](https://github.com/prisma/prisma/issues/21394)を参照)

このチュートリアルでは、Prisma アダプターでTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

## Node.js 環境で Prisma アダプターを使用する {#use-the-prisma-adapter-in-node-js-environments}

### あなたが始める前に {#before-you-begin}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)または好みのパッケージ マネージャー。
-   TiDB サーバーレス クラスター。何も持っていない場合は、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)を実行できます。

### ステップ 1. プロジェクトを作成する {#step-1-create-a-project}

1.  `prisma-example`という名前のプロジェクトを作成します。

        mkdir prisma-example
        cd prisma-example

2.  `@tidbcloud/prisma-adapter`ドライバー アダプター、 `@tidbcloud/serverless`サーバーレス ドライバー、および Prisma CLI をインストールします。

    次のコマンドは、パッケージ マネージャーとして npm を使用します。 `npm install @tidbcloud/serverless`を実行すると、プロジェクト ディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/prisma-adapter
        npm install @tidbcloud/serverless
        npm install prisma --save-dev

3.  `package.json`ファイルに`type: "module"`を追加して ES モジュールを指定します。

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

### ステップ 2. 環境を設定する {#step-2-set-the-environment}

1.  TiDB サーバーレス クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict

2.  プロジェクトのルート ディレクトリに`.env`という名前のファイルを作成し、次のように`DATABASE_URL`という名前の環境変数を定義し、この変数内のプレースホルダ`[]`接続文字列内の対応するパラメータに置き換えます。

    ```dotenv
    DATABASE_URL="mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict"
    ```

    > **注記：**
    >
    > `@tidbcloud/prisma-adapter`は、HTTPS 経由の Prisma クライアントの使用のみをサポートします。 [プリズママイグレーション](https://www.prisma.io/docs/concepts/components/prisma-migrate)と[プリズマの内観](https://www.prisma.io/docs/concepts/components/introspection)では、従来の TCP 接続が引き続き使用されます。 Prisma Client のみを使用する必要がある場合は、 `DATABASE_URL` `mysql://[username]:[password]@[host]/[database]`形式に簡素化できます。

3.  `dotenv`をインストールして、 `.env`ファイルから環境変数をロードします。

        npm install dotenv

### ステップ 3. スキーマを定義する {#step-3-define-your-schema}

1.  `schema.prisma`という名前のファイルを作成します。このファイルには、 `driverAdapters`プレビュー機能を含め、 `DATABASE_URL`環境変数を参照します。ファイルの例を次に示します。

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

3.  データベースを Prisma スキーマと同期します。 TiDB サーバーレス クラスターにデータベース テーブルを手動で作成することも、Prisma CLI を使用して次のように自動的に作成することもできます。

        npx prisma db push

    このコマンドは、 `@tidbcloud/prisma-adapter`使用した HTTPS 接続ではなく、従来の TCP 接続を通じて TiDB サーバーレス クラスターに`user`テーブルを作成します。これは、Prisma Migrate と同じエンジンを使用しているためです。このコマンドの詳細については、 [スキーマのプロトタイプを作成する](https://www.prisma.io/docs/concepts/components/prisma-migrate/db-push)を参照してください。

4.  Prisma クライアントを生成します。

        npx prisma generate

    このコマンドは、Prisma スキーマに基づいて Prisma Client を生成します。

### ステップ 4. CRUD 操作を実行する {#step-4-execute-crud-operations}

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

2.  Prisma Client を使用していくつかの CRUD 操作を実行します。例えば：

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

3.  Prisma Client を使用していくつかのトランザクション操作を実行します。例えば：

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

## エッジ環境で Prisma アダプターを使用する {#use-the-prisma-adapter-in-edge-environments}

現在、 `@tidbcloud/prisma-adapter` Vercel Edge Function や Cloudflare Workers などのエッジ環境とは互換性がありません。ただし、これらの環境をサポートする計画があります。詳細については、 [#21394](https://github.com/prisma/prisma/issues/21394)を参照してください。
