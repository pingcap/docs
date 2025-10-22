---
title: Scalability
summary: TiDB Cloudのスケーラビリティの概念について学習します。
---

# スケーラビリティ {#scalability}

TiDB Cloud は、さまざまなワークロードのニーズを満たすために、柔軟なスケーラビリティを備えた複数の展開オプションを提供します。

-   [TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter) 、プロトタイピング、開発、初期段階のワークロードに最適です。自動スケーリングが組み込まれているため、 TiDB Cloudをシンプルかつコスト効率よく導入できます。
-   [TiDB Cloudエッセンシャル](/tidb-cloud/select-cluster-tier.md#essential) 、トラフィックやデータ量の増加に応じて、より堅牢なスケーラビリティと予測可能なパフォーマンスを必要とする本番ワークロード向けに構築されています。
-   TiDB Cloud Dedicatedでは、データ量やワークロードの変化に合わせて、コンピューティングリソースとstorageリソースを個別に調整できます。TiDB TiDB Cloud Dedicatedは、サービスを中断することなくスケーリングできます。この柔軟性により、組織は高いパフォーマンスと可用性を維持しながら、インフラストラクチャコストを最適化できます。

> **ヒント：**
>
> TiDB Cloud Dedicated クラスターのサイズを決定する方法については、 [TiDBのサイズを決定する](/tidb-cloud/size-your-cluster.md)参照してください。

## 垂直方向と水平方向のスケーリング {#vertical-and-horizontal-scaling}

TiDB Cloud Dedicated は、垂直 (スケールアップ) スケーリングと水平 (スケールアウト) スケーリングの両方をサポートします。

-   水平スケーリングは、ワークロードを分散するために専用クラスターにノードを追加するプロセスです。
-   垂直スケーリングは、専用クラスターの vCPU と RAM を増やすプロセスです。

TiDB Cloud Dedicated では、垂直スケーリングと水平スケーリングの両方の組み合わせもサポートされています。

## TiDBのスケーラビリティ {#tidb-scalability}

TiDBはコンピューティングのみを目的としており、データの保存は行いません。TiDBのノード数、vCPU、RAMを設定できます。

一般に、TiDB のパフォーマンスは TiDB ノードの数に応じて直線的に増加します。

## TiKVのスケーラビリティ {#tikv-scalability}

TiKVは行ベースのデータの保存を担います。TiKVのノード数、vCPU、RAM、storageを設定できます。TiKVノードの数は少なくとも1セット（3つの異なる利用可能なゾーンに3ノード）で、3ノードずつ増加する必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内の3つの利用可能なゾーンにTiKVノードを均等にデプロイします。典型的な3レプリカ構成では、データはすべてのアベイラビリティゾーンにわたるTiKVノードに均等に分散され、各TiKVノードのディスクに永続化されます。TiKVは主にデータstorageに使用されますが、TiKVノードのパフォーマンスはワークロードによっても異なります。

## TiFlashのスケーラビリティ {#tiflash-scalability}

TiFlashは列指向データの保存を担います。TiFlashはTiKVからのデータをリアルタイムで同期し、すぐにリアルタイム分析ワークロードをサポートします。TiFlashのノード数、vCPU、RAM、storageを設定できます。

TiDB Cloudは、リージョン内の異なるアベイラビリティゾーンにTiFlashノードを均等に展開します。本番環境での高可用性を確保するため、各TiDB Cloudクラスターに少なくとも2つのTiFlashノードを設定し、データのレプリカを少なくとも2つ作成することをお勧めします。
