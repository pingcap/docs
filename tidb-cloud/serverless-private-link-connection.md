---
title: Private Link Connections for Dataflow
summary: Dataflow のプライベート リンク接続を設定する方法を学習します。
---

# Dataflow のプライベート リンク接続 {#private-link-connections-for-dataflow}

TiDB Cloudの Dataflow サービス（Changefeed や Data Migration (DM) など）は、RDS インスタンスや Kafka クラスターなどの外部リソースへの信頼性の高い接続を必要とします。パブリックエンドポイントもサポートされていますが、プライベートリンク接続は、より高い効率性、より低いレイテンシー、そして強化されたセキュリティを提供する優れた代替手段となります。

プライベートリンク接続により、TiDB Cloud Essentialとターゲットリソース間の直接接続が可能になります。これにより、 TiDB Cloudから他のクラウドプラットフォーム上のデータベースへのデータ移動は完全にプライベートネットワーク境界内に留まり、ネットワーク攻撃対象領域を大幅に削減し、重要なデータフローワークロードの安定したスループットを確保できます。

## プライベートリンク接続の種類 {#private-link-connection-types}

データフロー用のプライベートリンク接続は、クラウドプロバイダーとアクセス先のサービスに応じて、さまざまなタイプから選択できます。各タイプは、 TiDB Cloudクラスターと、同じクラウド環境内の外部リソース（RDS や Kafka など）間の安全でプライベートなネットワークアクセスを可能にします。

### AWS エンドポイントサービス {#aws-endpoint-service}

このタイプのプライベートリンク接続により、 **AWS**上のTiDB Cloudクラスターが AWS PrivateLink によって提供される[AWSエンドポイントサービス](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)に接続できるようになります。

プライベートリンク接続は、エンドポイントサービスに関連付けることで、RDS インスタンスや Kafka サービスなどのさまざまな AWS サービスにアクセスできます。

### Alibaba Cloud エンドポイントサービス {#alibaba-cloud-endpoint-service}

このタイプのプライベート リンク接続により、 **Alibaba Cloud**上のTiDB Cloudクラスターが Alibaba Cloud PrivateLink を搭載した[Alibaba Cloudエンドポイントサービス](https://www.alibabacloud.com/help/en/privatelink/share-your-service/#51976edba8no7)に接続できるようになります。

プライベートリンク接続は、エンドポイント サービスに関連付けることで、RDS インスタンスや Kafka サービスなどのさまざまな Alibaba Cloud サービスにアクセスできます。

## AWS エンドポイントサービスプライベートリンク接続を作成する {#create-an-aws-endpoint-service-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、AWS Endpoint Service プライベートリンク接続を作成できます。

AWS エンドポイントサービスが次の条件を満たしていることを確認します。

-   TiDB Cloudクラスターと同じリージョンに存在します。
-   TiDB Cloudアカウント ID を**許可されたプリンシパル**リストに追加します。
-   TiDB Cloudクラスターと重複する可用性ゾーンがあります。

アカウント ID と可用性ゾーンの情報は**、[プライベート リンク接続の作成**] ダイアログの下部で取得するか、次のコマンドを実行して取得できます。

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。

4.  **[プライベート リンク接続の作成]**ダイアログで、必要な情報を入力します。

    -   **プライベート リンク接続名**: プライベート リンク接続の名前を入力します。
    -   **接続タイプ**： **AWSエンドポイントサービス**を選択します。このオプションが表示されない場合は、クラスターがAWS上に作成されていることを確認してください。
    -   **エンドポイント サービス名**: AWS エンドポイント サービス名を入力します (例: `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx` )。

5.  **[作成]**をクリックします。

6.  [AWSコンソール](https://console.aws.amazon.com)のエンドポイント サービスの詳細ページに移動します。**エンドポイント接続**タブで、 TiDB Cloudからのエンドポイント接続要求を承認します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベート リンク接続を作成するには:

1.  次のコマンドを実行します。

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
    ```

2.  [AWSコンソール](https://console.aws.amazon.com)のエンドポイント サービスの詳細ページに移動します。**エンドポイント接続**タブで、 TiDB Cloudからのエンドポイント接続要求を承認します。

</div>
</SimpleTab>

## Alibaba Cloud Endpoint Service のプライベートリンク接続を作成する {#create-an-alibaba-cloud-endpoint-service-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、Alibaba Cloud Endpoint Service プライベート リンク接続を作成できます。

Alibaba Cloud エンドポイント サービスが次の条件を満たしていることを確認します。

-   TiDB Cloudクラスターと同じリージョンに存在します。
-   TiDB Cloudアカウント ID を**サービス ホワイトリスト**に追加します。
-   TiDB Cloudクラスターと重複する可用性ゾーンがあります。

アカウント ID と利用可能なゾーンの情報は**、[プライベート リンク接続の作成**] ダイアログの下部で取得するか、次のコマンドを実行して取得できます。

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[データフローのプライベート リンク接続]**領域で、 **[プライベート リンク接続の作成] を**クリックします。

4.  **[プライベート リンク接続の作成]**ダイアログで、必要な情報を入力します。

    -   **プライベート リンク接続名**: プライベート リンク接続の名前を入力します。
    -   **接続タイプ**： **Alibaba Cloud Endpoint Service**を選択します。このオプションが表示されない場合は、クラスターがAlibaba Cloud上に作成されていることを確認してください。
    -   **エンドポイント サービス名**: Alibaba Cloud エンドポイント サービス名を入力します (例: `com.aliyuncs.privatelink.<region>.epsrv-xxxxxxxxxxxxxxxxx` )。

5.  **[作成]**をクリックします。

6.  [Alibaba Cloudコンソール](https://console.alibabacloud.com)のエンドポイント サービスの詳細ページに移動します。**エンドポイント接続**タブで、 TiDB Cloudからのエンドポイント接続要求を許可します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベート リンク接続を作成するには:

1.  次のコマンドを実行します。

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
    ```

2.  [Alibaba Cloudコンソール](https://console.alibabacloud.com)のエンドポイント サービスの詳細ページに移動します。**エンドポイント接続**タブで、 TiDB Cloudからのエンドポイント接続要求を許可します。

</div>
</SimpleTab>

## プライベートリンク接続にドメインを添付する {#attach-domains-to-a-private-link-connection}

プライベートリンク接続にドメインをアタッチできます。ドメインをプライベートリンク接続にアタッチすると、 TiDB Cloudデータフローサービスからこのドメインへのすべてのトラフィックがこのプライベートリンク接続にルーティングされます。これは、Kafka のアドバタイズリスナーなど、サービスが実行時にクライアントにカスタムドメインを提供する場合に便利です。

プライベートリンク接続の種類によって、サポートされるドメインの種類が異なります。次の表は、各プライベートリンク接続の種類でサポートされるドメインの種類を示しています。

| プライベートリンク接続タイプ            | サポートされているドメインタイプ                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------------- |
| AWS エンドポイントサービス           | <li>TiDB Cloud管理（ `aws.tidbcloud.com` ）</li><li>コンフルエント専用 ( `aws.confluent.cloud` )</li> |
| Alibaba Cloud エンドポイントサービス | TiDB Cloud管理（ `alicloud.tidbcloud.com` ）                                                 |

ドメインがこの表に含まれていない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してサポートを依頼してください。

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、ドメインをプライベート リンク接続に接続できます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してドメインをプライベート リンク接続に接続するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[データフローのプライベート リンク接続]**領域で、対象のプライベート リンク接続を選択し、 **[...]**をクリックします。

4.  **[ドメインの接続]**をクリックします。

5.  **[ドメインの接続]**ダイアログで、ドメインの種類を選択します。

    -   **TiDB Cloud Managed** ：ドメインはTiDB Cloudによって自動的に生成されます。 **「ドメインをアタッチ」を**クリックして確定してください。
    -   **Confluent Cloud** : Confluent Cloud Dedicated クラスタからドメインを生成するために提供された一意の名前を入力し、 **「ドメインをアタッチ」を**クリックして確定します。一意の名前の取得方法の詳細については、 [プライベートリンク接続を介してConfluent Cloudに接続する](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md#step-1-set-up-a-confluent-cloud-network)を参照してください。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してTiDB Cloud管理対象ドメインをアタッチするには、次の手順を実行します。

1.  `dry run`使用すると、アタッチするドメインをプレビューできます。次のステップで使用する一意の名前が出力されます。

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
    ```

2.  前の手順で取得した一意の名前でドメインを添付します。

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --unique-name <unique-name>
    ```

Confluent Cloud ドメインを接続するには、次のコマンドを実行します。

```shell
ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type CONFLUENT --unique-name <unique-name>
```

</div>
</SimpleTab>

## プライベートリンク接続からドメインを切断する {#detach-domains-from-a-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、プライベート リンク接続からドメインをデタッチできます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してプライベート リンク接続からドメインをデタッチするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[データフローのプライベート リンク接続]**領域で、対象のプライベート リンク接続を選択し、 **[...]**をクリックします。

4.  **[ドメインの切り離し]**をクリックし、切り離しを確認します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベート リンク接続からドメインをデタッチするには、次の手順を実行します。

1.  プライベートリンク接続の詳細を取得して`attach-domain-id`を見つけます:

    ```shell
    ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
    ```

2.  `attach-domain-id`でドメインを切り離します:

    ```shell
     ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domain-id>
    ```

</div>
</SimpleTab>

## プライベートリンク接続を削除する {#delete-a-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用してプライベート リンク接続を削除できます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してプライベート リンク接続を削除するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  ターゲット クラスターの名前をクリックして概要ページに移動し、左側のナビゲーション ペインで**[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[データフローのプライベート リンク接続]**領域で、対象のプライベート リンク接続を選択し、 **[...]**をクリックします。

4.  **[削除]**をクリックし、削除を確認します。

</div>

<div label="CLI">

プライベート リンク接続を削除するには、次のコマンドを実行します。

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

## 参照 {#see-also}

-   [プライベートリンク接続を介してConfluent Cloudに接続する](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md)

<!--
- [Connect to Amazon RDS via a Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-aws-rds.md)
- [Connect to Alibaba Cloud ApsaraDB RDS for MySQL via a Private Link Connection ](/tidb-cloud/serverless-private-link-connection-to-alicloud-rds.md)
- [Connect to AWS Self-Hosted Kafka via Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [Connect to Alibaba Cloud Self-Hosted Kafka via a Private Link Connection](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)
-->
