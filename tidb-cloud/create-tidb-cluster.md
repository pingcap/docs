---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# TiDBクラスタを作成する {#create-a-tidb-cluster}

このチュートリアルでは、サインアップして TiDB クラスターを作成する方法について説明します。

## ステップ 1. TiDB Cloudアカウントを作成する {#step-1-create-a-tidb-cloud-account}

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップします。

    -   Google ユーザーの場合は、Google でサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Google にサインアップ**] をクリックします。メールアドレスとパスワードは Google によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   GitHub ユーザーの場合は、GitHub にサインアップすることもできます。これを行うには、 [サインアップ](https://tidbcloud.com/signup)ページで [ **Sign up with GitHub** ] をクリックします。メールアドレスとパスワードは GitHub によって管理され、 TiDB Cloudコンソールを使用して変更することはできません。
    -   AWS Marketplace ユーザーは、AWS Marketplace からサインアップすることもできます。これを行うには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントをセットアップします。
    -   Google Cloud Marketplace のユーザーは、Google Cloud Marketplace からサインアップすることもできます。これを行うには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントをセットアップします。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

## ステップ 2. クラスター層を選択する {#step-2-select-a-cluster-tier}

TiDB Cloudは、次の 2 つのクラスター層オプションを提供します。 TiDB クラスターを作成する前に、どのオプションがニーズに適しているかを検討してください。

-   Serverless Tier(ベータ)

    TiDB Cloud Serverless Tierは、TiDB のフル マネージド サービスです。まだベータ段階であり、本番環境では使用できません。ただし、Serverless Tierクラスターは、プロトタイプ アプリケーション、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

-   Dedicated Tier

    TiDB Cloud Dedicated Tierは、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた、本番使用専用です。

2 つのオプションの詳細については、 [Cluster Tierを選択する](/tidb-cloud/select-cluster-tier.md)を参照してください。

## ステップ 3. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成します {#step-3-use-your-default-project-or-create-a-new-project}

あなたが組織の所有者である場合、 TiDB Cloudにログインすると、デフォルトのプロジェクトが作成されます。プロジェクトの詳細については、 [組織とプロジェクト](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

-   無料試用版ユーザーの場合、必要に応じてデフォルト プロジェクトの名前を変更できます。
-   Dedicated Tierユーザーの場合、デフォルト プロジェクトの名前を変更するか、必要に応じて新しいプロジェクトを作成できます。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅にある**組織**。</mdsvgicon>

2.  [**組織の設定]**をクリックします。

    デフォルトでは、[**プロジェクト**] タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルト プロジェクトの名前を変更するには、[**アクション**] 列の [名前の<strong>変更</strong>] をクリックします。
    -   プロジェクトを作成するには、[**新しいプロジェクトの作成**] をクリックし、プロジェクトの名前を入力して、[<strong>確認</strong>] をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

あなたがプロジェクト メンバーである場合、組織の所有者があなたを招待した特定のプロジェクトにのみアクセスでき、新しいプロジェクトを作成することはできません。自分が所属しているプロジェクトを確認するには、次の手順を実行します。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅にある**組織**。</mdsvgicon>

2.  [**組織の設定]**をクリックします。

    デフォルトでは、[**プロジェクト**] タブが表示されます。

3.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ 4. TiDB クラスターを作成する {#step-4-create-a-tidb-cluster}

<SimpleTab>
<div label="Serverless Tier">

Serverless Tierクラスターを作成するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  [**クラスタの作成]**をクリックします。

3.  [ **Create クラスタ** ] ページで [ <strong>Serverless Tier]</strong>を選択し、必要に応じてデフォルトのクラスター名を更新します。

4.  Serverless Tierのクラウド プロバイダーは AWS であることに注意して、クラスターを作成するリージョンを選択します。

5.  [**作成]**をクリックします。

    クラスター作成プロセスが開始され、約 30 秒でTiDB Cloudクラスターが作成されます。

6.  クラスターが作成されたら、 [標準接続で接続する](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)の手順に従ってクラスターのパスワードを作成します。

    > **ノート：**
    >
    > パスワードを設定しないと、クラスターに接続できません。

</div>

<div label="Dedicated Tier">

Dedicated Tierクラスターを作成するには、次の手順を実行します。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、[**クラスター]**ページの左側のナビゲーション ペインでターゲット プロジェクトに切り替えることができます。

2.  [**クラスタの作成]**をクリックします。

3.  [**クラスタの作成**] ページで [<strong>Dedicated Tier</strong>] を選択し、必要に応じて既定のクラスター名とポート番号を更新し、クラウド プロバイダーとリージョンを選択して、 [<strong>次へ</strong>] をクリックします。

    > **ノート：**
    >
    > -   [AWS マーケットプレイス](https://aws.amazon.com/marketplace)からTiDB Cloudにサインアップした場合、クラウド プロバイダーは AWS であり、 TiDB Cloudで変更することはできません。
    > -   [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)からTiDB Cloudにサインアップした場合、クラウド プロバイダーは GCP であり、 TiDB Cloudで変更することはできません。

4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに対して CIDR が構成されていない場合は、プロジェクトの CIDR を設定し、[**次へ**] をクリックする必要があります。 [<strong>プロジェクト CIDR]</strong>フィールドが表示されない場合は、このプロジェクトに対して CIDR が既に構成されていることを意味します。

    > **ノート：**
    >
    > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR と競合しないようにしてください。プロジェクトの CIDR は、一度設定すると変更できません。

5.  TiDB、TiKV、およびTiFlash (オプション) にそれぞれ[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を構成し、[**次へ**] をクリックします。

6.  ページのクラスター情報と、左下隅の課金情報を確認します。

7.  支払い方法を追加していない場合は、右下隅にある [**クレジット カードを追加**] をクリックします。

    > **ノート：**
    >
    > [AWS マーケットプレイス](https://aws.amazon.com/marketplace)または[Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)でTiDB Cloudにサインアップした場合は、AWS アカウントまたは Google Cloud アカウントから直接支払うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

8.  [**作成]**をクリックします。

    TiDB Cloudクラスターは、約 20 ～ 30 分で作成されます。

9.  ターゲット クラスタの行で、[ **...** ] をクリックして [ <strong>Security Settings]</strong>を選択します。

10. root パスワードと許可された IP アドレスを設定してクラスターに接続し、[**適用**] をクリックします。

</div>
</SimpleTab>
