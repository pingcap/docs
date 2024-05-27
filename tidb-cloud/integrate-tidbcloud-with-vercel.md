---
title: Integrate TiDB Cloud with Vercel
summary: TiDB Cloudクラスターを Vercel プロジェクトに接続する方法を学習します。
---

<!-- markdownlint-disable MD029 -->

# TiDB CloudとVercelを統合する {#integrate-tidb-cloud-with-vercel}

[ヴェルセル](https://vercel.com/)はフロントエンド開発者向けのプラットフォームであり、イノベーターがインスピレーションの瞬間に創造するために必要なスピードと信頼性を提供します。

TiDB Cloudを Vercel と併用すると、MySQL 互換のリレーショナル モデルを使用して新しいフロントエンド アプリケーションをより迅速に構築し、回復力、拡張性、最高レベルのデータ プライバシーとセキュリティを実現するプラットフォームを使用して自信を持ってアプリを拡張できます。

このガイドでは、次のいずれかの方法を使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続する方法について説明します。

-   [TiDB Cloud Vercel統合を介して接続](#connect-via-the-tidb-cloud-vercel-integration)
-   [環境変数を手動で設定して接続する](#connect-via-manually-setting-environment-variables)

上記の両方の方法では、 TiDB Cloud はプログラムによってデータベースに接続するための次のオプションを提供します。

-   クラスタ: 直接接続または[サーバーレスドライバー](/tidb-cloud/serverless-driver.md)使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続します。
-   [データアプリ](/tidb-cloud/data-service-manage-data-app.md) : HTTP エンドポイントのコレクションを通じてTiDB Cloudクラスターのデータにアクセスします。

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Vercel アカウントと Vercel プロジェクト {#a-vercel-account-and-a-vercel-project}

Vercel にアカウントとプロジェクトがあることが前提となります。アカウントとプロジェクトがない場合は、次の Vercel ドキュメントを参照して作成してください。

-   [新しい個人アカウントを作成する](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)または[新しいチームの作成](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team) 。
-   Vercel の[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)使用している場合、またはデプロイするアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試してみることができます。

1 つの Vercel プロジェクトは 1 つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断してから、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターがあることが前提となります。アカウントとクラスターがない場合は、以下を参照して作成してください。

-   [TiDB サーバーレス クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注記：**
    >
    > TiDB Cloud Vercel 統合は、TiDB Serverless クラスターの作成をサポートしています。統合プロセス中に後で作成することもできます。

-   [TiDB専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

    > **注記：**
    >
    > TiDB 専用クラスターの場合、Vercel デプロイメントでは[動的IPアドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用されるため、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) が接続に許可されていることを確認してください。

[TiDB Cloud Vercel Integrationを介してVercelと統合する](#connect-via-the-tidb-cloud-vercel-integration)については、組織の`Organization Owner`ロールまたはTiDB Cloudの対象プロジェクトの`Project Owner`ロールを担っていることが求められます。詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

1 つのTiDB Cloudクラスターは複数の Vercel プロジェクトに接続できます。

### データアプリとエンドポイント {#a-data-app-and-endpoints}

[データアプリ](/tidb-cloud/data-service-manage-data-app.md)経由でTiDB Cloudクラスターに接続する場合は、事前にTiDB Cloudにターゲット データ アプリとエンドポイントを用意しておく必要があります。用意していない場合は、以下を参照して作成してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/console/data-service)ページに移動します。
2.  プロジェクトの[データアプリを作成する](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) 。
3.  [データアプリをリンクする](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)ターゲットのTiDB Cloudクラスターに追加します。
4.  [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)なので、SQL ステートメントを実行するようにカスタマイズできます。

1 つの Vercel プロジェクトは、1 つのTiDB Cloud Data App にのみ接続できます。Vercel プロジェクトのデータ App を変更するには、まず現在の App を切断してから、新しい App に接続する必要があります。

## TiDB Cloud Vercel統合を介して接続 {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel 統合を介して接続するには、 [Vercel の統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページに移動します。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloud はVercel プロジェクトに必要なすべての環境変数を自動的に生成します。

> **注記：**
>
> この方法は、TiDB Serverless クラスターでのみ使用できます。TiDB Dedicated クラスターに接続する場合は、 [手動方式](#connect-via-manually-setting-environment-variables)使用します。

### 統合ワークフロー {#integration-workflow}

詳細な手順は次のとおりです。

<SimpleTab>
<div label="Cluster">

1.  [TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある**「統合の追加」**をクリックします。 **「TiDB Cloudの追加」**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合の追加」**をクリックします。その後、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、次の操作を行います。

    1.  対象の Vercel プロジェクトを選択し、 **「次へ」**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**クラスタ**を選択します。
    4.  ターゲットのTiDB Cloudクラスターを選択します。**クラスタの**ドロップダウン リストが空の場合、または新しい TiDB Serverless クラスターを選択する場合は、リスト内の**+クラスタの作成を**クリックしてクラスターを作成します。
    5.  接続するデータベースを選択します。**データベースの**ドロップダウン リストが空の場合、または新しいデータベースを選択する場合は、リスト内の**[+ データベースの作成] をクリックしてデータベース**を作成します。
    6.  Vercel プロジェクトが使用しているフレームワークを選択します。ターゲット フレームワークがリストされていない場合は、 **[全般]**を選択します。フレームワークによって環境変数が異なります。
    7.  プレビュー環境用の新しいブランチを作成するために**ブランチを**有効にするかどうかを選択します。
    8.  **「統合を追加」をクリックし、Vercel に戻ります**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動して、 **「設定」** &gt; **「環境変数」**をクリックし、ターゲット TiDB クラスターの環境変数が自動的に追加されているかどうかを確認します。

    以下の変数が追加されていれば統合は完了です。

    **一般的な**

    ```shell
    TIDB_HOST
    TIDB_PORT
    TIDB_USER
    TIDB_PASSWORD
    TIDB_DATABASE
    ```

    **プリズマ**

        DATABASE_URL

    **TiDB CloudサーバーレスDriver**

        DATABASE_URL

</div>

<div label="Data App">

1.  [TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある**「統合の追加」**をクリックします。 **「TiDB Cloudの追加」**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合の追加」**をクリックします。その後、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、次の操作を行います。

    1.  対象の Vercel プロジェクトを選択し、 **「次へ」**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**データ アプリ**を選択します。
    4.  ターゲットの TiDB データ アプリを選択します。
    5.  **「統合を追加」をクリックし、Vercel に戻ります**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動して、 **「設定」** &gt; **「環境変数」**をクリックし、対象のデータ アプリの環境変数が自動的に追加されているかどうかを確認します。

    以下の変数が追加されていれば統合は完了です。

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

### 接続を構成する {#configure-connections}

[TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)インストールしている場合は、統合内で接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **「統合」**をクリックします。
2.  TiDB Cloudエントリで**[管理] を**クリックします。
3.  **[構成]を**クリックします。
4.  接続を追加または削除するには、 **「リンクの追加」**または「**削除」を**クリックします。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。ただし、このアクションは TiDB Serverless クラスターのデータには影響しません。

### TiDBサーバーレスブランチとの接続 {#connect-with-tidb-serverless-branching}

Vercel の[プレビュー展開](https://vercel.com/docs/deployments/preview-deployments)機能を使用すると、Git プロジェクトの本番ブランチに変更をマージすることなく、ライブ デプロイメントでアプリの変更をプレビューできます。 [TiDB サーバーレスブランチ](/tidb-cloud/branch-overview.md)を使用すると、Vercel プロジェクトのブランチごとに新しいインスタンスを作成できます。これにより、本番データに影響を与えることなく、ライブ デプロイメントでアプリの変更をプレビューできます。

> **注記：**
>
> 現在、TiDB Serverless ブランチは[GitHub リポジトリに関連付けられた Vercel プロジェクト](https://vercel.com/docs/deployments/git/vercel-for-github)のみをサポートしています。

TiDB サーバーレス ブランチを有効にするには、 [TiDB Cloud Vercel 統合ワークフロー](#integration-workflow)で次の点を確認する必要があります。

1.  接続タイプとして**クラスタ**を選択します。
2.  **ブランチを**有効にして、プレビュー環境用の新しいブランチを作成します。

変更を Git リポジトリにプッシュすると、Vercel はプレビュー デプロイメントをトリガーします。TiDB TiDB Cloud統合により、Git ブランチ用の TiDB Serverless ブランチが自動的に作成され、環境変数が設定されます。詳細な手順は次のとおりです。

1.  Git リポジトリに新しいブランチを作成します。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2.  いくつかの変更を追加し、その変更をリモート リポジトリにプッシュします。

3.  Vercel は新しいブランチのプレビュー展開をトリガーします。

    ![Vercel Preview\_Deployment](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1.  デプロイメント中に、 TiDB Cloud統合により、Git ブランチと同じ名前の TiDB Serverless ブランチが自動的に作成されます。TiDB Serverless ブランチがすでに存在する場合、 TiDB Cloud統合はこの手順をスキップします。

        ![TiDB\_Cloud\_Branch\_Check](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2.  TiDB Serverless ブランチの準備が整うと、 TiDB Cloud統合により、Vercel プロジェクトのプレビュー デプロイメントで環境変数が設定されます。

        ![Preview\_Envs](/media/tidb-cloud/vercel/preview-envs.png)

    3.  TiDB Cloud統合では、TiDB Serverless ブランチの準備ができるまで待機するためのブロッキング チェックも登録されます。チェックは手動で再実行できます。

4.  チェックに合格したら、プレビュー デプロイメントにアクセスして変更を確認できます。

> **注記：**
>
> Vercel デプロイメント ワークフローの制限により、デプロイメントで環境変数が確実に設定されるわけではありません。この場合、デプロイメントを再デプロイする必要があります。

> **注記：**
>
> TiDB Cloudの各組織では、デフォルトで最大 5 つの TiDB Serverless ブランチを作成できます。制限を超えないようにするには、不要になった TiDB Serverless ブランチを削除します。詳細については、 [TiDB サーバーレスブランチを管理する](/tidb-cloud/branch-manage.md)参照してください。

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

<SimpleTab>
<div label="Cluster">

1.  TiDB クラスターの接続情報を取得します。

    接続情報は、クラスターの接続ダイアログから取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)実行します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

ここでは、例として Prisma アプリケーションを使用します。以下は、TiDB Serverless クラスターの Prisma スキーマ ファイルのデータ ソース設定です。

    datasource db {
        provider = "mysql"
        url      = env("DATABASE_URL")
    }

Vercel では、次のように環境変数を宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

`<User>` `<Database>`情報`<Port>` `<Password>` `<Endpoint>` TiDB Cloudコンソールで取得できます。

</div>
<div label="Data App">

1.  データ アプリとそのエンドポイントをまだ作成していない場合は、手順[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)と[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)に従って作成します。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、データ アプリの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)実行します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    Vercel では、次のように環境変数を宣言できます。

    -   **キー**= `DATA_APP_BASE_URL`
    -   **値**= `<DATA_APP_BASE_URL>`
    -   **キー**= `DATA_APP_PUBLIC_KEY`
    -   **値**= `<DATA_APP_PUBLIC_KEY>`
    -   **キー**= `DATA_APP_PRIVATE_KEY`
    -   **値**= `<DATA_APP_PRIVATE_KEY>`

    `<DATA_APP_BASE_URL>`の情報`<DATA_APP_PRIVATE_KEY>` `<DATA_APP_PUBLIC_KEY>` TiDB Cloudコンソールの[データサービス](https://tidbcloud.com/console/data-service)ページから取得できます。

</div>
</SimpleTab>
