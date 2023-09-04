---
title: Create a TiDB Dedicated Cluster
summary: Learn how to create your TiDB Dedicated cluster.
---

# TiDB 専用クラスタの作成 {#create-a-tidb-dedicated-cluster}

このチュートリアルでは、TiDB 専用クラスターのサインアップと作成について説明します。

> **ヒント：**
>
> TiDB サーバーレス クラスターの作成方法については、 [TiDB サーバーレスクラスタの作成](/tidb-cloud/create-tidb-cluster-serverless.md)を参照してください。

## あなたが始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)をクリックしてアカウントにサインアップしてください。

-   TiDB Cloud を使用してパスワードを管理できるように電子メールとパスワードでサインアップすることも、Google、GitHub、または Microsoft アカウントでサインアップすることもできます。
-   AWS Marketplace ユーザーの場合は、AWS Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [AWSマーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。
-   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace を通じてサインアップすることもできます。これを行うには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudに登録し、画面上の指示に従ってTiDB Cloudアカウントを設定します。

## (オプション) ステップ 1. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成します {#optional-step-1-use-your-default-project-or-create-a-new-project}

[TiDB Cloudコンソール](https://tidbcloud.com/)にログインすると、デフォルトの[プロジェクト](/tidb-cloud/tidb-cloud-glossary.md#project)になります。組織内にプロジェクトが 1 つだけある場合、クラスターはそのプロジェクト内に作成されます。プロジェクトの詳細については、 [組織とプロジェクト](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

組織の所有者の場合は、次のように、必要に応じてデフォルトのプロジェクトの名前を変更するか、クラスターの新しいプロジェクトを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 をクリックします。<mdsvgicon name="icon-top-organization">左下隅にあります。</mdsvgicon>

2.  **[組織の設定]**をクリックします。

    デフォルトでは、 **「プロジェクト」**タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルトのプロジェクトの名前を変更するには、 **「アクション」**列の**「名前の変更」**をクリックします。
    -   プロジェクトを作成するには、 **[新しいプロジェクトの作成]**をクリックし、プロジェクトの名前を入力して、 **[確認]**をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ 2. TiDB 専用クラスターを作成する {#step-2-create-a-tidb-dedicated-cluster}

`Organization Owner`または`Project Owner`ロールに属している場合は、次のように TiDB 専用クラスターを作成できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅の をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  **「クラスタの作成」**をクリックします。

3.  **[クラスタの作成]**ページで**[専用]**を選択し、次のようにクラスター情報を構成します。

    1.  クラウドプロバイダーとリージョンを選択します。

        > **注記：**
        >
        > -   [AWSマーケットプレイス](https://aws.amazon.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは AWS であり、 TiDB Cloudで変更することはできません。
        > -   [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウド プロバイダーは Google Cloud となり、 TiDB Cloudで変更することはできません。

    2.  TiDB、TiKV、 TiFlash (オプション) にそれぞれ[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を設定します。

    3.  必要に応じて、デフォルトのクラスター名とポート番号を更新します。

    4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに対して CIDR が構成されていない場合は、プロジェクト CIDR を設定する必要があります。 **「プロジェクト CIDR」**フィールドが表示されない場合は、このプロジェクトに対して CIDR がすでに構成されていることを意味します。

        > **注記：**
        >
        > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR との競合を避けてください。プロジェクトの CIDR は、一度設定すると変更できません。

4.  右側でクラスターと課金情報を確認します。

5.  支払い方法を追加していない場合は、右下隅にある**「クレジット カードを追加」**をクリックします。

    > **注記：**
    >
    > [AWSマーケットプレイス](https://aws.amazon.com/marketplace)または[Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)でTiDB Cloudにサインアップした場合は、AWS アカウントまたは Google Cloud アカウントを通じて直接支払うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

6.  **「作成」**をクリックします。

    TiDB Cloudクラスターは約 20 ～ 30 分で作成されます。

## ステップ 3. 安全な設定を構成する {#step-3-configure-secure-settings}

クラスターの作成後、次の手順を実行してセキュリティ設定を構成します。

1.  クラスターの概要ページの右上隅で**[...]**をクリックし、 **[Security設定]**を選択します。

2.  root パスワードとクラスターへの接続を許可する IP アドレスを設定し、 **「適用」**をクリックします。

## 次は何ですか {#what-s-next}

クラスターがTiDB Cloud上に作成されたら、 [TiDB 専用クラスタに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)で提供される方法を介してクラスターに接続できます。
