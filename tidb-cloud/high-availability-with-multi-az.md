---
title: High Availability in TiDB Cloud Dedicated
summary: TiDB Cloud Dedicated は、マルチ AZ デプロイメントによる高可用性をサポートします。
---

# TiDB Cloud専用における高可用性 {#high-availability-in-tidb-cloud-dedicated}

TiDBはRaftコンセンサスアルゴリズムを使用し、 Raftグループ内のstorage全体にデータの高可用性と安全なレプリケーションを実現します。データはstorageノード間で冗長コピーされ、異なるアベイラビリティゾーンに配置されるため、マシンやデータセンターの障害から保護されます。自動フェイルオーバー機能により、TiDBはサービスの常時稼働を保証します。

TiDB Cloud Dedicated クラスタは、TiDB ノード、TiKV ノード、 TiFlashノードという 3 つの主要コンポーネントで構成されています。TiDB TiDB Cloud Dedicated の各コンポーネントの高可用性実装は次のとおりです。

-   **TiDBノード**

    TiDBはコンピューティングのみを目的としており、データの保存は行いません。水平方向に拡張可能です。TiDB TiDB Cloud Dedicatedは、リージョン内の異なるアベイラビリティゾーンにTiDBノードを均等に配置します。ユーザーがSQLリクエストを実行すると、リクエストはまず複数のアベイラビリティゾーンに展開されたロードバランサーを通過し、その後、ロードバランサーによって複数のTiDBノードに分散されて実行されます。高可用性を確保するため、各TiDB Cloud Dedicatedクラスタには少なくとも2つのTiDBノードを配置することをお勧めします。

-   **TiKVノード**

    [TiKV](https://docs.pingcap.com/tidb/stable/tikv-overview) 、水平スケーラビリティを備えたTiDB Cloud Dedicatedクラスタの行ベースのstorageレイヤーです。TiDB TiDB Cloud DedicatedクラスタのTiKVノードの最小数は3です。TiDB TiDB Cloud Dedicatedは、選択したリージョン内のすべてのアベイラビリティゾーン（少なくとも3つ）にTiKVノードを均等にデプロイすることで、耐久性と高可用性を実現します。典型的な3レプリカ構成では、データはすべてのアベイラビリティゾーンのTiKVノードに均等に分散され、各TiKVノードのディスクに永続化されます。

-   **TiFlashノード**

    [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 、TiKV の列指向storage拡張機能であり、TiDB を本質的にハイブリッドトランザクション/分析処理 (HTAP) データベースにする重要なコンポーネントです。TiFlashTiFlash、列指向レプリカはRaft Learnerコンセンサスアルゴリズムに従って非同期的に複製されます。TiDB TiDB Cloud Dedicated は、 TiFlashノードをリージョン内の異なるアベイラビリティゾーンに均等にデプロイします。本番環境での高可用性を確保するため、各TiDB Cloud Dedicated クラスターに少なくとも 2 つのTiFlashノードを設定し、少なくとも 2 つのデータレプリカを作成本番ことをお勧めします。
