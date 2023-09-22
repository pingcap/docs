---
title: Connect to TiDB Serverless via Private Endpoint
summary: Learn how to connect to your TiDB Cloud cluster via private endpoint.
---

# プライベートエンドポイント経由で TiDB サーバーレスに接続する {#connect-to-tidb-serverless-via-private-endpoint}

このドキュメントでは、プライベート エンドポイント経由で TiDB サーバーレス クラスターに接続する方法について説明します。

> **ヒント：**
>
> AWS のプライベート エンドポイント経由で TiDB 専用クラスターに接続する方法については、 [AWS のプライベート エンドポイント経由で専用 TiDB に接続する](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。 Google Cloud のプライベート エンドポイントを介して TiDB 専用クラスターに接続する方法については、 [プライベート サービス経由で専用 TiDB に接続 Google Cloud に接続](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

TiDB Cloud は、 AWS VPC でホストされているTiDB Cloudサービスへの[AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)経由の、あたかもそのサービスが独自の VPC 内にあるかのように、安全性の高い一方向のアクセスをサポートします。プライベート エンドポイントが VPC で公開され、許可を得てエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用したエンドポイント接続は安全かつプライベートであり、データが公共のインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベート エンドポイントとエンドポイント サービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB Cloud は、エンドポイント サービスが AWS でホストされている場合にのみ、TiDB Serverless へのプライベート エンドポイント接続をサポートしています。サービスが Google Cloud でホストされている場合、プライベート エンドポイントは適用されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

## AWS でプライベート エンドポイントをセットアップする {#set-up-a-private-endpoint-with-aws}

プライベート エンドポイント経由で TiDB サーバーレス クラスターに接続するには、次の手順に従います。

1.  [TiDB クラスターを選択する](#step-1-choose-a-tidb-cluster)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [TiDB クラスターに接続する](#step-3-connect-to-your-tidb-cluster)

### ステップ 1. TiDB クラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット TiDB サーバーレス クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **サービス名**、**アベイラビリティーゾーン ID** 、および**リージョンID**をメモします。

    > **注記：**
    >
    > AWS リージョンごとにプライベート エンドポイントを 1 つ作成するだけで済み、同じリージョンにあるすべての TiDB サーバーレス クラスターで共有できます。

### ステップ 2. AWS インターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **[エンドポイントの作成]**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **[その他のエンドポイント サービス]**を選択します。

4.  [ステップ1](#step-1-choose-a-tidb-cluster)で見つけたサービス名を入力します。

5.  **[サービスの確認]**をクリックします。

6.  ドロップダウン リストから VPC を選択します。 **[追加設定]**を展開し、 **[DNS 名を有効にする**] チェックボックスを選択します。

7.  **[サブネット]**領域で、TiDB クラスターが配置されているアベイラビリティ ゾーンを選択し、サブネット ID を選択します。

8.  **[Securityグループ]**領域でセキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループがポート 4000 での EC2 インスタンスからの受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネット ID**を取得するには、AWS マネジメントコンソールに移動し、関連するセクションでそれらを見つけます。 [ステップ1](#step-1-choose-a-tidb-cluster)で見つけた**アベイラビリティーゾーン ID を**必ず入力してください。
2.  以下に提供されているコマンドをコピーし、関連する引数を取得した情報に置き換えて、ターミナルで実行します。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細については[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

</div>
</SimpleTab>

その後、プライベート DNS 名を使用してエンドポイント サービスに接続できます。

### ステップ 3: TiDB クラスターに接続する {#step-3-connect-to-your-tidb-cluster}

インターフェイス エンドポイントを作成したら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **[接続方法**] ドロップダウン リストで、希望の接続方法を選択します。対応する接続​​文字列がダイアログの下部に表示されます。
5.  接続文字列を使用してクラスターに接続します。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)参照してください。
>
> VPC エンドポイントの作成時にエラー`private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`が発生した場合、プライベート エンドポイントがすでに作成されていることが原因であり、新しいエンドポイントを作成する必要はありません。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なぜ？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

場合によっては、AWS マネジメント コンソールで VPC エンドポイントのセキュリティ グループを適切に設定する必要があります。 **[VPC]** &gt; **[エンドポイント]**に移動します。 VPC エンドポイントを右クリックし、適切な**[セキュリティ グループの管理]**を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからの受信アクセスを許可する、VPC 内の適切なセキュリティ グループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。 <code>enableDnsSupport</code>および<code>enableDnsHostnames</code> VPC 属性が有効になっていないことを示すエラーが報告される {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。 AWS マネジメントコンソールで VPC を作成すると、デフォルトでは無効になります。
