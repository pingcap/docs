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

-   クラスタ: 直接接続または[サーバーレスドライバー](/tidb-cloud/serverless-driver.md)を使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続します。
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
    > TiDB 専用クラスターの場合、Vercel デプロイメントでは[動的IPアドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用されるため、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。

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

> **注記：**
>
> この方法は、TiDB サーバーレス クラスターでのみ使用できます。 TiDB 専用クラスターに接続する場合は、 [手動による方法](#connect-via-manually-setting-environment-variables)を使用します。

### 統合ワークフロー {#integration-workflow}

詳細な手順は次のとおりです。

<SimpleTab>
<div label="Cluster">

1.  [TiDB Cloud Vercel の統合](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**「統合の追加」**をクリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **[続行]**をクリックします。
4.  統合に必要な権限を確認し、 **[統合の追加]**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで次の操作を行います。

    1.  ターゲットの Vercel プロジェクトを選択し、 **[次へ]**をクリックします。
    2.  ターゲットのTiDB Cloud組織とプロジェクトを選択します。
    3.  接続タイプとして**クラスタを**選択します。
    4.  ターゲットのTiDB Cloudクラスターを選択します。 **[クラスタ]**ドロップダウン リストが空である場合、または新しい TiDB サーバーレス クラスターを選択する場合は、リスト内の**[+クラスタ**を作成します。
    5.  接続するデータベースを選択します。 **[データベース]**ドロップダウン リストが空の場合、または新しいデータベースを選択する場合は、リスト内の**[+ データベースの作成]**をクリックしてデータベースを作成します。
    6.  Vercel プロジェクトが使用しているフレームワークを選択します。ターゲット フレームワークがリストにない場合は、 **[一般]**を選択します。フレームワークが異なれば、決定される環境変数も異なります。
    7.  **ブランチングで**プレビュー環境用に新しいブランチを作成できるようにするかどうかを選択します。
    8.  **[統合を追加して Vercel に戻る]**をクリックします。

![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)

6.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、 **[設定]** &gt; **[環境変数]**をクリックして、ターゲット TiDB クラスターの環境変数が自動的に追加されているかどうかを確認します。

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

### 接続を構成する {#configure-connections}

[TiDB Cloud Vercel の統合](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内の接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **[統合]**をクリックします。
2.  [TiDB Cloud]エントリで**[管理]**をクリックします。
3.  **「構成」**をクリックします。
4.  **[リンクの追加]**または**[削除]**をクリックして接続を追加または削除します。

    ![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

    接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。ただし、このアクションは TiDB サーバーレス クラスターのデータには影響しません。

### TiDB サーバーレス ブランチで接続する {#connect-with-tidb-serverless-branching}

Vercel の[導入のプレビュー](https://vercel.com/docs/deployments/preview-deployments)機能を使用すると、Git プロジェクトの本番ブランチに変更をマージせずに、ライブ デプロイメントでアプリへの変更をプレビューできます。 [TiDB サーバーレス ブランチング](/tidb-cloud/branch-overview.md)を使用すると、Vercel プロジェクトのブランチごとに新しいインスタンスを作成できます。これにより、本番データに影響を与えることなく、ライブ デプロイメントでアプリの変更をプレビューできます。

> **注記：**
>
> 現在、TiDB サーバーレス ブランチは[GitHub リポジトリに関連付けられた Vercel プロジェクト](https://vercel.com/docs/deployments/git/vercel-for-github)のみをサポートしています。

TiDB サーバーレス ブランチングを有効にするには、 [TiDB Cloud Vercel 統合ワークフロー](#integration-workflow)で次のことを確認する必要があります。

1.  接続タイプとして**クラスタを**選択します。
2.  **ブランチングを**有効にして、プレビュー環境用に新しいブランチを作成します。

変更を Git リポジトリにプッシュすると、Vercel はプレビュー デプロイメントをトリガーします。 TiDB Cloud統合により、Git ブランチ用の TiDB サーバーレス ブランチが自動的に作成され、環境変数が設定されます。詳細な手順は次のとおりです。

1.  Git リポジトリに新しいブランチを作成します。

    ```shell
    cd tidb-prisma-vercel-demo1
    git checkout -b new-branch
    ```

2.  いくつかの変更を追加し、その変更をリモート リポジトリにプッシュします。

3.  Vercel は、新しいブランチのプレビュー デプロイメントをトリガーします。

    ![Vercel Preview\_Deployment](/media/tidb-cloud/vercel/vercel-preview-deployment.png)

    1.  デプロイメント中に、 TiDB Cloud統合により、Git ブランチと同じ名前の TiDB サーバーレス ブランチが自動的に作成されます。 TiDB サーバーレス ブランチがすでに存在する場合、 TiDB Cloud統合ではこのステップがスキップされます。

        ![TiDB\_Cloud\_Branch\_Check](/media/tidb-cloud/vercel/tidbcloud-branch-check.png)

    2.  TiDB サーバーレス ブランチの準備が完了すると、 TiDB Cloud統合によって Vercel プロジェクトのプレビュー デプロイメントに環境変数が設定されます。

        ![Preview\_Envs](/media/tidb-cloud/vercel/preview-envs.png)

    3.  TiDB Cloud統合では、TiDB サーバーレス ブランチの準備ができるまで待機するためのブロック チェックも登録します。チェックを手動で再実行できます。

4.  チェックに合格したら、プレビュー展開にアクセスして変更を確認できます。

> **注記：**
>
> Vercel デプロイメント ワークフローの制限により、デプロイメント内で環境変数が確実に設定されるようにすることはできません。この場合、デプロイメントを再デプロイする必要があります。

> **注記：**
>
> TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス ブランチを作成できます。制限を超えないようにするために、不要になった TiDB サーバーレス ブランチを削除できます。詳細については、 [TiDB サーバーレス ブランチを管理する](/tidb-cloud/branch-manage.md)を参照してください。

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

<SimpleTab>
<div label="Cluster">

1.  TiDB クラスターの接続情報を取得します。

    クラスターの接続ダイアログから接続情報を取得できます。ダイアログを開くには、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動し、右上隅の**[接続]**をクリックします。

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
