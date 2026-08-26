---
title: Connect to a TiDB Cloud Dedicated Cluster via AWS PrivateLink
summary: AWS を使用してプライベートエンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# AWS PrivateLink 経由でTiDB Cloud Dedicatedクラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-aws-privatelink}

このドキュメントでは、 [AWS プライベートリンク](https://aws.amazon.com/privatelink)経由でTiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **Tip:**
>
> - AWS PrivateLink 経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。
> - Azure のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [Azure Private Link 経由でTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)を参照してください。
> - Google Cloud のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスタに接続する方法については、 [Google Cloud Private Service Connect 経由でTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。

TiDB Cloudは、 AWS VPCでホストされているTiDB Cloudサービスへの、 [AWS プライベートリンク](https://aws.amazon.com/privatelink)経由の高度に安全な一方向アクセスをサポートします。まるでお客様のVPC内にあるかのように機能します。VPC内にプライベートエンドポイントが公開されており、権限があればエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートであり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベートエンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

- [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
- [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

- プライベートエンドポイントを作成できるのは、ロール`Organization Owner`または`Project Owner`持つユーザーのみです。
- プライベートエンドポイントと接続先の TiDB クラスターは同じリージョンに配置されている必要があります。

ほとんどのシナリオでは、VPC ピアリングではなくプライベートエンドポイント接続を使用することをお勧めします。ただし、以下のシナリオでは、プライベートエンドポイント接続ではなく VPC ピアリングを使用する必要があります。

- 高可用性を実現するために、ソースTiDBクラスターからターゲットTiDBクラスターへリージョンをまたいでデータをレプリケートするために、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用しています。現在、プライベートエンドポイントはリージョン間接続をサポートしていません。
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
> プライベートエンドポイント接続を既に作成している場合は、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックして**Networking**ページに移動します。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

> **Note:**
>
> 2023 年 3月 28日以降に作成されたTiDB Cloud Dedicated クラスターごとに、クラスターの作成後 3 ～ 4分後に対応するエンドポイントサービスが自動的に作成されます。

`TiDB Private Link Service is ready`メッセージが表示された場合、対応するエンドポイントサービスは準備完了です。エンドポイントを作成するには、以下の情報を提供してください。

1. **Your VPC ID**と**Your Subnet IDs**のフィールドに入力します。これらのIDは[AWS マネジメントコンソール](https://console.aws.amazon.com/)で確認できます。サブネットが複数ある場合は、IDをスペースで区切って入力してください。
2. **Generate Command**をクリックすると、次のエンドポイント作成コマンドが取得されます。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

次に、AWS CLI または[AWS マネジメントコンソール](https://aws.amazon.com/console/)を使用して AWS インターフェイスエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1. 生成されたコマンドをコピーしてターミナルで実行します。
2. 作成した VPC エンドポイント ID を記録します。

> **Tip:**
>
> - コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> - サービスが3つを超えるアベイラビリティゾーン（AZ）にまたがっている場合、VPCエンドポイントサービスがサブネットのAZをサポートしていないことを示すエラーメッセージが表示されます。この問題は、選択したリージョンに、TiDBクラスターが配置されているAZに加えて、追加のAZが存在する場合に発生します。この場合、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1. [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2. ナビゲーションペインで**Endpoints**をクリックし、右上隅の**Create Endpoint**をクリックします。

    **Create endpoint**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. **Endpoint settings**領域で、必要に応じて名前タグを入力し、 **Endpoint services that use NLBs and GWLBs**オプションを選択します。

4. **Service settings**領域に、生成されたコマンド（ `--service-name ${your_endpoint_service_name}` ）のサービス名`${your_endpoint_service_name}`入力します。

5. **Verify service**をクリックします。

6. **Network settings**領域で、ドロップダウンリストから VPC を選択します。

7. **Subnets**領域で、TiDB クラスターが配置されている可用性ゾーンを選択します。

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
> - クラスターレベルの**Networking**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。
> - プロジェクトレベルの**Network Access**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、**Project view** タブをクリックして対象のプロジェクトを見つけ、そのプロジェクトの <MDSvgIcon name="icon-project-settings" /> をクリックし、**Project Settings** の下にある **Network Access** をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns}

AWS でプライベート DNS を有効にします。AWS CLI または AWS マネジメントコンソールを使用できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、 **Create Private Endpoint Connection**ページから次の`aws ec2 modify-vpc-endpoint`コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

または、クラスターの**Networking**ページでコマンドを見つけることもできます。プライベートエンドポイントを探し、 **Action**列の**...** &gt; **Enable DNS**をクリックします。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには:

1. **VPC** &gt; **Endpoints**に移動します。
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
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティグループが正しく設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)ご覧ください。

### プライベートエンドポイントのステータスリファレンス {#private-endpoint-status-reference}

プライベートエンドポイント接続を使用すると、プライベートエンドポイントとプライベートエンドポイントサービスの状態が次のページに表示されます。

- クラスターレベルの**Networking**ページ: 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。
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

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDBクラスターに接続できません。なぜですか？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWSマネジメントコンソールで、VPCエンドポイントのセキュリティグループを適切に設定する必要がある場合があります。**VPC** &gt; **Endpoints**に移動します。これを行うには、 **VPC** &gt; **Endpoints**に移動し、VPCエンドポイントを右クリックして**Manage security groups**を選択します。選択したセキュリティグループが、ポート`4000`またはお客様定義のポートでEC2インスタンスからのインバウンドアクセスを許可していることを確認してください。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
