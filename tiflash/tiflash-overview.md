---
title: TiFlash Overview
summary: Learn the architecture and key features of TiFlash.
aliases: ['/tidb/stable/use-tiflash','/tidb/v6.1/use-tiflash']
---

# TiFlash の概要 {#tiflash-overview}

[ティフラッシュ](https://github.com/pingcap/tiflash)は、TiDB を本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースにする重要なコンポーネントです。 TiKV の柱状ストレージ拡張機能として、TiFlash は優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlash では、カラムナー レプリカはRaft Learner コンセンサス アルゴリズムに従って非同期的に複製されます。これらのレプリカが読み取られると、 Raftインデックスとマルチバージョン同時実行制御 (MVCC) を検証することによって、一貫性のスナップショット分離レベルが達成されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上の TiFlash ノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時に TiFlash ノード数が指定されていない場合、またはさらに TiFlash ノードを追加する場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture.png)

上の図は、TiFlash ノードを含む、HTAP 形式の TiDB のアーキテクチャです。

TiFlash は、ClickHouse によって効率的に実装されたコプロセッサのレイヤーを備えた柱状ストレージを提供します。 TiKV と同様に、TiFlash にも Multi-Raft システムがあり、リージョン単位でのデータの複製と配布をサポートしています (詳細は[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照)。

TiFlash は、TiKV での書き込みをブロックしない低コストで、TiKV ノード内のデータのリアルタイム レプリケーションを実行します。一方、TiKV と同じ読み取り一貫性を提供し、最新のデータが読み取られるようにします。 TiFlash のリージョンレプリカは、TiKV のリージョン レプリカと論理的に同一であり、TiKV のリーダー レプリカと同時に分割およびマージされます。

TiFlash は TiDB と TiSpark の両方と互換性があるため、これら 2 つのコンピューティング エンジンを自由に選択できます。

ワークロードの分離を確実にするために、TiKV とは異なるノードに TiFlash を展開することをお勧めします。ビジネスの分離が必要ない場合は、TiFlash と TiKV を同じノードに展開することもできます。

現在、データを直接 TiFlash に書き込むことはできません。学習者ロールとして TiDB クラスターに接続するため、TiKV にデータを書き込んでから TiFlash に複製する必要があります。 TiFlash はテーブル単位でのデータ レプリケーションをサポートしますが、デプロイ後のデフォルトではデータはレプリケートされません。指定したテーブルのデータをレプリケートするには、 [テーブルの TiFlash レプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)を参照してください。

TiFlash には、カラムナ ストレージ モジュール`tiflash proxy`と`pd buddy`の 3 つのコンポーネントがあります。 `tiflash proxy`は、Multi-Raft コンセンサス アルゴリズムを使用した通信を担当します。 `pd buddy`は PD と連携して、テーブル単位で TiKV から TiFlash にデータを複製します。

TiDB が TiFlash にレプリカを作成する DDL コマンドを受信すると、 `pd buddy`コンポーネントは、TiDB のステータス ポートを介して、複製するテーブルの情報を取得し、その情報を PD に送信します。次に、PD は、 `pd buddy`によって提供される情報に従って、対応するデータ スケジューリングを実行します。

## 主な機能 {#key-features}

TiFlash には次の主要な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [賢い選択](#intelligent-choice)
-   [コンピューティング アクセラレーション](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlash のレプリカは、 Raft Learner という特別な役割として非同期に複製されます。これは、TiFlash ノードがダウンしたり、ネットワークレイテンシーが発生したりした場合でも、TiKV のアプリケーションは正常に続行できることを意味します。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlash は、追加のレプリケーション チャネルに依存しませんが、多対多の方法で TiKV から直接データを受信します。
-   TiKV でデータが失われない限り、いつでも TiFlash でレプリカを復元できます。

### 一貫性 {#consistency}

TiFlash は、TiKV と同じスナップショット分離レベルの一貫性を提供し、最新のデータが読み取られることを保証します。つまり、以前に TiKV に書き込まれたデータを読み取ることができます。このような一貫性は、データ レプリケーションの進行状況を検証することによって達成されます。

TiFlash が読み取りリクエストを受信するたびに、リージョンレプリカは進行状況検証リクエスト (軽量の RPC リクエスト) をリーダー レプリカに送信します。 TiFlash は、現在のレプリケーションの進行状況に読み取り要求のタイムスタンプでカバーされたデータが含まれた後にのみ、読み取り操作を実行します。

### 賢い選択 {#intelligent-choice}

TiDB は自動的に TiFlash (列方向) または TiKV (行方向) を使用するか、または 1 つのクエリで両方を使用して最高のパフォーマンスを確保するかを選択できます。

この選択メカニズムは、クエリを実行するために異なるインデックスを選択する TiDB のメカニズムと似ています。 TiDB オプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティング アクセラレーション {#computing-acceleration}

TiFlash は、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   カラムナ ストレージ エンジンは、読み取り操作の実行においてより効率的です。
-   TiFlash は、TiDB のコンピューティング ワークロードの一部を共有します。

TiFlash は、TiKV コプロセッサと同じ方法でコンピューティング ワークロードを共有します。TiDB は、ストレージレイヤーで完了できるコンピューティングをプッシュ ダウンします。コンピューティングを押し下げることができるかどうかは、TiFlash のサポートに依存します。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

## TiFlash を使用する {#use-tiflash}

TiFlash が展開された後、データの複製は自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

TiDB を使用して中規模の分析処理用の TiFlash レプリカを読み取るか、TiSpark を使用して大規模な分析処理用の TiFlash レプリカを読み取ることができます。これは、独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [TiFlash レプリカの作成](/tiflash/create-tiflash-replicas.md)
-   [TiDB を使用して TiFlash レプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

-   [TiSpark を使用して TiFlash レプリカを読み取る](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

-   [MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

データのインポートから TPC-H データセットでのクエリまでのプロセス全体を体験するには、 [TiDB HTAPのクイック スタート ガイド](/quick-start-with-htap.md)を参照してください。

</CustomContent>

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   TiFlash ノードを使用して新しいクラスターをデプロイするには、 [TiUP を使用して TiDB クラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。
-   デプロイされたクラスターに TiFlash ノードを追加するには、 [TiFlash クラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
-   [TiFlash クラスターを管理する](/tiflash/maintain-tiflash.md) .
-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlash の構成](/tiflash/tiflash-configuration.md) .
-   [TiFlash クラスターを監視する](/tiflash/monitor-tiflash.md) .
-   学ぶ[TiFlash アラート ルール](/tiflash/tiflash-alert-rules.md) ．
-   [TiFlash クラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) .
-   [TiFlash でサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlash でのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlash の互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlash でサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlash の互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
