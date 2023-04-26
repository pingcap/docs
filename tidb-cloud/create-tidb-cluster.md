---
title: Create a TiDB Cluster
summary: Learn how to create your TiDB cluster.
---

# TiDBクラスタを作成する {#create-a-tidb-cluster}

このチュートリアルでは、サインアップして TiDB クラスターを作成する方法について説明します。

## ステップ 1. TiDB Cloudアカウントを作成する {#step-1-create-a-tidb-cloud-account}

1.  TiDB Cloudアカウントを持っていない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントにサインアップします。

    -   TiDB Cloudを使用してパスワードを管理できるように電子メールとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
    -   AWS Marketplace ユーザーは、AWS Marketplace からサインアップすることもできます。これを行うには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントをセットアップします。
    -   Google Cloud Marketplace のユーザーは、Google Cloud Marketplace からサインアップすることもできます。これを行うには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudにサブスクライブしてから、画面の指示に従ってTiDB Cloudアカウントをセットアップします。

2.  [ログイン](https://tidbcloud.com/)をTiDB Cloudアカウントに追加します。

## ステップ 2. クラスター層を選択する {#step-2-select-a-cluster-tier}

TiDB Cloud は、次の 2 つのクラスター層オプションを提供します。 TiDB クラスターを作成する前に、どのオプションがニーズに適しているかを検討してください。

-   Serverless Tier(ベータ)

    TiDB Cloud Serverless Tier は、 TiDB のフル マネージド サービスです。まだベータ段階であり、本番では使用できません。ただし、Serverless Tierクラスターは、プロトタイプ アプリケーション、ハッカソン、アカデミック コースなどの非運用ワークロードに使用したり、データセットに一時的なデータ サービスを提供したりするために使用できます。

-   Dedicated Tier

    TiDB Cloud Dedicated Tier は、クロスゾーンの高可用性、水平スケーリング、および[HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing)利点を備えた、本番使用専用です。

2 つのオプションの詳細については、 [Cluster Tierを選択する](/tidb-cloud/select-cluster-tier.md)を参照してください。

## ステップ 3. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成します {#step-3-use-your-default-project-or-create-a-new-project}

あなたが組織の所有者である場合、 TiDB Cloudにログインすると、デフォルトのプロジェクトが作成されます。プロジェクトの詳細については、 [組織とプロジェクト](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

-   無料試用版ユーザーの場合、必要に応じてデフォルト プロジェクトの名前を変更できます。
-   Dedicated Tierユーザーの場合、デフォルト プロジェクトの名前を変更するか、必要に応じて新しいプロジェクトを作成できます。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅に**ある組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **[プロジェクト]**タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルト プロジェクトの名前を変更するには、 **[アクション]**列の<strong>[名前の変更]</strong>をクリックします。
    -   プロジェクトを作成するには、 **[新しいプロジェクトの作成]**をクリックし、プロジェクトの名前を入力して、 <strong>[確認]</strong>をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

あなたがプロジェクト メンバーである場合、組織の所有者があなたを招待した特定のプロジェクトにのみアクセスでき、新しいプロジェクトを作成することはできません。自分が所属しているプロジェクトを確認するには、次の手順を実行します。

1.  クリック<mdsvgicon name="icon-top-organization">TiDB Cloudコンソールの右上隅に**ある組織**。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **[プロジェクト]**タブが表示されます。

3.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ 4. TiDB クラスターを作成する {#step-4-create-a-tidb-cluster}

<SimpleTab>
<div label="Serverless Tier">

Serverless Tierクラスターを作成するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **[クラスタの作成]**をクリックします。

3.  **[クラスタの作成]**ページでは、<strong>サーバーレスが</strong>デフォルトで選択されています。

4.  Serverless Tierのクラウドプロバイダーは AWS です。クラスターをホストする AWS リージョンを選択できます。

5.  (オプション) [無料割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)よりも多くのstorageとコンピューティング リソースを使用する予定がある場合は、使用制限を変更します。支払い方法を追加していない場合は、制限を編集した後にクレジット カードを追加する必要があります。

    > **ノート：**
    >
    > TiDB Cloudの組織ごとに、デフォルトで最大 5 つのServerless Tierクラスターを作成できます。さらにServerless Tierクラスターを作成するには、クレジット カードを追加し、使用量を[使用制限](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

6.  必要に応じてデフォルトのクラスター名を更新し、 **[作成]**をクリックします。

    クラスター作成プロセスが開始され、約 30 秒でTiDB Cloudクラスターが作成されます。

7.  クラスターが作成されたら、 [標準接続で接続する](/tidb-cloud/connect-via-standard-connection.md#serverless-tier)の手順に従ってクラスターのパスワードを作成します。

    > **ノート：**
    >
    > パスワードを設定しないと、クラスターに接続できません。

</div>

<div label="Dedicated Tier">

Dedicated Tierクラスターを作成するには、次の手順を実行します。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、プロジェクト リストを表示し、左上隅の ☰ ホバー メニューから別のプロジェクトに切り替えることができます。

2.  **[クラスタの作成]**をクリックします。

3.  **[クラスタの作成]**ページで<strong>[専用]</strong>を選択し、次のようにクラスター情報を構成します。

    1.  クラウド プロバイダーとリージョンを選択します。

        > **ノート：**
        >
        > -   [AWS マーケットプレイス](https://aws.amazon.com/marketplace)からTiDB Cloudにサインアップした場合、クラウド プロバイダーは AWS であり、 TiDB Cloudで変更することはできません。
        > -   [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)からTiDB Cloudにサインアップした場合、クラウド プロバイダーは GCP であり、 TiDB Cloudで変更することはできません。

    2.  TiDB、TiKV、およびTiFlash (オプション) に対してそれぞれ[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を構成します。

    3.  必要に応じて、デフォルトのクラスター名とポート番号を更新します。

    4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに対して CIDR が構成されていない場合は、プロジェクトの CIDR を設定する必要があります。 **[プロジェクト CIDR]**フィールドが表示されない場合は、このプロジェクトに対して CIDR が既に構成されていることを意味します。

        > **ノート：**
        >
        > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR と競合しないようにしてください。プロジェクトの CIDR は、一度設定すると変更できません。

4.  右側のクラスターと課金情報を確認します。

5.  支払い方法を追加していない場合は、右下隅にある**[クレジット カードを追加]**をクリックします。

    > **ノート：**
    >
    > [AWS マーケットプレイス](https://aws.amazon.com/marketplace)または[Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)でTiDB Cloudにサインアップした場合は、AWS アカウントまたは Google Cloud アカウントから直接支払うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

6.  **[作成]**をクリックします。

    TiDB Cloudクラスターは、約 20 ～ 30 分で作成されます。

7.  クラスターの概要ページの右上隅にある**[...]**をクリックし、 <strong>[Security Settings]</strong>を選択します。

8.  root パスワードと許可された IP アドレスを設定してクラスターに接続し、 **[適用]**をクリックします。

</div>
</SimpleTab>
