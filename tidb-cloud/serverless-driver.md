---
title: TiDB Cloud Serverless Driver (Beta)
summary: サーバーレス環境およびエッジ環境からTiDB Cloud Starter またはTiDB Cloud Essential に接続する方法を学習します。
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB CloudサーバーレスDriver(ベータ版) {#tidb-cloud-serverless-driver-beta}

> **注記：**
>
> サーバーレス ドライバーはベータ版であり、 TiDB Cloud Starter またはTiDB Cloud Essential クラスターにのみ適用されます。

## TiDB Cloud Serverless Driver (ベータ版) を使用する理由 {#why-use-tidb-cloud-serverless-driver-beta}

従来のTCPベースのMySQLドライバは、長寿命で永続的なTCP接続を前提としており、サーバーレス関数の短寿命な性質と矛盾するため、サーバーレス関数には適していません。さらに、包括的なTCPサポートと完全なNode.js互換性が欠如している可能性のある[Vercelエッジ関数](https://vercel.com/docs/functions/edge-functions)や[Cloudflareワーカー](https://workers.cloudflare.com/)などのエッジ環境では、これらのドライバが全く動作しない可能性があります。

JavaScript版の[TiDB Cloudサーバーレス ドライバー (ベータ版)](https://github.com/tidbcloud/serverless-js)使用すると、サーバーレス環境で一般的にサポートされているHTTP経由でTiDB Cloud StarterまたはTiDB Cloud Essentialクラスターに接続できます。これにより、エッジ環境からTiDB Cloud StarterまたはTiDB Cloud Essentialクラスターに接続し、従来のTCPベースのMySQLドライバーと同様の開発エクスペリエンスを維持しながら、TCPによる接続オーバーヘッドを削減できるようになります。

> **注記：**
>
> SQL や ORM ではなく RESTful API を使用してプログラミングしたい場合は、 [データサービス（ベータ版）](/tidb-cloud/data-service-overview.md)使用できます。

## サーバーレスドライバーをインストールする {#install-the-serverless-driver}

ドライバーは npm でインストールできます:

```bash
npm install @tidbcloud/serverless
```

## サーバーレスドライバーを使用する {#use-the-serverless-driver}

サーバーレス ドライバーを使用して、 TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータを照会したり、対話型トランザクションを実行したりできます。

### クエリ {#query}

TiDB Cloud StarterまたはTiDB Cloud Essentialクラスターからデータをクエリするには、まず接続を作成する必要があります。その後、その接続を使用して生のSQLクエリを実行できます。例：

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### トランザクション（実験的） {#transaction-experimental}

サーバーレスドライバーを使用してインタラクティブなトランザクションを実行することもできます。例:

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

エッジ環境でサーバーレスドライバーを使用する例をいくつかご紹介します。より詳細な例については、こちら[ライブデモ](https://github.com/tidbcloud/car-sales-insight)ご覧ください。

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

[VercelでTiDB Cloudサーバーレスドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)について詳しくご覧ください。

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

[Cloudflare WorkersでTiDB Cloudサーバーレスドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md)について詳しくご覧ください。

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

[NetlifyでTiDB Cloudサーバーレスドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function)について詳しくご覧ください。

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

## サーバーレスドライバーを構成する {#configure-the-serverless-driver}

TiDB Cloudサーバーレス ドライバーは、接続レベルと SQL レベルの両方で構成できます。

### 接続レベルの構成 {#connection-level-configurations}

接続レベルでは、次の構成を行うことができます。

| 名前           | タイプ | デフォルト値    | 説明                                                                                                                                                      |
| ------------ | --- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `username`   | 弦   | 該当なし      | クラスターのユーザー名。                                                                                                                                            |
| `password`   | 弦   | 該当なし      | クラスターのパスワード。                                                                                                                                            |
| `host`       | 弦   | 該当なし      | クラスターのホスト名。                                                                                                                                             |
| `database`   | 弦   | `test`    | クラスターのデータベース。                                                                                                                                           |
| `url`        | 弦   | 該当なし      | データベースの URL は`mysql://[username]:[password]@[host]/[database]`形式で、デフォルトのデータベースに接続する場合は`database`スキップできます。                                               |
| `fetch`      | 関数  | グローバルフェッチ | カスタムフェッチ関数。例えば、node.jsの`undici` fetch関数を使うことができます。                                                                                                      |
| `arrayMode`  | ブール | `false`   | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定してください。                                                                                              |
| `fullResult` | ブール | `false`   | 行だけでなく、完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、 `true`に設定してください。                                                                                              |
| `decoders`   | 物体  | `{}`      | キーと値のペアのコレクション。これにより、異なる列の型に応じてデコード処理をカスタマイズできます。各ペアでは、列の型をキーとして指定し、対応する関数を値として指定できます。この関数は、 TiDB Cloudサーバーレスドライバーから受信した生の文字列値を引数として受け取り、デコードされた値を返します。 |

**データベースURL**

> **注記：**
>
> ユーザー名、パスワード、またはデータベース名に特殊文字が含まれている場合、URLで渡す際にこれらの文字を[パーセンテージエンコード](https://en.wikipedia.org/wiki/Percent-encoding)文字にエンコードする必要があります。例えば、パスワードが`password1@//?`場合、URLでは`password1%40%2F%2F%3F`にエンコードする必要があります。

`url`設定されている場合、 `host` 、 `username` 、 `password` 、 `database`個別に設定する必要はありません。以下のコードは同等です。

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

### SQLレベルオプション {#sql-level-options}

> **注記：**
>
> SQL レベルのオプションは、接続レベルの構成よりも優先されます。

SQL レベルでは、次のオプションを構成できます。

| オプション        | タイプ | デフォルト値            | 説明                                                                                                                                                                                                                                                                                         |
| ------------ | --- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `arrayMode`  | ブール | `false`           | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定してください。                                                                                                                                                                                                                                 |
| `fullResult` | ブール | `false`           | 行だけでなく、完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、 `true`に設定してください。                                                                                                                                                                                                                                 |
| `isolation`  | 弦   | `REPEATABLE READ` | トランザクション分離レベル。 `READ COMMITTED`または`REPEATABLE READ`に設定できます。                                                                                                                                                                                                                                |
| `decoders`   | 物体  | `{}`              | キーと値のペアのコレクション。これにより、異なる列タイプに対するデコード処理をカスタマイズできます。各ペアでは、列タイプをキーとして指定し、対応する関数を値として指定できます。この関数は、 TiDB Cloudサーバーレスドライバーから受信した生の文字列値を引数として受け取り、デコードされた値を返します。接続レベルと SQL レベルの両方で`decoders`設定した場合、接続レベルで異なるキーが設定されたキーと値のペアは、SQL レベルにマージされて有効になります。両方のレベルで同じキー（列タイプ）が指定されている場合は、SQL レベルの値が優先されます。 |

**arrayMode と fullResult**

完全な結果オブジェクトを配列として返すには、オプション`arrayMode`と`fullResult`次のように構成します。

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```

**分離**

`isolation`オプションは`begin`機能でのみ使用できます。

```ts
const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const tx = await conn.begin({isolation:"READ COMMITTED"})
```

**デコーダー**

返される列の値の形式をカスタマイズするには、 `connect()`メソッドの`decoder`オプションを次のように構成します。

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
> TiDB Cloudサーバーレス ドライバーの構成の変更:
>
> -   v0.0.7: SQL レベル オプション`isolation`を追加します。
> -   v0.0.10: 接続レベル構成`decoders`と SQL レベル オプション`decoders`を追加します。

## 特徴 {#features}

### サポートされているSQL文 {#supported-sql-statements}

DDL がサポートされており、次の SQL ステートメントがサポートされています: `SELECT` 、 `SHOW` 、 `EXPLAIN` 、 `USE` 、 `INSERT` 、 `UPDATE` 、 `DELETE` 、 `BEGIN` 、 `COMMIT` 、 `ROLLBACK` 、および`SET` 。

### データ型のマッピング {#data-type-mapping}

TiDB と Javascript 間の型マッピングは次のとおりです。

| TiDBデータ型    | Javascriptタイプ |
| ----------- | ------------- |
| タイニーイント     | 番号            |
| 符号なしTINYINT | 番号            |
| ブール         | 番号            |
| スモールイント     | 番号            |
| 符号なしスモール整数  | 番号            |
| ミディアムミント    | 番号            |
| INT         | 番号            |
| 符号なし整数      | 番号            |
| 年           | 番号            |
| フロート        | 番号            |
| ダブル         | 番号            |
| ビッグイント      | 弦             |
| 符号なしBIGINT  | 弦             |
| 小数点         | 弦             |
| チャー         | 弦             |
| ヴァルチャー      | 弦             |
| バイナリ        | Uint8配列       |
| VARBINARY   | Uint8配列       |
| 小さなテキスト     | 弦             |
| TEXT        | 弦             |
| 中テキスト       | 弦             |
| 長文          | 弦             |
| タイニーブロブ     | Uint8配列       |
| ブロブ         | Uint8配列       |
| ミディアムブロブ    | Uint8配列       |
| ロングブロブ      | Uint8配列       |
| 日付          | 弦             |
| 時間          | 弦             |
| 日時          | 弦             |
| タイムスタンプ     | 弦             |
| 列挙型         | 弦             |
| セット         | 弦             |
| 少し          | Uint8配列       |
| JSON        | 物体            |
| ヌル          | ヌル            |
| その他         | 弦             |

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーは UTF-8 エンコードを使用して JavaScript 文字列を文字列にデコードするため、JavaScript 文字列への型変換には必ずTiDB Cloudのデフォルトの`utf8mb4`文字セットを使用してください。

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーのデータ型マッピングの変更:
>
> -   v0.1.0: `BINARY` 、 `VARBINARY` 、 `TINYBLOB` 、 `BLOB` 、 `MEDIUMBLOB` 、 `LONGBLOB` 、 `BIT`型は、 `string`ではなく`Uint8Array`として返されるようになりました。

### ORM統合 {#orm-integrations}

TiDB Cloudサーバーレス ドライバーは、次の ORM と統合されています。

-   [TiDB Cloudサーバーレス ドライバー Kysely 方言](https://github.com/tidbcloud/kysely) 。
-   [TiDB Cloudサーバーレス ドライバー Prisma アダプター](https://github.com/tidbcloud/prisma-adapter) 。

## 価格 {#pricing}

サーバーレス ドライバー自体は無料ですが、ドライバーを使用してデータにアクセスすると、 [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)とstorage使用量が発生します。

-   TiDB Cloud Starter クラスターの場合、価格は[TiDB Cloud Starterの価格](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)モデルに従います。
-   TiDB Cloud Essential クラスターの場合、価格は[TiDB Cloud Essential の価格](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)モデルに従います。

## 制限事項 {#limitations}

現在、サーバーレス ドライバーの使用には次の制限があります。

-   1 回のクエリで最大 10,000 行を取得できます。
-   一度に実行できるSQL文は1つだけです。1つのクエリで複数のSQL文を実行することはまだサポートされていません。
-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)との接続はまだサポートされていません。

## 次は何？ {#what-s-next}

-   [ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/serverless-driver-node-example.md)方法を学習します。
