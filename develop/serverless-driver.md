---
title: TiDB Cloud Serverless Driver (Beta)
summary: サーバーレス環境およびエッジ環境からTiDB Cloud StarterまたはTiDB Cloud Essentialに接続する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-driver-config/','/ja/tidbcloud/serverless-driver/']
---

# TiDB CloudサーバーレスDriver（ベータ版） {#tidb-cloud-serverless-driver-beta}

> **注記：**
>
> サーバーレスドライバーはベータ版であり、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにのみ適用可能です。

## TiDB Cloud Serverless Driver （ベータ版）を使用する理由 {#why-use-tidb-cloud-serverless-driver-beta}

従来のTCPベースのMySQLドライバは、サーバーレス関数の短命な性質と矛盾する、長期間持続するTCP接続を前提としているため、サーバーレス関数には適していません。さらに、 [Vercel Edgeの機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare Workers](https://workers.cloudflare.com/)などのエッジ環境では、包括的なTCPサポートと完全なNode.js互換性が欠けている場合があり、これらのドライバは全く動作しない可能性があります。

[TiDB Cloudサーバーレスドライバー（ベータ版）](https://github.com/tidbcloud/serverless-js) for JavaScript を使用すると、サーバーレス環境で一般的にサポートされている HTTP 経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続できます。これにより、エッジ環境からTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続し、従来の TCP ベースの MySQL ドライバーと同様の開発エクスペリエンスを維持しながら、TCP による接続オーバーヘッドを削減することが可能になります。

> **注記：**
>
> SQL や ORM ではなく RESTful API を使用したプログラミングを好む場合は、 [データサービス（ベータ版）](https://docs.pingcap.com/tidbcloud/data-service-overview/)を使用できます。

## サーバーレスドライバーをインストールします {#install-the-serverless-driver}

npmを使ってドライバーをインストールできます。

```bash
npm install @tidbcloud/serverless
```

## サーバーレスドライバーを使用する {#use-the-serverless-driver}

サーバーレスドライバーを使用すると、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのデータを照会したり、対話型トランザクションを実行したりできます。

### クエリ {#query}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスからデータをクエリするには、まず接続を作成する必要があります。その後、その接続を使用して生のSQLクエリを実行できます。例：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### トランザクション（実験的） {#transaction-experimental}

サーバーレスドライバーを使用して対話型トランザクションを実行することもできます。例：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin()

try {
  await tx.execute('insert into test values (1)')
  await tx.execute('select * from test')
  await tx.commit()
} catch (err) {
  await tx.rollback()
  throw err
}
```

## エッジの例 {#edge-examples}

エッジ環境でサーバーレスドライバーを使用する例をいくつかご紹介します。より詳しい例については、こちらの[ライブデモ](https://github.com/tidbcloud/car-sales-insight)もご覧ください。

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

[VercelでTiDB Cloudサーバーレスドライバーを使用する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-vercel)について詳しくは、こちらをご覧ください。

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

[Cloudflare WorkersでTiDB Cloudサーバーレスドライバーを使用する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-cloudflare)について詳しくご覧ください。

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

[NetlifyでTiDB Cloudサーバーレスドライバーを使用する](https://docs.pingcap.com/tidbcloud/integrate-tidbcloud-with-netlify#use-the-edge-function)について詳しくは、こちらをご覧ください。

</div>

<div label="Deno">

```ts
import { connect } from "npm:@tidbcloud/serverless"

const conn = connect({url: Deno.env.get('DATABASE_URL')})
const result = await conn.execute('show tables')
```

</div>

<div label="Bun">

```ts
import { connect } from "@tidbcloud/serverless"

const conn = connect({url: Bun.env.DATABASE_URL})
const result = await conn.execute('show tables')
```

</div>

</SimpleTab>

## サーバーレスドライバーを設定する {#configure-the-serverless-driver}

TiDB Cloudのサーバーレスドライバーは、接続レベルとSQLレベルの両方で設定できます。

### 接続レベル構成 {#connection-level-configurations}

接続レベルでは、以下の設定を行うことができます。

| 名前           | タイプ  | デフォルト値    | 説明                                                                                                                                                  |
| ------------ | ---- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `username`   | 弦    | 該当なし      | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのユーザー名。                                                                                              |
| `password`   | 弦    | 該当なし      | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのパスワード。                                                                                              |
| `host`       | 弦    | 該当なし      | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのホスト名。                                                                                               |
| `database`   | 弦    | `test`    | TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスのデータベース。                                                                                             |
| `url`        | 弦    | 該当なし      | データベースのURLを`mysql://[username]:[password]@[host]/[database]`形式で指定します。デフォルトのデータベースに接続する場合は、 `database`を省略できます。                                       |
| `fetch`      | 関数   | グローバルフェッチ | カスタムフェッチ関数。たとえば、node.js で`undici`フェッチを使用できます。                                                                                                       |
| `arrayMode`  | ブール値 | `false`   | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定してください。                                                                                          |
| `fullResult` | ブール値 | `false`   | 行だけでなく、結果オブジェクト全体を返すかどうか。より詳細な結果を取得するには、 `true`に設定します。                                                                                              |
| `decoders`   | 物体   | `{}`      | キーと値のペアの集合で、さまざまな列タイプに合わせてデコード処理をカスタマイズできます。各ペアでは、キーとして列タイプを指定し、値として対応する関数を指定できます。この関数は、TiDB Cloudサーバーレスドライバーから受け取った生の文字列値を引数として受け取り、デコードされた値を返します。 |

**データベースURL**

> **注記：**
>
> ユーザー名、パスワード、またはデータベース名に特殊文字が含まれている場合は、URL で渡す際にこれらの文字[パーセンテージエンコード](https://en.wikipedia.org/wiki/Percent-encoding)必要があります。たとえば、パスワード`password1@//?` URL では`password1%40%2F%2F%3F`のようにエンコードする必要があります。

`url`が設定されている場合、 `host` 、 `username` 、 `password` 、および`database`個別に設定する必要はありません。以下のコードは同等です。

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
> SQLレベルのオプションは、接続レベルの設定よりも優先順位が高くなります。

SQLレベルでは、以下のオプションを設定できます。

| オプション        | タイプ  | デフォルト値            | 説明                                                                                                                                                                                                                                                                                               |
| ------------ | ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `arrayMode`  | ブール値 | `false`           | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定してください。                                                                                                                                                                                                                                       |
| `fullResult` | ブール値 | `false`           | 行だけでなく、結果オブジェクト全体を返すかどうか。より詳細な結果を取得するには、 `true`に設定します。                                                                                                                                                                                                                                           |
| `isolation`  | 弦    | `REPEATABLE READ` | トランザクション分離レベルは、 `READ COMMITTED`または`REPEATABLE READ`に設定できます。                                                                                                                                                                                                                                     |
| `decoders`   | 物体   | `{}`              | キーと値のペアのコレクションで、さまざまな列タイプのデコード処理をカスタマイズできます。各ペアでは、キーとして列タイプを指定し、値として対応する関数を指定できます。この関数は、TiDB Cloudサーバーレス ドライバーから受け取った生の文字列値を引数として受け取り、デコードされた値を返します。接続レベルと SQL レベルの両方で`decoders`を設定している場合、接続レベルで設定された異なるキーを持つキーと値のペアが SQL レベルにマージされて有効になります。両方のレベルで同じキー (つまり、列タイプ) が指定されている場合は、SQL レベルの値が優先されます。 |

**arrayMode と fullResult**

結果オブジェクト全体を配列として返すには、 `arrayMode`および`fullResult`オプションを次のように設定します。

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

**分離**

`isolation`オプションは、 `begin`関数でのみ使用できます。

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

**デコーダー**

返される列値のフォーマットをカスタマイズするには、 `decoder`メソッドの`connect()`オプションを次のように設定します。

```ts
import { connect, ColumnType } from '@tidbcloud/serverless';

const conn = connect({
  url: 'mysql://[username]:[password]@[host]/[database]',
  decoders: {
    // By default, TiDB Cloud serverless driver returns the BIGINT type as text value. This decoder converts BIGINT to the JavaScript built-in BigInt type.
    [ColumnType.BIGINT]: (rawValue: string) => BigInt(rawValue),
    
    // By default, TiDB Cloud serverless driver returns the DATETIME type as the text value in the 'yyyy-MM-dd HH:mm:ss' format. This decoder converts the DATETIME text to the JavaScript native Date object.
    [ColumnType.DATETIME]: (rawValue: string) => new Date(rawValue),
  }
})

// You can also configure the decoder option at the SQL level to override the decoders with the same keys at the connection level.
conn.execute(`select ...`, [], {
  decoders: {
    // ...
  }
})
```

> **注記：**
>
> TiDB Cloudサーバーレスドライバの設定変更点：
>
> -   v0.0.7: SQL レベル オプション`isolation`を追加します。
> -   v0.0.10: 接続レベル構成`decoders`と SQL レベルオプション`decoders`を追加します。

## 特徴 {#features}

### サポートされているSQLステートメント {#supported-sql-statements}

DDL がサポートされており、次の SQL ステートメントがサポートされています: `SELECT` 、 `SHOW` 、 `EXPLAIN` 、 `USE` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `BEGIN` 、 `COMMIT` 、 `ROLLBACK` 、および`SET` 。

### データ型マッピング {#data-type-mapping}

TiDBとJavaScript間の型マッピングは以下のとおりです。

| TiDBデータ型    | JavaScriptタイプ |
| ----------- | ------------- |
| TINYINT     | 番号            |
| 未署名TINYINT  | 番号            |
| ブール         | 番号            |
| スモールイント     | 番号            |
| 署名なしスモールイント | 番号            |
| メディウムミント    | 番号            |
| INT         | 番号            |
| 署名なしインターセプト | 番号            |
| 年           | 番号            |
| フロート        | 番号            |
| ダブル         | 番号            |
| ビッグイント      | 弦             |
| 符号なしBIGINT  | 弦             |
| 十進数         | 弦             |
| チャール        | 弦             |
| VARCHAR     | 弦             |
| バイナリ        | Uint8Array    |
| 二進法         | Uint8Array    |
| 小さな文字       | 弦             |
| TEXT        | 弦             |
| 中文          | 弦             |
| 長文          | 弦             |
| タイニーブロブ     | Uint8Array    |
| ブロブ         | Uint8Array    |
| 中型スロブ       | Uint8Array    |
| ロングブロブ      | Uint8Array    |
| 日付          | 弦             |
| 時間          | 弦             |
| 日時          | 弦             |
| タイムスタンプ     | 弦             |
| 列挙型         | 弦             |
| セット         | 弦             |
| 少し          | Uint8Array    |
| JSON        | 物体            |
| NULL        | ヌル            |
| その他         | 弦             |

> **注記：**
>
> TiDB Cloud TiDB Cloudのデフォルトの`utf8mb4` E}} 文字セットを使用するようにしてください。

> **注記：**
>
> TiDB Cloudサーバーレスドライバーのデータ型マッピングの変更点：
>
> -   v0.1.0: `BINARY` 、 `VARBINARY` 、 `TINYBLOB` 、 `BLOB` 、 `MEDIUMBLOB` 、 `LONGBLOB` 、および`BIT`型は、 `Uint8Array`ではなく、 `string` }として返されるようになりました。

### ORM連携 {#orm-integrations}

TiDB Cloudのサーバーレスドライバーは、以下のORMと統合されています。

-   [TiDB Cloudサーバーレスドライバー Kysely 方言](https://github.com/tidbcloud/kysely)。
-   [TiDB Cloudサーバーレス ドライバー Prisma アダプター](https://github.com/tidbcloud/prisma-adapter)。

## 価格設定 {#pricing}

サーバーレスドライバー自体は無料ですが、ドライバーを使用してデータにアクセスすると[要求単位（RU）](https://docs.pingcap.com/tidbcloud/tidb-cloud-glossary#request-unit-ru)とstorageの使用量が発生します。

-   TiDB Cloud Starterインスタンスの料金は、 [TiDB Cloud Starter の価格](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)モデルに従います。
-   TiDB Cloud Essentialインスタンスの場合、価格は[TiDB Cloud Essential の価格設定](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)モデルに従います。

## 制限事項 {#limitations}

現在、サーバーレスドライバーの使用には以下の制限があります。

-   1回のクエリで最大10,000行まで取得できます。
-   一度に実行できるSQL文は1つだけです。1つのクエリで複数のSQL文を実行することは、現時点ではサポートされていません。
-   [プライベートエンドポイント](https://docs.pingcap.com/tidbcloud/set-up-private-endpoint-connections-serverless.md)との接続にはまだ対応していません。
-   サーバーは、クロスオリジンリソース共有（CORS）を介して、許可されていないブラウザからのリクエストをブロックし、認証情報を保護します。そのため、サーバーレスドライバーはバックエンドサービスからのみ使用できます。

## 次は？ {#what-s-next}

-   [ローカルのNode.jsプロジェクトでTiDB Cloudサーバーレスドライバーを使用する](/develop/serverless-driver-node-example.md)方法を学びましょう。
