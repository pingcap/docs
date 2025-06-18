---
title: Connect to TiDB Cloud Serverless via Private Endpoint
summary: プライベート エンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# プライベートエンドポイント経由でTiDB Cloud Serverless に接続する {#connect-to-tidb-cloud-serverless-via-private-endpoint}

このドキュメントでは、プライベート エンドポイント経由でTiDB Cloud Serverless クラスターに接続する方法について説明します。

> **ヒント：**
>
> -   AWS のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
> -   Azure のプライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [Azure Private Link 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)参照してください。
> -   Google Cloud のプライベート エンドポイント経由でTiDB Cloud Dedicated クラスタに接続する方法については、 [Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。

TiDB Cloudは、AWS VPCでホストされているTiDB Cloudサービスへの、 [AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)経由の高度に安全な一方向アクセスをサポートします。まるでお客様のVPC内にあるかのようにアクセス可能です。VPC内にプライベートエンドポイントが公開されており、権限があればエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートになり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB Cloud は、エンドポイントサービスが AWS でホストされている場合にのみ、 TiDB Cloud Serverless へのプライベートエンドポイント接続をサポートしています。サービスが Google Cloud でホストされている場合、プライベートエンドポイントは適用されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

## 前提条件 {#prerequisites}

AWS VPC設定でDNSホスト名とDNS解決の両方が有効になっていることを確認してください。1 [AWS マネジメントコンソール](https://console.aws.amazon.com/) VPCを作成すると、これらはデフォルトで無効になります。

## AWSでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

プライベート エンドポイント経由でTiDB Cloud Serverless クラスターに接続するには、次の手順に従います。

1.  [TiDBクラスタを選択する](#step-1-choose-a-tidb-cluster)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [TiDBクラスタに接続する](#step-3-connect-to-your-tidb-cluster)

### ステップ1. TiDBクラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲットのTiDB Cloud Serverless クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[接続タイプ]**ドロップダウン リストで、 **[プライベート エンドポイント]**を選択します。
4.  **サービス名**、**アベイラビリティーゾーン ID** 、**リージョンID を**メモします。

    > **注記：**
    >
    > AWS リージョンごとにプライベートエンドポイントを 1 つ作成するだけで、同じリージョンにあるすべてのTiDB Cloud Serverless クラスターで共有できます。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **NLB および GWLB を使用するエンドポイント サービス**を選択します。

4.  [ステップ1](#step-1-choose-a-tidb-cluster)で確認したサービス名を入力します。

5.  **[サービスの確認]**をクリックします。

6.  ドロップダウンリストからVPCを選択します。 **「追加設定」**を展開し、 **「DNS名を有効にする」**チェックボックスをオンにします。

7.  **[サブネット]**領域で、TiDB クラスターが配置されているアベイラビリティーゾーンを選択し、サブネット ID を選択します。

8.  **Securityグループ**領域でセキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループがポート 4000 上の EC2 インスタンスからの受信アクセスを許可していることを確認します。

9.  **[エンドポイントの作成]**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネット ID**を取得するには、AWS マネジメントコンソールに移動し、該当するセクションでそれらを見つけます[ステップ1](#step-1-choose-a-tidb-cluster)で確認した**アベイラビリティーゾーン ID**を必ず入力してください。
2.  以下のコマンドをコピーし、関連する引数を取得した情報に置き換えて、ターミナルで実行します。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。

</div>
</SimpleTab>

その後、プライベート DNS 名を使用してエンドポイント サービスに接続できます。

### ステップ3: TiDBクラスターに接続する {#step-3-connect-to-your-tidb-cluster}

インターフェース エンドポイントを作成したら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[接続タイプ]**ドロップダウン リストで、 **[プライベート エンドポイント]**を選択します。
4.  **「接続方法**」ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
5.  接続文字列を使用してクラスターに接続します。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティグループが正しく設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)ご覧ください。
>
> VPC エンドポイントを作成するときにエラー`private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`発生した場合は、プライベート エンドポイントがすでに作成されているため、新しいエンドポイントを作成する必要はありません。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDBクラスターに接続できません。なぜですか？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWSマネジメントコンソールで、VPCエンドポイントのセキュリティグループを適切に設定する必要がある場合があります。 **「VPC」** &gt; **「エンドポイント」**に移動します。VPCエンドポイントを右クリックし、「**セキュリティグループの管理」**を選択します。VPC内に適切なセキュリティグループを作成し、ポート4000またはお客様定義のポートでEC2インスタンスからのインバウンドアクセスを許可します。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
