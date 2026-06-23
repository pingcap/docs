---
title: Connect to TiDB Cloud Starter or Essential via AWS PrivateLink
summary: プライベートエンドポイントを介してTiDB Cloud StarterまたはEssentialインスタンスに接続する方法を学びましょう。
---

# AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。 {#connect-to-tidb-cloud-starter-or-essential-via-aws-privatelink}

このドキュメントでは、AWS PrivateLink を介してTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法について説明します。

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   Azure のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)D dedicated クラスターに接続する」を参照してください。
> -   Google Cloud のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)参照してください。

TiDB Cloudは、 AWS VPC内でホストされているTiDB Cloudサービスへの[AWSプライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)を介した高度に安全な一方向アクセスをサポートしています。まるでサービスがお客様自身のVPC内にあるかのように動作します。お客様のVPC内にプライベートエンドポイントが公開され、権限があればそのエンドポイントを介してTiDB Cloudサービスへの接続を作成できます。

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

AWS VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。 [AWS マネジメントコンソール](https://console.aws.amazon.com/)で VPC を作成すると、デフォルトでは無効になります。

## AWSでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにプライベートエンドポイント経由で接続するには、以下の手順に従ってください。

1.  [TiDB Cloud StarterまたはEssentialインスタンスを選択してください](#step-1-choose-a-tidb-instance)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [TiDB Cloudでプライベートエンドポイントを認証する（オプション）](#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional)
4.  [TiDB Cloud StarterまたはEssentialインスタンスに接続します](#step-4-connect-to-your-tidb)

### ステップ1. TiDB Cloud StarterまたはEssentialインスタンスを選択します {#step-1-choose-a-tidb-instance} {#step-1-choose-a-tidb-instance}

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **サービス名**、**アベイラビリティゾーンID** 、**リージョンID**をメモしておいてください。

    > **注記：**
    >
    > AWSリージョン内の各VPCにつき、作成する必要があるプライベートエンドポイントは1つだけです。このエンドポイントは、同じAWSリージョン内の同じVPCにあるすべてのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスで使用できますが、VPC間で共有することはできません。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)コンソールにサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーションペインの**「エンドポイント」**をクリックし、右上隅の**「エンドポイントの作成」を**クリックします。

    **エンドポイント作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **NLBとGWLBを使用するエンドポイントサービス**を選択します。

4.  [ステップ1](#step-1-choose-a-tidb-instance)で見つけたサービス名を入力します。

5.  **「サービスを確認する」**をクリックしてください。

6.  ドロップダウンリストからVPCを選択します。 **「追加設定」**を展開し、 **「DNS名を有効にする」**チェックボックスをオンにします。

7.  **サブネット**領域で、 TiDB Cloud StarterまたはEssentialインスタンスが配置されているアベイラビリティゾーンを選択し、サブネットIDを選択します。

8.  **セキュリティグループ**領域で、適切なセキュリティグループを選択してください。

    > **注記：**
    >
    > 選択したセキュリティグループが、EC2インスタンスからのポート4000への受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」を**クリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネットID**を取得するには、AWSマネジメントコンソールに移動し、該当するセクションでそれらを見つけてください。[ステップ1](#step-1-choose-a-tidb-instance)で見つけた**アベイラビリティゾーンID**を必ず入力してください。
2.  以下のコマンドをコピーし、該当する引数をあなたが取得した情報に置き換えてから、ターミナルで実行してください。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細については、 [AWS CLI設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。

</div>
</SimpleTab>

そうすれば、プライベートDNS名を使ってエンドポイントサービスに接続できます。

### ステップ3．TiDB Cloudでプライベートエンドポイントを認証する（オプション） {#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional}

> **注記：**
>
> この手順は任意です。特定のプライベートエンドポイント接続へのアクセスを制限する場合にのみ、**承認済みネットワーク**を設定する必要があります。ルールが設定されていない場合、すべてのプライベートエンドポイント接続がデフォルトで許可されます。

AWSインターフェースエンドポイントを作成した後、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに対して認証を行い、アクセスを制限できます。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックすると、その概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **プライベートエンドポイントの**セクションまでスクロールダウンし、**承認済みネットワークの**表を探してください。

4.  ファイアウォールルールを追加するには、 **「ルールの追加」**をクリックします。

    -   **エンドポイント サービス名**:[ステップ1](#step-1-choose-a-tidb-instance)から取得したサービス名を貼り付けます。

    -   **ファイアウォールルール名**：この接続を識別するための名前を入力してください。

    -   **VPCエンドポイントID** ：AWSマネジメントコンソールから取得した22文字のVPCエンドポイントIDを貼り付けてください（ `vpce-`で始まります）。

    > **ヒント：**
    >
    > -   **「承認済みネットワーク」**テーブルを空のままにした場合、デフォルトで全てのプライベートエンドポイント接続が許可されます。
    > -   クラウドリージョンからのすべてのプライベートエンドポイント接続を許可するには（テストまたはオープンアクセスのため）、 **[VPCエンドポイントID]**フィールドにアスタリスク( `*` )を1つ入力します。

5.  **「送信」**をクリックしてください。

### ステップ4. TiDB Cloud StarterまたはEssentialインスタンスに接続します {#step-4-connect-to-your-tidb} {#step-4-connect-to-your-tidb}

インターフェースエンドポイントを作成したら、 TiDB Cloudコンソールに戻り、以下の手順を実行してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。
5.  接続文字列を使用して、 TiDB Cloud StarterまたはEssentialインスタンスに接続します。

> **ヒント：**
>
> TiDB Cloud StarterまたはEssentialインスタンスに接続できない場合、AWSのVPCエンドポイントのセキュリティグループが正しく設定されていないことが原因である可能性があります。解決策については、[このFAQ](#troubleshooting)ご覧ください。
>
> VPCエンドポイントを作成する際に、 `private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`というエラーが発生した場合は、そのVPC内に既にプライベートエンドポイントが存在します。同じプライベートDNS名で別のエンドポイントを作成する必要はありません。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialインスタンスに接続できません。なぜでしょうか？ {#i-cannot-connect-to-a-tidb-cloud-starter-or-essential-instance-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで**、** VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。VPC &gt;**エンドポイント**に移動します。VPC エンドポイントを右クリックし、適切な**セキュリティ グループの管理**を選択します。VPC 内に、EC2 インスタンスからのポート 4000 またはお客様定義のポートへの受信アクセスを許可する適切なセキュリティ グループを設定します。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
