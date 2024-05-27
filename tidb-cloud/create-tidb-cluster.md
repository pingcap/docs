---
title: Create a TiDB Dedicated Cluster
summary: TiDB 専用クラスターを作成する方法を学習します。
---

# TiDB専用クラスタを作成する {#create-a-tidb-dedicated-cluster}

このチュートリアルでは、TiDB 専用クラスターのサインアップと作成について説明します。

> **ヒント：**
>
> TiDB Serverless クラスターを作成する方法については、 [TiDB サーバーレスクラスタを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)参照してください。

## あなたが始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントを登録してください。

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplace ユーザーの場合は、AWS Marketplace からサインアップすることもできます。そのためには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。
-   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。

## （オプション）ステップ1. デフォルトのプロジェクトを使用するか、新しいプロジェクトを作成する {#optional-step-1-use-your-default-project-or-create-a-new-project}

[TiDB Cloudコンソール](https://tidbcloud.com/)にログインすると、デフォルトの[プロジェクト](/tidb-cloud/tidb-cloud-glossary.md#project)が提供されます。組織内にプロジェクトが 1 つしかない場合は、そのプロジェクト内にクラスターが作成されます。プロジェクトの詳細については、 [組織とプロジェクト](/tidb-cloud/manage-user-access.md#organizations-and-projects)を参照してください。

組織の所有者の場合は、次のように、デフォルト プロジェクトの名前を変更したり、必要に応じてクラスターの新しいプロジェクトを作成したりできます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、<mdsvgicon name="icon-top-organization">左下隅にあります。</mdsvgicon>

2.  **組織設定を**クリックします。

    デフォルトでは**「プロジェクト」**タブが表示されます。

3.  次のいずれかを実行します。

    -   デフォルトのプロジェクトの名前を変更するには、 **[アクション]**列の**[名前の変更] を**クリックします。
    -   プロジェクトを作成するには、 **「新しいプロジェクトの作成」を**クリックし、プロジェクトの名前を入力して、 **「確認」**をクリックします。

4.  クラスター ページに戻るには、ウィンドウの左上隅にあるTiDB Cloudロゴをクリックします。

## ステップ2. TiDB専用クラスターを作成する {#step-2-create-a-tidb-dedicated-cluster}

ロール`Organization Owner`または`Project Owner`の場合は、次のように TiDB 専用クラスターを作成できます。

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

    > **ヒント：**
    >
    > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

2.  **クラスタの作成を**クリックします。

3.  **[クラスタの作成]**ページで**[専用]**を選択し、クラスター情報を次のように構成します。

    1.  クラウド プロバイダーとリージョンを選択します。

        > **注記：**
        >
        > -   [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは AWS となり、 TiDB Cloudで変更することはできません。
        > -   [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウド プロバイダーは Google Cloud となり、 TiDB Cloudで変更することはできません。

    2.  それぞれ TiDB、TiKV、 TiFlash (オプション) の[クラスターサイズ](/tidb-cloud/size-your-cluster.md)を設定します。

    3.  必要に応じて、デフォルトのクラスター名とポート番号を更新します。

    4.  これが現在のプロジェクトの最初のクラスターであり、このプロジェクトに CIDR が設定されていない場合は、プロジェクト CIDR を設定する必要があります。**プロジェクト CIDR**フィールドが表示されない場合は、このプロジェクトに CIDR がすでに設定されていることを意味します。

        > **注記：**
        >
        > プロジェクト CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR との競合を避けてください。プロジェクト CIDR は、設定後に変更することはできません。

4.  右側でクラスターと課金情報を確認します。

5.  支払い方法の追加をまだ行っていない場合は、右下にある**「クレジットカードを追加」を**クリックします。

    > **注記：**
    >
    > [AWS マーケットプレイス](https://aws.amazon.com/marketplace)または[Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を通じてTiDB Cloud にサインアップした場合、AWS アカウントまたは Google Cloud アカウントを通じて直接支払うことはできますが、 TiDB Cloudコンソールで支払い方法の追加や請求書のダウンロードを行うことはできません。

6.  **[作成]を**クリックします。

    TiDB Cloudクラスターは約 20 ～ 30 分で作成されます。

## ステップ3. 安全な設定を構成する {#step-3-configure-secure-settings}

クラスターが作成されたら、次の手順に従ってセキュリティ設定を構成します。

1.  クラスターの概要ページの右上隅で、 **[...]**をクリックし、 **[Security設定]**を選択します。

2.  クラスターに接続するためのルート パスワードと許可された IP アドレスを設定し、 **[適用] を**クリックします。

## 次は何ですか {#what-s-next}

TiDB Cloud上にクラスターを作成したら、 [TiDB専用クラスタに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)で説明した方法でクラスターに接続できます。
