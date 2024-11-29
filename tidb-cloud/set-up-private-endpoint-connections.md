---
title: Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with AWS
summary: AWS を使用してプライベートエンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# AWS のプライベートエンドポイント経由でTiDB Cloud専用クラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-private-endpoint-with-aws}

このドキュメントでは、AWS のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **ヒント：**
>
> プライベート エンドポイント経由でTiDB Cloud Serverless クラスタに接続する方法については、 [プライベートエンドポイント経由でTiDB Cloud Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)ご覧ください。Google Cloud でプライベート エンドポイント経由でTiDB Cloud Dedicated クラスタに接続する方法については、 [プライベートサービス経由でTiDB Cloud Dedicatedに接続する Google Cloudに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。

TiDB Cloud は、 [AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)を介して AWS VPC でホストされているTiDB Cloudサービスへの、非常に安全な一方向アクセスをサポートします。これは、サービスが自分の VPC 内にある場合と同じです。プライベート エンドポイントが VPC で公開され、アクセス許可を持つエンドポイントを介してTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用することで、エンドポイント接続は安全かつプライベートになり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは何ですか?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   プライベート エンドポイントを作成できるのは、ロール`Organization Owner`と`Project Owner`のみです。
-   プライベート エンドポイントと接続する TiDB クラスターは同じリージョンに配置されている必要があります。

ほとんどのシナリオでは、VPC ピアリング経由のプライベート エンドポイント接続を使用することをお勧めします。ただし、次のシナリオでは、プライベート エンドポイント接続ではなく VPC ピアリングを使用する必要があります。

-   高可用性を実現するために、 [ティCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用して、ソース TiDB クラスターからリージョンをまたがるターゲット TiDB クラスターにデータをレプリケートしています。現在、プライベート エンドポイントはリージョン間の接続をサポートしていません。
-   TiCDC クラスターを使用してダウンストリーム クラスター (Amazon Aurora、MySQL、Kafka など) にデータを複製していますが、エンドポイント サービスを独自に維持することはできません。
-   PD または TiKV ノードに直接接続しています。

## プライベートエンドポイント接続を設定し、クラスターに接続する {#set-up-a-private-endpoint-connection-and-connect-to-your-cluster}

プライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続するには、次の手順を実行します。

1.  [TiDBクラスタを選択](#step-1-select-a-tidb-cluster)
2.  [AWSインターフェースエンドポイントを作成する](#step-2-create-an-aws-interface-endpoint)
3.  [エンドポイントIDを入力してください](#step-3-fill-in-your-endpoint-id)
4.  [プライベートDNSを有効にして接続を作成する](#step-4-enable-private-dns-and-create-connection)
5.  [TiDBクラスターに接続する](#step-5-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### ステップ1. TiDBクラスターを選択する {#step-1-select-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット TiDB クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  [**接続タイプ]**ドロップダウン リストで**[プライベート エンドポイント]**を選択し、 **[プライベート エンドポイント接続の作成]**をクリックします。

> **注記：**
>
> プライベート エンドポイント接続を既に作成している場合は、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベート エンドポイント接続を作成するには、左側のナビゲーション ペインの**[ネットワーク]**ページに移動します。

### ステップ2. AWSインターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

> **注記：**
>
> 2023 年 3 月 28 日以降に作成されたTiDB Cloud Dedicated クラスターごとに、クラスターの作成後 3 ～ 4 分後に対応するエンドポイント サービスが自動的に作成されます。

`TiDB Private Link Service is ready`メッセージが表示された場合、対応するエンドポイント サービスは準備ができています。エンドポイントを作成するには、次の情報を指定できます。

1.  **「VPC ID」**フィールドと**「サブネット ID」**フィールドに入力します。これらの ID は[AWS マネジメントコンソール](https://console.aws.amazon.com/)から確認できます。サブネットが複数ある場合は、ID をスペースで区切って入力します。
2.  **[コマンドの生成]**をクリックすると、次のエンドポイント作成コマンドが取得されます。

    ```bash
    aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
    ```

次に、 [AWS マネジメントコンソール](https://aws.amazon.com/console/)または AWS CLI を使用して AWS インターフェイスエンドポイントを作成できます。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [https://console.aws.amazon.com/vpc/](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **「その他のエンドポイント サービス」**を選択します。

4.  生成されたコマンド（ `--service-name ${your_endpoint_service_name}` ）からサービス名`${your_endpoint_service_name}`入力します。

5.  **[サービスの確認]**をクリックします。

6.  ドロップダウン リストから VPC を選択します。

7.  **サブネット**領域で、TiDB クラスターが配置されている可用性ゾーンを選択します。

    > **ヒント：**
    >
    > サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、**サブネット**領域で AZ を選択できないことがあります。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合は、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

8.  **Securityグループ**領域でセキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループが、ポート 4000 または顧客定義のポート上の EC2 インスタンスからの受信アクセスを許可していることを確認します。

9.  **[エンドポイントの作成]**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  生成されたコマンドをコピーして、ターミナルで実行します。
2.  作成した VPC エンドポイント ID を記録します。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細については[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)参照してください。
>
> -   サービスが 3 つ以上のアベイラビリティーゾーン (AZ) にまたがっている場合、VPC エンドポイント サービスがサブネットの AZ をサポートしていないことを示すエラー メッセージが表示されます。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。

</div>
</SimpleTab>

### ステップ3. エンドポイントIDを入力します {#step-3-fill-in-your-endpoint-id}

1.  TiDB Cloudコンソールに戻ります。
2.  **「AWS プライベートエンドポイント接続の作成**」ページで、VPC エンドポイント ID を入力します。

### ステップ4. プライベートDNSを有効にして接続を作成する {#step-4-enable-private-dns-and-create-connection}

AWS でプライベート DNS を有効にします。AWS マネジメントコンソールまたは AWS CLI を使用できます。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには:

1.  **VPC** &gt;**エンドポイント**に移動します。
2.  エンドポイント ID を右クリックし、 **[プライベート DNS 名の変更]**を選択します。
3.  **このエンドポイントに対して有効にする**チェックボックスをオンにします。
4.  **「変更を保存」**をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、 **「プライベートエンドポイント接続の作成」**ページから次の`aws ec2 modify-vpc-endpoint`コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

または、クラスターの**[ネットワーク]**ページでコマンドを見つけることもできます。プライベート エンドポイントを見つけて、 **[アクション**] 列の**[...** *] &gt; **[DNS を有効にする]**をクリックします。

</div>
</SimpleTab>

TiDB Cloudコンソールで**「プライベート エンドポイント接続の作成」**をクリックして、プライベート エンドポイントの作成を完了します。

その後、TiDB クラスターに接続できます。

> **ヒント：**
>
> プライベート エンドポイント接続は、次の 2 つのページで表示および管理できます。
>
> -   クラスター レベルの**ネットワーク**ページ: クラスターの概要ページの左側のナビゲーション ペインで**[ネットワーク]**をクリックします。
> -   プロジェクト レベルの**ネットワーク アクセス**ページ:**プロジェクト設定**ページの左側のナビゲーション ペインで**[ネットワーク アクセス]**をクリックします。

### ステップ5. TiDBクラスターに接続する {#step-5-connect-to-your-tidb-cluster}

プライベート エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベート エンドポイントの接続ステータスが**「システム チェック中」**から**「アクティブ」**に変わるまで待ちます (約 5 分)。
2.  **[接続方法]**ドロップダウン リストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してクラスターに接続します。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)参照してください。

### プライベートエンドポイントステータスリファレンス {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが次のページに表示されます。

-   クラスター レベルの**ネットワーク**ページ: クラスターの概要ページの左側のナビゲーション ペインで**[ネットワーク]**をクリックします。
-   プロジェクト レベルの**ネットワーク アクセス**ページ:**プロジェクト設定**ページの左側のナビゲーション ペインで**[ネットワーク アクセス]**をクリックします。

プライベート エンドポイントの可能なステータスは次のように説明されます。

-   **未構成**: エンドポイント サービスは作成されていますが、プライベート エンドポイントはまだ作成されていません。
-   **保留中**: 処理を待機しています。
-   **アクティブ**: プライベート エンドポイントは使用可能です。このステータスのプライベート エンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントを削除しています。
-   **失敗**: プライベート エンドポイントの作成に失敗しました。その行の**[編集] を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスは、次のように説明されます。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **アクティブ**: プライベート エンドポイントが作成されたかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除中**: エンドポイント サービスまたはクラスターを削除中です。これには 3 ～ 5 分かかります。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なぜですか? {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメントコンソールで、VPC エンドポイントのセキュリティグループを適切に設定する必要がある場合があります。 **[VPC]** &gt; **[エンドポイント]**に移動します。VPC エンドポイントを右クリックし、適切な**[セキュリティグループの管理]**を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからのインバウンドアクセスを許可する、VPC 内の適切なセキュリティグループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。enableDnsSupport および<code>enableDnsSupport</code> VPC 属性が<code>enableDnsHostnames</code>になっていないことを示すエラーが報告されます {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。AWS マネジメントコンソールで VPC を作成すると、これらはデフォルトで無効になります。
