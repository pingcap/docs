---
title: Create a TiDB Cloud Premium Instance
summary: TiDB Cloud Premium インスタンスを作成する方法を学習します。
---

# TiDB Cloud Premiumインスタンスを作成する {#create-a-tidb-cloud-premium-instance}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud Premium インスタンスを作成する方法について説明します。

> **注記：**
>
> -   現在、 TiDB Cloud Premiumはリクエストに応じてのみご利用いただけます。リクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポート**をリクエスト」をクリックしてください。次に、 **「説明」**欄に「 TiDB Cloud Premiumを申請」と入力し、 **「送信」**をクリックしてください。
> -   TiDB Cloud Dedicated クラスターを作成する方法については、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントを登録してください。

<CustomContent language="en,zh">

-   TiDB Cloud を使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplaceをご利用の場合は、AWS Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplaceをご利用の場合は、Azure Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Azureマーケットプレイス](https://azuremarketplace.microsoft.com)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace ユーザーの方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Alibaba Cloud Marketplaceをご利用の方は、Alibaba Cloud Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [アリババクラウドマーケットプレイス](https://marketplace.alibabacloud.com/)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。

</CustomContent>

<CustomContent language="ja">

-   TiDB Cloud を使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplaceをご利用の場合は、AWS Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Azure Marketplaceをご利用の場合は、Azure Marketplaceからサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Azureマーケットプレイス](https://azuremarketplace.microsoft.com)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。
-   Google Cloud Marketplace ユーザーの方は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 「TiDB Cloud」をサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定してください。

</CustomContent>

## 手順 {#steps}

`Organization Owner`ロールを持っている場合は、次のようにTiDB Cloud Premium インスタンスを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、左下隅の**[プライベート プレビューに切り替える]**をクリックして、 TiDB Cloud Premium の**TiDB インスタンス**ページを開きます。

    > **注記：**
    >
    > TiDB Cloudコンソールの左下に**「プライベートプレビューに切り替える」**が表示されない場合は、組織がTiDB Cloud Premium のプライベートプレビューに招待されていないことを意味します。その場合は、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックしてTiDB Cloud Premium にお申し込みください。

2.  **TiDB インスタンス**ページで、**インスタンスの作成を**クリックします。

3.  TiDB Cloud Premium インスタンスの名前を入力します。

4.  クラウド プロバイダーとインスタンスをホストするリージョンを選択します。

5.  インスタンスのリクエスト容量ユニット（RCU）の最小数と最大数を指定します

    RCU は、ワークロード用にプロビジョニングされたコンピューティングリソースを表します。TiDB TiDB Cloud は、需要に応じてこの範囲内でインスタンスを自動的にスケーリングします。

6.  **[作成]**をクリックします。

    インスタンス作成プロセスが開始されます。選択したリージョンで最初のインスタンスを作成する場合、プロビジョニングには通常約30分かかります。選択したリージョンに既にインスタンスが存在する場合は、プロセスはより速く、通常は約1分以内に完了します。

<!--## What's next

After your instance is created, follow the instructions in [Connect to TiDB Cloud via Public Endpoint](/tidb-cloud/connect-via-standard-connection-premium.md) to create a password for your instance.

> **Note:**
>
> If you do not set a password, you cannot connect to the instance.
-->
