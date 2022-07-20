---
title: TiFlash Overview
summary: Learn the architecture and key features of TiFlash.
aliases: ['/tidb/stable/use-tiflash','/tidb/v6.1/use-tiflash']
---

# TiFlashの概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash)は、TiDBを本質的にハイブリッドトランザクション/分析処理（HTAP）データベースにする重要なコンポーネントです。 TiKVの列型ストレージ拡張として、TiFlashは優れた分離レベルと強力な一貫性の保証の両方を提供します。

TiFlashでは、柱状レプリカはRaftコンセンサスアルゴリズムに従って非同期に複製されます。これらのレプリカが読み取られると、スナップショット分離レベルの整合性は、 Raftインデックスとマルチバージョン同時実行制御（MVCC）を検証することによって達成されます。

## 建築 {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture.png)

上の図は、TiFlashノードを含むHTAP形式のTiDBのアーキテクチャです。

TiFlashは、ClickHouseによって効率的に実装されたコプロセッサーのレイヤーを備えた列型ストレージを提供します。 TiKVと同様に、TiFlashにもマルチラフトシステムがあり、リージョン単位でのデータの複製と配信をサポートします（詳細については[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照）。

TiFlashは、TiKVでの書き込みをブロックしない低コストで、TiKVノードのデータのリアルタイムレプリケーションを実行します。一方、TiKVと同じ読み取り整合性を提供し、最新のデータが確実に読み取られるようにします。 TiFlashのRegionレプリカは、TiKVのRegionレプリカと論理的に同一であり、TiKVのLeaderレプリカと同時に分割およびマージされます。

TiFlashはTiDBとTiSparkの両方と互換性があり、これら2つのコンピューティングエンジンから自由に選択できます。

ワークロードを確実に分離するために、TiKVとは異なるノードにTiFlashをデプロイすることをお勧めします。ビジネスの分離が必要ない場合は、TiFlashとTiKVを同じノードに展開することもできます。

現在、TiFlashに直接データを書き込むことはできません。学習者の役割としてTiDBクラスタに接続するため、TiKVでデータを書き込んでから、それをTiFlashに複製する必要があります。 TiFlashは、テーブル単位でのデータレプリケーションをサポートしていますが、展開後、デフォルトではデータはレプリケートされません。指定されたテーブルのデータを複製するには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)を参照してください。

TiFlashには、列型ストレージモジュール、 `tiflash proxy` 、および`pd buddy`の3つのコンポーネントがあります。 `tiflash proxy`は、マルチラフトコンセンサスアルゴリズムを使用した通信を担当します。 `pd buddy`はPDと連携して、テーブル単位でTiKVからTiFlashにデータを複製します。

TiDBがDDLコマンドを受信してTiFlashにレプリカを作成すると、 `pd buddy`コンポーネントは、TiDBのステータスポートを介して複製されるテーブルの情報を取得し、その情報をPDに送信します。次に、PDは、 `pd buddy`によって提供される情報に従って、対応するデータスケジューリングを実行します。

## 主な機能 {#key-features}

TiFlashには次の主要な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [インテリジェントな選択](#intelligent-choice)
-   [加速の計算](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlashのレプリカは、特別な役割であるRaftとして非同期に複製されます。これは、TiFlashノードがダウンしている場合、またはネットワーク遅延が大きい場合でも、TiKVのアプリケーションは正常に続行できることを意味します。

このレプリケーションメカニズムは、自動負荷分散と高可用性というTiKVの2つの利点を継承しています。

-   TiFlashは、追加のレプリケーションチャネルに依存しませんが、多対多の方法でTiKVからデータを直接受信します。
-   TiKVでデータが失われない限り、いつでもTiFlashでレプリカを復元できます。

### 一貫性 {#consistency}

TiFlashは、TiKVと同じスナップショット分離レベルの整合性を提供し、最新のデータが確実に読み取られるようにします。つまり、以前にTiKVで書き込まれたデータを読み取ることができます。このような一貫性は、データ複製の進行状況を検証することによって実現されます。

TiFlashが読み取り要求を受信するたびに、リージョンレプリカは進行状況検証要求（軽量RPC要求）をリーダーレプリカに送信します。 TiFlashは、現在のレプリケーションの進行状況に読み取り要求のタイムスタンプでカバーされるデータが含まれた後にのみ、読み取り操作を実行します。

### インテリジェントな選択 {#intelligent-choice}

TiDBは、TiFlash（列単位）またはTiKV（行単位）の使用を自動的に選択するか、1つのクエリで両方を使用して最高のパフォーマンスを確保することができます。

この選択メカニズムは、クエリを実行するために異なるインデックスを選択するTiDBのメカニズムに似ています。 TiDBオプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### 加速の計算 {#computing-acceleration}

TiFlashは、次の2つの方法でTiDBのコンピューティングを高速化します。

-   列指向ストレージエンジンは、読み取り操作の実行においてより効率的です。
-   TiFlashは、TiDBのコンピューティングワークロードの一部を共有します。

TiFlashは、TiKVコプロセッサーと同じ方法でコンピューティングワークロードを共有します。TiDBは、ストレージレイヤーで完了できるコンピューティングをプッシュダウンします。コンピューティングをプッシュダウンできるかどうかは、TiFlashのサポートに依存します。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashがデプロイされた後、データレプリケーションは自動的に開始されません。複製するテーブルを手動で指定する必要があります。

TiDBを使用して中規模の分析処理用のTiFlashレプリカを読み取るか、TiSparkを使用して大規模な分析処理用のTiFlashレプリカを読み取ることができます。これは独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)
-   [TiSparkを使用してTiFlashレプリカを読み取る](/tiflash/use-tispark-to-read-tiflash.md)
-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)

データのインポートからTPC-Hデータセットでのクエリまでのプロセス全体を体験するには、 [TiDB HTAPのクイックスタートガイド](/quick-start-with-htap.md)を参照してください。

## も参照してください {#see-also}

-   TiFlashノードを使用して新しいクラスタをデプロイするには、 [TiUPを使用してTiDBクラスタをデプロイする](/production-deployment-using-tiup.md)を参照してください。
-   デプロイされたクラスタにTiFlashノードを追加するには、 [TiFlashクラスタをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
-   [TiFlashクラスタを管理する](/tiflash/maintain-tiflash.md) 。
-   [TiFlashのパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashを構成する](/tiflash/tiflash-configuration.md) 。
-   [TiFlashクラスタを監視する](/tiflash/monitor-tiflash.md) 。
-   学ぶ[TiFlashアラートルール](/tiflash/tiflash-alert-rules.md) 。
-   [TiFlashクラスタのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) 。
-   [TiFlashでサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)
