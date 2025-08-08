---
title: Integrate TiDB Cloud with Cloudflare
summary: TiDB Cloudを使用して Cloudflare Workers をデプロイする方法を学びます。
---

# TiDB CloudとCloudflare Workersを統合する {#integrate-tidb-cloud-with-cloudflare-workers}

Cloudflare Workersは、HTTPリクエストやデータベースへの変更など、特定のイベントに応じてコードを実行できるプラットフォーム[Cloudflareワーカー](https://workers.cloudflare.com/) 。Cloudflare Workersは使いやすく、カスタムAPI、サーバーレス関数、マイクロサービスなど、さまざまなアプリケーションの構築に使用できます。特に、低レイテンシーのパフォーマンスが求められるアプリケーションや、迅速なスケーリングが必要なアプリケーションに便利です。

Cloudflare WorkersはV8エンジンで動作しており、直接TCP接続ができないため、 TiDB Cloudへの接続が難しい場合があります。1 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)使用すると、HTTP接続経由でCloudflare Workersに接続できます。

このドキュメントでは、TiDB Cloudサーバーレス ドライバーを使用して Cloudflare Workers に接続する方法を段階的に説明します。

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーは、 TiDB Cloud Serverless でのみ使用できます。

## 始める前に {#before-you-begin}

この記事の手順を試す前に、次のものを準備する必要があります。

-   TiDB CloudアカウントとTiDB Cloud上のTiDB Cloud Serverlessクラスター。詳細については、 [TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)ご覧ください。
-   A [Cloudflare Workersアカウント](https://dash.cloudflare.com/login) 。
-   [npm](https://docs.npmjs.com/about-npm)がインストールされています。

## ステップ1: Wranglerを設定する {#step-1-set-up-wrangler}

[ラングラー](https://developers.cloudflare.com/workers/wrangler/)はCloudflareの公式Worker CLIです。Workerの生成、ビルド、プレビュー、公開に使用できます。

1.  Wrangler をインストールします。

        npm install wrangler

2.  Wrangler を認証するには、wrangler login を実行します。

        wrangler login

3.  Wrangler を使用してワーカー プロジェクトを作成します。

        wrangler init tidb-cloud-cloudflare

4.  ターミナルでは、プロジェクトに関連する一連の質問が表示されます。すべての質問に対してデフォルト値を選択してください。

## ステップ2: サーバーレスドライバーをインストールする {#step-2-install-the-serverless-driver}

1.  プロジェクト ディレクトリを入力してください:

        cd tidb-cloud-cloudflare

2.  npm を使用してサーバーレス ドライバーをインストールします。

        npm install @tidbcloud/serverless

    これにより、 `package.json`にサーバーレス ドライバーの依存関係が追加されます。

## ステップ3: Cloudflare Worker関数を開発する {#step-3-develop-the-cloudflare-worker-function}

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

## ステップ4: 環境内でDATABASE_URLを設定する {#step-4-set-the-database-url-in-your-environment}

`DATABASE_URL` `mysql://username:password@host/database`形式に従います。環境変数はwrangler cliで設定できます。

    wrangler secret put <DATABASE_URL>

Cloudflare Workers ダッシュボードから`DATABASE_URL`シークレットを編集することもできます。

## ステップ5：Cloudflare Workersに公開する {#step-5-publish-to-cloudflare-workers}

これで、Cloudflare Workers にデプロイする準備が整いました。

プロジェクト ディレクトリで、次のコマンドを実行します。

    npx wrangler publish

## ステップ6：Cloudflare Workersを試す {#step-6-try-your-cloudflare-workers}

1.  [Cloudflareダッシュボード](https://dash.cloudflare.com)に進み、ワーカーを見つけてください。ワーカーの URL は概要ページで確認できます。

2.  URL にアクセスすると結果が表示されます。

## 例 {#examples}

[Cloudflare Workersの例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)参照してください。
