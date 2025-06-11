---
title: Connect to a TiDB Cloud Dedicated Cluster via Azure Private Link
summary: Azure Private Link 経由でTiDB Cloud Dedicated クラスタに接続する方法を学習します。
---

# Azure Private Link 経由でTiDB Cloud専用クラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-azure-private-link}

このドキュメントでは、 [Azure プライベート リンク](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)を介してTiDB Cloud Dedicated クラスターに接続する方法について説明します。

> **ヒント：**
>
> -   AWS のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
> -   Google Cloud のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスタに接続する方法については、 [Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)ご覧ください。
> -   プライベート エンドポイント経由でTiDB Cloud Serverless クラスターに接続する方法については、 [プライベートエンドポイント経由でTiDB Cloud Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

TiDB Cloud は、 Azure 仮想ネットワークでホストされているTiDB Cloudサービスへの、 [Azure プライベート リンク](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)経由の高度に安全な一方向アクセスをサポートします。これは、サービスがお客様の仮想ネットワーク内にあるかのように機能します。仮想ネットワーク内にプライベートエンドポイントを作成し、権限を持つエンドポイント経由でTiDB Cloudサービスに接続できます。

Azure Private Link を利用することで、エンドポイント接続は安全かつプライベートになり、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR 重複をサポートし、ネットワーク管理が容易になります。

Azure Private Link のアーキテクチャは次のとおりです[^1]

![Azure Private Link architecture](/media/tidb-cloud/azure-private-endpoint-arch.png)

プライベート エンドポイントとエンドポイント サービスの詳細な定義については、次の Azure ドキュメントを参照してください。

-   [Azureプライベートリンクとは](https://learn.microsoft.com/en-us/azure/private-link/private-link-overview)
-   [プライベートエンドポイントとは](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview)
-   [プライベートエンドポイントを作成する](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip)

## 制限 {#restrictions}

-   プライベート エンドポイントを作成できるのは、ロール`Organization Owner`と`Project Owner`のみです。
-   プライベート エンドポイントと接続する TiDB クラスターは同じリージョンに配置されている必要があります。

## Azure Private Link を使用してプライベート エンドポイントを設定する {#set-up-a-private-endpoint-with-azure-private-link}

プライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続するには、次の手順を実行します。

1.  [TiDBクラスタを選択](#step-1-select-a-tidb-cluster)
2.  [Azureプライベートエンドポイントを作成する](#step-2-create-an-azure-private-endpoint)
3.  [エンドポイントを受け入れる](#step-3-accept-the-endpoint)
4.  [TiDBクラスタに接続する](#step-4-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、Azure Private Link を使用して接続するクラスターごとにこれらの手順を繰り返す必要があります。

### ステップ1. TiDBクラスターを選択する {#step-1-select-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、ターゲット TiDB クラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[接続の種類]**ドロップダウン リストで**[プライベート エンドポイント]**を選択し、 **[プライベート エンドポイント接続の作成]**をクリックして**[Azure プライベート エンドポイント接続の作成]**ダイアログを開きます。

> **注記：**
>
> プライベートエンドポイント接続を既に作成している場合は、接続ダイアログにアクティブなエンドポイントが表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインの**「ネットワーク」**ページに移動してください。

### ステップ2. Azureプライベートエンドポイントを作成する {#step-2-create-an-azure-private-endpoint}

1.  **[Azure プライベート エンドポイント接続の作成**] ダイアログで、プライベート リンク サービスのTiDB Cloudリソース ID をコピーし、後で使用するためにダイアログを開いたままにしておきます。

    > **注記：**
    >
    > 各TiDB Cloud Dedicated クラスターでは、クラスターの作成後 3 ～ 4 分以内に、対応するエンドポイント サービスが自動的に作成されます。

2.  [Azureポータル](https://portal.azure.com/)にログインし、コピーしたTiDB Cloudリソース ID を使用して、次のようにクラスターのプライベート エンドポイントを作成します。

    1.  Azure ポータルで、**プライベート エンドポイント**を検索し、結果から**プライベート エンドポイント**を選択します。
    2.  **プライベート エンドポイント**ページで、 **+ 作成 を**クリックします。
    3.  **[基本]**タブで、プロジェクトとインスタンスの情報を入力し、 **[次へ: リソース]**をクリックします。
    4.  **[リソース]**タブで、**接続方法**として**[リソース ID またはエイリアスで Azure リソースに接続する]**を選択し、 TiDB Cloudリソース ID を**[リソース ID またはエイリアス]**フィールドに貼り付けます。
    5.  **「次へ」**をクリックし、残りの構成タブで必要な設定を完了してください。 **「作成」**をクリックして、プライベートエンドポイントを作成してデプロイします。Azure によるデプロイが完了するまで数秒かかる場合があります。詳細については、Azure ドキュメントの[プライベートエンドポイントを作成する](https://learn.microsoft.com/en-us/azure/private-link/create-private-endpoint-portal?tabs=dynamic-ip#create-a-private-endpoint)参照してください。

3.  プライベート エンドポイントが作成され、デプロイされたら、 **[リソースに移動] を**クリックし、次の操作を行います。

    -   左側のナビゲーション ペインで**[設定]** &gt; **[プロパティ]**をクリックし、後で使用するために**リソース ID**をコピーします。

        ![Azure private endpoint resource ID](/media/tidb-cloud/azure-private-endpoint-resource-id.png)

    -   左側のナビゲーション ペインで**[設定]** &gt; **[DNS 構成]**をクリックし、後で使用するために**IP アドレス**をコピーします。

        ![Azure private endpoint DNS IP](/media/tidb-cloud/azure-private-endpoint-dns-ip.png)

### ステップ3.エンドポイントを受け入れる {#step-3-accept-the-endpoint}

1.  TiDB Cloudコンソールの**[Azure プライベート エンドポイント接続の作成**] ダイアログに戻り、コピーした**リソース ID**と**IP アドレスを**対応するフィールドに貼り付けます。
2.  **「エンドポイントの検証」**をクリックして、プライベートエンドポイントへのアクセスを検証してください。エラーが発生した場合は、エラーメッセージに従ってトラブルシューティングを行い、もう一度お試しください。
3.  検証が成功したら、 **「エンドポイントを承認」**をクリックして、プライベート エンドポイントからの接続を承認します。

### ステップ4. TiDBクラスターに接続する {#step-4-connect-to-your-tidb-cluster}

エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベートエンドポイントの接続ステータスが**アクティブ**になるまで（約5分）お待ちください。クラスターの**「ネットワーク」**ページに移動して、ステータスを確認できます。
2.  **「接続方法**」ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してクラスターに接続します。

### プライベートエンドポイントのステータスリファレンス {#private-endpoint-status-reference}

クラスターの**[ネットワーク]**ページで、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスを表示できます。

プライベート エンドポイントの可能なステータスについては、次のように説明されます。

-   **検出済み**: TiDB Cloud は、リクエストを受け入れる前にエンドポイント サービスに関連付けられたプライベート エンドポイントを自動的に検出し、別のエンドポイントを作成する必要性を回避できます。
-   **保留中**: 処理を待機しています。
-   **アクティブ**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントを削除しています。
-   **失敗**: プライベートエンドポイントの作成に失敗しました。その行の**「編集」を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスについては、次のように説明されています。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **アクティブ**: プライベート エンドポイントが作成されたかどうかに関係なく、エンドポイント サービスが作成されます。

## トラブルシューティング {#troubleshooting}

### TiDB Cloud がエンドポイント サービスの作成に失敗しました。どうすればよいでしょうか? {#tidb-cloud-fails-to-create-an-endpoint-service-what-should-i-do}

**「Azure プライベート エンドポイントの作成」**ページを開いて TiDB クラスターを選択すると、エンドポイント サービスが自動的に作成されます。失敗と表示される場合、または長時間**「作成中**」状態のままになる場合は、エラー[サポートチケット](/tidb-cloud/tidb-cloud-support.md)送信してサポートを受けてください。

### セットアップ中にアクションをキャンセルした場合、プライベート エンドポイントを受け入れる前に何をすればよいですか? {#if-i-cancel-the-action-during-setup-what-should-i-do-before-accepting-the-private-endpoint}

Azureプライベートエンドポイント接続機能は、プライベートエンドポイントを自動的に検出します。つまり、Azureポータルで[Azureプライベートエンドポイントの作成](#step-2-create-an-azure-private-endpoint)クリックした後、 TiDB Cloudコンソールの**「Azureプライベートエンドポイント接続の作成」**ダイアログで「**キャンセル」をクリック**しても、 **「ネットワーク」**ページで作成されたエンドポイントを確認できます。キャンセルが意図的でない場合は、エンドポイントの構成を続行してセットアップを完了できます。キャンセルが意図的である場合は、 TiDB Cloudコンソールで直接エンドポイントを削除できます。

[^1]: Azure Private Linkアーキテクチャの図は、Azure ドキュメントの[Azure Private Link サービスとは](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview)のドキュメント ( [GitHub上のソースファイル](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/private-link/private-link-service-overview.md) ) からのものであり、Creative Commons Attribution 4.0 International ライセンスの下でライセンスされています。
