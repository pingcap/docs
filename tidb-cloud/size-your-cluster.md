---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDB のサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、Dedicated Tierクラスタのサイズを決定する方法について説明します。

> **ノート：**
>
> [開発者層クラスタ](/tidb-cloud/select-cluster-tier.md#developer-tier)にはデフォルトのクラスタサイズが付属しており、変更することはできません。

## サイズ TiDB {#size-tidb}

TiDB はコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。

TiDB のノード サイズとノード数の両方を構成できます。

さまざまなクラスタスケールのパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

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
> -   TiFlash は利用できません。

### TiDB ノード数 {#tidb-node-quantity}

高可用性のために、 TiDB Cloudクラスタごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

## サイズ TiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

TiKV のノード サイズ、ノード数、およびノード ストレージを構成できます。

さまざまなクラスタスケールのパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)を参照してください。

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
> -   TiFlash は利用できません。

### TiKV ノード数 {#tikv-node-quantity}

TiKV ノードの数は**、少なくとも 1 セット (3 つの異なる利用可能なゾーンに 3 つのノード) で**ある必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。典型的な 3 レプリカ セットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノード間で均等に分散され、各 TiKV ノードのディスクに永続化されます。

> **ノート：**
>
> TiDBクラスタをスケーリングすると、3 つのアベイラビリティーゾーンのノードが同時に増減します。ニーズに基づいて TiDBクラスタをスケールインまたはスケールアウトする方法については、 [TiDB クラスターをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

TiKV ノードの最小数: `ceil(compressed size of your data ÷ one TiKV capacity) × the number of replicas`

MySQL ダンプ ファイルのサイズが 5 TB で、TiDB の圧縮率が 70% であると仮定すると、必要なストレージは 3584 GB です。

たとえば、AWS 上の各 TiKV ノードのノード ストレージを 1024 GB として構成する場合、必要な TiKV ノードの数は次のようになります。

TiKV ノードの最小数: `ceil(3584 ÷ 1024) × 3 = 12`

### TiKV ノード ストレージ {#tikv-node-storage}

-   8 vCPU または 16 vCPU の各 TiKV ノードは、最大 4 TiB のストレージ容量をサポートします。
-   各 4 vCPU TiKV ノードは、最大 2 TiB のストレージ容量をサポートします。
-   各 2 vCPU TiKV ノードは、最大 500 GiB のストレージ容量をサポートします。

> **ノート：**
>
> クラスタの作成後に TiKV ノード ストレージを減らすことはできません。

## サイズ TiFlash {#size-tiflash}

TiFlash は TiKV からのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlash のノード サイズ、ノード数、およびノード ストレージを構成できます。

### TiFlash ノードサイズ {#tiflash-node-size}

サポートされているノード サイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB

TiDB または TiKV の vCPU サイズが**2 vCPU、8 GiB (ベータ)**または<strong>4 vCPU、16 GiB</strong>に設定されている場合、TiFlash は使用できないことに注意してください。

### TiFlash ノード数 {#tiflash-node-quantity}

TiDB Cloudは、リージョン内の異なるアベイラビリティ ゾーンに TiFlash ノードを均等にデプロイします。各TiDB Cloudクラスタで少なくとも 2 つの TiFlash ノードを構成し、実稼働環境での高可用性のためにデータの少なくとも 2 つのレプリカを作成することをお勧めします。

TiFlash ノードの最小数は、特定のテーブルの TiFlash レプリカ数によって異なります。

TiFlash ノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各 TiFlash ノードのノード ストレージを 1024 GB に設定し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GB) を設定すると、必要な TiFlash ノードの数は次のとおりです。

TiFlash ノードの最小数: `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`

### TiFlash ノード ストレージ {#tiflash-node-storage}

各 TiFlash ノードは、最大 2 TiB のストレージ容量をサポートします。

> **ノート：**
>
> クラスタの作成後に TiFlash ノード ストレージを減らすことはできません。
