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

## エンドポイントモデルを選択する {#choose-an-endpoint-model}

TiDB Cloudプランに応じて、適切なプライベートエンドポイントモデルを選択してください。

- {{{ .starter }}} インスタンス、または2026年7月1日より前に作成された {{{ .essential }}} インスタンスの場合は、[**endpoint shared model**](#set-up-a-private-endpoint-with-aws-endpoint-shared-model) を使用します。このモデルでは、同じAWSリージョンおよびVPC内の複数の {{{ .starter }}} または {{{ .essential }}} インスタンスで、1つのプライベートエンドポイントを共有できます。
- 2026年7月1日以降に作成された {{{ .essential }}} インスタンスの場合は、[**エンドポイント占有モデル**](#set-up-a-private-endpoint-with-aws-endpoint-exclusive-model) を使用します。このモデルでは、各 {{{ .essential }}} インスタンスが専用のスタンドアロンプライベートエンドポイントを使用します。このモデルでは接続時に [アカウントプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix) を含める必要がありませんが、各 {{{ .essential }}} インスタンスごとに設定手順を繰り返す必要があります。

## AWSでプライベートエンドポイントを設定する（endpoint shared model） {#set-up-a-private-endpoint-with-aws-endpoint-shared-model}

共有モデルを使用して {{{ .starter }}} または {{{ .essential }}} インスタンスにプライベートエンドポイント経由で接続するには、以下の手順に従ってください。

1. [{{{ .starter }}} または Essential インスタンスを選択する](#step-1-choose-a-tidb-instance)
2. [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3. [TiDB Cloudでプライベートエンドポイントを認証する（オプション）](#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional)
4. [{{{ .starter }}} または Essential インスタンスに接続する](#step-4-connect-to-your-tidb)

### ステップ1. TiDB Cloud StarterまたはEssentialインスタンスを選択します {#step-1-choose-a-tidb-instance} {#step-1-choose-a-tidb-instance}

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **サービス名**、**アベイラビリティゾーンID** 、**リージョンID**をメモしておいてください。

    > **注記：**
    >
    > AWSリージョン内の各VPCにつき、作成する必要があるプライベートエンドポイントは1つだけです。このエンドポイントは、同じAWSリージョン内の同じVPCにあるすべてのTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスで使用できますが、VPC間で共有することはできません。

## AWSでプライベートエンドポイントを設定する（endpoint exclusive model） {#set-up-a-private-endpoint-with-aws-endpoint-exclusive-model}

> **Note:**
>
> 現在、endpoint exclusive model は、一部のAWSリージョンにおいて、2026年7月1日以降に作成された {{{ .essential }}} インスタンスでのみ利用できます。お使いのインスタンスで利用できない場合は、代わりに [endpoint shared model](#set-up-a-private-endpoint-with-aws-endpoint-shared-model) を使用できます。

エンドポイント占有モデルでは、各 {{{ .essential }}} インスタンスが専用のスタンドアロンプライベートエンドポイントを使用します。このモデルでは接続時に [アカウントプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix) を含める必要がありませんが、各 {{{ .essential }}} インスタンスごとに設定手順を繰り返す必要があります。

占有モデルを使用して {{{ .essential }}} インスタンスにプライベートエンドポイント経由で接続するには、次の手順を実行します。

1. [{{{ .essential }}} インスタンスを選択する](#step-1-select-an-essential-instance)
2. [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint-exclusive-model)
3. [プライベートエンドポイント接続を作成する](#step-3-create-a-private-endpoint-connection-exclusive-model)
4. [プライベートDNSを有効にする](#step-4-enable-private-dns-exclusive-model)
5. [{{{ .essential }}} インスタンスに接続する](#step-5-connect-to-your-essential-instance)

複数のインスタンスがある場合、AWS PrivateLink を使用して接続する各インスタンスごとに、これらの手順を繰り返す必要があります。

### ステップ1. {{{ .essential }}} インスタンスを選択する {#step-1-select-an-essential-instance}

1. TiDB Cloudコンソールの [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象の {{{ .essential }}} インスタンスの名前をクリックして、その概要ページに移動します。
2. 右上隅の **Connect** をクリックします。接続ダイアログが表示されます。
3. **Connection Type** ドロップダウンリストで **Private Endpoint** を選択し、 **Create Private Endpoint Connection** をクリックします。

> **Note:**
>
> すでにプライベートエンドポイント接続を作成している場合、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで **Settings** > **Networking** をクリックして **Networking** ページに移動します。

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

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint-exclusive-model}

> **Note:**
>
> 各 {{{ .essential }}} インスタンスについて、対応するエンドポイントサービスはインスタンス作成後3〜4分で自動的に作成されます。

接続ダイアログに `TiDB Private Link Service is ready` メッセージが表示された場合、対応するエンドポイントサービスの準備ができています。エンドポイントを作成するために、以下の情報を指定できます。

1. 接続ダイアログで **How to Generate VPC Endpoint ID** をクリックし、 **Your VPC ID** フィールドと **Your Subnet IDs** フィールドに入力します。これらのIDは [AWS Management Console](https://console.aws.amazon.com/) で確認できます。複数のサブネットがある場合は、IDをスペースで区切って入力します。

2. **Generate Command** をクリックして、次のエンドポイント作成コマンドを取得します。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

その後、AWS CLI または [AWS Management Console](https://aws.amazon.com/console/) を使用してAWSインターフェースエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してVPCインターフェースエンドポイントを作成するには、次の手順を実行します。

1. 生成されたコマンドをコピーし、ターミナルで実行します。
2. 作成したVPCエンドポイントIDを記録します。

> **Tip:**
>
> - コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) を参照してください。
>
> - サービスが3つを超えるアベイラビリティゾーン（AZ）にまたがる場合、VPCエンドポイントサービスがサブネットのAZをサポートしていないことを示すエラーメッセージが表示されます。この問題は、選択したリージョンに、{{{ .essential }}} インスタンスが配置されているAZに加えて余分なAZがある場合に発生します。この場合は、[PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。

</div>
<div label="Use AWS Console">

AWS Management Console を使用してVPCインターフェースエンドポイントを作成するには、次の手順を実行します。

1. [AWS Management Console](https://aws.amazon.com/console/) にサインインし、[https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) でAmazon VPCコンソールを開きます。
2. ナビゲーションペインで **Endpoints** をクリックし、右上隅の **Create Endpoint** をクリックします。

    **Create endpoint** ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. **Endpoint settings** エリアで、必要に応じてネームタグを入力し、 **Endpoint services that use NLBs and GWLBs** オプションを選択します。
4. **Service settings** エリアで、生成されたコマンドの (`--service-name ${your_endpoint_service_name}`) からサービス名 `${your_endpoint_service_name}` を入力します。
5. **Verify service** をクリックします。
6. **Network settings** エリアで、ドロップダウンリストからVPCを選択します。
7. **Subnets** エリアで、{{{ .essential }}} インスタンスが配置されているアベイラビリティゾーンを選択します。

    > **Tip:**
    >
    > サービスが3つを超えるアベイラビリティゾーン（AZ）にまたがる場合、 **Subnets** エリアでAZを選択できないことがあります。この問題は、選択したリージョンに、{{{ .essential }}} インスタンスが配置されているAZに加えて余分なAZがある場合に発生します。この場合は、[PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。

8. **Security groups** エリアで、適切なセキュリティグループを選択します。

    > **Note:**
    >
    > 選択したセキュリティグループが、EC2インスタンスからポート `4000` またはカスタマー定義ポートへのインバウンドアクセスを許可していることを確認してください。

9. **Create endpoint** をクリックします。

</div>
</SimpleTab>

### ステップ3. プライベートエンドポイント接続を作成する {#step-3-create-a-private-endpoint-connection-exclusive-model}

1. TiDB Cloudコンソールに戻ります。
2. **Create AWS Private Endpoint Connection** ページで、VPCエンドポイントIDを入力します。
3. **Create Private Endpoint Connection** をクリックします。

> **Tip:**
>
> 対象の {{{ .essential }}} インスタンスの **Networking** ページで、プライベートエンドポイント接続を表示および管理できます。このページにアクセスするには、左側のナビゲーションペインで **Settings** > **Networking** をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns-exclusive-model}

AWSでプライベートDNSを有効にします。AWS CLI または AWS Management Console のいずれかを使用できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してプライベートDNSを有効にするには、 **Create Private Endpoint Connection** ページから次の `aws ec2 modify-vpc-endpoint` コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

または、インスタンスの **Networking** ページでこのコマンドを確認することもできます。プライベートエンドポイントを見つけて、 **Action** カラムの **...** > **Enable DNS** をクリックします。

</div>
<div label="Use AWS Console">

AWS Management Console でプライベートDNSを有効にするには、次の手順を実行します。

1. **VPC** > **Endpoints** に移動します。
2. エンドポイントIDを右クリックし、 **Modify private DNS name** を選択します。
3. **Enable for this endpoint** チェックボックスを選択します。
4. **Save changes** をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### ステップ5. {{{ .essential }}} インスタンスに接続する {#step-5-connect-to-your-essential-instance}

プライベートエンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1. プライベートエンドポイント接続のステータスが **System Checking** から **Active** に変わるまで待ちます（約5分）。
2. **Connect With** ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3. 接続文字列を使用してインスタンスに接続します。

> **Tip:**
>
> インスタンスに接続できない場合、原因はAWS内のVPCエンドポイントのセキュリティグループが適切に設定されていないことかもしれません。解決策については [this FAQ](#troubleshooting) を参照してください。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialインスタンスに接続できません。なぜでしょうか？ {#i-cannot-connect-to-a-tidb-cloud-starter-or-essential-instance-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで**、** VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。VPC &gt;**エンドポイント**に移動します。VPC エンドポイントを右クリックし、適切な**セキュリティ グループの管理**を選択します。VPC 内に、EC2 インスタンスからのポート 4000 またはお客様定義のポートへの受信アクセスを許可する適切なセキュリティ グループを設定します。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
