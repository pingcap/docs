---
title: Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link
summary: Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する方法を学びましょう。
---

# Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-azure-private-link}

このドキュメントでは[Azure プライベートリンク](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)経由でTiDB Cloud Dedicatedクラスターに接続する方法について説明します。

<CustomContent language="en,zh">

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   Google Cloud のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> -   プライベートエンドポイントを介してTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、以下のドキュメントを参照してください。
>     -   [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
>     -   [Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   Google Cloud のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)
> -   プライベートエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

</CustomContent>

TiDB Cloud は、 [Azure プライベートリンク](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)仮想ネットワークでホストされているTiDB Cloudサービスへの、Azure 経由の高度に安全な一方向アクセスをサポートしています。まるでサービスがお客様自身の仮想ネットワーク内にあるかのようにアクセスできます。仮想ネットワーク内にプライベートエンドポイントを作成し、そのエンドポイントを介して権限を付与してTiDB Cloudサービスに接続できます。

Azure Private Link を利用したエンドポイント接続は、安全かつプライベートであり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

Azure Private Link のアーキテクチャは次のとおりです: [^1]

![Azure Private Link architecture](/media/tidb-cloud/azure-private-endpoint-arch.png)

プライベートエンドポイントとエンドポイントサービスのより詳細な定義については、以下のAzureドキュメントを参照してください。

-   [Azureプライベートリンクとは何ですか？](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
-   [プライベートエンドポイントとは何ですか？](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
-   [プライベートエンドポイントを作成する](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## 制限 {#restrictions}

-   `Organization Owner`および`Project Owner`ロールのみがプライベートエンドポイントを作成できます。
-   接続するプライベートエンドポイントとTiDBクラスタは、同じリージョンに配置されている必要があります。

## Azure Private Link を使用してプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-azure-private-link}

プライベートエンドポイント経由でTiDB Cloud Dedicatedクラスタに接続するには、以下の手順を実行してください。

1.  [TiDBクラスタを選択してください](#step-1-select-a-tidb-cluster)
2.  [Azureプライベートエンドポイントを作成する](#step-2-create-an-azure-private-endpoint)
3.  [エンドポイントを受け入れる](#step-3-accept-the-endpoint)
4.  [TiDBクラスターに接続します](#step-4-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、Azure Private Link を使用して接続する各クラスターに対して、これらの手順を繰り返す必要があります。

### ステップ1. TiDBクラスタを選択します {#step-1-select-a-tidb-cluster}

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Dedicatedクラスタの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続の種類」**ドロップダウンリストで**「プライベートエンドポイント」**を選択し、 **「プライベートエンドポイント接続の作成」**をクリックして、 **「Azureプライベートエンドポイント接続の作成」**ダイアログを開きます。

> **注記：**
>
> 既にプライベートエンドポイント接続を作成済みの場合、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックして、 **「ネットワーク」**ページに移動します。

### ステップ2. Azureプライベートエンドポイントを作成する {#step-2-create-an-azure-private-endpoint}

1.  **「Azureプライベートエンドポイント接続の作成」**ダイアログで、プライベートリンクサービスのTiDB CloudリソースIDをコピーし、後で使用するためにダイアログを開いたままにしておきます。

    > **注記：**
    >
    > TiDB Cloud Dedicatedの各クラスターに対して、対応するエンドポイントサービスは、クラスター作成後3～4分で自動的に作成されます。

2.  AzureポータルまたはAzure CLIを使用して、プライベートエンドポイントを作成します。

<SimpleTab>
<div label="Use Azure portal">

1.  [Azureポータル](https://portal.azure.com/)にログインします。
2.  **「プライベートエンドポイント」**を検索し、検索結果から**「プライベートエンドポイント」**を選択してください。
3.  **プライベートエンドポイントの**ページで、 **[+ 作成]**をクリックします。
4.  **「基本」**タブで、プロジェクトとインスタンスの情報を入力し、 **「次へ: リソース」**をクリックします。
5.  **「リソース」**タブで、**接続方法**として**「リソース ID またはエイリアスを使用して Azure リソースに接続する」を**選択し、コピーしたTiDB Cloudリソース ID を**「リソース ID またはエイリアス」**フィールドに貼り付けます。
6.  引き続き**「次へ」**をクリックして残りの構成タブに進み、必要な設定を完了します。次に、 **[作成]**をクリックしてプライベート エンドポイントを作成してデプロイします。 Azure のデプロイが完了するまでに数秒かかる場合があります。詳細については、Azure ドキュメントの[プライベートエンドポイントを作成する](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint)参照してください。
7.  プライベートエンドポイントの作成とデプロイが完了したら、 **「リソースへ移動」**をクリックし、以下の手順を実行してください。

    -   左側のナビゲーションペインで**「設定」** ＞ **「プロパティ」**をクリックし、後で使用するために**リソースID**をコピーしてください。

        ![Azure private endpoint resource ID](/media/tidb-cloud/azure-private-endpoint-resource-id.png)

    -   左側のナビゲーションペインで**「設定」** ＞ **「DNS設定」**をクリックし、後で使用するために**IPアドレス**をコピーしてください。

        ![Azure private endpoint DNS IP](/media/tidb-cloud/azure-private-endpoint-dns-ip.png)

</div>
<div label="Use Azure CLI">

1.  Azure CLI にサインインして、サブスクリプションを選択してください。

    ```bash
    az login
    az account set --subscription ${your_subscription_id}
    ```

2.  **Azureプライベートエンドポイント接続の作成**ダイアログからコピーしたTiDB CloudリソースIDを使用して、プライベートエンドポイントを作成します。

    ```bash
    az network private-endpoint create \
      --name ${your_private_endpoint_name} \
      --resource-group ${your_resource_group_name} \
      --vnet-name ${your_vnet_name} \
      --subnet ${your_subnet_name} \
      --private-connection-resource-id "${your_tidb_cloud_resource_id}" \
      --connection-name ${your_private_endpoint_connection_name} \
      --location ${your_region}
    ```

3.  プライベートエンドポイントの**リソースID**を取得します。

    ```bash
    az network private-endpoint show \
      --name ${your_private_endpoint_name} \
      --resource-group ${your_resource_group_name} \
      --query "id" \
      --output tsv
    ```

4.  DNS設定からプライベートエンドポイントの**IPアドレス**を取得します。

    ```bash
    az network private-endpoint show \
      --name ${your_private_endpoint_name} \
      --resource-group ${your_resource_group_name} \
      --query "customDnsConfigs[0].ipAddresses[0]" \
      --output tsv
    ```

</div>
</SimpleTab>

### ステップ3. エンドポイントを受け入れる {#step-3-accept-the-endpoint}

1.  TiDB Cloudコンソールの**「Azureプライベートエンドポイント接続の作成」**ダイアログに戻り、コピーした**リソースID**と**IPアドレスを**それぞれのフィールドに貼り付けます。
2.  **「エンドポイントの検証」を**クリックして、プライベートエンドポイントへのアクセスを検証してください。エラーが発生した場合は、エラーメッセージの手順に従ってトラブルシューティングを行い、再度お試しください。
3.  検証が成功したら、 **「エンドポイントを承認」**をクリックして、プライベートエンドポイントからの接続を承認してください。

### ステップ4. TiDBクラスターに接続します {#step-4-connect-to-your-tidb-cluster}

エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベートエンドポイントの接続ステータスが**「アクティブ」**になるまでお待ちください（約5分）。ステータスを確認するには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックして、 **「ネットワーク」**ページに移動してください。
2.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してクラスターに接続してください。

### プライベートエンドポイントの状態参照 {#private-endpoint-status-reference}

プライベートエンドポイントまたはプライベートエンドポイントサービスのステータスを表示するには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックして、 **「ネットワーク」**ページに移動します。

プライベートエンドポイントの可能なステータスは、以下のように説明されます。

-   **発見**： TiDB Cloudは、リクエストを受け入れる前にエンドポイントサービスに関連付けられたプライベートエンドポイントを自動的に検出できるため、別のエンドポイントを作成する必要がなくなります。
-   **保留中**：処理待ち。
-   **アクティブ**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
-   **削除中**：プライベートエンドポイントが削除されています。
-   **失敗**：プライベートエンドポイントの作成に失敗しました。該当行の**「編集」を**クリックすると、作成を再試行できます。

プライベートエンドポイントサービスの可能なステータスは、以下のように説明されます。

-   **作成中**：エンドポイントサービスが作成されています。これには3～5分かかります。
-   **アクティブ**：プライベートエンドポイントが作成されるかどうかに関わらず、エンドポイントサービスが作成されます。

## トラブルシューティング {#troubleshooting}

### TiDB Cloudでエンドポイントサービスの作成に失敗しました。どうすればよいですか？ {#tidb-cloud-fails-to-create-an-endpoint-service-what-should-i-do}

**Azure プライベート エンドポイントの作成**ページを開き、TiDB クラスターを選択すると、エンドポイント サービスは自動的に作成されます。失敗と表示される場合、または**作成中の**状態が長時間続く場合は、サポートに問い合わせて[サポートチケット](/tidb-cloud/tidb-cloud-support.md)を受けてください。

### セットアップ中にアクションをキャンセルした場合、プライベートエンドポイントを受け入れる前に何をすべきですか？ {#if-i-cancel-the-action-during-setup-what-should-i-do-before-accepting-the-private-endpoint}

Azure プライベート エンドポイント接続機能は、プライベート エンドポイントを自動的に検出できます。つまり、 [Azureプライベートエンドポイントの作成](#step-2-create-an-azure-private-endpoint)Azure ポータルで、 TiDB Cloudコンソールの [ **Azure プライベート エンドポイント接続の作成**] ダイアログで**[キャンセル] を**クリックしても、作成されたエンドポイントを**[ネットワーク]**ページで表示できます。キャンセルが意図的でない場合は、エンドポイントの設定を続行してセットアップを完了できます。キャンセルが意図的な場合は、TiDB Cloudコンソールでエンドポイントを直接削除できます。

[^1]: Azure Private Linkアーキテクチャの図は、Creative Commons Attribution 4.0 International に基づいてライセンスされている、Azure ドキュメントの「Azureプライベートリンクサービス[Azureプライベートリンクサービスとは何ですか？](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview)ドキュメント ( [ソースファイルはGitHubにあります](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/private-link/private-link-service-overview.md)) からのものです。
