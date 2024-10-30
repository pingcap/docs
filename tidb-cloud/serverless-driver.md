---
title: TiDB Cloud Serverless Driver (Beta)
summary: サーバーレス環境およびエッジ環境からTiDB Cloud Serverless に接続する方法を学習します。
aliases: ['/tidbcloud/serverless-driver-config']
---

# TiDB CloudサーバーレスDriver(ベータ版) {#tidb-cloud-serverless-driver-beta}

## TiDB Cloud Serverless Driver (ベータ版) を使用する理由 {#why-use-tidb-cloud-serverless-driver-beta}

従来の TCP ベースの MySQL ドライバーは、長寿命で永続的な TCP 接続を期待しているため、サーバーレス関数には適していません。これは、サーバーレス関数の短寿命の性質と矛盾しています。さらに、包括的な TCP サポートと完全な Node.js 互換性が欠如している可能性のある[Vercel エッジ機能](https://vercel.com/docs/functions/edge-functions)や[Cloudflare ワーカー](https://workers.cloudflare.com/)などのエッジ環境では、これらのドライバーがまったく機能しない可能性があります。

JavaScript 用の[TiDB Cloudサーバーレス ドライバー (ベータ版)](https://github.com/tidbcloud/serverless-js)使用すると、サーバーレス環境で一般的にサポートされている HTTP 経由でTiDB Cloud Serverless クラスターに接続できます。これにより、従来の TCP ベースの MySQL ドライバーと同様の開発エクスペリエンスを維持しながら、エッジ環境からTiDB Cloud Serverless クラスターに接続し、TCP による接続オーバーヘッドを削減できるようになりました。

> **注記：**
>
> SQL や ORM ではなく RESTful API でプログラミングしたい場合は、 [データ サービス (ベータ版)](/tidb-cloud/data-service-overview.md)使用できます。

## サーバーレスドライバーをインストールする {#install-the-serverless-driver}

npm を使用してドライバーをインストールできます。

```bash
npm install @tidbcloud/serverless
```

## サーバーレスドライバーを使用する {#use-the-serverless-driver}

サーバーレス ドライバーを使用して、 TiDB Cloud Serverless クラスターのデータを照会したり、対話型トランザクションを実行したりできます。

### クエリ {#query}

TiDB Cloud Serverless クラスターからデータをクエリするには、まず接続を作成する必要があります。次に、接続を使用して生の SQL クエリを実行できます。例:

```ts
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'})
const results = await conn.execute('select * from test where id = ?',[1])
```

### トランザクション（実験的） {#transaction-experimental}

サーバーレス ドライバーを使用して対話型トランザクションを実行することもできます。例:

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

エッジ環境でサーバーレス ドライバーを使用する例をいくつか示します。完全な例については、こちら[ライブデモ](https://github.com/tidbcloud/car-sales-insight)も試してください。

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

[Vercel でTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-vercel.md)について詳しく学びます。

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

[Cloudflare Workers でTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-cloudflare.md)について詳しく学びます。

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

[Netlify でTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/integrate-tidbcloud-with-netlify.md#use-the-edge-function)について詳しく学びます。

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

| 名前           | タイプ | デフォルト値    | 説明                                                                                                                                                           |
| ------------ | --- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `username`   | 弦   | 該当なし      | TiDB Cloud Serverlessのユーザー名                                                                                                                                  |
| `password`   | 弦   | 該当なし      | TiDB Cloud Serverlessのパスワード                                                                                                                                  |
| `host`       | 弦   | 該当なし      | TiDB Cloud Serverlessのホスト名                                                                                                                                   |
| `database`   | 弦   | `test`    | TiDB Cloud Serverlessのデータベース                                                                                                                                 |
| `url`        | 弦   | 該当なし      | データベースの URL は`mysql://[username]:[password]@[host]/[database]`形式で、デフォルトのデータベースに接続する場合は`database`スキップできます。                                                    |
| `fetch`      | 関数  | グローバルフェッチ | カスタム フェッチ関数。たとえば、node.js の`undici`フェッチを使用できます。                                                                                                               |
| `arrayMode`  | ブール | `false`   | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定します。                                                                                                      |
| `fullResult` | ブール | `false`   | 行だけではなく完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、 `true`に設定します。                                                                                                      |
| `decoders`   | 物体  | `{}`      | キーと値のペアのコレクション。これにより、さまざまな列タイプのデコード プロセスをカスタマイズできます。各ペアでは、列タイプをキーとして指定し、対応する関数を値として指定できます。この関数は、 TiDB Cloudサーバーレス ドライバーから受信した生の文字列値を引数として受け取り、デコードされた値を返します。 |

**データベースURL**

> **注記：**
>
> ユーザー名、パスワード、またはデータベース名に特殊文字が含まれている場合は、URL で渡すときにこれらの文字を[パーセンテージエンコード](https://en.wikipedia.org/wiki/Percent-encoding)エンコードする必要があります。たとえば、パスワード`password1@//?` 、URL では`password1%40%2F%2F%3F`としてエンコードする必要があります。

`url`設定されている場合、 `host` 、 `username` 、 `password` 、および`database`個別に設定する必要はありません。次のコードは同等です。

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

### SQL レベル オプション {#sql-level-options}

> **注記：**
>
> SQL レベルのオプションは、接続レベルの構成よりも優先されます。

SQL レベルでは、次のオプションを構成できます。

| オプション        | タイプ | デフォルト値            | 説明                                                                                                                                                                                                                                                                                                  |
| ------------ | --- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `arrayMode`  | ブール | `false`           | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定します。                                                                                                                                                                                                                                             |
| `fullResult` | ブール | `false`           | 行だけではなく、完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、 `true`に設定します。                                                                                                                                                                                                                                            |
| `isolation`  | 弦   | `REPEATABLE READ` | トランザクション分離レベル。 `READ COMMITTED`または`REPEATABLE READ`に設定できます。                                                                                                                                                                                                                                         |
| `decoders`   | 物体  | `{}`              | キーと値のペアのコレクション。これにより、さまざまな列の種類のデコード処理をカスタマイズできます。各ペアでは、列の種類をキーとして指定し、対応する関数を値として指定できます。この関数は、 TiDB Cloudサーバーレス ドライバーから受け取った生の文字列値を引数として受け取り、デコードされた値を返します。接続レベルと SQL レベルの両方で`decoders`設定した場合、接続レベルで設定された異なるキーを持つキーと値のペアは、SQL レベルにマージされて有効になります。両方のレベルで同じキー (つまり、列の種類) が指定されている場合は、SQL レベルの値が優先されます。 |

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
> TiDB Cloudサーバーレス ドライバー構成の変更:
>
> -   v0.0.7: SQL レベル オプション`isolation`を追加します。
> -   v0.0.10: 接続レベルの構成`decoders`と SQL レベル オプション`decoders`を追加します。

## 特徴 {#features}

### サポートされているSQL文 {#supported-sql-statements}

DDL がサポートされ`DELETE` `UPDATE` 、次の`SET`ステートメント`EXPLAIN`サポートされ`SHOW` `USE` `INSERT` `COMMIT` `SELECT` `BEGIN`および`ROLLBACK` 。

### データ型マッピング {#data-type-mapping}

TiDB Cloud Serverless と Javascript 間の型マッピングは次のとおりです。

| TiDB Cloudサーバーレスタイプ | Javascriptタイプ |
| ------------------- | ------------- |
| 小さな                 | 番号            |
| 符号なし TINYINT        | 番号            |
| ブール                 | 番号            |
| スモールイント             | 番号            |
| 符号なし小整数             | 番号            |
| ミディアムミント            | 番号            |
| 内部                  | 番号            |
| 符号なし整数              | 番号            |
| 年                   | 番号            |
| フロート                | 番号            |
| ダブル                 | 番号            |
| ビッグイント              | 弦             |
| 符号なしBIGINT          | 弦             |
| 小数点                 | 弦             |
| 文字                  | 弦             |
| バルチャー               | 弦             |
| バイナリ                | Uint8配列       |
| バイナリ                | Uint8配列       |
| 小さなテキスト             | 弦             |
| TEXT                | 弦             |
| 中テキスト               | 弦             |
| 長文                  | 弦             |
| タイニーブロブ             | Uint8配列       |
| ブロブ                 | Uint8配列       |
| ミディアムブロブ            | Uint8配列       |
| ロングロブ               | Uint8配列       |
| 日付                  | 弦             |
| 時間                  | 弦             |
| 日時                  | 弦             |
| タイムスタンプ             | 弦             |
| 列挙                  | 弦             |
| セット                 | 弦             |
| 少し                  | Uint8配列       |
| 翻訳                  | 物体            |
| NULL                | ヌル            |
| その他                 | 弦             |

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーは UTF-8 エンコーディングを使用して JavaScript 文字列を文字列にデコードするため、JavaScript 文字列への型変換にはTiDB Cloudサーバーレスのデフォルトの`utf8mb4`文字セットを使用するようにしてください。

> **注記：**
>
> TiDB Cloudサーバーレス ドライバーのデータ型マッピングの変更:
>
> -   v0.1.0: `BINARY` 、 `VARBINARY` 、 `TINYBLOB` 、 `BLOB` 、 `MEDIUMBLOB` 、 `LONGBLOB` 、および`BIT`タイプは、 `string`ではなく`Uint8Array`として返されるようになりました。

### ORM統合 {#orm-integrations}

TiDB Cloudサーバーレス ドライバーは、次の ORM と統合されています。

-   [TiDB Cloudサーバーレス ドライバー Kysely 方言](https://github.com/tidbcloud/kysely) 。
-   [TiDB Cloudサーバーレス ドライバー Prisma アダプター](https://github.com/tidbcloud/prisma-adapter) 。

## 価格 {#pricing}

サーバーレス ドライバー自体は無料ですが、ドライバーを使用してデータにアクセスすると[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)とstorage使用量が発生します。価格は[TiDB Cloud Serverless の価格](https://www.pingcap.com/tidb-serverless-pricing-details/)モデルに従います。

## 制限事項 {#limitations}

現在、サーバーレス ドライバーの使用には次の制限があります。

-   1 回のクエリで最大 10,000 行を取得できます。
-   一度に実行できる SQL ステートメントは 1 つだけです。1 つのクエリで複数の SQL ステートメントを実行することはまだサポートされていません。
-   [プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)との接続はまだサポートされていません。

## 次は何か {#what-s-next}

-   [ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する](/tidb-cloud/serverless-driver-node-example.md)方法を学びます。
