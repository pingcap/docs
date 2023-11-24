---
title: TiDB Cloud Serverless Driver (Beta)
summary: Learn how to connect to TiDB Serverless from serverless and edge environments.
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB CloudサーバーレスDriver(ベータ版) {#tidb-cloud-serverless-driver-beta}

## TiDB CloudサーバーレスDriver(ベータ版) を使用する理由 {#why-use-tidb-cloud-serverless-driver-beta}

従来の TCP ベースの MySQL ドライバーは、サーバーレス関数の存続期間が短い性質と矛盾する、存続期間の長い永続的な TCP 接続を期待しているため、サーバーレス関数には適していません。さらに、 [バーセルエッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などのエッジ環境では、包括的な TCP サポートや Node.js の完全な互換性が不足している可能性があり、これらのドライバーはまったく機能しない可能性があります。

JavaScript の[TiDB Cloudサーバーレス ドライバー (ベータ版)](https://github.com/tidbcloud/serverless-js)を使用すると、HTTP 経由で TiDB サーバーレス クラスターに接続できます。これは通常、サーバーレス環境でサポートされています。これにより、従来の TCP ベースの MySQL ドライバーと同様の開発エクスペリエンスを維持しながら、エッジ環境から TiDB サーバーレス クラスターに接続し、TCP による接続オーバーヘッドを削減できるようになりました。

> **注記：**
>
> SQL や ORM ではなく RESTful API を使用したプログラミングを好む場合は、 [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)を使用できます。

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

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### トランザクション(実験的) {#transaction-experimental}

サーバーレス ドライバーを使用して対話型トランザクションを実行することもできます。例えば：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
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

以下に、エッジ環境でのサーバーレス ドライバーの使用例をいくつか示します。完全な例については、これを試すこともできます[ライブデモ](https://github.com/tidbcloud/car-sales-insight) 。

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

[Vercel でTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)の詳細をご覧ください。

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

[Cloudflare Workers でTiDB Cloudサーバーレスドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md)の詳細をご覧ください。

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

[Netlify でTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function)の詳細をご覧ください。

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

## サーバーレスドライバーを構成する {#configure-the-serverless-driver}

TiDB Cloudサーバーレス ドライバーは、接続レベルと SQL レベルの両方で構成できます。

### 接続レベルの構成 {#connection-level-configurations}

接続レベルでは、次の構成を行うことができます。

| 名前           | タイプ | デフォルト値    | 説明                                                                                                        |
| ------------ | --- | --------- | --------------------------------------------------------------------------------------------------------- |
| `username`   | 弦   | 該当なし      | TiDB サーバーレスのユーザー名                                                                                         |
| `password`   | 弦   | 該当なし      | TiDBサーバーレスのパスワード                                                                                          |
| `host`       | 弦   | 該当なし      | TiDB サーバーレスのホスト名                                                                                          |
| `database`   | 弦   | `test`    | TiDBサーバーレスのデータベース                                                                                         |
| `url`        | 弦   | 該当なし      | データベースの URL ( `mysql://[username]:[password]@[host]/[database]`形式)。デフォルトのデータベースに接続する場合は`database`を省略できます。 |
| `fetch`      | 関数  | グローバルフェッチ | カスタムフェッチ関数。たとえば、node.js で`undici`フェッチを使用できます。                                                             |
| `arrayMode`  | ブール | `false`   | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、これを`true`に設定します。                                                 |
| `fullResult` | ブール | `false`   | 行だけではなく完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、これを`true`に設定します。                                                 |

**データベースのURL**

> **注記：**
>
> ユーザー名、パスワード、またはデータベース名に特殊文字が含まれている場合は、URL で渡すときにこれらの文字を[パーセントエンコード](https://en.wikipedia.org/wiki/Percent-encoding)する必要があります。たとえば、パスワード`password1@//?`は、URL 内で`password1%40%2F%2F%3F`としてエンコードする必要があります。

`url`が設定されている場合、 `host` 、 `username` 、 `password` 、および`database`を個別に設定する必要はありません。次のコードは同等です。

```ts
const config = {
  host: '<host>',
  username: '<user>',
  password: '<password>',
  database: '<database>',
  arrayMode: true,
}

const conn = connect(config)
```

```ts
const config = {
  url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]',
  arrayMode: true
}

const conn = connect(config)
```

### SQLレベルのオプション {#sql-level-options}

> **注記：**
>
> SQL レベルのオプションは、接続レベルの設定よりも優先されます。

SQL レベルでは、次のオプションを構成できます。

| オプション        | タイプ | デフォルト値  | 説明                                                        |
| ------------ | --- | ------- | --------------------------------------------------------- |
| `arrayMode`  | ブール | `false` | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、これを`true`に設定します。 |
| `fullResult` | ブール | `false` | 行だけではなく完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、これを`true`に設定します。 |

例えば：

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

TiDB Cloudサーバーレス ドライバー v0.0.7 以降、トランザクションを使用するときに次の SQL レベル オプションを構成することもできます。

| オプション       | タイプ | デフォルト値            | 説明                                                          |
| ----------- | --- | ----------------- | ----------------------------------------------------------- |
| `isolation` | 弦   | `REPEATABLE READ` | トランザクション分離レベル。 `READ COMMITTED`または`REPEATABLE READ`に設定できます。 |

`isolation`オプションは`begin`機能でのみ使用できます。以下に例を示します。

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

## 特徴 {#features}

### サポートされている SQL ステートメント {#supported-sql-statements}

DDL がサポートされており、SQL ステートメント`SELECT` 、 `SHOW` 、 `EXPLAIN` 、 `USE` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `BEGIN` 、 `COMMIT` 、 `ROLLBACK` 、および`SET`がサポートされています。

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

### ORM統合 {#orm-integrations}

TiDB Cloudサーバーレス ドライバーは、次の ORM と統合されました。

-   [TiDB Cloudサーバーレス ドライバー Kysely の方言](https://github.com/tidbcloud/kysely) 。
-   [TiDB Cloudサーバーレス ドライバー Prisma アダプター](https://github.com/tidbcloud/prisma-adapter) 。

## 価格設定 {#pricing}

サーバーレス ドライバー自体は無料ですが、ドライバーを使用してデータにアクセスすると、 [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)とstorageの使用量が発生します。価格は[TiDB サーバーレスの価格](https://www.pingcap.com/tidb-serverless-pricing-details/)モデルに準じます。

## 制限事項 {#limitations}

現在、サーバーレス ドライバーの使用には次の制限があります。

-   1 つのクエリで最大 10,000 行をフェッチできます。
-   一度に実行できる SQL ステートメントは 1 つだけです。 1 つのクエリ内の複数の SQL ステートメントはまだサポートされていません。
-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)との接続はまだサポートされていません。

## 次は何ですか {#what-s-next}

-   [ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/serverless-driver-node-example.md)の方法を学びます。
