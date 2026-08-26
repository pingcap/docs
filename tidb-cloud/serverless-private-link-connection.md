---
title: Private Link Connections for Dataflow
summary: Dataflow のプライベートリンク接続を設定する方法を学習します。
---

# Dataflow のプライベートリンク接続 {#private-link-connections-for-dataflow}

TiDB Cloudの Dataflow サービス（Changefeed や Data Migration (DM) など）は、RDS インスタンスや Kafka クラスターなどの外部リソースへの信頼性の高い接続を必要とします。パブリックエンドポイントもサポートされていますが、プライベートリンク接続は、より高い効率性、より低いレイテンシー、そして強化されたセキュリティを提供する優れた代替手段となります。

プライベートリンク接続により、TiDB Cloud Essentialとターゲットリソース間の直接接続が可能になります。これにより、 TiDB Cloudから他のクラウドプラットフォーム上のデータベースへのデータ移動は完全にプライベートネットワーク境界内に留まり、ネットワーク攻撃対象領域を大幅に削減し、重要なデータフローワークロードの安定したスループットを確保できます。

## プライベートリンク接続の種類 {#private-link-connection-types}

データフロー用のプライベートリンク接続は、クラウドプロバイダーとアクセス先のサービスに応じて、さまざまなタイプから選択できます。各タイプは、 TiDB Cloudクラスターと、同じクラウド環境内の外部リソース（RDS や Kafka など）間の安全でプライベートなネットワークアクセスを可能にします。

### AWS エンドポイントサービス {#aws-endpoint-service}

このタイプのプライベートリンク接続により、 **AWS**上のTiDB Cloudクラスターが AWS PrivateLink によって提供される[AWSエンドポイントサービス](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html)に接続できるようになります。

プライベートリンク接続は、エンドポイントサービスに関連付けることで、RDS インスタンスや Kafka サービスなどのさまざまな AWS サービスにアクセスできます。

### Amazon MSK プロビジョニング {#amazon-msk-provisioned}

このタイプのプライベートリンク接続により、 **AWS**上のTiDB Cloudクラスターがプライベートリンクを使用して[Amazon MSK プロビジョニング](https://docs.aws.amazon.com/msk/latest/developerguide/msk-provisioned.html)に接続できるようになります。

### Alibaba Cloud エンドポイントサービス {#alibaba-cloud-endpoint-service}

このタイプのプライベートリンク接続により、 **Alibaba Cloud**上のTiDB Cloudクラスターが Alibaba Cloud PrivateLink を搭載した[Alibaba Cloudエンドポイントサービス](https://www.alibabacloud.com/help/en/privatelink/share-your-service/#51976edba8no7)に接続できるようになります。

プライベートリンク接続は、エンドポイントサービスに関連付けることで、RDS インスタンスや Kafka サービスなどのさまざまな Alibaba Cloud サービスにアクセスできます。

## AWS エンドポイントサービスプライベートリンク接続を作成する {#create-an-aws-endpoint-service-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、AWS Endpoint Service プライベートリンク接続を作成できます。

AWS エンドポイントサービスが次の条件を満たしていることを確認します。

- TiDB Cloudクラスターと同じリージョンに存在します。
- TiDB Cloudアカウント ID を**Allow principals**リストに追加します。
- TiDB Cloudクラスターと重複する可用性ゾーンがあります。

アカウント ID と可用性ゾーンの情報は、**Create Private Endpoint for External Services**ダイアログの下部で取得するか、次のコマンドを実行して取得できます。

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. **AWS Private Endpoints for External Services**領域で、**Create Private Endpoint for External Services**をクリックします。

    > **Note:**
    >
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日以降に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント専用モードでプライベートリンク接続が作成されます。このモードでは、各 {{{ .essential }}} インスタンスが独自のスタンドアロンプライベートエンドポイントを使用するため、接続時に[アカウントプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を含める必要がありません。
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日より前に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント共有モードでプライベートリンク接続が作成されます。このモードでは、同じ AWS Region 内の複数の {{{ .essential }}} インスタンスで 1つのプライベートエンドポイントを共有できます。

4. **Create Private Endpoint for External Services**ダイアログで、必要な情報を入力します。

    - **Private Link Connection Name**: プライベートリンク接続の名前を入力します。
    - **Connection Type**： **AWS Endpoint Service**を選択します。このオプションが表示されない場合は、クラスターがAWS上に作成されていることを確認してください。
    - **Endpoint Service Name**: AWS エンドポイントサービス名を入力します (例: `com.amazonaws.vpce.<region>.vpce-svc-xxxxxxxxxxxxxxxxx` )。

5. **Create**をクリックします。

6. [AWSコンソール](https://console.aws.amazon.com)のエンドポイントサービスの詳細ページに移動します。**Endpoint Connections**タブで、 TiDB Cloudからのエンドポイント接続要求を承認します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベートリンク接続を作成するには:

1. 次のコマンドを実行します。

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type AWS_ENDPOINT_SERVICE --aws.endpoint-service-name <endpoint-service-name>
    ```

2. [AWSコンソール](https://console.aws.amazon.com)のエンドポイントサービスの詳細ページに移動します。**Endpoint Connections**タブで、 TiDB Cloudからのエンドポイント接続要求を承認します。

</div>
</SimpleTab>

## Amazon MSK プロビジョニングされたプライベートリンク接続を作成する {#create-an-amazon-msk-provisioned-private-link-connection}

TiDB Cloudコンソールを使用して、Amazon MSK プロビジョニングされたプライベートリンク接続を作成できます。

Amazon MSK プロビジョニングプライベートリンク接続を作成する前に、Amazon MSK プロビジョニングクラスターでマルチVPC接続が有効になっていることを確認してください。詳細については、 [プライベートリンク接続経由​​でプロビジョニングされた Amazon MSK に接続する](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)を参照してください。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. **AWS Private Endpoints for External Services**領域で、**Create Private Endpoint for External Services**をクリックします。

    > **Note:**
    >
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日以降に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント専用モードでプライベートリンク接続が作成されます。このモードでは、各 {{{ .essential }}} インスタンスが独自のスタンドアロンプライベートエンドポイントを使用するため、接続時に[アカウントプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を含める必要がありません。
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日より前に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント共有モードでプライベートリンク接続が作成されます。このモードでは、同じ AWS Region 内の複数の {{{ .essential }}} インスタンスで 1つのプライベートエンドポイントを共有できます。

4. **Create Private Endpoint for External Services**ダイアログで、必要な情報を入力します。

    - **Private Link Connection Name**: プライベートリンク接続の名前を入力します。
    - **Connection Type**： **Amazon MSK Provisioned**を選択します。このオプションが表示されない場合は、クラスターがAWS上に作成されていることを確認してください。
    - **MSK Cluster ARN** : Amazon MSK プロビジョニングされたクラスターの ARN を入力します (例: `arn:aws:kafka:us-east-1:385595570414:cluster/<msk-name>/xxxx` )。

5. **Create**をクリックします。

## Alibaba Cloud Endpoint Service のプライベートリンク接続を作成する {#create-an-alibaba-cloud-endpoint-service-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、Alibaba Cloud Endpoint Service プライベートリンク接続を作成できます。

Alibaba Cloud エンドポイントサービスが次の条件を満たしていることを確認します。

- TiDB Cloudクラスターと同じリージョンに存在します。
- TiDB Cloudアカウント ID を**Service Whitelist**に追加します。
- TiDB Cloudクラスターと重複する可用性ゾーンがあります。

アカウント ID と可用性ゾーンの情報は、**Create Private Endpoint for External Services**ダイアログの下部で取得するか、次のコマンドを実行して取得できます。

```shell
ticloud serverless private-link-connection zones --cluster-id <cluster-id>
```

<SimpleTab>
<div label="Console">

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. **Alibaba Cloud Private Endpoints for External Services**領域で、**Create Private Endpoint for External Services**をクリックします。

    > **Note:**
    >
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日以降に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント専用モードでプライベートリンク接続が作成されます。このモードでは、各 {{{ .essential }}} インスタンスが独自のスタンドアロンプライベートエンドポイントを使用するため、接続時に[アカウントプレフィックス](/tidb-cloud/select-cluster-tier.md#user-name-prefix)を含める必要がありません。
    > - TiDB Cloud Essential インスタンスが 2026年 7月 1日より前に作成されている場合、**Create Private Endpoint for External Services** をクリックすると、エンドポイント共有モードでプライベートリンク接続が作成されます。このモードでは、同じ Alibaba Cloud Region 内の複数の {{{ .essential }}} インスタンスで 1つのプライベートエンドポイントを共有できます。

4. **Create Private Endpoint for External Services**ダイアログで、必要な情報を入力します。

    - **Private Link Connection Name**: プライベートリンク接続の名前を入力します。
    - **Connection Type**： **Alibaba Cloud Endpoint Service**を選択します。このオプションが表示されない場合は、クラスターがAlibaba Cloud上に作成されていることを確認してください。
    - **Endpoint Service Name**: Alibaba Cloud エンドポイントサービス名を入力します (例: `com.aliyuncs.privatelink.<region>.epsrv-xxxxxxxxxxxxxxxxx` )。

5. **Create**をクリックします。

6. [Alibaba Cloudコンソール](https://console.alibabacloud.com)のエンドポイントサービスの詳細ページに移動します。**Endpoint Connections**タブで、 TiDB Cloudからのエンドポイント接続要求を許可します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベートリンク接続を作成するには:

1. 次のコマンドを実行します。

    ```shell
    ticloud serverless private-link-connection create -c <cluster-id> --display-name <display-name> --type ALICLOUD_ENDPOINT_SERVICE --alicloud.endpoint-service-name <endpoint-service-name>
    ```

2. [Alibaba Cloudコンソール](https://console.alibabacloud.com)のエンドポイントサービスの詳細ページに移動します。**Endpoint Connections**タブで、 TiDB Cloudからのエンドポイント接続要求を許可します。

</div>
</SimpleTab>

## プライベートリンク接続にドメインを添付する {#attach-domains-to-a-private-link-connection}

プライベートリンク接続にドメインをアタッチできます。ドメインをプライベートリンク接続にアタッチすると、 TiDB Cloudデータフローサービスからこのドメインへのすべてのトラフィックがこのプライベートリンク接続にルーティングされます。これは、Kafka のアドバタイズリスナーなど、サービスが実行時にクライアントにカスタムドメインを提供する場合に便利です。

プライベートリンク接続の種類によって、サポートされるドメインの種類が異なります。次の表は、各プライベートリンク接続の種類でサポートされるドメインの種類を示しています。

| プライベートリンク接続タイプ            | サポートされているドメインタイプ                                                                               |
| ------------------------- | ---------------------------------------------------------------------------------------------- |
| AWS エンドポイントサービス           | <li>TiDB Cloud管理（ `aws.tidbcloud.com` ）</li><li>Confluent Dedicated( `aws.confluent.cloud` )</li> |
| Alibaba Cloud エンドポイントサービス | TiDB Cloud管理（ `alicloud.tidbcloud.com` ）                                                       |
| Amazon MSK プロビジョニング       | ドメインの添付はサポートされていません。                                                                           |

ドメインがこの表に含まれていない場合は、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)に連絡してサポートを依頼してください。

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、ドメインをプライベートリンク接続に接続できます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してドメインをプライベートリンク接続に接続するには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. クラウドプロバイダーの**Private Endpoints for External Services**領域で、対象のプライベートリンク接続を選択し、 **...**をクリックします。

4. **Attach Domains**をクリックします。

5. **Attach Domains**ダイアログで、ドメインの種類を選択します。

    - **TiDB Cloud Managed**：ドメインはTiDB Cloudによって自動的に生成されます。生成されたドメインの名前には、そのドメインの一意の名前が付与されます。例えば、生成されたドメインが`*.use1-az1.dvs6nl5jgveztmla3pxkxgh76i.aws.plc.tidbcloud.com`の場合、一意の名前は`dvs6nl5jgveztmla3pxkxgh76i`になります。 **Attach Domains**をクリックして確定します。
    - **Confluent Cloud** : Confluent Cloud Dedicatedクラスタからドメインを生成するために提供された一意の名前を入力し、 **Attach Domains**をクリックして確定します。一意の名前の取得方法の詳細については、 [プライベートリンク接続を介してConfluent Cloudに接続する](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md#step-1-set-up-a-confluent-cloud-network)を参照してください。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してTiDB Cloud管理対象ドメインをアタッチするには、次の手順を実行します。

1. `dry run`を使用すると、アタッチするドメインをプレビューできます。次のステップで使用する一意の名前が出力されます。

    ```shell
    ticloud serverless private-link-connection attach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --type TIDBCLOUD_MANAGED --dry-run
    ```

2. 前の手順で取得した一意の名前でドメインを添付します。

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

TiDB CloudコンソールまたはTiDB Cloud CLI を使用して、プライベートリンク接続からドメインをデタッチできます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してプライベートリンク接続からドメインをデタッチするには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. クラウドプロバイダーの**Private Endpoints for External Services**領域で、対象のプライベートリンク接続を選択し、 **...**をクリックします。

4. **Detach Domains**をクリックし、切り離しを確認します。

</div>

<div label="CLI">

TiDB Cloud CLI を使用してプライベートリンク接続からドメインをデタッチするには、次の手順を実行します。

1. プライベートリンク接続の詳細を取得して`attach-domain-id`を見つけます:

    ```shell
    ticloud serverless private-link-connection get -c <cluster-id> --private-link-connection-id <private-link-connection-id>
    ```

2. `attach-domain-id`でドメインを切り離します:

    ```shell
     ticloud serverless private-link-connection detach-domains -c <cluster-id> --private-link-connection-id <private-link-connection-id> --attach-domain-id <attach-domain-id>
    ```

</div>
</SimpleTab>

## プライベートリンク接続を削除する {#delete-a-private-link-connection}

TiDB CloudコンソールまたはTiDB Cloud CLI を使用してプライベートリンク接続を削除できます。

<SimpleTab>
<div label="Console">

TiDB Cloudコンソールを使用してプライベートリンク接続を削除するには、次の手順を実行します。

1. [TiDB Cloudコンソール](https://tidbcloud.com/)にログインし、[**My TiDB**](https://tidbcloud.com/tidbs)ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2. ターゲットクラスターの名前をクリックして概要ページに移動し、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックします。

3. クラウドプロバイダーの**Private Endpoints for External Services**領域で、対象のプライベートリンク接続を選択し、 **...**をクリックします。

4. **Delete**をクリックし、削除を確認します。

</div>

<div label="CLI">

プライベートリンク接続を削除するには、次のコマンドを実行します。

```shell
ticloud serverless private-link-connection delete -c <cluster-id> --private-link-connection-id <private-link-connection-id>
```

</div>
</SimpleTab>

## 参照 {#see-also}

- [プライベートリンク接続を介してConfluent Cloudに接続する](/tidb-cloud/serverless-private-link-connection-to-aws-confluent.md)
- [プライベートリンク接続経由​​で Amazon RDS に接続する](/tidb-cloud/serverless-private-link-connection-to-aws-rds.md)
- [プライベートリンク接続経由​​でプロビジョニングされた Amazon MSK に接続する](/tidb-cloud/serverless-private-link-connection-to-amazon-msk.md)
- [プライベートリンク接続を介して Alibaba Cloud ApsaraDB RDS for MySQL に接続する](/tidb-cloud/serverless-private-link-connection-to-alicloud-rds.md)
- [プライベートリンク接続を介して AWS セルフホスト Kafka に接続する](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-aws.md)
- [プライベートリンク接続を介して Alibaba Cloud Self-Hosted Kafka に接続する](/tidb-cloud/serverless-private-link-connection-to-self-hosted-kafka-in-alicloud.md)
