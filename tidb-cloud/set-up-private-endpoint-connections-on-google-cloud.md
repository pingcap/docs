---
title: Connect to a TiDB Dedicated Cluster via Google Cloud Private Service Connect
summary: Learn how to connect to your TiDB Cloud cluster via Google Cloud Private Service Connect.
---

# Google Cloud Private Service Connect 経由で TiDB 専用クラスタに接続する {#connect-to-a-tidb-dedicated-cluster-via-google-cloud-private-service-connect}

このドキュメントでは、Google Cloud Private Service Connect を介して TiDB 専用クラスターに接続する方法について説明します。 Google Cloud Private Service Connect は、Google Cloud が提供するプライベート エンドポイント サービスです。

> **ヒント：**
>
> -   AWS のプライベート エンドポイント経由で TiDB 専用クラスターに接続する方法については、 [AWS のプライベート エンドポイント経由で専用 TiDB に接続する](/tidb-cloud/set-up-private-endpoint-connections.md)を参照してください。
> -   プライベート エンドポイント経由で TiDB サーバーレス クラスターに接続する方法については、 [プライベートエンドポイント経由で TiDB サーバーレスに接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

TiDB Cloud は、 Google Cloud VPC でホストされているTiDB Cloudサービスへの、 [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)を介した安全性の高い一方向アクセスをサポートします。エンドポイントを作成し、それを使用してTiDB Cloudサービスに接続できます。

Google Cloud Private Service Connect を利用したエンドポイント接続は安全かつプライベートであり、データが公共のインターネットに公開されることはありません。さらに、エンドポイント接続は CIDR オーバーラップをサポートし、ネットワーク管理が容易になります。

プライベート エンドポイントのアーキテクチャは次のとおりです。

![Private Service Connect architecture](/media/tidb-cloud/google-cloud-psc-endpoint-overview.png)

プライベート エンドポイントとエンドポイント サービスの定義の詳細については、次の Google Cloud ドキュメントをご覧ください。

-   [プライベートサービス接続](https://cloud.google.com/vpc/docs/private-service-connect)
-   [エンドポイント経由で公開サービスにアクセスする](https://cloud.google.com/vpc/docs/configure-private-service-connect-services)

## 制限 {#restrictions}

-   この機能は、2023 年 4 月 13 日以降に作成された TiDB 専用クラスターに適用されます。古いクラスターについては、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。
-   Google Cloud Private Service Connect エンドポイントを作成できるのは、 `Organization Owner`と`Project Owner`の役割のみです。
-   各 TiDB クラスターは、最大 10 個のエンドポイントからの接続を処理できます。
-   各 Google Cloud プロジェクトには、TiDBクラスタに接続する最大 10 個のエンドポイントを含めることができます。
-   エンドポイント サービスが構成されたプロジェクトでは、Google Cloud でホストされる最大 8 つの TiDB 専用クラスタを作成できます。
-   接続するプライベート エンドポイントと TiDB クラスターは同じリージョンに存在する必要があります。
-   送信ファイアウォール ルールでは、エンドポイントの内部 IP アドレスへのトラフィックを許可する必要があります。 [暗黙の下り許可ファイアウォール ルール](https://cloud.google.com/firewall/docs/firewalls#default_firewall_rules)任意の宛先 IP アドレスへの出力を許可します。
-   VPC ネットワークで下り拒否ファイアウォール ルールを作成した場合、または暗黙的に許可された下り動作を変更する階層型ファイアウォール ポリシーを作成した場合、エンドポイントへのアクセスが影響を受ける可能性があります。この場合、エンドポイントの内部宛先 IP アドレスへのトラフィックを許可する特定の出力許可ファイアウォール ルールまたはポリシーを作成する必要があります。

ほとんどのシナリオでは、VPC ピアリング経由でプライベート エンドポイント接続を使用することをお勧めします。ただし、次のシナリオでは、プライベート エンドポイント接続の代わりに VPC ピアリングを使用する必要があります。

-   高可用性を実現するために、 [TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview)クラスターを使用して、ソース TiDB クラスターからリージョンをまたがるターゲット TiDB クラスターにデータをレプリケートしています。現在、プライベート エンドポイントはクロスリージョン接続をサポートしていません。
-   TiCDC クラスターを使用してデータをダウンストリームクラスター (Amazon Aurora、MySQL、Kafka など) にレプリケートしていますが、ダウンストリームのエンドポイント サービスを独自に維持することはできません。

## Google Cloud Private Service Connect を使用してプライベート エンドポイントをセットアップする {#set-up-a-private-endpoint-with-google-cloud-private-service-connect}

プライベート エンドポイント経由で TiDB 専用クラスターに接続するには、 [前提条件](#prerequisites)を完了し、次の手順に従います。

1.  [TiDB クラスターを選択する](#step-1-choose-a-tidb-cluster)
2.  [エンドポイントを作成するための情報を提供します](#step-2-provide-the-information-for-creating-an-endpoint)
3.  [エンドポイントアクセスを受け入れる](#step-3-accept-endpoint-access)
4.  [TiDB クラスターに接続する](#step-4-connect-to-your-tidb-cluster)

複数のクラスタがある場合は、Google Cloud Private Service Connect を使用して接続するクラスタごとにこれらの手順を繰り返す必要があります。

### 前提条件 {#prerequisites}

エンドポイントの作成を開始する前に、次のことを行ってください。

-   [有効にする](https://console.cloud.google.com/apis/library/compute.googleapis.com) Google Cloud プロジェクト内の次の API:
    -   [コンピューティング エンジン API](https://cloud.google.com/compute/docs/reference/rest/v1)
    -   [サービスディレクトリAPI](https://cloud.google.com/service-directory/docs/reference/rest)
    -   [クラウドDNS API](https://cloud.google.com/dns/docs/reference/v1)

-   エンドポイントの作成に必要な権限を付与した以下の[IAMの役割](https://cloud.google.com/iam/docs/understanding-roles)準備します。

    -   タスク:
        -   エンドポイントを作成する
        -   エンドポイントに[DNS エントリ](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#dns-endpoint)自動または手動で構成します
    -   必要なIAMロール:
        -   [コンピューティングネットワーク管理者](https://cloud.google.com/iam/docs/understanding-roles#compute.networkAdmin) (ロール/compute.networkAdmin)
        -   [サービスディレクトリエディター](https://cloud.google.com/iam/docs/understanding-roles#servicedirectory.editor) (ロール/サービスディレクトリ.エディタ)

次の手順を実行して、 **Google Cloud プライベート エンドポイント**ページに移動します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)にログインします。
2.  クリック<mdsvgicon name="icon-left-projects">複数のプロジェクトがある場合は、左下隅でターゲット プロジェクトに切り替え、 **[プロジェクト設定]**をクリックします。</mdsvgicon>
3.  プロジェクトの**[プロジェクト設定]**ページで、左側のナビゲーション ペインで**[ネットワーク アクセス]**をクリックし、 **[プライベート エンドポイント]**タブをクリックします。
4.  右上隅にある**[プライベート エンドポイントの作成]**をクリックし、 **[Google Cloud プライベート エンドポイント]**を選択します。

### ステップ 1. TiDB クラスターを選択する {#step-1-choose-a-tidb-cluster}

ドロップダウン リストをクリックして、利用可能な TiDB 専用クラスターを選択します。

次のいずれかのステータスのクラスターを選択できます。

-   **利用可能**
-   **復元中**
-   **変更中**
-   **インポート中**

### ステップ 2. エンドポイントを作成するための情報を入力します。 {#step-2-provide-the-information-for-creating-an-endpoint}

1.  次の情報を指定して、プライベート エンドポイント作成用のコマンドを生成します。
    -   **Google Cloud プロジェクト ID** : Google Cloud アカウントに関連付けられたプロジェクト ID。 ID は[Google Cloud**ダッシュボード**ページ](https://console.cloud.google.com/home/dashboard)で確認できます。
    -   **Google Cloud VPC Name** : 指定したプロジェクト内の VPC の名前。 [Google Cloud **VPC ネットワーク**ページ](https://console.cloud.google.com/networking/networks/list)で見つけることができます。
    -   **Google Cloud サブネット名**: 指定された VPC 内のサブネットの名前。これは、 **VPC ネットワークの詳細**ページで見つけることができます。
    -   **Private Service Connect エンドポイント名**: 作成されるプライベート エンドポイントの一意の名前を入力します。
2.  情報を入力したら、 **「コマンドの生成」**をクリックします。
3.  コマンドをコピーします。
4.  [Googleクラウドシェル](https://console.cloud.google.com/home/dashboard)に進み、コマンドを実行します。

### ステップ 3. エンドポイント アクセスを受け入れる {#step-3-accept-endpoint-access}

Google Cloud Shell でコマンドが正常に実行された後、 TiDB Cloudコンソールに戻り、 **[エンドポイント アクセスの受け入れ]**をクリックします。

エラー`not received connection request from endpoint`表示された場合は、コマンドが正しくコピーされ、Google Cloud Shell で正常に実行されたことを確認してください。

### ステップ 4. TiDB クラスターに接続する {#step-4-connect-to-your-tidb-cluster}

エンドポイント接続を受け入れたら、次の手順を実行して TiDB クラスターに接続します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページで、 **[アクション]**列の**[...]**をクリックします。
2.  **「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[プライベート エンドポイント]**タブを選択します。作成したプライベート エンドポイントが表示されます。 TiDB クラスターに接続するためのコマンドをコピーします。

### プライベート エンドポイントのステータス参照 {#private-endpoint-status-reference}

プライベート エンドポイント接続を使用すると、プライベート エンドポイントまたはプライベート エンドポイント サービスのステータスが[**プライベートエンドポイント**ページ](#prerequisites)に表示されます。

プライベート エンドポイントの考えられるステータスについては、次のように説明します。

-   **保留中**: 処理を待っています。
-   **Active** : プライベート エンドポイントを使用する準備ができています。このステータスのプライベート エンドポイントは編集できません。
-   **削除中**: プライベート エンドポイントは削除中です。
-   **失敗**: プライベート エンドポイントの作成は失敗します。その行の**「編集」を**クリックすると、作成を再試行できます。

プライベート エンドポイント サービスの考えられるステータスについては、次のように説明します。

-   **作成中**: エンドポイント サービスが作成されています。これには 3 ～ 5 分かかります。
-   **Active** : プライベート エンドポイントが作成されているかどうかに関係なく、エンドポイント サービスが作成されます。

## トラブルシューティング {#troubleshooting}

### TiDB Cloudはエンドポイント サービスの作成に失敗します。どうすればいいですか？ {#tidb-cloud-fails-to-create-an-endpoint-service-what-should-i-do}

**[Google Cloud プライベート エンドポイントの作成]**ページを開いて TiDB クラスターを選択すると、エンドポイント サービスが自動的に作成されます。失敗として表示されるか、**作成中**の状態が長時間続く場合は、 [サポートチケット](/tidb-cloud/tidb-cloud-support.md)送信してサポートを求めてください。

### Google Cloud でエンドポイントを作成できません。どうすればいいですか？ {#fail-to-create-an-endpoint-in-google-cloud-what-should-i-do}

この問題のトラブルシューティングを行うには、プライベート エンドポイント作成コマンドの実行後に Google Cloud Shell から返されるエラー メッセージを確認する必要があります。権限関連のエラーの場合は、再試行する前に必要な権限を付与する必要があります。

### いくつかのアクションをキャンセルしました。エンドポイント アクセスを受け入れる前にキャンセルを処理するにはどうすればよいですか? {#i-cancelled-some-actions-what-should-i-do-to-handle-cancellation-before-accepting-endpoint-access}

キャンセルされたアクションの未保存の下書きは保持されず、表示されません。次回TiDB Cloudコンソールで新しいプライベート エンドポイントを作成するときに、各手順を繰り返す必要があります。

Google Cloud Shell でプライベート エンドポイントを作成するコマンドをすでに実行している場合は、Google Cloud コンソールで[対応するエンドポイントを削除します](https://cloud.google.com/vpc/docs/configure-private-service-connect-services#delete-endpoint)で行う必要があります。

### TiDB Cloudコンソールでサービス アタッチメントを直接コピーして生成されたエンドポイントが表示されないのはなぜですか? {#why-can-t-i-see-the-endpoints-generated-by-directly-copying-the-service-attachment-in-the-tidb-cloud-console}

TiDB Cloudコンソールでは、 **「Google Cloud プライベート エンドポイントの作成」**ページで生成されたコマンドによって作成されたエンドポイントのみを表示できます。

ただし、サービス アタッチメントを直接コピーすることによって生成されたエンドポイント (つまり、 TiDB Cloudコンソールで生成されたコマンドを通じて作成されたものではない) は、 TiDB Cloudコンソールに表示されません。
