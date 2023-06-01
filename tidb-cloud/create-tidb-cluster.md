---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# TiDBクラスタを作成する {#create-a-tidb-cluster}

このチュートリアルでは、TiDB クラスターのサインアップと作成について説明します。

## ステップ 1. TiDB Cloudアカウントを作成する {#step-1-create-a-tidb-cloud-account}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [<a href="https://tidbcloud.com/signup">ここ</a>](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

    -   Google ユーザーの場合は、Google にサインアップすることもできます。これを行うには、 [<a href="https://tidbcloud.com/signup">サインアップ</a>](https://tidbcloud.com/signup)ページの**[Google でサインアップ]**をクリックします。あなたの電子メール アドレスとパスワードは Google によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHub ユーザーの場合は、GitHub にサインアップすることもできます。これを行うには、 [<a href="https://tidbcloud.com/signup">サインアップ</a>](https://tidbcloud.com/signup)ページの**「Sign up with GitHub」**をクリックします。あなたの電子メール アドレスとパスワードは GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   AWS Marketplace ユーザーの場合は、AWS Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。
    -   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。

2.  TiDB Cloudアカウントに[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/) 。

## ステップ 2. クラスター層を選択する {#step-2-select-a-cluster-tier}

TiDB Cloud は、次の 2 つのクラスター層オプションを提供します。 TiDB クラスターを作成する前に、どのオプションがニーズに適しているかを検討してください。

-   Serverless Tier(ベータ版)

    TiDB CloudServerless Tierは、TiDB のフルマネージド サービスです。これはまだベータ段階にあるため、本番では使用できません。ただし、Serverless Tierクラスターは、プロトタイプ アプリケーション、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

-   Dedicated Tier

    TiDB CloudDedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[<a href="https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing">HTAP</a>](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた本番稼働専用です。

2 つのオプションの詳細については、 [<a href="/tidb-cloud/select-cluster-tier.md">Cluster Tierを選択してください</a>](/tidb-cloud/select-cluster-tier.md)を参照してください。

## ステップ 3. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成します {#step-3-use-your-default-project-or-create-a-new-project}

組織の所有者の場合、 TiDB Cloudにログインすると、デフォルトのプロジェクトが作成されます。プロジェクトの詳細については、 [<a href="/tidb-cloud/manage-user-access.md#organizations-and-projects">組織とプロジェクト</a>](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

-   無料試用版ユーザーの場合は、必要に応じてデフォルトのプロジェクトの名前を変更できます。
-   Dedicated Tierユーザーの場合は、必要に応じてデフォルトのプロジェクトの名前を変更するか、新しいプロジェクトを作成できます。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅に**ある組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **「プロジェクト」**タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルトのプロジェクトの名前を変更するには、 **「アクション」**列の**「名前の変更」**をクリックします。
    -   プロジェクトを作成するには、 **[新しいプロジェクトの作成]**をクリックし、プロジェクトの名前を入力して、 **[確認]**をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

プロジェクト メンバーの場合は、組織の所有者が招待した特定のプロジェクトにのみアクセスでき、新しいプロジェクトを作成することはできません。自分がどのプロジェクトに属しているかを確認するには、次の手順を実行します。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅に**ある組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **「プロジェクト」**タブが表示されます。

3.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ 4. TiDB クラスターを作成する {#step-4-create-a-tidb-cluster}

<SimpleTab>
<div label="Serverless Tier">

Serverless Tierクラスターを作成するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **「クラスタの作成」**をクリックします。

3.  **[クラスタの作成]**ページで、 **[Serverless Tier]**を選択し、必要に応じてデフォルトのクラスター名を更新します。

4.  Serverless Tierのクラウドプロバイダーが AWS であることに注意し、クラスターを作成するリージョンを選択します。

5.  **「作成」**をクリックします。

    クラスター作成プロセスが開始され、 TiDB Cloudクラスターが約 30 秒で作成されます。

6.  クラスターが作成されたら、 [<a href="/tidb-cloud/connect-via-standard-connection.md#serverless-tier">標準接続で接続する</a>](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)の手順に従ってクラスターのパスワードを作成します。

    > **ノート：**
    >
    > パスワードを設定しないと、クラスターに接続できません。

</div>

<div label="Dedicated Tier">

Dedicated Tierクラスターを作成するには、次の手順を実行します。

1.  プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、 **「クラスター」**ページの左側のナビゲーション・ペインでターゲット・プロジェクトに切り替えることができます。

2.  **「クラスタの作成」**をクリックします。

3.  **[クラスタの作成]**ページで、 **[Dedicated Tier]**を選択し、必要に応じてデフォルトのクラスター名とポート番号を更新し、クラウド プロバイダーとリージョンを選択して、 [**次へ]**をクリックします。

    > **ノート：**
    >
    > -   [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは AWS であり、 TiDB Cloudで変更することはできません。
    > -   [<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウド プロバイダーは GCP であり、 TiDB Cloudで変更することはできません。

4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに CIDR が構成されていない場合は、プロジェクトの CIDR を設定して、 **「次へ」**をクリックする必要があります。 **「プロジェクト CIDR」**フィールドが表示されない場合は、このプロジェクトに対して CIDR がすでに構成されていることを意味します。

    > **ノート：**
    >
    > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR との競合を避けてください。プロジェクトの CIDR は、一度設定すると変更できません。

5.  TiDB、TiKV、 TiFlash (オプション) にそれぞれ[<a href="/tidb-cloud/size-your-cluster.md">クラスターサイズ</a>](/tidb-cloud/size-your-cluster.md)を設定し、 **[次へ]**をクリックします。

6.  ページ上のクラスター情報と左下隅の請求情報を確認します。

7.  支払い方法を追加していない場合は、右下隅にある**「クレジット カードを追加」**をクリックします。

    > **ノート：**
    >
    > [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)または[<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)でTiDB Cloudにサインアップした場合は、AWS アカウントまたは Google Cloud アカウントを通じて直接支払うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

8.  **「作成」**をクリックします。

    TiDB Cloudクラスターは約 20 ～ 30 分で作成されます。

9.  ターゲット クラスターの行で**[...]**をクリックし、 **[Security設定]**を選択します。

10. root パスワードとクラスターへの接続を許可する IP アドレスを設定し、 **「適用」**をクリックします。

</div>
</SimpleTab>
