---
title: Connect to TiDB Cloud Premium via AWS PrivateLink
summary: AWSのプライベートエンドポイントを使用して、 TiDB Cloud Premiumインスタンスに接続する方法を学びましょう。
---

# AWS PrivateLink経由でTiDB Cloud Premiumに接続します。 {#connect-to-tidb-cloud-premium-via-aws-privatelink}

このドキュメントでは[AWSプライベートリンク](https://aws.amazon.com/privatelink)経由でTiDB Cloud Premium インスタンスに接続する方法について説明します。

> **ヒント：**
>
> AWS PrivateLink 経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

TiDB Cloudは、 AWS VPC内でホストされているTiDB Cloudサービスへの高度に安全な一方向アクセスを[AWSプライベートリンク](https://aws.amazon.com/privatelink)経由でサポートしており、まるでサービスがお客様自身のVPC内にあるかのように動作します。お客様のVPC内にプライベートエンドポイントが公開され、権限があればそのエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用したエンドポイント接続は、安全かつプライベートであり、お客様のデータをパブリックインターネットに公開することはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

プライベートエンドポイントのアーキテクチャは以下のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントおよびエンドポイントサービスのより詳細な定義については、以下のAWSドキュメントを参照してください。

-   [AWS PrivateLinkとは何ですか？](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLinkの概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   `Organization Owner`ロールを持つユーザーのみがプライベートエンドポイント接続を作成できます。
-   接続先のプライベートエンドポイントとTiDB Cloud Premiumインスタンスは、同じリージョンに配置されている必要があります。

## 前提条件 {#prerequisites}

AWS VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。 [AWS マネジメントコンソール](https://console.aws.amazon.com/)で VPC を作成すると、デフォルトでは無効になります。

## プライベートエンドポイント接続を設定し、インスタンスに接続します。 {#set-up-a-private-endpoint-connection-and-connect-to-your-instance}

プライベートエンドポイント経由でTiDB Cloud Premiumインスタンスに接続するには、以下の手順に従ってください。

1.  [TiDB Cloud Premiumインスタンスを選択してください](#step-1-select-a-premium-instance)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [プライベートエンドポイント接続を作成する](#step-3-create-a-private-endpoint-connection)
4.  [プライベートDNSを有効にする](#step-4-enable-private-dns)
5.  [TiDB Cloud Premiumインスタンスに接続します](#step-5-connect-to-your-premium-instance)

複数のインスタンスがある場合は、AWS PrivateLinkを使用して接続したいインスタンスごとに、これらの手順を繰り返す必要があります。

### ステップ1. TiDB Cloud Premiumインスタンスを選択します {#step-1-select-a-premium-instance} {#step-1-select-a-premium-instance}

1.  TiDB Cloudコンソールの[**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Premium インスタンスの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで**「プライベートエンドポイント」**を選択し、 **「プライベートエンドポイント接続の作成」を**クリックします。

> **注記：**
>
> 既にプライベートエンドポイント接続を作成済みの場合、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックして、 **「ネットワーク」**ページに移動します。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

> **注記：**
>
> TiDB Cloud Premiumの各インスタンスに対して、対応するエンドポイントサービスは、インスタンス作成後3～4分で自動的に作成されます。

`TiDB Private Link Service is ready`というメッセージが表示された場合、対応するエンドポイントサービスが準備完了です。エンドポイントを作成するには、以下の情報を提供してください。

1.  **「VPC ID」**フィールドと**「サブネット ID」**フィールドに入力します。これらの ID は[AWS マネジメントコンソール](https://console.aws.amazon.com/)コンソールから見つけることができます。複数のサブネットの場合は、ID をスペースで区切って入力します。
2.  **「コマンド生成」を**クリックすると、以下のエンドポイント作成コマンドが表示されます。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

次に、AWS CLI または[AWS マネジメントコンソール](https://aws.amazon.com/console/)コンソールを使用して、AWS インターフェイスエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  生成されたコマンドをコピーして、ターミナルで実行してください。
2.  先ほど作成したVPCエンドポイントIDを記録してください。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細については、 [AWS CLI設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> -   サービスが3つ以上の可用性ゾーン（AZ）にまたがっている場合、VPCエンドポイントサービスがサブネットのAZをサポートしていないことを示すエラーメッセージが表示されます。この問題は、TiDB Cloud Premiumインスタンスが配置されているAZに加えて、選択したリージョンに別のAZが存在する場合に発生します。この場合は、 [PingCAPテクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)TiDB Cloudサポートにお問い合わせください。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)コンソールにサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーションペインの**「エンドポイント」**をクリックし、右上隅の**「エンドポイントの作成」を**クリックします。

    **エンドポイント作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **エンドポイント設定**領域で、必要に応じて名前タグを入力し、次に**「NLBとGWLBを使用するエンドポイントサービス」**オプションを選択します。

4.  **サービス設定**エリアで、生成されたコマンド（ `${your_endpoint_service_name}` `--service-name ${your_endpoint_service_name}` }を入力します。

5.  **「サービスを確認する」**をクリックしてください。

6.  **ネットワーク設定**エリアで、ドロップダウンリストからVPCを選択します。

7.  **サブネット**領域で、 TiDB Cloud Premiumインスタンスが配置されているアベイラビリティゾーンを選択します。

    > **ヒント：**
    >
    > サービスが3つ以上の可用性ゾーン（AZ）にまたがっている場合、**サブネット**領域でAZを選択できない場合があります。この問題は、選択したリージョンに、 TiDB Cloud Premiumインスタンスが配置されているAZに加えて、さらに別のAZが存在する場合に発生します。この場合は、 [PingCAPテクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)エンドサポートにお問い合わせください。

8.  **Securityグループの**領域で、適切なセキュリティグループを選択してください。

    > **注記：**
    >
    > 選択したセキュリティグループが、ポート`4000`または顧客定義ポートでの EC2 インスタンスからの受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」を**クリックします。

</div>
</SimpleTab>

### ステップ3. プライベートエンドポイント接続を作成する {#step-3-create-a-private-endpoint-connection}

1.  TiDB Cloudコンソールに戻ってください。
2.  **AWSプライベートエンドポイント接続の作成**ページで、VPCエンドポイントIDを入力します。
3.  **「プライベートエンドポイント接続の作成」**をクリックします。

> **ヒント：**
>
> プライベートエンドポイント接続は、対象のTiDB Cloud Premiumインスタンスの**「ネットワーク」**ページで表示および管理できます。このページにアクセスするには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns}

AWSでプライベートDNSを有効にするには、AWS CLIまたはAWSマネジメントコンソールを使用できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、 **[プライベート エンドポイント接続の作成**] ページから次の`aws ec2 modify-vpc-endpoint`コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

または、インスタンスの**ネットワーク**ページでコマンドを見つけることもできます。プライベートエンドポイントを見つけて、 **[アクション]**列の**[...]** &gt; **[DNSを有効にする]**をクリックします。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには：

1.  **VPC** &gt;**エンドポイント**に移動します。
2.  エンドポイント ID を右クリックして、 **[プライベート DNS 名の変更]**を選択します。
3.  **「このエンドポイントを有効にする**」チェックボックスを選択してください。
4.  **「変更を保存」**をクリックしてください。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### ステップ5．TiDB Cloud Premiumインスタンスに接続します {#step-5-connect-to-your-premium-instance} {#step-5-connect-to-your-premium-instance}

プライベートエンドポイントへの接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベートエンドポイントの接続ステータスが**「システムチェック中**」から**「アクティブ」**に変わるまでお待ちください（約5分）。
2.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してインスタンスに接続してください。

> **ヒント：**
>
> インスタンスに接続できない場合、AWS の VPC エンドポイントのセキュリティ グループが正しく設定されていないことが原因である可能性があります。解決策については、[このFAQ](#troubleshooting)参照してください。

### プライベートエンドポイントの状態参照 {#private-endpoint-status-reference}

プライベートエンドポイント接続を使用する場合、プライベートエンドポイントおよびプライベートエンドポイントサービスのステータスは、インスタンスレベルの**ネットワーク**ページに表示されます。

1.  組織の[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。
2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

プライベートエンドポイントの可能なステータスは、以下のように説明されます。

-   **未設定**：エンドポイントサービスは作成されていますが、プライベートエンドポイントはまだ作成されていません。
-   **保留中**：処理待ちです。
-   **アクティブ**：プライベートエンドポイントは使用可能です。この状態ではプライベートエンドポイントを編集することはできません。
-   **削除中**：プライベートエンドポイントが削除されています。
-   **失敗**：プライベートエンドポイントの作成に失敗しました。該当行の**「編集」を**クリックすると、作成を再試行できます。

プライベートエンドポイントサービスの可能なステータスは、以下のように説明されます。

-   **作成中**：エンドポイントサービスを作成中です。これには3～5分かかります。
-   **アクティブ**：プライベートエンドポイントが作成されるかどうかに関わらず、エンドポイントサービスが作成されます。
-   **削除中**：エンドポイントサービスまたはインスタンスが削除されています。これには3～5分かかります。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDB Cloud Premiumインスタンスに接続できません。なぜでしょうか？ {#i-cannot-connect-to-a-tidb-cloud-premium-instance-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで、VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。そのためには、 **[VPC]** &gt; **[エンドポイント]**に移動し、VPC エンドポイントを右クリックして、 **[セキュリティ グループの管理]**を選択します。選択したセキュリティ グループが、ポート`4000`またはお客様定義のポートで EC2 インスタンスからの受信アクセスを許可していることを確認してください。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
