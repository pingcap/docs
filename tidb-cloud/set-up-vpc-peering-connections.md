---
title: Set Up VPC Peering Connections
summary: Learn how to set up VPC peering connections.
---

# VPCピアリング接続を設定する {#set-up-vpc-peering-connections}

アプリケーションをTiDB Cloudに接続するには、 TiDB Cloudで[VPCピアリング](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)を設定する必要があります。それは[TiDBクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)の1つのステップです。このドキュメントでは、VPCピアリング接続[AWSで](#on-aws)および[GCPで](#on-gcp)の設定について説明します。

VPCピアリング接続は、プライベートIPアドレスを使用して2つのVPC間でトラフィックをルーティングできるようにする2つのVPC間のネットワーク接続です。いずれかのVPC内のインスタンスは、同じネットワーク内にあるかのように相互に通信できます。

現在、 TiDB Cloudは、同じプロジェクトの同じリージョンでのVPCピアリングのみをサポートしています。同じリージョン内の同じプロジェクトのTiDBクラスターは、同じVPCで作成されます。したがって、プロジェクトのリージョンでVPCピアリングを設定すると、このプロジェクトの同じリージョンで作成されたすべてのTiDBクラスターをVPCに接続できます。 VPCピアリングの設定はクラウドプロバイダーによって異なります。

## 前提条件：プロジェクトCIDRを設定する {#prerequisite-set-a-project-cidr}

プロジェクトCIDR（クラスレスドメイン間ルーティング）は、プロジェクトのネットワークピアリングに使用されるCIDRブロックです。

VPCピアリングリクエストをリージョンに追加する前に、プロジェクトのクラウドプロバイダー（AWSまたはGCP）のプロジェクトCIDRを設定して、アプリケーションのVPCへのピアリングリンクを確立する必要があります。

プロジェクトの最初の専用層を作成するときに、プロジェクトCIDRを設定できます。層を作成する前にプロジェクトCIDRを設定する場合は、次の操作を実行します。

1.  TiDB Cloudコンソールで、ターゲットプロジェクトを選択し、[**プロジェクト設定**]タブをクリックします。

2.  左側のペインで、[**プロジェクトCIDR** ]をクリックします。

3.  クラウドプロバイダーに応じて[ **AWSのプロジェクトCIDRを**<strong>追加</strong>]または[GoogleCloudのプロジェクトCIDRを追加]をクリックし、[<strong>プロジェクトCIDR</strong> ]フィールドに次のネットワークアドレスのいずれかを指定して、[<strong>確認</strong>]をクリックします。

    > **ノート：**
    >
    > プロジェクトのCIDRを設定するときは、アプリケーションが配置されているVPCのCIDRとの競合を回避してください。

    -   10.250.0.0/16
    -   10.250.0.0/17
    -   10.250.128.0 / 17
    -   172.30.0.0/16
    -   172.30.0.0 / 17
    -   172.30.128.0 / 17

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

4.  クラウドプロバイダーと特定の地域のCIDRをビューします。

    リージョンCIDRはデフォルトで非アクティブです。リージョンCIDRをアクティブ化するには、ターゲットリージョンにクラスタを作成する必要があります。リージョンCIDRがアクティブな場合、リージョンのVPCピアリングを作成できます。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## AWSの場合 {#on-aws}

### ステップ1：VPCピアリングリクエストを追加する {#step-1-add-vpc-peering-requests}

1.  TiDB Cloudコンソールで、VPCピアリングのターゲットプロジェクトを選択し、[**プロジェクト設定**]タブをクリックします。

    デフォルトでは、 **VPCピアリング**設定が表示されます。

2.  [**追加**]をクリックし、AWSアイコンを選択してから、既存のAWSVPCに必要な情報を入力します。

    -   領域
    -   AWSアカウントID
    -   VPC ID
    -   VPC CIDR

    これらの情報は、VPCダッシュボードのVPCの詳細から取得できます。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

3.  [**初期化]**をクリックします。 [ <strong>VPCPeeringsの承認</strong>]ダイアログが表示されます。

### ステップ2：VPCピアリングを承認および構成する {#step-2-approve-and-configure-the-vpc-peering}

次の2つのオプションのいずれかを使用して、VPCピアリング接続を承認および構成します。

-   [オプション1：AWSCLIを使用する](#option-1-use-aws-cli)
-   [オプション2：AWSダッシュボードを使用する](#option-2-use-the-aws-dashboard)

#### オプション1：AWSCLIを使用する {#option-1-use-aws-cli}

1.  AWSコマンドラインインターフェイス（AWS CLI）をインストールします。

    {{< copyable "" >}}

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2.  アカウント情報に従ってAWSCLIを設定します。 AWS CLIに必要な情報を取得するには、 [AWSCLI設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

    {{< copyable "" >}}

    ```bash
    aws configure
    ```

3.  次の変数値をアカウント情報に置き換えます。

    {{< copyable "" >}}

    ```bash
    # Sets up the related variables.
    pcx_tidb_to_app_id="<TiDB peering id>"
    app_region="<APP Region>"
    app_vpc_id="<Your VPC ID>"
    tidbcloud_project_cidr="<TiDB Cloud Project VPC CIDR>"
    ```

    例えば：

    ```
    # Set up the related variables
    pcx_tidb_to_app_id="pcx-069f41efddcff66c8"
    app_region="us-west-2"
    app_vpc_id="vpc-0039fb90bb5cf8698"
    tidbcloud_project_cidr="10.250.0.0/16"
    ```

4.  以下のコマンドを実行してください。

    {{< copyable "" >}}

    ```bash
    # Accepts the VPC peering connection request.
    aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    ```

    {{< copyable "" >}}

    ```bash
    # Creates route table rules.
    aws ec2 describe-route-tables --region "$app_region" --filters Name=vpc-id,Values="$app_vpc_id" --query 'RouteTables[*].RouteTableId' --output text | xargs -n 1 |  while read row
    do
        app_route_table_id="$row"
        aws ec2 create-route --route-table-id "$app_route_table_id" --destination-cidr-block "$tidbcloud_project_cidr" --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    done
    ```

    {{< copyable "" >}}

    ```bash
    # Modifies the VPC attribute to enable DNS-hostname and DNS-support.
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

設定が完了すると、VPCピアリングが作成されます。 [TiDBクラスタに接続します](#step-3-connect-to-the-tidb-cluster-on-tidb-cloud)で結果を確認できます。

#### オプション2：AWSダッシュボードを使用する {#option-2-use-the-aws-dashboard}

AWSダッシュボードを使用して、VPCピアリング接続を設定することもできます。

1.  AWSコンソールでピア接続リクエストを受け入れることを確認します。

    1.  AWSコンソールにサインインし、上部のメニューバーの[**サービス**]をクリックします。検索ボックスに`VPC`と入力し、VPCサービスページに移動します。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2.  左側のナビゲーションバーから、[**ピアリング接続]**ページを開きます。 [<strong>ピアリング接続の作成</strong>]タブで、ピアリング接続は<strong>[保留中の承認</strong>]ステータスになっています。

    3.  リクエスターの所有者がTiDB Cloud （ `380838443567` ）であることを確認します。ピアリング接続を右クリックし、[リクエストの承認]をクリックして**リクエスト**を承認します。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2.  各VPCサブネットルートテーブルのTiDB CloudVPCへのルートを追加します。

    1.  左側のナビゲーションバーから、[**ルートテーブル]**ページを開きます。

    2.  アプリケーションVPCに属するすべてのルートテーブルを検索します。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3.  各ルートテーブルを編集して、宛先を含むルートをプロジェクトCIDRに追加し、[**ターゲット**]列でピアリングIDを選択します。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3.  VPCに対してプライベートDNSホストゾーンのサポートが有効になっていることを確認してください。

    1.  左側のナビゲーションバーから、[ **VPC]**ページを開きます。

    2.  アプリケーションのVPCを選択します。

    3.  選択したVPCを右クリックします。設定ドロップダウンリストが表示されます。

    4.  [設定]ドロップダウンリストから、[ **DNSホスト名の編集**]をクリックします。 DNSホスト名を有効にして、[<strong>保存</strong>]をクリックします。

    5.  [設定]ドロップダウンリストから、[ **DNS解決の編集**]をクリックします。 DNS解決を有効にして、[<strong>保存</strong>]をクリックします。

### ステップ3： TiDB Cloud上のTiDBクラスタに接続する {#step-3-connect-to-the-tidb-cluster-on-tidb-cloud}

1.  [**アクティブクラスター**]ページに移動し、クラスタの名前をクリックします。

2.  [**接続]**をクリックします。 [ <strong>TiDBに接続</strong>]ダイアログが表示されます。 VPCピアリングの<strong>ステータス</strong>が<strong>アクティブ</strong>であることがわかります。

3.  VPC内のインスタンスからTiDBクラスターにアクセスします。 [TiDBクラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

## GCPの場合 {#on-gcp}

### 手順 {#steps}

1.  TiDB Cloudコンソールで、VPCピアリングのターゲットプロジェクトを選択し、[**プロジェクト設定**]タブをクリックします。

    デフォルトでは、 **VPCピアリング**設定が表示されます。

2.  [**追加**]をクリックし、Google Cloudアイコンを選択して、既存のGCPVPCに必要な情報を入力します。

    -   領域
    -   アプリケーションGCPプロジェクトID
    -   VPCネットワーク名
    -   VPC CIDR

3.  [**初期化]**をクリックします。 [ <strong>VPCPeeringsの承認</strong>]ダイアログが表示されます。

4.  TiDBVPCピアリングの接続情報を確認してください。

    ![VPC-Peering](/media/tidb-cloud/VPC-Peering3.png)

5.  次のコマンドを実行して、VPCピアリングのセットアップを完了します。

    {{< copyable "" >}}

    ```bash
    gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
    ```

    > **ノート：**
    >
    > 好きなように`<your-peer-name>`に名前を付けることができます。
