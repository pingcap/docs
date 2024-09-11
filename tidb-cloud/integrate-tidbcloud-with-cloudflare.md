---
title: Integrate TiDB Cloud with Cloudflare
summary: TiDB Cloudを使用して Cloudflare Workers をデプロイする方法を学びます。
---

# TiDB Cloudを Cloudflare Workers と統合する {#integrate-tidb-cloud-with-cloudflare-workers}

[Cloudflare ワーカー](https://workers.cloudflare.com/) 、HTTP リクエストやデータベースの変更など、特定のイベントに応じてコードを実行できるプラットフォームです。Cloudflare Workers は使いやすく、カスタム API、サーバーレス関数、マイクロサービスなど、さまざまなアプリケーションの構築に使用できます。特に、低レイテンシーのパフォーマンスが必要なアプリケーションや、迅速に拡張する必要があるアプリケーションに役立ちます。

Cloudflare Workers は直接 TCP 接続できない V8 エンジンで実行されるため、Cloudflare Workers からTiDB Cloudに接続するのは難しい場合があります。1 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)使用すると、HTTP 接続を介して Cloudflare Workers に接続できます。

このドキュメントでは、TiDB Cloudサーバーレス ドライバーを使用して Cloudflare Workers に接続する方法を段階的に説明します。

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーは、TiDB Cloud Serverless でのみ使用できます。

## 始める前に {#before-you-begin}

この記事の手順を試す前に、次のものを準備する必要があります。

-   TiDB CloudアカウントとTiDB Cloud上のTiDB Cloud Serverless クラスター。詳細については、 [TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)参照してください。
-   A [Cloudflare Workers アカウント](https://dash.cloudflare.com/login) 。
-   [ネプ](https://docs.npmjs.com/about-npm)がインストールされています。

## ステップ1: Wranglerを設定する {#step-1-set-up-wrangler}

[ラングラー](https://developers.cloudflare.com/workers/wrangler/)は公式の Cloudflare Worker CLI です。これを使用して、Worker を生成、構築、プレビュー、公開できます。

1.  Wrangler をインストールします。

        npm install wrangler

2.  Wrangler を認証するには、wrangler login を実行します。

        wrangler login

3.  Wrangler を使用してワーカー プロジェクトを作成します。

        wrangler init tidb-cloud-cloudflare

4.  ターミナルでは、プロジェクトに関連する一連の質問が表示されます。すべての質問に対してデフォルト値を選択します。

## ステップ2: サーバーレスドライバーをインストールする {#step-2-install-the-serverless-driver}

1.  プロジェクト ディレクトリを入力してください:

        cd tidb-cloud-cloudflare

2.  npm を使用してサーバーレス ドライバーをインストールします。

        npm install @tidbcloud/serverless

    これにより、 `package.json`にサーバーレス ドライバーの依存関係が追加されます。

## ステップ3: Cloudflare Worker機能を開発する {#step-3-develop-the-cloudflare-worker-function}

必要に応じて`src/index.ts`変更する必要があります。

たとえば、すべてのデータベースを表示する場合は、次のコードを使用できます。

```ts
import { connect } from '@tidbcloud/serverless'


export interface Env {
   DATABASE_URL: string;
}

export default {
   async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
      const conn = connect({url:env.DATABASE_URL})
      const resp = await conn.execute("show databases")
      return new Response(JSON.stringify(resp));
   },
};
```

## ステップ4: 環境でDATABASE_URLを設定する {#step-4-set-the-database-url-in-your-environment}

`DATABASE_URL` `mysql://username:password@host/database`形式に従います。環境変数は wrangler cli で設定できます。

    wrangler secret put <DATABASE_URL>

Cloudflare Workers ダッシュボードから`DATABASE_URL`シークレットを編集することもできます。

## ステップ5: Cloudflare Workersに公開する {#step-5-publish-to-cloudflare-workers}

これで、Cloudflare Workers にデプロイする準備が整いました。

プロジェクト ディレクトリで、次のコマンドを実行します。

    npx wrangler publish

## ステップ6: Cloudflare Workersを試す {#step-6-try-your-cloudflare-workers}

1.  [Cloudflareダッシュボード](https://dash.cloudflare.com)に進み、ワーカーを見つけます。ワーカーの URL は概要ページで確認できます。

2.  URL にアクセスすると結果が表示されます。

## 例 {#examples}

[Cloudflare Workersの例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)参照してください。
