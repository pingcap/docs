---
title: Configure an IP Access List for TiDB Cloud Premium
summary: TiDB Cloud Premium インスタンスへのアクセスを許可する IP アドレスを構成する方法を学習します。
---

# TiDB Cloud Premium の IP アクセス リストを構成する {#configure-an-ip-access-list-for-tidb-cloud-premium}

TiDB Cloud内の各TiDB Cloud Premium インスタンスに対して、IP アクセスリストを設定して、インスタンスへのアクセスを試みるインターネットトラフィックをフィルタリングできます。これは、ファイアウォールのアクセス制御リストと同様に機能します。設定後は、IP アクセスリストに含まれる IP アドレスを持つクライアントとアプリケーションのみがTiDB Cloud Premium インスタンスに接続できるようになります。

> **注記：**
>
> このドキュメントは**TiDB Cloud Premium**に適用されます。TiDB **TiDB Cloud Starter**または**TiDB Cloud Essential**の IP アクセスリストの設定手順については、 [パブリックエンドポイント用のTiDB Cloud Starter または Essential ファイアウォールルールを構成する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)参照してください。

TiDB Cloud Premium インスタンスの IP アクセス リストを構成するには、次の手順を実行します。

1.  [**TiDBインスタンス**](https://tidbcloud.com/tidbs)ページに移動し、ターゲット インスタンスの名前をクリックして概要ページに移動します。

    > **ヒント：**
    >
    > 左上隅のコンボ ボックスを使用して、組織を切り替えることができます。

2.  左側のナビゲーション ペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **[ネットワーク]**ページで、 **[パブリック エンドポイント**の**有効化]**をクリックして、インスタンスがパブリック エンドポイント経由でアクセスできるようにし、 **[IP アドレスの追加] を**クリックします。

4.  表示されたダイアログで、次のいずれかのオプションを選択します。

    -   **どこからでもアクセスを許可**：すべてのIPアドレスからのTiDB Cloudへのアクセスを許可します。このオプションはインスタンスをインターネットに完全に公開するため、非常に危険です。
    -   **IP アドレスを使用する**(推奨): SQL クライアント経由でTiDB Cloudにアクセスできる IP と CIDR アドレスのリストを追加できます。

5.  **[IP アドレスの使用]**を選択した場合は、オプションの説明とともに IP アドレスまたは CIDR 範囲を追加します。

6.  変更を保存するには、 **「確認」**をクリックします。
