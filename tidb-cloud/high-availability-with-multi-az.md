---
title: High Availability with Multi-AZ Deployments
summary: TiDB Cloud supports high availability with Multi-AZ deployments.
---

# マルチ AZ 配置による高可用性 {#high-availability-with-multi-az-deployments}

TiDB はRaftコンセンサス アルゴリズムを使用して、データの可用性を高め、 Raftグループ内のstorage全体で安全に複製されるようにします。データはstorageノード間で重複してコピーされ、異なる可用性ゾーンに配置されて、マシンまたはデータ センターの障害から保護されます。自動フェールオーバーにより、TiDB はサービスが常にオンになっていることを保証します。

TiDB Cloudクラスターは、TiDB ノード、TiKV ノード、 TiFlashノードの 3 つの主要コンポーネントで構成されています。 Dedicated Tierの各コンポーネントの高可用性実装は次のとおりです。

-   **TiDB ノード**

    TiDB はコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。 TiDB Cloud は、リージョン内の異なるアベイラビリティ ゾーンに TiDB ノードを均等にデプロイします。ユーザーが SQL リクエストを実行すると、リクエストは最初にアベイラビリティーゾーン全体にデプロイされたロードバランサーを通過し、次にロードバランサーがリクエストを実行のために異なる TiDB ノードに分散します。高可用性のために、各TiDB Cloudクラスターに少なくとも 2 つの TiDB ノードを配置することをお勧めします。

-   **TiKV ノード**

    [TiKV](https://docs.pingcap.com/tidb/stable/tikv-overview)は、水平スケーラビリティを備えたTiDB Cloudクラスターの行ベースのstorageレイヤーです。 TiDB Cloudでは、クラスターの TiKV ノードの最小数は 3 です。TiDB TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。典型的な 3 レプリカ セットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

-   **TiFlashノード**

    [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)は、TiKV の列storage拡張として、TiDB を本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースにする重要なコンポーネントです。 TiFlashでは、カラムナー レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。 TiDB Cloud は、リージョン内の異なるアベイラビリティ ゾーンにTiFlashノードを均等にデプロイします。各TiDB Cloudクラスターで少なくとも 2 つのTiFlashノードを構成し、本番環境での高可用性のためにデータの少なくとも 2 つのレプリカを作成することをお勧めします。
