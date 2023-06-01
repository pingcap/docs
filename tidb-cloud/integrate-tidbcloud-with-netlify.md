---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# TiDB Cloudと Netlify を統合する {#integrate-tidb-cloud-with-netlify}

[<a href="https://netlify.com/">ネットリファイ</a>](https://netlify.com/)は、最新の Web プロジェクトを自動化するためのオールインワン プラットフォームです。ホスティング インフラストラクチャ、継続的インテグレーション、デプロイ パイプラインを単一のワークフローに置き換え、プロジェクトの成長に合わせてサーバーレス関数、ユーザー認証、フォーム処理などの動的な機能を統合します。

このガイドでは、 TiDB Cloudクラスターを Netlify プロジェクトに接続する方法について説明します。

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Netlify アカウントとデプロイされたサイト {#a-netlify-account-and-a-deployed-site}

Netlify にアカウントとサイトが必要です。何も持っていない場合は、次のリンクを参照して作成してください。

-   [<a href="https://app.netlify.com/signup">新しいアカウントにサインアップする</a>](https://app.netlify.com/signup) 。
-   Netlifyでは[<a href="https://docs.netlify.com/welcome/add-new-site/">サイトを追加する</a>](https://docs.netlify.com/welcome/add-new-site/) 。導入するアプリケーションがない場合は、 [<a href="https://github.com/tidbcloud/nextjs-prisma-example">TiDB Cloudスターター テンプレート</a>](https://github.com/tidbcloud/nextjs-prisma-example)を使用して試してみてください。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。お持ちでない場合は[<a href="/tidb-cloud/create-tidb-cluster.md">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。

1 つのTiDB Cloudクラスターは複数の Netlify サイトに接続できます。

### TiDB Cloudのトラフィック フィルターに許可されるすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

Dedicated Tierクラスターの場合は、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。これは、Netlify デプロイメントが動的 IP アドレスを使用するためです。

Serverless Tierクラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

1.  [<a href="/tidb-cloud/connect-via-standard-connection.md">標準接続経由でTiDB Cloudクラスターに接続する</a>](/tidb-cloud/connect-via-standard-connection.md)の手順に従ってパスワードを設定し、TiDB クラスターの接続情報を取得します。

    > **ノート：**
    >
    > Dedicated Tierクラスターの場合は、この手順で**「どこからでもアクセスを許可」**トラフィック フィルターも設定していることを確認してください。

2.  **Netlify ダッシュボード**&gt; **Netlify プロジェクト**&gt;**サイト設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に従って[<a href="https://docs.netlify.com/environment-variables/get-started/#update-variables-with-the-netlify-ui">変数を更新する</a>](https://docs.netlify.com/environment-variables/get-started/#update-variables-with-the-netlify-ui)に移動します。

    ここでは例として Prisma アプリケーションを使用します。以下は、 TiDB CloudServerless Tierクラスターの Prisma スキーマ ファイル内のデータソース設定です。

    ```
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

    Netlify では、次のように環境変数を宣言できます。

    -   **キー**= DATABASE_URL
    -   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

    TiDB Cloudコンソールで`<User>` 、 `<Password>` 、 `<Endpoint>` 、 `<Port>` 、および`<Database>`の情報を取得できます。

![Set an environment variable in Netlify](/media/tidb-cloud/integration-netlify-environment-variables.jpg)

サイトを再デプロイした後、この新しい環境変数を使用してTiDB Cloudクラスターに接続できます。
