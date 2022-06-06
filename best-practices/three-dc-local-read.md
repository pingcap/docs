---
title: Local Read under Three Data Centers Deployment
summary: Learn how to use the Stale Read feature to read local data under three DCs deployment and thus reduce cross-center requests.
---

# 3つのデータセンター展開でのローカル読み取り {#local-read-under-three-data-centers-deployment}

3つのデータセンターのモデルでは、リージョンには各データセンターで分離された3つのレプリカがあります。ただし、強一貫性のある読み取りが必要なため、TiDBはすべてのクエリで対応するデータのリーダーレプリカにアクセスする必要があります。リーダーレプリカとは異なるデータセンターでクエリが生成された場合、TiDBは別のデータセンターからデータを読み取る必要があるため、アクセスの待ち時間が長くなります。

このドキュメントでは、 [古い読み取り](/stale-read.md)つの機能を使用して、クロスセンターアクセスを回避し、リアルタイムのデータ可用性を犠牲にしてアクセス遅延を削減する方法について説明します。

## 3つのデータセンターのTiDBクラスタをデプロイする {#deploy-a-tidb-cluster-of-three-data-centers}

3データセンターの導入方法については、 [1 つの地域展開における複数のデータセンター](/multi-data-centers-in-one-city-deployment.md)を参照してください。

TiKVノードとTiDBノードの両方に構成項目`labels`が構成されている場合、同じデータセンター内のTiKVノードとTiDBノードの`zone`ラベルの値は同じである必要があることに注意してください。たとえば、TiKVノードとTiDBノードの両方がデータセンター`dc-1`にある場合、2つのノードは次のラベルで構成する必要があります。

```
[labels]
zone=dc-1
```

## StaleReadを使用してローカル読み取りを実行します {#perform-local-read-using-stale-read}

[古い読み取り](/stale-read.md)は、TiDBがユーザーに履歴データを読み取るために提供するメカニズムです。このメカニズムを使用すると、特定の時点または指定された時間範囲内の対応する履歴データを読み取ることができるため、ストレージノード間のデータレプリケーションによってもたらされる遅延を節約できます。地理的分散展開の一部のシナリオでStaleReadを使用する場合、TiDBは現在のデータセンターのレプリカにアクセスして、リアルタイムのパフォーマンスを犠牲にして対応するデータを読み取ります。これにより、クロスセンター接続によってもたらされるネットワーク遅延が回避され、クエリプロセス全体のアクセスレイテンシ。

TiDBがStaleReadクエリを受信すると、そのTiDBノードの`zone`ラベルが構成されている場合、TiDBは、対応するデータレプリカが存在する同じ`zone`ラベルのTiKVノードに要求を送信します。

Stale Readを実行する方法については、 [`AS OF TIMESTAMP`句を使用して古い読み取りを実行します](/as-of-timestamp.md)を参照してください。
