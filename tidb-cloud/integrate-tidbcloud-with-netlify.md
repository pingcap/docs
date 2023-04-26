---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# TiDB Cloudを Netlify と統合する {#integrate-tidb-cloud-with-netlify}

[ネットリファイ](https://netlify.com/)は、最新の Web プロジェクトを自動化するためのオールインワン プラットフォームです。ホスティング インフラストラクチャ、継続的インテグレーション、デプロイ パイプラインを単一のワークフローに置き換え、プロジェクトの成長に合わせて、サーバーレス関数、ユーザー認証、フォーム処理などの動的機能を統合します。

このガイドでは、 TiDB Cloudクラスターを Netlify プロジェクトに接続する方法について説明します。

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Netlify アカウントとデプロイされたサイト {#a-netlify-account-and-a-deployed-site}

Netlify にアカウントとサイトが必要です。お持ちでない場合は、次のリンクを参照して作成してください。

-   [新しいアカウントにサインアップ](https://app.netlify.com/signup) .
-   ネットリファイで[サイトを追加](https://docs.netlify.com/welcome/add-new-site/) 。展開するアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://github.com/tidbcloud/nextjs-prisma-example)を使用して試すことができます。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。持っていない場合は、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

1 つのTiDB Cloudクラスターで複数の Netlify サイトに接続できます。

### TiDB Cloudでトラフィック フィルターに許可されているすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

Dedicated Tierクラスターの場合、クラスターのトラフィック フィルターがすべての IP アドレス ( `0.0.0.0/0`に設定) の接続を許可していることを確認してください。これは、Netlify デプロイが動的 IP アドレスを使用するためです。

Serverless Tierクラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

1.  [標準接続を介してTiDB Cloudクラスターに接続する](/tidb-cloud/connect-via-standard-connection.md)の手順に従ってパスワードを設定し、TiDB クラスターの接続情報を取得します。

    > **ノート：**
    >
    > Dedicated Tierクラスターの場合は、このステップで**[どこからでもアクセスを許可する]**トラフィック フィルターも設定していることを確認してください。

2.  **Netlify ダッシュボード**&gt; <strong>Netlify プロジェクト</strong>&gt;<strong>サイト設定</strong>&gt;<strong>環境変数</strong>に移動し、TiDB クラスターの接続情報に従って[変数を更新する](https://docs.netlify.com/environment-variables/get-started/#update-variables-with-the-netlify-ui)に進みます。

    ここでは例として Prisma アプリケーションを使用します。以下は、 TiDB Cloud Serverless Tierクラスターの Prisma スキーマ ファイルのデータソース設定です。

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
