---
title: Connect via Private Endpoint
summary: Learn how to connect to your TiDB Cloud cluster via private endpoint.
---

# プライベートエンドポイント経由で接続する {#connect-via-private-endpoint}

TiDB Cloud は、 AWS VPC でホストされているTiDB Cloudサービスへの[<a href="https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc">AWS プライベートリンク</a>](https://aws.amazon.com/privatelink/?privatelink-blogs.sort-by=item.additionalFields.createdDate&#x26;privatelink-blogs.sort-order=desc)経由の、あたかもそのサービスが独自の VPC 内にあるかのように、安全性の高い一方向のアクセスをサポートします。プライベート エンドポイントが VPC で公開され、許可を得てエンドポイント経由でTiDB Cloudサービスへの接続を作成できます。

AWS PrivateLink を利用したエンドポイント接続は安全かつプライベートであり、データが公共のインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private endpoint architecture](/media/tidb-cloud/aws-private-endpoint-arch.png)

プライベート エンドポイントとエンドポイント サービスの詳細な定義については、次の AWS ドキュメントを参照してください。

-   [<a href="https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html">AWS PrivateLink とは何ですか?</a>](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
-   [<a href="https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html">AWS PrivateLink の概念</a>](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html)

## 制限 {#restrictions}

-   現在、 TiDB Cloud は、エンドポイント サービスが AWS でホストされている場合にのみプライベート エンドポイント接続をサポートします。サービスが Google Cloud Platform (GCP) でホストされている場合、プライベート エンドポイントは適用されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

ほとんどのシナリオでは、VPC ピアリング経由でプライベート エンドポイント接続を使用することをお勧めします。ただし、次のシナリオでは、プライベート エンドポイント接続の代わりに VPC ピアリングを使用する必要があります。

-   高可用性を実現するために、 [<a href="https://docs.pingcap.com/tidb/stable/ticdc-overview">TiCDC</a>](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用して、ソース TiDB クラスターからリージョンをまたがるターゲット TiDB クラスターにデータを複製しています。現在、プライベート エンドポイントはクロスリージョン接続をサポートしていません。
-   TiCDC クラスターを使用してデータをダウンストリームクラスター (Amazon Aurora、MySQL、Kafka など) にレプリケートしていますが、エンドポイント サービスを独自に維持することはできません。
-   PD または TiKV ノードに直接接続しています。

## AWS でプライベート エンドポイントをセットアップする {#set-up-a-private-endpoint-with-aws}

このセクションでは、AWS PrivateLink を使用して TiDB Serverless クラスタおよび TiDB Dedicatedクラスター用のプライベート エンドポイントをセットアップする方法について説明します。

### TiDB Serverless {#tidb-serverless}

プライベート エンドポイント経由で TiDB Serverless クラスタに接続するには、次の手順に従います。

1.  [<a href="#step-1-choose-a-tidb-cluster">TiDB クラスターを選択する</a>](#step-1-choose-a-tidb-cluster)
2.  [<a href="#step-2-create-an-aws-interface-endpoint">AWSインターフェースエンドポイントを作成する</a>](#step-2-create-an-aws-interface-endpoint)
3.  [<a href="#step-3-connect-to-your-tidb-cluster">TiDB クラスターに接続する</a>](#step-3-connect-to-your-tidb-cluster)

#### ステップ 1. TiDB クラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、ターゲット TiDB Serverless クラスタの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **サービス名**、**アベイラビリティーゾーン ID** 、および**リージョンID**をメモします。

    > **ノート：**
    >
    > AWS リージョンごとにプライベート エンドポイントを 1 つ作成するだけで済み、同じリージョンにあるすべての TiDB Serverless クラスタで共有できます。

#### ステップ 2. AWS インターフェースエンドポイントを作成する {#step-2-create-an-aws-interface-endpoint}

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [<a href="https://aws.amazon.com/console/">AWS マネジメントコンソール</a>](https://aws.amazon.com/console/)にサインインし、 [<a href="https://console.aws.amazon.com/vpc/">https://console.aws.amazon.com/vpc/</a>](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **[エンドポイントの作成]**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **[その他のエンドポイント サービス]**を選択します。

4.  [<a href="#step-1-choose-a-tidb-cluster">ステップ1</a>](#step-1-choose-a-tidb-cluster)で見つけたサービス名を入力します。

5.  **[サービスの確認]**をクリックします。

6.  ドロップダウン リストから VPC を選択します。 **[追加設定]**を展開し、 **[DNS 名を有効にする]**チェックボックスを選択します。

7.  **[サブネット]**領域で、TiDB クラスターが配置されているアベイラビリティ ゾーンを選択し、サブネット ID を選択します。

8.  **[Securityグループ]**領域でセキュリティ グループを適切に選択します。

    > **ノート：**
    >
    > 選択したセキュリティ グループがポート 4000 での EC2 インスタンスからの受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  **VPC ID**と**サブネット ID**を取得するには、AWS マネジメントコンソールに移動し、関連するセクションでそれらを見つけます。 [<a href="#step-1-choose-a-tidb-cluster">ステップ1</a>](#step-1-choose-a-tidb-cluster)で見つけた**アベイラビリティーゾーン ID を**必ず入力してください。
2.  以下に提供されているコマンドをコピーし、関連する引数を取得した情報に置き換えて、ターミナルで実行します。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${region_id} --service-name ${service_name} --vpc-endpoint-type Interface --subnet-ids ${your_subnet_id}
```

> **ヒント：**
>
> コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細については[<a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html">AWS CLI 設定の基本</a>](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

</div>
</SimpleTab>

その後、プライベート DNS 名を使用してエンドポイント サービスに接続できます。

#### ステップ 3: TiDB クラスターに接続する {#step-3-connect-to-your-tidb-cluster}

インターフェイス エンドポイントを作成したら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[エンドポイント タイプ]**ドロップダウン リストで、 **[プライベート]**を選択します。
4.  **[接続方法**] ドロップダウン リストで、希望の接続方法を選択します。対応する接続​​文字列がダイアログの下部に表示されます。
5.  接続文字列を使用してクラスターに接続します。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[<a href="#troubleshooting">このFAQ</a>](#troubleshooting)参照してください。
>
> VPC エンドポイントの作成時にエラー`private-dns-enabled cannot be set because there is already a conflicting DNS domain for gatewayXX-privatelink.XX.prod.aws.tidbcloud.com in the VPC vpc-XXXXX`が発生した場合、プライベート エンドポイントがすでに作成されていることが原因であり、新しいエンドポイントを作成する必要はありません。

### TiDB Dedicated {#tidb-dedicated}

プライベート エンドポイント経由で TiDB Dedicatedクラスターに接続するには、 [<a href="#prerequisites">前提条件</a>](#prerequisites)を完了し、次の手順に従います。

1.  [<a href="#step-1-choose-a-tidb-cluster">TiDB クラスターを選択する</a>](#step-1-choose-a-tidb-cluster)
2.  [<a href="#step-2-check-the-service-endpoint-region">サービスエンドポイントのリージョンを確認する</a>](#step-2-check-the-service-endpoint-region)
3.  [<a href="#step-3-create-an-aws-interface-endpoint">AWSインターフェースエンドポイントを作成する</a>](#step-3-create-an-aws-interface-endpoint)
4.  [<a href="#step-4-accept-the-endpoint-connection">エンドポイント接続を受け入れる</a>](#step-4-accept-the-endpoint-connection)
5.  [<a href="#step-5-enable-private-dns">プライベートDNSを有効にする</a>](#step-5-enable-private-dns)
6.  [<a href="#step-6-connect-to-your-tidb-cluster">TiDB クラスターに接続する</a>](#step-6-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

#### 前提条件 {#prerequisites}

1.  [<a href="https://tidbcloud.com">TiDB Cloudコンソール</a>](https://tidbcloud.com)にログインします。

2.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページの左側のナビゲーション ウィンドウで、次のいずれかを実行します。

    -   複数のプロジェクトがある場合は、ターゲット プロジェクトに切り替えて、 **[管理]** &gt; **[ネットワーク アクセス]**をクリックします。
    -   プロジェクトが 1 つだけの場合は、 **[管理]** &gt; **[ネットワーク アクセス]**をクリックします。

3.  **[プライベート エンドポイント]**タブをクリックします。

4.  右上隅の**「追加」**をクリックします。

#### ステップ 1. TiDB クラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  ドロップダウン リストをクリックして、利用可能な TiDB Dedicatedクラスターを選択します。
2.  **「次へ」**をクリックします。

#### ステップ 2. サービスエンドポイントリージョンを確認する {#step-2-check-the-service-endpoint-region}

サービス エンドポイント リージョンはデフォルトで選択されています。簡単に確認して、 **「次へ」**をクリックします。

> **ノート：**
>
> デフォルトのリージョンは、クラスターが配置されている場所です。変更しないでください。クロスリージョンのプライベート エンドポイントは現在サポートされていません。

#### ステップ 3. AWS インターフェースエンドポイントを作成する {#step-3-create-an-aws-interface-endpoint}

> **ノート：**
>
> 2023 年 3 月 28 日以降に作成された各 TiDB Dedicatedクラスターでは、対応するエンドポイント サービスがクラスター作成後 3 ～ 4 分で自動的に作成されます。

`Endpoint Service Ready`メッセージが表示された場合は、後で使用できるように、コンソールの下部領域にあるコマンドからエンドポイント サービス名をメモしておきます。それ以外の場合は、 TiDB Cloud がクラスターのエンドポイント サービスを作成するまで 3 ～ 4 分待ちます。

```bash
aws ec2 create-vpc-endpoint --vpc-id ${your_vpc_id} --region ${your_region} --service-name ${your_endpoint_service_name} --vpc-endpoint-type Interface --subnet-ids ${your_application_subnet_ids}
```

次に、AWS マネジメントコンソールまたは AWS CLI を使用して、AWS インターフェイスエンドポイントを作成します。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールを使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  [<a href="https://aws.amazon.com/console/">AWS マネジメントコンソール</a>](https://aws.amazon.com/console/)にサインインし、 [<a href="https://console.aws.amazon.com/vpc/">https://console.aws.amazon.com/vpc/</a>](https://console.aws.amazon.com/vpc/)で Amazon VPC コンソールを開きます。

2.  ナビゲーション ペインで**[エンドポイント]**をクリックし、右上隅の**[エンドポイントの作成]**をクリックします。

    **[エンドポイントの作成]**ページが表示されます。

    ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

3.  **[その他のエンドポイント サービス]**を選択します。

4.  TiDB Cloudコンソールで見つけたサービス名を入力します。

5.  **[サービスの確認]**をクリックします。

6.  ドロップダウン リストから VPC を選択します。

7.  TiDB クラスターが配置されているアベイラビリティーゾーンを**「サブネット」**領域で選択します。

    > **ヒント：**
    >
    > サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、 **[サブネット]**領域で AZ を選択できない場合があります。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに追加の AZ がある場合に発生します。この場合は[<a href="https://docs.pingcap.com/tidbcloud/tidb-cloud-support">PingCAP テクニカル サポート</a>](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)にご連絡ください。

8.  **[Securityグループ]**領域でセキュリティ グループを適切に選択します。

    > **ノート：**
    >
    > 選択したセキュリティ グループが、ポート 4000 または顧客定義のポートで EC2 インスタンスからの受信アクセスを許可していることを確認してください。

9.  **「エンドポイントの作成」**をクリックします。

</div>
<div label="Use AWS CLI">

AWS CLI を使用して VPC インターフェイスエンドポイントを作成するには、次の手順を実行します。

1.  プライベート エンドポイント作成ページの**[VPC ID]**フィールドと**[サブネット ID]**フィールドに入力します。 ID は AWS マネジメントコンソールから取得できます。
2.  ページの下部にあるコマンドをコピーし、ターミナルで実行します。次に、 **「次へ」**をクリックします。

> **ヒント：**
>
> -   コマンドを実行する前に、AWS CLI をインストールして設定する必要があります。詳細については[<a href="https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html">AWS CLI 設定の基本</a>](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。
>
> -   サービスが 3 つを超えるアベイラビリティ ゾーン (AZ) にまたがっている場合、VPC エンドポイント サービスがサブネットの AZ をサポートしていないことを示すエラー メッセージが表示されます。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに追加の AZ がある場合に発生します。この場合、 [<a href="https://docs.pingcap.com/tidbcloud/tidb-cloud-support">PingCAP テクニカル サポート</a>](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)にご連絡ください。
>
> -   TiDB Cloud がバックグラウンドでエンドポイント サービスの作成を完了するまで、コマンドをコピーすることはできません。

</div>
</SimpleTab>

#### ステップ 4. エンドポイント接続を受け入れる {#step-4-accept-the-endpoint-connection}

1.  TiDB Cloudコンソールに戻ります。
2.  **[プライベート エンドポイントの作成]**ページで、ボックスに VPC エンドポイント ID を入力します。
3.  **「次へ」**をクリックします。

#### ステップ 5. プライベート DNS を有効にする {#step-5-enable-private-dns}

AWS でプライベート DNS を有効にします。 AWS マネジメントコンソールまたは AWS CLI のいずれかを使用できます。

<SimpleTab>
<div label="Use AWS Console">

AWS マネジメントコンソールでプライベート DNS を有効にするには:

1.  **[VPC]** &gt; **[エンドポイント]**に移動します。
2.  エンドポイント ID を右クリックし、 **[プライベート DNS 名の変更]**を選択します。
3.  **「このエンドポイントに対して有効にする**」チェックボックスを選択します。
4.  **「変更を保存」**をクリックします。

    ![Enable private DNS](/media/tidb-cloud/private-endpoint/enable-private-dns.png)

</div>
<div label="Use AWS CLI">

AWS CLI を使用してプライベート DNS を有効にするには、コマンドをコピーし、AWS CLI で実行します。

```bash
aws ec2 modify-vpc-endpoint --vpc-endpoint-id ${your_vpc_endpoint_id} --private-dns-enabled
```

</div>
</SimpleTab>

TiDB Cloudコンソールで**[作成]**をクリックして、プライベート エンドポイントの作成を完了します。

これで、エンドポイント サービスに接続できるようになります。

#### ステップ 6: TiDB クラスターに接続する {#step-6-connect-to-your-tidb-cluster}

プライベート DNS を有効にしたら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページで、ターゲット クラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[プライベート エンドポイント]**タブを選択します。作成したプライベート エンドポイントが**[ステップ 1: プライベート エンドポイントの作成]**の下に表示されます。
4.  **「ステップ 2: アプリケーションを接続する」**で、希望する接続方法のタブをクリックし、接続文字列を使用してクラスターに接続します。接続文字列内のプレースホルダー`<cluster_endpoint_name>:<port>`は、実際の値に自動的に置き換えられます。

> **ヒント：**
>
> クラスターに接続できない場合は、AWS の VPC エンドポイントのセキュリティ グループが適切に設定されていないことが原因である可能性があります。解決策については[<a href="#troubleshooting">このFAQ</a>](#troubleshooting)参照してください。

#### プライベート エンドポイントのステータス参照 {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[<a href="#prerequisites">**プライベートエンドポイント**ページ</a>](#prerequisites)に表示されます。

プライベート エンドポイントの考えられるステータスについては、次のように説明します。

-   **未構成**: エンドポイント サービスは作成されていますが、プライベート エンドポイントはまだ作成されていません。
-   **保留中**: 処理を待っています。
-   **Active** : プライベート エンドポイントを使用する準備ができています。このステータスのプライベート エンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントは削除中です。
-   **失敗**: プライベート エンドポイントの作成は失敗します。その行の**「編集」を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの考えられるステータスについては、次のように説明します。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **Active** : プライベート エンドポイントが作成されているかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除中**: エンドポイント サービスまたはクラスターが削除されています。これには 3 ～ 5 分かかります。

## トラブルシューティング {#troubleshooting}

### プライベート DNS を有効にした後、プライベート エンドポイント経由で TiDB クラスターに接続できません。なぜ？ {#i-cannot-connect-to-a-tidb-cluster-via-a-private-endpoint-after-enabling-private-dns-why}

場合によっては、AWS マネジメント コンソールで VPC エンドポイントのセキュリティ グループを適切に設定する必要があります。 **[VPC]** &gt; **[エンドポイント]**に移動します。 VPC エンドポイントを右クリックし、適切な**[セキュリティ グループの管理]**を選択します。ポート 4000 または顧客定義のポートで EC2 インスタンスからの受信アクセスを許可する、VPC 内の適切なセキュリティ グループ。

![Manage security groups](/media/tidb-cloud/private-endpoint/manage-security-groups.png)

### プライベート DNS を有効にできません。 <code>enableDnsSupport</code>および<code>enableDnsHostnames</code> VPC 属性が有効になっていないことを示すエラーが報告される {#i-cannot-enable-private-dns-an-error-is-reported-indicating-that-the-code-enablednssupport-code-and-code-enablednshostnames-code-vpc-attributes-are-not-enabled}

VPC 設定で DNS ホスト名と DNS 解決の両方が有効になっていることを確認してください。 AWS マネジメントコンソールで VPC を作成すると、デフォルトでは無効になります。
