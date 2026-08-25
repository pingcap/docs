---
title: Connect to Amazon RDS via a Private Link Connection
summary: AWS Endpoint Serviceのプライベートリンク接続を使用してAmazon RDSインスタンスに接続する方法を学びましょう。
---

# プライベートリンク接続を介してAmazon RDSに接続する {#connect-to-amazon-rds-via-a-private-link-connection}

このドキュメントでは[AWS Endpoint Service プライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用してTiDB Cloud Essentialインスタンスを[Amazon RDS](https://aws.amazon.com/rds/)インスタンスに接続する方法について説明します。

## 前提条件 {#prerequisites}

- 既存のAmazon RDSインスタンスをお持ちであるか、またはインスタンスを作成するために必要な権限をお持ちであること。

- お客様のアカウントには、ネットワークコンポーネントを管理するための以下の権限があります。

    - セキュリティグループを管理する
    - ロードバランサーを管理する
    - エンドポイントサービスを管理する

- お客様のTiDB Cloud EssentialはAWS上でホストされており、現在アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    - AWSアカウントID
    - 利用可能ゾーン（AZ）

AWSアカウントIDとアベイラビリティゾーンを表示するには、以下の手順を実行してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com)TiDB Cloud Essentialインスタンスの概要ページに移動し、左側のナビゲーションペインで **Settings** > **Networking** をクリックします。
2. **AWS Private Endpoints for External Services** 領域で、**Create Private Endpoint for External Services** をクリックします。
3. 表示されたダイアログには、AWSアカウントIDとアベイラビリティゾーンが表示されます。

## ステップ1. Amazon RDSインスタンスをセットアップする {#step-1-set-up-the-amazon-rds-instance}

使用する Amazon RDS インスタンスを特定するか、 [新しいものを作成する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html)。

Amazon RDSインスタンスは、以下の要件を満たす必要があります。

- リージョンの一致：インスタンスは、 TiDB Cloud Essentialインスタンスと同じAWSリージョンに存在する必要があります。
- Amazon RDS インスタンスの[サブネットグループ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets)には、TiDB Cloud Essentialインスタンスのアベイラビリティゾーンと重複するアベイラビリティゾーンが必要です。
- Amazon RDSインスタンスに適切なセキュリティグループを設定し、VPC内からアクセス可能であることを確認してください。例えば、以下のルールを持つセキュリティグループを作成できます。

    - MySQL/ Auroraを許可する受信ルール：
        - タイプ: `MySQL/Aurora`
        - ソース: `Anywhere-IPv4`
    - MySQL/ Auroraを許可する送信ルール：
        - タイプ: `MySQL/Aurora`
        - 宛先: `Anywhere-IPv4`

> **Note**
>
> 現在、 TiDB Cloud Essentialではリージョン間接続はサポートされていません。リージョン間接続が必要な場合は、 TiDB Cloud Premiumをご利用いただき、VPCピアリングによる接続を確立してください。

## ステップ2. Amazon RDSインスタンスをエンドポイントサービスとして公開する {#step-2-expose-the-amazon-rds-instance-as-an-endpoint-service}

AWSコンソールでロードバランサーとAWSエンドポイントサービスを設定する必要があります。

### ステップ2.1. ロードバランサーの設定 {#step-2-1-set-up-the-load-balancer}

ロードバランサーをRDSと同じリージョンに設定するには、以下の手順を実行してください。

1. [対象グループ](https://console.aws.amazon.com/ec2/home#CreateTargetGroup)に移動して、対象グループを作成します。次の情報を入力してください。

    - **Target type**: `IP addresses`を選択してください。
    - **Protocol and Port**: プロトコルを`TCP`に、ポートをデータベースのポートに設定します。たとえば、MySQL の場合は`3306`です。
    - **IP address type**： `IPv4`を選択してください。
    - **VPC** ：RDSが配置されているVPCを選択してください。
    - **Register targets**：Amazon RDSインスタンスのIPアドレスを登録します。RDSエンドポイントにpingを実行すると、IPアドレスを取得できます。

    詳細については、 [ネットワークロードバランサーのターゲットグループを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html)を参照してください。

2. [ロードバランサー](https://console.aws.amazon.com/ec2/home#LoadBalancers)に移動して、ネットワークロードバランサーを作成します。次の情報を入力してください。

    - **Schema**: `Internal`を選択

    - **Load balancer IP address type**： `IPv4`を選択

    - **VPC** ：RDSが配置されているVPCを選択してください。

    - **Availability Zones**： TiDB Cloud Essentialインスタンスと重複するアベイラビリティゾーンを選択してください。

    - **Security groups**：以下のルールで新しいセキュリティグループを作成します。
        - MySQL/ Auroraを許可する受信ルール：
            - タイプ: `MySQL/Aurora`
            - ソース: `Anywhere-IPv4`

        - MySQL/ Auroraを許可する送信ルール：
            - タイプ: `MySQL/Aurora`
            - 宛先: `Anywhere-IPv4`

    - **Listeners and routing**：
        - **Protocol and Port**：プロトコルを`TCP`に、ポートをデータベースのポート番号に設定します。例えば、MySQLの場合は`3306`です。
        - **Target group**: 前の手順で作成した対象グループを選択してください。

詳細については、 [ネットワークロードバランサーを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)を参照してください。

### ステップ2.2. AWSエンドポイントサービスの設定 {#step-2-2-set-up-the-aws-endpoint-service}

エンドポイントサービスをRDSと同じリージョンに設定するには、以下の手順を実行してください。

1. [エンドポイントサービス](https://console.aws.amazon.com/vpcconsole/home#EndpointServices)に移動して、エンドポイントサービスを作成します。次の情報を入力してください。

    - **Load balancer type**： `Network`を選択
    - **Available load balancers**：前の手順で作成したロードバランサーを入力してください。
    - **Supported Regions**：地域をまたぐ要件がない場合は空欄のままにしてください。
    - **Require acceptance for endpoint**： `Acceptance required`を選択することをお勧めします
    - **Supported IP address types**： `IPv4`を選択してください

2. エンドポイントサービスの詳細ページに移動し、 `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`の形式でエンドポイントサービス名をコピーしてください。この名前をTiDB Cloudに提供する必要があります。

3. エンドポイントサービスの詳細ページで、 **Allow principals**タブをクリックし、[前提条件](#prerequisites)で取得したAWSアカウントIDを許可リストに追加します。例えば、 `arn:aws:iam::<account_id>:root`のように追加します。

## ステップ3. TiDB CloudでAWSエンドポイントサービスのプライベートリンク接続を作成します。 {#step-3-create-an-aws-endpoint-service-private-link-connection-in-tidb-cloud}

TiDB CloudコンソールまたはTiDB Cloud CLIを使用して、プライベートリンク接続を作成できます。

詳細については、 [AWS Endpoint Service のプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)を参照してください。
