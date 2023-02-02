---
title: TiFlash Overview
summary: Learn the architecture and key features of TiFlash.
---

# TiFlash の概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash)は、TiDB を本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースにする重要なコンポーネントです。 TiKV の柱状ストレージ拡張機能として、 TiFlashは優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlashでは、カラムナー レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。これらのレプリカが読み取られると、 Raftインデックスとマルチバージョン同時実行制御 (MVCC) を検証することによって、一貫性のスナップショット分離レベルが達成されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上のTiFlashノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時にTiFlashノード数が指定されていない場合、またはさらにTiFlashノードを追加する場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上の図は、 TiFlashノードを含む、HTAP 形式の TiDB のアーキテクチャです。

TiFlashは、ClickHouse によって効率的に実装されたコプロセッサのレイヤーを備えた柱状ストレージを提供します。 TiKV と同様に、 TiFlashにも Multi-Raft システムがあり、リージョン単位でのデータの複製と配布をサポートしています (詳細は[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照)。

TiFlashは、TiKV での書き込みをブロックしない低コストで、TiKV ノード内のデータのリアルタイム レプリケーションを実行します。一方、TiKV と同じ読み取り一貫性を提供し、最新のデータが読み取られるようにします。 TiFlash のリージョンレプリカは、 TiFlashのリージョン レプリカと論理的に同一であり、TiKV のLeaderレプリカと同時に分割およびマージされます。

Linux AMD64アーキテクチャでTiFlashを展開するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`を使用して、出力があることを確認します。このような CPU 命令セットを使用することで、TiFlash のベクトル化エンジンはパフォーマンスを向上させることができます。

TiFlashは TiDB と TiSpark の両方と互換性があるため、これら 2 つのコンピューティング エンジンを自由に選択できます。

ワークロードの分離を確実にするために、TiKV とは異なるノードにTiFlashを展開することをお勧めします。ビジネスの分離が必要ない場合は、 TiFlashと TiKV を同じノードに展開することもできます。

現在、データを直接TiFlashに書き込むことはできません。 TiDB クラスターにLearnerロールとして接続するため、TiKV にデータを書き込んでからTiFlashに複製する必要があります。 TiFlashはテーブル単位でのデータ レプリケーションをサポートしますが、デプロイ後のデフォルトではデータはレプリケートされません。指定したテーブルのデータをレプリケートするには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)を参照してください。

TiFlashには、カラムナ ストレージ モジュール`tiflash proxy`と`pd buddy`の 3 つのコンポーネントがあります。 `tiflash proxy`は、Multi-Raft コンセンサス アルゴリズムを使用した通信を担当します。 `pd buddy`は PD と連携して、テーブル単位で TiKV からTiFlashにデータを複製します。

TiDB がTiFlashにレプリカを作成する DDL コマンドを受信すると、 `pd buddy`コンポーネントは TiDB のステータス ポートを介して複製対象のテーブルの情報を取得し、その情報を PD に送信します。次に、PD は、 `pd buddy`によって提供される情報に従って、対応するデータ スケジューリングを実行します。

## 主な機能 {#key-features}

TiFlashには次の主要な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [賢い選択](#intelligent-choice)
-   [コンピューティング アクセラレーション](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlashのレプリカは、特別なロールRaft Learnerとして非同期に複製されます。これは、 TiFlashノードがダウンしたり、ネットワークレイテンシーが発生したりした場合でも、TiKV のアプリケーションは正常に続行できることを意味します。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlashは、追加のレプリケーション チャネルに依存しませんが、多対多の方法で TiKV から直接データを受信します。
-   TiKV でデータが失われない限り、いつでもTiFlashでレプリカを復元できます。

### 一貫性 {#consistency}

TiFlashは、TiKV と同じスナップショット分離レベルの一貫性を提供し、最新のデータが読み取られることを保証します。つまり、以前に TiKV に書き込まれたデータを読み取ることができます。このような一貫性は、データ レプリケーションの進行状況を検証することによって達成されます。

TiFlashが読み取りリクエストを受信するたびに、リージョンレプリカは進行状況検証リクエスト (軽量の RPC リクエスト) をLeaderレプリカに送信します。 TiFlashは、現在のレプリケーションの進行状況に読み取り要求のタイムスタンプでカバーされたデータが含まれた後にのみ、読み取り操作を実行します。

### 賢い選択 {#intelligent-choice}

TiDB は自動的にTiFlash (列方向) または TiKV (行方向) を使用するか、または 1 つのクエリで両方を使用して最高のパフォーマンスを確保するかを選択できます。

この選択メカニズムは、クエリを実行するために異なるインデックスを選択する TiDB のメカニズムと似ています。 TiDB オプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティング アクセラレーション {#computing-acceleration}

TiFlashは、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   カラムナ ストレージ エンジンは、読み取り操作の実行においてより効率的です。
-   TiFlashは、TiDB のコンピューティング ワークロードの一部を共有します。

TiFlashは、TiKVコプロセッサーと同じ方法でコンピューティング ワークロードを共有します。TiDB は、ストレージレイヤーで完了できるコンピューティングをプッシュ ダウンします。コンピューティングを押し下げることができるかどうかは、 TiFlashのサポートに依存します。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashが展開された後、データの複製は自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

TiDB を使用して中規模の分析処理用のTiFlashレプリカを読み取るか、TiSpark を使用して大規模な分析処理用のTiFlashレプリカを読み取ることができます。これは、独自のニーズに基づいています。詳細については、次のセクションを参照してください。

-   [TiFlashレプリカの作成](/tiflash/create-tiflash-replicas.md)
-   [TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

-   [TiSpark を使用してTiFlashレプリカを読み取る](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

-   [MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

データのインポートから TPC-H データセットでのクエリまでのプロセス全体を体験するには、 [TiDB HTAPのクイック スタート ガイド](/quick-start-with-htap.md)を参照してください。

</CustomContent>

## こちらもご覧ください {#see-also}

<CustomContent platform="tidb">

-   TiFlashノードを使用して新しいクラスターをデプロイするには、 [TiUP を使用してTiUPクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。
-   デプロイされたクラスターにTiFlashノードを追加するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
-   [TiFlashクラスターを管理する](/tiflash/maintain-tiflash.md) .
-   [TiFlashのパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlash の構成](/tiflash/tiflash-configuration.md) .
-   [TiFlashクラスターを監視する](/tiflash/monitor-tiflash.md) .
-   学ぶ[TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md) ．
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) .
-   [TiFlashでサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlash の互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlashのパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlashでサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlash の互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
