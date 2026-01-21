---
title: Connect to Amazon RDS via a Private Link Connection
summary: AWS エンドポイント サービス プライベートリンク接続を使用して Amazon RDS インスタンスに接続する方法を学習します。
---

# プライベートリンク接続経由で Amazon RDS に接続する {#connect-to-amazon-rds-via-a-private-link-connection}

このドキュメントでは、 [AWS エンドポイントサービスプライベートリンク接続](/tidb-cloud/serverless-private-link-connection.md)を使用してTiDB Cloud Essential クラスターを[アマゾンRDS](https://aws.amazon.com/rds/)インスタンスに接続する方法について説明します。

## 前提条件 {#prerequisites}

-   既存の Amazon RDS インスタンスがあるか、インスタンスを作成するために必要な権限があります。

-   アカウントには、ネットワーク コンポーネントを管理するための次の権限があります。

    -   セキュリティ グループを管理する
    -   ロードバランサーの管理
    -   エンドポイントサービスの管理

-   TiDB Cloud Essential は AWS でホストされており、アクティブです。後で使用するために、以下の詳細情報を取得して保存してください。

    -   AWSアカウントID
    -   可用性ゾーン（AZ）

AWS アカウント ID とアベイラビリティーゾーンを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、TiDB クラスターのクラスター概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。
2.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。
3.  表示されたダイアログで、AWS アカウント ID とアベイラビリティーゾーンを見つけることができます。

## ステップ1. Amazon RDSインスタンスをセットアップする {#step-1-set-up-the-amazon-rds-instance}

使用する Amazon RDS インスタンスを識別します。または[新しいものを作成する](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_CreateDBInstance.html) 。

Amazon RDS インスタンスは次の要件を満たしている必要があります。

-   リージョンの一致: インスタンスは、 TiDB Cloud Essential クラスターと同じ AWS リージョンに存在する必要があります。
-   Amazon RDS インスタンスの[サブネットグループ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_VPC.WorkingWithRDSInstanceinaVPC.html#USER_VPC.Subnets)つには、 TiDB Cloud Essential クラスターのアベイラビリティーゾーンと重複するアベイラビリティーゾーンが必要です。
-   Amazon RDS インスタンスに適切なセキュリティグループを設定し、VPC 内でアクセスできるようにします。例えば、以下のルールでセキュリティグループを作成できます。

    -   MySQL/ Auroraを許可するインバウンドルール:
        -   タイプ: `MySQL/Aurora`
        -   出典: `Anywhere-IPv4`
    -   MySQL/ Auroraを許可するアウトバウンドルール:
        -   タイプ: `MySQL/Aurora`
        -   目的地: `Anywhere-IPv4`

> **注記**
>
> クロスリージョン RDS インスタンスに接続するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。

## ステップ2. Amazon RDSインスタンスをエンドポイントサービスとして公開する {#step-2-expose-the-amazon-rds-instance-as-an-endpoint-service}

AWS コンソールでロードバランサーと AWS エンドポイントサービスを設定する必要があります。

### ステップ2.1. ロードバランサーを設定する {#step-2-1-set-up-the-load-balancer}

RDS と同じリージョンにロードバランサーを設定するには、次の手順を実行します。

1.  ターゲットグループを作成するには、 [対象グループ](https://console.aws.amazon.com/ec2/home#CreateTargetGroup)に進んでください。以下の情報を入力してください。

    -   **ターゲットタイプ**: `IP addresses`を選択します。
    -   **プロトコルとポート**: プロトコルを`TCP`に設定し、ポートをデータベース ポート (たとえば、MySQL の場合は`3306`に設定します。
    -   **IP アドレスの種類**: `IPv4`を選択します。
    -   **VPC** : RDS が配置されている VPC を選択します。
    -   **ターゲットの登録**: Amazon RDSインスタンスのIPアドレスを登録します。RDSエンドポイントにpingを実行してIPアドレスを取得できます。

    詳細については[ネットワークロードバランサーのターゲットグループを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-target-group.html)参照してください。

2.  [ロードバランサー](https://console.aws.amazon.com/ec2/home#LoadBalancers)に進み、ネットワークロードバランサーを作成します。以下の情報を入力してください。

    -   **スキーマ**: `Internal`を選択

    -   **ロードバランサのIPアドレスタイプ**： `IPv4`選択

    -   **VPC** : RDS が配置されている VPC を選択します。

    -   **可用性ゾーン**: TiDB Cloud Essential クラスターと重複する可用性ゾーンを選択します

    -   **Securityグループ**: 次のルールで新しいセキュリティ グループを作成します。
        -   MySQL/ Auroraを許可するインバウンドルール:
            -   タイプ: `MySQL/Aurora`
            -   出典: `Anywhere-IPv4`

        -   MySQL/ Auroraを許可するアウトバウンドルール:
            -   タイプ: `MySQL/Aurora`
            -   目的地: `Anywhere-IPv4`

    -   **リスナーとルーティング**:
        -   **プロトコルとポート**: プロトコルを`TCP`に設定し、ポートをデータベースポートに設定します。たとえば、MySQLの場合は`3306` 。
        -   **ターゲットグループ**: 前の手順で作成したターゲットグループを選択します

詳細については[ネットワークロードバランサーを作成する](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/create-network-load-balancer.html)参照してください。

### ステップ2.2. AWSエンドポイントサービスを設定する {#step-2-2-set-up-the-aws-endpoint-service}

RDS と同じリージョンにエンドポイント サービスを設定するには、次の手順を実行します。

1.  エンドポイントサービスを作成するには、 [エンドポイントサービス](https://console.aws.amazon.com/vpcconsole/home#EndpointServices)に進んでください。以下の情報を入力してください。

    -   **ロードバランサの種類**: `Network`選択
    -   **利用可能なロードバランサ**: 前の手順で作成したロードバランサを入力します。
    -   **サポートされているリージョン**: リージョン間の要件がない場合は空白のままにしてください
    -   **エンドポイントの承認が必要**: `Acceptance required`選択することをお勧めします
    -   **サポートされているIPアドレスの種類**： `IPv4`選択

2.  エンドポイントサービスの詳細ページに移動し、エンドポイントサービス名`com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx`の形式）をコピーします。この名前をTiDB Cloudに提供する必要があります。

3.  エンドポイントサービスの詳細ページで、 **「プリンシパルの許可」**タブをクリックし、 [前提条件](#prerequisites)で取得した AWS アカウント ID (例: `arn:aws:iam::<account_id>:root`を許可リストに追加します。

## ステップ3. TiDB CloudでAWSエンドポイントサービスのプライベートリンク接続を作成する {#step-3-create-an-aws-endpoint-service-private-link-connection-in-tidb-cloud}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用してプライベート リンク接続を作成できます。

詳細については[AWS エンドポイントサービスプライベートリンク接続を作成する](/tidb-cloud/serverless-private-link-connection.md#create-an-aws-endpoint-service-private-link-connection)参照してください。
