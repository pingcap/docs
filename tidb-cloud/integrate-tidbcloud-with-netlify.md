---
title: Integrate TiDB Cloud with Netlify
summary: TiDB Cloudクラスターを Netlify プロジェクトに接続する方法を学習します。
---

# TiDB Cloudを Netlify と統合する {#integrate-tidb-cloud-with-netlify}

[ネットリファイ](https://netlify.com/) 、最新の Web プロジェクトを自動化するためのオールインワン プラットフォームです。ホスティング インフラストラクチャ、継続的インテグレーション、デプロイメント パイプラインを単一のワークフローに置き換え、プロジェクトの拡大に​​合わせてサーバーレス関数、ユーザー認証、フォーム処理などの動的な機能を統合します。

このドキュメントでは、TiDB Cloud をデータベース バックエンドとして使用して、Netlify にフルスタック アプリをデプロイする方法について説明します。また、 TiDB Cloudサーバーレス ドライバーを使用して Netlify エッジ機能を使用する方法も学習できます。

## 前提条件 {#prerequisites}

展開する前に、次の前提条件が満たされていることを確認してください。

### Netlify アカウントと CLI {#a-netlify-account-and-cli}

Netlify アカウントと CLI が必要です。お持ちでない場合は、次のリンクを参照して作成してください。

-   [Netlifyアカウントにサインアップする](https://app.netlify.com/signup) 。
-   [Netlify CLI を入手する](https://docs.netlify.com/cli/get-started/) 。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターがあることが前提となります。アカウントとクラスターがない場合は、以下を参照して作成してください。

-   [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)
-   [TiDB Cloud専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

1 つのTiDB Cloudクラスターは複数の Netlify サイトに接続できます。

### TiDB Cloudのトラフィック フィルターで許可されるすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

TiDB Cloud Dedicated クラスターの場合、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) が接続に許可されていることを確認します。これは、Netlify デプロイメントで動的 IP アドレスが使用されるためです。

TiDB Cloud Serverless クラスターは、デフォルトですべての IP アドレスの接続を許可するため、トラフィック フィルターを構成する必要はありません。

## ステップ1. サンプルプロジェクトと接続文字列を取得する {#step-1-get-the-example-project-and-the-connection-string}

すぐに使い始められるように、 TiDB Cloud、 React と Prisma Client を使用して、Next.js による TypeScript のフルスタック サンプル アプリを提供しています。これは、自分のブログを投稿したり削除したりできるシンプルなブログ サイトです。すべてのコンテンツは、Prisma を通じてTiDB Cloudに保存されます。

### サンプルプロジェクトをフォークして自分のスペースにクローンする {#fork-the-example-project-and-clone-it-to-your-own-space}

1.  [Next.js と Prisma を使用したフルスタックの例](https://github.com/tidbcloud/nextjs-prisma-example)リポジトリを自分の GitHub リポジトリにフォークします。

2.  フォークしたリポジトリを自分のスペースにクローンします。

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### TiDB Cloud接続文字列を取得する {#get-the-tidb-cloud-connection-string}

TiDB Cloud Serverless クラスターの場合、接続文字列は[TiDB CloudCLI](/tidb-cloud/cli-reference.md)または[TiDB Cloudコンソール](https://tidbcloud.com/)から取得できます。

TiDB Cloud Dedicated クラスターの場合、接続文字列はTiDB Cloudコンソールからのみ取得できます。

<SimpleTab>
<div label="TiDB Cloud CLI">

> **ヒント：**
>
> Cloud CLI をインストールしていない場合は、次の手順を実行する前に、クイック インストールの[TiDB CloudCLI クイック スタート](/tidb-cloud/get-started-with-cli.md)を参照してください。

1.  対話モードでクラスターの接続文字列を取得します。

    ```shell
    ticloud cluster connect-info
    ```

2.  プロンプトに従って、クラスター、クライアント、およびオペレーティング システムを選択します。このドキュメントで使用されているクライアントは`Prisma`であることに注意してください。

        Choose the cluster
        > [x] Cluster0(13796194496)
        Choose the client
        > [x] Prisma
        Choose the operating system
        > [x] macOS/Alpine (Detected)

    出力は次のようになります。1 `url`値に Prisma の接続文字列が含まれています。

    ```shell
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **注記：**
    >
    > 後に接続文字列を使用する場合は、次の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えます。
    > -   このドキュメントのサンプル アプリには新しいデータベースが必要なので、 `<Database>`一意の新しい名前に置き換える必要があります。

</div>
<div label="TiDB Cloud console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。表示されるダイアログで、接続文字列から次の接続パラメータを取得できます。

    -   `${host}`
    -   `${port}`
    -   `${user}`
    -   `${password}`

2.  次の接続文字列に接続パラメータを入力します。

    ```shell
    mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
    ```

    > **注記：**
    >
    > 後に接続文字列を使用する場合は、次の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えます。
    > -   このドキュメントのサンプル アプリには新しいデータベースが必要なので、 `<Database>`一意の新しい名前に置き換える必要があります。

</div>
</SimpleTab>

## ステップ2. サンプルアプリをNetlifyにデプロイ {#step-2-deploy-the-example-app-to-netlify}

1.  Netlify CLI で、Netlify アカウントを認証し、アクセス トークンを取得します。

    ```shell
    netlify login
    ```

2.  自動セットアップを開始します。この手順では、継続的なデプロイのためにリポジトリを接続するため、Netlify CLI にはリポジトリにデプロイ キーと Webhook を作成するためのアクセス権が必要です。

    ```shell
    netlify init
    ```

    プロンプトが表示されたら、 **「新しいサイトの作成と構成」**を選択し、GitHub へのアクセスを許可します。その他のオプションはすべてデフォルト値を使用します。

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

3.  環境変数を設定します。自分のスペースと Netlify スペースからTiDB Cloudクラスターに接続するには、 [ステップ1](#step-1-get-the-example-project-and-the-connection-string)から取得した接続文字列として`DATABASE_URL`を設定する必要があります。

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

4.  アプリをローカルでビルドし、スキーマをTiDB Cloudクラスターに移行します。

    > **ヒント:**
    >
    > ローカルデプロイをスキップしてアプリを Netlify に直接デプロイする場合は、手順 6 に進んでください。

    ```shell
    npm install .
    npm run netlify-build
    ```

5.  アプリケーションをローカルで実行します。ローカル開発サーバーを起動してサイトをプレビューできます。

    ```shell
    netlify dev
    ```

    次に、ブラウザで`http://localhost:3000/`に移動して、その UI を調べます。

6.  アプリを Netlify にデプロイ。ローカル プレビューに満足したら、次のコマンドを使用してサイトを Netlify にデプロイできます。1 `--trigger` 、ローカル ファイルをアップロードせずにデプロイすることを意味します。ローカルで変更を加えた場合は、必ず GitHub リポジトリにコミットしてください。

    ```shell
    netlify deploy --prod --trigger
    ```

    Netlify コンソールに移動して、デプロイメントの状態を確認します。デプロイメントが完了すると、アプリのサイトには Netlify によって提供されるパブリック IP アドレスが割り当てられ、誰でもアクセスできるようになります。

## エッジ機能を使用する {#use-the-edge-function}

上のセクションで説明したサンプル アプリは、Netlify サーバーレス関数で実行されます。このセクションでは、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)でエッジ関数を使用する方法を説明します。エッジ関数は Netlify が提供する機能で、Netlify CDN のエッジでサーバーレス関数を実行できます。

エッジ機能を使用するには、次の手順を実行します。

1.  プロジェクトのルート ディレクトリに`netlify/edge-functions`という名前のディレクトリを作成します。

2.  ディレクトリに`hello.ts`という名前のファイルを作成し、次のコードを追加します。

    ```typescript
    import { connect } from 'https://esm.sh/@tidbcloud/serverless'

    export default async () => {
      const conn = connect({url: Netlify.env.get('DATABASE_URL')})
      const result = await conn.execute('show databases')
      return new Response(JSON.stringify(result));
    }

    export const config = { path: "/api/hello" };
    ```

3.  `DATABASE_URL`環境変数を設定します。3 から接続情報を取得できます[TiDB Cloudコンソール](https://tidbcloud.com/)

    ```shell
    netlify env:set DATABASE_URL 'mysql://<username>:<password>@<host>/<database>'
    ```

4.  エッジ機能を Netlify にデプロイ。

    ```shell
    netlify deploy --prod --trigger
    ```

次に、Netlify コンソールに移動して、デプロイメントの状態を確認します。デプロイメントが完了すると、 `https://<netlify-host>/api/hello` URL からエッジ機能にアクセスできます。
