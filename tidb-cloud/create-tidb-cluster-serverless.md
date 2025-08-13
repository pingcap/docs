---
title: Create a TiDB Cloud Starter or Essential Cluster
summary: TiDB Cloud Starter またはTiDB Cloud Essential クラスターを作成する方法を学習します。
---

# TiDB Cloud StarterまたはEssential クラスタを作成する {#create-a-tidb-cloud-starter-or-essential-cluster}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud Starter またはTiDB Cloud Essential クラスターを作成する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターを作成する方法については、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントを登録してください。

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplaceユーザーの方は、AWS Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplaceユーザーの方は、Azure Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Azureマーケットプレイス](https://azuremarketplace.microsoft.com)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace ユーザーの方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Alibaba Cloud Marketplaceをご利用の方は、Alibaba Cloud Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。

## 手順 {#steps}

ロール`Organization Owner`または`Project Owner`の場合は、次のようにしてTiDB Cloud Starter またはTiDB Cloud Essential クラスターを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

2.  **[クラスタの作成]を**クリックします。

3.  クラスター プランとクラウド プロバイダーを選択します。

    -   AWS の場合は、**スターター**クラスターから始めることができます。
    -   Alibaba Cloud では、 **Starter**クラスターから始めて、後でニーズの拡大に応じて**Essential**クラスターにアップグレードできます。

    詳細については[クラスター計画](/tidb-cloud/select-cluster-tier.md)参照してください。

4.  クラスターをホストするリージョンを選択します。

5.  必要に応じてデフォルトのクラスター名を更新します。

6.  クラスターの容量を更新します。

    -   **スターター**プラン:

        -   クラスターの使用制限を更新できます。使用制限が0に設定されている場合、クラスターは無料のままです。使用制限が0より大きい場合は、クラスターを作成する前にクレジットカードを追加する必要があります。

        -   デフォルトでは、各組織は最大 5 つの[無料のスタータークラスター](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)作成できます。追加のスターター クラスターを作成するには、クレジットカードを追加し、支出限度額を指定する必要があります。

    -   **必須**プラン:

        -   クラスターのリクエスト容量ユニット (RCU) の最小数と最大数の両方を指定する必要があります。

        -   RCU は、ワークロード用にプロビジョニングされたコンピューティングリソースを表します。TiDB TiDB Cloud は、需要に応じてこの範囲内でクラスターを自動的にスケーリングします。

7.  **[作成]を**クリックします。

    クラスター作成プロセスが開始され、約 30 秒以内にTiDB Cloudクラスターが作成されます。

## 次は何？ {#what-s-next}

クラスターが作成されたら、 [パブリックエンドポイント経由でTiDB Cloudに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)の手順に従ってクラスターのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、クラスターに接続できません。
