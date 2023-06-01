---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

<!-- markdownlint-disable MD029 -->

# TiDB Cloudと Vercel を統合する {#integrate-tidb-cloud-with-vercel}

[<a href="https://vercel.com/">ヴェルセル</a>](https://vercel.com/)はフロントエンド開発者向けのプラットフォームで、イノベーターがインスピレーションの瞬間に作成する必要があるスピードと信頼性を提供します。

Vercel でTiDB Cloudを使用すると、MySQL 互換のリレーショナル モデルで新しいフロントエンド アプリケーションをより迅速に構築でき、復元力、拡張性、最高レベルのデータ プライバシーとセキュリティを目指して構築されたプラットフォームで自信を持ってアプリを成長させることができます。

このガイドでは、次のいずれかの方法を使用してTiDB Cloudクラスターを Vercel プロジェクトに接続する方法について説明します。

-   [<a href="#connect-via-the-tidb-cloud-vercel-integration">TiDB Cloud Vercel 統合経由で接続する</a>](#connect-via-the-tidb-cloud-vercel-integration)
-   [<a href="#connect-via-manually-setting-environment-variables">環境変数を手動で構成して接続する</a>](#connect-via-manually-setting-environment-variables)

## 前提条件 {#prerequisites}

接続する前に、次の前提条件が満たされていることを確認してください。

### Vercel アカウントと Vercel プロジェクト {#a-vercel-account-and-a-vercel-project}

Vercel にアカウントとプロジェクトが必要です。何も持っていない場合は、次の Vercel ドキュメントを参照して作成してください。

-   [<a href="https://vercel.com/docs/teams-and-accounts#creating-a-personal-account">新しい個人アカウントの作成</a>](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account)または[<a href="https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team">新しいチームを作成する</a>](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team) 。
-   Vercel では[<a href="https://vercel.com/docs/concepts/projects/overview#creating-a-project">プロジェクトの作成</a>](https://vercel.com/docs/concepts/projects/overview#creating-a-project)使用するか、デプロイするアプリケーションがない場合は、 [<a href="https://vercel.com/templates/next.js/tidb-cloud-starter">TiDB Cloudスターター テンプレート</a>](https://vercel.com/templates/next.js/tidb-cloud-starter)使用して試すことができます。

1 つの Vercel プロジェクトは 1 つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断してから、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。お持ちでない場合は[<a href="/tidb-cloud/create-tidb-cluster.md">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md)を参照してください。

[<a href="#connect-via-the-tidb-cloud-vercel-integration">TiDB Cloud Vercel Integration を介して Vercel と統合する</a>](#connect-via-the-tidb-cloud-vercel-integration)では、組織への「オーナー」アクセス権、またはTiDB Cloudのターゲット プロジェクトへの「メンバー」アクセス権を持っていることが期待されます。詳細については、 [<a href="/tidb-cloud/manage-user-access.md#manage-role-access">役割のアクセスを管理する</a>](/tidb-cloud/manage-user-access.md#manage-role-access)を参照してください。

1 つのTiDB Cloudクラスターは複数の Vercel プロジェクトに接続できます。

### TiDB Cloudのトラフィック フィルターに許可されるすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

Dedicated Tierクラスターの場合は、クラスターのトラフィック フィルターですべての IP アドレス ( `0.0.0.0/0`に設定) の接続が許可されていることを確認してください。これは、Vercel デプロイメントでは[<a href="https://vercel.com/guides/how-to-allowlist-deployment-ip-address">動的IPアドレス</a>](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)使用されるためです。 TiDB Cloud Vercel 統合を使用する場合、 TiDB Cloud は統合ワークフローのクラスターにトラフィック フィルター`0.0.0.0/0`自動的に追加します (存在しない場合)。

Serverless Tierクラスターでは、デフォルトですべての IP アドレスの接続が許可されるため、トラフィック フィルターを構成する必要はありません。

## TiDB Cloud Vercel 統合経由で接続する {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel 統合経由で接続するには、 [<a href="https://vercel.com/integrations">Vercel の統合マーケットプレイス</a>](https://vercel.com/integrations)から[<a href="https://vercel.com/integrations/tidb-cloud">TiDB Cloud統合</a>](https://vercel.com/integrations/tidb-cloud)ページに移動します。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloud はVercel プロジェクトに必要なすべての環境変数を自動的に生成します。

詳細な手順は次のとおりです。

1.  [<a href="https://vercel.com/integrations/tidb-cloud">TiDB Cloud Vercel の統合</a>](https://vercel.com/integrations/tidb-cloud)ページの右上領域にある**「統合の追加」**をクリックします。 **[TiDB Cloudの追加]**ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、 **[続行]**をクリックします。
3.  統合を追加する Vercel プロジェクトを選択し、 **[続行]**をクリックします。
4.  統合に必要な権限を確認し、 **[統合を追加]**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  左側で、ターゲットの Vercel プロジェクトと Vercel プロジェクトが使用するフレームワークを選択します。フレームワークがリストにない場合は、 **[全般]**を選択します。フレームワークが異なれば、決定される環境変数も異なります。
6.  クラスター情報を指定した後、右側でターゲットのTiDB Cloudクラスターを選択します。各TiDB Cloudクラスターは[<a href="/tidb-cloud/manage-user-access.md#organizations-and-projects">組織とプロジェクト</a>](/tidb-cloud/manage-user-access.md#organizations-and-projects)に属します。
7.  **[統合を追加して Vercel に戻る]**をクリックします。

![Vercel Integration Page](/media/tidb-cloud/integration-vercel-link-page.png)

8.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、 **[設定]** &gt; **[環境変数]**をクリックして、環境変数が自動的に追加されたことを確認します。

    変数が追加されていれば接続は完了です。

統合セットアップを完了し、 TiDB Cloudクラスターを Vercel プロジェクトに正常に接続すると、接続に必要な情報がプロジェクトの環境変数に自動的に設定されます。

**全般的**

```shell
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

Dedicated Tierクラスターの場合、ルート CA は次の変数に設定されます。

```
TIDB_SSL_CA
```

**プリズマ**

```
DATABASE_URL
```

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

1.  [<a href="/tidb-cloud/connect-via-standard-connection.md">標準接続経由でTiDB Cloudクラスターに接続する</a>](/tidb-cloud/connect-via-standard-connection.md)の手順に従って、TiDB クラスターの接続情報を取得します。

    > **ノート：**
    >
    > Dedicated Tierクラスターの場合は、この手順で**「どこからでもアクセスを許可」**トラフィック フィルターを設定していることを確認してください。

2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;**環境変数**に移動し、TiDB クラスターの接続情報に従って[<a href="https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable">各環境変数の値を宣言する</a>](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)に移動します。

![Vercel Environment Variables](/media/tidb-cloud/integration-vercel-environment-variables.png)

ここでは例として Prisma アプリケーションを使用します。以下は、 TiDB CloudServerless Tierクラスターの Prisma スキーマ ファイル内のデータソース設定です。

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

Vercel では、次のように環境変数を宣言できます。

-   **キー**= `DATABASE_URL`
-   **値**= `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

TiDB Cloudコンソールで`<User>` 、 `<Password>` 、 `<Endpoint>` 、 `<Port>` 、および`<Database>`の情報を取得できます。

## 接続を構成する {#configure-connections}

[<a href="https://vercel.com/integrations/tidb-cloud">TiDB Cloud Vercel の統合</a>](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内の接続を追加または削除できます。

1.  Vercel ダッシュボードで、 **[統合]**をクリックします。
2.  [TiDB Cloud]エントリで**[管理]**をクリックします。
3.  **「構成」**をクリックします。
4.  **[プロジェクトの追加]**または**[削除]**をクリックして接続を追加または削除します。

![Vercel Integration Configuration Page](/media/tidb-cloud/integration-vercel-configuration-page.png)

接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。トラフィック フィルターとTiDB Cloudクラスターのデータは影響を受けません。
