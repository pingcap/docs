---
title: Connect to TiDB Cloud Dedicated via VPC Peering
summary: VPC ピアリング経由でTiDB Cloud Dedicated に接続する方法を学習します。
---

# VPC ピアリング経由でTiDB Cloud Dedicated に接続する {#connect-to-tidb-cloud-dedicated-via-vpc-peering}

> **注記：**
>
> VPCピアリング接続は、AWSおよびGoogle CloudでホストされているTiDB Cloud Dedicatedクラスターでのみ利用可能です。Azureでホストされている[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターおよび[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターにはVPCピアリングを使用して接続することはできません。

アプリケーションをVPCピアリング経由でTiDB Cloudに接続するには、 TiDB Cloudで[VPCピアリング](/tidb-cloud/tidb-cloud-glossary.md#vpc-peering)設定する必要があります。このドキュメントでは、VPCピアリング接続[AWS上](#set-up-vpc-peering-on-aws)と[Google Cloudで](#set-up-vpc-peering-on-google-cloud)設定と、VPCピアリング経由でTiDB Cloudに接続する手順を説明します。

VPCピアリング接続は、2つのVPC間のネットワーク接続であり、プライベートIPアドレスを使用してトラフィックをルーティングできます。どちらのVPC内のインスタンスも、同じネットワーク内にあるかのように相互に通信できます。

現在、同一リージョン内の同一プロジェクトのTiDBクラスターは同じVPC内に作成されます。そのため、あるプロジェクトのリージョンでVPCピアリングを設定すると、そのプロジェクトの同一リージョン内に作成されたすべてのTiDBクラスターをVPC内で接続できるようになります。VPCピアリングの設定はクラウドプロバイダーによって異なります。

> **ヒント：**
>
> アプリケーションをTiDB Cloudに接続するには、 TiDB Cloudで[プライベートエンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)設定することもできます。これは安全でプライベートであり、データがパブリックインターネットに公開されることはありません。VPCピアリング接続ではなく、プライベートエンドポイントを使用することをお勧めします。

## 前提条件: リージョンの CIDR を設定する {#prerequisite-set-a-cidr-for-a-region}

CIDR (Classless Inter-Domain Routing) は、 TiDB Cloud Dedicated クラスターの VPC を作成するために使用される CIDR ブロックです。

VPCピアリングリクエストをリージョンに追加するには、そのリージョンのCIDRを設定し、そのリージョンに最初のTiDB Cloud専用クラスターを作成する必要があります。最初の専用クラスターが作成されると、 TiDB CloudはクラスターのVPCを作成し、アプリケーションのVPCへのピアリングリンクを確立できるようになります。

最初のTiDB Cloud Dedicatedクラスタを作成する際にCIDRを設定できます。クラスタを作成する前にCIDRを設定する場合は、以下の操作を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象のプロジェクトに切り替えて、 **[プロジェクト設定] を**クリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「プロジェクト CIDR」**タブをクリックして、クラウド プロバイダーに応じて**AWS**または**Google Cloud**を選択します。

4.  右上隅の**「CIDR の作成」を**クリックします。 **「AWS CIDR の作成」**または**「Google Cloud CIDR の作成」**ダイアログでリージョンと CIDR 値を指定し、 **「確認」**をクリックします。

    ![Project-CIDR4](/media/tidb-cloud/Project-CIDR4.png)

    > **注記：**
    >
    > -   アプリケーションが配置されている VPC の CIDR との競合を避けるには、このフィールドに別のプロジェクト CIDR を設定する必要があります。
    > -   AWSリージョンの場合、IP範囲のサイズを`/16` ～ `/23`に設定することをお勧めします。サポートされているネットワークアドレスは次のとおりです。
    >     -   10.250.0.0 - 10.251.255.255
    >     -   172.16.0.0 - 172.31.255.255
    >     -   192.168.0.0 - 192.168.255.255
    > -   Google Cloudリージョンの場合、IPアドレス範囲のサイズを`/19` ～ `/20`範囲で設定することを推奨します。IPアドレス範囲のサイズを`/16` ～ `/18`範囲で設定したい場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。サポートされているネットワークアドレスは次のとおりです。
    >     -   10.250.0.0 - 10.251.255.255
    >     -   172.16.0.0 - 172.17.255.255
    >     -   172.30.0.0 - 172.31.255.255
    > -   TiDB Cloud は、リージョンの CIDR ブロック サイズに基づいて、プロジェクトのリージョン内のTiDB Cloudノードの数を制限します。

5.  クラウド プロバイダーと特定のリージョンの CIDR をビュー。

    CIDRはデフォルトで無効になっています。CIDRを有効にするには、ターゲットリージョンにクラスターを作成する必要があります。リージョンのCIDRが有効な場合は、そのリージョンにVPCピアリングを作成できます。

    ![Project-CIDR2](/media/tidb-cloud/Project-CIDR2.png)

## AWS で VPC ピアリングを設定する {#set-up-vpc-peering-on-aws}

このセクションでは、AWS で VPC ピアリング接続を設定する方法について説明します。Google Cloud については、 [Google Cloud で VPC ピアリングを設定する](#set-up-vpc-peering-on-google-cloud)ご覧ください。

### ステップ1. VPCピアリングリクエストを追加する {#step-1-add-vpc-peering-requests}

VPC ピアリング リクエストは、 TiDB Cloudコンソールのプロジェクト レベルの [**ネットワーク アクセス]**ページまたはクラスタ レベルの**[ネットワーキング]**ページのいずれかで追加できます。

<SimpleTab>
<div label="VPC peering setting on the project-level Network Access page">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象のプロジェクトに切り替えて、 **[プロジェクト設定] を**クリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「VPC ピアリング」** &gt; **「AWS」**タブをクリックします。

    **VPC ピアリング**構成はデフォルトで表示されます。

4.  右上隅で**[VPC ピアリングの作成] を**クリックし、 **[TiDB Cloud VPCリージョン]**を選択して、既存の AWS VPC の必要な情報を入力します。

    -   VPCリージョン
    -   AWSアカウントID
    -   VPC ID
    -   VPC CIDR

    このような情報は、 [AWS マネジメントコンソール](https://console.aws.amazon.com/)の VPC 詳細ページから取得できます。TiDB TiDB Cloud は、同じリージョン内または 2 つの異なるリージョンの VPC 間における VPC ピアリングの作成をサポートしています。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

5.  **「作成」**をクリックしてVPCピアリングリクエストを送信し、 **「VPCピアリング」** &gt; **「AWS」**タブでVPCピアリング情報を確認します。新しく作成されたVPCピアリングのステータスは**「システムチェック中」**です。

6.  新しく作成したVPCピアリングの詳細情報を表示するには、 **「アクション」**列の**「...** 」&gt; **「ビュー」を**クリックします。 **「VPCピアリングの詳細」**ページが表示されます。

</div>
<div label="VPC peering setting on the cluster-level Networking page">

1.  ターゲット クラスターの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックすると、概要ページに移動します。

2.  左側のナビゲーション ペインで**[Networking]**をクリックし、 **[Create VPC Peering] を**クリックします。

3.  既存の AWS VPC の必須情報を入力します。

    -   VPCリージョン
    -   AWSアカウントID
    -   VPC ID
    -   VPC CIDR

    このような情報は、 [AWS マネジメントコンソール](https://console.aws.amazon.com/)の VPC 詳細ページから取得できます。TiDB TiDB Cloud は、同じリージョン内または 2 つの異なるリージョンの VPC 間における VPC ピアリングの作成をサポートしています。

    ![VPC peering](/media/tidb-cloud/vpc-peering/vpc-peering-creating-infos.png)

4.  **「作成」**をクリックしてVPCピアリングリクエストを送信し、 **「ネットワーク」** &gt; **「AWS VPCピアリング」**セクションでVPCピアリング情報を確認します。新しく作成されたVPCピアリングのステータスは**「システムチェック中」**です。

5.  新しく作成したVPCピアリングの詳細情報を表示するには、 **「アクション」**列の**「...** 」&gt; **「ビュー」**をクリックします。AWS **VPCピアリングの詳細**ページが表示されます。

</div>
</SimpleTab>

### ステップ2. VPCピアリングを承認して設定する {#step-2-approve-and-configure-the-vpc-peering}

AWS CLI または AWS ダッシュボードを使用して、VPC ピアリング接続を承認および設定できます。

<SimpleTab>
<div label="Use AWS CLI">

1.  AWS コマンドラインインターフェイス (AWS CLI) をインストールします。

    ```bash
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    sudo ./aws/install
    ```

2.  アカウント情報に応じてAWS CLIを設定してください。AWS CLIに必要な情報を取得するには、 [AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。

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
    > ルートテーブルルールが正常に作成されたにもかかわらず、エラー`An error occurred (MissingParameter) when calling the CreateRoute operation: The request must contain the parameter routeTableId`発生する場合があります。その場合は、作成されたルールを確認し、エラーを無視してください。

    ```bash
    # Modifies the VPC attribute to enable DNS-hostname and DNS-support.
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-hostnames
    aws ec2 modify-vpc-attribute --vpc-id "$app_vpc_id" --enable-dns-support
    ```

設定が完了すると、VPCピアリングが作成されます。1 [TiDBクラスタに接続する](#connect-to-the-tidb-cluster)結果を確認できます。

</div>
<div label="Use the AWS dashboard">

AWS ダッシュボードを使用して VPC ピアリング接続を構成することもできます。

1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)でピア接続要求を受け入れることを確認します。

    1.  [AWS マネジメントコンソール](https://console.aws.amazon.com/)にサインインし、上部のメニューバーで**「サービス」を**クリックします。検索ボックスに`VPC`と入力して、VPC サービスページに移動します。

        ![AWS dashboard](/media/tidb-cloud/vpc-peering/aws-vpc-guide-1.jpg)

    2.  左側のナビゲーションバーから**「ピアリング接続」**ページを開きます。 **「ピアリング接続の作成」**タブで、ピアリング接続のステータスが「**承認保留中**」になっていることを確認します。

    3.  [TiDB Cloudコンソール](https://tidbcloud.com)の**VPC ピアリングの詳細**ページで、リクエスターの所有者とリクエスターVPC が**TiDB Cloud AWS アカウント ID**と**TiDB Cloud VPC ID**と一致していることを確認します。ピアリング接続を右クリックし、[リクエストの**承認]**を選択して、 **[VPC ピアリング接続リクエストの承認]**ダイアログでリクエストを承認します。

        ![AWS VPC peering requests](/media/tidb-cloud/vpc-peering/aws-vpc-guide-3.png)

2.  各 VPC サブネット ルート テーブルに対して、 TiDB Cloud VPC へのルートを追加します。

    1.  左側のナビゲーション バーから、**ルート テーブル**ページを開きます。

    2.  アプリケーション VPC に属するすべてのルートテーブルを検索します。

        ![Search all route tables related to VPC](/media/tidb-cloud/vpc-peering/aws-vpc-guide-4.png)

    3.  各ルートテーブルを右クリックし、 **「ルートの編集」**を選択します。編集ページで、 TiDB Cloud CIDR への宛先を持つルートを追加し（ TiDB Cloudコンソールの**VPC ピアリング**設定ページで確認）、**ターゲット**列にピアリング接続 ID を入力します。

        ![Edit all route tables](/media/tidb-cloud/vpc-peering/aws-vpc-guide-5.png)

3.  VPC でプライベート DNS ホストゾーンのサポートが有効になっていることを確認してください。

    1.  左側のナビゲーション バーから、 **[Your VPCs]**ページを開きます。

    2.  アプリケーション VPC を選択します。

    3.  選択したVPCを右クリックします。設定ドロップダウンリストが表示されます。

    4.  設定ドロップダウンリストから**「DNSホスト名の編集」を**クリックします。DNSホスト名を有効にして**「保存」**をクリックします。

    5.  設定ドロップダウンリストから**「DNS解決の編集」を**クリックします。DNS解決を有効にして**「保存」**をクリックします。

これでVPCピアリング接続の設定が完了しました。次に、 [VPCピアリング経由でTiDBクラスターに接続する](#connect-to-the-tidb-cluster) .

</div>
</SimpleTab>

## Google Cloud で VPC ピアリングを設定する {#set-up-vpc-peering-on-google-cloud}

### ステップ1. VPCピアリングリクエストを追加する {#step-1-add-vpc-peering-requests}

VPC ピアリング リクエストは、 TiDB Cloudコンソールのプロジェクト レベルの [**ネットワーク アクセス]**ページまたはクラスタ レベルの**[ネットワーキング]**ページのいずれかで追加できます。

<SimpleTab>
<div label="VPC peering setting on the project-level Network Access page">

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。

2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象のプロジェクトに切り替えて、 **[プロジェクト設定] を**クリックします。</mdsvgicon>

3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「VPC ピアリング」** &gt; **「Google Cloud」**タブをクリックします。

    **VPC ピアリング**構成はデフォルトで表示されます。

4.  右上隅で**[VPC ピアリングを作成]**をクリックし、 **[TiDB Cloud VPCリージョン]**を選択して、既存の Google Cloud VPC の必要な情報を入力します。

    > **ヒント：**
    >
    > **Google Cloud プロジェクト ID**と**VPC ネットワーク名**フィールドの横にある指示に従って、プロジェクト ID と VPC ネットワーク名を見つけることができます。

    -   Google Cloud プロジェクト ID
    -   VPC ネットワーク名
    -   VPC CIDR

5.  **「作成」**をクリックしてVPCピアリングリクエストを送信し、 **「VPCピアリング」** &gt; **「Google Cloud」**タブでVPCピアリング情報を確認します。新しく作成されたVPCピアリングのステータスは**「システムチェック中」**です。

6.  新しく作成したVPCピアリングの詳細情報を表示するには、 **「アクション」**列の**「...** 」&gt; **「ビュー」を**クリックします。 **「VPCピアリングの詳細」**ページが表示されます。

</div>
<div label="VPC peering setting on the cluster-level Networking page">

1.  ターゲット クラスターの概要ページを開きます。

    1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

        > **ヒント：**
        >
        > 複数のプロジェクトがある場合は、<mdsvgicon name="icon-left-projects">左下隅にある をクリックして、別のプロジェクトに切り替えます。</mdsvgicon>

    2.  ターゲット クラスターの名前をクリックすると、概要ページに移動します。

2.  左側のナビゲーション ペインで**[Networking]**をクリックし、 **[Create VPC Peering] を**クリックします。

3.  既存の Google Cloud VPC の必須情報を入力します。

    > **ヒント：**
    >
    > **Google Cloud プロジェクト ID**と**VPC ネットワーク名**フィールドの横にある指示に従って、プロジェクト ID と VPC ネットワーク名を見つけることができます。

    -   Google Cloud プロジェクト ID
    -   VPC ネットワーク名
    -   VPC CIDR

4.  **「作成」**をクリックしてVPCピアリングリクエストを送信し、 **「ネットワーク」** &gt; **「Google Cloud VPCピアリング」**セクションでVPCピアリング情報を確認します。新しく作成されたVPCピアリングのステータスは**「システムチェック中」**です。

5.  新しく作成したVPCピアリングの詳細情報を表示するには、 **「アクション」**列の**「...** 」&gt; **「ビュー」**をクリックします。Google **Cloud VPCピアリングの詳細**ページが表示されます。

</div>
</SimpleTab>

### ステップ2. VPCピアリングを承認する {#step-2-approve-the-vpc-peering}

次のコマンドを実行して、VPC ピアリングのセットアップを完了します。

```bash
gcloud beta compute networks peerings create <your-peer-name> --project <your-project-id> --network <your-vpc-network-name> --peer-project <tidb-project-id> --peer-network <tidb-vpc-network-name>
```

> **注記：**
>
> `<your-peer-name>`お好きな名前を付けることができます。

これでVPCピアリング接続の設定が完了しました。次に、 [VPCピアリング経由でTiDBクラスターに接続する](#connect-to-the-tidb-cluster) .

## TiDBクラスタに接続する {#connect-to-the-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。

2.  右上隅の**[接続]**をクリックし、 **[接続タイプ]**ドロップダウン リストから**[VPC ピアリング]**を選択します。

    VPC ピアリング接続ステータスが**システムチェック**から**アクティブ**に変わるまで待ちます (約 5 分)。

3.  **「接続方法**」ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。

4.  接続文字列を使用してクラスターに接続します。
