---
title: TiDB Cloud Serverless Driver Node.js Tutorial
summary: ローカルのNode.jsプロジェクトでTiDB Cloudサーバーレスドライバーを使用する方法を学びましょう。
aliases: ['/ja/tidbcloud/serverless-driver-node-example/']
---

# TiDB Cloud Serverless Driver Node.js チュートリアル {#tidb-cloud-serverless-driver-node-js-tutorial}

このチュートリアルでは、ローカルのNode.jsプロジェクトでTiDB Cloudサーバーレスドライバーを使用する方法について説明します。

> **注記：**
>
> -   このドキュメントの手順は、 TiDB Cloud Starterインスタンスに加えて、 TiDB Cloud Essentialインスタンスでも適用できます。
> -   Cloudflare Workers、Vercel Edge Functions、および Netlify Edge Functions でTiDB Cloudサーバーレス ドライバーを使用する方法については、[自動車販売に関する洞察](https://car-sales-insight.vercel.app/)と[サンプルリポジトリ](https://github.com/tidbcloud/car-sales-insight)を確認してください。

## 始める前に {#before-you-begin}

このステップバイステップのチュートリアルを完了するには、以下のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 18.0.0。
-   [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 、またはお好みのパッケージマネージャーを使用してください。
-   TiDB Cloud Starterインスタンス。お持ちでない場合は、 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。

## ステップ1. ローカルのNode.jsプロジェクトを作成する {#step-1-create-a-local-node-js-project}

1.  `node-example`という名前のプロジェクトを作成します。

    ```shell
    mkdir node-example
    cd node-example
    ```

2.  npmまたはお好みのパッケージマネージャーを使用して、 TiDB Cloudサーバーレスドライバーをインストールしてください。

    以下のコマンドは、npm を使用したインストールを例として示しています。このコマンドを実行すると、プロジェクトディレクトリ内に`node_modules`ディレクトリと`package.json`ファイルが作成されます。

        npm install @tidbcloud/serverless

## ステップ2. サーバーレスドライバーを使用する {#step-2-use-the-serverless-driver}

サーバーレスドライバーは、CommonJSモジュールとESモジュールの両方をサポートしています。以下の手順では、ESモジュールの使用例を示します。

1.  TiDB Cloud Starterインスタンスの概要ページで、右上隅の**「接続」**をクリックし、表示されたダイアログからデータベースの接続文字列を取得します。接続文字列は次のようになります。

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

3.  プロジェクトディレクトリに`index.js`という名前のファイルを作成し、以下のコードを追加してください。

    ```js
    import { connect } from '@tidbcloud/serverless'

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Cloud Starter instance information
    console.log(await conn.execute("show tables"))
    ```

4.  以下のコマンドでプロジェクトを実行してください。

        node index.js

## 以前のバージョンのNode.jsとの互換性 {#compatibility-with-earlier-versions-of-node-js}

Node.js 18.0.0 より前のバージョンを使用しており、グローバルな`fetch`関数がない場合は、以下の手順で`fetch`を取得できます。

1.  `fetch`を提供するパッケージをインストールしてください。例えば`undici`などです。

        npm install undici

2.  `fetch`関数を`connect`関数に渡します。

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'

    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```
