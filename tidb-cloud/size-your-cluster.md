---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDB サイズを決定する {#determine-your-tidb-size}

このドキュメントでは、Dedicated Tierクラスターのサイズを決定する方法について説明します。

> **ノート：**
>
> [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターのサイズは変更できません。

## サイズ TiDB {#size-tidb}

TiDB はコンピューティング専用であり、データは保存されません。水平方向にスケーラブルです。

TiDB のノード サイズとノード数の両方を構成できます。

さまざまなクラスター規模のパフォーマンス テストの結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiDB ノードのサイズ {#tidb-node-size}

サポートされているノード サイズには次のものがあります。

-   2 vCPU、8 GiB (ベータ版)
-   4 vCPU、16 GiB
-   8 vCPU、16 GiB
-   16 vCPU、32 GiB

> **ノート：**
>
> TiDB のノード サイズが**2 vCPU、8 GiB (ベータ版)**または**4 vCPU、16 GiB**に設定されている場合は、次の制限事項に注意してください。
>
> -   TiDB のノード数は 1 または 2 のみに設定でき、TiKV のノード数は 3 に固定されます。
> -   2 vCPU TiDB は 2 vCPU TiKV でのみ使用できます。 4 vCPU TiDB は 4 vCPU TiKV でのみ使用できます。
> -   TiFlashは使用できません。

### TiDB ノードの数 {#tidb-node-quantity}

高可用性を実現するには、 TiDB Cloudクラスターごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

## サイズTiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

TiKV のノード サイズ、ノード数、ノードstorageを構成できます。

さまざまなクラスター規模のパフォーマンス テストの結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

### TiKV ノードのサイズ {#tikv-node-size}

サポートされているノード サイズには次のものがあります。

-   2 vCPU、8 GiB (ベータ版)
-   4 vCPU、16 GiB
-   8 vCPU、32 GiB
-   8 vCPU、64 GiB
-   16 vCPU、64 GiB

> **ノート：**
>
> TiKV のノード サイズが**2 vCPU、8 GiB (ベータ版)**または**4 vCPU、16 GiB**に設定されている場合は、次の制限事項に注意してください。
>
> -   TiDB のノード数は 1 または 2 のみに設定でき、TiKV のノード数は 3 に固定されます。
> -   2 vCPU TiKV は 2 vCPU TiDB でのみ使用できます。 4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは使用できません。

### TiKV ノードの数量 {#tikv-node-quantity}

TiKV ノードの数**は少なくとも 1 セット (3 つの異なる利用可能なゾーンに 3 つのノード)**である必要があります。

TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョン内のすべての可用性ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。一般的な 3 レプリカのセットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

> **ノート：**
>
> TiDB クラスターをスケールすると、3 つのアベイラビリティ ゾーン内のノードが同時に増加または減少します。ニーズに基づいて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタを拡張する](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

推奨される TiKV ノード数: `ceil(compressed size of your data ÷ TiKV storage usage ratio ÷ one TiKV capacity) × the number of replicas`

MySQL ダンプ ファイルのサイズが 5 TB で、TiDB 圧縮率が 40% であると仮定すると、必要なstorageは2048 GiB になります。

一般に、TiKVstorageの使用率が 80% を超えることは推奨されません。

たとえば、AWS 上の各 TiKV ノードのノードstorageを1024 GiB に構成する場合、必要な TiKV ノードの数は次のとおりです。

TiKV ノードの最小数: `ceil(2048 ÷ 0.8 ÷ 1024) × 3 = 9`

### TiKVノードstorage {#tikv-node-storage}

さまざまな TiKV ノード サイズでサポートされるノードstorageは次のとおりです。

|  ノードサイズ | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-----: | :----------: | :----------: | :--------------: |
|  2 vCPU |    200 GiB   |    500 GiB   |      200 GiB     |
|  4 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |
|  8 vCPU |    200 GiB   |   4096 GiB   |      500 GiB     |
| 16 vCPU |    200 GiB   |   4096 GiB   |      500 GiB     |

> **ノート：**
>
> クラスターの作成後に TiKV ノードのstorageを減らすことはできません。

## サイズTiFlash {#size-tiflash}

TiFlash は、 TiKV からのデータをリアルタイムで同期し、すぐに使用できるリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlashのノード サイズ、ノード数、ノードstorageを構成できます。

### TiFlashノードのサイズ {#tiflash-node-size}

サポートされているノード サイズには次のものがあります。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB

TiDB または TiKV の vCPU サイズが**2 vCPU、8 GiB (ベータ)**または**4 vCPU、16 GiB**に設定されている場合、 TiFlash は利用できないことに注意してください。

### TiFlashノードの数量 {#tiflash-node-quantity}

TiDB Cloud は、 TiFlashノードをリージョン内のさまざまなアベイラビリティ ゾーンに均等にデプロイします。本番環境での高可用性を実現するために、各TiDB Cloudクラスターに少なくとも 2 つのTiFlashノードを構成し、データの少なくとも 2 つのレプリカを作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノードstorageを1024 GiB に設定し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GiB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GiB) を設定した場合、必要なTiFlashノードの数は次のとおりです。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノードstorage {#tiflash-node-storage}

さまざまなTiFlashノード サイズでサポートされるノードstorageは次のとおりです。

|  ノードサイズ | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-----: | :----------: | :----------: | :--------------: |
|  8 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |
| 16 vCPU |    200 GiB   |   2048 GiB   |      500 GiB     |

> **ノート：**
>
> クラスターの作成後にTiFlashノードのstorageを減らすことはできません。
