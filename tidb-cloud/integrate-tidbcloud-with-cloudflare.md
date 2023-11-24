---
title: Integrate TiDB Cloud with Cloudflare
summary: Learn how to deploy Cloudflare Workers with TiDB Cloud.
---

# TiDB Cloudと Cloudflare ワーカーを統合する {#integrate-tidb-cloud-with-cloudflare-workers}

[Cloudflare ワーカー](https://workers.cloudflare.com/)は、HTTP リクエストやデータベースへの変更などの特定のイベントに応答してコードを実行できるプラットフォームです。 Cloudflare Workers は使いやすく、カスタム API、サーバーレス関数、マイクロサービスなどのさまざまなアプリケーションの構築に使用できます。これは、低レイテンシのパフォーマンスを必要とするアプリケーションや、迅速に拡張する必要があるアプリケーションに特に役立ちます。

Cloudflare Workers は直接 TCP 接続を行うことができない V8 エンジン上で実行されるため、Cloudflare Workers からTiDB Cloudに接続するのが難しいと感じるかもしれません。 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)を使用すると、HTTP 接続経由で Cloudflare Workers に接続できます。

このドキュメントでは、TiDB Cloudサーバーレスドライバーを使用して Cloudflare Workers に接続する方法を段階的に説明します。

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーは、TiDB サーバーレスでのみ使用できます。

## あなたが始める前に {#before-you-begin}

この記事の手順を試す前に、次のものを準備する必要があります。

-   TiDB CloudアカウントとTiDB Cloud上の TiDB サーバーレス クラスター。詳細については、 [TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)を参照してください。
-   回答[Cloudflare ワーカーアカウント](https://dash.cloudflare.com/login) ．
-   [npm](https://docs.npmjs.com/about-npm)がインストールされています。

## ステップ 1: Wrangler をセットアップする {#step-1-set-up-wrangler}

[ラングラー](https://developers.cloudflare.com/workers/wrangler/)は公式のCloudflare Worker CLIです。これを使用して、ワーカーを生成、構築、プレビュー、公開できます。

1.  ラングラーをインストールします。

        npm install wrangler

2.  Wrangler を認証するには、wrangler ログインを実行します。

        wrangler login

3.  Wrangler を使用してワーカー プロジェクトを作成します。

        wrangler init tidb-cloud-cloudflare

4.  ターミナルでは、プロジェクトに関連する一連の質問が表示されます。すべての質問に対してデフォルト値を選択します。

## ステップ 2: サーバーレスドライバーをインストールする {#step-2-install-the-serverless-driver}

1.  プロジェクト ディレクトリを入力します。

        cd tidb-cloud-cloudflare

2.  npm を使用してサーバーレス ドライバーをインストールします。

        npm install @tidbcloud/serverless

    これにより、サーバーレス ドライバーの依存関係が`package.json`に追加されます。

## ステップ 3: Cloudflare Worker 機能を開発する {#step-3-develop-the-cloudflare-worker-function}

必要に応じて`src/index.ts`を変更する必要があります。

たとえば、すべてのデータベースを表示したい場合は、次のコードを使用できます。

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

## ステップ 4: 環境に DATABASE_URL を設定する {#step-4-set-the-database-url-in-your-environment}

`DATABASE_URL`は`mysql://username:password@host/database`形式に従います。 Wrangler cli を使用して環境変数を設定できます。

    wrangler secret put <DATABASE_URL>

Cloudflare Workers ダッシュボードから`DATABASE_URL`シークレットを編集することもできます。

## ステップ5: Cloudflareワーカーに公開する {#step-5-publish-to-cloudflare-workers}

これで、Cloudflare Workers にデプロイする準備ができました。

プロジェクト ディレクトリで、次のコマンドを実行します。

    npx wrangler publish

## ステップ 6: Cloudflare ワーカーを試す {#step-6-try-your-cloudflare-workers}

1.  [Cloudflareダッシュボード](https://dash.cloudflare.com)に進み、ワーカーを見つけます。ワーカーの URL は概要ページで確認できます。

2.  URL にアクセスすると結果が表示されます。

## 例 {#examples}

[Cloudflare ワーカーの例](https://github.com/tidbcloud/car-sales-insight/tree/main/examples/cloudflare-workers)参照してください。
