---
title: High Availability with Multi-AZ Deployments
summary: TiDB Cloud supports high availability with Multi-AZ deployments.
---

# マルチ AZ 展開による高可用性 {#high-availability-with-multi-az-deployments}

TiDB は、 Raftコンセンサス アルゴリズムを使用して、データの可用性が高く、 Raftグループ内のstorage全体に安全に複製されることを保証します。マシンやデータセンターの障害から保護するために、データはstorageノード間で冗長的にコピーされ、異なるアベイラビリティ ゾーンに配置されます。 TiDB は自動フェイルオーバーにより、サービスが常に稼働していることを保証します。

TiDB Cloudクラスターは、TiDB ノード、TiKV ノード、 TiFlashノードの 3 つの主要コンポーネントで構成されます。 TiDB Dended の各コンポーネントの高可用性実装は次のとおりです。

-   **TiDB ノード**

    TiDB はコンピューティング専用であり、データは保存されません。水平方向にスケーラブルです。 TiDB Cloud は、 TiDB ノードをリージョン内のさまざまなアベイラビリティ ゾーンに均等にデプロイします。ユーザーが SQL リクエストを実行すると、リクエストはまずアベイラビリティ ゾーン全体にデプロイされたロード バランサを通過し、次にロード バランサはリクエストを実行のためにさまざまな TiDB ノードに分散します。高可用性を実現するために、各TiDB Cloudクラスターに少なくとも 2 つの TiDB ノードを含めることをお勧めします。

-   **TiKVノード**

    [TiKV](https://docs.pingcap.com/tidb/stable/tikv-overview)は、水平スケーラビリティを備えたTiDB Cloudクラスターの行ベースのstorageレイヤーです。 TiDB Cloudでは、クラスターの TiKV ノードの最小数は 3 です。TiDBTiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内のすべての可用性ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。一般的な 3 レプリカのセットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

-   **TiFlashノード**

    TiKV の列指向storage拡張機能である[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)は、TiDB を本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースにする重要なコンポーネントです。 TiFlashでは、柱状レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。 TiDB Cloud は、 TiFlashノードをリージョン内のさまざまなアベイラビリティ ゾーンに均等にデプロイします。本番環境での高可用性を実現するために、各TiDB Cloudクラスターに少なくとも 2 つのTiFlashノードを構成し、データの少なくとも 2 つのレプリカを作成することをお勧めします。
