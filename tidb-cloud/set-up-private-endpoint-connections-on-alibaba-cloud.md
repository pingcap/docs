---
title: Connect to TiDB Cloud Starter or Essential via Alibaba Cloud Private Endpoint
summary: Alibaba Cloudのプライベートエンドポイントを介して、TiDB Cloud StarterまたはEssentialインスタンスに接続する方法を学びましょう。
---

# Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します。 {#connect-to-tidb-cloud-starter-or-essential-via-alibaba-cloud-private-endpoint}

このチュートリアルでは、Alibaba Cloud のプライベートエンドポイントを介してTiDB Cloud StarterまたはEssentialインスタンスに接続する手順を説明します。プライベートエンドポイントを介して接続することで、パブリックインターネットを使用せずに、サービスとTiDB Cloud StarterまたはEssentialインスタンス間の安全でプライベートな通信が可能になります。

> **Tip:**
>
> AWS PrivateLink 経由でTiDB Cloud StarterまたはEssentialインスタンスに接続する方法については、 [AWS PrivateLink経由でTiDB Cloudに接続します](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)を参照してください。

## 制限 {#restrictions}

- 現在、 TiDB Cloud StarterとTiDB Cloud Essentialは、エンドポイントサービスがAWSまたはAlibaba Cloudでホストされている場合に、プライベートエンドポイント接続をサポートしています。サービスが他のクラウドプロバイダーでホストされている場合、プライベートエンドポイントは利用できません。
- リージョンをまたいだプライベートエンドポイント接続はサポートされていません。

## Alibaba Cloudでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-alibaba-cloud}

TiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスにプライベートエンドポイント経由で接続するには、以下の手順に従ってください。

1. [TiDB Cloud StarterまたはEssentialインスタンスを選択してください](#step-1-choose-a-tidb-instance)
2. [Alibaba Cloud上にプライベートエンドポイントを作成する](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3. [TiDB Cloudでプライベートエンドポイントを認証する（オプション）](#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional)
4. [プライベートエンドポイントを使用して、 TiDB Cloud StarterまたはEssentialインスタンスに接続します](#step-4-connect-to-your-instance-using-the-private-endpoint)

### ステップ1. TiDB Cloud StarterまたはEssentialインスタンスを選択します {#step-1-choose-a-tidb-instance} {#step-1-choose-a-tidb-instance}

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックすると、その概要ページに移動します。
2. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。
3. **Connection Type**ドロップダウンリストで、 **Private Endpoint**を選択します。
4. **Service Name**、**Availability Zone ID** 、**Region ID**をメモしておいてください。

### ステップ2. Alibaba Cloud上にプライベートエンドポイントを作成する {#step-2-create-a-private-endpoint-on-alibaba-cloud}

Alibaba Cloud管理コンソールを使用してVPCインターフェースエンドポイントを作成するには、次の手順を実行します。

1. [Alibaba Cloud管理コンソール](https://account.alibabacloud.com/login/login.htm)にサインインします。

2. **VPC** &gt;**Endpoints**に移動します。

3. **Interface Endpoints**タブで、 **Create Endpoint**をクリックします。

4. エンドポイント情報を入力してください。
    - **リージョン**： TiDB Cloud StarterまたはEssentialインスタンスと同じリージョンを選択してください。
    - **Endpoint Name**：エンドポイントの名前を選択してください。
    - **Endpoint Type**：**Interface Endpoint**を選択します。
    - **Endpoint Service**： **Other Endpoint Services**を選択します。

5. **Endpoint Service Name**フィールドに、 TiDB Cloudからコピーしたサービス名を貼り付けます。

6. **Verify**をクリックしてください。サービスが有効な場合は、緑色のチェックマークが表示されます。

7. エンドポイントに使用する**VPC** 、**Security Group**、および**Zone**を選択してください。

8. エンドポイントを作成するには、 **OK**をクリックしてください。

9. エンドポイントの状態が**Active**になり、接続状態が**Connected**済みになるまで待ちます。

### ステップ3．TiDB Cloudでプライベートエンドポイントを認証する（オプション） {#step-3-authorize-your-private-endpoint-in-tidb-cloud-optional}

> **Note:**
>
> この手順は任意です。特定のプライベートエンドポイント接続へのアクセスを制限する場合にのみ、**Authorized Networks**を設定する必要があります。ルールが設定されていない場合、すべてのプライベートエンドポイント接続がデフォルトで許可されます。

Alibaba Cloud上にインターフェースエンドポイントを作成した後、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスに対して認証を行い、アクセスを制限できます。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialインスタンスの名前をクリックすると、その概要ページに移動します。

2. 左側のナビゲーションペインで、 **Settings** &gt; **Networking**をクリックします。

3. **Private Endpoint**セクションまでスクロールダウンし、**Authorized Networks**表を探してください。

4. ファイアウォールルールを追加するには、 **Add Rule**をクリックします。

    - **Endpoint Service Name**:[ステップ1](#step-1-choose-a-tidb-instance)から取得したサービス名を貼り付けます。

    - **Firewall Rule Name**：この接続を識別するための名前を入力してください。

    - **Your Endpoint ID** : Alibaba Cloud 管理コンソールから取得した 23 文字のエンドポイント ID ( `ep-`で始まる) を貼り付けてください。

    > **Tip:**
    >
    > - **Authorized Networks**テーブルを空のままにした場合、デフォルトで全てのプライベートエンドポイント接続が許可されます。
    > - クラウドリージョンからのすべてのプライベートエンドポイント接続を許可するには（テストまたはオープンアクセス用）、**Your Endpoint ID**フィールドにアスタリスク1つ（ `*` ）を入力します。

5. **Submit**をクリックしてください。

### ステップ4. プライベートエンドポイントを使用して、 TiDB Cloud StarterまたはEssentialインスタンスに接続します。{#step-4-connect-to-your-instance-using-the-private-endpoint} {#step-4-connect-to-your-instance-using-the-private-endpoint}

インターフェースエンドポイントを作成したら、 TiDB Cloudコンソールに戻り、以下の手順を実行してください。

1. [**My TiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックすると、その概要ページに移動します。

2. 右上隅の**Connect**をクリックしてください。接続ダイアログが表示されます。

3. **Connection Type**ドロップダウンリストで、 **Private Endpoint**を選択します。

4. **Connect With**ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。

    ホストについては、Alibaba Cloudの**Endpoint Details**ページに移動し、**エンドポイントサービスのドメイン名を**ホストとしてコピーしてください。

5. 接続文字列を使用して、 TiDB Cloud StarterまたはEssentialインスタンスに接続します。
