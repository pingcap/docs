---
title: Manage TiProxy
summary: TiProxyの有効化、無効化、表示、および変更方法について学びましょう。
---

# TiProxyを管理する {#manage-tiproxy}

このドキュメントでは、TiProxyの有効化、無効化、表示、および変更方法について説明します。

> **注記：**
>
> TiProxyは現在、AWS上にデプロイされたTiDB Cloud Dedicatedクラスターでのみ利用可能です。

## TiProxyを有効にする {#enable-tiproxy}

TiProxyは、任意のTiDBノードグループ内の新規クラスタまたは既存クラスタのどちらでも有効にできます。

### TiProxyノードのサイズと数を決定する {#decide-the-size-and-number-of-tiproxy-nodes}

TiProxyノードのサイズと数は、 TiDB Cloud DedicatedクラスタのQPS（1秒あたりのクエリ数）とネットワーク帯域幅の両方に依存します。ネットワーク帯域幅は、クライアントのリクエスト帯域幅とTiDBのレスポンス帯域幅の合計です。

以下の表は、各TiProxyサイズにおける最大QPSとネットワーク帯域幅を示しています。

| サイズ | 最大QPS | 最大ネットワーク帯域幅 |
| :-- | :---- | :---------- |
| 小さい | 30K   | 93 MiB/秒    |
| 大きい | 12万   | 312 MiB/秒   |

利用可能な TiProxy のサイズは`Small`と`Large`です。利用可能な TiProxy ノード数は 2、3、6、9、12、15、18、21、24 です。デフォルトの 2 つの小型 TiProxy ノードは、60K QPS と 186 MiB/s のネットワーク帯域幅を提供できます。高レイテンシーを防ぐために、QPS 容量の 20% を予約することをお勧めします。

例えば、クラスターの最大QPSが10万、最大ネットワーク帯域幅が100MiB/sの場合、TiProxyノードのサイズと数は主にQPSによって決まります。この場合、小型のTiProxyノードを6個選択できます。

### 新しいクラスターで TiProxy を有効にする {#enable-tiproxy-for-a-new-cluster}

新しいクラスターを作成する際に TiProxy を有効にするには、TiProxy のトグルをクリックし、TiProxy のサイズと数を選択します。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 既存のクラスターでTiProxyを有効にする {#enable-tiproxy-for-an-existing-cluster}

> **注記：**
>
> TiProxyを有効にすると、該当するTiDBノードグループ内のTiDBノードがローリング再起動され、再起動中に既存の接続が切断されます。また、新しい接続の作成に最大30秒かかる場合があります。TiProxyは必ずメンテナンス期間中に有効にしてください。

既存のクラスタで TiProxy を有効にするには、次の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「…」**をクリックし、ドロップダウンメニューから**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  **「クラスタの変更」**ページで、TiProxyのトグルをクリックし、TiProxyのサイズと数を選択します。

![Enable TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

### 制限事項と割り当て {#limitations-and-quotas}

-   TiDBノードグループには、少なくとも2つのTiDBノードが必要です。
-   TiDBノードのサイズは、少なくとも4つのvCPUである必要があります。
-   組織内の TiProxy ノードのデフォルトの最大数は`10`です。詳細については、[制限と割り当て](/tidb-cloud/limitations-and-quotas.md)参照してください。
-   TiDBクラスタのバージョンはv6.5.0以降である必要があります。

## TiProxyを無効にする {#disable-tiproxy}

> **注記：**
>
> TiProxyを無効にすると、接続が切断されます。また、新しい接続の作成に最大10秒間かかる場合があります。TiProxyを無効にする際は、必ずメンテナンス時間内に行ってください。

TiProxyを無効にするには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「…」**をクリックし、ドロップダウンメニューから**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  「**クラスタの変更」**ページで、TiProxyのトグルをクリックしてTiProxyを無効にします。

![Disable TiProxy](/media/tidb-cloud/tiproxy-disable-tiproxy.png)

## TiProxyをビュー {#view-tiproxy}

### TiProxyのトポロジーをビュー {#view-tiproxy-topology}

TiProxyのトポロジーを表示するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[監視] &gt; [ノード]**をクリックします。**ノードマップ**ページが表示されます。
3.  **ノードマップ**ページでは、TiProxyのトポロジーが**TiDB**ペインに表示されます。

![TiProxy Topology](/media/tidb-cloud/tiproxy-topology.png)

### TiProxyのメトリクスをビュー {#view-tiproxy-metrics}

TiProxyのメトリクスを表示するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  左側のナビゲーションペインで、 **[監視] &gt; [メトリクス]**をクリックします。[**メトリクス]**ページが表示されます。
3.  **メトリクス**ページで、 **[サーバー]**をクリックし、TiProxy関連のメトリクスまでスクロールします。特定のTiDBノードグループのTiProxyメトリクスを表示するには、 **[TiDBノードグループビュー]**をクリックし、TiDBノードグループを選択してから、TiProxy関連のメトリクスまでスクロールします。

指標には以下が含まれます。

-   **TiProxyのCPU使用率**：各TiProxyノードのCPU使用率統計情報。上限は100%です。CPU使用率が80%を超える場合は、TiProxyのスケールアウトをお勧めします。
-   **TiProxy接続数**：各TiProxyノード上の接続数。
-   **TiProxy スループット**: 各 TiProxy ノードで 1 秒あたりに転送されるバイト数。最大スループットが最大ネットワーク帯域幅に達した場合は、TiProxy をスケールアウトすることをお勧めします。最大ネットワーク帯域幅の詳細については、 [TiProxyノードのサイズと数を決定する](#decide-the-size-and-number-of-tiproxy-nodes)参照してください。
-   **TiProxyセッション移行の理由**：1分ごとに発生するセッション移行の数とその理由。たとえば、TiDBがスケールインし、TiProxyがセッションを他のTiDBノードに移行する場合、理由は`status`です。その他の移行理由については、 [TiProxyのモニタリング指標](https://docs.pingcap.com/tidb/stable/tiproxy-grafana#balance)参照してください。

### TiProxyの請求書をビュー {#view-tiproxy-bills}

TiProxyの請求書を表示するには、以下の手順を実行してください。

1.  [TiDB Cloudコンソール](https://tidbcloud.com)では、左上隅のコンボボックスを使用して、対象の組織に切り替えてください。
2.  左側のナビゲーションペインで**「請求」**をクリックします。 **「請求」**ページでは、デフォルトで**「請求書」**タブが表示されます。
3.  **サービス別概要**セクションでは、TiProxy ノードのコストは**TiDB Dedicated の**下に表示され、TiProxy のデータ転送コストは**データ転送 &gt; 同一リージョン**に含まれています。

![TiProxy Billing](/media/tidb-cloud/tiproxy-billing.png)

## TiProxyを変更する {#modify-tiproxy}

> **注記**
>
> -   TiProxyのサイズを直接変更することはサポートされていません。代わりに、TiProxyノードの数を変更することをお勧めします。TiProxyのサイズを変更する必要がある場合は、すべてのTiDBノードグループでTiProxyを無効にしてから再度有効にし、別のサイズを選択する必要があります。
> -   TiProxyでスケーリングを行うと、接続が切断されます。TiProxyのスケーリングは、必ずメンテナンス時間内に行ってください。

TiProxyをスケールインまたはスケールアウトするには、以下の手順を実行します。

1.  [TiDB Cloudコンソール](https://tidbcloud.com/)で、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、ターゲットのTiDB Cloud Dedicatedクラスターの名前をクリックして、その概要ページに移動します。
2.  右上隅の**「…」**をクリックし、ドロップダウンメニューから**「変更」**をクリックします。 **「クラスタの変更」**ページが表示されます。
3.  **「クラスタの変更」**ページで、TiProxyノードの数を変更します。

![Modify TiProxy](/media/tidb-cloud/tiproxy-enable-tiproxy.png)

## 複数のTiDBノードグループでTiProxyを管理する {#manage-tiproxy-in-multiple-tidb-node-groups}

複数の TiDB ノード グループがある場合、各 TiDB ノード グループには専用の TiProxy グループが割り当てられます。TiProxy は、同じ TiDB ノード グループ内の TiDB ノードにトラフィックをルーティングし、コンピューティング リソースを分離します。各 TiDB ノード グループで TiProxy を有効化、無効化、または変更できます。ただし、すべての TiDB ノード グループで TiProxy のサイズは同じである必要があります。
