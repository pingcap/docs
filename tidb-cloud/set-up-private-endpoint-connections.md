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
-   プライベート エンドポイントのサポートは、 TiDB Cloud Dedicated Tier に対してのみ提供され、Developer Tier に対しては提供されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

ほとんどのシナリオでは、VPC ピアリング経由でプライベート エンドポイント接続を使用することをお勧めします。ただし、次のシナリオでは、プライベート エンドポイント接続の代わりに VPC ピアリングを使用する必要があります。

-   [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)のクラスターを使用して、ソース TiDB クラスターからターゲット TiDB クラスターにリージョン間でデータをレプリケートし、高可用性を実現しています。現在、プライベート エンドポイントはクロスリージョン接続をサポートしていません。
-   TiCDC クラスターを使用してダウンストリーム クラスター (Amazon Aurora、MySQL、Kafka など) にデータをレプリケートしていますが、エンドポイント サービスを自分で維持することはできません。
-   PD または TiKV ノードに直接接続しています。

## AWS でプライベート エンドポイントを設定する {#set-up-a-private-endpoint-with-aws}

このセクションでは、AWS PrivateLink を使用してプライベート エンドポイントを設定する方法について説明します。

次の手順を実行して、プライベート エンドポイントを設定します。複数のクラスターがある場合は、AWS PrivateLink を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

TiDB Cloudは、Dedicated Tier クラスターのプライベート エンドポイントのみをサポートします。プライベート エンドポイントを作成する前に、Dedicated Tier クラスターを作成する必要があります。詳細な手順については、 [TiDB Cloudで TiDBクラスタを作成する](/tidb-cloud/create-tidb-cluster.md)を参照してください。

#### ステップ 1. プライベート エンドポイントの作成ページを開く {#step-1-open-the-private-endpoint-creation-page}

プライベート エンドポイントの作成ページを開くには、次の手順を実行します。

1.  TiDB Cloudコンソールで [**プロジェクト設定**] タブをクリックし、左側のメニューで [<strong>プライベート エンドポイント</strong>] をクリックします。
2.  [**プライベート エンドポイント**] ページで、右上隅にある [<strong>追加</strong>] をクリックして作成ページを開きます。

> **ヒント：**
>
> または、次の手順に従ってプライベート エンドポイントの作成ページを開くこともできます。
>
> 1.  TiDB Cloudコンソールで、[**クラスター**] ページに移動します。
> 2.  クラスターを見つけて、クラスター領域の右上隅にある [**接続**] をクリックします。接続ダイアログボックスが表示されます。
> 3.  [**プライベート エンドポイント**] タブを選択します。プライベート エンドポイントが作成されていない場合は、ダイアログで [<strong>作成</strong>] をクリックして作成ページを開きます。

#### ステップ 2. TiDB クラスターを選択する {#step-2-choose-a-tidb-cluster}

ドロップダウン リストをクリックして、プライベート エンドポイントを作成する TiDB クラスターを選択し、 [**次へ**] をクリックします。

> **ノート：**
>
> クラスターが作成される前は、ドロップダウン リストに表示されません。

#### ステップ 3. サービス エンドポイント リージョンを選択する {#step-3-choose-the-service-endpoint-region}

**リージョン**リストから、プライベート エンドポイントを作成するリージョンを選択します。次に、[<strong>次へ</strong>] をクリックします。

> **ノート：**
>
> デフォルトのリージョンは、クラスターが配置されている場所です。変更しないでください。クロスリージョン プライベート エンドポイントは現在サポートされていません。

#### ステップ 4.AWS インターフェイス エンドポイントを作成する {#step-4-create-an-aws-interface-endpoint}

この段階で、 TiDB Cloudはエンドポイント サービスの作成を開始します。これには 3 ～ 4 分かかります。作成プロセス中に、次の操作を実行します。

1.  **VPC ID**および<strong>サブネット ID</strong>フィールドに入力します。 ID は AWS マネジメント コンソールから取得できます。

    これらの ID を取得する方法がわからない場合は、[**手順の表示**] をクリックすると、参照用の 2 つのスクリーンショットが表示されます。

2.  エンドポイント サービスが作成されたら、[ **Create VPC Interface Endpoint]**領域のコマンドを確認し、エンドポイント サービス名をメモします。

    ![Endpoint service name](/media/tidb-cloud/private-endpoint/private-endpoint-service-name.png)

3.  AWS で VPC インターフェイス エンドポイントを作成します。 AWS マネジメント コンソールまたは AWS CLI を使用できます。

    <SimpleTab>
     <div label="Use AWS Console">

    AWS マネジメント コンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

    1.  AWS マネジメント コンソールで、[ **VPC** ] &gt; [<strong>エンドポイント</strong>] に移動し、右上隅にある [<strong>エンドポイントの作成</strong>] をクリックします。<strong>エンドポイントの作成</strong>ページが表示されます。

        ![Create endpoint](/media/tidb-cloud/private-endpoint/create-endpoint-1.png)

    2.  [**サービス カテゴリ]**で、[<strong>その他のエンドポイント サービス]</strong>を選択します。

    3.  **Service settings**で、 TiDB Cloudコンソールの<strong>Interface endpoint</strong>ページから取得したエンドポイント サービス名を入力し、 <strong>Verify service</strong>をクリックします。

        ![Verify endpoint service](/media/tidb-cloud/private-endpoint/create-endpoint-2.png)

    4.  サービス名が確認されたら、 VPC の下で、ドロップダウン リストから**VPC**を選択します。次に、事前設定された<strong>サブネット</strong>領域が表示されます。

    5.  [**サブネット**] 領域で、TiDB クラスターが配置されている可用性ゾーンを選択します。次に、ページの下部にある [<strong>エンドポイントの作成</strong>] をクリックします。

        ![Create endpoint service 2](/media/tidb-cloud/private-endpoint/create-endpoint-3.png)

    > **ヒント：**
    >
    > サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、[**サブネット**] 領域で AZ を選択できない場合があります。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合は[PingCAP テクニカル サポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)にお問い合わせください。

    </div>
     <div label="AWS CLI">

    AWS CLI を使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

    1.  AWS コマンド ライン インターフェイス (AWS CLI) をインストールします。

        ```bash
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        ```

    2.  アカウント情報に従って AWS CLI を設定します。 AWS CLI で必要な情報を取得するには、 [AWS CLI 設定の基本](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)を参照してください。

        ```bash
        aws configure
        ```

    3.  **Create VPC Interface Endpoint**領域のコマンドをコピーし、ターミナルで実行して VPC インターフェイス エンドポイントを作成します。次に、[<strong>次へ</strong>] をクリックします。

    エンドポイント サービスが作成されると、コマンド内のプレースホルダーは自動的に実際の値に置き換えられます。

    > **ヒント：**
    >
    > -   サービスが 3 つ以上のアベイラビリティ ゾーン (AZ) にまたがっている場合、VPC エンドポイント サービスがサブネットの AZ をサポートしていないことを示すエラー メッセージが表示されます。この問題は、TiDB クラスターが配置されている AZ に加えて、選択したリージョンに余分な AZ がある場合に発生します。この場合、 [PingCAP テクニカル サポート](https://docs.pingcap.com/tidbcloud/tidb-cloud-support)に連絡できます。
    >
    > -   TiDB Cloudがエンドポイント サービスの作成をバックグラウンドで完了するまで、コマンドをコピーすることはできません。

    </div>
     </SimpleTab>

#### ステップ 5. エンドポイント接続を受け入れる {#step-5-accept-the-endpoint-connection}

ボックスに VPC エンドポイント ID を入力し、[**次へ**] をクリックします。

#### ステップ 6. プライベート DNS を有効にする {#step-6-enable-private-dns}

[**コピー**] ボタンをクリックしてコマンドをコピーし、AWS CLI で実行します。 `<your_vpc_endpoint_id>`プレースホルダーは、ステップ 5 で指定した値に自動的に置き換えられます。

または、AWS マネジメント コンソールでプライベート DNS を有効にすることもできます。方法がわからない場合は、[**説明を表示**] をクリックすると、参照用のスクリーンショットが表示されます。

次に、 [作成] をクリックして、プライベート エンドポイントの**作成**を完了します。

#### ステップ 7. エンドポイント サービスに接続する {#step-7-connect-to-the-endpoint-service}

詳細は[プライベート エンドポイント経由で TiDB クラスターに接続する](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-private-endpoint)を参照してください。

## プライベート エンドポイントのステータス リファレンス {#private-endpoint-status-reference}

[プライベート エンドポイント接続](/tidb-cloud/set-up-private-endpoint-connections.md)を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[**プライベート エンドポイント**ページ](/tidb-cloud/set-up-private-endpoint-connections.md#step-1-open-the-private-endpoint-creation-page)に表示されます。

プライベート エンドポイントの可能なステータスは、次のように説明されています。

-   **未構成**: エンドポイント サービスを作成したばかりですが、プライベート エンドポイントはまだ作成していません。その行の [<strong>編集</strong>] をクリックすると、プライベート エンドポイントを作成する<strong>インターフェイス エンドポイント</strong>ステージに移動します。詳細は[ステップ 4. エンドポイント サービスを作成する](/tidb-cloud/set-up-private-endpoint-connections.md#step-4-create-an-aws-interface-endpoint)を参照してください。
-   **Initiating** : プライベート エンドポイントの作成の<strong>インターフェイス エンドポイント</strong>ステージで VPC ID を入力した後、プライベート エンドポイントが開始または検証されています。新しい<strong>プライベート エンドポイント</strong>ページを開くと、行の [<strong>編集</strong>] ボタンが無効になっていることがわかります。
-   **Pending** : プライベート エンドポイントを作成する<strong>インターフェイス エンドポイント</strong>ステージで VPC ID が検証された後、プライベート DNS はまだ有効になっていません。その行の [<strong>編集</strong>] をクリックすると、プライベート エンドポイントを作成する<strong>プライベート DNS</strong>の有効化ステージに移動します。詳細は[ステップ 6.プライベート DNS を有効にする](/tidb-cloud/set-up-private-endpoint-connections.md#step-6-enable-private-dns)を参照してください。
-   **Active** : プライベート エンドポイントを使用する準備ができています。このステータスのプライベート エンドポイントは編集できません。
-   **削除**中 : プライベート エンドポイントを削除しています。
-   **Failed** : プライベート エンドポイントの作成に失敗しました。その行の [<strong>編集</strong>] をクリックして、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスは、次のように説明されています。

-   **作成**中 : エンドポイント サービスが作成されています。これには 3 ～ 5 分かかります。
-   **Active** : プライベート エンドポイントが作成されているかどうかに関係なく、エンドポイント サービスが作成されます。
-   **削除**中 : エンドポイント サービスまたはクラスターを削除しています。これには 3 ～ 5 分かかります。
