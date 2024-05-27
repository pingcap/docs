---
title: Connect to a TiDB Dedicated Cluster via Private Endpoint with AWS
summary: AWS を使用してプライベートエンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# AWS のプライベートエンドポイント経由で TiDB 専用クラスタに接続する {#connect-to-a-tidb-dedicated-cluster-via-private-endpoint-with-aws}

このドキュメントでは、AWS のプライベートエンドポイント経由で TiDB 専用クラスターに接続する方法について説明します。

> **ヒント：**
>
> プライベート エンドポイント経由で TiDB サーバーレス クラスタに接続する方法については、 [プライベートエンドポイント経由で TiDB Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)ご覧ください。Google Cloud でプライベート エンドポイント経由で TiDB 専用クラスタに接続する方法については、 [プライベートサービス経由でTiDB Dedicatedに接続 Google Cloudに接続](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)をご覧ください。

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

## AWSでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

プライベート エンドポイント経由で TiDB 専用クラスターに接続するには、 [前提条件](#prerequisites)完了し、次の手順に従います。

1.  [TiDBクラスタを選択する](#step-1-choose-a-tidb-cluster)
2.  [サービスエンドポイントのリージョンを確認する](#step-2-check-the-service-endpoint-region)
3.  [AWSインターフェースエンドポイントを作成する](#step-3-create-an-aws-interface-endpoint)
4.  [エンドポイント接続を受け入れる](#step-4-accept-the-endpoint-connection)
5.  [プライベートDNSを有効にする](#step-5-enable-private-dns)
6.  [TiDBクラスターに接続する](#step-6-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  クリック<mdsvgicon name="icon-left-projects">左下隅で、複数のプロジェクトがある場合は対象プロジェクトに切り替えて、 **[プロジェクト設定]**をクリックします。</mdsvgicon>
3.  プロジェクトの**「プロジェクト設定」**ページで、左側のナビゲーション ペインの**「ネットワーク アクセス」**をクリックし、 **「プライベート エンドポイント」**タブをクリックします。
4.  右上隅の**「プライベートエンドポイントの作成」を**クリックし、 **「AWS プライベートエンドポイント」**を選択します。

### ステップ1. TiDBクラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  ドロップダウン リストをクリックして、利用可能な TiDB 専用クラスターを選択します。
2.  **「次へ」**をクリックします。

### ステップ2. サービスエンドポイントのリージョンを確認する {#step-2-check-the-service-endpoint-region}

サービス エンドポイントのリージョンはデフォルトで選択されています。簡単に確認して、 **「次へ」**をクリックします。

> **注記：**
>
> デフォルトのリージョンは、クラスターが配置されている場所です。変更しないでください。現在、リージョン間のプライベート エンドポイントはサポートされていません。

### ステップ3. AWSインターフェースエンドポイントを作成する {#step-3-create-an-aws-interface-endpoint}

> **注記：**
>
> 2023 年 3 月 28 日以降に作成された TiDB 専用クラスターごとに、クラスターの作成後 3 ～ 4 分後に対応するエンドポイント サービスが自動的に作成されます。

`Endpoint Service Ready`メッセージが表示された場合は、後で使用するために、コンソールの下部にあるコマンドからエンドポイント サービス名をメモしてください。それ以外の場合は、 TiDB Cloud がクラスターのエンドポイント サービスを作成するまで 3 ～ 4 分待ちます。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
```

次に、AWS マネジメントコンソールまたは AWS CLI を使用して AWS インターフェイスエンドポイントを作成します。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [AWS マネジメントコンソール](https://aws.amazon.com/console/)にサインインし、 [詳しくはこちら](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント**] をクリックし、右上隅の**[エンドポイントの作成] を**クリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **その他のエンドポイント サービス**を選択します。

4.  TiDB Cloudコンソールで見つけたサービス名を入力します。

5.  **[サービスの確認]を**クリックします。

6.  ドロップダウンリストから VPC を選択します。

7.  **サブネット**領域で、TiDB クラスターが配置されている可用性ゾーンを選択します。

    > **ヒント：**
    >
    > サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、**サブネット**領域で AZ を選択できないことがあります。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合は、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)にお問い合わせください。

8.  **Securityグループ**領域でセキュリティ グループを適切に選択します。

    > **注記：**
    >
    > 選択したセキュリティ グループが、ポート 4000 または顧客定義のポート上の EC2 インスタンスからの受信アクセスを許可していることを確認します。

9.  **[エンドポイントの作成]を**クリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  プライベートエンドポイント作成ページの**VPC ID**と**サブネット ID**フィールドに入力します。ID は AWS マネジメントコンソールから取得できます。
2.  ページの下部にあるコマンドをコピーし、ターミナルで実行します。次に、 **「次へ」**をクリックします。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定しておく必要があります。詳細については[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> -   サービスが 3 つ以上のアベイラビリティーゾーン (AZ) にまたがっている場合、VPC エンドポイント サービスがサブネットの AZ をサポートしていないことを示すエラー メッセージが表示されます。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合、 [PingCAP テクニカルサポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)お問い合わせください。
>
> -   TiDB Cloud がバックグラウンドでエンドポイント サービスの作成を完了するまで、コマンドをコピーすることはできません。

</div>
</SimpleTab>

### ステップ4. エンドポイント接続を承認する {#step-4-accept-the-endpoint-connection}

1.  TiDB Cloudコンソールに戻ります。
2.  **「プライベート エンドポイントの作成」**ページで、ボックスに VPC エンドポイント ID を入力します。
3.  **「次へ」**をクリックします。

### ステップ5. プライベートDNSを有効にする {#step-5-enable-private-dns}

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

AWS CLI を使用してプライベート DNS を有効にするには、コマンドをコピーして AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

</div>
</SimpleTab>

TiDB Cloudコンソールで**[作成] を**クリックして、プライベート エンドポイントの作成を完了します。

その後、エンドポイント サービスに接続できます。

### ステップ6. TiDBクラスターに接続する {#step-6-connect-to-your-tidb-cluster}

プライベート DNS を有効にしたら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、 **[アクション]**列の**[...]**をクリックします。
2.  **「接続」を**クリックします。接続ダイアログが表示されます。
3.  [**プライベート エンドポイント]**タブを選択します。作成したプライベート エンドポイントが**、[ステップ 1: プライベート エンドポイントの作成]**の下に表示されます。
4.  **「ステップ 2: 接続を接続する**」で、 **「接続」**をクリックし、希望する接続方法のタブをクリックして、接続文字列を使用してクラスターに接続します。接続文字列内のプレースホルダー`<cluster_endpoint_name>:<port>`は、実際の値に自動的に置き換えられます。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[このFAQ](#troubleshooting)参照してください。

### プライベートエンドポイントステータスリファレンス {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[**プライベートエンドポイント**ページ](#prerequisites)に表示されます。

プライベート エンドポイントの可能なステータスは次のように説明されます。

-   **未構成**: エンドポイント サービスは作成されていますが、プライベート エンドポイントはまだ作成されていません。
-   **保留中**: 処理を待機しています。
-   **アクティブ**: プライベート エンドポイントは使用可能です。このステータスのプライベート エンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントを削除しています。
-   **失敗**: プライベート エンドポイントの作成に失敗しました。その行の**[編集] を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスは、次のように説明されます。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **アクティブ**: プライベート エンドポイントが作成されたかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除中**: エ​​ンドポイント サービスまたはクラスターを削除中です。これには 3 ～ 5 分かかります。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なぜですか? {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメントコンソールで、VPC エンドポイントのセキュリティグループを適切に設定する必要がある場合があります。 **[VPC]** &gt; **[エンドポイント**] に移動します。VPC エンドポイントを右クリックし、適切な**[セキュリティグループの管理]**を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからのインバウンドアクセスを許可する、VPC 内の適切なセキュリティグループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。enableDnsSupport および<code>enableDnsSupport</code> VPC 属性が有効になっていないことを示すエラー<code>enableDnsHostnames</code>報告されます {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。AWS マネジメントコンソールで VPC を作成すると、これらはデフォルトで無効になります。
