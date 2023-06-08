---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# TiDBクラスタを作成する {#create-a-tidb-cluster}

このチュートリアルでは、TiDB クラスターのサインアップと作成について説明します。

## ステップ 1. TiDB Cloudアカウントを作成する {#step-1-create-a-tidb-cloud-account}

1.  TiDB Cloudアカウントをお持ちでない場合は、 [<a href="https://tidbcloud.com/signup">ここ</a>](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

    -   TiDB Cloud を使用してパスワードを管理できるように電子メールとパスワードでサインアップすることも、Google、GitHub、または Microsoft アカウントでサインアップすることもできます。
    -   AWS Marketplace ユーザーの場合は、AWS Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。
    -   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。

2.  TiDB Cloudアカウントに[<a href="https://tidbcloud.com/">ログイン</a>](https://tidbcloud.com/) 。

## ステップ 2. クラスター オプションを選択する {#step-2-select-a-cluster-option}

TiDB Cloud、次の 2 つのオプションが提供されます。 TiDB クラスターを作成する前に、どのオプションがニーズに適しているかを検討してください。

-   TiDB Serverless (ベータ版)

    TiDB Serverless は、TiDB のフルマネージド サービスです。これはまだベータ段階にあるため、本番では使用できません。ただし、TiDB Serverless クラスタは、プロトタイプ アプリケーション、ハッカソン、学術コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

-   TiDB Dedicated

    TiDB D dedicated は、クロスゾーンの高可用性、水平スケーリング、および[<a href="https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing">HTAP</a>](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)の利点を備えた本番稼働専用です。

2 つのオプションの詳細については、 [<a href="/tidb-cloud/select-cluster-tier.md">クラスタオプションを選択してください</a>](/tidb-cloud/select-cluster-tier.md)を参照してください。

## ステップ 3. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成します {#step-3-use-your-default-project-or-create-a-new-project}

組織の所有者の場合、 TiDB Cloudにログインすると、デフォルトのプロジェクトが作成されます。プロジェクトの詳細については、 [<a href="/tidb-cloud/manage-user-access.md#organizations-and-projects">組織とプロジェクト</a>](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

-   無料試用版ユーザーの場合は、必要に応じてデフォルトのプロジェクトの名前を変更できます。
-   TiDB D dedicated ユーザーの場合、必要に応じて、デフォルトのプロジェクトの名前を変更するか、新しいプロジェクトを作成できます。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅に**ある組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **「プロジェクト」**タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルトのプロジェクトの名前を変更するには、 **「アクション」**列の**「名前の変更」**をクリックします。
    -   プロジェクトを作成するには、 **[新しいプロジェクトの作成]**をクリックし、プロジェクトの名前を入力して、 **[確認]**をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

プロジェクト メンバーの場合は、組織の所有者が招待した特定のプロジェクトにのみアクセスでき、新しいプロジェクトを作成することはできません。自分がどのプロジェクトに属しているかを確認するには、次の手順を実行します。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅にある**組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **「プロジェクト」**タブが表示されます。

3.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ 4. TiDB クラスターを作成する {#step-4-create-a-tidb-cluster}

<SimpleTab>
<div label="TiDB Serverless">

TiDB Serverless クラスタを作成するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **「クラスタの作成」**をクリックします。

3.  **「クラスタの作成」**ページでは、デフォルトで**サーバーレス**が選択されています。

4.  TiDB Serverless のクラウドプロバイダーは AWS です。クラスターをホストする AWS リージョンを選択できます。

5.  (オプション) [<a href="/tidb-cloud/select-cluster-tier.md#usage-quota">無料割り当て</a>](/tidb-cloud/select-cluster-tier.md#usage-quota)よりも多くのstorageとコンピューティング リソースを使用する予定がある場合は、使用量制限を変更します。支払い方法を追加していない場合は、限度額を編集した後にクレジット カードを追加する必要があります。

    > **ノート：**
    >
    > TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB Serverless クラスタを作成できます。さらに TiDB Serverless クラスタを作成するには、クレジット カードを追加し、使用量を[<a href="/tidb-cloud/tidb-cloud-glossary.md#spend-limit">支出制限</a>](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

6.  必要に応じてデフォルトのクラスター名を更新し、 **「作成」**をクリックします。

    クラスター作成プロセスが開始され、 TiDB Cloudクラスターが約 30 秒で作成されます。

7.  クラスターが作成されたら、 [<a href="/tidb-cloud/connect-via-standard-connection.md#tidb-serverless">標準接続で接続する</a>](/tidb-cloud/connect-via-standard-connection.md#tidb-serverless)の手順に従ってクラスターのパスワードを作成します。

    > **ノート：**
    >
    > パスワードを設定しないと、クラスターに接続できません。

</div>

<div label="TiDB Dedicated">

TiDB Dedicatedクラスターを作成するには、次の手順を実行します。

1.  プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅にある ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  **「クラスタの作成」**をクリックします。

3.  **[クラスタの作成]**ページで**[専用]**を選択し、次のようにクラスター情報を構成します。

    1.  クラウドプロバイダーとリージョンを選択します。

        > **ノート：**
        >
        > -   [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは AWS であり、 TiDB Cloudで変更することはできません。
        > -   [<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウド プロバイダーは GCP であり、 TiDB Cloudで変更することはできません。

    2.  TiDB、TiKV、 TiFlash (オプション) にそれぞれ[<a href="/tidb-cloud/size-your-cluster.md">クラスターサイズ</a>](/tidb-cloud/size-your-cluster.md)を設定します。

    3.  必要に応じて、デフォルトのクラスター名とポート番号を更新します。

    4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに対して CIDR が構成されていない場合は、プロジェクト CIDR を設定する必要があります。 **「プロジェクト CIDR」**フィールドが表示されない場合は、このプロジェクトに対して CIDR がすでに構成されていることを意味します。

        > **ノート：**
        >
        > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR との競合を避けてください。プロジェクトの CIDR は、一度設定すると変更できません。

4.  右側でクラスターと課金情報を確認します。

5.  支払い方法を追加していない場合は、右下隅にある**「クレジット カードを追加」を**クリックします。

    > **ノート：**
    >
    > [<a href="https://aws.amazon.com/marketplace">AWSマーケットプレイス</a>](https://aws.amazon.com/marketplace)または[<a href="https://console.cloud.google.com/marketplace">Google Cloud マーケットプレイス</a>](https://console.cloud.google.com/marketplace)でTiDB Cloudにサインアップした場合は、AWS アカウントまたは Google Cloud アカウントを通じて直接支払うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

6.  **「作成」**をクリックします。

    TiDB Cloudクラスターは約 20 ～ 30 分で作成されます。

7.  クラスターの概要ページの右上隅で**[...]**をクリックし、 **[Security設定]**を選択します。

8.  root パスワードとクラスターへの接続を許可する IP アドレスを設定し、 **「適用」**をクリックします。

</div>
</SimpleTab>
