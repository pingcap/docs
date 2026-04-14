---
title: Integrate TiDB Cloud with Vercel
summary: TiDB CloudクラスターをVercelプロジェクトに接続する方法を学びましょう。
---

<!-- markdownlint-disable MD029 -->

# TiDB CloudとVercelを統合する {#integrate-tidb-cloud-with-vercel}

[ヴェルセル](https://vercel.com/)はフロントエンド開発者向けのプラットフォームであり、イノベーターがひらめきの瞬間に創造するために必要なスピードと信頼性を提供します。

TiDB CloudとVercelを組み合わせることで、MySQL互換のリレーショナルモデルを使用して新しいフロントエンドアプリケーションをより迅速に構築できるだけでなく、回復力、拡張性、そして最高レベルのデータプライバシーとセキュリティを備えたプラットフォームによって、自信を持ってアプリケーションを成長させることができます。

このガイドでは、以下のいずれかの方法を使用して、 TiDB CloudのリソースをVercelプロジェクトに接続する方法について説明します。

-   [TiDB Cloud Vercelとの連携を介して接続します。](#connect-via-the-tidb-cloud-vercel-integration)
-   [環境変数を手動で設定して接続します](#connect-via-manually-setting-environment-variables)

上記2つの方法のいずれにおいても、 TiDB Cloudはデータベースにプログラムで接続するための以下のオプションを提供します。

-   クラスタ: 直接接続または[サーバーレスドライバー](/develop/serverless-driver.md)レス ドライバーを使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続します。
-   [データアプリ](/tidb-cloud/data-service-manage-data-app.md): HTTP エンドポイントのコレクションを通じてTiDB Cloudクラスターのデータにアクセスします。

## 前提条件 {#prerequisites}

接続する前に、以下の前提条件が満たされていることを確認してください。

### VercelアカウントとVercelプロジェクト {#a-vercel-account-and-a-vercel-project}

Vercelにアカウントとプロジェクトをお持ちであることが前提となります。お持ちでない場合は、以下のVercelドキュメントを参照して作成してください。

-   [新しい個人アカウントを作成する](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)、 [新しいチームを作る](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team)。
-   Vercel で[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)か、デプロイするアプリケーションがない場合は、 [TiDB Cloud Starterテンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試すことができます。

Vercelプロジェクトは、1つのTiDB Cloudクラスターにしか接続できません。統合を変更するには、まず現在のクラスターとの接続を解除してから、新しいクラスターに接続する必要があります。

### TiDB CloudアカウントとTiDBクラスタ {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが既に作成されている必要があります。アカウントとクラスターをお持ちでない場合は、以下の手順に従って作成してください。

-   [TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)

    > **注記：**
    >
    > TiDB Cloud Vercelとの連携では、TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスの作成がサポートされています。また、連携プロセス中に後からインスタンスを作成することも可能です。

-   [TiDB Cloud Dedicatedクラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

    > **注記：**
    >
    > TiDB Cloud Dedicatedクラスターの場合、Vercel デプロイメントは IP アドレスを使用するため、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0` } に設定) が接続を許可されて[動的IPアドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)ことを確認してください。

[TiDB Cloud Vercel統合を介してVercelと統合する](#connect-via-the-tidb-cloud-vercel-integration)には、組織の`Organization Owner`ロール、またはTiDB Cloudのターゲット プロジェクトの`Project Owner`ロールに所属することが求められます。詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

1つのTiDB Cloudクラスターは、複数のVercelプロジェクトに接続できます。

### データアプリとエンドポイント {#a-data-app-and-endpoints}

データ[データアプリ](/tidb-cloud/data-service-manage-data-app.md)を介してTiDB Cloudクラスターに接続する場合は、事前にTiDB Cloudに対象のデータアプリとエンドポイントが設定されている必要があります。設定されていない場合は、以下の手順に従って作成してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、プロジェクトの[**データサービス**](https://tidbcloud.com/project/data-service)ページに移動します。
2.  あなたのプロジェクトに合わせて[データアプリを作成する](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app)。
3.  [データアプリをリンクする](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources)ターゲットのTiDB Cloudクラスターにリンクします。
4.  [エンドポイントを管理する](/tidb-cloud/data-service-manage-endpoint.md)ことで、SQL ステートメントを実行するようにカスタマイズできます。

Vercelプロジェクトは、1つのTiDB Cloudデータアプリにしか接続できません。Vercelプロジェクトのデータアプリを変更するには、まず現在のアプリとの接続を解除してから、新しいアプリに接続する必要があります。

## TiDB Cloud Vercelとの連携を介して接続します。 {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel 統合経由で接続するには、 [Vercelの統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページにアクセスしてください。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloud はVercel プロジェクトに必要なすべての環境変数を自動的に生成します。

> **注記：**
>
> この方法は、 TiDB Cloud StarterおよびTiDB Cloud Essentialインスタンスでのみ利用可能です。TiDB Cloud Dedicatedクラスターに接続する場合は、 [手動法](#connect-via-manually-setting-environment-variables)を使用してください。

### 統合ワークフロー {#integration-workflow}

詳細な手順は以下のとおりです。

<SimpleTab>
<div label="Cluster">

1.  [TiDB Cloud Vercelとの統合](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**[統合の追加] を**クリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウンリストから統合の範囲を選択し、 **「続行」**をクリックしてください。
3.  統合を追加するVercelプロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合を追加」**をクリックしてください。すると、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、以下の操作を行います。

    1.  対象となるVercelプロジェクトを選択し、 **「次へ」**をクリックしてください。
    2.  対象となるTiDB Cloud組織とプロジェクトを選択してください。
    3.  接続タイプとして**「クラスタ」**を選択してください。
    4.  対象のTiDB Cloudリソースを選択してください。**クラスタの**ドロップダウン リストが空の場合、または新しいTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを選択する場合は、リストの**[+クラスタの作成**] をクリックして作成してください。
    5.  接続するデータベースを選択してください。**データベースの**ドロップダウンリストが空の場合、または新しいデータベースを選択する場合は、リスト内の**「+ データベースの作成**」をクリックして作成してください。
    6.  Vercelプロジェクトで使用しているフレームワークを選択してください。対象のフレームワークが一覧にない場合は、 **「一般」**を選択してください。フレームワークによって環境変数が異なります。
    7.  プレビュー環境用に新しいブランチを作成するために、**ブランチ機能**を有効にするかどうかを選択してください。
    8.  **「統合を追加」をクリックしてVercelに戻ります**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6.  Vercelダッシュボードに戻り、Vercelプロジェクトに移動して、 **[設定]** &gt; **[環境変数]**をクリックし、対象のTiDBクラスタの環境変数が自動的に追加されているかどうかを確認してください。

    以下の変数が追加された場合、積分は完了です。

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

1.  [TiDB Cloud Vercelとの統合](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**[統合の追加] を**クリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウンリストから統合の範囲を選択し、 **「続行」**をクリックしてください。
3.  統合を追加するVercelプロジェクトを選択し、 **「続行」**をクリックします。
4.  統合に必要な権限を確認し、 **「統合を追加」**をクリックしてください。すると、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、以下の操作を行います。

    1.  対象となるVercelプロジェクトを選択し、 **「次へ」**をクリックしてください。
    2.  対象となるTiDB Cloud組織とプロジェクトを選択してください。
    3.  接続タイプとして**「データアプリ」**を選択してください。
    4.  対象のTiDBデータアプリを選択してください。
    5.  **「統合を追加」をクリックしてVercelに戻ります**。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)

6.  Vercelダッシュボードに戻り、Vercelプロジェクトに移動して、 **[設定]** &gt; **[環境変数]**をクリックし、対象のデータアプリの環境変数が自動的に追加されているかどうかを確認してください。

    以下の変数が追加された場合、積分は完了です。

    ```shell
    DATA_APP_BASE_URL
    DATA_APP_PUBLIC_KEY
    DATA_APP_PRIVATE_KEY
    ```

</div>
</SimpleTab>

### 接続を設定する {#configure-connections}

[TiDB Cloud Vercelとの統合](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内の接続を追加または削除できます。

1.  Vercelダッシュボードで、 **[統合]**をクリックします。
2.  TiDB Cloudのエントリで**「管理」**をクリックします。
3.  **「設定」**をクリックします。
4.  接続を追加または削除するには、 **「リンクを追加」**または**「削除」**をクリックします。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    接続を削除すると、統合ワークフローによって設定された環境変数もVercelプロジェクトから削除されます。ただし、この操作はTiDB Cloudクラスタのデータには影響しません。

### TiDB Cloudのブランチ機能に接続します {#connect-with-branching} {#connect-with-branching}

Vercel の[プレビュー展開](https://vercel.com/docs/deployments/preview-deployments)機能を使用すると、変更を Git プロジェクトの本番ブランチにマージすることなく、ライブデプロイメントでアプリの変更をプレビューできます。TiDB [TiDB Cloudブランチング](/tidb-cloud/branch-overview.md)を使用すると、Vercel プロジェクトのブランチごとに新しいインスタンスを作成できます。これにより、本番データに影響を与えることなく、ライブデプロイメントでアプリの変更をプレビューできます。

> **注記：**
>
> 現在、 TiDB Cloud Branching は[VercelプロジェクトとGitHubリポジトリの関連付け](https://vercel.com/docs/deployments/git/vercel-for-github)のみをサポートしています。

TiDB Cloud Branching を有効にするには、 [TiDB Cloud Vercel統合ワークフロー](#integration-workflow)で次のことを確認する必要があります。

1.  接続タイプとして**「クラスタ」**を選択してください。
2.  プレビュー環境用の新しいブランチを作成するには、**ブランチ機能**を有効にしてください。

Gitリポジトリに変更をプッシュすると、Vercelがプレビューデプロイメントをトリガーします。TiDB Cloudとの連携により、Gitブランチ用のTiDB Cloudクラスタのブランチが自動的に作成され、環境変数が設定されます。詳細な手順は以下のとおりです。

1.  Gitリポジトリに新しいブランチを作成します。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2.  変更を加えて、その変更をリモートリポジトリにプッシュします。

3.  Vercelは、新しいブランチのプレビュー展開を開始します。

    ![Vercel Preview\_Deployment](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1.  デプロイ時に、 TiDB Cloud統合機能は、Gitブランチと同じ名前のブランチをクラスタ用に自動的に作成します。ブランチが既に存在する場合は、 TiDB Cloud統合機能はこの手順をスキップします。

        ![TiDB\_Cloud\_Branch\_Check](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2.  ブランチの準備が完了すると、 TiDB Cloud統合によって、Vercelプロジェクトのプレビューデプロイメントで環境変数が設定されます。

        ![Preview\_Envs](/media/tidb-cloud/vercel/preview-envs.png)

    3.  TiDB Cloudとの連携により、ブランチの準備が整うまで待機するためのブロッキングチェックも登録されます。このチェックは手動で再実行することも可能です。

4.  チェックに合格したら、プレビュー環境にアクセスして変更内容を確認できます。

> **注記：**
>
> Vercelのデプロイワークフローの制限により、環境変数がデプロイ時に確実に設定されるとは限りません。この場合、デプロイを再実行する必要があります。

> **注記：**
>
> TiDB Cloudの各組織では、デフォルトではTiDB Cloud Starterインスタンス用に最大 5 つのブランチを作成できます。制限を超えないようにするには、不要になったTiDB Cloud Starterインスタンスのブランチを削除してください。詳細については、 [TiDB Cloudブランチを管理する](/tidb-cloud/branch-manage.md)参照してください。 .

## 環境変数を手動で設定して接続します {#connect-via-manually-setting-environment-variables}

<SimpleTab>
<div label="Cluster">

1.  TiDBクラスタの接続情報を取得します。

    接続情報は、クラスタの接続ダイアログから取得できます。ダイアログを開くには、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象リソースの名前をクリックして概要ページを開き、右上隅の**[接続]**をクリックします。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

ここでは例として、PrismaアプリケーションとTiDB Cloud Starterインスタンスを使用します。以下は、 TiDB Cloud StarterインスタンスのPrismaスキーマファイルにおけるデータソース設定です。

    datasource db {
        provider = "mysql"
        url      = env("DATABASE_URL")
    }

Vercelでは、環境変数を次のように宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

TiDB Cloud コンソールでは、 `<User>` 、 `<Password>` 、 `<Endpoint>` 、 `<Port>` 、および`<Database>`TiDB Cloudを取得できます。

</div>
<div label="Data App">

1.  データ アプリとそのエンドポイントをまだ作成していない場合は、「データ アプリ[データアプリを管理する](/tidb-cloud/data-service-manage-data-app.md)と[エンドポイントの管理](/tidb-cloud/data-service-manage-endpoint.md)の手順に従ってデータ アプリとそのエンドポイントを作成します。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、データ アプリの接続情報に従って[各環境変数の値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)。

    ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

    Vercelでは、環境変数を次のように宣言できます。

    -   **キー**= `DATA_APP_BASE_URL`
    -   **値**= `<DATA_APP_BASE_URL>`
    -   **キー**= `DATA_APP_PUBLIC_KEY`
    -   **値**= `<DATA_APP_PUBLIC_KEY>`
    -   **キー**= `DATA_APP_PRIVATE_KEY`
    -   **値**= `<DATA_APP_PRIVATE_KEY>`

    `<DATA_APP_BASE_URL>` 、 `<DATA_APP_PUBLIC_KEY>` 、 `<DATA_APP_PRIVATE_KEY>`の情報は、 TiDB Cloudコンソールのデータ [データサービス](https://tidbcloud.com/project/data-service)ページから取得できます。

</div>
</SimpleTab>
