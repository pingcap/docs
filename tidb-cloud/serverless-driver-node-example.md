---
title: TiDB Cloud Serverless Driver Node.js Tutorial
summary: ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する方法を学習します。
---

# TiDB CloudレスDriverNode.js チュートリアル {#tidb-cloud-serverless-driver-node-js-tutorial}

このチュートリアルでは、ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

> **注記：**
>
> -   このチュートリアルは、 TiDB Cloud Serverless クラスターにのみ適用されます。
> -   Cloudflare Workers、Vercel Edge Functions、Netlify Edge Functions でTiDB Cloudサーバーレス ドライバーを使用する方法については、 [自動車販売に関する洞察](https://car-sales-insight.vercel.app/)と[サンプルリポジトリ](https://github.com/tidbcloud/car-sales-insight)ご覧ください。

## 始める前に {#before-you-begin}

このステップバイステップのチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [ネプ](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)またはお好みのパッケージ マネージャーを使用します。
-   TiDB Cloud Serverless クラスター。ない場合は、 [TiDB Cloud Serverless クラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)使用できます。

## ステップ1. ローカルNode.jsプロジェクトを作成する {#step-1-create-a-local-node-js-project}

1.  `node-example`という名前のプロジェクトを作成します。

    ```shell
    mkdir node-example
    cd node-example
    ```

2.  npm または任意のパッケージ マネージャーを使用して、 TiDB Cloudサーバーレス ドライバーをインストールします。

    次のコマンドは、npm を使用したインストールを例にしています。このコマンドを実行すると、プロジェクト ディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/serverless

## ステップ2. サーバーレスドライバーを使用する {#step-2-use-the-serverless-driver}

サーバーレス ドライバーは、CommonJS モジュールと ES モジュールの両方をサポートしています。次の手順では、ES モジュールの使用例を示します。

1.  TiDB Cloud Serverless クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されるダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

2.  `package.json`ファイルで、 `type: "module"`を追加して ES モジュールを指定します。

    例えば：

    ```json
    {
      "type": "module",
      "dependencies": {
        "@tidbcloud/serverless": "^0.0.7",
      }
    }
    ```

3.  プロジェクト ディレクトリに`index.js`という名前のファイルを作成し、次のコードを追加します。

    ```js
    import { connect } from '@tidbcloud/serverless'

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Cloud Serverless cluster information
    console.log(await conn.execute("show tables"))
    ```

4.  次のコマンドでプロジェクトを実行します。

        node index.js

## Node.js の以前のバージョンとの互換性 {#compatibility-with-earlier-versions-of-node-js}

グローバル`fetch`関数を持たない Node.js 18.0.0 より前のバージョンを使用している場合は、次の手順で`fetch`を取得できます。

1.  `fetch` （ `undici`など）を提供するパッケージをインストールします。

        npm install undici

2.  `fetch`関数を`connect`関数に渡します。

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```
