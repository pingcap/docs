---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDB のサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、 Dedicated Tierクラスターのサイズを決定する方法について説明します。

> **ノート：**
>
> [サーバーレス層](/tidb-cloud/select-cluster-tier.md#serverless-tier)クラスターのサイズは変更できません。

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

## サイズ TiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

TiKV のノード サイズ、ノード数、およびノード ストレージを構成できます。

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

TiKV ノードの数は**、少なくとも 1 セット (3 つの異なる利用可能なゾーンに 3 つのノード) で**ある必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。典型的な 3 レプリカ セットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

> **ノート：**
>
> TiDB クラスターをスケーリングすると、3 つのアベイラビリティーゾーンのノードが同時に増減します。ニーズに基づいて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

TiKV ノードの推奨数: `ceil(compressed size of your data ÷ TiKV storage usage ratio ÷ one TiKV capacity) × the number of replicas`

MySQL ダンプ ファイルのサイズが 5 TB で、TiDB の圧縮率が 40% であると仮定すると、必要なストレージは 2048 GiB です。

一般的に、TiKV ストレージの使用率が 80% を超えることは推奨されません。

たとえば、AWS 上の各 TiKV ノードのノード ストレージを 1024 GiB として構成する場合、必要な TiKV ノードの数は次のようになります。

TiKV ノードの最小数: `ceil(2048 ÷ 0.8 ÷ 1024) × 3 = 9`

### TiKV ノード ストレージ {#tikv-node-storage}

さまざまな TiKV ノード サイズでサポートされているノード ストレージは次のとおりです。

|  ノードサイズ | 最小ノード ストレージ | 最大ノード ストレージ | デフォルトのノード ストレージ |
| :-----: | :---------: | :---------: | :-------------: |
|  2 vCPU |   200 GiB   |   500 GiB   |     200 GiB     |
|  4 vCPU |   200 GiB   |   2048 GiB  |     500 GiB     |
|  8 vCPU |   200 GiB   |   4096 GiB  |     500 GiB     |
| 16 vCPU |   200 GiB   |   4096 GiB  |     500 GiB     |

> **ノート：**
>
> クラスターの作成後に TiKV ノード ストレージを減らすことはできません。

## サイズTiFlash {#size-tiflash}

TiFlashは TiKV からのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlashのノード サイズ、ノード数、およびノード ストレージを設定できます。

### TiFlashノードサイズ {#tiflash-node-size}

サポートされているノード サイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB

TiDB または TiKV の vCPU サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合、 TiFlashは使用できないことに注意してください。

### TiFlashノード数 {#tiflash-node-quantity}

TiDB Cloudは、リージョン内の異なるアベイラビリティ ゾーンにTiFlashノードを均等にデプロイします。各TiDB Cloudクラスターで少なくとも 2 つのTiFlashノードを構成し、実稼働環境での高可用性のためにデータの少なくとも 2 つのレプリカを作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノード ストレージを 1024 GiB として構成し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GiB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GiB) を設定すると、必要なTiFlashノードの数は次のとおりです。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノード ストレージ {#tiflash-node-storage}

さまざまなTiFlashノード サイズでサポートされているノード ストレージは次のとおりです。

|  ノードサイズ | 最小ノード ストレージ | 最大ノード ストレージ | デフォルトのノード ストレージ |
| :-----: | :---------: | :---------: | :-------------: |
|  8 vCPU |   200 GiB   |   2048 GiB  |     500 GiB     |
| 16 vCPU |   200 GiB   |   2048 GiB  |     500 GiB     |

> **ノート：**
>
> クラスターの作成後にTiFlashノード ストレージを減らすことはできません。
