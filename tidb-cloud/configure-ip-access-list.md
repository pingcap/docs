---
title: Configure an IP Access List
summary: TiDB Cloud Dedicatedクラスターへのアクセスを許可するIPアドレスを設定する方法を学びましょう。
---

# IPアクセスリストを設定する {#configure-an-ip-access-list}

TiDB Cloudの各TiDB Cloud Dedicatedクラスターに対して、IP アクセス リストを設定することで、クラスターへのアクセスを試みるインターネット トラフィックをフィルタリングできます。これは、ファイアウォールのアクセス コントロール リストと同様の機能を持ちます。設定後、IP アクセス リストに登録されている IP アドレスを持つクライアントおよびアプリケーションのみが、TiDB Cloud Dedicatedクラスターに接続できるようになります。

> **注記：**
>
> このドキュメントは[**TiDB Cloud Dedicated**](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)に適用されます。 **TiDB Cloud Starter**または**TiDB Cloud Essential**の IP アクセス リストを構成する手順については、 [パブリックエンドポイント向けにTiDB Cloud StarterまたはEssential Firewallルールを設定する](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)するを参照してください。

TiDB Cloud Dedicatedクラスターの IP アクセス リストを設定するには、次の手順を実行します。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

    > **ヒント：**
    >
    > 複数の組織に所属している場合は、左上隅のコンボボックスを使用して、まず目的の組織に切り替えてください。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワーク設定**ページで、 **「IPアドレスの追加」**をクリックします。

4.  表示されたダイアログで、以下のいずれかのオプションを選択してください。

    -   **どこからでもアクセスを許可する**：すべてのIPアドレスからTiDB Cloudへのアクセスを許可します。このオプションを選択すると、TiDB Cloud Dedicatedクラスタが完全にインターネットに公開されるため、非常に危険です。
    -   **IPアドレスを使用する**（推奨）：SQLクライアント経由でTiDB Cloudへのアクセスを許可するIPアドレスとCIDRアドレスのリストを追加できます。

5.  **「IPアドレスを使用する」**を選択した場合は、IPアドレスまたはCIDR範囲を追加し、必要に応じて説明を入力してください。TiDB Cloud Dedicatedクラスタごとに、最大100個のIPアドレスを追加できます。

6.  変更を保存するには、 **「確認」**をクリックしてください。
