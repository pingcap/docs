---
title: Determine Your TiDB Size
summary: Learn how to determine the size of your TiDB Cloud cluster.
---

# TiDBサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、TiDBクラスタのサイズを決定する方法について説明します。

## サイズTiDB {#size-tidb}

TiDBはコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。

TiDBのvCPUサイズとノード数の両方を構成できます。

### TiDBvCPUのサイズ {#tidb-vcpus-size}

サポートされているvCPUサイズには、4つのvCPU（ベータ）、8つのvCPU、および16のvCPUが含まれます。

> **ノート：**
>
> TiDBのvCPUサイズが**4vCPU（ベータ）**に設定されている場合は、次の制限に注意してください。
>
> -   TiDBのノード数は1または2にのみ設定でき、TiKVのノード数は3に固定されています。
> -   TiDBは、4vCPUのTiKVでのみ使用できます。
> -   TiFlash<sup>ベータ</sup>はサポートされていません。

### TiDBノードの数量 {#tidb-node-quantity}

高可用性を実現するには、TiDBクラウドクラスタごとに少なくとも2つのTiDBノードを構成することをお勧めします。

## サイズTiKV {#size-tikv}

TiKVはデータの保存を担当します。水平方向にスケーラブルです。

TiKVのvCPUサイズ、ノード数、およびストレージサイズを構成できます。

### TiKVvCPUのサイズ {#tikv-vcpus-size}

サポートされているサイズには、4 vCPU（ベータ）、8 vCPU、および16vCPUが含まれます。

> **ノート：**
>
> TiKVのvCPUサイズが**4vCPU（ベータ）**に設定されている場合は、次の制限に注意してください。
>
> -   TiDBのノード数は1または2にのみ設定でき、TiKVのノード数は3に固定されています。
> -   TiKVは、4vCPUのTiDBでのみ使用できます。
> -   TiFlash<sup>ベータ</sup>はサポートされていません。

### TiKVノードの数量 {#tikv-node-quantity}

TiKVノードの数は**少なくとも1セット（3つの異なる使用可能ゾーンに3つのノード）で**ある必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョンのすべてのアベイラビリティーゾーン（少なくとも3つ）にTiKVノードを均等にデプロイします。通常の3レプリカのセットアップでは、データはすべてのアベイラビリティーゾーンのTiKVノードに均等に分散され、各TiKVノードのディスクに保持されます。

> **ノート：**
>
> TiDBクラスタをスケーリングすると、3つのアベイラビリティーゾーンのノードが同時に増減します。ニーズに基づいてTiDBクラスタをスケールインまたはスケールアウトする方法については、 [TiDBクラスターをスケーリングする](/tidb-cloud/scale-tidb-cluster.md)を参照してください。

TiKVノードの最小数： `ceil(compressed size of your data ÷ one TiKV capacity) × the number of replicas`

MySQLダンプファイルのサイズが5TBで、TiDB圧縮率が70％であるとすると、必要なストレージは3584GBです。

たとえば、AWSの各TiKVノードのストレージサイズを1024 GBに設定した場合、必要なTiKVノードの数は次のようになります。

TiKVノードの最小数： `ceil(3584 ÷ 1024) × 3 = 12`

### TiKVストレージサイズ {#tikv-storage-size}

TiKVストレージサイズは、クラスタを作成または復元する場合にのみ構成できます。

## サイズTiFlash<sup>ベータ</sup> {#size-tiflash-sup-beta-sup}

TiFlash<sup>ベータ版</sup>は、TiKVからのデータをリアルタイムで同期し、箱から出してすぐにリアルタイム分析ワークロードをサポートします。水平方向にスケーラブルです。

TiFlash<sup>ベータ版</sup>のvCPUサイズ、ノード数、およびストレージサイズを構成できます。

### TiFlash<sup>ベータ</sup>vCPUのサイズ {#tiflash-sup-beta-sup-vcpus-size}

サポートされているvCPUのサイズには、8個のvCPUと16個のvCPUが含まれます。

TiDBまたはTiKVのvCPUサイズが**4vCPU（ベータ）**に設定されている場合、TiFlash<sup>ベータ</sup>はサポートされません。

### TiFlash<sup>ベータ</sup>ノードの数量 {#tiflash-sup-beta-sup-node-quantity}

TiDB Cloudは、TiFlash<sup>ベータ</sup>ノードをリージョン内のさまざまなアベイラビリティーゾーンに均等にデプロイします。各TiDBクラウドクラスタに少なくとも2つのTiFlash<sup>ベータ</sup>ノードを構成し、実稼働環境で高可用性を実現するためにデータのレプリカを少なくとも2つ作成することをお勧めします。

TiFlash<sup>ベータ</sup>ノードの最小数は、特定のテーブルのTiFlash<sup>ベータ</sup>レプリカ数によって異なります。

TiFlash<sup>ベータ</sup>ノードの最小数： `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWSの各TiFlash<sup>ベータ</sup>ノードのストレージサイズを1024 GBに設定し、テーブルAに2つのレプリカ（圧縮サイズは800 GB）、テーブルBに1つのレプリカ（圧縮サイズは100 GB）を設定すると、その場合、必要なTiFlash<sup>ベータ</sup>ノードの数は次のとおりです。

TiFlash<sup>ベータ</sup>ノードの最小数： `min((800 GB * 2 + 100 GB * 1) / 1024 GB, max(2, 1)) ≈ 2`

### TiFlash<sup>ベータ</sup>ストレージサイズ {#tiflash-sup-beta-sup-storage-size}

クラスタを作成または復元する場合にのみ、TiFlash<sup>ベータ</sup>ストレージサイズを構成できます。
