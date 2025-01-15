---
title: Scalability
summary: TiDB Cloudのスケーラビリティの概念について学習します。
---

# スケーラビリティ {#scalability}

TiDB Cloud Dedicated を使用すると、データ量やワークロードの変化に合わせてコンピューティング リソースとstorageリソースを個別に調整できます。TiDB TiDB Cloud Dedicated は、サービスを中断することなくスケーリングできます。この柔軟性により、組織は高いパフォーマンスと可用性を維持しながらインフラストラクチャ コストを最適化できます。

> **注記：**
>
> [TiDB Cloudサーバーレス](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 、アプリケーションのワークロードの変化に基づいて自動的にスケーリングされます。ただし、 TiDB Cloud Serverless クラスターを手動でスケーリングすることはできません。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターのサイズを決定する方法については、 [TiDBのサイズを決定する](/tidb-cloud/size-your-cluster.md)参照してください。

## 垂直および水平スケーリング {#vertical-and-horizontal-scaling}

TiDB Cloud Dedicated は、垂直 (スケールアップ) スケーリングと水平 (スケールアウト) スケーリングの両方をサポートします。

-   水平スケーリングは、ワークロードを分散するために専用クラスターにノードを追加するプロセスです。
-   垂直スケーリングは、専用クラスターの vCPU と RAM を増やすプロセスです。

TiDB Cloud Dedicated では、垂直スケーリングと水平スケーリングの両方の組み合わせもサポートされています。

## TiDB のスケーラビリティ {#tidb-scalability}

TiDB はコンピューティング専用であり、データは保存しません。TiDB のノード数、vCPU、および RAM を構成できます。

一般に、TiDB のパフォーマンスは TiDB ノードの数に応じて直線的に増加します。

## TiKV のスケーラビリティ {#tikv-scalability}

TiKV は行ベースのデータを保存する役割を担います。TiKV のノード数、vCPU と RAM、storageを構成できます。TiKV ノードの数は少なくとも 1 セット (3 つの異なる使用可能なゾーンの 3 つのノード) で、3 ノードずつ増加する必要があります。

TiDB Cloud は、耐久性と高可用性を実現するために、選択したリージョンの 3 つの利用可能なゾーンに TiKV ノードを均等にデプロイします。一般的な 3 つのレプリカのセットアップでは、データはすべての可用性ゾーンの TiKV ノードに均等に分散され、各 TiKV ノードのディスクに保持されます。TiKV は主にデータstorageに使用されますが、TiKV ノードのパフォーマンスはさまざまなワークロードによっても異なります。

## TiFlashのスケーラビリティ {#tiflash-scalability}

TiFlash は列指向データを保存する役割を担います。TiFlashはTiKV からのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。TiFlashのノード数、vCPU と RAM、storageを構成できます。

TiDB Cloud は、 TiFlashノードをリージョン内の異なるアベイラビリティ ゾーンに均等にデプロイします。本番環境で高可用性を確保するには、各TiDB Cloudクラスターに少なくとも 2 つのTiFlashノードを設定し、データのレプリカを少なくとも 2 つ作成することをお勧めします。
