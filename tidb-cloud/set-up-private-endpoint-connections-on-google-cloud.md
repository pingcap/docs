---
title: Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect
summary: Google Cloud Private Service Connect を介してTiDB Cloudクラスタに接続する方法を学習します。
---

# Google Cloud Private Service Connect 経由でTiDB Cloud専用クラスタに接続する {#connect-to-a-tidb-cloud-dedicated-cluster-via-google-cloud-private-service-connect}

このドキュメントでは、 [プライベートサービスコネクト](https://cloud.google.com/vpc/docs/private-service-connect)を介してTiDB Cloud Dedicated クラスタに接続する方法について説明します。Google Cloud Private Service Connect は、Google Cloud が提供するプライベート エンドポイント サービスです。

> **ヒント：**
>
> -   AWS のプライベートエンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
> -   Azure のプライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続する方法については、 [Azure Private Link 経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)参照してください。
> -   プライベート エンドポイント経由でTiDB Cloud Serverless クラスターに接続する方法については、 [プライベートエンドポイント経由でTiDB Cloud Serverless に接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

TiDB Cloud は、 [プライベートサービスコネクト](https://cloud.google.com/vpc/docs/private-service-connect)を介して Google Cloud VPC でホストされているTiDB Cloudサービスへの、高度に安全な一方向アクセスをサポートしています。エンドポイントを作成し、それを使用してTiDB Cloudサービスに接続できます。

Google Cloud Private Service Connect を利用することで、エンドポイント接続は安全かつプライベートに保たれ、データがパブリックインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

Google Cloud Private Service Connect のアーキテクチャは次のとおりです[^1]

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

プライベート エンドポイントとエンドポイント サービスの詳細な定義については、次の Google Cloud ドキュメントをご覧ください。

-   [プライベートサービスコネクト](https://cloud.google.com/vpc/docs/private-service-connect)
-   [エンドポイントを介して公開されたサービスにアクセスする](https://cloud.google.com/vpc/docs/configure-private-service-connect-services)

## 制限 {#restrictions}

-   この機能は、2023 年 4 月 13 日以降に作成されたTiDB Cloud Dedicated クラスターに適用されます。それより古いクラスターについては、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
-   Google Cloud Private Service Connect エンドポイントを作成できるのは、ロール`Organization Owner`と`Project Owner`のみです。
-   各 TiDB クラスターは、最大 10 個のエンドポイントからの接続を処理できます。
-   各 Google Cloud プロジェクトには、TiDBクラスタに接続するエンドポイントを最大 10 個まで含めることができます。
-   エンドポイント サービスが構成されたプロジェクトでは、Google Cloud でホストされるTiDB Cloud Dedicated クラスタを最大 8 個作成できます。
-   プライベート エンドポイントと接続する TiDB クラスターは同じリージョンに配置されている必要があります。
-   出力ファイアウォールルールは、エンドポイントの内部IPアドレスへのトラフィックを許可する必要があります。1 [暗黙の出口許可ファイアウォールルール](https://cloud.google.com/firewall/docs/firewalls#default_firewall_rules)任意の宛先IPアドレスへの出力を許可します。
-   VPC ネットワークで出力拒否ファイアウォールルールを作成した場合、または暗黙的に許可された出力動作を変更する階層型ファイアウォールポリシーを作成した場合、エンドポイントへのアクセスに影響が出る可能性があります。この場合、エンドポイントの内部宛先 IP アドレスへのトラフィックを許可する、特定の出力許可ファイアウォールルールまたはポリシーを作成する必要があります。

ほとんどのシナリオでは、VPC ピアリングではなくプライベートエンドポイント接続を使用することをお勧めします。ただし、以下のシナリオでは、プライベートエンドポイント接続ではなく VPC ピアリングを使用する必要があります。

-   高可用性を実現するために、ソースTiDBクラスターからターゲットTiDBクラスターへリージョンをまたいでデータをレプリケートするために、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用しています。現在、プライベートエンドポイントはリージョン間接続をサポートしていません。
-   TiCDC クラスターを使用してダウンストリーム クラスター (Amazon Aurora、MySQL、Kafka など) にデータをレプリケートしていますが、ダウンストリームのエンドポイント サービスを独自に維持することはできません。

## Google Cloud Private Service Connect を使用してプライベート エンドポイントを設定する {#set-up-a-private-endpoint-with-google-cloud-private-service-connect}

プライベート エンドポイント経由でTiDB Cloud Dedicated クラスターに接続するには、 [前提条件](#prerequisites)を完了し、次の手順に従います。

1.  [TiDBクラスタを選択](#step-1-select-a-tidb-cluster)
2.  [Google Cloud プライベート エンドポイントを作成する](#step-2-create-a-google-cloud-private-endpoint)
3.  [エンドポイントアクセスを許可する](#step-3-accept-endpoint-access)
4.  [TiDBクラスタに接続する](#step-4-connect-to-your-tidb-cluster)

複数のクラスタがある場合は、Google Cloud Private Service Connect を使用して接続するクラスタごとにこれらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

エンドポイントの作成を開始する前に:

-   Google Cloud プロジェクトで次の API を[有効にする](https://console.cloud.google.com/apis/library/compute.googleapis.com) 。
    -   [コンピューティングエンジン API](https://cloud.google.com/compute/docs/reference/rest/v1)
    -   [サービスディレクトリAPI](https://cloud.google.com/service-directory/docs/reference/rest)
    -   [クラウドDNS API](https://cloud.google.com/dns/docs/reference/v1)

-   エンドポイントを作成するために必要な権限を持つ次の[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)準備します。

    -   タスク:
        -   エンドポイントを作成する
        -   エンドポイントの[DNSエントリ](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#dns-endpoint)自動または手動で構成する
    -   必要なIAMロール:
        -   [コンピューティングネットワーク管理者](https://cloud.google.com/iam/docs/understanding-roles#compute.networkAdmin) (ロール/compute.networkAdmin)
        -   [サービスディレクトリエディター](https://cloud.google.com/iam/docs/understanding-roles#servicedirectory.editor) (ロール/サービスディレクトリ.エディター)

### ステップ1. TiDBクラスターを選択する {#step-1-select-a-tidb-cluster}

1.  プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲットTiDBクラスタの名前をクリックして概要ページに移動します。以下のいずれかのステータスのクラスタを選択できます。

    -   **利用可能**
    -   **復元**
    -   **変更**
    -   **インポート**

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  [**接続タイプ]**ドロップダウン リストで**[プライベート エンドポイント]**を選択し、 **[プライベート エンドポイント接続の作成]**をクリックします。

    > **注記：**
    >
    > プライベートエンドポイント接続を既に作成している場合は、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**[設定]** &gt; **[ネットワーク] を**クリックして**[ネットワーク]**ページに移動します。

### ステップ 2. Google Cloud プライベート エンドポイントを作成する {#step-2-create-a-google-cloud-private-endpoint}

1.  プライベート エンドポイント作成コマンドを生成するには、次の情報を指定します。
    -   **Google Cloud プロジェクト ID** : Google Cloud アカウントに関連付けられたプロジェクト ID。ID は[Google Cloud**ダッシュボード**ページ](https://console.cloud.google.com/home/dashboard)に記載されています。
    -   **Google Cloud VPC名**: 指定したプロジェクト内のVPCの名前[Google Cloud **VPC ネットワーク**ページ](https://console.cloud.google.com/networking/networks/list)で確認できます。
    -   **Google Cloud サブネット名**: 指定された VPC 内のサブネットの名前。VPC**ネットワークの詳細**ページで確認できます。
    -   **プライベート サービス接続エンドポイント名**: 作成するプライベート エンドポイントの一意の名前を入力します。
2.  情報を入力したら、 **[コマンドの生成] を**クリックします。
3.  生成されたコマンドをコピーします。
4.  [Google クラウド シェル](https://console.cloud.google.com/home/dashboard)を開き、コマンドを実行してプライベート エンドポイントを作成します。

### ステップ3. エンドポイントアクセスを許可する {#step-3-accept-endpoint-access}

Google Cloud Shell でコマンドを正常に実行したら、 TiDB Cloudコンソールに戻り、 **「エンドポイント アクセスを承認」**をクリックします。

エラー`not received connection request from endpoint`が表示された場合は、コマンドを正しくコピーし、Google Cloud Shell で正常に実行したことを確認してください。

### ステップ4. TiDBクラスターに接続する {#step-4-connect-to-your-tidb-cluster}

プライベート エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベート エンドポイントの接続ステータスが**「システム チェック中」**から**「アクティブ」**に変わるまで待ちます (約 5 分)。
2.  **「接続方法**」ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してクラスターに接続します。

### プライベートエンドポイントのステータスリファレンス {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[**プライベートエンドポイント**ページ](#prerequisites)に表示されます。

プライベート エンドポイントの可能なステータスについては、次のように説明されます。

-   **保留中**: 処理を待機しています。
-   **アクティブ**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントを削除しています。
-   **失敗**: プライベートエンドポイントの作成に失敗しました。その行の**「編集」を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの可能なステータスについては、次のように説明されています。

-   **作成中**: エンドポイント サービスを作成中です。これには 3 ～ 5 分かかります。
-   **アクティブ**: プライベート エンドポイントが作成されたかどうかに関係なく、エンドポイント サービスが作成されます。

## トラブルシューティング {#troubleshooting}

### TiDB Cloud がエンドポイント サービスの作成に失敗しました。どうすればよいでしょうか? {#tidb-cloud-fails-to-create-an-endpoint-service-what-should-i-do}

**「Google Cloud Private エンドポイント接続の作成」**ページを開いて TiDB クラスタを選択すると、エンドポイント サービスが自動的に作成されます。失敗と表示される場合、または長時間**「作成中**」状態のままになる場合は、エラー[サポートチケット](/tidb-cloud/tidb-cloud-support.md)送信してサポートを受けてください。

### Google Cloud でエンドポイントを作成できません。どうすればいいですか？ {#fail-to-create-an-endpoint-in-google-cloud-what-should-i-do}

この問題を解決するには、プライベートエンドポイント作成コマンドを実行した後にGoogle Cloud Shellから返されるエラーメッセージを確認する必要があります。権限関連のエラーの場合は、再試行する前に必要な権限を付与する必要があります。

### いくつかのアクションをキャンセルしました。エンドポイントへのアクセスを許可する前にキャンセルを処理するにはどうすればよいですか？ {#i-cancelled-some-actions-what-should-i-do-to-handle-cancellation-before-accepting-endpoint-access}

キャンセルされたアクションの未保存の下書きは保持も表示もされません。次回TiDB Cloudコンソールで新しいプライベートエンドポイントを作成する際は、各手順を繰り返す必要があります。

Google Cloud Shell でプライベート エンドポイントを作成するコマンドをすでに実行している場合は、Google Cloud コンソールで手動で[対応するエンドポイントを削除する](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint)実行する必要があります。

### サービス アタッチメントを直接コピーして生成されたエンドポイントがTiDB Cloudコンソールに表示されないのはなぜですか? {#why-can-t-i-see-the-endpoints-generated-by-directly-copying-the-service-attachment-in-the-tidb-cloud-console}

TiDB Cloudコンソールでは、 **「Google Cloud プライベート エンドポイント接続の作成」**ページで生成されたコマンドを通じて作成されたエンドポイントのみを表示できます。

ただし、サービス アタッチメントを直接コピーして生成されたエンドポイント (つまり、 TiDB Cloudコンソールで生成されたコマンドによって作成されていないエンドポイント) は、 TiDB Cloudコンソールに表示されません。

[^1]: Google Cloud Private Service Connectアーキテクチャの図は、Google Cloud ドキュメントの[プライベートサービスコネクト](https://cloud.google.com/vpc/docs/private-service-connect)ドキュメントからのものであり、Creative Commons Attribution 4.0 International ライセンスの下でライセンスされています。
