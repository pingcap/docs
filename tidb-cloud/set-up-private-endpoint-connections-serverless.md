---
title: Connect to TiDB Cloud Starter or Essential via AWS PrivateLink
summary: プライベートエンドポイントを介してTiDB Cloudクラスターに接続する方法を学びましょう。
---

# AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。 {#connect-to-tidb-cloud-starter-or-essential-via-aws-privatelink}

このドキュメントでは、AWS PrivateLink を介してTiDB Cloud StarterまたはTiDB Cloud Essentialクラスターに接続する方法について説明します。

> **ヒント：**
>
> -   AWS のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
> -   Azure のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)参照してください。
> -   Google Cloud のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

TiDB Cloud は、AWS VPC でホストされているTiDB Cloudサービスへの[AWSプライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)に安全な一方向アクセスをサポートしており、まるでサービスがお客様自身の VPC 内にあるかのように動作します。プライベートエンドポイントがお客様の VPC 内に公開され、権限があればそのエンドポイントを介してTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用したエンドポイント接続は、安全かつプライベートであり、お客様のデータをパブリックインターネットに公開することはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

プライベートエンドポイントのアーキテクチャは以下のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントおよびエンドポイントサービスのより詳細な定義については、以下のAWSドキュメントを参照してください。

-   [AWS PrivateLinkとは何ですか？](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLinkの概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB CloudはエンドポイントサービスがAWSでホストされている場合にのみAWS PrivateLink接続をサポートしています。サービスが他のクラウドプロバイダーでホストされている場合、AWS PrivateLink接続は利用できません。
-   リージョンをまたいだプライベートエンドポイント接続はサポートされていません。

## 前提条件 {#prerequisites}

AWS VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。これらは、 [AWS マネジメントコンソール](https://console.aws.amazon.com/)で VPC を作成するときにデフォルトで無効になっています。

## AWSでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

プライベートエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタに接続するには、以下の手順に従ってください。

1.  [TiDBクラスタを選択してください](#step-1-choose-a-tidb-cluster)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [TiDB Cloudでプライベートエンドポイントを認証します。](#step-3-authorize-your-private-endpoint-in-tidb-cloud)
4.  [TiDBクラスターに接続します](#step-4-connect-to-your-tidb-cluster)

### ステップ1. TiDBクラスタを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **サービス名**、**アベイラビリティゾーンID** 、**リージョンID**をメモしておいてください。

    > **注記：**
    >
    > 各AWSリージョンにつき、プライベートエンドポイントを1つ作成するだけで済みます。このエンドポイントは、同じリージョンにあるすべてのTiDB Cloud StarterまたはTiDB Cloud Essentialクラスターで共有できます。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーションペインの**「エンドポイント」**をクリックし、右上隅の**「エンドポイントの作成」を**クリックします。

    **エンドポイント作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **NLBとGWLBを使用するエンドポイントサービス**を選択します。

4.  [ステップ1](#step-1-choose-a-tidb-cluster)で見つけたサービス名を入力してください。

5.  **「サービスを確認する」**をクリックしてください。

6.  ドロップダウンリストからVPCを選択します。 **「追加設定」**を展開し、 **「DNS名を有効にする」**チェックボックスをオンにします。

7.  **サブネット**領域で、TiDBクラスタが配置されているアベイラビリティゾーンを選択し、サブネットIDを選択します。

8.  **Securityグループ**領域で、適切なセキュリティグループを選択してください。

    > **注記：**
    >
    > 選択したセキュリティグループが、EC2インスタンスからのポート4000への受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」を**クリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネット ID**を取得するには、AWS マネジメント コンソールに移動し、該当するセクションでそれらを見つけます。7 [ステップ1](#step-1-choose-a-tidb-cluster)見つけた**アベイラビリティ ゾーン ID を**必ず入力してください。
2.  以下のコマンドをコピーし、該当する引数をあなたが取得した情報に置き換えてから、ターミナルで実行してください。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は[AWS CLI設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。

</div>
</SimpleTab>

そうすれば、プライベートDNS名を使ってエンドポイントサービスに接続できます。

### ステップ3. TiDB Cloudでプライベートエンドポイントを認証します {#step-3-authorize-your-private-endpoint-in-tidb-cloud}

AWSインターフェースエンドポイントを作成したら、それをクラスターの許可リストに追加する必要があります。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **プライベートエンドポイントの**セクションまでスクロールダウンし、**承認済みネットワークの**表を探してください。

4.  ファイアウォールルールを追加するには、 **「ルールの追加」**をクリックします。

    -   **エンドポイントサービス名**： [ステップ1](#step-1-choose-a-tidb-cluster)で取得したサービス名を貼り付けてください。

    -   **ファイアウォールルール名**：この接続を識別するための名前を入力してください。

    -   **VPCエンドポイントID** ：AWSマネジメントコンソールから取得した22文字のVPCエンドポイントID（ `vpce-`で始まる）を貼り付けてください。

    > **ヒント：**
    >
    > クラウドリージョンからのすべてのプライベートエンドポイント接続を許可するには（テストまたはオープンアクセスのため）、 **[VPCエンドポイントID]**フィールドにアスタリスク( `*` )を1つ入力します。

5.  **「送信」**をクリックしてください。

### ステップ4. TiDBクラスターに接続します {#step-4-connect-to-your-tidb-cluster}

インターフェースエンドポイントを作成したら、 TiDB Cloudコンソールに戻り、以下の手順を実行してください。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象クラスターの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。
5.  接続文字列を使用してクラスターに接続してください。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが正しく設定されていないことが原因である可能性があります。解決策については、 [このFAQ](#troubleshooting)参照してください。
>
> VPCエンドポイントを作成する際にエラー`private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`が発生した場合は、既にプライベートエンドポイントが作成されているため、新しいエンドポイントを作成する必要がないことを意味します。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDBクラスタに接続できなくなりました。原因は何でしょうか？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで**、** VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。VPC &gt;**エンドポイント**に移動します。VPC エンドポイントを右クリックし、適切な**セキュリティ グループの管理**を選択します。VPC 内に、EC2 インスタンスからのポート 4000 またはお客様定義のポートへの受信アクセスを許可する適切なセキュリティ グループを設定します。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
