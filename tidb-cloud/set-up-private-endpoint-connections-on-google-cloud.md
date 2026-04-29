---
title: Connect to a TiDB Cloud Dedicated Cluster via Google Cloud Private Service Connect
summary: Google Cloud Private Service Connectを使用してTiDB Cloudクラスターに接続する方法を学びましょう。
---

# Google Cloud Private Service Connect を介してTiDB Cloud Dedicatedクラスタに接続します。 {#connect-to-a-tidb-cloud-dedicated-cluster-via-google-cloud-private-service-connect}

このドキュメントでは[プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)を介してTiDB Cloud Dedicatedクラスターに接続する方法について説明します。 Google Cloud Private Service Connect は、Google Cloud が提供するプライベート エンドポイント サービスです。

<CustomContent language="en,zh">

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   Azure のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)D dedicated クラスターに接続する」を参照してください。
> -   プライベートエンドポイントを介してTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、以下のドキュメントを参照してください。
>     -   [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
>     -   [Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

</CustomContent>

<CustomContent language="ja">

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続する方法については、 [AWS PrivateLink を介してTiDB Cloud Dedicatedクラスタに接続します。](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   Azure のプライベート エンドポイントを介してTiDB Cloud Dedicatedクラスターに接続する方法については、 [Azureプライベートリンクを介してTiDB Cloud Dedicatedクラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md)D dedicated クラスターに接続する」を参照してください。
> -   プライベートエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloud StarterまたはEssentialに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

</CustomContent>

TiDB Cloud は、 [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)経由で、Google Cloud VPC でホストされているTiDB Cloudサービスへの安全性の高い一方向のアクセスをサポートします。エンドポイントを作成し、それを使用してTiDB Cloudサービスに接続できます。

Google Cloud Private Service Connect を利用したエンドポイント接続は、安全かつプライベートであり、お客様のデータをパブリックインターネットに公開することはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートしており、ネットワーク管理が容易です。

Google Cloud Private Service Connect のアーキテクチャは以下のとおりです。 [^1]

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

プライベートエンドポイントおよびエンドポイントサービスに関するより詳細な定義については、以下の Google Cloud ドキュメントを参照してください。

-   [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)
-   [エンドポイントを介して公開サービスにアクセスします](https://cloud.google.com/vpc/docs/configure-private-service-connect-services)

## 制限 {#restrictions}

-   この機能は、2023年4月13日以降に作成されたTiDB Cloud Dedicatedクラスタに適用されます。それ以前のクラスタについては、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
-   `Organization Owner`および`Project Owner`ロールのみが、Google Cloud Private Service Connect エンドポイントを作成できます。
-   各TiDBクラスタは、最大10個のエンドポイントからの接続を処理できます。
-   各Google Cloudプロジェクトは、最大10個のエンドポイントをTiDBクラスタに接続できます。
-   2025年8月12日以降、Google Cloud上のTiDB Cloud Dedicatedクラスターでリージョンごとに作成できるGoogle Private Service Connect（PSC）接続の最大数は、NATサブネットCIDRブロックサイズによって異なります。
    -   `/20` : 地域ごとに最大 7 つの PSC 接続
    -   `/19` : 地域ごとに最大 23 の PSC 接続
    -   `/18` : 地域ごとに最大55のPSC接続
    -   `/17` : 地域ごとに最大 119 の PSC 接続
    -   `/16` : 地域ごとに最大 247 の PSC 接続
-   接続するプライベートエンドポイントとTiDBクラスタは、同じリージョンに配置されている必要があります。
-   送信ファイアウォール ルールでは、エンドポイントの内部 IP アドレスへのトラフィックを許可する必要があります。 [暗黙の送信許可ファイアウォールルール](https://cloud.google.com/firewall/docs/firewalls#default_firewall_rules)任意の宛先 IP アドレスへの送信を許可します。
-   VPCネットワークで送信拒否ファイアウォールルールを作成している場合、または暗黙的に許可される送信動作を変更する階層型ファイアウォールポリシーを作成している場合、エンドポイントへのアクセスに影響が出る可能性があります。この場合、エンドポイントの内部宛先IPアドレスへのトラフィックを許可する、特定の送信許可ファイアウォールルールまたはポリシーを作成する必要があります。

ほとんどのシナリオでは、VPCピアリングよりもプライベートエンドポイント接続を使用することをお勧めします。ただし、以下のシナリオでは、プライベートエンドポイント接続の代わりにVPCピアリングを使用する必要があります。

-   高可用性を実現するために、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスタを使用して、ソースTiDBクラスタからターゲットTiDBクラスタへリージョンをまたいでデータをレプリケートしています。現在、プライベートエンドポイントはリージョン間接続をサポートしていません。
-   TiCDCクラスタを使用してデータをダウンストリームクラスタ（Amazon Aurora、MySQL、Kafkaなど）に複製していますが、ダウンストリームのエンドポイントサービスを独自に維持することはできません。

## Google Cloud Private Service Connect を使用してプライベートエンドポイントを設定します。 {#set-up-a-private-endpoint-with-google-cloud-private-service-connect}

[前提条件](#prerequisites)エンドポイント経由でTiDB Cloud Dedicatedクラスターに接続するには、 を完了し、以下の手順に従ってください。

1.  [TiDBクラスタを選択してください](#step-1-select-a-tidb-cluster)
2.  [Google Cloudプライベートエンドポイントを作成する](#step-2-create-a-google-cloud-private-endpoint)
3.  [エンドポイントへのアクセスを許可する](#step-3-accept-endpoint-access)
4.  [TiDBクラスターに接続します](#step-4-connect-to-your-tidb-cluster)

複数のクラスターがある場合は、Google Cloud Private Service Connectを使用して接続する各クラスターに対して、これらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

エンドポイントの作成を開始する前に：

-   Google Cloud プロジェクトで次の API [有効にする](https://console.cloud.google.com/apis/library/compute.googleapis.com)。
    -   [Comput Engine API](https://cloud.google.com/compute/docs/reference/rest/v1)
    -   [サービスディレクトリAPI](https://cloud.google.com/service-directory/docs/reference/rest)
    -   [クラウドDNS API](https://cloud.google.com/dns/docs/reference/v1)

-   エンドポイントを作成するために必要な権限を持つ以下の[IAMロール](https://cloud.google.com/iam/docs/understanding-roles)を準備してください。

    -   タスク:
        -   エンドポイントを作成する
        -   エンドポイントの[DNSエントリ](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#dns-endpoint)自動または手動で構成する
    -   必須のIAMロール：
        -   コンピュータネットワーク[コンピュータネットワーク管理者](https://cloud.google.com/iam/docs/understanding-roles#compute.networkAdmin))
        -   サービスディレクトリエディター(roles/ [サービスディレクトリエディター](https://cloud.google.com/iam/docs/understanding-roles#servicedirectory.editor))

### ステップ1. TiDBクラスタを選択します {#step-1-select-a-tidb-cluster}

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして、概要ページに移動します。以下のいずれかのステータスのクラスタを選択できます。

    -   **利用可能**
    -   **復元**
    -   **変更する**
    -   **輸入**

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  **「接続タイプ」**ドロップダウンリストで**「プライベートエンドポイント」**を選択し、 **「プライベートエンドポイント接続の作成」を**クリックします。

    > **注記：**
    >
    > 既にプライベートエンドポイント接続を作成済みの場合、アクティブなエンドポイントが接続ダイアログに表示されます。追加のプライベートエンドポイント接続を作成するには、左側のナビゲーションペインで**「設定」** &gt; **「ネットワーク」**をクリックして、 **「ネットワーク」**ページに移動します。

### ステップ2. Google Cloudプライベートエンドポイントを作成する {#step-2-create-a-google-cloud-private-endpoint}

1.  プライベートエンドポイント作成用のコマンドを生成するには、以下の情報を提供してください。
    -   **Google Cloud プロジェクト ID** ：Google Cloud アカウントに関連付けられたプロジェクト ID です。この ID は[Google Cloud **Dashboard**ページ](https://console.cloud.google.com/home/dashboard)で確認できます。
    -   **Google Cloud VPC Name** : 指定したプロジェクト内の VPC の名前。 [Google Cloud **VPC ネットワークの**ページ](https://console.cloud.google.com/networking/networks/list)にあります。
    -   **Google Cloud サブネット名**：指定された VPC 内のサブネットの名前です。VPC**ネットワークの詳細**ページで確認できます。
    -   **プライベートサービス接続エンドポイント名**：作成されるプライベートエンドポイントの一意の名前を入力してください。
2.  情報を入力したら、 **「コマンド生成」**をクリックしてください。
3.  Google Cloud CLI または Google Cloud コンソールを使用して、プライベートエンドポイントを作成します。

<SimpleTab>
<div label="Use Google Cloud CLI">

1.  生成されたコマンドをコピーしてください。
2.  [Google Cloud Shell](https://console.cloud.google.com/home/dashboard)を開き、コマンドを実行してプライベートエンドポイントを作成します。

</div>
<div label="Use Google Cloud console">

1.  [Google Cloud Console](https://console.cloud.google.com/)で、現在のプロジェクトがTiDB Cloudに入力した**Google Cloud プロジェクト ID**と同じであることを確認してください。
2.  **VPC ネットワーク**&gt;**プライベート サービス接続**&gt;**接続済みエンドポイント**に移動し、 **[エンドポイントに接続]**をクリックします。
3.  TiDB Cloudで生成されたコマンドの値を使用してエンドポイントを設定します。
    -   **エンドポイント名**：コマンドで指定した転送ルール名を使用します。
    -   **対象**: **[公開サービス]**を選択し、 `--target-service-attachment`からサービス添付ファイル URI を入力します。
    -   **リージョン**：コマンドから地域を選択してください。
    -   **ネットワーク**: `--network`から VPC ネットワークを選択してください。
    -   **サブネットワーク**： `--subnet`からサブネットを選択してください。
4.  エンドポイントを作成するには、 **「エンドポイントの追加」**をクリックしてください。
5.  **「接続済みエンドポイント」**で、新しいエンドポイントが作成されていることを確認し、そのエンドポイント名を記録します。

</div>
</SimpleTab>

### ステップ3. エンドポイントへのアクセスを許可する {#step-3-accept-endpoint-access}

Google Cloudでエンドポイントを正常に作成したら、 TiDB Cloudコンソールに戻り、 **「エンドポイントアクセスを承認」**をクリックします。

エラー`not received connection request from endpoint`が表示された場合は、Google Cloud プロジェクトでエンドポイントが正常に作成されていること、およびその構成が生成されたコマンドと一致していることを確認してください。

### ステップ4. TiDBクラスターに接続します {#step-4-connect-to-your-tidb-cluster}

プライベートエンドポイントへの接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベートエンドポイントの接続ステータスが**「システムチェック中**」から**「アクティブ」**に変わるまでお待ちください（約5分）。
2.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。
3.  接続文字列を使用してクラスターに接続してください。

### プライベートエンドポイントの状態参照 {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[**プライベートエンドポイント**ページ](#prerequisites)ページに表示されます。

プライベートエンドポイントの可能なステータスは、以下のように説明されます。

-   **保留中**：処理待ち。
-   **アクティブ**：プライベートエンドポイントは使用可能です。このステータスのプライベートエンドポイントは編集できません。
-   **削除中**：プライベートエンドポイントが削除されています。
-   **失敗**：プライベートエンドポイントの作成に失敗しました。該当行の**「編集」を**クリックすると、作成を再試行できます。

プライベートエンドポイントサービスの可能なステータスは、以下のように説明されます。

-   **作成中**：エンドポイントサービスが作成されています。これには3～5分かかります。
-   **アクティブ**：プライベートエンドポイントが作成されるかどうかに関わらず、エンドポイントサービスが作成されます。

## トラブルシューティング {#troubleshooting}

### TiDB Cloudでエンドポイントサービスの作成に失敗しました。どうすればよいですか？ {#tidb-cloud-fails-to-create-an-endpoint-service-what-should-i-do}

エンドポイント サービスは、 **[Google Cloud Private エンドポイント接続の作成**] ページを開いて TiDB クラスターを選択すると自動的に作成されます。作成が失敗と表示される場合、または[サポートチケット](/tidb-cloud/tidb-cloud-support.md)**作成中] の**状態が長時間続く場合は、サポートに問い合わせてください。

### Google Cloudでエンドポイントを作成できませんでした。どうすればよいですか？ {#fail-to-create-an-endpoint-in-google-cloud-what-should-i-do}

問題のトラブルシューティングを行うには、プライベートエンドポイント作成コマンドを実行した後に Google Cloud Shell から返されるエラーメッセージを確認する必要があります。権限関連のエラーの場合は、再試行する前に必要な権限を付与してください。

### いくつかの操作をキャンセルしました。エンドポイントへのアクセスを許可する前に、キャンセルをどのように処理すればよいでしょうか？ {#i-cancelled-some-actions-what-should-i-do-to-handle-cancellation-before-accepting-endpoint-access}

キャンセルされたアクションの未保存の下書きは保持も表示もされません。次回TiDB Cloudコンソールで新しいプライベートエンドポイントを作成する際は、各手順を繰り返す必要があります。

Google Cloud Shell でプライベート エンドポイントを作成するコマンドをすでに実行している場合は、Google Cloud コンソールで手動で[対応するエンドポイントを削除します](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint)必要があります。

### TiDB Cloudコンソールで、サービス添付ファイルを直接コピーして生成されたエンドポイントが表示されないのはなぜですか？ {#why-can-t-i-see-the-endpoints-generated-by-directly-copying-the-service-attachment-in-the-tidb-cloud-console}

TiDB Cloudコンソールでは、 **[Google Cloudプライベートエンドポイント接続の作成**]ページで生成されたコマンドによって作成されたエンドポイントのみを表示できます。

ただし、サービス添付ファイルを直接コピーして生成されたエンドポイント（つまり、 TiDB Cloudコンソールで生成されたコマンドを使用して作成されたものではないエンドポイント）は、 TiDB Cloudコンソールには表示されません。

[^1]: Google Cloud Private Service Connectアーキテクチャの図は、クリエイティブ コモンズ表示 4.0 インターナショナルに基づいてライセンスされている、Google Cloud ドキュメントの[プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)ドキュメントからのものです。
