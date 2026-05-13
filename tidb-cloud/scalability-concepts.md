---
title: Scalability
summary: TiDB Cloudのスケーラビリティに関する概念について学びましょう。
---

# 拡張性 {#scalability}

TiDB Cloudは、さまざまなワークロードのニーズに対応できるよう、柔軟な拡張性を備えた複数の導入オプションを提供します。

-   [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 、プロトタイプ作成、開発、および初期段階のワークロードに最適です。自動スケーリング機能が組み込まれているため、 TiDB Cloudを簡単かつ費用対効果の高い方法で使い始めることができます。
-   [TiDB Cloud Essential](/tidb-cloud/select-cluster-tier.md#essential)は、トラフィックやデータ量の増加下でも、より堅牢な拡張性と予測可能なパフォーマンスを必要とする本番のワークロード向けに構築されています。
-   [TiDB Cloudプレミアム](/tidb-cloud/select-cluster-tier.md#premium)は、無制限のリアルタイム拡張性を必要とするミッションクリティカルなビジネス向けに設計されています。ワークロードに応じた自動スケーリングと包括的なエンタープライズ機能を提供します。
-   TiDB Cloud Dedicated、データ量やワークロードの変化に合わせて、コンピューティングリソースとstorageリソースを個別に調整できます。TiDB TiDB Cloud Dedicatedは、サービスの中断なしにスケーリングが可能です。この柔軟性により、組織は高いパフォーマンスと可用性を維持しながら、インフラストラクチャコストを最適化できます。

> **ヒント：**
>
> TiDB Cloud Dedicatedクラスターのサイズを決定する方法については、 [TiDBサイズを決定する](/tidb-cloud/size-your-cluster.md)参照してください。

## 垂直方向および水平方向のスケーリング {#vertical-and-horizontal-scaling}

TiDB Cloud Dedicatedは、垂直スケーリング（スケールアップ）と水平スケーリング（スケールアウト）の両方をサポートしています。

-   水平スケーリングとは、ワークロードを分散するために、専用クラスターにノードを追加するプロセスです。
-   垂直スケーリングとは、専用クラスターのvCPUとRAMを増やすプロセスです。

TiDB Cloud Dedicatedでは、垂直スケーリングと水平スケーリングの両方の組み合わせもサポートされています。

## TiDBのスケーラビリティ {#tidb-scalability}

TiDBは計算処理専用であり、データを保存する機能はありません。TiDBのノード数、vCPU、およびRAM容量を設定できます。

一般的に、TiDBのパフォーマンスはTiDBノードの数に比例して向上します。

## TiKVのスケーラビリティ {#tikv-scalability}

TiKVは行ベースのデータを保存する役割を担います。TiKVのノード数、vCPU、RAM、storageを設定できます。TiKVノード数は最低1セット（3つの異なるゾーンにそれぞれ3ノード）とし、3ノードずつ増やしていく必要があります。

TiDB Cloudは、耐久性と高可用性を実現するために、選択したリージョン内の3つのアベイラブルゾーンにTiKVノードを均等に配置します。一般的な3レプリカ構成では、データはすべてのアベイラブルゾーンのTiKVノードに均等に分散され、各TiKVノードのディスクに永続化されます。TiKVは主にデータstorageに使用されますが、TiKVノードのパフォーマンスはワークロードによっても異なります。

## TiFlashの拡張性 {#tiflash-scalability}

TiFlashは、カラム型データの保存を担当します。TiFlashはTiKVからリアルタイムでデータを同期し、リアルタイム分析ワークロードをすぐにサポートします。TiFlashのノード数、vCPU、RAM、storageは設定可能です。

TiDB Cloudは、リージョン内の異なるアベイラビリティゾーンにTiFlashノードを均等に配置します。本番環境での高可用性を確保するため、各TiDB Cloud Dedicatedクラスタに少なくとも2つのTiFlashノードを設定し、データのレプリカを少なくとも2つ作成することをお勧めします。
