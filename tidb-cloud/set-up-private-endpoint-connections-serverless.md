---
title: Connect to TiDB Serverless via Private Endpoint
summary: プライベート エンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# プライベートエンドポイント経由で TiDB Serverless に接続する {#connect-to-tidb-serverless-via-private-endpoint}

このドキュメントでは、プライベート エンドポイント経由で TiDB Serverless クラスターに接続する方法について説明します。

> **ヒント：**
>
> AWS のプライベート エンドポイント経由で TiDB 専用クラスタに接続する方法については、 [AWS のプライベートエンドポイント経由で TiDB Dedicated に接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。Google Cloud のプライベート エンドポイント経由で TiDB 専用クラスタに接続する方法については、 [プライベートサービス経由でTiDB Dedicatedに接続 Google Cloudに接続](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)を参照してください。

TiDB Cloud は、 [AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)を介して AWS VPC でホストされているTiDB Cloudサービスへの、非常に安全な一方向アクセスをサポートします。これは、サービスが自分の VPC 内にある場合と同じです。プライベート エンドポイントが VPC で公開され、アクセス許可を持つエンドポイントを介してTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートになり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB Cloud は、エンドポイント サービスが AWS でホストされている場合にのみ、TiDB Serverless へのプライベート エンドポイント接続をサポートしています。サービスが Google Cloud でホストされている場合、プライベート エンドポイントは適用されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

## AWSでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

プライベート エンドポイント経由で TiDB Serverless クラスターに接続するには、次の手順に従います。

1.  [TiDBクラスタを選択する](#step-1-choose-a-tidb-cluster)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [TiDBクラスターに接続する](#step-3-connect-to-your-tidb-cluster)

### ステップ1. TiDBクラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲットの TiDB Serverless クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **サービス名**、**アベイラビリティーゾーン ID** 、**リージョンID**をメモします。

    > **注記：**
    >
    > AWS リージョンごとにプライベートエンドポイントを 1 つ作成するだけで、同じリージョンにあるすべての TiDB Serverless クラスターで共有できます。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [詳しくはこちら](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント**] をクリックし、右上隅の**[エンドポイントの作成] を**クリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **その他のエンドポイント サービス**を選択します。

4.  [ステップ1](#step-1-choose-a-tidb-cluster)で確認したサービス名を入力します。

5.  **[サービスの確認]を**クリックします。

6.  ドロップダウン リストから VPC を選択します。 **[追加設定]**を展開し、 **[DNS 名を有効にする]**チェックボックスをオンにします。

7.  **[サブネット]**領域で、TiDB クラスターが配置されている可用性ゾーンを選択し、サブネット ID を選択します。

8.  **Securityグループ**領域でセキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループが、ポート 4000 上の EC2 インスタンスからの受信アクセスを許可していることを確認します。

9.  **[エンドポイントの作成]を**クリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネット ID**を取得するには、AWS マネジメントコンソールに移動し、関連するセクションでそれらを見つけます[ステップ1](#step-1-choose-a-tidb-cluster)で確認した**アベイラビリティーゾーン ID**を必ず入力してください。
2.  以下のコマンドをコピーし、関連する引数を取得した情報に置き換えて、ターミナルで実行します。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細については[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

</div>
</SimpleTab>

その後、プライベート DNS 名を使用してエンドポイント サービスに接続できます。

### ステップ3: TiDBクラスターに接続する {#step-3-connect-to-your-tidb-cluster}

インターフェース エンドポイントを作成したら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **[接続方法]**ドロップダウン リストで、希望する接続方法を選択します。対応する接続​​文字列がダイアログの下部に表示されます。
5.  接続文字列を使用してクラスターに接続します。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)参照してください。
>
> VPC エンドポイントを作成するときにエラー`private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`発生した場合は、プライベート エンドポイントがすでに作成されているため、新しいエンドポイントを作成する必要はありません。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なぜですか? {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメントコンソールで、VPC エンドポイントのセキュリティグループを適切に設定する必要がある場合があります。 **[VPC]** &gt; **[エンドポイント**] に移動します。VPC エンドポイントを右クリックし、適切な**[セキュリティグループの管理]**を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからのインバウンドアクセスを許可する、VPC 内の適切なセキュリティグループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。enableDnsSupport および<code>enableDnsSupport</code> VPC 属性が有効になっていないことを示すエラー<code>enableDnsHostnames</code>報告されます {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。AWS マネジメントコンソールで VPC を作成すると、これらはデフォルトで無効になります。
