---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloudと Vercel の統合 {#integrate-tidb-cloud-with-vercel}

[ヴェルセル](https://vercel.com/)はフロントエンド開発者向けのプラットフォームであり、イノベーターがひらめいた瞬間に作成するために必要なスピードと信頼性を提供します。

Vercel でTiDB Cloudを使用すると、MySQL 互換のリレーショナル モデルを使用して新しいフロントエンド アプリケーションをより迅速に構築し、回復力、拡張性、および最高レベルのデータ プライバシーとセキュリティのために構築されたプラットフォームで自信を持ってアプリを成長させることができます。

このガイドでは、次のいずれかの方法を使用して、 TiDB Cloudクラスターを Vercel プロジェクトに接続する方法について説明します。

-   [TiDB Cloud Vercel 統合を介して接続する](#connect-via-the-tidb-cloud-vercel-integration)
-   [環境変数を手動で構成して接続する](#connect-via-manually-setting-environment-variables)

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Vercel アカウントと Vercel プロジェクト {#a-vercel-account-and-a-vercel-project}

Vercel にアカウントとプロジェクトが必要です。持っていない場合は、次の Vercel ドキュメントを参照して作成してください。

-   [新しい個人アカウントの作成](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)または[新しいチームの作成](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team) 。
-   Vercel で[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)使用するか、デプロイするアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試すことができます。

1 つの Vercel プロジェクトは、1 つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断してから、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。持っていない場合は、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

[TiDB Cloud Vercel Integration を介して Vercel と統合する](#connect-via-the-tidb-cloud-vercel-integration)に、組織への「所有者」アクセス、またはTiDB Cloudのターゲット プロジェクトへの「メンバー」アクセスが必要です。詳細については、 [ロール アクセスの管理](/tidb-cloud/manage-user-access.md#manage-role-access)を参照してください。

1 つのTiDB Cloudクラスターで複数の Vercel プロジェクトに接続できます。

### TiDB Cloudでトラフィック フィルターに許可されているすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

Dedicated Tierクラスターの場合、クラスターのトラフィック フィルターがすべての IP アドレス ( `0.0.0.0/0`に設定) の接続を許可していることを確認してください。これは、Vercel デプロイが[動的 IP アドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用するためです。 TiDB Cloud Vercel 統合を使用する場合、 TiDB Cloud は、統合ワークフローでクラスターに`0.0.0.0/0`トラフィック フィルターを自動的に追加します (存在しない場合)。

Serverless Tierクラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## TiDB Cloud Vercel 統合を介して接続する {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel インテグレーション経由で接続するには、 [Vercel の統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページに移動します。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloud はVercel プロジェクトに必要なすべての環境変数を自動的に生成します。

詳細な手順は次のとおりです。

1.  [TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある**[統合の追加]**をクリックします。 <strong>[TiDB Cloudの追加]</strong>ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **[続行]**をクリックします。
4.  統合に必要な権限を確認し、 **ADD INTEGRATION**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  左側で、ターゲットの Vercel プロジェクトを選択し、使用する Vercel プロジェクトのフレームワークを作成します。フレームワークがリストされていない場合は、 **[一般]**を選択します。異なるフレームワークは、異なる環境変数を決定します。
6.  右側で、クラスター情報を提供した後、ターゲットのTiDB Cloudクラスターを選択します。各TiDB Cloudクラスターは[組織とプロジェクト](/tidb-cloud/manage-user-access.md#organizations-and-projects)に属します。
7.  **[統合を追加して Vercel に戻る]**をクリックします。

![Vercel Integration Page](/media/tidb-cloud/integration-vercel-link-page.png)

8.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、 **[設定]** &gt; <strong>[環境変数]</strong>をクリックして、環境変数が自動的に追加されていることを確認します。

    変数が追加されていれば、接続は完了です。

統合セットアップを完了し、 TiDB Cloudクラスターを Vercel プロジェクトに正常に接続すると、接続に必要な情報がプロジェクトの環境変数に自動的に設定されます。

**全般的**

```shell
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

Dedicated Tierクラスターの場合、ルート CA はこの変数に設定されます。

```
TIDB_SSL_CA
```

**プリズマ**

```
DATABASE_URL
```

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

1.  [標準接続を介してTiDB Cloudクラスターに接続する](/tidb-cloud/connect-via-standard-connection.md)の手順に従って、TiDB クラスターの接続情報を取得します。

    > **ノート：**
    >
    > Dedicated Tierクラスターの場合は、このステップで**[どこからでもアクセスを許可する]**トラフィック フィルターを設定していることを確認してください。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;<strong>環境変数</strong>に移動し、TiDB クラスターの接続情報に従って[各環境変数値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)に進みます。

![Vercel Environment Variables](/media/tidb-cloud/integration-vercel-environment-variables.png)

ここでは例として Prisma アプリケーションを使用します。以下は、 TiDB Cloud Serverless Tierクラスターの Prisma スキーマ ファイルのデータソース設定です。

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

Vercel では、環境変数を次のように宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

TiDB Cloudコンソールで`<User>` 、 `<Password>` 、 `<Endpoint>` 、 `<Port>` 、および`<Database>`の情報を取得できます。

## 接続の構成 {#configure-connections}

[TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内で接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **[統合]**をクリックします。
2.  TiDB Cloudエントリで**[管理]**をクリックします。
3.  **[構成]**をクリックします。
4.  **[プロジェクトの追加]**または<strong>[削除]</strong>をクリックして、接続を追加または削除します。

![Vercel Integration Configuration Page](/media/tidb-cloud/integration-vercel-configuration-page.png)

接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。トラフィック フィルターとTiDB Cloudクラスターのデータは影響を受けません。
