---
title: High Availability with Multi-AZ Deployments
summary: TiDB Cloud supports high availability with Multi-AZ deployments.
---

# マルチAZ展開による高可用性 {#high-availability-with-multi-az-deployments}

TiDBは、Raftコンセンサスアルゴリズムを使用して、データの可用性が高く、Raftグループのストレージ全体に安全に複製されるようにします。データはストレージノード間で冗長的にコピーされ、マシンまたはデータセンターの障害から保護するために異なるアベイラビリティーゾーンに配置されます。自動フェイルオーバーにより、TiDBはサービスが常にオンになっていることを保証します。

TiDB Cloudクラスターは、TiDBノード、TiKVノード、TiFlashノードの3つの主要コンポーネントで構成されています。専用層の各コンポーネントの高可用性実装は次のとおりです。

-   **TiDBノード**

    TiDBはコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。 TiDB Cloudは、TiDBノードをリージョン内のさまざまなアベイラビリティーゾーンに均等にデプロイします。ユーザーがSQLリクエストを実行すると、リクエストは最初にアベイラビリティーゾーン全体にデプロイされたロードバランサーを通過し、次にロードバランサーがリクエストをさまざまなTiDBノードに分散して実行します。高可用性を実現するには、各TiDB Cloudクラスタに少なくとも2つのTiDBノードを配置することをお勧めします。

-   **TiKVノード**

    TiKV（ [https://docs.pingcap.com/tidb/stable/tikv-overview](https://docs.pingcap.com/tidb/stable/tikv-overview) ）は、水平方向のスケーラビリティを備えたTiDB Cloudクラスタの行ベースのストレージレイヤーです。 TiDB Cloudでは、クラスタのTiKVノードの最小数は3です。TiDBCloudは、耐久性と高可用性を実現するために、選択したリージョンのすべてのアベイラビリティーゾーン（少なくとも3つ）にTiKVノードを均等にデプロイします。通常の3レプリカのセットアップでは、データはすべてのアベイラビリティーゾーンのTiKVノードに均等に分散され、各TiKVノードのディスクに保持されます。

-   **TiFlash<sup>ベータ</sup>ノード**

    TiKVの列型ストレージ拡張としてのTiFlash<sup>ベータ</sup>（ [https://docs.pingcap.com/tidb/stable/tiflash-overview](https://docs.pingcap.com/tidb/stable/tiflash-overview) ）は、TiDBを本質的にハイブリッドトランザクション/分析処理（HTAP）データベースにする重要なコンポーネントです。 TiFlash<sup>ベータ版</sup>では、列レプリカはRaftLearnerコンセンサスアルゴリズムに従って非同期に複製されます。 TiDB Cloudは、TiFlash<sup>ベータ</sup>ノードをリージョン内のさまざまなアベイラビリティーゾーンに均等にデプロイします。本番環境で高可用性を実現するために、各TiDB Cloudクラスタに少なくとも2つのTiFlash<sup>ベータ</sup>ノードを構成し、データのレプリカを少なくとも2つ作成することをお勧めします。
