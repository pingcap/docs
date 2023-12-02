---
title: Local Read under Three Data Centers Deployment
summary: Learn how to use the Stale Read feature to read local data under three DCs deployment and thus reduce cross-center requests.
---

# 3 つのデータセンター展開におけるローカル読み取り {#local-read-under-three-data-centers-deployment}

3 つのデータセンターのモデルでは、リージョンには各データセンターに分離された 3 つのレプリカがあります。ただし、強力な一貫性のある読み取りの要件により、TiDB はクエリごとに対応するデータのLeaderレプリカにアクセスする必要があります。Leaderレプリカとは異なるデータ センターでクエリが生成された場合、TiDB は別のデータ センターからデータを読み取る必要があるため、アクセスレイテンシーが増加します。

このドキュメントでは、 [ステイル読み取り](/stale-read.md)機能を使用して、リアルタイムのデータ可用性を犠牲にしてセンター間アクセスを回避し、アクセスレイテンシーを短縮する方法について説明します。

## 3 つのデータセンターからなる TiDB クラスターをデプロイ {#deploy-a-tidb-cluster-of-three-data-centers}

3 データセンター展開方法については、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md)を参照してください。

TiKV ノードと TiDB ノードの両方に構成項目`labels`が構成されている場合、同じデータセンター内の TiKV ノードと TiDB ノードの`zone`ラベルの値が同じである必要があることに注意してください。たとえば、TiKV ノードと TiDB ノードが両方ともデータ センター`dc-1`にある場合、2 つのノードを次のラベルで構成する必要があります。

    [labels]
    zone=dc-1

## ステイル読み取りを使用してローカル読み取りを実行する {#perform-local-read-using-stale-read}

[ステイル読み取り](/stale-read.md)は、ユーザーが履歴データを読み取るために TiDB が提供するメカニズムです。このメカニズムを使用すると、特定の時点または指定された時間範囲内の対応する履歴データを読み取ることができるため、storageノード間のデータ レプリケーションによってもたらされるレイテンシーを節約できます。地域分散展開の一部のシナリオでステイル読み取りを使用すると、TiDB は現在のデータ センターのレプリカにアクセスして、リアルタイム パフォーマンスを犠牲にして対応するデータを読み取ります。これにより、センター間接続によってもたらされるネットワークレイテンシーが回避され、クエリプロセス全体のアクセスレイテンシー。

TiDB がステイル読み取りクエリを受信したとき、その TiDB ノードの`zone`ラベルが構成され、 [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)が`closest-replicas`に設定されている場合、TiDB は、対応するデータ レプリカが存在する同じ`zone`ラベルを持つ TiKV ノードにリクエストを送信します。

ステイル読み取りの実行方法については、 [`AS OF TIMESTAMP`句を使用してステイル読み取りを実行する](/as-of-timestamp.md)を参照してください。
