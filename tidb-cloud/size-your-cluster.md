---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDB のサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、 Dedicated Tierクラスターのサイズを決定する方法について説明します。

> **ノート：**
>
> [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのサイズは変更できません。

## サイズ TiDB {#size-tidb}

TiDB はコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。

TiDB のノード サイズとノード数の両方を構成できます。

さまざまなクラスター スケールのパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiDB ノードサイズ {#tidb-node-size}

サポートされているノード サイズは次のとおりです。

-   2 vCPU、8 GiB (ベータ)
-   4 vCPU、16 GiB
-   8 vCPU、16 GiB
-   16 vCPU、32 GiB

> **ノート：**
>
> TiDB のノード サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合は、次の制限に注意してください。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用できます。 4 vCPU TiDB は 4 vCPU TiKV でのみ使用できます。
> -   TiFlashは利用できません。

### TiDB ノード数 {#tidb-node-quantity}

高可用性のために、 TiDB Cloudクラスターごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

一般に、TiDB のパフォーマンスは、TiDB ノードの数に比例して向上します。ただし、TiDB ノードの数が 8 を超えると、パフォーマンスの増加は線形比例よりもわずかに少なくなります。追加の 8 ノードごとに、パフォーマンス偏差係数は約 5% です。

例えば：

-   TiDBノードが9台の場合、性能偏差係数は約5%なので、TiDBの性能はTiDBノード単体の約`9 * (1 - 5%) = 8.55`倍です。
-   TiDBノードが16台の場合、性能の偏差係数は約10%なので、TiDBの性能はTiDBノード1台の性能の`16 * (1 - 10%) = 14.4`倍になります。

TiDB ノードの指定されたレイテンシーの場合、TiDB のパフォーマンスは、さまざまな読み取り/書き込み比率によって異なります。

さまざまなワークロードでの 8 vCPU、16 GiB TiDB ノードのパフォーマンスは次のとおりです。

| ワークロード | QPS (P95 ≒ 100ms) | QPS (P99 ≒ 300ms) | QPS (P99 ≒ 100ms) |
| ------ | ----------------- | ----------------- | ----------------- |
| 読む     | 18,900            | 9,450             | 6,300             |
| 混合     | 15,500            | 7,750             | 5,200             |
| 書く     | 18,000            | 9,000             | 6,000             |

TiDBノード数が8未満の場合、性能偏差係数はほぼ0%なので、16 vCPU、32 GiB TiDBノードのTiDBパフォーマンスは、8 vCPU、16 GiB TiDBノードの約2倍になります。 TiDB ノードの数が 8 を超える場合は、16 個の vCPU、32 GiB の TiDB ノードを選択することをお勧めします。これは、必要なノードが少なくなり、パフォーマンスの偏差係数が小さくなることを意味します。

クラスターのサイズを計画するときは、次の式を使用して、ワークロードの種類、全体的な期待パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiDB ノードのパフォーマンスに従って、TiDB ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、最初に`node num = ceil(overall expected performance ÷ performance per node)`を計算して大まかなノード番号を取得し、次に対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスは 110,000 QPS で、P95レイテンシーは約 100 ミリ秒で、8 個の vCPU、16 GiB の TiDB ノードを使用するとします。次に、8 vCPU、16 GiB の TiDB ノードの推定 TiDB パフォーマンスを前の表 (つまり`15,500` ) から取得し、TiDB ノードのおおよその数を次のように計算できます。

`node num = ceil(110,000 ÷ 15,500) = 8`

8 ノードのパフォーマンス偏差係数は約 5% であるため、推定 TiDB パフォーマンスは`8 * 15,500 * (1 - 5%) = 117,800`であり、110,000 QPS の期待パフォーマンスを満たすことができます。

したがって、8 つの TiDB ノード (8 つの vCPU、16 GiB) が推奨されます。

## サイズ TiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

TiKV のノード サイズ、ノード数、およびノードstorageを構成できます。

さまざまなクラスター スケールのパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiKV ノードサイズ {#tikv-node-size}

サポートされているノード サイズは次のとおりです。

-   2 vCPU、8 GiB (ベータ)
-   4 vCPU、16 GiB
-   8 vCPU、32 GiB
-   8 vCPU、64 GiB
-   16 vCPU、64 GiB

> **ノート：**
>
> TiKV のノード サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合は、次の制限に注意してください。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。 4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは利用できません。

### TiKV ノード数 {#tikv-node-quantity}

TiKV ノードの数は**、少なくとも 1 セット (3 つの異なる利用可能なゾーンに 3 つのノード)**である必要があります。

TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。典型的な 3 レプリカ セットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

> **ノート：**
>
> TiDB クラスターをスケーリングすると、3 つのアベイラビリティーゾーンのノードが同時に増減します。ニーズに基づいて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

TiKV は主にデータstorageに使用されますが、TiKV ノードのパフォーマンスはワークロードによっても異なります。したがって、TiKV ノードの数を計画するときは、 [**データ量**](#estimate-tikv-node-quantity-according-to-data-volume)と[期待されるパフォーマンス](#estimate-tikv-node-quantity-according-to-expected-performance)の両方に従って見積もり、2 つの見積もりのうち大きい方を推奨ノード数として使用する必要があります。

#### データ量に応じてTiKVノード数を見積もる {#estimate-tikv-node-quantity-according-to-data-volume}

次のように、データ量に応じて TiKV ノードの推奨数を計算できます。

`node num = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

一般的に、TiKVstorageの使用率は 80% 未満に抑えることをお勧めします。 TiDB Cloudのレプリカの数は、デフォルトで 3 です。 8 vCPU、64 GiB の TiKV ノードの最大storage容量は 4096 GiB です。

過去のデータに基づくと、TiKV の平均圧縮率は約 40% です。

MySQL ダンプ ファイルのサイズが 20 TB で、TiKV 圧縮率が 40% であるとします。次に、データ量に応じて推奨される TiKV ノードの数を次のように計算できます。

`node num = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### 期待されるパフォーマンスに応じて TiKV ノードの数量を見積もる {#estimate-tikv-node-quantity-according-to-expected-performance}

TiDB のパフォーマンスと同様に、TiKV のパフォーマンスは TiKV ノードの数に比例して増加します。ただし、TiKV ノードの数が 8 を超えると、パフォーマンスの増加は線形比例よりもわずかに少なくなります。追加の 8 ノードごとに、パフォーマンス偏差係数は約 5% です。

例えば：

-   TiKVノードが9台の場合、性能偏差係数は約5%であるため、TiKVの性能はTiKVノード1台の性能の約`9 * (1 - 5%) = 8.55`倍になります。
-   TiKVノードが18台ある場合の性能偏差係数は約10%なので、TiKVの性能はTiKVノード単体の性能の`18 * (1 - 10%) = 16.2`倍になります。

TiKV ノードの指定されたレイテンシーの場合、TiKV のパフォーマンスは、さまざまな読み取り/書き込み比率によって異なります。

さまざまなワークロードでの 8 vCPU、32 GiB TiKV ノードのパフォーマンスは次のとおりです。

| ワークロード | QPS (P95 ≒ 100ms) | QPS (P99 ≒ 300ms) | QPS (P99 ≒ 100ms) |
| ------ | ----------------- | ----------------- | ----------------- |
| 読む     | 28,000            | 14,000            | 7,000             |
| 混合     | 17,800            | 8,900             | 4,450             |
| 書く     | 14,500            | 7,250             | 3,625             |

TiKV ノード数が 8 以下の場合、性能偏差係数はほぼ 0% であるため、16 vCPU、64 GiB TiKV ノードのパフォーマンスは、8 vCPU、32 GiB TiKV ノードの約 2 倍になります。 TiKV ノードの数が 8 を超える場合は、16 個の vCPU、64 GiB の TiKV ノードを選択することをお勧めします。これは、必要なノードが少なくなり、パフォーマンスの偏差係数が小さくなることを意味します。

クラスターのサイズを計画するときは、次の式を使用して、ワークロードの種類、全体的な期待パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiKV ノードのパフォーマンスに従って、TiKV ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、最初に`node num = ceil(overall expected performance ÷ performance per node)`を計算して大まかなノード番号を取得し、次に対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスは 110,000 QPS で、P95レイテンシーは約 100 ミリ秒で、8 個の vCPU、32 GiB TiKV ノードを使用するとします。次に、8 vCPU、32 GiB の TiKV ノードの推定 TiKV パフォーマンスを前の表 (つまり`17,800` ) から取得し、TiKV ノードのおおよその数を次のように計算できます。

`node num = ceil(110,000 / 17,800 ) = 7`

7 は 8 より小さいため、7 ノードのパフォーマンス偏差係数は 0 です。推定 TiKV パフォーマンスは`7 * 17,800 * (1 - 0) = 124,600`であり、110,000 QPS の期待パフォーマンスを満たすことができます。

したがって、期待されるパフォーマンスに応じて、7 つの TiKV ノード (8 つの vCPU、32 GiB) が推奨されます。

次に、データ量に基づいて計算された TiKV ノード数と、期待されるパフォーマンスに基づいて計算された数を比較し、大きい方を TiKV ノードの推奨数として使用できます。

### TiKV ノードstorage {#tikv-node-storage}

さまざまな TiKV ノード サイズでサポートされているノードstorageは次のとおりです。

|  ノードサイズ | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-----: | :----------: | :----------: | :--------------: |
|  2 vCPU |    200 GiB   |    500 GiB   |      200 GiB     |
|  4 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |
|  8 vCPU |    200 GiB   |   4096 GiB   |      500 GiB     |
| 16 vCPU |    200 GiB   |   4096 GiB   |      500 GiB     |

> **ノート：**
>
> クラスターの作成後に TiKV ノードstorageを減らすことはできません。

## サイズTiFlash {#size-tiflash}

TiFlash はTiKV からのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlashのノード サイズ、ノード数、およびノードstorageを設定できます。

### TiFlashノードサイズ {#tiflash-node-size}

サポートされているノード サイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB

TiDB または TiKV の vCPU サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合、 TiFlash は使用できないことに注意してください。

### TiFlashノード数 {#tiflash-node-quantity}

TiDB Cloud は、リージョン内の異なるアベイラビリティ ゾーンにTiFlashノードを均等にデプロイします。各TiDB Cloudクラスターで少なくとも 2 つのTiFlashノードを構成し、本番環境での高可用性のためにデータの少なくとも 2 つのレプリカを作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノードstorageを1024 GiB として構成し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GiB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GiB) を設定すると、必要なTiFlashノードの数は次のとおりです。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノードstorage {#tiflash-node-storage}

さまざまなTiFlashノード サイズでサポートされているノードstorageは次のとおりです。

|  ノードサイズ | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-----: | :----------: | :----------: | :--------------: |
|  8 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |
| 16 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |

> **ノート：**
>
> クラスターの作成後にTiFlashノードstorageを減らすことはできません。
