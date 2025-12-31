---
title: Connect to Confluent Cloud on AWS via a Private Link Connection
summary: AWS エンドポイント サービス プライベート リンク接続を使用して AWS 上の Confluent Cloud Dedicated クラスターに接続する方法を学習します。
---

# プライベートリンク接続を介して AWS 上の Confluent Cloud に接続する {#connect-to-confluent-cloud-on-aws-via-a-private-link-connection}

このドキュメントでは、 [AWS エンドポイントサービスプライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用してTiDB Cloud Essential クラスターを AWS 上の[Confluent Cloud 専用クラスタ](https://docs.confluent.io/cloud/current/clusters/cluster-types.html)に接続する方法について説明します。

> **注記**
>
> AWS 上のすべての Confluent Cloud クラスター タイプのうち、プライベート リンク接続をサポートするのは Confluent Cloud Dedicated クラスターのみです。

## 前提条件 {#prerequisites}

-   アカウントは[コンフルエントクラウド](https://confluent.cloud/)あります。

-   TiDB Cloud Essential は AWS でホストされており、アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    -   AWSアカウントID
    -   可用性ゾーン（AZ）

AWS アカウント ID とアベイラビリティーゾーンを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  表示されたダイアログで、AWS アカウント ID とアベイラビリティーゾーンを見つけることができます。

## ステップ1. Confluent Cloudネットワークをセットアップする {#step-1-set-up-a-confluent-cloud-network}

使用する Confluent Cloud ネットワークを識別します。または[AWS 上に新しい Confluent Cloud ネットワークを作成する](https://docs.confluent.io/cloud/current/networking/ccloud-network/aws.html#create-ccloud-network-aws) 。

Confluent Cloud ネットワークは次の要件を満たしている必要があります。

-   タイプ: ネットワークは**PrivateLink**ネットワークである必要があります。
-   リージョンの一致: ネットワークは、 TiDB Cloud Essential クラスターと同じ AWS リージョンに存在する必要があります。
-   AZ (アベイラビリティ ゾーン) の可用性: ネットワークのアベイラビリティ ゾーンは、 TiDB Cloud Essential クラスターのアベイラビリティ ゾーンと重複している必要があります。

Confluent Cloud ネットワークの一意の名前を取得するには、次の手順を実行します。

1.  [Confluent クラウド コンソール](https://confluent.cloud/)で[**環境**](https://confluent.cloud/environments)ページに移動し、Confluent Cloud ネットワークが配置されている環境をクリックします。
2.  **[ネットワーク管理]**をクリックし、 **[専用クラスター用]**を選択して、作成したネットワークを見つけます。
3.  Confluent Cloud ネットワークの DNS サブドメインを取得するには、**ネットワークの概要**ページに移動します。
4.  DNSサブドメインからConfluent Cloudネットワークの一意の名前を抽出します。例えば、DNSサブドメインが`use1-az1.domnprzqrog.us-east-1.aws.confluent.cloud`の場合、一意の名前は`domnprzqrog.us-east-1`です。
5.  後で使用するために一意の名前を保存します。

## ステップ2. ネットワークにPrivateLinkアクセスを追加する {#step-2-add-a-privatelink-access-to-the-network}

[ステップ1](#step-1-set-up-a-confluent-cloud-network)で特定または設定したネットワークにPrivateLinkアクセスを追加します。詳細については、 [Confluent Cloud に PrivateLink アクセスを追加する](https://docs.confluent.io/cloud/current/networking/private-links/aws-privatelink.html#add-a-privatelink-access-in-ccloud)参照してください。

プロセス中に、次の操作を行う必要があります。

-   [前提条件](#prerequisites)で取得したTiDB Cloud AWS アカウント ID を入力します。
-   Confluent Cloud によって提供される`VPC Service Endpoint` 、後で使用するために、通常は`com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`形式で保存します。

## ステップ3. ネットワークの下にConfluent Cloud専用クラスタを作成する {#step-3-create-a-confluent-cloud-dedicated-cluster-under-the-network}

[ステップ1](#step-1-set-up-a-confluent-cloud-network)で設定した既存のネットワーク下に Confluent Cloud Dedicated クラスターを作成します。詳細については、 [Confluent Cloud で専用クラスターを作成する](https://docs.confluent.io/cloud/current/clusters/create-cluster.html#create-ak-clusters)参照してください。

## ステップ4. TiDB Cloudでプライベートリンク接続を作成する {#step-4-create-a-private-link-connection-in-tidb-cloud}

TiDB Cloudでプライベート リンク接続を作成するには、次の手順を実行します。

1.  Confluent Cloud の`VPC Service Endpoint`使用して、 TiDB Cloudにプライベート リンク接続を作成します。

    詳細については[AWS エンドポイントサービスプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)参照してください。

    > **注記：**
    >
    > AWS 上の Confluent Cloud Dedicated クラスターの場合、 TiDB Cloudからのエンドポイント接続リクエストを手動で承認するために、AWS コンソールのエンドポイントサービスの詳細ページに移動する必要はありません。Confluent Cloud が自動的に処理します。

2.  TiDB Cloudのデータフロー サービスが Confluent クラスターにアクセスできるように、Confluent Cloud サービス ドメインをプライベート リンク接続に接続します。

    詳細については[プライベートリンク接続にドメインを添付する](/tidb-cloud/serverless-private-link-connection.md#attach-domains-to-a-private-link-connection)参照してください。
