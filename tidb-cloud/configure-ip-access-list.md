---
title: Configure an IP Access List
summary: Learn how to configure IP addresses that are allowed to access your Dedicated Tier cluster.
---

# IP アクセス リストの構成 {#configure-an-ip-access-list}

TiDB CloudのDedicated Tierクラスターごとに、IP アクセス リストを構成して、クラスターにアクセスしようとするインターネット トラフィックをフィルター処理できます。これは、ファイアウォール アクセス制御リストと同様に機能します。構成後は、IP アクセス リストに IP アドレスが含まれているクライアントとアプリケーションのみがDedicated Tierクラスターに接続できます。

> **ノート：**
>
> IP アクセス リストの設定は、 [Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)クラスタでのみ使用できます。

Dedicated Tierクラスターの場合、次のいずれかの方法で IP アクセス リストを構成できます。

-   [標準接続で IP アクセス リストを構成する](#configure-an-ip-access-list-in-standard-connection)

-   [セキュリティ設定で IP アクセス リストを構成する](#configure-an-ip-access-list-in-security-settings)

## 標準接続で IP アクセス リストを構成する {#configure-an-ip-access-list-in-standard-connection}

標準接続でDedicated Tierクラスターの IP アクセス リストを構成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。
2.  Dedicated Tierクラスターの行で、 **[...]**をクリックして<strong>[接続]</strong>を選択します。ダイアログが表示されます。
3.  ダイアログで、 **[標準接続]**タブの<strong>[ステップ 1: トラフィック フィルターの作成]</strong>を見つけて、IP アクセス リストを構成します。

    -   クラスターの IP アクセス リストが設定されていない場合は、 **[現在の IP アドレスを追加]**をクリックして現在の IP アドレスを IP アクセス リストに追加し、必要に応じて<strong>[項目を追加]</strong>をクリックしてさらに IP アドレスを追加します。次に、 <strong>[フィルターの更新]</strong>をクリックして構成を保存します。

        > **ノート：**
        >
        > Dedicated Tierクラスターごとに、最大 7 つの IP アドレスを IP アクセス リストに追加できます。 IP アドレスを追加するためのクォータを申請するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    -   クラスターの IP アクセス リストが設定されている場合は、 **[編集]**をクリックして IP アドレスを追加、編集、または削除し、 <strong>[フィルターの更新]</strong>をクリックして構成を保存します。

    -   任意の IP アドレスがクラスターにアクセスできるようにするには (推奨されません)、[**どこからでもアクセスを許可する]**をクリックし、 <strong>[フィルターの更新]</strong>をクリックします。セキュリティのベスト プラクティスによると、任意の IP アドレスにクラスターへのアクセスを許可することはお勧めしません。これは、クラスターがインターネットに完全に公開されてしまうため、非常に危険です。

## セキュリティ設定で IP アクセス リストを構成する {#configure-an-ip-access-list-in-security-settings}

セキュリティ設定でDedicated Tierクラスターの IP アクセス リストを構成するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/console/clusters)ページに移動します。

2.  Dedicated Tierクラスターの行で、 **[...]**をクリックして<strong>[Security Settings]</strong>を選択します。セキュリティ設定ダイアログが表示されます。

3.  ダイアログで、次のように IP アクセス リストを構成します。

    -   現在の IP アドレスを IP アクセス リストに追加するには、 **[現在の IP アドレスを追加]**をクリックします。

    -   IP アクセス リストに IP アドレスを追加するには、IP アドレスと説明を入力し、 **[Add to IP List]**をクリックします。

        > **ノート：**
        >
        > Dedicated Tierクラスターごとに、最大 7 つの IP アドレスを IP アクセス リストに追加できます。 IP アドレスを追加するためのクォータを申請するには、 [TiDB Cloudのサポート](/tidb-cloud/tidb-cloud-support.md)にお問い合わせください。

    -   任意の IP アドレスがクラスターにアクセスできるようにするには (推奨されません)、 **[どこからでもアクセスを許可する]**をクリックします。セキュリティのベスト プラクティスによると、任意の IP アドレスにクラスターへのアクセスを許可することはお勧めしません。これは、クラスターがインターネットに完全に公開されてしまうため、非常に危険です。

    -   アクセス リストから IP アドレスを削除するには、IP アドレスの行で**[削除]**をクリックします。

4.  **[適用]**をクリックして構成を保存します。
