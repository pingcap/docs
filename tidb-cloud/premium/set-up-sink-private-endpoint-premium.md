---
title: Set Up Private Endpoint for Changefeeds
summary: 変更フィードのプライベート エンドポイントを設定する方法を学習します。
---

# Changefeeds のプライベート エンドポイントを設定する {#set-up-private-endpoint-for-changefeeds}

このドキュメントでは、TiDB Cloud Premium インスタンスで変更フィード用のプライベート エンドポイントを作成し、プライベート接続を介してセルフホスト型 Kafka または MySQL にデータを安全にストリーミングする方法について説明します。

## 前提条件 {#prerequisites}

-   プライベートエンドポイント作成の権限を確認する
-   ネットワーク接続を設定する

### 権限 {#permissions}

組織内で次のいずれかのロールを持つユーザーのみが、変更フィードのプライベート エンドポイントを作成できます。

-   `Organization Owner`
-   対応するインスタンスの場合は`Instance Manager`

TiDB Cloudのロールの詳細については、 [ユーザーロール](/tidb-cloud/premium/manage-user-access-premium.md#user-roles)参照してください。

### ネットワーク {#network}

プライベート エンドポイントは、クラウド プロバイダーの**Private Link**テクノロジーを活用し、VPC 内のリソースが、あたかもそれらのサービスが VPC 内で直接ホストされているかのように、プライベート IP アドレスを介して他の VPC 内のサービスに接続できるようにします。

<SimpleTab>
<div label="AWS">

changefeed ダウンストリーム サービスが AWS でホストされている場合は、次の情報を収集します。

-   ダウンストリーム サービスのプライベート エンドポイント サービスの名前
-   ダウンストリーム サービスがデプロイされているアベイラビリティ ゾーン (AZ)

ダウンストリーム サービスでプライベート エンドポイント サービスが利用できない場合は、手順[ステップ 2. Kafka クラスターをプライベート リンク サービスとして公開する](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)に従ってロード バランサーとプライベート リンク サービスを設定します。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

changefeed ダウンストリーム サービスが Alibaba Cloud でホストされている場合は、次の情報を収集します。

-   ダウンストリーム サービスのプライベート エンドポイント サービスの名前
-   ダウンストリーム サービスがデプロイされているアベイラビリティ ゾーン (AZ)

TiDB Cloud VPC アクセスを許可するには、TiDB Cloud の Alibaba Cloud アカウント ID をエンドポイント サービスの許可リストに追加する必要があります。

ダウンストリーム サービスでプライベート エンドポイント サービスが利用できない場合は、手順[ステップ 2. Kafka クラスターをプライベート リンク サービスとして公開する](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)に従ってロード バランサーとプライベート リンク サービスを設定します。

</div>
</CustomContent>

</SimpleTab>

## ステップ1. インスタンスのネットワークページを開きます {#step-1-open-the-networking-page-for-your-instance}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページで、ターゲットインスタンスの名前をクリックして、概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織とインスタンスを切り替えることができます。

3.  左側のナビゲーション ペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

## ステップ2. 変更フィードのプライベートエンドポイントを構成する {#step-2-configure-the-private-endpoint-for-changefeeds}

構成手順は、インスタンスがデプロイされているクラウド プロバイダーによって異なります。

<SimpleTab>
<div label="AWS">

1.  **[ネットワーキング]**ページで、 **[Changefeed の AWS プライベートエンドポイント]**セクションの**[プライベートエンドポイントの作成]**をクリックします。

2.  **「Changefeed のプライベート エンドポイントの作成」**ダイアログで、プライベート エンドポイントの名前を入力します。

3.  リマインダーに従って、 TiDB Cloudの[AWS プリンシパル](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts)エンドポイントの作成を承認します。

4.  セクション[ネットワーク](#network)で収集した**エンドポイント サービス名**を入力します。

5.  **AZ の数**を選択します。AZ の数と AZ ID が Kafka のデプロイメントと一致していることを確認してください。

6.  このプライベート エンドポイントが Apache Kafka 用に作成される場合は、 **Kafka のアドバタイズ リスナー**オプションを有効にします。

7.  **TiDB 管理**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka のアドバタイズされたリスナーを構成します。

    -   アドバタイズされたリスナーに**TiDB マネージド**ドメインを使用するには、 **「ドメインパターン」**フィールドに一意の文字列を入力し、 **「生成」**をクリックします。TiDB は、各アベイラビリティゾーンのサブドメインを持つブローカーアドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメイン タイプを**[カスタム]**に切り替え、 **[カスタム ドメイン]**フィールドにルート ドメインを入力し、 **[チェック]**をクリックして、各アベイラビリティー ゾーンのブローカー サブドメインを指定します。

8.  **[作成]**をクリックして構成を検証し、プライベート エンドポイントを作成します。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1.  **「ネットワーク」**ページで、 **「Changefeed 用 Alibaba Cloud プライベート エンドポイント」**セクションの**「プライベート エンドポイントの作成」を**クリックします。

2.  **「Changefeed のプライベート エンドポイントの作成」**ダイアログで、プライベート エンドポイントの名前を入力します。

3.  リマインダーに従って、TiDB Cloud の Alibaba Cloud アカウント ID をエンドポイントサービスの許可リストに追加し、 TiDB Cloud VPC へのアクセスを許可してください。詳細については、 [エンドポイントサービスの許可リスト内のアカウントIDの管理](https://www.alibabacloud.com/help/en/privatelink/user-guide/add-and-manage-service-whitelists)ご覧ください。

4.  セクション[ネットワーク](#network)で収集した**エンドポイント サービス名**を入力します。

5.  **AZ の数**を選択します。AZ の数と AZ ID が Kafka のデプロイメントと一致していることを確認してください。

6.  このプライベート エンドポイントが Apache Kafka 用に作成される場合は、 **Kafka のアドバタイズ リスナー**オプションを有効にします。

7.  **TiDB 管理**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka のアドバタイズされたリスナーを構成します。

    -   アドバタイズされたリスナーに**TiDB マネージド**ドメインを使用するには、 **「ドメインパターン」**フィールドに一意の文字列を入力し、 **「生成」**をクリックします。TiDB は、各アベイラビリティゾーンのサブドメインを持つブローカーアドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメイン タイプを**[カスタム]**に切り替え、 **[カスタム ドメイン]**フィールドにルート ドメインを入力し、 **[チェック]**をクリックして、各アベイラビリティー ゾーンのブローカー サブドメインを指定します。

8.  **[作成]**をクリックして構成を検証し、プライベート エンドポイントを作成します。

</div>
</CustomContent>
</SimpleTab>
