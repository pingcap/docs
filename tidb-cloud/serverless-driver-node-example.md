---
title: TiDB Cloud Serverless Driver Node.js Tutorial
summary: Learn how to use TiDB Cloud serverless driver in a local Node.js project.
---

# TiDB CloudサーバーレスDriverNode.js チュートリアル {#tidb-cloud-serverless-driver-node-js-tutorial}

このチュートリアルでは、ローカル Node.js プロジェクトでTiDB Cloudサーバーレス ドライバーを使用する方法について説明します。

> **注記：**
>
> -   このチュートリアルは、TiDB サーバーレス クラスターにのみ適用されます。
> -   Cloudflare Workers、Vercel Edge Functions、および Netlify Edge Functions でTiDB Cloudサーバーレス ドライバーを使用する方法については、 [自動車販売に関する洞察](https://car-sales-insight.vercel.app/)と「 [サンプルリポジトリ](https://github.com/tidbcloud/car-sales-insight)を参照してください。

## あなたが始める前に {#before-you-begin}

この段階的なチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)または好みのパッケージ マネージャー。
-   TiDB サーバーレス クラスター。何も持っていない場合は、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)を実行できます。

## ステップ 1. ローカル Node.js プロジェクトを作成する {#step-1-create-a-local-node-js-project}

1.  `node-example`という名前のプロジェクトを作成します。

    ```shell
    mkdir node-example
    cd node-example
    ```

2.  npm または任意のパッケージ マネージャーを使用して、 TiDB Cloudサーバーレス ドライバーをインストールします。

    次のコマンドは、npm を使用したインストールを例にしています。このコマンドを実行すると、プロジェクト ディレクトリに`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/serverless

## ステップ 2. サーバーレスドライバーを使用する {#step-2-use-the-serverless-driver}

サーバーレス ドライバーは、CommonJS モジュールと ES モジュールの両方をサポートします。次の手順では、ES モジュールの使用例を取り上げます。

1.  TiDB Cloudサーバーレス クラスターの概要ページで、右上隅の**[接続]**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

        mysql://[username]:[password]@[host]/[database]

2.  `package.json`ファイルに`type: "module"`を追加して ES モジュールを指定します。

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

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Serverless cluster information
    console.log(await conn.execute("show tables"))
    ```

4.  次のコマンドを使用してプロジェクトを実行します。

        node index.js

## 以前のバージョンの Node.js との互換性 {#compatability-with-earlier-versions-of-node-js}

グローバル`fetch`関数を持たない 18.0.0 より前の Node.js を使用している場合は、次の手順を実行して`fetch`を取得できます。

1.  `fetch`を提供するパッケージ ( `undici`など) をインストールします。

        npm install undici

2.  `fetch`関数を`connect`関数に渡します。

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```
