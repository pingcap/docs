---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

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
-   Vercel で[プロジェクトの作成](https://vercel.com/docs/concepts/projects/overview#creating-a-project)を使用するか、デプロイするアプリケーションがない場合は、 [TiDB Cloudスターター テンプレート](https://vercel.com/templates/next.js/tidb-cloud-starter)を使用して試すことができます。

1 つの Vercel プロジェクトは、1 つのTiDB Cloudクラスターにのみ接続できます。統合を変更するには、まず現在のクラスターを切断してから、新しいクラスターに接続する必要があります。

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudにアカウントとクラスターが必要です。持っていない場合は、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

Vercel と統合するには、組織への「所有者」アクセス、またはTiDB Cloudのターゲット プロジェクトへの「メンバー」アクセスが必要です。詳細については、 [メンバーの役割を構成する](/tidb-cloud/manage-user-access.md#configure-member-roles)を参照してください。

1 つのTiDB Cloudクラスターで複数の Vercel プロジェクトに接続できます。

### TiDB Cloudでトラフィック フィルターに許可されているすべての IP アドレス {#all-ip-addresses-allowed-for-traffic-filter-in-tidb-cloud}

TiDB Cloudクラスターのトラフィック フィルターで、接続にすべての IP アドレス ( `0.0.0.0/0`に設定) が許可されていることを確認してください。これは、Vercel のデプロイで[動的 IP アドレス](https://vercel.com/guides/how-to-allowlist-deployment-ip-address)が使用されているためです。 TiDB Cloud Vercel 統合を使用する場合、TiDB TiDB Cloudは、統合ワークフローでクラスターに`0.0.0.0/0`トラフィック フィルターを自動的に追加します (存在しない場合)。

## TiDB Cloud Vercel 統合を介して接続する {#connect-via-the-tidb-cloud-vercel-integration}

TiDB Cloud Vercel インテグレーション経由で接続するには、 [Vercel の統合マーケットプレイス](https://vercel.com/integrations)から[TiDB Cloud統合](https://vercel.com/integrations/tidb-cloud)ページに移動します。この方法を使用すると、接続するクラスターを選択でき、 TiDB Cloudは Vercel プロジェクトに必要なすべての環境変数を自動的に生成します。

詳細な手順は次のとおりです。

1.  [TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)ページの右上にある [**統合の追加] を**クリックします。 [ <strong>TiDB Cloudの追加</strong>] ダイアログが表示されます。
2.  ドロップダウン リストで統合の範囲を選択し、[**続行**] をクリックします。
3.  統合を追加する**Vercel**プロジェクトを選択し、[続行] をクリックします。
4.  統合に必要な権限を確認し、 **ADD INTEGRATION**をクリックします。次に、 TiDB Cloudコンソールの統合ページに移動します。
5.  統合ページで、対象の Vercel プロジェクトを選択し、クラスター情報を提供した後、対象のTiDB Cloudクラスターを選択します。各TiDB Cloudクラスターは[組織とプロジェクト](/tidb-cloud/manage-user-access.md#view-the-organization-and-project)に属します。
6.  [**統合を追加して Vercel に戻る] を**クリックします。
7.  Vercel ダッシュボードに戻り、Vercel プロジェクトに移動し、[**設定]** &gt; [<strong>環境変数</strong>] をクリックして、環境変数が自動的に追加されていることを確認します。

    変数が追加されていれば、接続は完了です。

統合セットアップを完了し、 TiDB Cloudクラスターを Vercel プロジェクトに正常に接続すると、接続に必要な情報がプロジェクトの環境変数に自動的に設定されます。以下は、いくつかの一般的な変数です。

```
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

Dedicated Tierクラスターの場合、ルート CA はこの変数に設定されます。

```
TIDB_SSL_CA
```

## 環境変数を手動で設定して接続する {#connect-via-manually-setting-environment-variables}

この方法を使用するには、 [**セキュリティ設定**](/tidb-cloud/configure-security-settings.md)ダイアログで [**どこからでもアクセスを許可**する] トラフィック フィルタを設定していることを確認し、パスワードを保存します。

1.  [標準接続を介してTiDB Cloudクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection)の手順に従って、TiDB クラスターの接続情報を取得します。
2.  Vercel ダッシュボード &gt; Vercel プロジェクト &gt;**設定**&gt;<strong>環境変数</strong>に移動し、TiDB クラスターの接続情報に従って[各環境変数値を宣言する](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable)に進みます。

以下は、 TiDB Cloud Dedicated Tierクラスターの接続変数の例です。

```
var connection = mysql.createConnection({
  host: '<your_host>',
  port: 4000,
  user: 'root',
  password: '<your_password>',
  database: 'test',
  ssl: {
    ca: fs.readFileSync('ca.pem'),
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true
  }
});
```

Vercel では、次のように変数を宣言できます。プロジェクトの必要に応じて名前をカスタマイズできます。

-   **名前**= <strong>TIDB_HOST</strong>値 = `<your_host>`
-   **名前**= <strong>TIDB_PORT</strong>値 = 4000
-   **名前**= <strong>TIDB_USER</strong>値 = ルート
-   **名前**= <strong>TIDB_PASSWORD</strong>値 = `<your_password>`
-   **名前**= <strong>TIDB_SSL_CA</strong>値 = `<content_of_ca.pem>`

## 接続の構成 {#configure-connections}

[TiDB Cloud Vercel 統合](https://vercel.com/integrations/tidb-cloud)をインストールしている場合は、統合内で接続を追加または削除できます。

1.  Vercel ダッシュボードで、[**統合**] をクリックします。
2.  TiDB Cloudエントリで [**管理**] をクリックします。
3.  [**構成]**をクリックします。
4.  [**プロジェクトの追加]**または [<strong>削除]</strong>をクリックして、接続を追加または削除します。

接続を削除すると、統合ワークフローによって設定された環境変数も Vercel プロジェクトから削除されます。トラフィック フィルターとTiDB Cloudクラスターのデータは影響を受けません。
