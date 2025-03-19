---
title: Configure an IP Access List
summary: TiDB Cloud Dedicated クラスターへのアクセスを許可する IP アドレスを構成する方法について説明します。
---

# IPアクセスリストを構成する {#configure-an-ip-access-list}

TiDB Cloud内の各TiDB Cloud Dedicated クラスターに対して、クラスターにアクセスしようとするインターネット トラフィックをフィルタリングするための IP アクセス リストを設定できます。これは、ファイアウォールのアクセス制御リストと同様に機能します。設定後は、IP アドレスが IP アクセス リストに含まれているクライアントとアプリケーションのみがTiDB Cloud Dedicated クラスターに接続できます。

> **注記：**
>
> このドキュメントは[**TiDB Cloud専用**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に適用されます。TiDB **TiDB Cloud Serverless**の IP アクセス リストを構成する手順については、 [パブリックエンドポイント用のTiDB Cloudサーバーレス ファイアウォール ルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

IP アクセス リストを設定するには、 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)で次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  左側のナビゲーション ウィンドウで、 **[ネットワーク]**をクリックし、 **[IP アドレスの追加] を**クリックします。

3.  ダイアログで、次のいずれかのオプションを選択します。

    -   **どこからでもアクセスを**許可: すべての IP アドレスがTiDB Cloudにアクセスできるようにします。このオプションはクラスターをインターネットに完全に公開するため、非常に危険です。
    -   **IP アドレスを使用する**(推奨): SQL クライアント経由でTiDB Cloudにアクセスできる IP と CIDR アドレスのリストを追加できます。

4.  **[IP アドレスの使用]**を選択した場合は、オプションの説明とともに IP アドレスまたは CIDR 範囲を追加します。TiDB TiDB Cloud Dedicated クラスターごとに、最大 100 個の IP アドレスを追加できます。

5.  変更を保存するには、 **「確認」**をクリックします。
