---
title: Integrate TiDB Cloud with Netlify
summary: TiDB CloudクラスターをNetlifyプロジェクトに接続する方法を学びましょう。
---

# TiDB CloudとNetlifyを統合する {#integrate-tidb-cloud-with-netlify}

[Netlify](https://netlify.com/) 、最新のWebプロジェクトを自動化するためのオールインワンプラットフォームです。ホスティングインフラストラクチャ、継続的インテグレーション、デプロイメントパイプラインを単一のワークフローに置き換え、プロジェクトの成長に合わせてサーバーレス関数、ユーザー認証、フォーム処理などの動的な機能を統合します。

このドキュメントでは、データベースバックエンドとしてTiDB Cloudを使用してNetlify上にフルスタックアプリをデプロイする方法について説明します。また、 TiDB Cloudサーバーレスドライバーを使用してNetlifyエッジ関数を利用する方法についても学ぶことができます。

## 前提条件 {#prerequisites}

展開前に、以下の前提条件が満たされていることを確認してください。

### NetlifyアカウントとCLI {#a-netlify-account-and-cli}

NetlifyアカウントとCLIをお持ちであることが前提となります。お持ちでない場合は、以下のリンクを参照して作成してください。

-   [Netlifyアカウントに登録する](https://app.netlify.com/signup)。
-   [Netlify CLI を入手](https://docs.netlify.com/cli/get-started/)。

### TiDB CloudアカウントとTiDB Cloudリソース {#a-tidb-cloud-account-and-a-tidb-cloud-resource}

アカウントとTiDB Cloudリソースをお持ちであることが前提となります。お持ちでない場合は、以下の手順に従って作成してください。

-   [TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)
-   [TiDB Cloud Dedicatedクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

TiDB Cloudのリソース1つで、複数のNetlifyサイトに接続できます。

### TiDB Cloudのトラフィックフィルタで許可されているすべてのIPアドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

TiDB Cloud Dedicatedクラスターの場合、クラスターのトラフィックフィルターで、すべての IP アドレスからの接続を許可する設定（ `0.0.0.0/0` } に設定）になっていることを確認してください。これは、Netlify のデプロイメントでは動的 IP アドレスが使用されるためです。

TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスは、デフォルトで全てのIPアドレスからの接続を許可するため、トラフィックフィルタを設定する必要はありません。

## ステップ1. サンプルプロジェクトと接続文字列を取得します。 {#step-1-get-the-example-project-and-the-connection-string}

TiDB Cloudは、すぐに開発を始められるように、TypeScriptとNext.js、React、Prisma Clientを使用したフルスタックのサンプルアプリを提供しています。これは、ブログ記事の投稿や削除ができるシンプルなブログサイトです。すべてのコンテンツはPrismaを介してTiDB Cloudに保存されます。

### サンプルプロジェクトをフォークして、自分のスペースにクローンしてください。 {#fork-the-example-project-and-clone-it-to-your-own-space}

1.  [Next.jsとPrismaを使用したフルスタックの例](https://github.com/tidbcloud/nextjs-prisma-example)リポジトリを自分のGitHubリポジトリにフォークします。

2.  フォークしたリポジトリを自分のスペースにクローンしてください。

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### TiDB Cloud接続文字列を取得します {#get-the-tidb-cloud-connection-string}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの場合、接続文字列は[TiDB Cloud CLI](/tidb-cloud/cli-reference.md)または[TiDB Cloudコンソール](https://tidbcloud.com/)から取得できます。 。

TiDB Cloud Dedicatedクラスタの場合、接続文字列はTiDB Cloudコンソールからのみ取得できます。

<SimpleTab>
<div label="TiDB Cloud CLI">

> **ヒント：**
>
> Cloud CLI をインストールしていない場合は、次の手順を実行する前に、 [TiDB Cloud CLI クイックスタート](/tidb-cloud/get-started-with-cli.md)を参照して簡単にインストールしてください。

1.  TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの接続文字列を対話モードで取得します。

    ```shell
    ticloud cluster connect-info
    ```

2.  プロンプトに従って、 TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンス、クライアント、およびオペレーティングシステムを選択してください。なお、このドキュメントで使用されているクライアントは`Prisma`です。

        Choose the cluster
        > [x] Cluster0(13796194496)
        Choose the client
        > [x] Prisma
        Choose the operating system
        > [x] macOS/Alpine (Detected)

    出力は以下のとおりです。 `url`の値の中に Prisma の接続文字列があります。

    ```shell
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **注記：**
    >
    > 後で接続文字列を使用する際は、以下の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えてください。
    > -   このドキュメントのサンプルアプリでは新しいデータベースが必要なので、 `<Database>`固有の新しい名前に置き換える必要があります。

</div>
<div label="TiDB Cloud console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)では、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットリソースの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。表示されたダイアログで、接続文字列から以下の接続パラメータを取得できます。

    -   `${host}`
    -   `${port}`
    -   `${user}`
    -   `${password}`

2.  以下の接続文字列に接続パラメータを入力してください。

    ```shell
    mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
    ```

    > **注記：**
    >
    > 後で接続文字列を使用する際は、以下の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えてください。
    > -   このドキュメントのサンプルアプリでは新しいデータベースが必要なので、 `<Database>`固有の新しい名前に置き換える必要があります。

</div>
</SimpleTab>

## ステップ2. サンプルアプリをNetlifyにデプロイ {#step-2-deploy-the-example-app-to-netlify}

1.  Netlify CLIで、Netlifyアカウントを認証し、アクセストークンを取得します。

    ```shell
    netlify login
    ```

2.  自動セットアップを開始します。この手順では、継続的デプロイのためにリポジトリを接続するため、Netlify CLI がリポジトリ上にデプロイキーとウェブフックを作成するためのアクセス権が必要です。

    ```shell
    netlify init
    ```

    プロンプトが表示されたら、 **「新しいサイトを作成して設定する」**を選択し、GitHub にアクセス権を付与してください。その他のオプションはすべてデフォルト値を使用してください。

    ```shell
    Adding local .netlify folder to .gitignore file...
    ? What would you like to do? +  Create & configure a new site
    ? Team: your_username’s team
    ? Site name (leave blank for a random name; you can change it later):

    Site Created

    Admin URL: https://app.netlify.com/sites/mellow-crepe-e2ca2b
    URL:       https://mellow-crepe-e2ca2b.netlify.app
    Site ID:   b23d1359-1059-49ed-9d08-ed5dba8e83a2

    Linked to mellow-crepe-e2ca2b


    ? Netlify CLI needs access to your GitHub account to configure Webhooks and Deploy Keys. What would you like to do? Authorize with GitHub through app.netlify.com
    Configuring Next.js runtime...

    ? Your build command (hugo build/yarn run build/etc): npm run netlify-build
    ? Directory to deploy (blank for current dir): .next

    Adding deploy key to repository...
    (node:36812) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
    (Use `node --trace-warnings ...` to show where the warning was created)
    Deploy key added!

    Creating Netlify GitHub Notification Hooks...
    Netlify Notification Hooks configured!

    Success! Netlify CI/CD Configured!

    This site is now configured to automatically deploy from github branches & pull requests

    Next steps:

    git push       Push to your git repository to trigger new site builds
    netlify open   Open the Netlify admin URL of your site
    ```

3.  環境変数を設定します。自分のスペースと Netlify スペースからTiDB Cloudに接続するには、 [ステップ1](#step-1-get-the-example-project-and-the-connection-string)で取得した接続文字列として`DATABASE_URL`を設定する必要があります。

    ```shell
    # set the environment variable for your own space
    export DATABASE_URL='mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'

    # set the environment variable for the Netlify space
    netlify env:set DATABASE_URL 'mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    ```

    環境変数を確認してください。

    ```shell
    # check the environment variable for your own space
    env | grep DATABASE_URL

    # check the environment variable for the Netlify space
    netlify env:list
    ```

4.  アプリをローカルでビルドし、スキーマをTiDB Cloudリソースに移行します。

    > **ヒント：**
    >
    > ローカル環境へのデプロイをスキップして、アプリを直接 Netlify にデプロイしたい場合は、手順 6 に進んでください。

    ```shell
    npm install .
    npm run netlify-build
    ```

5.  アプリケーションをローカル環境で実行してください。ローカル開発サーバーを起動して、サイトをプレビューできます。

    ```shell
    netlify dev
    ```

    次に、ブラウザで`http://localhost:3000/`にアクセスして、そのUIを探索してください。

6.  アプリを Netlify にデプロイ。ローカルプレビューで問題がなければ、次のコマンドを使用してサイトを Netlify にデプロイできます。 `--trigger`ローカルファイルをアップロードせずにデプロイすることを意味します。ローカルで変更を加えた場合は、GitHub リポジトリにコミットされていることを確認してください。

    ```shell
    netlify deploy --prod --trigger
    ```

    Netlifyコンソールにアクセスして、デプロイ状況を確認してください。デプロイが完了すると、アプリのサイトにはNetlifyからパブリックIPアドレスが割り当てられ、誰でもアクセスできるようになります。

## エッジ機能を使用する {#use-the-edge-function}

上記のセクションで説明したサンプルアプリは、Netlifyのサーバーレス関数上で動作します。このセクションでは[TiDB Cloudサーバーレスドライバー](/develop/serverless-driver.md)でエッジ関数を使用する方法を示します。 レス エッジ関数はNetlifyが提供する機能で、Netlify CDNのエッジでサーバーレス関数を実行できます。

エッジ機能を使用するには、以下の手順に従ってください。

1.  プロジェクトのルートディレクトリに`netlify/edge-functions`という名前のディレクトリを作成します。

2.  ディレクトリ内に`hello.ts`という名前のファイルを作成し、以下のコードを追加してください。

    ```typescript
    import { connect } from 'https://esm.sh/@tidbcloud/serverless'

    export default async () => {
      const conn = connect({url: Netlify.env.get('DATABASE_URL')})
      const result = await conn.execute('show databases')
      return new Response(JSON.stringify(result));
    }

    export const config = { path: "/api/hello" };
    ```

3.  `DATABASE_URL`環境変数を設定してください。接続情報は[TiDB Cloudコンソール](https://tidbcloud.com/)から取得できます。 .

    ```shell
    netlify env:set DATABASE_URL 'mysql://<username>:<password>@<host>/<database>'
    ```

4.  Netlifyにエッジ機能をデプロイ。

    ```shell
    netlify deploy --prod --trigger
    ```

その後、Netlify コンソールにアクセスしてデプロイの状態を確認できます。デプロイが完了すると、 `https://<netlify-host>/api/hello` URL を介してエッジ機能にアクセスできます。
