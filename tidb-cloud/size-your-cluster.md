---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDB サイズを決定する {#determine-your-tidb-size}

このドキュメントでは、TiDB 専用クラスターのサイズを決定する方法について説明します。

> **注記：**
>
> [TiDB サーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-serverless)クラスターのサイズは変更できません。

## サイズ TiDB {#size-tidb}

TiDB はコンピューティング専用であり、データは保存されません。水平方向にスケーラブルです。

TiDB のノード番号、vCPU、RAM を構成できます。

さまざまなクラスター規模のパフォーマンス テストの結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiDB vCPU と RAM {#tidb-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

-   4 vCPU、16 GiB
-   8 vCPU、16 GiB
-   16 vCPU、32 GiB

> **注記：**
>
> TiDB の vCPU および RAM サイズが**4 vCPU、16 GiB**に設定されている場合は、次の制限に注意してください。
>
> -   TiDB のノード番号は 1 または 2 のみに設定でき、TiKV のノード番号は 3 に固定されます。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用できます。
> -   TiFlashは使用できません。

### TiDB ノード番号 {#tidb-node-number}

高可用性を実現するには、 TiDB Cloudクラスターごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

一般に、TiDB のパフォーマンスは、TiDB ノードの数に応じて直線的に増加します。ただし、TiDB ノードの数が 8 を超えると、パフォーマンスの増加は線形比例よりわずかに小さくなります。追加の 8 ノードごとに、パフォーマンス偏差係数は約 5% になります。

例えば：

-   TiDB ノードが 9 個ある場合、性能偏差係数は約 5% であるため、TiDB の性能は単一の TiDB ノードの性能の約`9 * (1 - 5%) = 8.55`倍になります。
-   TiDB ノードが 16 個ある場合、性能偏差係数は約 10% となるため、TiDB の性能は単一の TiDB ノードの性能の`16 * (1 - 10%) = 14.4`倍となります。

TiDB ノードの指定されたレイテンシーでは、TiDB のパフォーマンスは読み取り/書き込み比率の違いによって異なります。

さまざまなワークロードにおける 8 vCPU、16 GiB TiDB ノードのパフォーマンスは次のとおりです。

| ワークロード | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
| ------ | ----------------- | ----------------- | ----------------- |
| 読む     | 18,900            | 9,450             | 6,300             |
| 混合     | 15,500            | 7,750             | 5,200             |
| 書く     | 18,000            | 9,000             | 6,000             |

TiDB ノードの数が 8 未満の場合、パフォーマンス偏差係数はほぼ 0% になるため、16 vCPU、32 GiB TiDB ノードの TiDB パフォーマンスは、8 vCPU、16 GiB TiDB ノードのおよそ 2 倍になります。 TiDB ノードの数が 8 を超える場合は、必要なノードが少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、32 GiB TiDB ノードを選択することをお勧めします。

クラスターのサイズを計画するときは、次の式を使用して、ワークロード タイプ、全体的な期待パフォーマンス (QPS)、およびワークロード タイプに対応する単一 TiDB ノードのパフォーマンスに応じて TiDB ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node num = ceil(overall expected performance ÷ performance per node)`を計算して大まかなノード番号を取得し、次に対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスは 110,000 QPS、P95レイテンシーは約 100 ミリ秒、8 vCPU、16 GiB TiDB ノードを使用するとします。次に、前の表から 8 vCPU、16 GiB TiDB ノードの推定 TiDB パフォーマンス (これは`15,500` ) を取得し、次のように TiDB ノードのおおよその数を計算できます。

`node num = ceil(110,000 ÷ 15,500) = 8`

8 ノードのパフォーマンス偏差係数は約 5% であるため、TiDB の推定パフォーマンスは`8 * 15,500 * (1 - 5%) = 117,800`となり、予想される 110,000 QPS のパフォーマンスを満たすことができます。

したがって、8 つの TiDB ノード (8 vCPU、16 GiB) が推奨されます。

## サイズTiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

TiKV のノード番号、vCPU と RAM、storageを構成できます。

さまざまなクラスター規模のパフォーマンス テストの結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiKV vCPU と RAM {#tikv-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

-   4 vCPU、16 GiB
-   8 vCPU、32 GiB
-   8 vCPU、64 GiB
-   16 vCPU、64 GiB

> **注記：**
>
> TiKV の vCPU および RAM サイズが**4 vCPU、16 GiB**に設定されている場合は、次の制限に注意してください。
>
> -   TiDB のノード番号は 1 または 2 のみに設定でき、TiKV のノード番号は 3 に固定されます。
> -   4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは使用できません。

### TiKV ノード番号 {#tikv-node-number}

TiKV ノードの数**は少なくとも 1 セット (3 つの異なる利用可能なゾーンに 3 つのノード)**である必要があります。

TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョン内のすべての可用性ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。一般的な 3 レプリカのセットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

> **注記：**
>
> TiDB クラスターをスケールすると、3 つのアベイラビリティ ゾーン内のノードが同時に増加または減少します。ニーズに基づいて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタを拡張する](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

TiKV は主にデータstorageに使用されますが、TiKV ノードのパフォーマンスはさまざまなワークロードによっても異なります。したがって、TiKV ノードの数を計画するときは、 [**データ量**](#estimate-tikv-node-number-according-to-data-volume)と[期待されるパフォーマンス](#estimate-tikv-node-number-according-to-expected-performance)の両方に従って推定し、2 つの推定のうち大きい方を推奨ノード数として採用する必要があります。

#### データ量に応じてTiKVノード数を見積もる {#estimate-tikv-node-number-according-to-data-volume}

データ量に応じて、推奨される TiKV ノードの数を次のように計算できます。

`node num = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

一般に、TiKVstorageの使用率を 80% 未満に保つことをお勧めします。 TiDB Cloud内のレプリカの数はデフォルトで 3 です。 8 vCPU、64 GiB TiKV ノードの最大storage容量は 4096 GiB です。

過去のデータに基づくと、TiKV の平均圧縮率は約 40% です。

MySQL ダンプ ファイルのサイズが 20 TB で、TiKV 圧縮率が 40% であると仮定します。次に、データ量に応じて推奨される TiKV ノードの数を次のように計算できます。

`node num = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### 予想されるパフォーマンスに応じて TiKV ノード数を見積もる {#estimate-tikv-node-number-according-to-expected-performance}

TiDB のパフォーマンスと同様に、TiKV のパフォーマンスも TiKV ノードの数に応じて直線的に増加します。ただし、TiKV ノードの数が 8 を超えると、パフォーマンスの増加は線形比例よりわずかに小さくなります。追加の 8 ノードごとに、パフォーマンス偏差係数は約 5% になります。

例えば：

-   TiKV ノードが 9 個ある場合、性能偏差係数は約 5% となるため、TiKV の性能は単一の TiKV ノードの性能の約`9 * (1 - 5%) = 8.55`倍になります。
-   TiKV ノードが 18 個ある場合、性能偏差係数は約 10% となるため、TiKV の性能は単一の TiKV ノードの性能の`18 * (1 - 10%) = 16.2`倍となります。

TiKV ノードの指定されたレイテンシーでは、TiKV のパフォーマンスは読み取り/書き込み比率の違いによって異なります。

さまざまなワークロードにおける 8 vCPU、32 GiB TiKV ノードのパフォーマンスは次のとおりです。

| ワークロード | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
| ------ | ----------------- | ----------------- | ----------------- |
| 読む     | 28,000            | 14,000            | 7,000             |
| 混合     | 17,800            | 8,900             | 4,450             |
| 書く     | 14,500            | 7,250             | 3,625             |

TiKV ノードの数が 8 未満の場合、パフォーマンス偏差係数はほぼ 0% になるため、16 vCPU、64 GiB TiKV ノードのパフォーマンスは、8 vCPU、32 GiB TiKV ノードのパフォーマンスの約 2 倍になります。 TiKV ノードの数が 8 を超える場合は、必要なノードが少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、64 GiB TiKV ノードを選択することをお勧めします。

クラスターのサイズを計画するときは、次の式を使用して、ワークロード タイプ、全体的な期待パフォーマンス (QPS)、およびワークロード タイプに対応する単一 TiKV ノードのパフォーマンスに応じて TiKV ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node num = ceil(overall expected performance ÷ performance per node)`を計算して大まかなノード番号を取得し、次に対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスは 110,000 QPS、P95レイテンシーは約 100 ミリ秒、8 vCPU、32 GiB TiKV ノードを使用するとします。次に、上の表から 8 vCPU、32 GiB TiKV ノードの推定 TiKV パフォーマンス (これは`17,800` ) を取得し、次のように TiKV ノードのおおよその数を計算できます。

`node num = ceil(110,000 / 17,800 ) = 7`

7 は 8 より小さいため、7 ノードのパフォーマンス偏差係数は 0 です。推定される TiKV パフォーマンスは`7 * 17,800 * (1 - 0) = 124,600`で、これは予想される 110,000 QPS のパフォーマンスを満たすことができます。

したがって、期待されるパフォーマンスに応じて、7 つの TiKV ノード (8 vCPU、32 GiB) が推奨されます。

次に、データ量に基づいて計算された TiKV ノード数と、予想されるパフォーマンスに基づいて計算された数を比較し、大きい方を TiKV ノードの推奨数として採用します。

### TiKVノードstorage {#tikv-node-storage}

さまざまな TiKV vCPU でサポートされるノードstorageは次のとおりです。

| TiKV vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-------: | :----------: | :----------: | :--------------: |
|   4 vCPU  |    200 GiB   |   2048 GiB   |      500 GiB     |
|   8 vCPU  |    200 GiB   |   4096 GiB   |      500 GiB     |
|  16 vCPU  |    200 GiB   |   6144 GiB   |      500 GiB     |

> **注記：**
>
> クラスターの作成後に TiKV ノードのstorageを減らすことはできません。

## サイズTiFlash {#size-tiflash}

TiFlash は、 TiKV からのデータをリアルタイムで同期し、すぐに使用できるリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlashのノード番号、vCPU と RAM、storageを構成できます。

### TiFlash vCPU と RAM {#tiflash-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB

TiDB または TiKV の vCPU および RAM サイズが**4 vCPU、16 GiB**に設定されている場合、 TiFlash は使用できないことに注意してください。

### TiFlashノード番号 {#tiflash-node-number}

TiDB Cloud は、 TiFlashノードをリージョン内のさまざまなアベイラビリティ ゾーンに均等にデプロイします。本番環境での高可用性を実現するために、各TiDB Cloudクラスターに少なくとも 2 つのTiFlashノードを構成し、データの少なくとも 2 つのレプリカを作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノードstorageを1024 GiB に設定し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GiB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GiB) を設定した場合、必要なTiFlashノードの数は次のとおりです。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノードstorage {#tiflash-node-storage}

さまざまなTiFlash vCPU でサポートされるノードstorageは次のとおりです。

| TiFlash vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :----------: | :----------: | :----------: | :--------------: |
|    8 vCPU    |    200 GiB   |   2048 GiB   |      500 GiB     |
|    16 vCPU   |    200 GiB   |   2048 GiB   |      500 GiB     |

> **注記：**
>
> クラスターの作成後にTiFlashノードのstorageを減らすことはできません。
