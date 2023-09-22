---
title: TiDB Cloud Serverless Driver (Beta)
summary: Learn how to connect to TiDB Serverless from serverless and edge environments over HTTP.
---

# TiDB CloudサーバーレスDriver(ベータ版) {#tidb-cloud-serverless-driver-beta}

JavaScript の[TiDB Cloudサーバーレス ドライバー (ベータ版)](https://github.com/tidbcloud/serverless-js)を使用すると、HTTPS 経由で TiDB サーバーレス クラスターに接続できます。これは、TCP 接続が[バーセルエッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などに制限されているエッジ環境で特に役立ちます。

## サーバーレスドライバーをインストールする {#install-the-serverless-driver}

npm を使用してドライバーをインストールできます。

```bash
npm install @tidbcloud/serverless
```

## サーバーレスドライバーを使用する {#use-the-serverless-driver}

サーバーレス ドライバーを使用して、TiDB サーバーレス クラスターのデータをクエリしたり、対話型トランザクションを実行したりできます。

### クエリ {#query}

TiDB サーバーレス クラスターからデータをクエリするには、まず接続を作成する必要があります。その後、その接続を使用して生の SQL クエリを実行できます。例えば：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### トランザクション(実験的) {#transaction-experimental}

サーバーレス ドライバーを使用して対話型トランザクションを実行することもできます。例えば：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://username:password@host/database'})
const tx = await conn.begin()

try {
  await tx.execute('insert into test values (1)')
  await tx.execute('select * from test')
  await tx.commit()
}catch (err) {
  await tx.rollback()
  throw err
}
```

## エッジの例 {#edge-examples}

以下に、エッジ環境でのサーバーレス ドライバーの使用例をいくつか示します。完全な例として、これを試すこともできます[ライブデモ](https://github.com/tidbcloud/car-sales-insight) 。

<SimpleTab>

<div label="Vercel Edge Function">

```ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { connect } from '@tidbcloud/serverless'
export const runtime = 'edge'

export async function GET(request: NextRequest) {
  const conn = connect({url: process.env.DATABASE_URL})
  const result = await conn.execute('show tables')
  return NextResponse.json({result});
}
```

</div>

<div label="Cloudflare Workers">

```ts
import { connect } from '@tidbcloud/serverless'
export interface Env {
  DATABASE_URL: string;
}
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const conn = connect({url: env.DATABASE_URL})
    const result = await conn.execute('show tables')
    return new Response(JSON.stringify(result));
  },
};
```

</div>

<div label="Netlify Edge Function">

```ts
import { connect } from 'https://esm.sh/@tidbcloud/serverless'

export default async () => {
  const conn = connect({url: Netlify.env.get('DATABASE_URL')})
  const result = await conn.execute('show tables')
  return new Response(JSON.stringify(result));
}
```

</div>

<div label="Deno">

```ts
import { connect } from "npm:@tidbcloud/serverless-js"

const conn = connect({url: Deno.env.get('DATABASE_URL')})
const result = await conn.execute('show tables')
```

</div>

<div label="Bun">

```ts
import { connect } from "@tidbcloud/serverless-js"

const conn = connect({url: Bun.env.DATABASE_URL})
const result = await conn.execute('show tables')
```

</div>

</SimpleTab>

## 特徴 {#features}

### サポートされている SQL ステートメント {#supported-sql-statements}

DDL がサポートされており、SQL ステートメント`SELECT` 、 `SHOW` 、 `EXPLAIN` 、 `USE` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `BEGIN` 、 `COMMIT` 、 `ROLLBACK`がサポートされています。

### データ型マッピング {#data-type-mapping}

TiDB サーバーレスと Javascript の間のタイプ マッピングは次のとおりです。

| TiDB サーバーレスタイプ | JavaScriptの種類 |
| -------------- | ------------- |
| タイイント          | 番号            |
| 未署名の TINYINT   | 番号            |
| ブール            | 番号            |
| スモールント         | 番号            |
| 署名のない SMALLINT | 番号            |
| ミディアムミント       | 番号            |
| INT            | 番号            |
| 符号なし整数         | 番号            |
| 年              | 番号            |
| 浮く             | 番号            |
| ダブル            | 番号            |
| BIGINT         | 弦             |
| 符号なし BIGINT    | 弦             |
| 10進数           | 弦             |
| チャー            | 弦             |
| VARCHAR        | 弦             |
| バイナリ           | 弦             |
| ヴァービナリー        | 弦             |
| 小さなテキスト        | 弦             |
| TEXT           | 弦             |
| メディアテキスト       | 弦             |
| 長文             | 弦             |
| タイニーブロブ        | 弦             |
| BLOB           | 弦             |
| ミディアムブロブ       | 弦             |
| ロングブロブ         | 弦             |
| 日付             | 弦             |
| 時間             | 弦             |
| 日付時刻           | 弦             |
| タイムスタンプ        | 弦             |
| ENUM           | 弦             |
| セット            | 弦             |
| 少し             | 弦             |
| JSON           | 物体            |
| ヌル             | ヌル            |
| その他            | 弦             |

## 価格設定 {#pricing}

サーバーレス ドライバー自体は無料ですが、ドライバーを使用してデータにアクセスすると、 [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)とstorageの使用量が発生します。価格は[TiDB サーバーレスの価格](https://www.pingcap.com/tidb-serverless-pricing-details/)モデルに準じます。

## 制限事項 {#limitations}

現在、サーバーレス ドライバーの使用には次の制限があります。

-   1 つのクエリで最大 10,000 行をフェッチできます。
-   一度に実行できる SQL ステートメントは 1 つだけです。 1 つのクエリ内の複数の SQL ステートメントはまだサポートされていません。
-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)との接続はまだサポートされていません。

## 次は何ですか {#what-s-next}

-   [TiDB Cloudサーバーレス ドライバーを構成する方法を学ぶ](/tidb-cloud/serverless-driver-config.md) 。
-   [TiDB Cloudサーバーレス ドライバー言語で Kysely ORM を使用する方法を学ぶ](https://github.com/tidbcloud/kysely) 。
