---
title: Connect to a TiDB Cloud Premium Instance via AWS PrivateLink
summary: AWS のプライベートエンドポイント経由でTiDB Cloud Premium インスタンスに接続する方法を学習します。
---

# AWS PrivateLink 経由でTiDB Cloud Premium インスタンスに接続する {#connect-to-a-tidb-cloud-premium-instance-via-aws-privatelink}

このドキュメントでは、 [AWS プライベートリンク](https://aws.amazon.com/privatelink)経由でTiDB Cloud Premium インスタンスに接続する方法について説明します。

> **ヒント：**
>
> AWS PrivateLink 経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud Starter または Essential に接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

TiDB Cloudは、 AWS VPCでホストされているTiDB Cloudサービスへの、 [AWS プライベートリンク](https://aws.amazon.com/privatelink)経由の高度に安全な一方向アクセスをサポートします。まるでお客様のVPC内にあるかのように機能します。VPC内にプライベートエンドポイントが公開されており、権限があればエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートであり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   プライベート エンドポイント接続を作成できるのは、ロール`Organization Owner`を持つユーザーのみです。
-   プライベート エンドポイントと接続先の TiDB インスタンスは、同じリージョンに配置されている必要があります。

## 前提条件 {#prerequisites}

AWS VPC設定でDNSホスト名とDNS解決の[AWS マネジメントコンソール](https://console.aws.amazon.com/)が有効になっていることを確認してください。1でVPCを作成すると、これらはデフォルトで無効になります。

## プライベートエンドポイント接続を設定し、インスタンスに接続する {#set-up-a-private-endpoint-connection-and-connect-to-your-instance}

プライベート エンドポイント経由でTiDB Cloud Premium インスタンスに接続するには、次の手順に従います。

1.  [TiDBインスタンスを選択](#step-1-select-a-tidb-instance)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [プライベートエンドポイント接続を作成する](#step-3-create-a-private-endpoint-connection)
4.  [プライベートDNSを有効にする](#step-4-enable-private-dns)
5.  [TiDBインスタンスに接続する](#step-5-connect-to-your-tidb-instance)

複数のインスタンスがある場合は、AWS PrivateLink を使用して接続するインスタンスごとにこれらの手順を繰り返す必要があります。

### ステップ1. TiDBインスタンスを選択する {#step-1-select-a-tidb-instance}

1.  TiDB Cloud Web コンソールの[**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページで、対象の TiDB インスタンスの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  [**接続タイプ]**ドロップダウン リストで**[プライベート エンドポイント]**を選択し、 **[プライベート エンドポイント接続の作成]**をクリックします。

> **注記：**
>
> プライベートエンドポイント接続を既に作成している場合は、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**[設定]** &gt; **[ネットワーク]**をクリックして**[ネットワーク]**ページに移動します。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

> **注記：**
>
> 各TiDB Cloud Premium インスタンスでは、インスタンスの作成後 3 ～ 4 分以内に、対応するエンドポイント サービスが自動的に作成されます。

`TiDB Private Link Service is ready`メッセージが表示された場合、対応するエンドポイントサービスは準備完了です。エンドポイントを作成するには、以下の情報を提供してください。

1.  **「VPC ID」**と**「サブネットID」**のフィールドに入力します。これらのIDは[AWS マネジメントコンソール](https://console.aws.amazon.com/)で確認できます。サブネットが複数ある場合は、IDをスペースで区切って入力してください。
2.  **[コマンドの生成]**をクリックすると、次のエンドポイント作成コマンドが取得されます。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

次に、AWS CLI または[AWS マネジメントコンソール](https://aws.amazon.com/console/)を使用して AWS インターフェイスエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  生成されたコマンドをコピーしてターミナルで実行します。
2.  作成した VPC エンドポイント ID を記録します。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細は[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。
>
> -   サービスが3つ以上のアベイラビリティゾーン（AZ）にまたがっている場合、VPCエンドポイントサービスがサブネットのAZをサポートしていないことを示すエラーメッセージが表示されます。この問題は、選択したリージョンに、TiDBインスタンスが配置されているAZに加えて、追加のAZが存在する場合に発生します。この場合、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **エンドポイント設定**領域で、必要に応じて名前タグを入力し、 **NLB および GWLB を使用するエンドポイント サービス**オプションを選択します。

4.  **サービス設定**領域に、生成されたコマンド（ `--service-name ${your_endpoint_service_name}` ）のサービス名`${your_endpoint_service_name}`入力します。

5.  **[サービスの確認]**をクリックします。

6.  **ネットワーク設定**領域で、ドロップダウンリストから VPC を選択します。

7.  **[サブネット]**領域で、TiDB インスタンスが配置されているアベイラビリティーゾーンを選択します。

    > **ヒント：**
    >
    > サービスが3つ以上のアベイラビリティゾーン（AZ）にまたがっている場合、 **「サブネット**」エリアでAZを選択できない場合があります。この問題は、選択したリージョンに、TiDBインスタンスが配置されているAZに加えて、追加のAZが存在する場合に発生します。その場合は、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

8.  **[Securityグループ]**領域で、セキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループが、ポート`4000`または顧客定義のポート上の EC2 インスタンスからのインバウンド アクセスを許可していることを確認します。

9.  **[エンドポイントの作成]**をクリックします。

</div>
</SimpleTab>

### ステップ3. プライベートエンドポイント接続を作成する {#step-3-create-a-private-endpoint-connection}

1.  TiDB Cloudコンソールに戻ります。
2.  **「AWS プライベートエンドポイント接続の作成**」ページで、VPC エンドポイント ID を入力します。
3.  **[プライベート エンドポイント接続の作成]**をクリックします。

> **ヒント：**
>
> プライベートエンドポイント接続は、ターゲットTiDBインスタンスの**「ネットワーク」**ページで表示および管理できます。このページにアクセスするには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックします。

### ステップ4. プライベートDNSを有効にする {#step-4-enable-private-dns}

AWSでプライベートDNSを有効にします。AWS CLIまたはAWSマネジメントコンソールを使用できます。

<SimpleTab>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、 **「プライベートエンドポイント接続の作成」**ページから次の`aws ec2 modify-vpc-endpoint`コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

または、インスタンスの**「ネットワーク」**ページでコマンドを見つけることもできます。プライベートエンドポイントを探し、 **「アクション」**列の**「...」** &gt; **「DNSを有効にする」**をクリックします。

</div>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには:

1.  **VPC** &gt;**エンドポイント**に移動します。
2.  エンドポイント ID を右クリックし、 **[プライベート DNS 名の変更]**を選択します。
3.  **このエンドポイントに対して有効にする**チェックボックスをオンにします。
4.  **[変更を保存]**をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
</SimpleTab>

### ステップ5. TiDBインスタンスに接続する {#step-5-connect-to-your-tidb-instance}

プライベート エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベート エンドポイントの接続ステータスが**「システム チェック中」**から**「アクティブ」**に変わるまで待ちます (約 5 分)。
2.  **「接続方法」**ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してインスタンスに接続します。

> **ヒント：**
>
> インスタンスに接続できない場合は、AWS の VPC エンドポイントのセキュリティグループが正しく設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)ご覧ください。

### プライベートエンドポイントのステータスリファレンス {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、インスタンス レベルの**[ネットワーク]**ページにプライベート エンドポイントとプライベート エンドポイント サービスのステータスが表示されます。

1.  左上隅のコンボ ボックスを使用して、ターゲット インスタンスに切り替えます。
2.  左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

プライベート エンドポイントの可能なステータスについては、次のように説明されます。

-   **未構成**: エンドポイント サービスは作成されていますが、プライベート エンドポイントはまだ作成されていません。
-   **保留中**: 処理を待機中です。
-   **アクティブ**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントを削除しています。
-   **失敗**: プライベートエンドポイントの作成に失敗しました。その行の**「編集」を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスについては、次のように説明されます。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **アクティブ**: プライベート エンドポイントが作成されたかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除中**: エンドポイント サービスまたはインスタンスを削除中です。これには 3 ～ 5 分かかります。

## トラブルシューティング {#troubleshooting}

### プライベートDNSを有効にした後、プライベートエンドポイント経由でTiDBインスタンスに接続できません。なぜですか？ {#i-cannot-connect-to-a-tidb-instance-via-a-private-endpoint-after-enabling-private-dns-why}

AWSマネジメントコンソールで、VPCエンドポイントのセキュリティグループを適切に設定する必要がある場合があります。設定するには、 **「VPC」** &gt; **「エンドポイント」**に移動し、VPCエンドポイントを右クリックして**「セキュリティグループの管理」**を選択します。選択したセキュリティグループが、ポート`4000`またはお客様定義のポートでEC2インスタンスからのインバウンドアクセスを許可していることを確認してください。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)
