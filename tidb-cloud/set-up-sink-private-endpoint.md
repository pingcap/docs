---
title: Set Up Private Endpoint for Changefeeds
summary: 変更フィードのプライベートエンドポイントを設定する方法を学習します。
---

# Changefeeds のプライベートエンドポイントを設定する {#set-up-private-endpoint-for-changefeeds}

このドキュメントでは、 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターで変更フィード用のプライベートエンドポイントを作成し、プライベート接続を介してセルフホスト型 Kafka または MySQL にデータを安全にストリーミングできるようにする方法について説明します。

## 制限 {#restrictions}

同じVPC内では、AWSのプライベートエンドポイントサービス、Google Cloudのサービスアタッチメント、またはAzureのプライベートリンクサービスごとに、最大5つのプライベートエンドポイントを設定できます。この上限を超える場合は、新しいプライベートエンドポイントを作成する前に、未使用のプライベートエンドポイントを削除してください。

## 前提条件 {#prerequisites}

-   プライベートエンドポイント作成の権限を確認する
-   ネットワーク接続を設定する

### 権限 {#permissions}

組織内で次のいずれかのロールを持つユーザーのみが、変更フィードのプライベートエンドポイントを作成できます。

-   `Organization Owner`
-   `Project Owner`
-   `Project Data Access Read-Write`

TiDB Cloudのロールの詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

### ネットワーク {#network}

プライベートエンドポイントは、クラウド プロバイダーの**Private Link**または**Private Service Connect**テクノロジーを活用し、VPC 内のリソースが、あたかもそれらのサービスが VPC 内で直接ホストされているかのように、プライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。

<SimpleTab>
<div label="AWS">

changefeed ダウンストリーム サービスが AWS でホストされている場合は、次の情報を収集します。

-   ダウンストリーム サービスのプライベートエンドポイント サービスの名前
-   ダウンストリーム サービスがデプロイされているアベイラビリティ ゾーン (AZ)

ダウンストリーム サービスでプライベートエンドポイント サービスが利用できない場合は、手順[ステップ 2. Kafka クラスターをプライベートリンク サービスとして公開する](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)に従ってロード バランサーとプライベートリンク サービスを設定します。

</div>

<div label="Google Cloud">

changefeed ダウンストリーム サービスが Google Cloud でホストされている場合は、ダウンストリーム サービスのサービス アタッチメント情報を収集します。

ダウンストリーム サービスでサービス アタッチメントが利用できない場合は、手順[ステップ2. Kafka-proxyをプライベートサービス接続サービスとして公開する](/tidb-cloud/setup-self-hosted-kafka-private-service-connect.md#step-2-expose-kafka-proxy-as-private-service-connect-service)に従ってサービス アタッチメント情報を取得します。

</div>

<div label="Azure">

changefeed ダウンストリーム サービスが Azure でホストされている場合は、ダウンストリーム サービスのプライベートリンク サービスのエイリアスを収集します。

ダウンストリーム サービスでプライベートエンドポイント サービスが利用できない場合は、手順[ステップ 2. Kafka クラスターをプライベートリンク サービスとして公開する](/tidb-cloud/setup-azure-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)に従ってロード バランサーとプライベートリンク サービスを設定します。

</div>
</SimpleTab>

## ステップ1. クラスターのネットワークページを開きます {#step-1-open-the-networking-page-for-your-cluster}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。

    > **Tip:**
    >
    > 左上隅のコンボボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

3.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク] を**クリックします。

## ステップ2. 変更フィードのプライベートエンドポイントを構成する {#step-2-configure-the-private-endpoint-for-changefeeds}

構成手順は、クラスターがデプロイされているクラウド プロバイダーによって異なります。

<SimpleTab>
<div label="AWS">

1.  **[ネットワーキング]**ページで、 **[外部サービス用 AWS プライベートエンドポイント]**セクションの**[外部サービス用プライベートエンドポイントの作成]**をクリックします。

2.  **「外部サービス用プライベートエンドポイントの作成」**ダイアログで、プライベートエンドポイントの名前を入力します。

3.  リマインダーに従って、 TiDB Cloudの[AWS プリンシパル](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts)にエンドポイントの作成を承認します。

4.  セクション[ネットワーク](#network)で収集した**Endpoint Service Name**を入力します。

5.  **Number of AZs**を選択します。AZ の数と AZ ID が Kafka のデプロイメントと一致していることを確認してください。

6.  このプライベートエンドポイントが Apache Kafka 用に作成される場合は、 **Kafka 用のアドバタイズドリスナーを構成する**チェックボックスを選択します。

7.  **TiDB Managed**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka のアドバタイズされたリスナーを構成します。

    -   アドバタイズされたリスナーに**TiDB Managed**ドメインを使用するには、 **Domain Pattern**フィールドに一意の文字列を入力し、 **「生成」**をクリックします。TiDB は、各アベイラビリティゾーンのサブドメインを持つブローカーアドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメイン タイプを**[カスタム]**に切り替え、 **Custom Domain**フィールドにルート ドメインを入力し、[**チェック]**をクリックして、各アベイラビリティー ゾーンのブローカー サブドメインを指定します。

8.  **[作成]**をクリックして構成を検証し、プライベートエンドポイントを作成します。

</div>

<div label="Google Cloud">

1.  **[ネットワーキング]**ページで、 **[外部サービス用 Google Cloud プライベートエンドポイント]**セクションの**[外部サービス用プライベートエンドポイントの作成]**をクリックします。

2.  **「外部サービス用プライベートエンドポイントの作成」**ダイアログで、プライベートエンドポイントの名前を入力します。

3.  リマインダーに従って、 TiDB Cloudの[Google Cloud プロジェクト](https://cloud.google.com/resource-manager/docs/creating-managing-projects)にエンドポイントの作成を事前承認するよう許可するか、エンドポイント接続要求を受け取ったら手動で承認します。

4.  セクション[ネットワーク](#network)で収集した**Service Attachment**を入力します。

5.  このプライベートエンドポイントが Apache Kafka 用に作成される場合は、 **Kafka 用のアドバタイズドリスナーを構成する**チェックボックスを選択します。

6.  **TiDB Managed**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka のアドバタイズされたリスナーを構成します。

    -   アドバタイズされたリスナーに**TiDB Managed**ドメインを使用するには、 **Domain Pattern**フィールドに一意の文字列を入力し、 **「生成」**をクリックします。TiDB は、各アベイラビリティゾーンのサブドメインを持つブローカーアドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメイン タイプを**[カスタム]**に切り替え、 **Custom Domain**フィールドにルート ドメインを入力し、[**チェック]**をクリックして、各アベイラビリティー ゾーンのブローカー サブドメインを指定します。

7.  **[作成]**をクリックして構成を検証し、プライベートエンドポイントを作成します。

</div>

<div label="Azure">

1.  **[ネットワーク]**ページで、 **[外部サービス用 Azure プライベートエンドポイント]**セクションの**[外部サービス用プライベートエンドポイントの作成]**をクリックします。

2.  **「外部サービス用プライベートエンドポイントの作成」**ダイアログで、プライベートエンドポイントの名前を入力します。

3.  変更フィードを作成する前に、リマインダーに従って、 TiDB Cloudの Azure サブスクリプションを承認するか、エイリアスを持つすべてのユーザーが Private Link サービスにアクセスできるようにしてください。Private Link サービスの可視性に関する詳細については、Azure ドキュメントの[制御サービスの公開](https://learn.microsoft.com/en-us/azure/private-link/private-link-service-overview#control-service-exposure)を参照してください。

4.  セクション[ネットワーク](#network)で収集した**プライベートリンク サービスのエイリアス**を入力します。

5.  このプライベートエンドポイントが Apache Kafka 用に作成される場合は、 **Kafka 用のアドバタイズドリスナーを構成する**チェックボックスを選択します。

6.  **TiDB Managed**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka のアドバタイズされたリスナーを構成します。

    -   アドバタイズされたリスナーに**TiDB Managed**ドメインを使用するには、 **Domain Pattern**フィールドに一意の文字列を入力し、 **「生成」**をクリックします。TiDB は、各アベイラビリティゾーンのサブドメインを持つブローカーアドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメイン タイプを**[カスタム]**に切り替え、 **Custom Domain**フィールドにルート ドメインを入力し、[**チェック]**をクリックして、各アベイラビリティー ゾーンのブローカー サブドメインを指定します。

7.  **[作成]**をクリックして構成を検証し、プライベートエンドポイントを作成します。

</div>
</SimpleTab>
