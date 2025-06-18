---
title: Integrate TiDB Cloud with Vercel
summary: TiDB Cloudクラスターを Vercel プロジェクトに接続する方法を学習します。
---

<!-- markdownlint-disable MD029 -->

# TiDB CloudとVercelの統合 {#integrate-tidb-cloud-with-vercel}

[ヴェルセル](https://vercel.com/)はフロントエンド開発者向けのプラットフォームであり、イノベーターがインスピレーションの瞬間に創造するために必要なスピードと信頼性を提供します。

TiDB Cloud をVercel と併用することで、MySQL 互換のリレーショナル モデルを使用して新しいフロントエンド アプリケーションをより迅速に構築し、回復力、拡張性、最高レベルのデータ プライバシーとセキュリティを実現するプラットフォームを使用して自信を持ってアプリを拡張できます。

このガイドでは、次のいずれかの方法を使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続する方法について説明します。

-   [TiDB Cloud Vercel統合を介して接続](#connect-via-the-tidb-cloud-vercel-integration)
-   [環境変数を手動で設定して接続する](#connect-via-manually-setting-environment-variables)

上記の両方の方法では、 TiDB Cloud はプログラムによってデータベースに接続するための次のオプションを提供します。

-   クラスタ: 直接接続または[サーバーレスドライバー](/tidb-cloud/serverless-driver.md)を使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続します。
-   [データアプリ](/tidb-cloud/data-service-manage-data-app.md) : HTTP エンドポイントのコレクションを通じてTiDB Cloudクラスターのデータにアクセスします。

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### VercelアカウントとVercelプロジェクト {#a-vercel-account-and-a-vercel-project}

Vercel のアカウントとプロジェクトが必要です。まだお持ちでない場合は、以下の Vercel ドキュメントを参照して作成してください。

-   [新しい個人アカウントを作成する](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)または[新しいチームの作成](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team) 。
-   Vercel の[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)使用している場合、またはデプロイするアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試してみることができます。

1つのVercelプロジェクトは1つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断し、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudのアカウントとクラスターが必要です。まだお持ちでない場合は、以下を参照して作成してください。

-   [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注記：**
    >
    > TiDB Cloud Vercel 統合は、 TiDB Cloud Serverless クラスターの作成をサポートしています。統合プロセス中に後からクラスターを作成することもできます。

-   [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

    > **注記：**
    >
    > TiDB Cloud Dedicated クラスターの場合、Vercel デプロイメントでは[動的IPアドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用されるため、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) が接続に許可されていることを確認してください。

[TiDB Cloud Vercel統合を介してVercelと統合する](#connect-via-the-tidb-cloud-vercel-integration)については、所属組織の`Organization Owner`ロール、またはTiDB Cloudの対象プロジェクトの`Project Owner`ロールを担うことが求められます。詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)ご覧ください。

1 つのTiDB Cloudクラスターは複数の Vercel プロジェクトに接続できます。

### データアプリとエンドポイント {#a-data-app-and-endpoints}

[データアプリ](/tidb-cloud/data-service-manage-data-app.md)経由でTiDB Cloudクラスターに接続する場合は、事前にTiDB Cloudに対象のデータアプリとエンドポイントを用意しておく必要があります。まだ用意していない場合は、以下を参照して作成してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  プロジェクトの[データアプリを作成する](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) 。
3.  [データアプリをリンクする](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)ターゲットのTiDB Cloudクラスターに追加します。
4.  [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)なので、SQL ステートメントを実行するようにカスタマイズできます。

1つのVercelプロジェクトは1つのTiDB Cloudデータアプリにのみ接続できます。Vercelプロジェクトのデータアプリを変更するには、まず現在のアプリを切断し、新しいアプリに接続する必要があります。

## TiDB Cloud Vercel統合を介して接続 {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel統合を介して接続するには、 [Vercelの統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページに進みます。この方法では、接続するクラスターを選択すると、 TiDB CloudがVercelプロジェクトに必要なすべての環境変数を自動的に生成します。

> **注記：**
>
> この方法はTiDB Cloud Serverlessクラスターでのみ利用可能です。TiDB TiDB Cloud Dedicatedクラスターに接続する場合は、 [手動の方法](#connect-via-manually-setting-environment-variables)使用してください。

### 統合ワークフロー {#integration-workflow}

詳細な手順は次のとおりです。

<SimpleTab>
<div label="Cluster">

1.  [TiDB Cloud Vercel統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある**「統合を追加」を**クリックします。 **「TiDB Cloudを追加」**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合を追加」**をクリックします。すると、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、次の操作を行います。

    1.  対象の Vercel プロジェクトを選択し、 **「次へ」**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**「クラスタ」**を選択します。
    4.  対象のTiDB Cloudクラスターを選択します。 **「クラスタ」**ドロップダウンリストが空の場合、または新しいTiDB Cloud Serverlessクラスターを選択する場合は、リスト内の**「+クラスタの作成」**をクリックしてクラスターを作成してください。
    5.  接続するデータベースを選択します。**データベースの**ドロップダウンリストが空の場合、または新しいデータベースを選択する場合は、リスト内の**「+ データベースの作成」**をクリックしてデータベースを作成してください。
    6.  Vercelプロジェクトで使用しているフレームワークを選択してください。ターゲットフレームワークがリストにない場合は、 **「一般」**を選択してください。フレームワークによって環境変数が異なります。
    7.  プレビュー環境用の新しいブランチを作成するために**ブランチ**を有効にするかどうかを選択します。
    8.  **「統合を追加」をクリックして、Vercel に戻ります**。

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

1.  [TiDB Cloud Vercel統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある**「統合を追加」を**クリックします。 **「TiDB Cloudを追加」**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合を追加」**をクリックします。すると、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、次の操作を行います。

    1.  対象の Vercel プロジェクトを選択し、 **「次へ」**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**データ アプリ**を選択します。
    4.  ターゲットの TiDB データ アプリを選択します。
    5.  **「統合を追加」をクリックして、Vercel に戻ります**。

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

[TiDB Cloud Vercel統合](https://vercel.com/integrations/tidb-cloud)インストールしている場合は、統合内で接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **「統合」**をクリックします。
2.  TiDB Cloudエントリで**[管理] を**クリックします。
3.  **［構成］**をクリックします。
4.  接続を追加または削除するには、 **「リンクの追加」**または**「削除」**をクリックします。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    接続を削除すると、統合ワークフローによって設定された環境変数もVercelプロジェクトから削除されます。ただし、このアクションはTiDB Cloud Serverlessクラスターのデータには影響しません。

### TiDB Cloud Serverless ブランチに接続 {#connect-with-tidb-cloud-serverless-branching}

Vercel の[プレビュー展開](https://vercel.com/docs/deployments/preview-deployments)機能を使用すると、Git プロジェクトの本番ブランチに変更をマージすることなく、ライブデプロイメントでアプリの変更をプレビューできます。 [TiDB Cloudサーバーレス ブランチ](/tidb-cloud/branch-overview.md)では、Vercel プロジェクトのブランチごとに新しいインスタンスを作成できます。これにより、本番データに影響を与えることなく、ライブデプロイメントでアプリの変更をプレビューできます。

> **注記：**
>
> 現在、 TiDB Cloud Serverless ブランチは[GitHubリポジトリに関連付けられたVercelプロジェクト](https://vercel.com/docs/deployments/git/vercel-for-github)のみをサポートしています。

TiDB Cloud Serverless Branching を有効にするには、 [TiDB Cloud Vercel 統合ワークフロー](#integration-workflow)で次の点を確認する必要があります。

1.  接続タイプとして**「クラスタ」**を選択します。
2.  **ブランチ**を有効にして、プレビュー環境用の新しいブランチを作成します。

Gitリポジトリに変更をプッシュすると、Vercelはプレビューデプロイメントをトリガーします。TiDB TiDB Cloud統合により、Gitブランチ用のTiDB Cloud Serverlessブランチが自動的に作成され、環境変数が設定されます。詳細な手順は以下のとおりです。

1.  Git リポジトリに新しいブランチを作成します。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2.  いくつか変更を加えて、その変更をリモート リポジトリにプッシュします。

3.  Vercel は新しいブランチのプレビュー展開をトリガーします。

    ![Vercel Preview\_Deployment](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1.  デプロイ中に、 TiDB Cloud統合により、Git ブランチと同じ名前のTiDB Cloud Serverless ブランチが自動的に作成されます。TiDB TiDB Cloud Serverless ブランチが既に存在する場合、 TiDB Cloud統合はこの手順をスキップします。

        ![TiDB\_Cloud\_Branch\_Check](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2.  TiDB Cloud Serverless ブランチの準備が整うと、 TiDB Cloud統合によって、Vercel プロジェクトのプレビュー デプロイメントで環境変数が設定されます。

        ![Preview\_Envs](/media/tidb-cloud/vercel/preview-envs.png)

    3.  TiDB Cloud統合では、 TiDB Cloud Serverless ブランチの準備が整うまで待機するためのブロッキングチェックも登録されます。このチェックは手動で再実行できます。

4.  チェックに合格したら、プレビュー デプロイメントにアクセスして変更を確認できます。

> **注記：**
>
> Vercel のデプロイメントワークフローの制限により、デプロイメントで環境変数が確実に設定されるとは限りません。この場合、デプロイメントを再デプロイする必要があります。

> **注記：**
>
> TiDB Cloudでは、組織ごとにデフォルトで最大5つのTiDB Cloud Serverless ブランチを作成できます。この制限を超えないようにするには、不要になったTiDB Cloud Serverless ブランチを削除してください。詳細については、 [TiDB Cloud Serverlessブランチを管理する](/tidb-cloud/branch-manage.md)ご覧ください。

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

<SimpleTab>
<div label="Cluster">

1.  TiDB クラスターの接続情報を取得します。

    接続情報は、クラスターの接続ダイアログから取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲットクラスターの名前をクリックして概要ページに移動し、右上隅の**「接続」**をクリックします。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に応じて[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)実行します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

ここではPrismaアプリケーションを例として使用します。以下は、 TiDB Cloud ServerlessクラスターのPrismaスキーマファイルのデータソース設定です。

    datasource db {
        provider = "mysql"
        url      = env("DATABASE_URL")
    }

Vercel では、次のように環境変数を宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

`<User>` `<Endpoint>`情報`<Database>` `<Password>` TiDB Cloudコンソールで取得できます`<Port>`

</div>
<div label="Data App">

1.  データ アプリとそのエンドポイントをまだ作成していない場合は、手順[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)と[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)に従って作成します。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、データ アプリの接続情報に応じて[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)実行します。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    Vercel では、次のように環境変数を宣言できます。

    -   **キー**= `DATA_APP_BASE_URL`
    -   **値**= `<DATA_APP_BASE_URL>`
    -   **キー**= `DATA_APP_PUBLIC_KEY`
    -   **値**= `<DATA_APP_PUBLIC_KEY>`
    -   **キー**= `DATA_APP_PRIVATE_KEY`
    -   **値**= `<DATA_APP_PRIVATE_KEY>`

    `<DATA_APP_BASE_URL>` `<DATA_APP_PRIVATE_KEY>`情報は`<DATA_APP_PUBLIC_KEY>` TiDB Cloudコンソールの[データサービス](https://tidbcloud.com/project/data-service)ページから取得できます。

</div>
</SimpleTab>
