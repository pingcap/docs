---
title: Create a TiDB Cloud Dedicated Cluster
summary: TiDB Cloud Dedicatedクラスターの作成方法を学びましょう。
---

# TiDB Cloud Dedicatedクラスタを作成する {#create-a-tidb-cloud-dedicated-cluster}

このチュートリアルでは、TiDB Cloud Dedicatedクラスターへのサインアップと作成の手順を説明します。

> **ヒント：**
>
> TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスを作成する方法については、 [TiDB Cloud StarterまたはEssentialインスタンスを作成します。](/tidb-cloud/create-tidb-cluster-serverless.md)を参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、[ここ](https://tidbcloud.com/signup)をクリックしてアカウントを作成してください。

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードで登録するか、Google、GitHub、またはMicrosoftアカウントで登録することができます。
-   AWS Marketplace をご利用の方は、AWS Marketplace からサインアップすることもできます。サインアップするには、 [AWS Marketplace](https://aws.amazon.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplace をご利用の方は、Azure Marketplace からサインアップすることもできます。サインアップするには、 [Azure Marketplace](https://azuremarketplace.microsoft.com)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace をご利用の方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace)で`TiDB Cloud`を検索し、 TiDB Cloudを購読してから、画面の指示に従ってTiDB Cloudアカウントを設定してください。

## ステップ1. TiDB Cloud Dedicatedクラスタを作成する {#step-1-create-a-tidb-cloud-dedicated-cluster}

`Organization Owner`または`Project Owner`の役割を担っている場合は、次のようにしてTiDB Cloud Dedicatedクラスターを作成できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  **「リソースの作成」を**クリックします。

3.  **「リソースの作成」**ページで**「Dedicated」**を選択し、クラスタ情報を次のように構成します。

    1.  TiDB Cloud Dedicatedクラスターのプロジェクトを選択してください。組織内にプロジェクトがない場合は、 **「プロジェクトの作成」を**クリックして作成できます。

    2.  TiDB Cloud Dedicatedクラスターの名前を入力してください。

    3.  クラウドプロバイダーと、クラスターをホストするリージョンを選択してください。

        > **注記：**
        >
        > -   現在、Azure 上でのTiDB Cloud Dedicatedのサポートはパブリックプレビュー段階です。
        > -   [AWS Marketplace](https://aws.amazon.com/marketplace)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは AWS となり、 TiDB Cloudで変更することはできません。
        > -   [Azure Marketplace](https://azuremarketplace.microsoft.com)を通じてTiDB Cloudにサインアップした場合、クラウドプロバイダーは Azure Cloud となり、 TiDB Cloudで変更することはできません。
        > -   TiDB Cloudを[Google Cloud Marketplace](https://console.cloud.google.com/marketplace)経由で登録した場合、クラウドプロバイダーはGoogle Cloudとなり、 TiDB Cloudで変更することはできません。

    4.  TiDB、TiKV、 TiFlashの[クラスターサイズ](/tidb-cloud/size-your-cluster.md)をそれぞれ設定します (オプション)。

    5.  必要に応じて、デフォルトのポート番号を更新してください。

    6.  このリージョンにCIDRが設定されていない場合は、CIDRを設定する必要があります。**プロジェクトCIDR**フィールドが表示されない場合は、このリージョンにCIDRが既に設定されていることを意味します。

        > **注記：**
        >
        > -   TiDB Cloudは、このリージョンで最初のクラスターが作成される際に、このCIDRを持つVPCを作成します。このリージョン内の同じプロジェクトの以降のすべてのクラスターは、このVPCを使用します。
        > -   CIDRを設定する際は、アプリケーションが配置されているVPCのCIDRと競合しないようにしてください。VPCが作成されると、CIDRを変更することはできません。

4.  右側のクラスター情報と請求情報を確認してください。

5.  支払い方法を登録していない場合は、右下隅の**「クレジットカードを追加」**をクリックしてください。

    > **注記：**
    >
    > [AWS Marketplace](https://aws.amazon.com/marketplace) 、 [Azure Marketplace](https://azuremarketplace.microsoft.com) 、または[Google Cloud Marketplace](https://console.cloud.google.com/marketplace)経由でTiDB Cloudに登録した場合、AWSアカウント、Azureアカウント、またはGoogle Cloudアカウントを通じて直接支払いを行うことができますが、 TiDB Cloudコンソールで支払い方法を追加したり、請求書をダウンロードしたりすることはできません。

6.  **「作成」**をクリックします。

    TiDB Cloudクラスタの作成には約20～30分かかります。作成が完了すると、 TiDB Cloudコンソールから通知が届きます。

    > **注記：**
    >
    > クラスターの作成時間は地域によって異なり、30分以上かかる場合があります。処理に予想以上に時間がかかる場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

## ステップ2. ルートパスワードを設定する {#step-2-set-the-root-password}

TiDB Cloud Dedicatedクラスターの作成が完了したら、以下の手順に従ってルートパスワードを設定してください。

1.  クラスター概要ページの右上隅にある**「...」**をクリックし、 **「パスワード設定」**を選択します。

2.  クラスターに接続するためのルートパスワードを設定し、 **[保存]**をクリックします。

    **「パスワードを自動生成」をクリックすると、ランダムなパスワード**が生成されます。生成されたパスワードは二度と表示されないため、安全な場所に保存してください。

## 次は？ {#what-s-next}

TiDB Cloud DedicatedクラスターがTiDB Cloud上に作成されたら、 [TiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/connect-to-tidb-cluster.md)に接続します」で提供されている方法を介してそれに接続できます。
