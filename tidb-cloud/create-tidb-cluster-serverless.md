---
title: Create a TiDB Serverless Cluster
summary: Learn how to create your TiDB Serverless cluster.
---

# TiDB サーバーレスクラスタを作成する {#create-a-tidb-serverless-cluster}

このドキュメントでは、 [TiDB Cloudコンソール](https://tidbcloud.com/)で TiDB Serverless クラスターを作成する方法について説明します。

> **ヒント：**
>
> TiDB 専用クラスターを作成する方法については、 [TiDB専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md)参照してください。

## あなたが始める前に {#before-you-begin}

TiDB Cloudアカウントをお持ちでない場合は、 [ここ](https://tidbcloud.com/signup)クリックしてアカウントを登録してください。

-   TiDB Cloudを使用してパスワードを管理できるように、メールアドレスとパスワードでサインアップするか、Google、GitHub、または Microsoft アカウントでサインアップすることができます。
-   AWS Marketplace ユーザーの場合は、AWS Marketplace からサインアップすることもできます。そのためには、 `TiDB Cloud` in [AWS マーケットプレイス](https://aws.amazon.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。
-   Google Cloud Marketplace ユーザーの場合は、Google Cloud Marketplace からサインアップすることもできます。サインアップするには、 `TiDB Cloud` in [Google Cloud マーケットプレイス](https://console.cloud.google.com/marketplace)を検索し、 TiDB Cloudをサブスクライブして、画面の指示に従ってTiDB Cloudアカウントを設定します。

## 手順 {#steps}

ロール`Organization Owner`または`Project Owner`の場合は、次のように TiDB Serverless クラスターを作成できます。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、 [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  **クラスタの作成を**クリックします。

3.  **「クラスタの作成」**ページでは、デフォルトで**「Serverless」**が選択されています。

4.  TiDB Serverless のクラウド プロバイダーは AWS です。クラスターをホストする AWS リージョンを選択できます。

5.  必要に応じてデフォルトのクラスター名を更新します。

6.  クラスター プランを選択します。TiDB Serverless では、**無料クラスタ**と**スケーラブルクラスタ**の 2 つ[クラスター計画](/tidb-cloud/select-cluster-tier.md#cluster-plans)プランが提供されています。まずは無料クラスターから始めて、ニーズの拡大に応じてスケーラブル クラスターにアップグレードできます。スケーラブル クラスターを作成するには、**月間支出限度額**を指定し、クレジットカードを追加する必要があります。

    > **注記：**
    >
    > TiDB Cloudの各組織では、デフォルトで最大 5 [フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)のクラスターを作成できます。さらに TiDB Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)作成する必要があります。

7.  **[作成]を**クリックします。

    クラスター作成プロセスが開始され、約 30 秒以内にTiDB Cloudクラスターが作成されます。

## 次は何ですか {#what-s-next}

クラスターが作成されたら、 [パブリックエンドポイント経由でTiDB Serverlessに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)手順に従ってクラスターのパスワードを作成します。

> **注記：**
>
> パスワードを設定しないと、クラスターに接続できません。
