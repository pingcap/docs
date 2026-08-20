---
title: Set Up Private Endpoint for Changefeeds
summary: 変更フィード用のプライベートエンドポイントを設定する方法を学びましょう。
---

# Changefeeds用のプライベートエンドポイントを設定する {#set-up-private-endpoint-for-changefeeds}

このドキュメントでは、TiDB Cloud Premiumインスタンスで変更フィード用のプライベートエンドポイントを作成する方法について説明します。これにより、プライベート接続を介して、自己ホスト型のKafka、Amazon MSK Provisionedクラスター、またはMySQLにデータを安全にストリーミングできるようになります。

## 前提条件 {#prerequisites}

-   プライベートエンドポイント作成の権限を確認してください
-   ネットワーク接続を設定する

### 権限 {#permissions}

変更フィード用のプライベートエンドポイントを作成できるのは、組織内で以下のいずれか1つの役割を持つユーザーのみです。

-   `Organization Owner`
-   対応するインスタンスの`Instance Manager`

TiDB Cloudのロールの詳細については、 [ユーザーロール](/tidb-cloud/manage-user-access.md#user-roles)を参照してください。

### ネットワーク {#network}

プライベートエンドポイントは、クラウドプロバイダーの**Private Link**技術を活用し、VPC内のリソースがプライベートIPアドレスを介して他のVPC内のサービスに接続できるようにします。これにより、あたかもそれらのサービスがVPC内で直接ホストされているかのように動作します。

<SimpleTab>
<div label="AWS">

変更フィードのダウンストリームサービスがAWS上でホストされている場合は、接続タイプに応じて以下の情報を収集してください。

-   **AWS Endpoint Service**: ダウンストリームサービスのエンドポイントサービス名と、ダウンストリームサービスがデプロイされている可用性ゾーン（AZ）。

    ダウンストリーム サービスでプライベート エンドポイント サービスを利用できない場合は、 [ステップ2. Kafkaクラスタをプライベートリンクサービスとして公開する](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)プライベートリンクサービスとして公開することで、ロードバランサーとプライベートリンクサービスを設定します。

-   **Amazon MSK Provisioned**: Amazon MSK ProvisionedクラスターのARN。変更フィード用のAmazon MSK Provisionedクラスターの作成方法については、[AWS PrivateLink 経由で Amazon MSK Provisioned クラスターを設定する](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md)を参照してください。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

変更フィードのダウンストリームサービスがAlibaba Cloudでホストされている場合は、以下の情報を収集してください。

-   ダウンストリームサービスのプライベートエンドポイントサービスの名前
-   ダウンストリームサービスがデプロイされている可用性ゾーン（AZ）

TiDB Cloud VPCへのアクセスを許可するには、エンドポイントサービスの許可リストにTiDB CloudのAlibaba CloudアカウントIDを追加する必要があります。

ダウンストリーム サービスでプライベート エンドポイント サービスを利用できない場合は、 [ステップ2. Kafkaクラスタをプライベートリンクサービスとして公開する](/tidb-cloud/setup-aws-self-hosted-kafka-private-link-service.md#step-2-expose-the-kafka-cluster-as-private-link-service)プライベートリンクサービスとして公開することで、ロードバランサーとプライベートリンクサービスをセットアップします。

</div>
</CustomContent>

</SimpleTab>

## ステップ1. インスタンスのネットワークページを開きます。 {#step-1-open-the-networking-page-for-your-instance}

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)にログインします。

2.  [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Premiumインスタンスの名前をクリックすると、その概要ページに移動します。

    > **Tip:**
    >
    > 左上隅にあるコンボボックスを使用して、組織とインスタンスを切り替えることができます。

3.  左側のナビゲーションペインで、 **[設定]** > **[ネットワーク]**をクリックします。

## ステップ2．変更フィード用のプライベートエンドポイントを設定する {#step-2-configure-the-private-endpoint-for-changefeeds}

設定手順は、インスタンスがデプロイされているクラウドプロバイダーによって異なります。

<SimpleTab>
<div label="AWS">

AWS では、ダウンストリームサービスに応じて接続タイプを選択します。

- ダウンストリームサービスが自己ホスト型KafkaやMySQLなどのAWSエンドポイントサービスを通じて公開されている場合は、**AWS Endpoint Service**を選択します。
- ダウンストリームサービスがAmazon MSK Provisionedクラスターである場合は、**Amazon MSK Provisioned**を選択します。

**AWS Endpoint Service**

1.  **ネットワーク**ページで、 **「AWS External Services 用プライベートエンドポイント」**セクションの**「External Services 用プライベートエンドポイントの作成」**をクリックします。

2.  表示されたダイアログで、プライベートエンドポイントの名前を入力します。

3.  リマインダーに従って、 TiDB Cloudの[AWSプリンシパル](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-accounts)にエンドポイントを作成する権限を与えます。

4.  [ネットワーク](#network)セクションで収集した**Endpoint Service Name**を入力し、接続タイプとして**AWS Endpoint Service**を選択します。

5.  **Number of AZs**を選択してください。AZの数とAZ IDが、Kafkaのデプロイメントと一致していることを確認してください。

6.  このプライベートエンドポイントがApache Kafka用に作成された場合は、 **「Kafka 用のアドバタイズドリスナーを設定する」**チェックボックスを選択します。

7.  **TiDB Managed**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka用のアドバタイズドリスナーを設定します。

    -   アドバタイズされたリスナーに**TiDB Managed**ドメインを使用するには、 **Domain Pattern**フィールドに一意の文字列を入力し、 **[生成]**をクリックします。TiDB Cloud は、各アベイラビリティ ゾーンごとにサブドメインを含むブローカー アドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメインタイプを**「カスタム」**に切り替え、**Custom Domain**フィールドにルートドメインを入力し、 **「チェック」**をクリックしてから、各アベイラビリティゾーンのブローカーサブドメインを指定します。

8.  **「作成」**をクリックして設定を検証し、プライベートエンドポイントを作成します。

**Amazon MSK Provisioned**

1.  **ネットワーク**ページで、 **「AWS External Services 用プライベートエンドポイント」**セクションの**「External Services 用プライベートエンドポイントの作成」**をクリックします。

2.  表示されたダイアログで、プライベートエンドポイントの名前を入力し、接続タイプとして**AWS MSK Provisioned**を選択します。

3.  Amazon MSK Provisionedクラスターの**MSK Cluster ARN**を入力します。変更フィード用のAmazon MSK Provisionedクラスターの作成方法については、[AWS PrivateLink 経由で Amazon MSK Provisioned クラスターを設定する](/tidb-cloud/setup-aws-msk-provisioned-private-link-service.md)を参照してください。

4.  **「作成」**をクリックして設定を検証し、プライベートエンドポイントを作成します。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud">

1.  **ネットワーク**ページで、 **「Alibaba Cloud External Services 用プライベートエンドポイント」**セクションの**「External Services 用プライベートエンドポイントの作成」**をクリックします。

2.  **「External Services のプライベートエンドポイントの作成」**ダイアログで、プライベートエンドポイントの名前を入力します。

3.  リマインダーに従って、TiDB Cloud の Alibaba Cloud アカウント ID をエンドポイント サービスのホワイトリストに追加して、 TiDB Cloud VPC アクセスを許可します。詳細については、 [エンドポイントサービスの許可リストにおけるアカウントIDの管理](https://www.alibabacloud.com/help/en/privatelink/user-guide/add-and-manage-service-whitelists)を参照してください。

4.  [ネットワーク](#network)セクションで収集した**Endpoint Service Name**を入力します。

5.  **Number of AZs**を選択してください。AZの数とAZ IDが、Kafkaのデプロイメントと一致していることを確認してください。

6.  このプライベートエンドポイントがApache Kafka用に作成された場合は、 **「Kafka 用のアドバタイズドリスナーを設定する」**チェックボックスを選択します。

7.  **TiDB Managed**ドメインまたは**カスタム**ドメインのいずれかを使用して、Kafka用のアドバタイズドリスナーを設定します。

    -   アドバタイズされたリスナーに**TiDB Managed**ドメインを使用するには、 **Domain Pattern**フィールドに一意の文字列を入力し、 **[生成]**をクリックします。TiDB は、各アベイラビリティ ゾーンごとにサブドメインを含むブローカー アドレスを生成します。
    -   アドバタイズされたリスナーに独自の**カスタム**ドメインを使用するには、ドメインタイプを**「カスタム」**に切り替え、**Custom Domain**フィールドにルートドメインを入力し、 **「チェック」**をクリックしてから、各アベイラビリティゾーンのブローカーサブドメインを指定します。

8.  **「作成」**をクリックして設定を検証し、プライベートエンドポイントを作成します。

</div>
</CustomContent>
</SimpleTab>
