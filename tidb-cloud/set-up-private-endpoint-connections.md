---
title: Set Up Private Endpoint Connections
summary: Learn how to set up private endpoint connections in TiDB Cloud.
---

# プライベート エンドポイント接続のセットアップ {#set-up-private-endpoint-connections}

TiDB Cloudは、サービスが独自の VPC にあるかのように、AWS VPC でホストされているTiDB Cloudサービスへの非常に安全な一方向アクセスを[AWS プライベートリンク](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)経由でサポートします。プライベート エンドポイントが VPC で公開されており、エンドポイントを介してTiDB Cloudサービスへの接続を許可付きで作成できます。

AWS PrivateLink を利用したエンドポイント接続は安全でプライベートであり、データが公共のインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベート エンドポイントとエンドポイント サービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [AWS PrivateLink とは?](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [AWS PrivateLink の概念](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB Cloudは、エンドポイント サービスが AWS でホストされている場合にのみ、プライベート エンドポイント接続をサポートしています。サービスが Google Cloud Platform (GCP) でホストされている場合、プライベート エンドポイントは適用されません。
-   プライベート エンドポイントのサポートは、サーバーレス層ではなく、 TiDB Cloud Dedicated Tierに対してのみ提供されます。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

ほとんどのシナリオでは、VPC ピアリング経由でプライベート エンドポイント接続を使用することをお勧めします。ただし、次のシナリオでは、プライベート エンドポイント接続の代わりに VPC ピアリングを使用する必要があります。

-   [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)のクラスターを使用して、ソース TiDB クラスターからターゲット TiDB クラスターにリージョン間でデータをレプリケートし、高可用性を実現しています。現在、プライベート エンドポイントはクロスリージョン接続をサポートしていません。
-   TiCDC クラスターを使用してダウンストリーム クラスター (Amazon Aurora、MySQL、Kafka など) にデータをレプリケートしていますが、エンドポイント サービスを自分で維持することはできません。
-   PD または TiKV ノードに直接接続しています。

## AWS でプライベート エンドポイントをセットアップする {#set-up-a-private-endpoint-with-aws}

このセクションでは、AWS PrivateLink を使用してプライベート エンドポイントを設定する方法について説明します。

[前提条件](#prerequisites)に加えて、AWS PrivateLink とのプライベート エンドポイント接続をセットアップするには 5 つのステップがあります。

1.  [TiDB クラスターを選択する](#step-1-choose-a-tidb-cluster)
2.  [サービス エンドポイントのリージョンを確認する](#step-2-check-the-service-endpoint-region)
3.  [AWS インターフェイス エンドポイントを作成する](#step-3-create-an-aws-interface-endpoint)
4.  [エンドポイント接続を受け入れる](#step-4-accept-the-endpoint-connection)
5.  [プライベート DNS を有効にする](#step-5-enable-private-dns)

複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

TiDB Cloudは、 Dedicated Tierクラスターのプライベート エンドポイントのみをサポートします。プライベート エンドポイントを作成する前に、 Dedicated Tierクラスターを作成する必要があります。詳細な手順については、 [TiDB Cloudで TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

プライベート エンドポイントの設定を開始するには、プライベート エンドポイントの作成ページを開きます。

1.  TiDB Cloudコンソールの [**プロジェクト設定**] タブをクリックします。
2.  左側のメニューで [**プライベート エンドポイント**] をクリックします。
3.  [**プライベート エンドポイント]**ページで [<strong>追加]</strong>をクリックします。

### ステップ 1. TiDB クラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  ドロップダウン リストをクリックして、利用可能な TiDB クラスターを選択します。
2.  [**次へ**] をクリックします。

### ステップ 2. サービス エンドポイント リージョンを確認する {#step-2-check-the-service-endpoint-region}

サービス エンドポイント リージョンはデフォルトで選択されています。簡単に確認して、[**次へ**] をクリックします。

> **ノート：**
>
> デフォルトのリージョンは、クラスターが配置されている場所です。変更しないでください。クロスリージョン プライベート エンドポイントは現在サポートされていません。

### ステップ 3.AWS インターフェイス エンドポイントを作成する {#step-3-create-an-aws-interface-endpoint}

TiDB Cloudがエンドポイント サービスの作成を開始します。これには 3 ～ 4 分かかります。

エンドポイント サービスが作成されたら、コンソールの下部領域にあるコマンドからエンドポイント サービス名をメモします。

```bash
aws ec2 create-vpc-endpoint --vpc-id <your_vpc_id> --region <your_region> --service-name <your_endpoint_service_name> --vpc-endpoint-type Interface --subnet-ids <your_application_subnet_ids>
```

次に、AWS マネジメント コンソールまたは AWS CLI を使用して、AWS インターフェイス エンドポイントを作成します。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメント コンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  **VPC** &gt;<strong>エンドポイント</strong>に移動します。

2.  [**エンドポイントの作成]**をクリックします。

    **エンドポイントの作成**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  [**その他のエンドポイント サービス] を**選択します。

4.  エンドポイント サービス名を入力します。

5.  [**サービスの確認 ] を**クリックします。

6.  ドロップダウン リストで VPC を選択します。

7.  **サブネット**領域で、TiDB クラスターが配置されている可用性ゾーンを選択します。

    > **ヒント：**
    >
    > サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、[**サブネット**] 領域で AZ を選択できない場合があります。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合は[PingCAP テクニカル サポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)にお問い合わせください。

8.  [**セキュリティ グループ**] 領域でセキュリティ グループを適切に選択します。

    > **ノート：**
    >
    > 選択したセキュリティ グループが、ポート 4000 または顧客定義のポートで EC2 インスタンスからのインバウンド アクセスを許可していることを確認してください。

9.  [**エンドポイントの作成]**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  プライベート エンドポイントの作成ページで、 **VPC** ID フィールドと<strong>サブネット ID</strong>フィールドに入力します。 ID は AWS マネジメント コンソールから取得できます。
2.  ページの下部にあるコマンドをコピーして、ターミナルで実行します。次に、[**次へ**] をクリックします。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細は[AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> -   サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、VPC エンドポイント サービスがサブネットの AZ をサポートしていないことを示すエラー メッセージが表示されます。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合、 [PingCAP テクニカル サポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)に連絡できます。
>
> -   TiDB Cloudがバックグラウンドでエンドポイント サービスの作成を完了するまで、コマンドをコピーすることはできません。

</div>
</SimpleTab>

### ステップ 4. エンドポイント接続を受け入れる {#step-4-accept-the-endpoint-connection}

1.  TiDB Cloudコンソールに戻ります。
2.  [**プライベート エンドポイントの作成]**ページで、ボックスに VPC エンドポイント ID を入力します。
3.  [**次へ**] をクリックします。

### ステップ 5. プライベート DNS を有効にする {#step-5-enable-private-dns}

AWS でプライベート DNS を有効にします。 AWS マネジメント コンソールまたは AWS CLI を使用できます。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメント コンソールでプライベート DNS を有効にするには:

1.  **VPC** &gt;<strong>エンドポイント</strong>に移動します。
2.  エンドポイント ID を右クリックし、 **[プライベート DNS 名の変更**] を選択します。
3.  [**このエンドポイントを有効にする]**チェック ボックスをオンにします。
4.  [**変更を保存] を**クリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、コマンドをコピーして AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id <your_vpc_endpoint_id> --private-dns-enabled
```

</div>
</SimpleTab>

TiDB Cloudコンソールで [**作成**] をクリックして、プライベート エンドポイントの作成を完了します。

その後、エンドポイント サービスに接続できます。詳細は[プライベート エンドポイント経由で TiDB クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-private-endpoint-recommended)を参照してください。

## プライベート エンドポイントのステータス リファレンス {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスの状態が[**プライベート エンドポイント**ページ](#prerequisites)に表示されます。

プライベート エンドポイントの可能なステータスは、次のように説明されています。

-   **未構成**: エンドポイント サービスを作成したばかりですが、プライベート エンドポイントはまだ作成していません。
-   **保留中**: 処理を待っています。
-   **Active** : プライベート エンドポイントを使用する準備ができています。このステータスのプライベート エンドポイントは編集できません。
-   **削除**中 : プライベート エンドポイントを削除しています。
-   **Failed** : プライベート エンドポイントの作成に失敗しました。その行の [<strong>編集</strong>] をクリックして、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスは、次のように説明されています。

-   **作成**中 : エンドポイント サービスが作成されています。これには 3 ～ 5 分かかります。
-   **Active** : プライベート エンドポイントが作成されているかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除**中 : エンドポイント サービスまたはクラスターを削除しています。これには 3 ～ 5 分かかります。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なんで？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

AWS マネジメント コンソールで VPC エンドポイントのセキュリティ グループを適切に設定する必要がある場合があります。 **VPC** &gt;<strong>エンドポイント</strong>に移動します。 VPC エンドポイントを右クリックし、適切な<strong>Manage security groups</strong>を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからのインバウンド アクセスを許可する、VPC 内の適切なセキュリティ グループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。 <code>enableDnsSupport</code>および<code>enableDnsHostnames</code> VPC 属性が有効になっていないことを示すエラーが報告される {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認します。 AWS マネジメント コンソールで VPC を作成すると、デフォルトで無効になります。
