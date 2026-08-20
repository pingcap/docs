---
title: Connect to TiDB Cloud Premium via AWS PrivateLink
summary: AWSのプライベートエンドポイントを使用して、 TiDB Cloud Premiumインスタンスに接続する方法を学びましょう。
---

# AWS PrivateLink経由でTiDB Cloud Premiumに接続します。 {#connect-to-tidb-cloud-premium-via-aws-privatelink}

このドキュメントでは、[AWS PrivateLink](https://aws.amazon.com/privatelink) 経由で {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスに接続する方法について説明します。

> **Tip:**
>
> AWS PrivateLink 経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

TiDB Cloudは、 AWS VPC内でホストされているTiDB Cloudサービスへの高度に安全な一方向アクセスを[AWSプライベートリンク](https://aws.amazon.com/privatelink)経由でサポートしており、まるでサービスがお客様自身のVPC内にあるかのように動作します。お客様のVPC内にプライベートエンドポイントが公開され、権限があればそのエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用したエンドポイント接続は、安全かつプライベートであり、お客様のデータをパブリックインターネットに公開することはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

プライベートエンドポイントのアーキテクチャは以下のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントおよびエンドポイントサービスのより詳細な定義については、以下のAWSドキュメントを参照してください。

-   [AWS PrivateLinkとは何ですか？](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLinkの概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   対象インスタンスの `Organization Owner`、`Project Owner`、または `Instance Owner` ロールを持つユーザーのみがプライベートエンドポイント接続を作成できます。
-   接続先のプライベートエンドポイントと {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスは、**同じリージョン** に配置されている必要があります。

## 前提条件 {#prerequisites}

AWS VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。 [AWS マネジメントコンソール](https://console.aws.amazon.com/)で VPC を作成すると、デフォルトでは無効になります。

## プライベートエンドポイント接続を設定し、インスタンスに接続します。 {#set-up-a-private-endpoint-connection-and-connect-to-your-instance}

プライベートエンドポイント経由で{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスに接続するには、以下の手順に従ってください。

1. [プライベートエンドポイント接続ダイアログを開く](#step-1-open-the-private-endpoint-connection-dialog)
2. [AWS で VPC エンドポイントを作成する](#step-2-create-a-vpc-endpoint-in-aws)
3. [TiDB Cloud で VPC エンドポイント ID を入力する](#step-3-enter-the-vpc-endpoint-id-in-tidb-cloud)
4. [プライベートDNSを有効にする](#step-4-enable-private-dns)
5. [{{{ .premium }}} <CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスに接続する](#step-5-connect-to-your-premium-instance)

複数のインスタンスがある場合は、AWS PrivateLinkを使用して接続したいインスタンスごとに、これらの手順を繰り返す必要があります。

### Step 1. プライベートエンドポイント接続ダイアログを開く {#step-1-open-the-private-endpoint-connection-dialog}

1. TiDB Cloud コンソールの [**My TiDB**](https://tidbcloud.com/tidbs) ページで、対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンス名をクリックして、その概要ページに移動します。
2. 右上隅の **Connect** をクリックします。接続ダイアログが表示されます。
3. **Connection Type** ドロップダウンリストで **Private Endpoint** を選択し、**Create Private Endpoint Connection** をクリックします。
4. **Create AWS Private Endpoint Connection** ダイアログで、`TiDB Private Link Service is ready` メッセージが表示されるまで待ちます。
5. **Endpoint Service Name** をコピーします。

> **Note:**
>
> - すでにプライベートエンドポイント接続を作成している場合、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで **Settings** > **Networking** をクリックして **Networking** ページに移動します。
> - 各 {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスについて、対応するエンドポイントサービスはインスタンス作成後 3 ～ 4 分で自動的に作成されます。

### Step 2. AWS で VPC endpoint を作成する {#step-2-create-a-vpc-endpoint-in-aws}

endpoint service の準備ができたら、AWS アカウントで VPC interface endpoint を作成します。TiDB Cloud が生成した AWS CLI コマンドを使用することも、AWS Management Console で endpoint を手動で作成することもできます。

TiDB Cloud で AWS CLI コマンドを生成するには、**Create AWS Private Endpoint Connection** ダイアログで **How to Generate VPC Endpoint ID** を展開し、次の操作を行います。

1. **Your VPC ID** を入力します。
2. **Your Subnet IDs** を入力します。複数の subnet を指定する場合は、subnet ID をスペースで区切ります。
3. subnet がダイアログでサポートされている availability zone にあることを確認します。他の availability zone の subnet は使用しないでください。
4. **Generate Command** をクリックします。

生成されるコマンドは次のようになります。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
```

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用して VPC endpoint を作成するには、次の手順を実行します。

1. TiDB Cloud で生成されたコマンドをコピーします。
2. ターミナルでコマンドを実行します。
3. AWS から返される VPC endpoint ID を記録します。VPC endpoint ID は `vpce-` で始まります。

> **Tip:**
>
> - コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は [AWS CLI configuration basics](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) を参照してください。
>
> - サービスが 3 つを超える availability zone (AZ) にまたがっている場合、VPC endpoint service が subnet の AZ をサポートしていないことを示すエラーメッセージが表示されます。この問題は、選択したリージョンに、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスが配置されている AZ に加えて、余分な AZ が存在する場合に発生します。この場合は、[PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。

</div>
<div label="Use AWS Console">

AWS Management Console を使用して VPC endpoint を作成するには、次の手順を実行します。

1. [AWS Management Console](https://aws.amazon.com/console/) にサインインし、[https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/) で Amazon VPC コンソールを開きます。
2. ナビゲーションペインで **Endpoints** をクリックし、右上隅の **Create Endpoint** をクリックします。

    **Create endpoint** ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3. **Endpoint settings** エリアで、必要に応じて name tag を入力し、**Endpoint services that use NLBs and GWLBs** オプションを選択します。
4. **Service settings** エリアで、TiDB Cloud からコピーした **Endpoint Service Name** を入力します。
5. **Verify service** をクリックします。
6. **Network settings** エリアで、ドロップダウンリストから VPC を選択します。
7. **Subnets** エリアで、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスが配置されている availability zone を選択します。

    > **Tip:**
    >
    > サービスが 3 つを超える availability zone (AZ) にまたがっている場合、**Subnets** エリアで AZ を選択できないことがあります。この問題は、選択したリージョンに、{{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスが配置されている AZ に加えて、余分な AZ が存在する場合に発生します。この場合は、[PingCAP Technical Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) にお問い合わせください。

8. **Security groups** エリアで、適切な security group を選択します。

    > **Note:**
    >
    > 選択した security group が、EC2 インスタンスからポート `4000` またはユーザー定義ポートへの inbound access を許可していることを確認してください。

9. **Create endpoint** をクリックします。
10. endpoint の作成後、その VPC endpoint ID を記録します。VPC endpoint ID は `vpce-` で始まります。

</div>
</SimpleTab>

### Step 3. TiDB Cloud で VPC endpoint ID を入力する {#step-3-enter-the-vpc-endpoint-id-in-tidb-cloud}

1. TiDB Cloud コンソールに戻ります。
2. **Create AWS Private Endpoint Connection** ダイアログで、AWS で作成した VPC endpoint ID を **Your VPC Endpoint ID** フィールドに入力します。
3. **Create Private Endpoint** をクリックします。

> **Tip:**
>
> プライベートエンドポイント接続は、対象の {{{ .premium }}}<CustomContent plan="byoc"> または {{{ .byoc }}}</CustomContent> インスタンスの **Networking** ページで表示および管理できます。このページにアクセスするには、左側のナビゲーションペインで **Settings** > **Networking** をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns}

TiDB Cloud でプライベートエンドポイントを作成したら、プライベートエンドポイント接続を完了するために AWS でプライベート DNS を有効にします。TiDB Cloud では、**Create AWS Private Endpoint Connection** ダイアログに `aws ec2 modify-vpc-endpoint` コマンドが表示されます。このコマンドは後から **Networking** ページでも取得できます。

<SimpleTab>
<div label="Use command generated by TiDB Cloud">

TiDB Cloud によって生成されたコマンドを使用してプライベート DNS を有効にするには、次の手順を実行します。

1. 次のいずれかの場所から `aws ec2 modify-vpc-endpoint` コマンドをコピーします。

    - プライベートエンドポイントの作成後に表示される **Create AWS Private Endpoint Connection** ダイアログ
    - インスタンスの **Networking** ページで、**AWS Private Endpoint** エリアにある対象のプライベートエンドポイントの **...** > **Enable DNS** をクリックします。

2. AWS CLI でコマンドを実行します。

    ```bash
    aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --region ${your_region} --private-dns-enabled
    ```

3. コマンドが正常に実行されたら、TiDB Cloud のダイアログに戻り、**Done** をクリックします。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには：

1. **VPC** > **Endpoints** に移動します。
2. エンドポイント ID を右クリックし、**Modify private DNS name** を選択します。
3. **Enable for this endpoint** チェックボックスを選択します。
4. **Save changes** をクリックします。
5. TiDB Cloud に戻り、**Create AWS Private Endpoint Connection** または **Enable DNS** ダイアログで **Done** をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### ステップ5．TiDB Cloud Premiumインスタンスに接続します {#step-5-connect-to-your-premium-instance} {#step-5-connect-to-your-premium-instance}

プライベートエンドポイント接続が作成されると、接続ダイアログにリダイレクトされます。

1. プライベートエンドポイント接続のステータスが **System Checking** から **Active** に変わるまで待機してください（約 5 分）。
2. **Connection Type** ドロップダウンリストで、**Private Endpoint** を選択します。
3. **Endpoint ID** ドロップダウンリストで、使用するアクティブな VPC エンドポイントを選択します。

    **Endpoint ID** ドロップダウンリストには、アクティブなエンドポイントのみが表示されます。さらにエンドポイントを追加するには、**Networking** ページに移動してください。

4. **Connect With** ドロップダウンリストで、希望する接続方法を選択します。
5. インスタンスに root パスワードが設定されていない場合は、**Set Root Password** をクリックして、先にパスワードを設定してください。
6. ダイアログから接続パラメータまたは接続文字列をコピーし、その後インスタンスに接続します。

> **Tip:**
>
> インスタンスに接続できない場合、AWS の VPC エンドポイントのセキュリティ グループが正しく設定されていないことが原因である可能性があります。解決策については、[このFAQ](#troubleshooting)を参照してください。

### プライベートエンドポイントの状態参照 {#private-endpoint-status-reference}

プライベートエンドポイント接続を使用する場合、プライベートエンドポイントおよびプライベートエンドポイントサービスのステータスは、インスタンスレベルの**ネットワーク**ページに表示されます。

1. 組織の[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象の{{{ .premium }}}<CustomContent plan="byoc">または{{{ .byoc }}}</CustomContent>インスタンスの名前をクリックして、その概要ページに移動します。
2. 左側のナビゲーションペインで、**Settings** > **Networking**をクリックします。

プライベートエンドポイントの可能なステータスは、以下のように説明されます。

-   **Not Configured**：エンドポイントサービスは作成されていますが、プライベートエンドポイントはまだ作成されていません。
-   **保留中**：処理待ちです。
-   **アクティブ**：プライベートエンドポイントは使用可能です。この状態ではプライベートエンドポイントを編集することはできません。
-   **削除中**：プライベートエンドポイントが削除されています。
-   **失敗**：プライベートエンドポイントの作成に失敗しました。該当行の**編集**をクリックすると、作成を再試行できます。

プライベートエンドポイントサービスの可能なステータスは、以下のように説明されます。

-   **作成中**：エンドポイントサービスを作成中です。これには3～5分かかります。
-   **アクティブ**：プライベートエンドポイントが作成されるかどうかに関わらず、エンドポイントサービスが作成されます。
-   **削除中**：エンドポイントサービスまたはインスタンスが削除されています。これには3～5分かかります。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDB Cloud Premiumインスタンスに接続できません。なぜでしょうか？ {#i-cannot-connect-to-a-tidb-cloud-premium-instance-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで、VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。そのためには、 **[VPC]** &gt; **[エンドポイント]**に移動し、VPC エンドポイントを右クリックして、 **Manage security groups**を選択します。選択したセキュリティ グループが、ポート`4000`またはお客様定義のポートで EC2 インスタンスからの受信アクセスを許可していることを確認してください。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
