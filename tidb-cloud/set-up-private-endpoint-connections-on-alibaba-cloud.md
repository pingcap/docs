---
title: Connect to TiDB Cloud Starter or Essential via Alibaba Cloud Private Endpoint
summary: Alibaba Cloud プライベート エンドポイント経由でTiDB Cloudクラスターに接続する方法を学習します。
---

# Alibaba Cloud プライベートエンドポイント経由でTiDB Cloud Starter または Essential に接続します {#connect-to-tidb-cloud-starter-or-essential-via-alibaba-cloud-private-endpoint}

このチュートリアルでは、Alibaba Cloud 上のプライベートエンドポイントを介してTiDB Cloud Starter または Essential クラスターに接続する手順を詳しく説明します。プライベートエンドポイントを介して接続することで、パブリックインターネットを利用せずに、サービスとTiDB Cloudクラスター間の安全かつプライベートな通信が可能になります。

> **ヒント：**
>
> AWS PrivateLink 経由でTiDB Cloud Starter または Essential クラスターに接続する方法については、 [AWS PrivateLink 経由でTiDB Cloudに接続する](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)参照してください。

## 制限 {#restrictions}

-   現在、 TiDB Cloud StarterおよびTiDB Cloud Essentialは、エンドポイントサービスがAWSまたはAlibaba Cloudでホストされている場合にプライベートエンドポイント接続をサポートしています。サービスが他のクラウドプロバイダーでホストされている場合、プライベートエンドポイントは適用されません。
-   リージョン間のプライベート エンドポイント接続はサポートされていません。

## Alibaba Cloudでプライベートエンドポイントを設定する {#set-up-a-private-endpoint-with-alibaba-cloud}

プライベート エンドポイント経由でTiDB Cloud Starter またはTiDB Cloud Essential クラスターに接続するには、次の手順に従います。

1.  [TiDBクラスタを選択する](#step-1-choose-a-tidb-cluster)
2.  [Alibaba Cloud にプライベートエンドポイントを作成する](#step-2-create-a-private-endpoint-on-alibaba-cloud)
3.  [プライベートエンドポイントを使用して TiDB クラスターに接続する](#step-3-connect-to-your-tidb-cluster-using-the-private-endpoint)

### ステップ1. TiDBクラスターを選択する {#step-1-choose-a-tidb-cluster}

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲットのTiDB Cloudクラスターの名前をクリックして、概要ページに移動します。
2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。
3.  **[接続タイプ]**ドロップダウン リストで、 **[プライベート エンドポイント]**を選択します。
4.  **サービス名**、**アベイラビリティーゾーン ID** 、**リージョンID**をメモします。

### ステップ2. Alibaba Cloudにプライベートエンドポイントを作成する {#step-2-create-a-private-endpoint-on-alibaba-cloud}

Alibaba Cloud 管理コンソールを使用して VPC インターフェイス エンドポイントを作成するには、次の手順を実行します。

1.  [Alibaba Cloud 管理コンソール](https://account.alibabacloud.com/login/login.htm)にサインインします。

2.  **VPC** &gt;**エンドポイント**に移動します。

3.  **[インターフェイス エンドポイント]**タブで、 **[エンドポイントの作成] を**クリックします。

4.  エンドポイント情報を入力します。
    -   **リージョン**: TiDB Cloudクラスターと同じリージョンを選択します。
    -   **エンドポイント名**: エンドポイントの名前を選択します。
    -   **エンドポイント タイプ**:**インターフェイス エンドポイント**を選択します。
    -   **エンドポイント サービス**: **[その他のエンドポイント サービス]**を選択します。

5.  **「エンドポイント サービス名」**フィールドに、 TiDB Cloudからコピーしたサービス名を貼り付けます。

6.  **「確認」**をクリックします。サービスが有効な場合は緑色のチェックマークが表示されます。

7.  エンドポイントに使用する**VPC** 、**Securityグループ**、**ゾーン**を選択します。

8.  **[OK]**をクリックしてエンドポイントを作成します。

9.  エンドポイントのステータスが**Active**になり、接続ステータスが**Connected**になるまで待ちます。

### ステップ3: プライベートエンドポイントを使用してTiDBクラスターに接続する {#step-3-connect-to-your-tidb-cluster-using-the-private-endpoint}

インターフェース エンドポイントを作成したら、 TiDB Cloudコンソールに戻り、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲット クラスターの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **[接続タイプ]**ドロップダウン リストで、 **[プライベート エンドポイント]**を選択します。

4.  **「接続**方法」ドロップダウンリストで、希望する接続方法を選択します。対応する接続文字列がダイアログの下部に表示されます。

    ホストについては、Alibaba Cloud の**エンドポイントの詳細**ページに移動し、**エンドポイント サービスのドメイン名を**ホストとしてコピーします。

5.  接続文字列を使用してクラスターに接続します。
