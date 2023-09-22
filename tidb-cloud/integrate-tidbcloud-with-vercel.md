---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloudと Vercel を統合する {#integrate-tidb-cloud-with-vercel}

[ヴェルセル](https://vercel.com/)はフロントエンド開発者向けのプラットフォームで、イノベーターがインスピレーションの瞬間に作成するために必要なスピードと信頼性を提供します。

Vercel でTiDB Cloudを使用すると、MySQL 互換のリレーショナル モデルで新しいフロントエンド アプリケーションをより迅速に構築でき、復元力、拡張性、最高レベルのデータ プライバシーとセキュリティを目指して構築されたプラットフォームで自信を持ってアプリを成長させることができます。

このガイドでは、次のいずれかの方法を使用してTiDB Cloudクラスターを Vercel プロジェクトに接続する方法について説明します。

-   [TiDB Cloud Vercel 統合経由で接続する](#connect-via-the-tidb-cloud-vercel-integration)
-   [環境変数を手動で構成して接続する](#connect-via-manually-setting-environment-variables)

上記の両方の方法について、 TiDB Cloud はプログラムでデータベースに接続するための次のオプションを提供します。

-   直接接続: MySQL の標準接続システムを使用して、 TiDB Cloudクラスターを Vercel プロジェクトに直接接続します。
-   [データアプリ](/tidb-cloud/data-service-manage-data-app.md) : HTTP エンドポイントのコレクションを通じてTiDB Cloudクラスターのデータにアクセスします。

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Vercel アカウントと Vercel プロジェクト {#a-vercel-account-and-a-vercel-project}

Vercel にアカウントとプロジェクトが必要です。何も持っていない場合は、次の Vercel ドキュメントを参照して作成してください。

-   [新しい個人アカウントの作成](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)または[新しいチームを作成する](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team) 。
-   Vercel では[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)使用するか、デプロイするアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試すことができます。

1 つの Vercel プロジェクトは 1 つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断してから、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。何も持っていない場合は、以下を参照して作成してください。

-   [TiDB サーバーレスクラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注記：**
    >
    > TiDB Cloud Vercel 統合は、TiDB サーバーレス クラスターの作成をサポートします。後で統合プロセス中に作成することもできます。

-   [TiDB 専用クラスターの作成](/tidb-cloud/create-tidb-cluster.md)

    > **注記：**
    >
    > TiDB 専用クラスターの場合、Vercel デプロイメントでは[動的IPアドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用されるため、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。 TiDB Cloud Vercel 統合を使用する場合、 TiDB Cloud は統合ワークフローのクラスターにトラフィック フィルター`0.0.0.0/0`自動的に追加します (存在しない場合)。

[TiDB Cloud Vercel Integration を介して Vercel と統合する](#connect-via-the-tidb-cloud-vercel-integration)では、組織の`Organization Owner`役割、またはTiDB Cloudのターゲット プロジェクトの`Project Owner`の役割を担うことが期待されます。詳細については、 [ユーザーの役割](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

1 つのTiDB Cloudクラスターは複数の Vercel プロジェクトに接続できます。

### データアプリとエンドポイント {#a-data-app-and-endpoints}

[データアプリ](/tidb-cloud/data-service-manage-data-app.md)経由でTiDB Cloudクラスターに接続する場合は、事前にTiDB Cloudにターゲット データ アプリとエンドポイントを用意しておく必要があります。何も持っていない場合は、以下を参照して作成してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  プロジェクトの場合は[データアプリを作成する](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) 。
3.  [データアプリをリンクする](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)をターゲットTiDB Cloudクラスターに割り当てます。
4.  [エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)を使用すると、SQL ステートメントを実行するようにカスタマイズできます。

1 つの Vercel プロジェクトは 1 つのTiDB Cloudデータ アプリにのみ接続できます。 Vercel プロジェクトのデータ アプリを変更するには、まず現在のアプリを切断してから、新しいアプリに接続する必要があります。

## TiDB Cloud Vercel 統合経由で接続する {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel 統合経由で接続するには、 [Vercel の統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページに移動します。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloud はVercel プロジェクトに必要なすべての環境変数を自動的に生成します。

詳細な手順は次のとおりです。

<SimpleTab>
<div label="Direct connection">

1.  [TiDB Cloud Vercel の統合](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**「統合の追加」**をクリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **[続行]**をクリックします。
4.  統合に必要な権限を確認し、 **[統合の追加]**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで次の操作を行います。

    1.  ターゲットの Vercel プロジェクトを選択し、 **[次へ]**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**クラスタを**選択します。
    4.  ターゲットのTiDB Cloudクラスターを選択します。 **[クラスタ]**ドロップダウン リストが空である場合、または新しい TiDB サーバーレス クラスターを選択する場合は、リスト内の**[+クラスタ**を作成します。
    5.  Vercel プロジェクトが使用しているフレームワークを選択します。ターゲット フレームワークがリストにない場合は、 **[一般]**を選択します。フレームワークが異なれば、決定される環境変数も異なります。
    6.  **[統合を追加して Vercel に戻る]**をクリックします。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、 **[設定]** &gt; **[環境変数]**をクリックして、ターゲット TiDB クラスターの環境変数が自動的に追加されているかどうかを確認します。

    以下の変数が追加されていれば統合は完了です。

    **一般的な**

    ```shell
    TIDB_HOST
    TIDB_PORT
    TIDB_USER
    TIDB_PASSWORD
    ```

    TiDB 専用クラスターの場合、ルート CA は次の変数に設定されます。

        TIDB_SSL_CA

    **プリズマ**

        DATABASE_URL

</div>

<div label="Data App">

1.  [TiDB Cloud Vercel の統合](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**「統合の追加」**をクリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **[続行]**をクリックします。
4.  統合に必要な権限を確認し、 **[統合の追加]**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで次の操作を行います。

    1.  ターゲットの Vercel プロジェクトを選択し、 **[次へ]**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**データ アプリ**を選択します。
    4.  ターゲットの TiDB データ アプリを選択します。
    5.  **[統合を追加して Vercel に戻る]**をクリックします。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、 **[設定]** &gt; **[環境変数]**をクリックして、ターゲット データ アプリの環境変数が自動的に追加されているかどうかを確認します。

    以下の変数が追加されていれば統合は完了です。

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

<SimpleTab>
<div label="Direct connection">

1.  TiDB クラスターの接続情報を取得します。

    クラスターの接続ダイアログから接続情報を取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。

    > **注記：**
    >
    > TiDB 専用クラスターの場合は、このステップで**「どこからでもアクセスを許可」**トラフィック フィルターを設定していることを確認してください。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)に移動します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

ここでは例として Prisma アプリケーションを使用します。以下は、TiDB サーバーレス クラスターの Prisma スキーマ ファイル内のデータソース設定です。

    datasource db {
        provider = "mysql"
        url      = env("DATABASE_URL")
    }

Vercel では、次のように環境変数を宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

TiDB Cloudコンソールで`<User>` 、 `<Password>` 、 `<Endpoint>` 、 `<Port>` 、および`<Database>`の情報を取得できます。

</div>
<div label="Data App">

1.  データ アプリとそのエンドポイントを作成していない場合は、 [データAPPを管理する](/tidb-cloud/data-service-manage-data-app.md)と[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)の手順に従ってください。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、データ アプリの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)に移動します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    Vercel では、次のように環境変数を宣言できます。

    -   **キー**= `DATA_APP_BASE_URL`
    -   **値**= `<DATA_APP_BASE_URL>`
    -   **キー**= `DATA_APP_PUBLIC_KEY`
    -   **値**= `<DATA_APP_PUBLIC_KEY>`
    -   **キー**= `DATA_APP_PRIVATE_KEY`
    -   **値**= `<DATA_APP_PRIVATE_KEY>`

    TiDB Cloudコンソールの[データサービス](https://tidbcloud.com/console/data-service)ページから`<DATA_APP_BASE_URL>` 、 `<DATA_APP_PUBLIC_KEY>` 、 `<DATA_APP_PRIVATE_KEY>`の情報を取得できます。

</div>
</SimpleTab>

## 接続を構成する {#configure-connections}

[TiDB Cloud Vercel の統合](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内の接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **[統合]**をクリックします。
2.  [TiDB Cloud]エントリで**[管理]**をクリックします。
3.  **「構成」**をクリックします。
4.  **[リンクの追加]**または**[削除]**をクリックして接続を追加または削除します。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。トラフィック フィルターとTiDB Cloudクラスターのデータは影響を受けません。
