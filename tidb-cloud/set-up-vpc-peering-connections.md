---
title: Set Up VPC Peering Connections
summary: Learn how to set up VPC peering connections.
---

# VPC ピアリング接続のセットアップ {#set-up-vpc-peering-connections}

アプリケーションをTiDB Cloudに接続するには、TiDB TiDB Cloudで[VPC ピアリング](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)をセットアップする必要があります。 [TiDB クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)の 1 ステップです。このドキュメントでは、VPC ピアリング接続[AWS で](#on-aws)および[GCP 上](#on-gcp)の設定について説明します。

VPC ピアリング接続は、プライベート IP アドレスを使用してそれらの間でトラフィックをルーティングできるようにする 2 つの VPC 間のネットワーク接続です。どちらの VPC のインスタンスも、同じネットワーク内にあるかのように相互に通信できます。

現在、 TiDB Cloudは、同じプロジェクトの同じリージョンでの VPC ピアリングのみをサポートしています。同じリージョン内の同じプロジェクトの TiDB クラスターは、同じ VPC に作成されます。したがって、VPC ピアリングがプロジェクトのリージョンで設定されると、このプロジェクトの同じリージョンで作成されたすべての TiDB クラスターを VPC で接続できます。 VPC ピアリングのセットアップは、クラウド プロバイダーによって異なります。

## 前提条件: プロジェクト CIDR を設定する {#prerequisite-set-a-project-cidr}

Project CIDR (Classless Inter-Domain Routing) は、プロジェクト内のネットワーク ピアリングに使用される CIDR ブロックです。

VPC ピアリング リクエストをリージョンに追加する前に、プロジェクトのクラウド プロバイダー (AWS または GCP) のプロジェクト CIDR を設定して、アプリケーションの VPC へのピアリング リンクを確立する必要があります。

プロジェクトの最初の Dedicated Tier を作成するときに、プロジェクトの CIDR を設定できます。層を作成する前にプロジェクト CIDR を設定する場合は、次の操作を実行します。

1.  TiDB Cloudコンソールで、ターゲット プロジェクトを選択し、[**プロジェクト設定**] タブをクリックします。

2.  左ペインで、 **Project CIDR**をクリックします。

3.  クラウド プロバイダに応じて [ **AWS のプロジェクト CIDR を**<strong>追加] または [Google Cloud のプロジェクト CIDR を追加</strong>] をクリックし、[<strong>プロジェクト CIDR</strong> ] フィールドに次のいずれかのネットワーク アドレスを指定して、[<strong>確認</strong>] をクリックします。

    > **ノート：**
    >
    > プロジェクトの CIDR を設定するときは、アプリケーションが配置されている VPC の CIDR と競合しないようにしてください。

    -   10.250.0.0/16
    -   10.250.0.0/17
    -   10.250.128.0/17
    -   172.30.0.0/16
    -   172.30.0.0/17
    -   172.30.128.0/17

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

4.  クラウド プロバイダーと特定のリージョンの CIDR をビューします。

    リージョン CIDR は、デフォルトでは非アクティブです。リージョン CIDR を有効にするには、ターゲット リージョンにクラスタを作成する必要があります。リージョン CIDR がアクティブな場合、リージョンの VPC ピアリングを作成できます。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## AWS で {#on-aws}

### ステップ 1: VPC ピアリング リクエストを追加する {#step-1-add-vpc-peering-requests}

1.  TiDB Cloudコンソールで、VPC ピアリングのターゲット プロジェクトを選択し、[**プロジェクト設定**] タブをクリックします。

    デフォルトでは、 **VPC ピアリング**構成が表示されます。

2.  [**追加**] をクリックし、AWS アイコンを選択してから、既存の AWS VPC の必要な情報を入力します。

    -   リージョン
    -   AWS アカウント ID
    -   VPC ID
    -   VPC CIDR

    これらの情報は、VPC ダッシュボードの VPC の詳細から取得できます。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

3.  [**初期化]**をクリックします。 [ <strong>VPC ピアリングの承認</strong>] ダイアログが表示されます。

### ステップ 2: VPC ピアリングを承認して構成する {#step-2-approve-and-configure-the-vpc-peering}

次の 2 つのオプションのいずれかを使用して、VPC ピアリング接続を承認および構成します。

-   [オプション 1: AWS CLI を使用する](#option-1-use-aws-cli)
-   [オプション 2: AWS ダッシュボードを使用する](#option-2-use-the-aws-dashboard)

#### オプション 1: AWS CLI を使用する {#option-1-use-aws-cli}

1.  AWS コマンドライン インターフェイス (AWS CLI) をインストールします。

    {{< copyable "" >}}

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2.  アカウント情報に従って AWS CLI を設定します。 AWS CLI で必要な情報を取得するには、 [AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

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

4.  次のコマンドを実行します。

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

設定が完了すると、VPC ピアリングが作成されました。 [TiDBクラスタに接続する](#step-3-connect-to-the-tidb-cluster-on-tidb-cloud)で結果を確認できます。

#### オプション 2: AWS ダッシュボードを使用する {#option-2-use-the-aws-dashboard}

AWS ダッシュボードを使用して、VPC ピアリング接続を構成することもできます。

1.  AWS コンソールでピア接続リクエストを受け入れることを確認します。

    1.  AWS コンソールにサインインし、上部のメニュー バーで [**サービス**] をクリックします。検索ボックスに`VPC`と入力し、VPC サービス ページに移動します。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2.  左側のナビゲーション バーから、[**ピアリング接続]**ページを開きます。 [<strong>ピアリング接続の作成</strong>] タブで、ピアリング接続は<strong>[承認待ち</strong>] ステータスになっています。

    3.  リクエスタの所有者がTiDB Cloud ( `380838443567` ) であることを確認します。ピアリング接続を右クリックし、[**要求**を受け入れる] をクリックして要求を受け入れます。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2.  VPC サブネット ルート テーブルごとに、 TiDB Cloud VPC へのルートを追加します。

    1.  左側のナビゲーション バーから、[**ルート テーブル]**ページを開きます。

    2.  アプリケーション VPC に属するすべてのルート テーブルを検索します。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3.  各ルート テーブルを編集して宛先を含むルートをプロジェクト CIDR に追加し、[**ターゲット**] 列でピアリング ID を選択します。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3.  VPC のプライベート DNS ホスト ゾーン サポートが有効になっていることを確認します。

    1.  左側のナビゲーション バーから、[ **Your VPCs]**ページを開きます。

    2.  アプリケーション VPC を選択します。

    3.  選択した VPC を右クリックします。設定ドロップダウン リストが表示されます。

    4.  設定ドロップダウン リストから、[ **DNS ホスト名の編集**] をクリックします。 DNS ホスト名を有効にして、[<strong>保存</strong>] をクリックします。

    5.  設定ドロップダウン リストから、[ **DNS 解決の編集**] をクリックします。 DNS 解決を有効にして、[<strong>保存</strong>] をクリックします。

### ステップ 3: TiDB Cloud上の TiDBクラスタに接続する {#step-3-connect-to-the-tidb-cluster-on-tidb-cloud}

1.  [**アクティブなクラスター]**ページに移動します。

2.  ターゲットクラスタの領域を見つけて、領域の右上隅にある [**接続**] をクリックします。接続ダイアログが表示されます。 VPC ピアリングの<strong>Status</strong>が<strong>active</strong>であることを確認できます。

    > **ヒント：**
    >
    > または、[**アクティブなクラスター**] ページでターゲットクラスタの名前をクリックし、右上隅にある [<strong>接続</strong>] をクリックすることもできます。

3.  VPC 内のインスタンスから TiDB クラスターにアクセスします。 [TiDB クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md)を参照してください。

## GCP 上 {#on-gcp}

### 手順 {#steps}

1.  TiDB Cloudコンソールで、VPC ピアリングのターゲット プロジェクトを選択し、[**プロジェクト設定**] タブをクリックします。

    デフォルトでは、 **VPC ピアリング**構成が表示されます。

2.  [**追加**] をクリックし、Google Cloud アイコンを選択して、既存の GCP VPC の必要な情報を入力します。

    -   リージョン
    -   アプリケーション GCP プロジェクト ID
    -   VPC ネットワーク名
    -   VPC CIDR

3.  [**初期化]**をクリックします。 [ <strong>VPC ピアリングの承認</strong>] ダイアログが表示されます。

4.  TiDB VPC ピアリングの接続情報を確認します。

    ![VPC-Peering](/media/tidb-cloud/VPC-Peering3.png)

5.  次のコマンドを実行して、VPC ピアリングのセットアップを完了します。

    {{< copyable "" >}}

    ```bash
    gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
    ```

    > **ノート：**
    >
    > `<your-peer-name>`はお好きな名前をつけてください。
