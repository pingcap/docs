---
title: High Availability FAQs
summary: Learn about the FAQs related to high availability of TiDB.
---

# 高可用性に関するよくある質問 {#high-availability-faqs}

このドキュメントには、TiDB の高可用性に関する FAQ がまとめられています。

## TiDB はどのように強い一貫性を持っていますか? {#how-is-tidb-strongly-consistent}

データは[Raftコンセンサスアルゴリズム](https://raft.github.io/)使用して TiKV ノード間で冗長的に複製され、ノード障害が発生した場合の回復可能性を確保します。

最レイヤーでは、TiKV はレプリケーション ログ + ステート マシンのモデルを使用してデータをレプリケートします。書き込みリクエストの場合、データはLeaderに書き込まれ、Leaderはコマンドをログの形式でフォロワーに複製します。クラスター内の大部分のノードがこのログを受信すると、このログはコミットされ、ステート マシンに適用できます。

## 3 つの地理的に分散されたデータセンターの展開に推奨されるソリューションは何ですか? {#what-s-the-recommended-solution-for-the-deployment-of-three-geo-distributed-data-centers}

TiDB のアーキテクチャは、地理的分散とマルチアクティブ性を完全にサポートすることを保証します。データとアプリケーションは常に稼働しています。すべての停止はアプリケーションに対して透過的であり、データは自動的に回復されます。動作はネットワークのレイテンシーと安定性に依存します。レイテンシーを5 ミリ秒以内に保つことをお勧めします。現在、TiDB にはすでに同様の使用例があります。詳細は[2 つの地域に配置された 3 つのデータ センター](/three-data-centers-in-two-cities-deployment.md)を参照してください。
