---
title: Create a TiDB Cloud Starter or Essential Instance
summary: TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの作成方法を学びましょう。
---

# TiDB Cloud StarterまたはEssentialインスタンスを作成します。 {#create-a-tidb-cloud-starter-or-essential-instance}

このドキュメントでは、TiDB [TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicatedクラスターを作成する方法については、 [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、[ここ](https://tidbcloud.com/signup)をクリックしてアカウントを作成してください。

<CustomContent language="en,zh">

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードで登録するか、Google、GitHub、またはMicrosoftアカウントで登録することができます。
-   AWS Marketplace をご利用の方は、AWS Marketplace からサインアップすることもできます。サインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplace をご利用の方は、Azure Marketplace からサインアップすることもできます。サインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace をご利用の方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Alibaba Cloud Marketplace ユーザーの場合は、Alibaba Cloud Marketplace を通じてサインアップすることもできます。これを行うには、[アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)で`TiDB Cloud`を検索し、 TiDB Cloudにサブスクライブし、画面上の指示に従ってTiDB Cloudアカウントを設定します。

</CustomContent>

<CustomContent language="ja">

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードで登録するか、Google、GitHub、またはMicrosoftアカウントで登録することができます。
-   AWS Marketplace をご利用の方は、AWS Marketplace からサインアップすることもできます。サインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplace をご利用の方は、Azure Marketplace からサインアップすることもできます。サインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace をご利用の方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。

</CustomContent>

## 手順 {#steps}

`Organization Owner`または`Project Owner`の役割に属している場合は、次のようにしてTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

2.  **「リソースの作成」を**クリックします。

3.  プランを選択してください。

    **Starter**インスタンスから開始し、後でニーズの増大に応じて**Essential**インスタンスにアップグレードできます。詳細については、[プランを選択してください](/tidb-cloud/select-cluster-tier.md)ご覧ください。

4.  インスタンスの名前を入力し、次にインスタンスをホストするクラウドプロバイダーとリージョンを選択してください。

5.  （オプション）このインスタンスを管理対象プロジェクトにグループ化するには、 **[インスタンスをプロジェクトにグループ化]を**クリックし、インスタンスのターゲットプロジェクトを選択します。組織内にプロジェクトがない場合は、 **[プロジェクトの作成]を**クリックして作成できます。

6.  インスタンスの容量を更新します。

    -   **Starter**プラン：

        -   TiDB Cloud Starterインスタンスの利用限度額を更新できます。利用限度額を0に設定すると、インスタンスは無料のままです。利用限度額を0より大きい値に設定する場合は、 TiDB Cloud Starterインスタンスを作成する前にクレジットカードを追加する必要があります。

        -   デフォルトでは、各組織は最大 5 つ [無料のTiDB Cloud Starterインスタンス](/tidb-cloud/select-cluster-tier.md#starter)を作成できます。追加のTiDB Cloud Starterインスタンスを作成するには、クレジット カードを追加し、使用制限を指定する必要があります。

    -   **Essential**プラン：

        -   TiDB Cloud Essentialインスタンスでは、リクエストキャパシティユニット（RCU）の最小数と最大数の両方を指定する必要があります。

        -   RCUは、ワークロード用にプロビジョニングされたコンピューティングリソースを表します。TiDB TiDB Cloudは、需要に基づいて、この範囲内でTiDB Cloud Essentialインスタンスを自動的にスケーリングします。

7.  **「作成」**をクリックします。

    インスタンス作成プロセスが開始され、約30秒でインスタンスが作成されます。

## 次は？ {#what-s-next}

TiDB Cloud StarterまたはEssentialインスタンスが作成されたら、 [パブリックエンドポイント経由でTiDB Cloudに接続します](/tidb-cloud/connect-via-standard-connection-serverless.md)インスタンスのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、 TiDB Cloud StarterまたはEssentialインスタンスに接続できません。
