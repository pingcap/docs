---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# TiDB Cloudと Netlify を統合する {#integrate-tidb-cloud-with-netlify}

[ネットリファイ](https://netlify.com/)は、最新の Web プロジェクトを自動化するためのオールインワン プラットフォームです。ホスティング インフラストラクチャ、継続的インテグレーション、デプロイ パイプラインを単一のワークフローに置き換え、プロジェクトの成長に合わせてサーバーレス関数、ユーザー認証、フォーム処理などの動的な機能を統合します。

このドキュメントでは、 TiDB Cloud をデータベース バックエンドとして使用して Netlify にフルスタック アプリをデプロイする方法について説明します。 TiDB Cloudサーバーレス ドライバーで Netlify エッジ機能を使用する方法も学習できます。

## 前提条件 {#prerequisites}

展開する前に、次の前提条件が満たされていることを確認してください。

### Netlify アカウントと CLI {#a-netlify-account-and-cli}

Netlify アカウントと CLI が必要です。何も持っていない場合は、次のリンクを参照して作成してください。

-   [Netlify アカウントにサインアップする](https://app.netlify.com/signup) 。
-   [Netlify CLIを入手する](https://docs.netlify.com/cli/get-started/) 。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。何も持っていない場合は、以下を参照して作成してください。

-   [TiDB サーバーレスクラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)
-   [TiDB 専用クラスターの作成](/tidb-cloud/create-tidb-cluster.md)

1 つのTiDB Cloudクラスターは複数の Netlify サイトに接続できます。

### TiDB Cloudのトラフィック フィルターに許可されるすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

TiDB 専用クラスターの場合、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。これは、Netlify デプロイメントでは動的 IP アドレスが使用されるためです。

TiDB サーバーレス クラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## ステップ 1. サンプル プロジェクトと接続文字列を取得する {#step-1-get-the-example-project-and-the-connection-string}

すぐに始められるように、 TiDB Cloud、React と Prisma Client を使用した Next.js を使用した TypeScript のフルスタック サンプル アプリを提供しています。自分でブログを投稿・削除できるシンプルなブログサイトです。すべてのコンテンツは Prisma を通じてTiDB Cloudに保存されます。

### サンプル プロジェクトをフォークし、自分のスペースにクローン作成します。 {#fork-the-example-project-and-clone-it-to-your-own-space}

1.  [Next.js と Prisma を使用したフルスタックの例](https://github.com/tidbcloud/nextjs-prisma-example)リポジトリを自分の GitHub リポジトリにフォークします。

2.  フォークされたリポジトリのクローンを自分のスペースに作成します。

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### TiDB Cloud接続文字列を取得する {#get-the-tidb-cloud-connection-string}

TiDB サーバーレス クラスターの場合、接続文字列は[TiDB CloudCLI](/tidb-cloud/cli-reference.md)または[TiDB Cloudコンソール](https://tidbcloud.com/)から取得できます。

TiDB 専用クラスターの場合、接続文字列はTiDB Cloudコンソールからのみ取得できます。

<SimpleTab>
<div label="TiDB Cloud CLI">

> **ヒント：**
>
> Cloud CLI をインストールしていない場合は、次の手順を実行する前に、 [TiDB CloudCLI クイック スタート](/tidb-cloud/get-started-with-cli.md)のクイック インストールを参照してください。

1.  対話型モードでクラスターの接続文字列を取得します。

    ```shell
    ticloud cluster connect-info
    ```

2.  プロンプトに従って、クラスター、クライアント、およびオペレーティング システムを選択します。このドキュメントで使用されるクライアントは`Prisma`であることに注意してください。

        Choose the cluster
        > [x] Cluster0(13796194496)
        Choose the client
        > [x] Prisma
        Choose the operating system
        > [x] macOS/Alpine (Detected)

    出力は次のとおりです。値`url`に Prisma の接続文字列が含まれています。

    ```shell
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **注記：**
    >
    > 後で接続文字列を使用する場合は、次の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えます。
    > -   このドキュメントのサンプル アプリには新しいデータベースが必要なので、 `<Database>`一意の新しい名前に置き換える必要があります。

</div>
<div label="TiDB Cloud console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)では、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。表示されたダイアログで、接続文字列から次の接続パラメータを取得できます。

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
    > 後で接続文字列を使用する場合は、次の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えます。
    > -   このドキュメントのサンプル アプリには新しいデータベースが必要なので、 `<Database>`一意の新しい名前に置き換える必要があります。

</div>
</SimpleTab>

## ステップ 2. サンプルアプリを Netlify にデプロイ {#step-2-deploy-the-example-app-to-netlify}

1.  Netlify CLI で、Netlify アカウントを認証し、アクセス トークンを取得します。

    ```shell
    netlify login
    ```

2.  自動セットアップを開始します。この手順では、継続的なデプロイのためにリポジトリに接続するため、Netlify CLI は、リポジトリ上にデプロイ キーと Webhook を作成するためのアクセス権を必要とします。

    ```shell
    netlify init
    ```

    プロンプトが表示されたら、 **[新しいサイトの作成と構成]**を選択し、GitHub アクセスを許可します。他のすべてのオプションにはデフォルト値を使用します。

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

3.  環境変数を設定します。自分のスペースおよび Netlify スペースからTiDB Cloudクラスターに接続するには、 [ステップ1](#step-1-get-the-example-project-and-the-connection-string)から取得した接続文字列として`DATABASE_URL`を設定する必要があります。

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

4.  アプリをローカルで構築し、スキーマをTiDB Cloudクラスターに移行します。

    > **チップ：**
    >
    > ローカル デプロイをスキップしてアプリを Netlify に直接デプロイする場合は、ステップ 6 に進みます。

    ```shell
    npm install .
    npm run netlify-build
    ```

5.  アプリケーションをローカルで実行します。ローカル開発サーバーを起動してサイトをプレビューできます。

    ```shell
    netlify dev
    ```

    次に、ブラウザーで`http://localhost:3000/`に移動して、その UI を調べます。

6.  アプリを Netlify にデプロイ。ローカル プレビューに満足したら、次のコマンドを使用してサイトを Netlify にデプロイできます。 `--trigger`ローカル ファイルをアップロードせずに展開することを意味します。ローカルで変更を加えた場合は、それを GitHub リポジトリにコミットしていることを確認してください。

    ```shell
    netlify deploy --prod --trigger
    ```

    Netlify コンソールに移動して、デプロイメントの状態を確認します。デプロイメントが完了すると、アプリのサイトには Netlify によって提供されるパブリック IP アドレスが設定され、誰もがアクセスできるようになります。

## エッジ機能を使う {#use-the-edge-function}

上のセクションで説明したサンプル アプリは、Netlify サーバーレス機能で実行されます。このセクションでは、 [TiDB Cloudサーバーレス ドライバー](/tidb-cloud/serverless-driver.md)でエッジ関数を使用する方法を示します。エッジ機能は Netlify が提供する機能で、Netlify CDN のエッジでサーバーレス関数を実行できるようになります。

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

3.  `DATABASE_URL`環境変数を設定します。接続情報は[TiDB Cloudコンソール](https://tidbcloud.com/)から取得できます。

    ```shell
    netlify env:set DATABASE_URL 'mysql://<username>:<password>@<host>/<database>'
    ```

4.  Netlifyにエッジ機能をデプロイ。

    ```shell
    netlify deploy --prod --trigger
    ```

次に、Netlify コンソールに移動して、デプロイメントの状態を確認できます。デプロイが完了すると、 `https://<netlify-host>/api/hello` URL を介してエッジ機能にアクセスできるようになります。
