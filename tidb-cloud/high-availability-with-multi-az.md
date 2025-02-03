---
title: High Availability in TiDB Cloud Dedicated
summary: TiDB Cloud Dedicated は、マルチ AZ デプロイメントによる高可用性をサポートします。
---

# TiDB Cloud専用における高可用性 {#high-availability-in-tidb-cloud-dedicated}

TiDB はRaftコンセンサス アルゴリズムを使用して、データの可用性を高め、 Raftグループのstorage全体に安全に複製できるようにします。データはstorageノード間で冗長的にコピーされ、マシンまたはデータ センターの障害から保護するために異なる可用性ゾーンに配置されます。自動フェイルオーバーにより、TiDB はサービスの常時稼働を保証します。

TiDB Cloud Dedicated クラスターは、TiDB ノード、TiKV ノード、 TiFlashノードの 3 つの主要コンポーネントで構成されています。TiDB TiDB Cloud Dedicated の各コンポーネントの高可用性実装は次のとおりです。

-   **TiDBノード**

    TiDB はコンピューティング専用であり、データを保存しません。水平方向に拡張可能です。TiDB TiDB Cloud Dedicated は、リージョン内の異なるアベイラビリティ ゾーンに TiDB ノードを均等にデプロイします。ユーザーが SQL リクエストを実行すると、リクエストはまずアベイラビリティ ゾーン全体にデプロイされたロード バランサーを通過し、次にロード バランサーはリクエストを異なる TiDB ノードに分散して実行します。高可用性のために、各TiDB Cloud Dedicated クラスターには少なくとも 2 つの TiDB ノードを配置することをお勧めします。

-   **TiKVノード**

    [ティクヴ](https://docs.pingcap.com/tidb/stable/tikv-overview) 、水平スケーラビリティを備えたTiDB Cloud Dedicated クラスターの行ベースのstorageレイヤーです。TiDB TiDB Cloud Dedicated クラスターの TiKV ノードの最小数は 3 です。TiDB TiDB Cloud Dedicated は、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。一般的な 3 つのレプリカのセットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノードに均等に分散され、各 TiKV ノードのディスクに保持されます。

-   **TiFlashノード**

    [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)は、TiKV の列指向storage拡張機能として、TiDB を本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースにする重要なコンポーネントです。TiFlash では、列指向TiFlashはRaft Learnerコンセンサス アルゴリズムに従って非同期的にレプリケートされます。TiDB TiDB Cloud Dedicated は、 TiFlashノードをリージョン内の異なるアベイラビリティ ゾーンに均等にデプロイします。実稼働環境で高可用性を確保するには、各TiDB Cloud Dedicated クラスターに少なくとも 2 つのTiFlashノードを設定し、データのレプリカを少なくとも 2 つ作成本番ことをお勧めします。
