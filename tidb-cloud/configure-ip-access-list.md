---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your TiDB Dedicated cluster.
---

# IPアクセスリストの設定 {#configure-an-ip-access-list}

TiDB TiDB Cloudの TiDB 専用クラスターごとに、クラスターにアクセスしようとするインターネット トラフィックをフィルターする IP アクセス リストを構成できます。これは、ファイアウォールのアクセス コントロール リストと同様に機能します。構成後は、IP アクセス リストに IP アドレスが含まれているクライアントとアプリケーションのみが TiDB 専用クラスターに接続できます。

> **ノート：**
>
> IP アクセス リストの設定は[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB専用</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)クラスタでのみ使用できます。

TiDB 専用クラスターの場合、次のいずれかの方法で IP アクセス リストを構成できます。

-   [<a href="#configure-an-ip-access-list-in-standard-connection">標準接続でのIPアクセスリストの設定</a>](#configure-an-ip-access-list-in-standard-connection)

-   [<a href="#configure-an-ip-access-list-in-security-settings">セキュリティ設定で IP アクセス リストを構成する</a>](#configure-an-ip-access-list-in-security-settings)

## 標準接続でのIPアクセスリストの設定 {#configure-an-ip-access-list-in-standard-connection}

標準接続で TiDB 専用クラスターの IP アクセス リストを構成するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)で、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。
2.  TiDB 専用クラスターの行で**[...]**をクリックし、 **[接続]**を選択します。ダイアログが表示されます。
3.  ダイアログの「**標準接続」**タブで**「ステップ 1: トラフィック フィルタを作成する」**を見つけて、IP アクセス リストを構成します。

    -   クラスターの IP アクセス リストが設定されていない場合は、 **[現在の IP アドレスを追加]**をクリックして現在の IP アドレスを IP アクセス リストに追加し、必要に応じて**[項目の追加]**をクリックして IP アドレスを追加できます。次に、 **「フィルターの更新」**をクリックして構成を保存します。

        > **ノート：**
        >
        > TiDB 専用クラスターごとに、最大 7 つの IP アドレスを IP アクセス リストに追加できます。 IP アドレスを追加するためのクォータを申請するには、 [<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudのサポート</a>](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    -   クラスターの IP アクセス リストが設定されている場合は、 **[編集]**をクリックして IP アドレスを追加、編集、または削除し、 **[フィルターの更新]**をクリックして構成を保存します。

    -   任意の IP アドレスがクラスターにアクセスできるようにするには (非推奨)、[**どこからでもアクセスを許可する]**をクリックし、 **[フィルターの更新]**をクリックします。セキュリティのベスト プラクティスによれば、任意の IP アドレスによるクラスターへのアクセスを許可することはお勧めできません。これは、クラスターが完全にインターネットに公開されることになり、非常に危険です。

## セキュリティ設定で IP アクセス リストを構成する {#configure-an-ip-access-list-in-security-settings}

セキュリティ設定で TiDB 専用クラスターの IP アクセス リストを構成するには、次の手順を実行します。

1.  [<a href="https://tidbcloud.com/">TiDB Cloudコンソール</a>](https://tidbcloud.com/)で、プロジェクトの[<a href="https://tidbcloud.com/console/clusters">**クラスター**</a>](https://tidbcloud.com/console/clusters)ページに移動します。

2.  TiDB 専用クラスターの行で**[...]**をクリックし、 **[Security設定]**を選択します。セキュリティ設定ダイアログが表示されます。

3.  ダイアログで、次のように IP アクセス リストを設定します。

    -   現在の IP アドレスを IP アクセス リストに追加するには、 **[現在の IP アドレスを追加]**をクリックします。

    -   IP アドレスを IP アクセス リストに追加するには、IP アドレスと説明を入力し、 **[Add to IP List]**をクリックします。

        > **ノート：**
        >
        > TiDB 専用クラスターごとに、最大 7 つの IP アドレスを IP アクセス リストに追加できます。 IP アドレスを追加するためのクォータを申請するには、 [<a href="/tidb-cloud/tidb-cloud-support.md">TiDB Cloudのサポート</a>](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    -   任意の IP アドレスがクラスターにアクセスできるようにするには (推奨されません)、 **「どこからでもアクセスを許可する」**をクリックします。セキュリティのベスト プラクティスによれば、任意の IP アドレスによるクラスターへのアクセスを許可することはお勧めできません。これは、クラスターが完全にインターネットに公開されることになり、非常に危険です。

    -   アクセス リストから IP アドレスを削除するには、IP アドレスの行にある**[削除]**をクリックします。

4.  **「適用」**をクリックして構成を保存します。
