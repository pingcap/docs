---
title: Integrate TiDB Cloud with Cloudflare
summary: Learn how deploy Cloudflare Workers with TiDB Cloud.
---

# TiDB Cloudと Cloudflare ワーカーを統合する {#integrate-tidb-cloud-with-cloudflare-workers}

[Cloudflare ワーカー](https://workers.cloudflare.com/)は、HTTP リクエストやデータベースへの変更などの特定のイベントに応答してコードを実行できるプラットフォームです。 Cloudflare Workers は使いやすく、カスタム API、サーバーレス関数、マイクロサービスなどのさまざまなアプリケーションの構築に使用できます。これは、低レイテンシのパフォーマンスを必要とするアプリケーションや、迅速に拡張する必要があるアプリケーションに特に役立ちます。

ただし、Cloudflare Workers は直接 TCP 接続を行うことができない V8 エンジン上で実行されるため、Cloudflare Workers からTiDB Cloudに接続するのが難しい場合があります。

幸いなことに、Prisma は[データプロキシ](https://www.prisma.io/docs/data-platform/data-proxy)をサポートします。これは、Cloudflare Workers を使用して、TCP 接続経由で送信されるデータを処理および操作するのに役立ちます。

このドキュメントでは、 TiDB Cloudおよび Prisma Data Proxy を使用して Cloudflare Workers をデプロイする方法を段階的に説明します。

> **注記：**
>
> ローカルにデプロイされた TiDB を Cloudflare Workers に接続する場合は、Cloudflare トンネルをプロキシとして使用する[労働者-情報](https://github.com/shiyuhang0/worker-tidb)を試すことができます。ただし、worker-tdb は本番での使用はお勧めできません。

## あなたが始める前に {#before-you-begin}

この記事の手順を試す前に、次のものを準備する必要があります。

-   TiDB CloudアカウントとTiDB Cloud上の TiDB サーバーレス クラスター。詳細については、 [TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)を参照してください。
-   回答[Cloudflare ワーカーアカウント](https://dash.cloudflare.com/login) ．
-   回答[Prisma データ プラットフォーム アカウント](https://cloud.prisma.io/) ．
-   回答[GitHub アカウント](https://github.com/login) ．
-   Node.js と npm をインストールします。
-   `npm install -D prisma typescript wrangler`を使用して依存関係をインストールします

## ステップ 1: Wrangler をセットアップする {#step-1-set-up-wrangler}

[ラングラー](https://developers.cloudflare.com/workers/wrangler/)は公式のCloudflare Worker CLIです。これを使用して、ワーカーを生成、構築、プレビュー、公開できます。

1.  Wrangler を認証するには、wrangler ログインを実行します。

        wrangler login

2.  Wrangler を使用してワーカー プロジェクトを作成します。

        wrangler init prisma-tidb-cloudflare

3.  ターミナルでは、プロジェクトに関連する一連の質問が表示されます。すべての質問に対してデフォルト値を選択します。

## ステップ 2: Prisma をセットアップする {#step-2-set-up-prisma}

1.  プロジェクト ディレクトリを入力します。

        cd prisma-tidb-cloudflare

2.  `prisma init`コマンドを使用して Prisma をセットアップします。

        npx prisma init

    これにより、 `prisma/schema.prisma`に Prisma スキーマが作成されます。

3.  `prisma/schema.prisma`内に、TiDB のテーブルに従ってスキーマを追加します。 TiDB に`table1`と`table2`あると仮定すると、次のスキーマを追加できます。

        generator client {
          provider = "prisma-client-js"
        }

        datasource db {
          provider = "mysql"
          url      = env("DATABASE_URL")
        }

        model table1 {
          id   Int                   @id @default(autoincrement())
          name String
        }

        model table2 {
          id   Int                   @id @default(autoincrement())
          name String
        }

    このデータ モデルは、ワーカーからの受信リクエストを保存するために使用されます。

## ステップ 3: プロジェクトを GitHub にプッシュする {#step-3-push-your-project-to-github}

1.  GitHub では[リポジトリを作成する](https://github.com/new) `prisma-tidb-cloudflare`と名付けました。

2.  リポジトリを作成したら、プロジェクトを GitHub にプッシュできます。

        git remote add origin https://github.com/<username>/prisma-tidb-cloudflare
        git add .
        git commit -m "initial commit"
        git push -u origin main

## ステップ 4: プロジェクトを Prisma データ プラットフォームにインポートする {#step-4-import-your-project-into-the-prisma-data-platform}

Cloudflare Workers では、TCP サポートがないため、データベースに直接アクセスできません。代わりに、上記のように Prisma Data Proxy を使用できます。

1.  開始するには、 [プリズマ データ プラットフォーム](https://cloud.prisma.io/)にサインインし、 **[新しいプロジェクト]**をクリックします。

2.  **接続文字列**にこのパターンを入力します`mysql://USER:PASSWORD@HOST:PORT/DATABASE?sslaccept=strict` 。接続情報は[TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)にあります。

3.  TiDB Serverless にはどの IP アドレスからでもアクセスできるため、**静的 IP は**無効のままにしておきます。

4.  TiDB Cloudクラスターの場所に地理的に近いデータ プロキシ リージョンを選択します。次に、 **「プロジェクトの作成」**をクリックします。

    ![Configure project settings](/media/tidb-cloud/cloudflare/cloudflare-project.png)

5.  リポジトリに入力し、 **「開始」**ページで**「Prisma スキーマをリンク」を**クリックします。

6.  **[新しい接続文字列の作成]**をクリックすると、 `prisma://.`で始まる新しい接続文字列が取得されます。この接続文字列をコピーして、後で使用できるように保存します。

    ![Create new connection string](/media/tidb-cloud/cloudflare/cloudflare-start.png)

7.  **[スキップしてデータ プラットフォームに進む]**をクリックして、データ プラットフォームに移動します。

## ステップ 5: 環境でデータ プロキシ接続文字列を設定する {#step-5-set-the-data-proxy-connection-string-in-your-environment}

1.  データ プロキシ接続文字列をローカル環境`.env`ファイルに追加します。

        DATABASE_URL=prisma://aws-us-east-1.prisma-data.com/?api_key=•••••••••••••••••"

2.  シークレットを使用してデータ プロキシ接続を Cloudflare Workers に追加します。

        wrangler secret put DATABASE_URL

3.  プロンプトに従って、データ プロキシ接続文字列を入力します。

> **注記：**
>
> Cloudflare Workers ダッシュボードから`DATABASE_URL`シークレットを編集することもできます。

## ステップ 6: Prisma クライアントを生成する {#step-6-generate-a-prisma-client}

[データプロキシ](https://www.prisma.io/docs/data-platform/data-proxy)を介して接続する Prisma クライアントを生成します。

    npx prisma generate --data-proxy

## ステップ7: Cloudflare Worker機能を開発する {#step-7-develop-the-cloudflare-worker-function}

必要に応じて`src/index.ts`を変更する必要があります。

たとえば、URL 変数を使用してさまざまなテーブルをクエリする場合は、次のコードを使用できます。

```js
import { PrismaClient } from '@prisma/client/edge'
const prisma = new PrismaClient()

addEventListener('fetch', (event) => {
  event.respondWith(handleEvent(event))
})

async function handleEvent(event: FetchEvent): Promise<Response> {
  // Get URL parameters
  const { request } = event
  const url = new URL(request.url);
  const table = url.searchParams.get('table');
  let limit = url.searchParams.get('limit');
  const limitNumber = limit? parseInt(limit): 100;

  // Get model
  let model
  for (const [key, value] of Object.entries(prisma)) {
    if (typeof value == 'object' && key == table) {
      model = value
      break
    }
  }
  if(!model){
    return new Response("Table not defined")
  }

  // Get data
  const result = await model.findMany({ take: limitNumber })
  return new Response(JSON.stringify({ result }))
}
```

## ステップ8: Cloudflareワーカーに公開する {#step-8-publish-to-cloudflare-workers}

これで、Cloudflare Workers にデプロイする準備ができました。

プロジェクト ディレクトリで、次のコマンドを実行します。

    npx wrangler publish

## ステップ9: Cloudflareワーカーを試す {#step-9-try-your-cloudflare-workers}

1.  [Cloudflareダッシュボード](https://dash.cloudflare.com)に進み、ワーカーを見つけます。ワーカーの URL は概要ページで確認できます。

2.  テーブル名を含む URL にアクセスします: `https://{your-worker-url}/?table={table_name}` 。対応する TiDB テーブルから結果を取得します。

## プロジェクトを更新する {#update-the-project}

### サーバーレス機能を変更する {#change-the-serverless-function}

サーバーレス機能を変更したい場合は、 `src/index.ts`更新して再度Cloudflare Workersに公開してください。

### 新しいテーブルを作成する {#create-a-new-table}

新しいテーブルを作成してクエリを実行する場合は、次の手順を実行します。

1.  `prisma/schema.prisma`で新しいモデルを追加します。

2.  変更をリポジトリにプッシュします。

        git add prisma
        git commit -m "add new model"
        git push

3.  Prisma クライアントを再度生成します。

        npx prisma generate --data-proxy

4.  Cloudflare Workerを再度公開します。

        npx wrangler publish
