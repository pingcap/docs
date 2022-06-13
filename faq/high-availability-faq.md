---
title: High Availability FAQs
summary: Learn about the FAQs related to high availability of TiDB.
---

# 高可用性に関するFAQ {#high-availability-faqs}

このドキュメントは、TiDBの高可用性に関連するFAQをまとめたものです。

## TiDBはどのように強く一貫していますか？ {#how-is-tidb-strongly-consistent}

ノード障害が発生した場合の回復可能性を確保するために、 [いかだコンセンサスアルゴリズム](https://raft.github.io/)を使用してTiKVノード間でデータが冗長的にコピーされます。

最下層では、TiKVはレプリケーションログとステートマシンのモデルを使用してデータをレプリケートします。書き込み要求の場合、データはリーダーに書き込まれ、リーダーはコマンドをログの形式でフォロワーに複製します。クラスタのノードの大部分がこのログを受信すると、このログはコミットされ、ステートマシンに適用できます。

## 3つの地理的に分散したデータセンターの展開に推奨されるソリューションは何ですか？ {#what-s-the-recommended-solution-for-the-deployment-of-three-geo-distributed-data-centers}

TiDBのアーキテクチャは、地理分布とマルチアクティブ性を完全にサポートすることを保証します。データとアプリケーションは常にオンになっています。すべての停止はアプリケーションに対して透過的であり、データは自動的に回復できます。操作は、ネットワークの遅延と安定性によって異なります。レイテンシを5ms以内に保つことをお勧めします。現在、同様のユースケースがすでにあります。詳しくは[info@pingcap.com](mailto:info@pingcap.com)までお問い合わせください。
