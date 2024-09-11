---
title: Vector Search Limitations
summary: TiDB ベクトル検索の制限について学習します。
---

# ベクトル検索の制限 {#vector-search-limitations}

このドキュメントでは、TiDB Vector Search の既知の制限について説明します。当社は、より多くの機能を追加することで、お客様のエクスペリエンスを向上させるために継続的に取り組んでいます。

-   TiDB Vector Search は[TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターでのみ使用できます。TiDB TiDB Cloud Dedicated または TiDB Self-Managed では使用できません。

-   [ベクター](/tidb-cloud/vector-search-data-types.md)最大 16,000 次元をサポートします。

-   ベクター データは単精度浮動小数点数 (Float32) のみをサポートします。

-   [ベクトル検索インデックス](/tidb-cloud/vector-search-index.md)を作成する場合、コサイン距離と L2 距離のみがサポートされます。

## フィードバック {#feedback}

私たちはあなたのフィードバックを大切にしており、いつでもお手伝いいたします。

-   [Discordに参加する](https://discord.gg/zcqexutz2R)
-   [サポートポータルにアクセス](https://tidb.support.pingcap.com/)
