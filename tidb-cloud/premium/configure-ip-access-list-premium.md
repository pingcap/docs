---
title: Configure an IP Access List for TiDB Cloud Premium
summary: TiDB Cloud Premiumインスタンスへのアクセスを許可するIPアドレスを設定する方法を学びましょう。
---

# TiDB Cloud Premium の IP アクセス リストを設定します {#configure-an-ip-access-list-for-tidb-cloud-premium}

TiDB Cloudの各TiDB Cloud Premium インスタンスに対して、IP アクセス リストを設定することで、インスタンスへのアクセスを試みるインターネット トラフィックをフィルタリングできます。これはファイアウォールのアクセス制御リストと同様の機能を持ちます。設定後、IP アクセス リストに登録されている IP アドレスを持つクライアントおよびアプリケーションのみが、 TiDB Cloud Premium インスタンスに接続できるようになります。

> **注記：**
>
> このドキュメントは**TiDB Cloud Premium**に適用されます。 **TiDB Cloud Starter**または**TiDB Cloud Essential**の IP アクセス リストを構成する手順については、 [パブリックエンドポイント向けにTiDB Cloud StarterまたはEssential Firewallルールを設定する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)するを参照してください。

TiDB Cloud PremiumインスタンスのIPアクセスリストを設定するには、以下の手順に従ってください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックして、インスタンスがパブリックエンドポイント経由でアクセスできるようにし、 **[IP アドレスを追加] を**クリックします。

4.  表示されたダイアログで、以下のいずれかのオプションを選択してください。

    -   **どこからでもアクセスを許可する**：すべてのIPアドレスからTiDB Cloudへのアクセスを許可します。このオプションを選択すると、インスタンスがインターネットに完全に公開されるため、非常に危険です。
    -   **IPアドレスを使用する**（推奨）：SQLクライアント経由でTiDB Cloudへのアクセスを許可するIPアドレスとCIDRアドレスのリストを追加できます。

5.  **「IPアドレスを使用する」**を選択した場合は、IPアドレスまたはCIDR範囲を追加し、必要に応じて説明を追加してください。

6.  変更を保存するには、 **「確認」**をクリックしてください。
