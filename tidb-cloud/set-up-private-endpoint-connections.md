---
title: Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink
summary: AWS を使用してプライベートエンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# AWS PrivateLink 経由でTiDB Cloud Dedicatedクラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-aws-privatelink}

このドキュメントでは、 [AWS PrivateLink](https://aws.amazon.com/privatelink)経由でTiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **Tip:**
>
> - AWS PrivateLink 経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。
> - Azure のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [Azure Private Link 経由でTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)を参照してください。
> - Google Cloud のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスタに接続する方法については、 [Google Cloud Private Service Connect 経由でTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)をご覧ください。

TiDB Cloudは、 AWS VPCでホストされているTiDB Cloudサービスへの、 [AWS PrivateLink](https://aws.amazon.com/privatelink)経由の高度に安全な一方向アクセスをサポートします。まるでお客様のVPC内にあるかのように機能します。VPC内にプライベートエンドポイントが公開されており、権限があればエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートであり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベートエンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

- [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

- プライベートエンドポイントを作成できるのは、`Organization Owner`または`Project Owner`ロールを持つユーザーのみです。
- デフォルトでは、プライベートエンドポイントと接続先の TiDB クラスターは同じリージョンに配置されている必要があります。別のリージョンから接続するには、対象のノードグループにそのリージョンを許可します。詳細については、[プライベートエンドポイント経由でリージョン間接続を使用する](#use-cross-region-connections-over-a-private-endpoint)を参照してください。

ほとんどのシナリオでは、VPC ピアリングではなくプライベートエンドポイント接続を使用することをお勧めします。ただし、以下のシナリオでは、プライベートエンドポイント接続ではなく VPC ピアリングを使用する必要があります。

- 高可用性のために、ソースTiDBクラスターからターゲットTiDBクラスターへリージョンをまたいでデータをレプリケートするために、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用していますが、組織でリージョン間接続が有効になっていません。リージョン間接続が有効で、ソースリージョンが対象のノードグループに対して許可されている場合は、代わりにプライベートエンドポイントを使用できます。詳細については、[プライベートエンドポイント経由でリージョン間接続を使用する](#use-cross-region-connections-over-a-private-endpoint)を参照してください。
- TiCDC クラスターを使用してダウンストリームクラスター (Amazon Aurora、MySQL、Kafka など) にデータをレプリケートしていますが、エンドポイントサービスを独自に維持することはできません。
- PD または TiKV ノードに直接接続しています。

## 前提条件 {#prerequisites}

AWS VPC設定でDNSホスト名とDNS解決の両方が有効になっていることを確認してください。[AWS マネジメントコンソール](https://console.aws.amazon.com/)でVPCを作成すると、これらはデフォルトで無効になります。

## プライベートエンドポイント接続を設定し、クラスターに接続する {#set-up-a-private-endpoint-connection-and-connect-to-your-cluster}

プライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続するには、次の手順を実行します。

1. [TiDBクラスタを選択](#step-1-select-a-tidb-cluster)
2. [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3. [プライベートエンドポイント接続を作成する](#step-3-create-a-private-endpoint-connection)
4. [プライベートDNSを有効にする](#step-4-enable-private-dns)
5. [TiDBクラスタに接続する](#step-5-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### ステップ1. TiDBクラスターを選択する {#step-1-select-a-tidb-cluster}

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、概要ページに移動します。
2. 右上隅の**Connect**をクリックします。接続ダイアログが表示されます。
3. **Connection Type**ドロップダウンリストで**Private Endpoint**を選択し、 **Create Private Endpoint Connection**をクリックします。

> **Note:**
>
> プライベートエンドポイント接続を既に作成している場合は、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**Settings** > **Networking**をクリックして**Networking**ページに移動します。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

> **Note:**
>
> - IPv6 経由でクラスターに接続する場合は、追加の IPv6 設定について[プライベートエンドポイント経由で IPv6 接続を使用する](#use-ipv6-connectivity-over-a-private-endpoint)を参照してください。
> - 2023 年 3月 28日以降に作成されたTiDB Cloud Dedicated クラスターごとに、クラスターの作成後 3 ～ 4分後に対応するエンドポイントサービスが自動的に作成されます。
> - リージョン間接続の場合、生成されるコマンド内の`${your_region}`は、クラスターのリージョンとは異なる、VPC のリージョンである必要があります。AWS CLI を使用する場合は、`--service-region ${your_cluster_region}`も渡します。詳細については、[プライベートエンドポイント経由でリージョン間接続を使用する](#use-cross-region-connections-over-a-private-endpoint)を参照してください。

`TiDB Private Link Service is ready`メッセージが表示された場合、対応するエンドポイントサービスは準備完了です。エンドポイントを作成するには、以下の情報を提供してください。

1. **Your VPC ID**と**Your Subnet IDs**のフィールドに入力します。これらのIDは[AWS マネジメントコンソール](https://console.aws.amazon.com/)で確認できます。サブネットが複数ある場合は、IDをスペースで区切って入力してください。
2. **Generate Command**をクリックすると、次のエンドポイント作成コマンドが取得されます。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

次に、AWS CLI または[AWS マネジメントコンソール](https://aws.amazon.com/console/)を使用して AWS インターフェースエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェースエンドポイントを作成するには、次の手順を実行します。

1. 生成されたコマンドをコピーしてターミナルで実行します。
2. 作成した VPC エンドポイント ID を記録します。

> **Tip:**
>
> - コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> - サービスが3つを超えるアベイラビリティゾーン（AZ）にまたがっている場合、VPCエンドポイントサービスがサブネットのAZをサポートしていないことを示すエラーメッセージが表示されます。この問題は、選択したリージョンに、TiDBクラスターが配置されているAZに加えて、追加のAZが存在する場合に発生します。この場合、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェースエンドポイントを作成するには、次の手順を実行します。

1. [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2. ナビゲーションペインで**Endpoints**をクリックし、右上隅の**Create Endpoint**をクリックします。

    **Create endpoint**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. **Endpoint settings**領域で、必要に応じて名前タグを入力し、 **Endpoint services that use NLBs and GWLBs**オプションを選択します。

4. **Service settings**領域に、生成されたコマンド（ `--service-name ${your_endpoint_service_name}` ）のサービス名`${your_endpoint_service_name}`を入力します。

5. **Verify service**をクリックします。

6. **Network settings**領域で、ドロップダウンリストから VPC を選択します。

7. **Subnets**領域で、TiDB クラスターが配置されているアベイラビリティゾーンを選択します。

    > **Tip:**
    >
    > サービスが3つを超えるアベイラビリティゾーン（AZ）にまたがっている場合、 **Subnets**エリアでAZを選択できない場合があります。この問題は、選択したリージョンに、TiDBクラスターが配置されているAZに加えて、追加のAZが存在する場合に発生します。その場合は、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

8. **Security groups**領域で、セキュリティグループを適切に選択します。

    > **Note:**
    >
    > 選択したセキュリティグループが、ポート`4000`または顧客定義のポート上の EC2 インスタンスからのインバウンド アクセスを許可していることを確認します。

9. **Create endpoint**をクリックします。

</div>
</SimpleTab>

### ステップ3. プライベートエンドポイント接続を作成する {#step-3-create-a-private-endpoint-connection}

1. TiDB Cloudコンソールに戻ります。
2. **Create AWS Private Endpoint Connection**ページで、VPC エンドポイント ID を入力します。
3. **Create Private Endpoint Connection**をクリックします。

> **Tip:**
>
> プライベートエンドポイント接続は、次の2つのページで表示および管理できます。
>
> - クラスターレベルの**Networking**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** > **Networking**をクリックします。
> - プロジェクトレベルの**Network Access**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、**Project view** タブをクリックして対象のプロジェクトを見つけ、そのプロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックし、**Project Settings** の下にある **Network Access** をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns}

AWS でプライベート DNS を有効にします。AWS CLI または AWS マネジメントコンソールを使用できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、 **Create Private Endpoint Connection**ページから次の`aws ec2 modify-vpc-endpoint`コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --region ${your_vpc_region} --private-dns-enabled
```

> **Note:**
>
> `${your_vpc_region}`は、VPC エンドポイントが作成されるリージョンです。リージョン間接続の場合、これは TiDB クラスターのリージョンではなく、VPC エンドポイントのリージョンです。誤ったリージョンでコマンドを実行すると、`InvalidVpcEndpointId.NotFound`で失敗します。

または、クラスターの**Networking**ページでコマンドを見つけることもできます。プライベートエンドポイントを探し、 **Action**列の**...** > **Enable DNS**をクリックします。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには:

1. **VPC** > **Endpoints**に移動します。
2. エンドポイント ID を右クリックし、 **Modify private DNS name**を選択します。
3. **Enable for this endpoint**チェックボックスをオンにします。
4. **Save changes**をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### ステップ5. TiDBクラスターに接続する {#step-5-connect-to-your-tidb-cluster}

プライベートエンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1. プライベートエンドポイントの接続ステータスが**System Checking**から**Active**に変わるまで待ちます (約5分)。
2. **Connect With**ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3. 接続文字列を使用してクラスターに接続します。

> **Tip:**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティグループが正しく設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)をご覧ください。

### プライベートエンドポイントのステータスリファレンス {#private-endpoint-status-reference}

プライベートエンドポイント接続を使用すると、プライベートエンドポイントとプライベートエンドポイントサービスの状態が次のページに表示されます。

- クラスターレベルの**Networking**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** > **Networking**をクリックします。
- プロジェクトレベルの**Network Access**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、**Project view** タブをクリックして対象のプロジェクトを見つけ、そのプロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックし、**Project Settings** の下にある **Network Access** をクリックします。

プライベートエンドポイントの可能なステータスについては、次のように説明されます。

- **Not Configured**: エンドポイントサービスは作成されていますが、プライベートエンドポイントはまだ作成されていません。
- **Pending**: 処理を待機中です。
- **Active**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
- **Deleting**: プライベートエンドポイントを削除しています。
- **Failed**: プライベートエンドポイントの作成に失敗しました。その行の**Edit**をクリックすると、作成を再試行できます。

プライベートエンドポイントサービスの可能なステータスについては、次のように説明されます。

- **Creating**: エンドポイントサービスを作成中です。これには 3 ～ 5分かかります。
- **Active**: プライベートエンドポイントが作成されたかどうかに関係なく、エンドポイントサービスが作成されます。
- **Deleting**: エンドポイントサービスまたはクラスターを削除中です。これには 3 ～ 5分かかります。

## プライベートエンドポイント経由で IPv6 接続を使用する {#use-ipv6-connectivity-over-a-private-endpoint}

TiDB Cloud Dedicated は、AWS PrivateLink 経由のインバウンド IPv6 接続をサポートしています。

> **Note:**
>
> 現在、IPv6 接続機能はリクエストに応じて利用可能です。この機能を利用するには、[TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) に連絡し、組織 ID を提供してください。

TiDB Cloud では、各 [TiDB ノードグループ](/tidb-cloud/tidb-node-group-management.md) の IP プロトコルタイプを個別に設定できます。IPv6 経由で TiDB Cloud Dedicated クラスターに接続するには、対象ノードグループの IP プロトコルタイプをデュアルスタックに切り替えてから、次のようにデュアルスタックの AWS インターフェースエンドポイントを作成します。

### ステップ1. IP プロトコルタイプをデュアルスタックに切り替える {#step-1-switch-the-ip-protocol-type-to-dual-stack}

[TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) が組織に対して IPv6 接続機能を有効にした後、[TiDB Cloud コンソール](https://tidbcloud.com/) で IP プロトコルタイプを切り替えることができます。

1. 組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象クラスターの名前をクリックして概要ページを開き、左側のナビゲーションペインで **Settings** > **Networking** をクリックします。
2. 各 TiDB Cloud Dedicated クラスターにはデフォルトの [TiDB ノードグループ](/tidb-cloud/tidb-node-group-management.md) があります。クラスターに複数のノードグループがある場合は、右上の **TiDB Node Group** リストから対象の TiDB ノードグループを選択します。
3. **AWS Private Endpoints** セクションで、**Edit** をクリックします。
4. **AWS Private Endpoints Connection Settings** ダイアログで、IP プロトコルタイプとして **Dual Stack (IPv4 + IPv6)** を選択し、**Save** をクリックします。

> **Note:**
>
> IP プロトコルタイプを **IPv4 Only** に戻すには、まず IPv6 を使用するすべてのプライベートエンドポイントを削除する必要があります。IPv4 のみを使用するプライベートエンドポイントは削除する必要はありません。

IP プロトコルタイプは、クラスターの作成後にのみ変更できます。

### ステップ2. IPv6 用のデュアルスタック AWS インターフェースエンドポイントを作成する {#step-2-create-a-dual-stack-aws-interface-endpoint-for-ipv6}

[ステップ2. AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint) の説明に従って AWS インターフェースエンドポイントを作成し、次の点に注意してください。

- **IP address type** では、エンドポイントのネットワークインターフェースに IPv4 アドレスと IPv6 アドレスの両方を割り当てるために、**Dualstack** を選択します。
- **Subnets** では、それぞれが IPv4 CIDR ブロックと IPv6 CIDR ブロックの両方を持つサブネットを選択します。
- AWS CLI を使用する場合は、生成されたコマンドに `--ip-address-type dualstack` を追加します。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids} --ip-address-type dualstack
    ```

その後、[ステップ3](#step-3-create-a-private-endpoint-connection) から [ステップ5](#step-5-connect-to-your-tidb-cluster) までを完了して、プライベートエンドポイント接続を作成し、IPv6 経由でクラスターに接続します。

## プライベートエンドポイント経由でリージョン間接続を使用する {#use-cross-region-connections-over-a-private-endpoint}

デフォルトでは、プライベートエンドポイントと、それが接続する TiDB Cloud Dedicated クラスターは、同じ AWS リージョン内に存在する必要があります。TiDB Cloud Dedicated はリージョン間接続もサポートしており、これにより、あるリージョンで VPC エンドポイントを作成し、別のリージョンのクラスターに接続できます。接続文字列と DNS の使用方法は、同一リージョン接続の場合と同じです。

> **Note:**
>
> 現在、リージョン間接続機能はリクエストベースでのみ利用できます。この機能を利用するには、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡し、組織 ID を提供してください。

TiDB Cloud では、[TiDB ノードグループ](/tidb-cloud/tidb-node-group-management.md)ごとに接続スコープを個別に設定できます。別のリージョンからクラスターに接続するには、対象のノードグループにそのリージョンを許可してから、自分のリージョンに AWS インターフェースエンドポイントを作成します。

### ステップ1. VPC エンドポイントのリージョンを許可する {#step-1-allow-the-region-of-your-vpc-endpoint}

1. 組織の [**My TiDB**](https://tidbcloud.com/tidbs) ページに移動し、対象クラスターの名前をクリックして概要ページに移動してから、左側のナビゲーションペインで **Settings** > **Networking** をクリックします。
2. 各 TiDB Cloud Dedicated クラスターには、デフォルトの [TiDB ノードグループ](/tidb-cloud/tidb-node-group-management.md) があります。クラスターに複数のノードグループがある場合は、右上隅の **TiDB Node Group** リストから対象の TiDB ノードグループを選択します。
3. **AWS Private Endpoints** セクションで、**Edit** をクリックします。
4. **AWS Private Endpoints Connection Settings** ダイアログで、**Connection Scope** に **Cross-Region** を選択し、許可するリージョンを選択して、**Save** をクリックします。

設定が保存されると、許可されたリージョンが **AWS Private Endpoints** セクションの **Connection Scope** 領域に表示されます。

> **Note:**
>
> - 設定を保存しても、許可するリージョンが記録されるだけです。TiDB Cloud は更新を非同期に適用するため、表示された後でも許可されたリージョンの調整がまだ進行中である場合があります。次のステップで VPC エンドポイントを作成する前に、**Connection Scope** の更新が正常に完了するまで待ってください。そうしないと、リージョンがすでに表示されていても、エンドポイントの作成が失敗する可能性があります。更新が失敗した場合は、再試行するか、[TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md) に連絡してください。
> - リージョン間接続には料金が発生します。AWS は、許可した各リージョンごとではなく、少なくとも 1 つの接続済みインターフェースエンドポイントがある **active** なリモートリージョンごとに、サービスプロバイダーに課金します。VPC エンドポイントの所有者として、標準のエンドポイント時間料金とデータ処理使用量、およびリージョン間データ転送料金も課金されます。さらに、TiDB Cloud はリージョン間 PrivateLink サービス料金を請求します。詳細については、[AWS PrivateLink pricing](https://aws.amazon.com/privatelink/pricing/) と [TiDB Cloud Dedicated pricing details](https://www.pingcap.com/tidb-dedicated-pricing-details/) を参照してください。
> - リージョンを削除したり、**Connection Scope** を **Current Region Only** に戻したりしても、そのリージョン内の既存の接続には影響しません。そこで新しいプライベートエンドポイントを作成できなくなるだけで、既存のエンドポイントは切断されないため、それらのエンドポイントが削除されるまで AWS の課金が継続する可能性があります。許可されなくなったリージョン内の接続には、**AWS Private Endpoints** リストで警告が表示されます。

### ステップ2. リージョン間 AWS インターフェースエンドポイントを作成する {#step-2-create-a-cross-region-aws-interface-endpoint}

[ステップ2. AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint) の説明に従って AWS インターフェースエンドポイントを作成し、次の点に注意してください。

- エンドポイントは、TiDB Cloud Dedicated クラスターのリージョンとは異なる、アプリケーションが実行される AWS リージョンに作成します。AWS マネジメントコンソールでは、**Enable Cross Region endpoint** を選択し、**Service Region** を TiDB Cloud Dedicated クラスターのリージョンに設定します。
- **Subnets** では、リージョン間アクセスをサポートするアベイラビリティゾーン内のサブネットを選択します。リージョン内のすべてのアベイラビリティゾーンがリージョン間アクセスをサポートしているわけではありません。サブネットがサポートされていないアベイラビリティゾーンにある場合、作成は失敗し、サポートされているアベイラビリティゾーンを一覧表示するエラーが表示されるため、代わりに一覧に表示されたアベイラビリティゾーン内のサブネットを選択できます。
- リージョン間エンドポイントを作成する前に、呼び出し元の ID ポリシーと適用される Service Control Policy で `vpce:AllowMultiRegion` が許可されていることを確認してください。
- AWS CLI を使用する場合は、`--service-region ${your_cluster_region}` でクラスターのリージョンを渡します。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_vpc_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids} --service-region ${your_cluster_region}
    ```

次に、[ステップ3. プライベートエンドポイント接続を作成する](#step-3-create-a-private-endpoint-connection) から [ステップ5. TiDBクラスターに接続する](#step-5-connect-to-your-tidb-cluster) までを完了して、プライベートエンドポイント接続を作成し、別のリージョンからクラスターに接続します。

> **Note:**
>
> VPC エンドポイントを作成するリージョンが対象ノードグループの許可リージョンでない場合、プライベートエンドポイント接続を作成できず、TiDB Cloud はエラーを報告します。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDBクラスターに接続できません。なぜですか？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWSマネジメントコンソールで、VPCエンドポイントのセキュリティグループを適切に設定する必要がある場合があります。**VPC** > **Endpoints**に移動します。これを行うには、 **VPC** > **Endpoints**に移動し、VPCエンドポイントを右クリックして**Manage security groups**を選択します。選択したセキュリティグループが、ポート`4000`またはお客様定義のポートでEC2インスタンスからのインバウンドアクセスを許可していることを確認してください。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
