---
title: Configure TiDB Cloud Serverless Driver (Beta)
summary: Learn how to configure TiDB Cloud Serverless Driver.
---

# TiDB CloudサーバーレスDriverの構成 (ベータ版) {#configure-tidb-cloud-serverless-driver-beta}

TiDB Cloudサーバーレス ドライバーは、接続レベルと SQL レベルの両方で構成できます。

## 接続レベルの構成 {#connection-level-configurations}

接続レベルでは、次の構成を行うことができます。

| 名前           | タイプ | デフォルト値    | 説明                                                                                                |
| ------------ | --- | --------- | ------------------------------------------------------------------------------------------------- |
| `username`   | 弦   | 該当なし      | TiDB サーバーレスのユーザー名                                                                                 |
| `password`   | 弦   | 該当なし      | TiDBサーバーレスのパスワード                                                                                  |
| `host`       | 弦   | 該当なし      | TiDB サーバーレスのホスト名                                                                                  |
| `database`   | 弦   | `test`    | TiDBサーバーレスのデータベース                                                                                 |
| `url`        | 弦   | 該当なし      | データベースの URL ( `mysql://username:password@host/database`形式)。デフォルトのデータベースに接続する場合は`database`を省略できます。 |
| `fetch`      | 関数  | グローバルフェッチ | カスタムフェッチ関数。たとえば、node.js で`undici`フェッチを使用できます。                                                     |
| `arrayMode`  | ブール | `false`   | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、これを`true`に設定します。                                         |
| `fullResult` | ブール | `false`   | 行だけではなく完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、これを`true`に設定します。                                         |

### データベースのURL {#database-url}

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
  url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database',
  arrayMode: true
}

const conn = connect(config)
```

## SQLレベルのオプション {#sql-level-options}

> **注記：**
>
> SQL レベルのオプションは、接続レベルの設定よりも優先されます。

SQL レベルでは、次のオプションを構成できます。

| オプション        | タイプ | デフォルト値  | 説明                                                        |
| ------------ | --- | ------- | --------------------------------------------------------- |
| `arrayMode`  | ブール | `false` | 結果をオブジェクトではなく配列として返すかどうか。パフォーマンスを向上させるには、 `true`に設定します。   |
| `fullResult` | ブール | `false` | 行だけではなく完全な結果オブジェクトを返すかどうか。より詳細な結果を取得するには、これを`true`に設定します。 |

例えば：

```ts
const conn = connect({url: process.env['DATABASE_URL'] || 'mysql://username:password@host/database'})
const results = await conn.execute('select * from test',null,{arrayMode:true,fullResult:true})
```
