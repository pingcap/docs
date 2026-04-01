---
title: Connect to TiDB Cloud Starter or Essential via Alibaba Cloud Private Endpoint
summary: Alibaba Cloudのプライベートエンドポイントを介してTiDB Cloudクラスターに接続する方法を学びましょう。
---

# Alibaba Cloudプライベートエンドポイント経由でTiDB Cloud StarterまたはEssentialに接続します。 {#connect-to-tidb-cloud-starter-or-essential-via-alibaba-cloud-private-endpoint}

このチュートリアルでは、Alibaba Cloud のプライベートエンドポイントを介してTiDB Cloud StarterまたはEssentialクラスターに接続する手順を説明します。プライベートエンドポイントを介して接続することで、パブリックインターネットを使用せずに、サービスとTiDB Cloudクラスター間の安全でプライベートな通信が可能になります。

> **ヒント：**
>
> AWS PrivateLink を介してTiDB Cloud StarterまたはEssentialクラスターに接続する方法については、 [AWS PrivateLink経由でTiDB Cloudに接続します。](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

## 制限 {#restrictions}

-   現在、 TiDB Cloud StarterとTiDB Cloud Essentialは、エンドポイントサービスがAWSまたはAlibaba Cloudでホストされている場合に、プライベートエンドポイント接続をサポートしています。サービスが他のクラウドプロバイダーでホストされている場合、プライベートエンドポイントは利用できません。
-   リージョンをまたいだプライベートエンドポイント接続はサポートされていません。

## Alibaba Cloudでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-alibaba-cloud}

プライベートエンドポイント経由でTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタに接続するには、以下の手順に従ってください。

1.  [TiDBクラスタを選択してください](#step-1-choose-a-tidb-cluster)
2.  [Alibaba Cloud上にプライベートエンドポイントを作成する](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3.  [TiDB Cloudでプライベートエンドポイントを認証します。](#step-3-authorize-your-private-endpoint-in-tidb-cloud)
4.  [プライベートエンドポイントを使用してTiDBクラスタに接続します。](#step-4-connect-to-your-tidb-cluster-using-the-private-endpoint)

### ステップ1. TiDBクラスタを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象のTiDB Cloudクラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。
3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。
4.  **サービス名**、**アベイラビリティゾーンID** 、**リージョンID**をメモしておいてください。

### ステップ2. Alibaba Cloud上にプライベートエンドポイントを作成する {#step-2-create-a-private-endpoint-on-alibaba-cloud}

Alibaba Cloud管理コンソールを使用してVPCインターフェースエンドポイントを作成するには、次の手順を実行します。

1.  [Alibaba Cloud管理コンソール](https://account.alibabacloud.com/login/login.htm)にサインインしてください。

2.  **VPC** &gt;**エンドポイント**に移動します。

3.  **「インターフェースエンドポイント」**タブで、 **「エンドポイントの作成」を**クリックします。

4.  エンドポイント情報を入力してください。
    -   **リージョン**： TiDB Cloudクラスターと同じリージョンを選択してください。
    -   **エンドポイント名**：エンドポイントの名前を選択してください。
    -   **エンドポイントタイプ**：**インターフェースエンドポイント**を選択します。
    -   **エンドポイントサービス**： **[その他のエンドポイントサービス]**を選択します。

5.  **「エンドポイントサービス名」**フィールドに、 TiDB Cloudからコピーしたサービス名を貼り付けます。

6.  **「確認」**をクリックしてください。サービスが有効な場合は、緑色のチェックマークが表示されます。

7.  エンドポイントに使用する**VPC** 、**Securityグループ**、および**ゾーン**を選択してください。

8.  エンドポイントを作成するには、 **「OK」**をクリックしてください。

9.  エンドポイントの状態が**アクティブ**になり、接続状態が**接続**済みになるまで待ちます。

### ステップ3. TiDB Cloudでプライベートエンドポイントを認証します {#step-3-authorize-your-private-endpoint-in-tidb-cloud}

Alibaba Cloudでインターフェースエンドポイントを作成したら、それをクラスターの許可リストに追加する必要があります。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象のTiDB Cloud StarterまたはTiDB Cloud Essentialクラスタの名前をクリックして、概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **プライベートエンドポイントの**セクションまでスクロールダウンし、**承認済みネットワークの**表を探してください。

4.  ファイアウォールルールを追加するには、 **「ルールの追加」**をクリックします。

    -   **エンドポイントサービス名**： [ステップ1](#step-1-choose-a-tidb-cluster)で取得したサービス名を貼り付けてください。

    -   **ファイアウォールルール名**：この接続を識別するための名前を入力してください。

    -   **エンドポイント ID** : Alibaba Cloud 管理コンソールから取得した 23 文字のエンドポイント ID ( `ep-`で始まる) を貼り付けてください。

    > **ヒント：**
    >
    > クラウドリージョンからのすべてのプライベートエンドポイント接続を許可するには（テストまたはオープンアクセスのため）、 **[エンドポイントID]**フィールドにアスタリスク ( `*` ) を 1 つ入力します。

5.  **「送信」**をクリックしてください。

### ステップ4. プライベートエンドポイントを使用してTiDBクラスタに接続します。 {#step-4-connect-to-your-tidb-cluster-using-the-private-endpoint}

インターフェースエンドポイントを作成したら、 TiDB Cloudコンソールに戻り、以下の手順を実行してください。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページ目で、対象クラスターの名前をクリックすると、その概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  **「接続タイプ」**ドロップダウンリストで、 **「プライベートエンドポイント」**を選択します。

4.  **「接続**方法」ドロップダウンリストから、希望する接続方法を選択してください。対応する接続​​文字列がダイアログの下部に表示されます。

    ホストについては、Alibaba Cloudの**エンドポイント詳細**ページに移動し、**エンドポイントサービスのドメイン名を**ホストとしてコピーしてください。

5.  接続文字列を使用してクラスターに接続してください。
