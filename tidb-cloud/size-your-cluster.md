---
title: Determine Your TiDB Size
summary: TiDB Cloudクラスターのサイズを決定する方法を学びます。
---

# TiDBのサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、 TiDB Cloud Dedicated クラスターのサイズを決定する方法について説明します。

> **注記：**
>
> [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのサイズを変更することはできません。

## サイズ TiDB {#size-tidb}

TiDBはコンピューティング専用であり、データの保存は行いません。水平方向にスケーラブルです。

TiDB のノード数、vCPU、RAM を構成できます。

さまざまなクラスター規模のパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)参照してください。

### TiDB vCPU と RAM {#tidb-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

|      標準サイズ     |      大容量メモリ     |
| :------------: | :-------------: |
|  4 vCPU、16 GiB |       該当なし      |
|  8 vCPU、16 GiB |  8 vCPU、32 GiB  |
| 16 vCPU、32 GiB |  16 vCPU、64 GiB |
| 32 vCPU、64 GiB | 32 vCPU、128 GiB |

> **注記：**
>
> **32 vCPU、128 GiB**サイズの TiDB を使用するには、 [TiDB Cloudサポート](/tidb-cloud/tidb-cloud-support.md)お問い合わせください。
>
> TiDB の vCPU と RAM サイズが**4 vCPU、16 GiB**に設定されている場合、次の制限に注意してください。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用できます。
> -   TiFlashは利用できません。

### TiDBノード数 {#tidb-node-count}

高可用性を確保するには、 TiDB Cloudクラスターごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

一般的に、TiDBのパフォーマンスはTiDBノード数に比例して増加します。しかし、TiDBノード数が8を超えると、パフォーマンスの向上は線形比例からわずかに減少します。ノード数が8増えるごとに、パフォーマンスの偏差係数は約5%になります。

例えば：

-   TiDB ノードが 9 台の場合、パフォーマンス偏差係数は約 5% となるため、TiDB パフォーマンスは単一の TiDB ノードの約`9 * (1 - 5%) = 8.55`倍の性能になります。
-   TiDB ノードが 16 個ある場合、パフォーマンス偏差係数は約 10% なので、TiDB パフォーマンスは単一の TiDB ノードの`16 * (1 - 10%) = 14.4`倍のパフォーマンスになります。

TiDB ノードの指定されたレイテンシーでは、TiDB のパフォーマンスは読み取り/書き込み比率によって異なります。

さまざまなワークロードにおける 8 vCPU、16 GiB TiDB ノードのパフォーマンスは次のとおりです。

| 作業負荷 | QPS（P95 ≈ 100ms） | QPS（P99 ≈ 300ms） | QPS（P99 ≈ 100ms） |
| ---- | ---------------- | ---------------- | ---------------- |
| 読む   | 18,900           | 9,450            | 6,300            |
| 混合   | 15,500           | 7,750            | 5,200            |
| 書く   | 18,000           | 9,000            | 6,000            |

TiDBノード数が8未満の場合、パフォーマンス偏差係数はほぼ0%であるため、16 vCPU、32 GiBのTiDBノードのTiDBパフォーマンスは、8 vCPU、16 GiBのTiDBノードの約2倍になります。TiDBノード数が8を超える場合は、必要なノード数が少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、32 GiBのTiDBノードを選択することをお勧めします。

クラスターのサイズを計画する際には、次の式を使用して、ワークロードの種類、全体的な予想パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiDB ノードのパフォーマンスに応じて、TiDB ノードの数を見積もることができます。

`node count = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node count = ceil(overall expected performance ÷ performance per node)`計算して大まかなノード数を取得し、対応するパフォーマンス偏差係数を使用してノード数の最終結果を取得する必要があります。

例えば、混合ワークロードにおける全体的な期待パフォーマンスが 110,000 QPS、P95レイテンシーが約 100 ミリ秒で、8 vCPU、16 GiB の TiDB ノードを使用したいとします。この場合、前述の表から 8 vCPU、16 GiB の TiDB ノードの推定 TiDB パフォーマンス（ `15,500` ）を取得し、以下のように TiDB ノードの大まかな数を計算できます。

`node count = ceil(110,000 ÷ 15,500) = 8`

8 ノードのパフォーマンス偏差係数は約 5% なので、推定 TiDB パフォーマンスは`8 * 15,500 * (1 - 5%) = 117,800`となり、期待される 110,000 QPS のパフォーマンスを満たすことができます。

したがって、8 つの TiDB ノード (8 vCPU、16 GiB) が推奨されます。

## サイズ TiKV {#size-tikv}

TiKVはデータの保存を担当し、水平方向に拡張可能です。

TiKV のノード数、vCPU と RAM、storageを構成できます。

さまざまなクラスター規模のパフォーマンス テスト結果については、 [TiDB Cloudパフォーマンス リファレンス](/tidb-cloud/tidb-cloud-performance-reference.md)参照してください。

### TiKV vCPU と RAM {#tikv-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

|      標準サイズ      |     大容量メモリ    |
| :-------------: | :-----------: |
|  4 vCPU、16 GiB  |      該当なし     |
|  8 vCPU、32 GiB  | 8 vCPU、64 GiB |
|  16 vCPU、64 GiB |      近日公開     |
| 32 vCPU、128 GiB |      該当なし     |

> **注記：**
>
> TiKV の vCPU と RAM サイズが**4 vCPU、16 GiB**に設定されている場合、次の制限に注意してください。
>
> -   TiDB のノード数は 1 または 2 にのみ設定でき、TiKV のノード数は 3 に固定されています。
> -   4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは利用できません。

### TiKVノード数 {#tikv-node-count}

TiKV ノードの数は**少なくとも 1 セット (3 つの異なる利用可能ゾーン内の 3 つのノード) で**ある必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティゾーン（少なくとも3つ）にTiKVノードを均等にデプロイします。典型的な3レプリカ構成では、データはすべてのアベイラビリティゾーンのTiKVノードに均等に分散され、各TiKVノードのディスクに永続化されます。

> **注記：**
>
> TiDB クラスターをスケールすると、3 つのアベイラビリティゾーンのノードが同時に増減します。ニーズに応じて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)参照してください。

TiKVは主にデータstorageに使用されますが、TiKVノードのパフォーマンスはワークロードによって異なります。そのため、TiKVノードの数を計画する際には、 [**データ量**](#estimate-tikv-node-count-according-to-data-volume)と[期待されるパフォーマンス](#estimate-tikv-node-count-according-to-expected-performance)両方に基づいて見積もり、そのうち大きい方の見積もりを推奨ノード数とする必要があります。

#### データ量に応じてTiKVノード数を見積もる {#estimate-tikv-node-count-according-to-data-volume}

次のように、データ量に応じて TiKV ノードの推奨数を計算できます。

`node count = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

一般的に、TiKVstorageの使用率は80%未満に抑えることが推奨されます。TiDB TiDB Cloudのレプリカ数はデフォルトで3です。8 vCPU、64 GiBのTiKVノードの最大storage容量は4096 GiBです。

過去のデータに基づくと、TiKV の平均圧縮率は約 40% です。

MySQLダンプファイルのサイズが20TBで、TiKVの圧縮率が40%だとします。この場合、データ量に応じて推奨されるTiKVノード数は以下のように計算できます。

`node count = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### 予想されるパフォーマンスに応じて TiKV ノード数を見積もる {#estimate-tikv-node-count-according-to-expected-performance}

TiDBのパフォーマンスと同様に、TiKVのパフォーマンスはTiKVノード数に比例して直線的に増加します。ただし、TiKVノード数が8を超えると、パフォーマンスの向上は直線的な比例関係からわずかに減少します。ノード数が8増えるごとに、パフォーマンスの偏差係数は約5%になります。

例えば：

-   TiKV ノードが 9 個ある場合、パフォーマンス偏差係数は約 5% なので、TiKV パフォーマンスは単一の TiKV ノードのパフォーマンスの約`9 * (1 - 5%) = 8.55`倍になります。
-   TiKV ノードが 18 個ある場合、パフォーマンス偏差係数は約 10% なので、TiKV パフォーマンスは単一の TiKV ノードの`18 * (1 - 10%) = 16.2`倍のパフォーマンスになります。

TiKV ノードの指定されたレイテンシーでは、TiKV のパフォーマンスは読み取りと書き込みの比率によって異なります。

さまざまなワークロードにおける 8 vCPU、32 GiB TiKV ノードのパフォーマンスは次のとおりです。

| 作業負荷 | QPS（P95 ≈ 100ms） | QPS（P99 ≈ 300ms） | QPS（P99 ≈ 100ms） |
| ---- | ---------------- | ---------------- | ---------------- |
| 読む   | 2万8000           | 14,000           | 7,000            |
| 混合   | 17,800           | 8,900            | 4,450            |
| 書く   | 14,500           | 7,250            | 3,625            |

TiKVノード数が8未満の場合、パフォーマンス偏差係数はほぼ0%であるため、16 vCPU、64 GiBのTiKVノードのパフォーマンスは、8 vCPU、32 GiBのTiKVノードの約2倍になります。TiKVノード数が8を超える場合は、必要なノード数が少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、64 GiBのTiKVノードを選択することをお勧めします。

クラスターのサイズを計画するときは、次の式を使用して、ワークロードの種類、全体的な予想パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiKV ノードのパフォーマンスに応じて、TiKV ノードの数を見積もることができます。

`node count = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node count = ceil(overall expected performance ÷ performance per node)`計算して大まかなノード数を取得し、対応するパフォーマンス偏差係数を使用してノード数の最終結果を取得する必要があります。

例えば、混合ワークロードにおける全体的な期待パフォーマンスが 110,000 QPS、P95レイテンシーが約 100 ミリ秒で、8 vCPU、32 GiB TiKV ノードを使用したいとします。この場合、前述の表から 8 vCPU、32 GiB TiKV ノードの推定 TiKV パフォーマンス（ `17,800` ）を取得し、TiKV ノードの大まかな数を以下のように計算します。

`node count = ceil(110,000 / 17,800 ) = 7`

7 は 8 未満なので、7 ノードのパフォーマンス偏差係数は 0 です。推定 TiKV パフォーマンスは`7 * 17,800 * (1 - 0) = 124,600`であり、期待される 110,000 QPS のパフォーマンスを満たすことができます。

したがって、期待されるパフォーマンスに応じて、7 つの TiKV ノード (8 vCPU、32 GiB) が推奨されます。

次に、データ量に応じて計算された TiKV ノード数と、予想されるパフォーマンスに応じて計算された数を比較し、大きい方を TiKV ノードの推奨数とします。

### TiKVノードのstorageサイズ {#tikv-node-storage-size}

さまざまな TiKV vCPU でサポートされているノードstorageサイズは次のとおりです。

| TiKV vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-------: | :----------: | :----------: | :--------------: |
|  4 仮想CPU  |   200ギガバイト   |   2048ギガバイト  |     500ギガバイト     |
|  8 仮想CPU  |   200ギガバイト   |   4096ギガバイト  |     500ギガバイト     |
|  16 仮想CPU |   200ギガバイト   |   6144ギガバイト  |     500ギガバイト     |
|  32 仮想CPU |   200ギガバイト   |   6144ギガバイト  |     500ギガバイト     |

> **注記：**
>
> クラスターの作成後に TiKV ノードのstorageサイズを減らすことはできません。

### TiKVノードのstorageタイプ {#tikv-node-storage-types}

TiDB Cloud は、 AWS でホストされる[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して次の TiKVstorageタイプを提供します。

-   [基本的なstorage](#basic-storage)
-   [標準storage](#standard-storage)
-   [パフォーマンスとプラスstorage](#performance-and-plus-storage)

#### 基本的なstorage {#basic-storage}

ベーシックstorageは、スタンダードstorageよりもパフォーマンスが低い汎用storageタイプです。

ベーシックstorageタイプは、AWS でホストされている次のクラスターに自動的に適用されます。

-   2025 年 4 月 1 日より前に作成された既存のクラスター。
-   v7.5.5、v8.1.2、または v8.5.0 より前のバージョンの TiDB で作成された新しいクラスター。

#### 標準storage {#standard-storage}

スタンダードstorageは、パフォーマンスとコスト効率のバランスが取れており、ほとんどのワークロードに最適です。ベーシックstorageと比較して、 Raftログ用に十分なディスクリソースを確保することで、より優れたパフォーマンスを提供します。これにより、 Raft I/OがデータディスクI/Oに与える影響が軽減され、TiKVの読み取りおよび書き込みパフォーマンスが向上します。

標準storageタイプは、AWS でホストされ、TiDB バージョン v7.5.5、v8.1.2、v8.5.0 以降で作成された新しいクラスターに自動的に適用されます。

#### パフォーマンスとプラスstorage {#performance-and-plus-storage}

パフォーマンスストレージとプラスstorageは、より高いパフォーマンスと安定性を提供し、これらの拡張機能を反映した価格設定となっています。現在、これらの2つのstorageタイプは、AWSにデプロイされたクラスターに対してのみリクエストに応じて利用可能です。パフォーマンスストレージまたはプラスstorageをリクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポート**をリクエスト」をクリックします。次に、 **「説明」**フィールドに「TiKVstorageタイプを申請」と入力し、 **「送信」を**クリックします。

## サイズTiFlash {#size-tiflash}

TiFlashはTiKVからのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。水平方向に拡張可能です。

TiFlashのノード数、vCPU と RAM、storageを構成できます。

### TiFlash vCPUとRAM {#tiflash-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB
-   32 vCPU、128 GiB
-   32 vCPU、256 GiB

TiDB または TiKV の vCPU と RAM サイズが**4 vCPU、16 GiB**に設定されている場合、 TiFlash は使用できません。

### TiFlashノード数 {#tiflash-node-count}

TiDB Cloudは、リージョン内の異なるアベイラビリティゾーンにTiFlashノードを均等に展開します。本番環境での高可用性を確保するため、各TiDB Cloudクラスターに少なくとも2つのTiFlashノードを設定し、データのレプリカを少なくとも2つ作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノードstorageを 1024 GiB に設定し、テーブル A にレプリカを 2 つ (圧縮サイズは 800 GiB)、テーブル B にレプリカを 1 つ (圧縮サイズは 100 GiB) 設定した場合、必要なTiFlashノードの数は次のようになります。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノードstorage {#tiflash-node-storage}

さまざまなTiFlash vCPU でサポートされているノードstorageは次のとおりです。

| TiFlash vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :----------: | :----------: | :----------: | :--------------: |
|    8 仮想CPU   |   200ギガバイト   |   4096ギガバイト  |     500ギガバイト     |
|   16 仮想CPU   |   200ギガバイト   |   4096ギガバイト  |     500ギガバイト     |
|   32 仮想CPU   |   200ギガバイト   |  8192 ギガバイト  |     500ギガバイト     |

> **注記：**
>
> クラスターの作成後にTiFlashノードのstorageを減らすことはできません。

### TiFlashノードのstorageタイプ {#tiflash-node-storage-types}

TiDB Cloud は、 AWS でホストされる[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)クラスターに対して次のTiFlashstorageタイプを提供します。

-   [基本的なstorage](#basic-storage-1)
-   [プラスstorage](#plus-storage)

#### 基本的なstorage {#basic-storage}

ベーシックstorageは、パフォーマンスとコスト効率のバランスが取れており、ほとんどのワークロードに最適です。

#### プラスstorage {#plus-storage}

Plusstorageは、より高いパフォーマンスと安定性を提供し、これらの拡張機能を反映した価格設定となっています。現在、このstorageタイプはAWSにデプロイされたクラスターに対してのみ、リクエストに応じて利用可能です。リクエストするには、 [TiDB Cloudコンソール](https://tidbcloud.com)の右下にある**「？」**をクリックし、 **「サポートをリクエスト」**をクリックしてください。次に、「**説明」**欄に「 TiFlashstorageタイプを申請」と入力し、 **「送信」を**クリックしてください。
