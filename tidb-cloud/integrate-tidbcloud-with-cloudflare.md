---
title: Integrate TiDB Cloud with Cloudflare
summary: TiDB Cloudで Cloudflare Workers をデプロイする方法を学びましょう。
---

# TiDB CloudとCloudflare Workersを統合する {#integrate-tidb-cloud-with-cloudflare-workers}

[Cloudflare Workers](https://workers.cloudflare.com/) 、HTTPリクエストやデータベースの変更といった特定のイベントに応じてコードを実行できるプラットフォームです。Cloudflare Workersは使いやすく、カスタムAPI、サーバーレス関数、マイクロサービスなど、さまざまなアプリケーションの構築に利用できます。特に、低遅延性能が求められるアプリケーションや、迅速なスケーリングが必要なアプリケーションに最適です。

Cloudflare WorkersはV8エンジン上で動作するため、直接TCP接続を確立できないため、Cloudflare WorkersからTiDB Cloudへの接続は難しい場合があります。TiDB [TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md)HTTP接続を介してCloudflare Workersに接続するのに役立ちます。 レス

このドキュメントでは、TiDB Cloudサーバーレスドライバーを使用してCloudflare Workersに接続する方法をステップバイステップで説明します。

> **注記：**
>
> TiDB Cloudのサーバーレスドライバーは、 TiDB Cloud StarterおよびTiDB Cloud Essentialでのみ使用できます。

## 始める前に {#before-you-begin}

この記事の手順を試す前に、以下のものを準備する必要があります。

-   [TiDB Cloudアカウント](https://tidbcloud.com/signup)。
-   TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス。お持ちでない場合は、 [TiDB Cloud StarterまたはEssentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)参照してください。
-   [Cloudflare Workersアカウント](https://dash.cloudflare.com/login)。
-   [npm](https://docs.npmjs.com/about-npm)がインストールされています。

## ステップ1：ラングラーをセットアップする {#step-1-set-up-wrangler}

[ラングラー](https://developers.cloudflare.com/workers/wrangler/)Cloudflare Worker の公式 CLI です。これを使用して、Worker の生成、構築、プレビュー、および公開を行うことができます。

1.  Wranglerをインストールする：

        npm install wrangler

2.  Wranglerを認証するには、`wrangler login`を実行します。

        wrangler login

3.  Wranglerを使用してワーカープロジェクトを作成します。

        wrangler init tidb-cloud-cloudflare

4.  端末に、プロジェクトに関する一連の質問が表示されます。すべての質問に対して、デフォルト値を選択してください。

## ステップ2：サーバーレスドライバーをインストールする {#step-2-install-the-serverless-driver}

1.  プロジェクトディレクトリを入力してください：

        cd tidb-cloud-cloudflare

2.  npmを使用してサーバーレスドライバーをインストールします。

        npm install @tidbcloud/serverless

    これにより`package.json`にサーバーレスドライバの依存関係が追加されます。

## ステップ3：Cloudflare Worker関数を開発する {#step-3-develop-the-cloudflare-worker-function}

`src/index.ts`は必要に応じて変更する必要があります。

例えば、すべてのデータベースを表示したい場合は、次のコードを使用できます。

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

## ステップ4：環境設定でDATABASE_URLを設定します {#step-4-set-the-database-url-in-your-environment}

`DATABASE_URL`は`mysql://username:password@host/database`の形式に従います。環境変数は wrangler cli を使用して設定できます。

    wrangler secret put <DATABASE_URL>

Cloudflare Workers ダッシュボードから`DATABASE_URL`シークレットを編集することもできます。

## ステップ5：Cloudflare Workersに公開する {#step-5-publish-to-cloudflare-workers}

これでCloudflare Workersへのデプロイ準備が整いました。

プロジェクトディレクトリで、以下のコマンドを実行してください。

    npx wrangler publish

## ステップ6：Cloudflare Workersを試してみる {#step-6-try-your-cloudflare-workers}

1.  [Cloudflareダッシュボード](https://dash.cloudflare.com)に移動してワーカーを見つけます。ワーカーの URL は概要ページで確認できます。

2.  そのURLにアクセスすれば、結果が表示されます。

## 例 {#examples}

[Cloudflare Workersの例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)参照してください。
