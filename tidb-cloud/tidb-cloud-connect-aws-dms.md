---
title: Connect AWS DMS to TiDB Cloud clusters
summary: AWS Database Migration Service (AWS DMS) を使用して、 TiDB Cloudとの間でデータを移行する方法を学びます。
---

# AWS DMS をTiDB Cloudクラスターに接続する {#connect-aws-dms-to-tidb-cloud-clusters}

[AWS データベース移行サービス (AWS DMS)](https://aws.amazon.com/dms/)は、リレーショナルデータベース、データウェアハウス、NoSQL データベース、その他さまざまなデータストアの移行を可能にするクラウドサービスです。AWS DMS を使用して、 TiDB Cloudクラスター間でデータを移行できます。このドキュメントでは、AWS DMS をTiDB Cloudクラスターに接続する方法について説明します。

## 前提条件 {#prerequisites}

### 十分なアクセス権を持つAWSアカウント {#an-aws-account-with-enough-access}

DMS関連リソースを管理するための十分なアクセス権を持つAWSアカウントをお持ちであることが前提となります。お持ちでない場合は、以下のAWSドキュメントをご参照ください。

- [AWSアカウントにサインアップする](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SettingUp.html#sign-up-for-aws)
- [AWS Database Migration Service の ID およびアクセス管理](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html)

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudアカウントと、 TiDB Cloud Starter、 TiDB Cloud Essential、またはTiDB Cloud Dedicated クラスターをお持ちであることが前提となります。お持ちでない場合は、以下のドキュメントを参照して作成してください。

- [TiDB Cloud Starter または Essential クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)
- [TiDB Cloud Dedicatedクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)

## ネットワークを構成する {#configure-network}

DMSリソースを作成する前に、DMSがTiDB Cloudクラスターと通信できるようにネットワークを適切に設定する必要があります。AWSに詳しくない場合は、AWSサポートにお問い合わせください。以下に、参考までにいくつかの設定例を示します。

<SimpleTab>

<div label="TiDB Cloud Starter or Essential">

TiDB Cloud Starter またはTiDB Cloud Essential の場合、クライアントはパブリック エンドポイントまたはプライベート エンドポイントを介してクラスターに接続できます。

<CustomContent language="en,zh">

- [パブリックエンドポイント経由でTiDB Cloud Starter または Essential クラスターに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)場合、次のいずれかを実行して、DMS レプリケーション インスタンスがインターネットにアクセスできることを確認します。

    - レプリケーションインスタンスをパブリックサブネットにデプロイし、 **Public accessible**を有効にします。詳細については、 [インターネットアクセスのコンフィグレーション](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)を参照してください。

    - レプリケーションインスタンスをプライベートサブネットにデプロイし、プライベートサブネット内のトラフィックをパブリックサブネットにルーティングします。この場合、少なくとも3つのサブネット（プライベートサブネット2つとパブリックサブネット1つ）が必要です。2つのプライベートサブネットは、レプリケーションインスタンスが存在するサブネットグループを形成します。次に、パブリックサブネットにNATゲートウェイを作成し、2つのプライベートサブネットのトラフィックをNATゲートウェイにルーティングする必要があります。詳細については、 [プライベートサブネットからインターネットにアクセスする](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)を参照してください。

- プライベート エンドポイント経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続するには、次のドキュメントを参照して、まずプライベート エンドポイントを設定し、プライベート サブネットにレプリケーション インスタンスをデプロイします。

    - [AWS PrivateLink 経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
    - [Alibaba Cloud プライベートエンドポイント経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

- [パブリックエンドポイント経由でTiDB Cloud Starter または Essential クラスターに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)場合、次のいずれかを実行して、DMS レプリケーション インスタンスがインターネットにアクセスできることを確認します。

    - レプリケーションインスタンスをパブリックサブネットにデプロイし、 **Public accessible**を有効にします。詳細については、 [インターネットアクセスのコンフィグレーション](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)を参照してください。

    - レプリケーションインスタンスをプライベートサブネットにデプロイし、プライベートサブネット内のトラフィックをパブリックサブネットにルーティングします。この場合、少なくとも3つのサブネット（プライベートサブネット2つとパブリックサブネット1つ）が必要です。2つのプライベートサブネットは、レプリケーションインスタンスが存在するサブネットグループを形成します。次に、パブリックサブネットにNATゲートウェイを作成し、2つのプライベートサブネットのトラフィックをNATゲートウェイにルーティングする必要があります。詳細については、 [プライベートサブネットからインターネットにアクセスする](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)を参照してください。

- プライベート エンドポイント経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続するには、まず[AWS PrivateLink 経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してプライベート エンドポイントを設定し、レプリケーション インスタンスをプライベート サブネットにデプロイします。

</CustomContent>

</div>

<div label="TiDB Cloud Dedicated">

TiDB Cloud Dedicated の場合、クライアントはパブリック エンドポイント、プライベート エンドポイント、または VPC ピアリングを介してクラスターに接続できます。

- [パブリックエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する](/tidb-cloud/connect-via-standard-connection.md)については、DMS レプリケーションインスタンスがインターネットにアクセスできることを確認するために、次のいずれかを実行します。さらに、レプリケーションインスタンスまたは NAT ゲートウェイのパブリック IP アドレスをクラスターの[IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)に追加する必要があります。

    - レプリケーションインスタンスをパブリックサブネットにデプロイし、 **Public accessible**を有効にします。詳細については、 [インターネットアクセスのコンフィグレーション](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)を参照してください。

    - レプリケーションインスタンスをプライベートサブネットにデプロイし、プライベートサブネット内のトラフィックをパブリックサブネットにルーティングします。この場合、少なくとも3つのサブネット（プライベートサブネット2つとパブリックサブネット1つ）が必要です。2つのプライベートサブネットは、レプリケーションインスタンスが存在するサブネットグループを形成します。次に、パブリックサブネットにNATゲートウェイを作成し、2つのプライベートサブネットのトラフィックをNATゲートウェイにルーティングする必要があります。詳細については、 [プライベートサブネットからインターネットにアクセスする](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)を参照してください。

- プライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続するには、 [プライベートエンドポイントを設定する](/tidb-cloud/set-up-private-endpoint-connections.md) 、プライベート サブネットにレプリケーション インスタンスをデプロイします。

- VPC ピアリング経由でTiDB Cloud Dedicated クラスターに接続するには、 [VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md) 、プライベート サブネットにレプリケーション インスタンスをデプロイします。

</div>
</SimpleTab>

## AWS DMS レプリケーションインスタンスを作成する {#create-an-aws-dms-replication-instance}

1. AWS DMSコンソールの[**Replication instances**](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。AWS DMSでは、 TiDB Cloudと同じリージョンを使用することをお勧めします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-replication-instances.png)

2. **Create replication instance**をクリックします。

3. インスタンス名、ARN、説明を入力します。

4. **Instance configuration**セクションで、インスタンスを構成します。
    - **Instance class**: 適切なインスタンスクラスを選択します。詳細については、 [レプリケーションインスタンスタイプの選択](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html)を参照してください。
    - **Engine version**: デフォルト構成を維持します。
    - **High Availability**: ビジネス ニーズに応じて、**Multi-AZ**または**Single-AZ**を選択します。

5. **Allocated storage (GiB)**フィールドでストレージを構成します。

6. 接続とセキュリティを設定します。ネットワーク設定については[前のセクション](#configure-network)を参照してください。

    - **Network type - new**: **IPv4**を選択します。
    - **Virtual private cloud (VPC) for IPv4**: 必要な VPC を選択します。
    - **Replication subnet group**: レプリケーション インスタンスのサブネット グループを選択します。
    - **Public accessible**: ネットワーク構成に基づいて設定します。

    ![Connectivity and security](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-connectivity-security.png)

7. 必要に応じて、 **Advanced settings** 、 **Maintenance** 、 **Tags**セクションを構成し、 **Create replication instance**をクリックしてインスタンスの作成を完了します。

> **Note:**
>
> AWS DMS はサーバーレスレプリケーションもサポートしています。詳細な手順については、 [サーバーレスレプリケーションの作成](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.Components.html#CHAP_Serverless.create)をご覧ください。レプリケーションインスタンスとは異なり、AWS DMS のサーバーレスレプリケーションでは**Public accessible**オプションは提供されません。

## TiDB Cloud DMSエンドポイントを作成する {#create-tidb-cloud-dms-endpoints}

接続に関しては、 TiDB Cloudクラスターをソースとして使用する場合とターゲットとして使用する場合の手順は似ていますが、DMS ではソースとターゲットでデータベース設定要件が異なります。詳細については、 [MySQLをソースとして使用する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html)または[MySQLをターゲットとして使用する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html)を参照してください。TiDB Cloudクラスターをソースとして使用する場合、TiDB は MySQL binlogをサポートしていないため、**Migrate existing data**のみが可能です。

1. AWS DMS コンソールで、 [**Endpoints**](https://console.aws.amazon.com/dms/v2/home#endpointList)ページに移動し、対応するリージョンに切り替えます。

    ![Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-create-endpoint.png)

2. **Create endpoint**をクリックして、ターゲット データベース エンドポイントを作成します。

3. **Endpoint type**セクションで、 **Source endpoint**または**Target endpoint**を選択します。

4. **Endpoint configuration**セクションで、**Endpoint identifier**とARNフィールドに入力します。次に、**Source engine**または**Target engine**として**MySQL**を選択します。

5. **Access to endpoint database**フィールドで、 **Provide access information manually**チェックボックスをオンにし、次のようにクラスター情報を入力します。

    <SimpleTab>

    <div label="TiDB Cloud Starter or Essential">

    - **Server name**: クラスターの`HOST` 。
    - **Port**: クラスターの`PORT` 。
    - **User name**: 移行先クラスターのユーザー。DMSの要件を満たしていることを確認してください。
    - **Password**: クラスター ユーザーのパスワード。
    - **Secure Socket Layer (SSL) mode**：パブリックエンドポイント経由で接続する場合は、トランスポートセキュリティを確保するために、モードを**verify-full**に設定することを強くお勧めします。プライベートエンドポイント経由で接続する場合は、モードを**none**に設定できます。
    - （オプション） **CA certificate**： [ISRGルートX1証明書](https://letsencrypt.org/certs/isrgrootx1.pem)を使用します。詳細については、 [TiDB Cloud Starter または Essential への TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。

    </div>

    <div label="TiDB Cloud Dedicated">

    - **Server name**: TiDB Cloud Dedicatedクラスターの`HOST` 。
    - **Port**: TiDB Cloud Dedicated クラスターの`PORT` 。
    - **User name**：移行用のTiDB Cloud Dedicatedクラスタのユーザー。DMS要件を満たしていることを確認してください。
    - **Password**: TiDB Cloud Dedicated クラスター ユーザーのパスワード。
    - **Secure Socket Layer (SSL) mode**：パブリックエンドポイント経由で接続する場合は、トランスポートセキュリティを確保するために、モードを**verify-full**に設定することを強くお勧めします。プライベートエンドポイント経由で接続する場合は、 **none**に設定できます。
    - (オプション) **CA certificate**: [TiDB Cloud DedicatedへのTLS接続](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)に従って CA 証明書を取得します。

    </div>
     </SimpleTab>

    ![Provide access information manually](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-configure-endpoint.png)

6. エンドポイントを**Target endpoint**として作成する場合は、**Endpoint settings**セクションを展開し、**Use endpoint connection attributes**チェックボックスをオンにして、**Extra connection attributes**を`Initstmt=SET FOREIGN_KEY_CHECKS=0;`に設定します。

7. 必要に応じて、 **KMS Key**と**Tags**のセクションを設定します。 **Create endpoint**をクリックしてインスタンスの作成を完了します。
