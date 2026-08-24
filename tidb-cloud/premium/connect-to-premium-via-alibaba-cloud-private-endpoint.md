---
title: Connect to TiDB Cloud Premium via Alibaba Cloud Private Endpoint
summary: Alibaba Cloud上のプライベートエンドポイントを介してTiDB Cloud Premiumインスタンスに接続する方法を学びましょう。
---

# Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud Premiumに接続します {#connect-to-tidb-cloud-premium-via-alibaba-cloud-private-endpoint}

このドキュメントでは、Alibaba Cloud のプライベートエンドポイントを介してTiDB Cloud Premium インスタンスに接続する方法について説明します。プライベートエンドポイントを介して接続することで、パブリックインターネットを使用せずに、サービスとTiDB Cloud Premium インスタンス間の安全かつプライベートな通信が可能になります。

> **Tip:**
>
> AWS PrivateLink 経由でTiDB Cloud Premium インスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

## 制限 {#restrictions}

-   現在、TiDB Premiumは、エンドポイントサービスがAWSまたはAlibaba Cloudでホストされている場合に限り、プライベートエンドポイント接続をサポートしています。サービスが他のクラウドプロバイダーでホストされている場合、プライベートエンドポイントは利用できません。
-   リージョンをまたぐプライベートエンドポイント接続はサポートされていません。

## Alibaba Cloudでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-alibaba-cloud}

プライベートエンドポイント経由でPremiumインスタンスに接続するには、以下の手順を実行してください。

### ステップ1. TiDB Cloud Premiumインスタンスを選択します。 {#step-1-choose-a-tidb-cloud-premium-instance}

1.  [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Premiumインスタンスの名前をクリックすると、その概要ページに移動します。
2.  右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。
3.  **Connection Type**ドロップダウンリストで、 **Private Endpoint**を選択します。
4.  **Service Name**、**Availability Zone ID** 、**Region ID**をメモしておいてください。

### ステップ2. Alibaba Cloud上にプライベートエンドポイントを作成する {#step-2-create-a-private-endpoint-on-alibaba-cloud}

Alibaba Cloud管理コンソールを使用してVPCインターフェースエンドポイントを作成するには、次の手順を実行します。

1.  [Alibaba Cloud管理コンソール](https://account.alibabacloud.com/login/login.htm)にサインインします。
2.  **VPC** &gt;**Endpoints**に移動します。
3.  **Interface Endpoints**タブをクリックし、 **Create Endpoint**をクリックします。
4.  エンドポイントの詳細を入力してください。
    -   **リージョン**： TiDB Cloud Premiumインスタンスと同じリージョンを選択してください。
    -   **Endpoint Name**：エンドポイントの名前を入力してください。
    -   **Endpoint Type**：**Interface Endpoint**を選択してください。
    -   **Endpoint Service**： **[その他のエンドポイントサービス]**を選択します。
5.  **Endpoint Service Name**フィールドに、 TiDB Cloudからコピーしたサービス名を貼り付けます。
6.  **Verify**をクリックしてください。緑色のチェックマークが表示されれば、サービスが有効であることを示します。
7.  エンドポイントに関連付ける**VPC** 、**Security Group**、および**ゾーン**を選択してください。
8.  エンドポイントを作成するには、 **OK**をクリックしてください。
9.  エンドポイントの状態が**Active**になり、接続の状態が**Connected**になるまで待ちます。

インターフェースエンドポイントを作成したら、**EndPoints**ページに移動し、新しく作成したエンドポイントを選択します。

-   **Basic Information**セクションで、**Endpoint ID**をコピーしてください。この値は後で*エンドポイントリソースID*として使用します。

-   **Domain name of Endpoint Service**セクションで、 **Default Domain Name**をコピーしてください。この値は後で*ドメイン名*として使用します。

    ![AliCloud private endpoint Information](/media/tidb-cloud/private-endpoint/alicloud-private-endpoint-info.png)

### ステップ3. エンドポイントを受け入れ、エンドポイント接続を作成します。 {#step-3-accept-the-endpoint-and-create-the-endpoint-connection}

1.  TiDB Cloudコンソールの**Create Alibaba Cloud Private Endpoint Connection**ダイアログに戻ります。

2.  先ほどコピーした*エンドポイントリソースID*と*ドメイン名*を、それぞれのフィールドに貼り付けてください。

3.  プライベートエンドポイントからの接続を受け入れるには、 **Create Private Endpoint Connection**をクリックしてください。

### ステップ4. TiDB Cloud Premiumインスタンスに接続します {#step-4-connect-to-your-tidb-cloud-premium-instance}

エンドポイント接続を承認すると、接続ダイアログにリダイレクトされます。

1.  プライベートエンドポイントの接続ステータスが**Active**になるまでお待ちください（約5分）。ステータスを確認するには、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックして、 **Networking**ページに移動してください。

2.  **Connect With**ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。

3.  接続文字列を使用してインスタンスに接続してください。

## プライベートエンドポイントの状態参照 {#private-endpoint-status-reference}

プライベートエンドポイントまたはプライベートエンドポイントサービスのステータスを表示するには、左側のナビゲーションペインで**Settings** &gt; **Networking**をクリックして、 **Networking**ページに移動します。

プライベートエンドポイントの可能なステータスは、以下のように説明されます。

-   **Pending**：処理待ち。
-   **Active**：プライベートエンドポイントは使用可能です。
-   **Deleting**：プライベートエンドポイントが削除されています。
-   **Failed**：プライベートエンドポイントの作成に失敗しました。プライベートエンドポイントを削除して、新しいものを作成してください。

プライベートエンドポイントサービスの可能なステータスは、以下のように説明されます。

-   **Creating**：エンドポイントサービスが作成されています。これには3～5分かかります。
-   **Active**：プライベートエンドポイントが作成されるかどうかに関わらず、エンドポイントサービスが作成されます。
