---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# TiDB Cloudと Netlify を統合する {#integrate-tidb-cloud-with-netlify}

[<a href="https://netlify.com/">ネットリファイ</a>](https://netlify.com/)は、最新の Web プロジェクトを自動化するためのオールインワン プラットフォームです。ホスティング インフラストラクチャ、継続的インテグレーション、デプロイ パイプラインを単一のワークフローに置き換え、プロジェクトの成長に合わせてサーバーレス関数、ユーザー認証、フォーム処理などの動的な機能を統合します。

このドキュメントでは、 TiDB Cloud をデータベース バックエンドとして使用して Netlify にフルスタック アプリをデプロイする方法について説明します。

## 前提条件 {#prerequisites}

展開する前に、次の前提条件が満たされていることを確認してください。

### Netlify アカウントと CLI {#a-netlify-account-and-cli}

Netlify アカウントと CLI が必要です。何も持っていない場合は、次のリンクを参照して作成してください。

-   [<a href="https://app.netlify.com/signup">Netlify アカウントにサインアップする</a>](https://app.netlify.com/signup) 。
-   [<a href="https://docs.netlify.com/cli/get-started/">Netlify CLIを入手する</a>](https://docs.netlify.com/cli/get-started/) 。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。お持ちでない場合は[<a href="/tidb-cloud/create-tidb-cluster.md">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。

1 つのTiDB Cloudクラスターは複数の Netlify サイトに接続できます。

### TiDB Cloudのトラフィック フィルターに許可されるすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

TiDB Dedicatedクラスターの場合、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。これは、Netlify デプロイメントでは動的 IP アドレスが使用されるためです。

TiDB Serverless クラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## ステップ 1. サンプル プロジェクトと接続文字列を取得する {#step-1-get-the-example-project-and-the-connection-string}

すぐに始められるように、 TiDB Cloud、React と Prisma Client を使用した Next.js を使用した TypeScript のフルスタック サンプル アプリを提供しています。自分でブログを投稿・削除できるシンプルなブログサイトです。すべてのコンテンツは Prisma を通じてTiDB Cloudに保存されます。

### サンプル プロジェクトをフォークし、自分のスペースにクローン作成します。 {#fork-the-example-project-and-clone-it-to-your-own-space}

1.  [<a href="https://github.com/tidbcloud/nextjs-prisma-example">Next.js と Prisma を使用したフルスタックの例</a>](https://github.com/tidbcloud/nextjs-prisma-example)リポジトリを自分の GitHub リポジトリにフォークします。

2.  フォークされたリポジトリのクローンを自分のスペースに作成します。

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### TiDB Cloud接続文字列を取得する {#get-the-tidb-cloud-connection-string}

TiDB Serverless クラスターの場合、接続文字列は[<a href="/tidb-cloud/cli-reference.md">TiDB CloudCLI</a>](/tidb-cloud/cli-reference.md)または[<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)から取得できます。

TiDB Dedicatedクラスターの場合、接続文字列はTiDB Cloudコンソールからのみ取得できます。

<SimpleTab>
<div label="TiDB Cloud CLI">

> **ヒント：**
>
> Cloud CLI をインストールしていない場合は、次の手順を実行する前に、 [<a href="/tidb-cloud/get-started-with-cli.md">TiDB CloudCLI クイック スタート</a>](/tidb-cloud/get-started-with-cli.md)のクイック インストールを参照してください。

1.  対話型モードでクラスターの接続文字列を取得します。

    ```shell
    ticloud cluster connect-info
    ```

2.  プロンプトに従って、クラスター、クライアント、およびオペレーティング システムを選択します。このドキュメントで使用されるクライアントは`Prisma`であることに注意してください。

    ```
    Choose the cluster
    > [x] Cluster0(13796194496)
    Choose the client
    > [x] Prisma
    Choose the operating system
    > [x] macOS/Alpine (Detected)
    ```

    出力は次のとおりです。値`url`に Prisma の接続文字列が含まれています。

    ```
    datasource db {
    provider = "mysql"
    url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
    }
    ```

    > **ノート：**
    >
    > 後で接続文字列を使用する場合は、次の点に注意してください。
    >
    > -   接続文字列内のパラメータを実際の値に置き換えます。
    > -   このドキュメントのサンプル アプリには新しいデータベースが必要なので、 `<Database>`一意の新しい名前に置き換える必要があります。

</div>
<div label="TiDB Cloud console">

1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)に移動し、 [<a href="/tidb-cloud/connect-via-standard-connection.md">**接続**</a>](/tidb-cloud/connect-via-standard-connection.md)ダイアログの接続文字列から次の接続パラメータを取得します。

    -   `${host}`
    -   `${port}`
    -   `${user}`
    -   `${password}`

2.  次の接続文字列に接続パラメータを入力します。

    ```
    mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
    ```

    > **ノート：**
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

2.  自動セットアップを開始します。この手順では、継続的なデプロイのためにリポジトリに接続するため、Netlify CLI は、リポジトリ上にデプロイ キーと Webhook を作成するためのアクセスを必要とします。

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

3.  環境変数を設定します。自分のスペースおよび Netlify スペースからTiDB Cloudクラスターに接続するには、 [<a href="#step-1-get-the-example-project-and-the-connection-string">ステップ1</a>](#step-1-get-the-example-project-and-the-connection-string)から取得した接続文字列として`DATABASE_URL`を設定する必要があります。

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
