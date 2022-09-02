---
title: High Availability FAQs
summary: Learn about the FAQs related to high availability of TiDB.
---

# 高可用性に関するよくある質問 {#high-availability-faqs}

このドキュメントは、TiDB の高可用性に関する FAQ をまとめたものです。

## TiDB の強整合性はどのようになっていますか? {#how-is-tidb-strongly-consistent}

[Raftコンセンサスアルゴリズム](https://raft.github.io/)を使用して TiKV ノード間でデータが冗長にコピーされ、ノード障害が発生した場合の回復可能性を確保します。

最レイヤーでは、TiKV はレプリケーション ログ + ステート マシンのモデルを使用してデータをレプリケートします。書き込みリクエストの場合、データはリーダーに書き込まれ、リーダーはコマンドをログの形式でフォロワーに複製します。クラスタ内の大部分のノードがこのログを受信すると、このログがコミットされ、ステート マシンに適用できます。

## 地理的に分散した 3 つのデータ センターの展開に推奨されるソリューションは何ですか? {#what-s-the-recommended-solution-for-the-deployment-of-three-geo-distributed-data-centers}

TiDB のアーキテクチャは、地理的分散とマルチアクティブ性を完全にサポートすることを保証します。データとアプリケーションは常時稼働しています。すべての停止はアプリケーションに対して透過的であり、データは自動的に回復できます。操作は、ネットワークのレイテンシーと安定性に依存します。レイテンシーを 5 ミリ秒以内に保つことをお勧めします。現在、すでに同様のユースケースがあります。詳しくは[info@pingcap.com](mailto:info@pingcap.com)までお問い合わせください。
