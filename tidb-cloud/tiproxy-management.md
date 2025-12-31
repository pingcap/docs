---
title: Manage TiProxy
summary: TiProxy を有効化、無効化、表示、および変更する方法について説明します。
---

# TiProxyを管理する {#manage-tiproxy}

このドキュメントでは、TiProxy を有効化、無効化、表示、および変更する方法について説明します。

> **注記：**
>
> TiProxy はベータ版であり、現在は AWS にデプロイされたTiDB Cloud Dedicated クラスターでのみ利用できます。

## TiProxyを有効にする {#enable-tiproxy}

任意の TiDB ノード グループ内の新しいクラスターまたは既存のクラスターに対して TiProxy を有効にできます。

### TiProxyノードのサイズと数を決定する {#decide-the-size-and-number-of-tiproxy-nodes}

TiProxyノードのサイズと数は、クラスターのQPSとネットワーク帯域幅の両方に依存します。ネットワーク帯域幅は、クライアントリクエストとTiDBレスポンスの帯域幅の合計です。

次の表は、各 TiProxy サイズの最大 QPS とネットワーク帯域幅を示しています。

| サイズ | 最大QPS | 最大ネットワーク帯域幅 |
| :-- | :---- | :---------- |
| 小さい | 3万    | 93 MiB/秒    |
| 大きい | 12万   | 312 MiB/秒   |

利用可能な TiProxy のサイズは`Small`と`Large`です。利用可能な TiProxy ノード番号は 2、3、6、9、12、15、18、21、24 です。デフォルトの 2 つの小型 TiProxy ノードは、60K QPS と 186 MiB/s のネットワーク帯域幅を提供できます。高レイテンシーを防ぐため、QPS 容量の 20% を予約することをお勧めします。

例えば、クラスターの最大QPSが100Kで、最大ネットワーク帯域幅が100MiB/sの場合、TiProxyノードのサイズと数は主にQPSによって決まります。この場合、6つの小型TiProxyノードを選択できます。

### 新しいクラスタで TiProxy を有効にする {#enable-tiproxy-for-a-new-cluster}

新しいクラスターを作成するときに TiProxy を有効にするには、TiProxy トグルをクリックし、TiProxy のサイズと数を選択します。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 既存のクラスターで TiProxy を有効にする {#enable-tiproxy-for-an-existing-cluster}

> **注記：**
>
> TiProxy を有効にすると、対応する TiDB ノードグループ内の TiDB ノードがローリング再起動されます。この再起動中は既存の接続が切断されます。また、新しい接続の作成時に最大 30 秒間ハングする可能性があります。メンテナンスウィンドウで TiProxy を有効にしてください。

既存のクラスターに対して TiProxy を有効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「...」**をクリックし、ドロップダウンメニューの**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  **[クラスタの変更]**ページで、TiProxy トグルをクリックし、TiProxy のサイズと数を選択します。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 制限と割り当て {#limitations-and-quotas}

-   TiDB ノード グループには少なくとも 2 つの TiDB ノードが必要です。
-   TiDB ノードのサイズは少なくとも 4 vCPU である必要があります。
-   組織内の TiProxy ノードのデフォルトの最大数は`10`です。詳細については、 [制限と割り当て](/tidb-cloud/limitations-and-quotas.md)参照してください。
-   TiDB クラスターのバージョンは v6.5.0 以降である必要があります。

## TiProxyを無効にする {#disable-tiproxy}

> **注記：**
>
> TiProxyを無効にすると、接続が切断されます。また、新しい接続の作成時に最大10秒間ハングする可能性があります。メンテナンスウィンドウでTiProxyを必ず無効にしてください。

TiProxy を無効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「...」**をクリックし、ドロップダウンメニューの**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  **[クラスタの変更]**ページで、TiProxy トグルをクリックして TiProxy を無効にします。

![Disable TiProxy](/media/tidb-cloud/tiproxy-disable-tiproxy.png)

## TiProxy をビュー {#view-tiproxy}

### TiProxyトポロジをビュー {#view-tiproxy-topology}

TiProxy トポロジを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  左側のナビゲーションペインで、 **「監視」&gt;「ノード」**をクリックします。「**ノードマップ」**ページが表示されます。
3.  **ノード マップ**ページで、TiProxy トポロジが**TiDB**ペインに表示されます。

![TiProxy Topology](/media/tidb-cloud/tiproxy-topology.png)

### TiProxy メトリックをビュー {#view-tiproxy-metrics}

TiProxy メトリックを表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  左側のナビゲーションペインで、 **「監視」&gt;「メトリック」**をクリックします。「**メトリック」**ページが表示されます。
3.  **「メトリクス」**ページで**「サーバー」**をクリックし、TiProxy関連のメトリクスまでスクロールダウンします。特定のTiDBノードグループのTiProxyメトリクスを表示するには、 **「TiDBノードグループビュー」**をクリックし、TiDBノードグループを選択して、TiProxy関連のメトリクスまでスクロールダウンします。

指標には次のものが含まれます。

-   **TiProxy CPU 使用率**: 各 TiProxy ノードの CPU 使用率の統計情報です。上限は 100% です。最大 CPU 使用率が 80% を超える場合は、TiProxy をスケールアウトすることをお勧めします。
-   **TiProxy 接続**: 各 TiProxy ノード上の接続の数。
-   **TiProxyスループット**：各TiProxyノードにおける1秒あたりの転送バイト数。最大スループットが最大ネットワーク帯域幅に達する場合は、TiProxyをスケールアウトすることをお勧めします。最大ネットワーク帯域幅の詳細については、 [TiProxyノードのサイズと数を決定する](#decide-the-size-and-number-of-tiproxy-nodes)参照してください。
-   **TiProxyセッション移行理由**：1分ごとに発生するセッション移行の数とその理由。例えば、TiDBがスケールインし、TiProxyがセッションを他のTiDBノードに移行する場合、理由は`status`です。その他の移行理由については、 [TiProxy 監視メトリクス](https://docs.pingcap.com/tidb/stable/tiproxy-grafana#balance)参照してください。

### TiProxyの請求書をビュー {#view-tiproxy-bills}

TiProxy の請求書を表示するには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)で、左上隅のコンボ ボックスを使用して対象の組織に切り替えます。
2.  左側のナビゲーション ペインで、 **[請求]**をクリックします。 **[請求]**ページには、デフォルトで [**請求書]**タブが表示されます。
3.  **「サービス別概要**」セクションでは、TiProxy ノード コストが**TiDB Dedicated の**下に表示されますが、TiProxy データ転送コストは**Data Transfer &gt; Same リージョン**に含まれています。

![TiProxy Billing](/media/tidb-cloud/tiproxy-billing.png)

## TiProxyを変更する {#modify-tiproxy}

> **注記**
>
> -   TiProxy のサイズを直接変更することはサポートされていません。代わりに、TiProxy ノードの数を変更することをお勧めします。TiProxy のサイズを変更する必要がある場合は、すべての TiDB ノードグループで TiProxy を無効にし、その後再度有効にして、異なるサイズを選択する必要があります。
> -   TiProxy をスケールインすると接続が切断されます。メンテナンス期間中に TiProxy をスケールインしてください。

TiProxy をスケールインまたはスケールアウトするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、プロジェクトの[**クラスター**](https://tidbcloud.com/project/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。
2.  右上隅の**「...」**をクリックし、ドロップダウンメニューの**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  **「クラスタの変更」**ページで、TiProxy ノードの数を変更します。

![Modify TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

## 複数の TiDB ノード グループで TiProxy を管理する {#manage-tiproxy-in-multiple-tidb-node-groups}

複数のTiDBノードグループがある場合、各TiDBノードグループには専用のTiProxyグループがあります。TiProxyは、同じTiDBノードグループ内のTiDBノードにトラフィックをルーティングすることで、コンピューティングリソースを分離します。各TiDBノードグループでTiProxyを有効化、無効化、または変更できます。ただし、すべてのTiDBノードグループでTiProxyのサイズは同じである必要があります。
