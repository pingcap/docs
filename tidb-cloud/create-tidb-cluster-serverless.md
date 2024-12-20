---
title: Create a TiDB Cloud Serverless Cluster
summary: TiDB Cloud Serverless クラスターを作成する方法を学習します。
---

# TiDB Cloudサーバーレスクラスタを作成する {#create-a-tidb-cloud-serverless-cluster}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com/)でTiDB Cloud Serverless クラスターを作成する方法について説明します。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターを作成する方法については、 [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

## 始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントを登録してください。

-   TiDB Cloud を使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplace ユーザーの場合は、AWS Marketplace からサインアップすることもできます。そのためには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。
-   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。

## 手順 {#steps}

ロール`Organization Owner`または`Project Owner`の場合は、次のようにしてTiDB Cloud Serverless クラスターを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **クラスタの作成を**クリックします。

3.  **「クラスタの作成」**ページでは、デフォルトで**「Serverless」**が選択されています。

4.  TiDB Cloud Serverless のクラウド プロバイダーは AWS です。クラスターをホストする AWS リージョンを選択できます。

5.  必要に応じてデフォルトのクラスター名を更新します。

6.  クラスター プランを選択します。TiDB TiDB Cloud Serverless では、**無料クラスタ**と**スケーラブルクラスタの**2 [クラスター計画](/tidb-cloud/select-cluster-tier.md#cluster-plans)プランが提供されています。まずは無料クラスターから始めて、ニーズの拡大に応じてスケーラブル クラスターにアップグレードできます。スケーラブル クラスターを作成するには、**月間支出限度額**を指定し、クレジットカードを追加する必要があります。

    > **注記：**
    >
    > TiDB Cloudの各組織では、デフォルトで最大 5 つの[フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)を作成できます。さらにTiDB Cloud Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)作成する必要があります。

7.  **[作成]**をクリックします。

    クラスター作成プロセスが開始され、約 30 秒以内にTiDB Cloudクラスターが作成されます。

## 次は何か {#what-s-next}

クラスターが作成されたら、 [パブリックエンドポイント経由でTiDB Cloud Serverlessに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)手順に従ってクラスターのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、クラスターに接続できません。
