---
title: Connect to TiDB Dedicated via VPC Peering
summary: Learn how to connect to TiDB Dedicated via VPC peering.
---

# VPC ピアリング経由で TiDB Dedicated に接続する {#connect-to-tidb-dedicated-via-vpc-peering}

> **注記：**
>
> VPC ピアリング接続は TiDB 専用クラスターでのみ使用できます。VPC ピアリングを使用して[TiDB サーバーレス クラスター](/tidb-cloud/select-cluster-tier.md#tidb-serverless)に接続することはできません。

VPC ピアリング経由でアプリケーションをTiDB Cloudに接続するには、 TiDB Cloudで[VPC ピアリング](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)設定する必要があります。このドキュメントでは、VPC ピアリング接続[AWSで](#set-up-vpc-peering-on-aws)と[Google Cloudで](#set-up-vpc-peering-on-google-cloud)を設定し、VPC ピアリング経由でTiDB Cloudに接続する手順を説明します。

VPC ピアリング接続は、2 つの VPC 間のネットワーク接続であり、プライベート IP アドレスを使用してそれらの間でトラフィックをルーティングできます。どちらの VPC 内のインスタンスも、同じネットワーク内にあるかのように相互に通信できます。

現在、同じリージョン内の同じプロジェクトの TiDB クラスターは同じ VPC 内に作成されます。したがって、プロジェクトのリージョンで VPC ピアリングを設定すると、このプロジェクトの同じリージョンで作成されたすべての TiDB クラスターを VPC 内で接続できます。VPC ピアリングの設定は、クラウド プロバイダーによって異なります。

> **ヒント：**
>
> アプリケーションをTiDB Cloudに接続するには、安全でプライベートであり、データがパブリック インターネットに公開されないTiDB Cloudで[プライベートエンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)設定することもできます。VPC ピアリング接続よりもプライベート エンドポイントを使用することをお勧めします。

## 前提条件: リージョンのCIDRを設定する {#prerequisite-set-a-cidr-for-a-region}

CIDR (Classless Inter-Domain Routing) は、TiDB 専用クラスターの VPC を作成するために使用される CIDR ブロックです。

VPC ピアリング リクエストをリージョンに追加する前に、そのリージョンの CIDR を設定し、そのリージョンに最初の TiDB 専用クラスターを作成する必要があります。最初の専用クラスターが作成されると、 TiDB Cloudによってクラスターの VPC が作成され、アプリケーションの VPC へのピアリング リンクを確立できるようになります。

最初の TiDB 専用クラスターを作成するときに CIDR を設定できます。クラスターを作成する前に CIDR を設定する場合は、次の操作を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「プロジェクト CIDR」**タブをクリックします。

4.  **[Create CIDR]**をクリックし、クラウド プロバイダーに応じて [ **AWS CIDR]**または**[Google Cloud CIDR]**をクリックします。 **[Create AWS CIDR]**または**[Create Google Cloud CIDR]**ウィンドウでリージョンと CIDR 値を指定し、 **[Confirm]**をクリックします。

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

    > **注記：**
    >
    > -   アプリケーションが配置されている VPC の CIDR との競合を避けるには、このフィールドに別のプロジェクト CIDR を設定する必要があります。
    > -   AWSリージョンの場合、 IP 範囲のサイズを`/16` ～ `/23`に設定することをお勧めします。サポートされているネットワーク アドレスは次のとおりです。
    >     -   10.250.0.0 - 10.251.255.255
    >     -   172.16.0.0 - 172.31.255.255
    >     -   192.168.0.0 - 192.168.255.255

    > -   Google Cloudリージョンの場合、 IP 範囲のサイズを`/19`から`/20`の間で設定することをお勧めします。 IP 範囲のサイズを`/16`から`/18`の間で設定する場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。 サポートされているネットワーク アドレスは次のとおりです。
    >     -   10.250.0.0 - 10.251.255.255
    >     -   172.16.0.0 - 172.17.255.255
    >     -   172.30.0.0 - 172.31.255.255

    > -   TiDB Cloud は、リージョンの CIDR ブロック サイズに基づいて、プロジェクトのリージョン内のTiDB Cloudノードの数を制限します。

5.  クラウド プロバイダーと特定のリージョンの CIDRをビュー。

    CIDR はデフォルトでは非アクティブです。CIDR をアクティブにするには、ターゲット リージョンにクラスターを作成する必要があります。リージョンの CIDR がアクティブな場合は、リージョンの VPC ピアリングを作成できます。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## AWS で VPC ピアリングを設定する {#set-up-vpc-peering-on-aws}

このセクションでは、AWS で VPC ピアリング接続を設定する方法について説明します。Google Cloud については、 [Google Cloud で VPC ピアリングを設定する](#set-up-vpc-peering-on-google-cloud)を参照してください。

### ステップ1. VPCピアリングリクエストを追加する {#step-1-add-vpc-peering-requests}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「VPC ピアリング」**タブをクリックします。

    **VPC ピアリング**構成はデフォルトで表示されます。

4.  **[追加] を**クリックし、AWS アイコンを選択して、 **TiDB Cloud VPCリージョン**を選択し、既存の AWS VPC の必要な情報を入力します。

    -   既存のVPCリージョン
    -   AWS アカウント ID
    -   VPCID
    -   VPC CIDR

    これらの情報は、VPC ダッシュボードの VPC の詳細から取得できます。TiDB TiDB Cloud は、同じリージョン内または 2 つの異なるリージョンの VPC 間の VPC ピアリングの作成をサポートしています。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

5.  **「初期化」**をクリックします。 **「VPC ピアリングの承認」**ダイアログが表示されます。

### ステップ2. VPCピアリングを承認して構成する {#step-2-approve-and-configure-the-vpc-peering}

VPC ピアリング接続を承認および構成するには、次の 2 つのオプションのいずれかを使用します。

-   [オプション 1: AWS CLI を使用する](#option-1-use-aws-cli)
-   [オプション2: AWSダッシュボードを使用する](#option-2-use-the-aws-dashboard)

#### オプション 1. AWS CLI を使用する {#option-1-use-aws-cli}

1.  AWS コマンドラインインターフェイス (AWS CLI) をインストールします。

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2.  アカウント情報に応じて AWS CLI を設定します。AWS CLI に必要な情報を取得するには、 [AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。

    ```bash
    aws configure
    ```

3.  次の変数値をアカウント情報に置き換えます。

    ```bash
    # Sets up the related variables.
    pcx_tidb_to_app_id="<TiDB peering id>"
    app_region="<APP Region>"
    app_vpc_id="<Your VPC ID>"
    tidbcloud_project_cidr="<TiDB Cloud Project VPC CIDR>"
    ```

    例えば：

        # Sets up the related variables
        pcx_tidb_to_app_id="pcx-069f41efddcff66c8"
        app_region="us-west-2"
        app_vpc_id="vpc-0039fb90bb5cf8698"
        tidbcloud_project_cidr="10.250.0.0/16"

4.  次のコマンドを実行します。

    ```bash
    # Accepts the VPC peering connection request.
    aws ec2 accept-vpc-peering-connection --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    ```

    ```bash
    # Creates route table rules.
    aws ec2 describe-route-tables --region "$app_region" --filters Name=vpc-id,Values="$app_vpc_id" --query 'RouteTables[*].RouteTableId' --output text | tr "\t" "\n" | while read row
    do
        app_route_table_id="$row"
        aws ec2 create-route --region "$app_region" --route-table-id "$app_route_table_id" --destination-cidr-block "$tidbcloud_project_cidr" --vpc-peering-connection-id "$pcx_tidb_to_app_id"
    done
    ```

    > **注記：**
    >
    > 場合によっては、ルート テーブル ルールが正常に作成された場合でも、エラー`An error occurred (MissingParameter) when calling the CreateRoute operation: The request must contain the parameter routeTableId`が発生することがあります。この場合、作成されたルールを確認して、エラーを無視できます。

    ```bash
    # Modifies the VPC attribute to enable DNS-hostname and DNS-support.
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

設定が完了すると、VPC ピアリングが作成されます。結果を確認するには[TiDBクラスタに接続する](#connect-to-the-tidb-cluster)実行します。

#### オプション2. AWSダッシュボードを使用する {#option-2-use-the-aws-dashboard}

AWS ダッシュボードを使用して VPC ピアリング接続を構成することもできます。

1.  AWS コンソールでピア接続リクエストを受け入れることを確認します。

    1.  AWS コンソールにサインインし、上部のメニューバーで**[サービス] を**クリックします。検索ボックスに`VPC`と入力し、VPC サービス ページに移動します。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2.  左側のナビゲーション バーから、[**ピアリング接続]**ページを開きます。 **[ピアリング接続の作成]**タブで、ピアリング接続は**[承認保留中]**ステータスになっています。

    3.  リクエスターの所有者がTiDB Cloud ( `380838443567` 、 `143458967504` 、または`730335266318` ) であることを確認します。ピアリング接続を右クリックし、 **[リクエストの承認]**を選択して、 **[VPC ピアリング接続リクエストの**承認] ダイアログでリクエストを承認します。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2.  各 VPC サブネット ルート テーブルに対して、 TiDB Cloud VPC へのルートを追加します。

    1.  左側のナビゲーション バーから、**ルート テーブル**ページを開きます。

    2.  アプリケーション VPC に属するすべてのルートテーブルを検索します。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3.  各ルート テーブルを右クリックし、 **[ルートの編集]**を選択します。編集ページで、 TiDB Cloud CIDR への宛先を持つルートを追加し ( TiDB Cloudコンソールの**VPC ピアリング**構成ページを確認して)、 **[ターゲット]**列にピアリング接続 ID を入力します。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3.  VPC のプライベート DNS ホストゾーンのサポートが有効になっていることを確認してください。

    1.  左側のナビゲーション バーから、 **[Your VPCs]**ページを開きます。

    2.  アプリケーション VPC を選択します。

    3.  選択した VPC を右クリックします。設定ドロップダウン リストが表示されます。

    4.  設定のドロップダウンリストから、 **「DNS ホスト名の編集」**をクリックします。DNS ホスト名を有効にして、 **「保存」**をクリックします。

    5.  設定のドロップダウンリストから、 **「DNS 解決の編集」**をクリックします。DNS 解決を有効にして、 **「保存」**をクリックします。

これで、VPC ピアリング接続が正常に設定されました。次に、 [VPCピアリング経由でTiDBクラスターに接続する](#connect-to-the-tidb-cluster) 。

## Google Cloud で VPC ピアリングを設定する {#set-up-vpc-peering-on-google-cloud}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「VPC ピアリング」**タブをクリックします。

    **VPC ピアリング**構成はデフォルトで表示されます。

4.  **[追加] を**クリックし、Google Cloud アイコンを選択して、 **TiDB Cloud VPCリージョン**を選択し、既存の Google Cloud VPC の必要な情報を入力します。

    > **ヒント：**
    >
    > プロジェクト ID と VPC ネットワーク名を見つけるには、 **「アプリケーションの Google Cloud プロジェクト ID」**フィールドと「VPC ネットワーク**名」**フィールドの横にある指示に従ってください。

    -   アプリケーション Google Cloud プロジェクト ID
    -   VPC ネットワーク名
    -   VPC CIDR

5.  **「初期化」**をクリックします。 **「VPC ピアリングの承認」**ダイアログが表示されます。

6.  TiDB VPC ピアリングの接続情報を確認します。

    ![VPC-Peering](/media/tidb-cloud/VPC-Peering3.png)

7.  次のコマンドを実行して、VPC ピアリングの設定を完了します。

    ```bash
    gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
    ```

    > **注記：**
    >
    > `<your-peer-name>`お好きな名前を付けることができます。

これで、VPC ピアリング接続が正常に設定されました。次に、 [VPCピアリング経由でTiDBクラスターに接続する](#connect-to-the-tidb-cluster) 。

## TiDBクラスターに接続する {#connect-to-the-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。

2.  右上隅の [**接続]**をクリックし、接続ダイアログで**[VPC ピアリング]**タブを選択します。

    VPC ピアリングの**ステータス**が**アクティブになって**いることがわかります。**ステータス**がまだ**システム チェック**中の場合は、約 5 分待ってからダイアログを再度開きます。

3.  **「エンドポイントの取得」を**クリックし、数分間待ちます。その後、接続コマンドがダイアログに表示されます。

4.  ダイアログ ボックスの**[手順 2: SQL クライアントを使用して接続する]**で、希望する接続方法のタブをクリックし、接続文字列を使用してクラスターに接続します。
