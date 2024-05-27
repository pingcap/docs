---
title: Connect AWS DMS to TiDB Cloud clusters
summary: AWS Database Migration Service (AWS DMS) を使用して、TiDB Cloud から、またはTiDB Cloudにデータを移行する方法を学びます。
---

# AWS DMS をTiDB Cloudクラスターに接続する {#connect-aws-dms-to-tidb-cloud-clusters}

[AWS データベース移行サービス (AWS DMS)](https://aws.amazon.com/dms/) 、リレーショナル データベース、データ ウェアハウス、NoSQL データベース、およびその他の種類のデータ ストアの移行を可能にするクラウド サービスです。AWS DMS を使用して、 TiDB Cloudクラスターから、または TiDB Cloud クラスターにデータを移行できます。このドキュメントでは、AWS DMS をTiDB Cloudクラスターに接続する方法について説明します。

## 前提条件 {#prerequisites}

### 十分なアクセス権を持つAWSアカウント {#an-aws-account-with-enough-access}

DMS 関連のリソースを管理するのに十分なアクセス権を持つ AWS アカウントを持っている必要があります。そうでない場合は、次の AWS ドキュメントを参照してください。

-   [AWSアカウントにサインアップする](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SettingUp.html#sign-up-for-aws)
-   [AWS データベース移行サービスの ID およびアクセス管理](https://docs.aws.amazon.com/dms/latest/userguide/security-iam.html)

### TiDB Cloudアカウントと TiDB クラスター {#a-tidb-cloud-account-and-a-tidb-cluster}

TiDB Cloudアカウントと、TiDB Serverless または TiDB Dedicated クラスターが必要です。ない場合は、次のドキュメントを参照して作成してください。

-   [TiDB サーバーレス クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)
-   [TiDB専用クラスターを作成する](/tidb-cloud/create-tidb-cluster.md)

## ネットワークを構成する {#configure-network}

DMS リソースを作成する前に、DMS がTiDB Cloudクラスターと通信できるようにネットワークを適切に構成する必要があります。AWS に詳しくない場合は、AWS サポートにお問い合わせください。以下に、参考までにいくつかの可能な構成を示します。

<SimpleTab>

<div label="TiDB Serverless">

TiDB Serverless の場合、クライアントはパブリック エンドポイントまたはプライベート エンドポイントを介してクラスターに接続できます。

-   [パブリックエンドポイント経由でTiDB Serverlessクラスタに接続する](/tidb-cloud/connect-via-standard-connection-serverless.md)の場合、次のいずれかを実行して、DMS レプリケーション インスタンスがインターネットにアクセスできることを確認します。

    -   パブリックサブネットにレプリケーションインスタンスをデプロイ、**パブリックアクセス**を有効にします。詳細については、 [インターネットアクセスのコンフィグレーション](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)を参照してください。

    -   レプリケーション インスタンスをプライベート サブネットにデプロイ、プライベート サブネットのトラフィックをパブリック サブネットにルーティングします。この場合、少なくとも 3 つのサブネット (2 つのプライベート サブネットと 1 つのパブリック サブネット) が必要です。2 つのプライベート サブネットは、レプリケーション インスタンスが存在するサブネット グループを形成します。次に、パブリック サブネットに NAT ゲートウェイを作成し、2 つのプライベート サブネットのトラフィックを NAT ゲートウェイにルーティングする必要があります。詳細については、 [プライベートサブネットからインターネットにアクセスする](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)参照してください。

-   プライベート エンドポイント経由で TiDB Serverless クラスターに接続するには、 [プライベートエンドポイントを設定する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)プライベート サブネットにレプリケーション インスタンスをデプロイします。

</div>

<div label="TiDB Dedicated">

TiDB Dedicated の場合、クライアントはパブリック エンドポイント、プライベート エンドポイント、または VPC ピアリングを介してクラスターに接続できます。

-   [パブリックエンドポイント経由でTiDB専用クラスタに接続する](/tidb-cloud/connect-via-standard-connection.md)を実行するには、次のいずれかを実行して、DMS レプリケーション インスタンスがインターネットにアクセスできることを確認します。さらに、レプリケーション インスタンスまたは NAT ゲートウェイのパブリック IP アドレスをクラスターの[IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)に追加する必要があります。

    -   パブリックサブネットにレプリケーションインスタンスをデプロイ、**パブリックアクセス**を有効にします。詳細については、 [インターネットアクセスのコンフィグレーション](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html#vpc-igw-internet-access)を参照してください。

    -   レプリケーション インスタンスをプライベート サブネットにデプロイ、プライベート サブネットのトラフィックをパブリック サブネットにルーティングします。この場合、少なくとも 3 つのサブネット (2 つのプライベート サブネットと 1 つのパブリック サブネット) が必要です。2 つのプライベート サブネットは、レプリケーション インスタンスが存在するサブネット グループを形成します。次に、パブリック サブネットに NAT ゲートウェイを作成し、2 つのプライベート サブネットのトラフィックを NAT ゲートウェイにルーティングする必要があります。詳細については、 [プライベートサブネットからインターネットにアクセスする](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateway-scenarios.html#public-nat-internet-access)参照してください。

-   プライベート エンドポイント経由で TiDB 専用クラスターに接続するには、まず[プライベートエンドポイントを設定する](/tidb-cloud/set-up-private-endpoint-connections.md)実行し、プライベート サブネットにレプリケーション インスタンスをデプロイします。

-   VPC ピアリング経由で TiDB 専用クラスターに接続するには、まず[VPCピアリング接続を設定する](/tidb-cloud/set-up-vpc-peering-connections.md)実行し、プライベート サブネットにレプリケーション インスタンスをデプロイします。

</div>
</SimpleTab>

## AWS DMS レプリケーションインスタンスを作成する {#create-an-aws-dms-replication-instance}

1.  AWS DMS コンソールで、 [**レプリケーションインスタンス**](https://console.aws.amazon.com/dms/v2/home#replicationInstances)ページに移動し、対応するリージョンに切り替えます。AWS DMS にはTiDB Cloudと同じリージョンを使用することをお勧めします。

    ![Create replication instance](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-replication-instances.png)

2.  **レプリケーションインスタンスの作成を**クリックします。

3.  インスタンス名、ARN、説明を入力します。

4.  **インスタンス構成**セクションで、インスタンスを構成します。
    -   **インスタンスクラス**: 適切なインスタンスクラスを選択します。詳細については、 [レプリケーションインスタンスタイプの選択](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_ReplicationInstance.Types.html)を参照してください。
    -   **エンジン バージョン**: デフォルト設定を維持します。
    -   **高可用性**: ビジネス ニーズに応じて、**マルチ AZ**または**シングル AZ**を選択します。

5.  **割り当てられたstorage(GiB)**フィールドでstorageを構成します。

6.  接続性とセキュリティを構成します。ネットワーク構成については[前のセクション](#configure-network)を参照してください。

    -   **ネットワークタイプ - 新規**: **IPv4**を選択します。
    -   **IPv4 用の仮想プライベート クラウド (VPC)** : 必要な VPC を選択します。
    -   **レプリケーション サブネット グループ**: レプリケーション インスタンスのサブネット グループを選択します。
    -   **パブリックアクセス可能**: ネットワーク構成に基づいて設定します。

    ![Connectivity and security](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-connectivity-security.png)

7.  必要に応じて、 **[詳細設定]** 、 **[メンテナンス**]、 **[タグ]**セクションを構成し、 **[レプリケーション インスタンスの作成] を**クリックしてインスタンスの作成を完了します。

> **注記：**
>
> AWS DMS はサーバーレスレプリケーションもサポートしています。詳細な手順については、 [サーバーレスレプリケーションの作成](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Serverless.Components.html#CHAP_Serverless.create)参照してください。レプリケーションインスタンスとは異なり、AWS DMS サーバーレスレプリケーションでは**パブリックアクセス可能**オプションは提供されません。

## TiDB Cloud DMSエンドポイントを作成する {#create-tidb-cloud-dms-endpoints}

接続に関しては、 TiDB Cloudクラスターをソースとして使用する場合もターゲットとして使用する場合も手順は似ていますが、DMS ではソースとターゲットでデータベース設定要件が異なります。詳細については、 [MySQLをソースとして使用する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Source.MySQL.html)または[MySQLをターゲットとして使用する](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Target.MySQL.html)を参照してください。TiDB TiDB Cloudクラスターをソースとして使用する場合、TiDB は MySQL binlogをサポートしていないため、**既存のデータの移行**のみが可能です。

1.  AWS DMS コンソールで、 [**エンドポイント**](https://console.aws.amazon.com/dms/v2/home#endpointList)ページに移動し、対応するリージョンに切り替えます。

    ![Create endpoint](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-create-endpoint.png)

2.  **エンドポイントの作成を**クリックして、ターゲット データベース エンドポイントを作成します。

3.  **[エンドポイント タイプ]**セクションで、 **[ソース エンドポイント]**または**[ターゲット エンドポイント]**を選択します。

4.  **エンドポイント設定**セクションで、**エンドポイント識別子**と ARN フィールドに入力します。次に、**ソース エンジン**または**ターゲット エンジン**として**MySQL**を選択します。

5.  **[エンドポイント データベースへのアクセス]**フィールドで、 **[アクセス情報を手動で提供する]**チェックボックスをオンにし、次のようにクラスター情報を入力します。

    <SimpleTab>

    <div label="TiDB Serverless">

    -   **サーバー名**: TiDB Serverless クラスターの`HOST` 。
    -   **ポート**: TiDB Serverless クラスターの`PORT` 。
    -   **ユーザー名**: 移行用の TiDB Serverless クラスターのユーザー。DMS 要件を満たしていることを確認してください。
    -   **パスワード**: TiDB Serverless クラスター ユーザーのパスワード。
    -   **セキュリティ Socket Layer (SSL) モード**: パブリック エンドポイント経由で接続する場合は、トランスポート セキュリティを確保するために、モードを**verify-full に**設定することを強くお勧めします。プライベート エンドポイント経由で接続する場合は、モードを**none**に設定できます。
    -   (オプション) **CA 証明書**: [ISRG ルート X1 証明書](https://letsencrypt.org/certs/isrgrootx1.pem)を使用します。詳細については、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。

    </div>

    <div label="TiDB Dedicated">

    -   **サーバー名**: TiDB 専用クラスターの`HOST` 。
    -   **ポート**: TiDB 専用クラスターの`PORT` 。
    -   **ユーザー名**: 移行用の TiDB 専用クラスターのユーザー。DMS 要件を満たしていることを確認してください。
    -   **パスワード**: TiDB 専用クラスター ユーザーのパスワード。
    -   **セキュリティ Socket Layer (SSL) モード**: パブリック エンドポイント経由で接続する場合は、トランスポート セキュリティを確保するために、モードを**verify-full に**設定することを強くお勧めします。プライベート エンドポイント経由で接続する場合は、 **none**に設定できます。
    -   (オプション) **CA 証明書**: [TiDB専用へのTLS接続](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)に従って CA 証明書を取得します。

    </div>
     </SimpleTab>

    ![Provide access information manually](/media/tidb-cloud/aws-dms-tidb-cloud/aws-dms-connect-configure-endpoint.png)

6.  エンドポイントを**ターゲット エンドポイント**として作成する場合は、**エンドポイント設定**セクションを展開し、**エンドポイント接続属性を使用する**チェックボックスをオンにして、**追加の接続属性を**`Initstmt=SET FOREIGN_KEY_CHECKS=0;`に設定します。

7.  必要に応じて、 **KMS キー**と**タグの**セクションを構成します。**エンドポイントの作成を**クリックして、インスタンスの作成を完了します。
