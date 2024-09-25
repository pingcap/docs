---
title: Determine Your TiDB Size
summary: TiDB Cloudクラスターのサイズを決定する方法について説明します。
---

# TiDBのサイズを決定する {#determine-your-tidb-size}

このドキュメントでは、 TiDB Cloud Dedicated クラスターのサイズを決定する方法について説明します。

> **注記：**
>
> [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)クラスターのサイズを変更することはできません。

## サイズ TiDB {#size-tidb}

TiDB はコンピューティング専用であり、データを保存しません。水平方向にスケーラブルです。

TiDB のノード番号、vCPU、RAM を構成できます。

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
> -   TiDB のノード番号は 1 または 2 にのみ設定でき、TiKV のノード番号は 3 に固定されています。
> -   4 vCPU TiDB は 4 vCPU TiKV でのみ使用できます。
> -   TiFlashは利用できません。

### TiDBノード番号 {#tidb-node-number}

高可用性を確保するには、 TiDB Cloudクラスターごとに少なくとも 2 つの TiDB ノードを構成することをお勧めします。

一般的に、TiDB のパフォーマンスは TiDB ノードの数に応じて直線的に増加します。ただし、TiDB ノードの数が 8 を超えると、パフォーマンスの増加は直線的な比例よりわずかに小さくなります。ノードが 8 つ増えるごとに、パフォーマンス偏差係数は約 5% になります。

例えば：

-   TiDB ノードが 9 個ある場合、パフォーマンス偏差係数は約 5% なので、TiDB パフォーマンスは単一の TiDB ノードのパフォーマンスの約`9 * (1 - 5%) = 8.55`倍になります。
-   TiDB ノードが 16 個ある場合、パフォーマンス偏差係数は約 10% なので、TiDB パフォーマンスは単一の TiDB ノードの`16 * (1 - 10%) = 14.4`倍のパフォーマンスになります。

TiDB ノードの指定されたレイテンシーでは、読み取りと書き込みの比率に応じて TiDB のパフォーマンスが異なります。

さまざまなワークロードにおける 8 vCPU、16 GiB TiDB ノードのパフォーマンスは次のとおりです。

| 作業負荷 | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
| ---- | ----------------- | ----------------- | ----------------- |
| 読む   | 18,900            | 9,450             | 6,300             |
| 混合   | 15,500            | 7,750             | 5,200             |
| 書く   | 18,000            | 9,000             | 6,000             |

TiDB ノードの数が 8 未満の場合、パフォーマンス偏差係数はほぼ 0% であるため、16 vCPU、32 GiB TiDB ノードの TiDB パフォーマンスは、8 vCPU、16 GiB TiDB ノードの約 2 倍になります。TiDB ノードの数が 8 を超える場合は、必要なノード数が少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、32 GiB TiDB ノードを選択することをお勧めします。

クラスターのサイズを計画するときは、次の式を使用して、ワークロードの種類、全体的な予想パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiDB ノードのパフォーマンスに応じて、TiDB ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node num = ceil(overall expected performance ÷ performance per node)`計算して大まかなノード番号を取得し、対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスが 110,000 QPS で、P95レイテンシーが約 100 ミリ秒で、8 vCPU、16 GiB TiDB ノードを使用するとします。この場合、前の表から 8 vCPU、16 GiB TiDB ノードの推定 TiDB パフォーマンス ( `15,500` ) を取得し、次のようにして TiDB ノードの大まかな数を計算できます。

`node num = ceil(110,000 ÷ 15,500) = 8`

8 ノードのパフォーマンス偏差係数は約 5% なので、推定 TiDB パフォーマンスは`8 * 15,500 * (1 - 5%) = 117,800`となり、期待される 110,000 QPS のパフォーマンスを満たすことができます。

したがって、8 つの TiDB ノード (8 vCPU、16 GiB) が推奨されます。

## サイズ TiKV {#size-tikv}

TiKV はデータの保存を担当します。水平方向にスケーラブルです。

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
> -   TiDB のノード番号は 1 または 2 にのみ設定でき、TiKV のノード番号は 3 に固定されています。
> -   4 vCPU TiKV は 4 vCPU TiDB でのみ使用できます。
> -   TiFlashは利用できません。

### TiKVノード番号 {#tikv-node-number}

TiKV ノードの数は**少なくとも 1 セット (3 つの異なる使用可能ゾーン内の 3 つのノード)**である必要があります。

TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョン内のすべてのアベイラビリティ ゾーン (少なくとも 3 つ) に TiKV ノードを均等にデプロイします。一般的な 3 つのレプリカのセットアップでは、データはすべてのアベイラビリティ ゾーンの TiKV ノードに均等に分散され、各 TiKV ノードのディスクに保存されます。

> **注記：**
>
> TiDB クラスターをスケールすると、3 つのアベイラビリティーゾーンのノードが同時に増加または減少します。ニーズに応じて TiDB クラスターをスケールインまたはスケールアウトする方法については、 [TiDBクラスタのスケール](/tidb-cloud/scale-tidb-cluster.md)参照してください。

TiKV は主にデータstorageに使用されますが、TiKV ノードのパフォーマンスはワークロードによっても異なります。したがって、TiKV ノードの数を計画するときは、 [**データ量**](#estimate-tikv-node-number-according-to-data-volume)と[期待されるパフォーマンス](#estimate-tikv-node-number-according-to-expected-performance)両方に応じて見積もり、2 つの見積もりの​​うち大きい方を推奨ノード数とする必要があります。

#### データ量に応じてTiKVノード数を推定する {#estimate-tikv-node-number-according-to-data-volume}

次のように、データ量に応じて TiKV ノードの推奨数を計算できます。

`node num = ceil(size of your data * TiKV compression ratio * the number of replicas ÷ TiKV storage usage ratio ÷ one TiKV capacity ÷ 3) * 3`

一般的に、TiKVstorageの使用率は 80% 未満に保つことをお勧めします。TiDB TiDB Cloudのレプリカ数はデフォルトで 3 です。8 vCPU、64 GiB TiKV ノードの最大storage容量は 4096 GiB です。

過去のデータに基づくと、TiKV の平均圧縮率は約 40% です。

MySQL ダンプ ファイルのサイズが 20 TB で、TiKV 圧縮率が 40% であるとします。この場合、データ量に応じて、推奨される TiKV ノード数を次のように計算できます。

`node num = ceil(20 TB * 40% * 3 ÷ 0.8 ÷ 4096 GiB ÷ 3) * 3 = 9`

#### 予想されるパフォーマンスに応じてTiKVノード数を見積もる {#estimate-tikv-node-number-according-to-expected-performance}

TiDB のパフォーマンスと同様に、TiKV のパフォーマンスは TiKV ノードの数に応じて直線的に増加します。ただし、TiKV ノードの数が 8 を超えると、パフォーマンスの増加は直線的な比例よりもわずかに小さくなります。8 ノード追加するごとに、パフォーマンス偏差係数は約 5% になります。

例えば：

-   TiKV ノードが 9 個ある場合、パフォーマンス偏差係数は約 5% なので、TiKV パフォーマンスは単一の TiKV ノードのパフォーマンスの約`9 * (1 - 5%) = 8.55`倍になります。
-   TiKV ノードが 18 個ある場合、パフォーマンス偏差係数は約 10% なので、TiKV パフォーマンスは単一の TiKV ノードの`18 * (1 - 10%) = 16.2`倍のパフォーマンスになります。

TiKV ノードの指定されたレイテンシーでは、読み取りと書き込みの比率の違いによって TiKV のパフォーマンスが異なります。

さまざまなワークロードにおける 8 vCPU、32 GiB TiKV ノードのパフォーマンスは次のとおりです。

| 作業負荷 | QPS (P95 ≈ 100ms) | QPS (P99 ≈ 300ms) | QPS (P99 ≈ 100ms) |
| ---- | ----------------- | ----------------- | ----------------- |
| 読む   | 28,000            | 14,000            | 7,000             |
| 混合   | 17,800            | 8,900             | 4,450             |
| 書く   | 14,500            | 7,250             | 3,625             |

TiKV ノードの数が 8 未満の場合、パフォーマンス偏差係数はほぼ 0% であるため、16 vCPU、64 GiB TiKV ノードのパフォーマンスは、8 vCPU、32 GiB TiKV ノードの約 2 倍になります。TiKV ノードの数が 8 を超える場合は、必要なノード数が少なくなり、パフォーマンス偏差係数が小さくなるため、16 vCPU、64 GiB TiKV ノードを選択することをお勧めします。

クラスターのサイズを計画するときは、次の式を使用して、ワークロードの種類、全体的な予想パフォーマンス (QPS)、およびワークロードの種類に対応する単一の TiKV ノードのパフォーマンスに応じて、TiKV ノードの数を見積もることができます。

`node num = ceil(overall expected performance ÷ performance per node * (1 - performance deviation coefficient))`

式では、まず`node num = ceil(overall expected performance ÷ performance per node)`計算して大まかなノード番号を取得し、対応するパフォーマンス偏差係数を使用してノード番号の最終結果を取得する必要があります。

たとえば、混合ワークロードでの全体的な予想パフォーマンスが 110,000 QPS で、P95レイテンシーが約 100 ms で、8 vCPU、32 GiB TiKV ノードを使用するとします。この場合、前の表から 8 vCPU、32 GiB TiKV ノードの推定 TiKV パフォーマンス ( `17,800` ) を取得し、次のようにして TiKV ノードのおおよその数を計算できます。

`node num = ceil(110,000 / 17,800 ) = 7`

7 は 8 未満なので、7 ノードのパフォーマンス偏差係数は 0 です。推定 TiKV パフォーマンスは`7 * 17,800 * (1 - 0) = 124,600`であり、期待されるパフォーマンス 110,000 QPS を満たすことができます。

したがって、予想されるパフォーマンスに応じて、7 つの TiKV ノード (8 vCPU、32 GiB) が推奨されます。

次に、データ量に応じて計算された TiKV ノード数と、予想されるパフォーマンスに応じて計算された数を比較し、大きい方を TiKV ノードの推奨数とします。

### TiKV ノードstorage {#tikv-node-storage}

さまざまな TiKV vCPU でサポートされているノードstorageは次のとおりです。

| TiKV vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :-------: | :----------: | :----------: | :--------------: |
|  4 仮想CPU  |   200ギガバイト   |   2048ギガバイト  |     500ギガバイト     |
|  8 仮想CPU  |   200ギガバイト   |    4096ギバ    |     500ギガバイト     |
|  16 仮想CPU |   200ギガバイト   |    6144ギバ    |     500ギガバイト     |
|  32 仮想CPU |   200ギガバイト   |    6144ギバ    |     500ギガバイト     |

> **注記：**
>
> クラスターの作成後に TiKV ノードのstorageを減らすことはできません。

## サイズTiFlash {#size-tiflash}

TiFlash は、 TiKV からのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。水平方向に拡張可能です。

TiFlashのノード数、vCPU と RAM、storageを構成できます。

### TiFlash vCPU と RAM {#tiflash-vcpu-and-ram}

サポートされている vCPU と RAM のサイズは次のとおりです。

-   8 vCPU、64 GiB
-   16 vCPU、128 GiB
-   32 vCPU、128 GiB
-   32 vCPU、256 GiB

TiDB または TiKV の vCPU と RAM サイズが**4 vCPU、16 GiB**に設定されている場合、 TiFlashは使用できないことに注意してください。

### TiFlashノード番号 {#tiflash-node-number}

TiDB Cloud は、 TiFlashノードをリージョン内の異なるアベイラビリティ ゾーンに均等にデプロイします。本番環境で高可用性を確保するには、各TiDB Cloudクラスターに少なくとも 2 つのTiFlashノードを設定し、データのレプリカを少なくとも 2 つ作成することをお勧めします。

TiFlashノードの最小数は、特定のテーブルのTiFlashレプリカ数によって異なります。

TiFlashノードの最小数: `min((compressed size of table A * replicas for table A + compressed size of table B * replicas for table B) / size of each TiFlash capacity, max(replicas for table A, replicas for table B))`

たとえば、AWS 上の各TiFlashノードのノードstorageを1024 GiB に設定し、テーブル A に 2 つのレプリカ (圧縮サイズは 800 GiB)、テーブル B に 1 つのレプリカ (圧縮サイズは 100 GiB) を設定する場合、必要なTiFlashノードの数は次のようになります。

TiFlashノードの最小数: `min((800 GiB * 2 + 100 GiB * 1) / 1024 GiB, max(2, 1)) ≈ 2`

### TiFlashノードstorage {#tiflash-node-storage}

さまざまなTiFlash vCPU でサポートされているノードstorageは次のとおりです。

| TiFlash vCPU | 最小ノードstorage | 最大ノードstorage | デフォルトのノードstorage |
| :----------: | :----------: | :----------: | :--------------: |
|    8 仮想CPU   |   200ギガバイト   |   2048ギガバイト  |     500ギガバイト     |
|   16 仮想CPU   |   200ギガバイト   |    4096ギバ    |     500ギガバイト     |
|   32 仮想CPU   |   200ギガバイト   |    4096ギバ    |     500ギガバイト     |

> **注記：**
>
> クラスターの作成後にTiFlashノードのstorageを減らすことはできません。
