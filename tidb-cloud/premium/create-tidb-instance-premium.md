---
title: Create a TiDB Cloud Premium Instance
summary: TiDB Cloud Premiumインスタンスの作成方法を学びましょう。
---

# TiDB Cloud Premiumインスタンスを作成する {#create-a-tidb-cloud-premium-instance}

このドキュメントでは[TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud Premium インスタンスを作成する方法について説明します。 。

> **注記：**
>
> -   現在、 TiDB Cloud Premiumはリクエストに応じてのみご利用いただけます。TiDB Cloud Premiumをリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)**？」**をクリックし、 次に**「サポートチケット」**をクリックして[ヘルプセンター](https://tidb.support.pingcap.com/servicedesk/customer/portals)に移動します。チケットを作成し、「**説明」**フィールドに「 TiDB Cloud Premiumの申請」と入力して、 **「送信」を**クリックします。
> -   TiDB Cloud Dedicatedクラスターを作成する方法については、 [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

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

`Organization Owner`ロールをお持ちの場合は、次のようにしてTiDB Cloud Premium インスタンスを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/tidbs)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、右上隅の**「リソースの作成」**をクリックします。

2.  **リソース作成**ページで、プランとして**「プレミアム」**を選択してください。

3.  TiDB Cloud Premiumインスタンスの名前を入力し、インスタンスをホストするクラウドプロバイダーとリージョンを選択してください。

4.  （オプション）このTiDB Cloud Premium インスタンスを管理用のプロジェクトにグループ化するには、 **[インスタンスをプロジェクトにグループ化] を**クリックし、インスタンスの対象となるプロジェクトを選択します。組織内にプロジェクトがない場合は、 **[プロジェクトの作成] を**クリックして作成できます。

5.  「**容量」**エリアで、インスタンスのリクエスト容量ユニット（RCU）の最大数を設定します。

    RCUは、ワークロード用にプロビジョニングされたコンピューティングリソースを表します。TiDB Cloudは、需要に基づいてこの範囲内でインスタンスを自動的にスケーリングします。

    > **注記：**
    >
    > 実際の使用量がそれよりも少ない場合でも、最大RCU数の下に表示されている**最小請求RCU**数に基づいて請求されます。最大RCU値は100単位で設定する必要があります。

6.  TiDB Cloud Premiumインスタンスでは、リージョンごとの高可用性のみが有効になっており、設定変更はできません。詳細については、[高可用性](/tidb-cloud/serverless-high-availability.md)を参照してください。

7.  **「作成」**をクリックします。

    インスタンス作成プロセスが開始されます。選択したリージョンで初めてインスタンスを作成する場合、プロビジョニングには通常約30分かかります。選択したリージョンに既にインスタンスが存在する場合は、プロセスはより迅速に行われ、通常約1分以内に完了します。

## 次は？ {#what-s-next}

インスタンスの作成後、 [パブリックエンドポイント経由でTiDB Cloudに接続します](/tidb-cloud/premium/connect-to-premium-via-public-connection.md)手順に従ってインスタンスのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、インスタンスに接続できません。
