---
title: Configure an IP Access List
summary: TiDB Cloud Dedicated クラスターへのアクセスを許可する IP アドレスを構成する方法を学習します。
---

# IPアクセスリストを設定する {#configure-an-ip-access-list}

TiDB Cloud内の各TiDB Cloud Dedicated クラスターに対して、IP アクセスリストを設定して、クラスターへのアクセスを試みるインターネットトラフィックをフィルタリングできます。これは、ファイアウォールのアクセス制御リストと同様に機能します。設定後は、IP アクセスリストに含まれる IP アドレスを持つクライアントとアプリケーションのみがTiDB Cloud Dedicated クラスターに接続できるようになります。

> **注記：**
>
> このドキュメントは[**TiDB Cloud専用**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に適用されます。TiDB **TiDB Cloud Serverless**の IP アクセス リストを構成する手順については、 [パブリックエンドポイント用のTiDB Cloudサーバーレス ファイアウォール ルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

TiDB Cloud Dedicated クラスターの IP アクセス リストを構成するには、次の手順を実行します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織、プロジェクト、クラスターを切り替えることができます。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[ネットワーク] を**クリックします。

3.  **[ネットワーク]**ページで、 **[IP アドレスの追加] を**クリックします。

4.  表示されたダイアログで、次のいずれかのオプションを選択します。

    -   **どこからでもアクセスを許可**：すべてのIPアドレスからのTiDB Cloudへのアクセスを許可します。このオプションはクラスターをインターネットに完全に公開するため、非常に危険です。
    -   **IP アドレスを使用する**(推奨): SQL クライアント経由でTiDB Cloudにアクセスできる IP と CIDR アドレスのリストを追加できます。

5.  **「IPアドレスを使用する」を**選択した場合は、IPアドレスまたはCIDR範囲を、必要に応じて説明とともに追加します。TiDB TiDB Cloud Dedicatedクラスタごとに、最大100個のIPアドレスを追加できます。

6.  変更を保存するには、 **「確認」**をクリックします。
