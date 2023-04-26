---
title: TiFlash Overview
summary: Learn the architecture and key features of TiFlash.
---

# TiFlashの概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash)は、TiDB を本質的に Hybrid Transactional/Analytical Processing (HTAP) データベースにする重要なコンポーネントです。 TiKV の柱状storage拡張機能として、 TiFlash は優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlashでは、カラムナー レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。これらのレプリカが読み取られると、 Raftインデックスとマルチバージョン同時実行制御 (MVCC) を検証することによって、一貫性のスナップショット分離レベルが達成されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上のTiFlashノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時にTiFlashノード数が指定されていない場合、またはさらにTiFlashノードを追加する場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上の図は、 TiFlashノードを含む、HTAP 形式の TiDB のアーキテクチャです。

TiFlash は、ClickHouse によって効率的に実装されたコプロセッサのレイヤーを備えた柱状storageを提供します。 TiKV と同様に、 TiFlashにも Multi-Raft システムがあり、リージョン単位でのデータの複製と配布をサポートしています (詳細は[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照)。

TiFlash は、 TiKV での書き込みをブロックしない低コストで、TiKV ノード内のデータのリアルタイム レプリケーションを実行します。一方、TiKV と同じ読み取り一貫性を提供し、最新のデータが読み取られるようにします。 TiFlashのリージョンレプリカは、TiKV のリージョン レプリカと論理的に同一であり、TiKV のLeaderレプリカと同時に分割およびマージされます。

Linux AMD64アーキテクチャでTiFlashを展開するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを展開するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セットの拡張機能を使用することで、TiFlash のベクトル化エンジンはパフォーマンスを向上させることができます。

<CustomContent platform="tidb">

TiFlash はTiDB と TiSpark の両方と互換性があるため、これら 2 つのコンピューティング エンジンを自由に選択できます。

</CustomContent>

ワークロードの分離を確実にするために、TiKV とは異なるノードにTiFlashを展開することをお勧めします。ビジネスの分離が必要ない場合は、 TiFlashと TiKV を同じノードに展開することもできます。

現在、データを直接TiFlashに書き込むことはできません。 TiDB クラスターにLearnerロールとして接続するため、TiKV にデータを書き込んでからTiFlashに複製する必要があります。 TiFlash はテーブル単位でのデータ レプリケーションをサポートしますが、デプロイ後のデフォルトではデータはレプリケートされません。指定したテーブルのデータをレプリケートするには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)を参照してください。

TiFlashには、カラムナstorageモジュール`tiflash proxy`と`pd buddy` 3 つのコンポーネントがあります。 `tiflash proxy` Multi-Raft コンセンサス アルゴリズムを使用した通信を担当します。 `pd buddy` PD と連携して、テーブル単位で TiKV からTiFlashにデータを複製します。

TiDB がTiFlashにレプリカを作成する DDL コマンドを受信すると、 `pd buddy`コンポーネントはTiDB のステータス ポートを介して複製対象のテーブルの情報を取得し、その情報を PD に送信します。次に、PD は`pd buddy`によって提供される情報に従って、対応するデータ スケジューリングを実行します。

## 主な機能 {#key-features}

TiFlashには次の主要な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [賢い選択](#intelligent-choice)
-   [コンピューティング アクセラレーション](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlashのレプリカは、特別なロールRaft Learnerとして非同期に複製されます。これは、 TiFlashノードがダウンしたり、ネットワークレイテンシーが発生したりした場合でも、TiKV のアプリケーションは正常に続行できることを意味します。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlash は、追加のレプリケーション チャネルに依存しませんが、多対多の方法で TiKV から直接データを受信します。
-   TiKV でデータが失われない限り、いつでもTiFlashでレプリカを復元できます。

### 一貫性 {#consistency}

TiFlash は、 TiKV と同じスナップショット分離レベルの一貫性を提供し、最新のデータが読み取られることを保証します。つまり、以前に TiKV に書き込まれたデータを読み取ることができます。このような一貫性は、データ レプリケーションの進行状況を検証することによって達成されます。

TiFlash が読み取りリクエストを受信するたびに、リージョンレプリカは進行状況検証リクエスト (軽量の RPC リクエスト) をLeaderレプリカに送信します。 TiFlash は、現在のレプリケーションの進行状況に読み取り要求のタイムスタンプでカバーされたデータが含まれた後にのみ、読み取り操作を実行します。

### 賢い選択 {#intelligent-choice}

TiDB は自動的にTiFlash (列方向) または TiKV (行方向) を使用するか、または 1 つのクエリで両方を使用して最高のパフォーマンスを確保するかを選択できます。

この選択メカニズムは、クエリを実行するために異なるインデックスを選択する TiDB のメカニズムと似ています。 TiDB オプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティング アクセラレーション {#computing-acceleration}

TiFlash は、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   カラムナstorageエンジンは、読み取り操作の実行においてより効率的です。
-   TiFlash は、 TiDB のコンピューティング ワークロードの一部を共有します。

TiFlash は、 TiKVコプロセッサーと同じ方法でコンピューティング ワークロードを共有します。TiDB は、storageレイヤーで完了できるコンピューティングをプッシュ ダウンします。コンピューティングを押し下げることができるかどうかは、 TiFlashのサポートに依存します。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashが展開された後、データの複製は自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

<CustomContent platform="tidb">

TiDB を使用して中規模の分析処理用のTiFlashレプリカを読み取るか、TiSpark を使用して大規模な分析処理用のTiFlashレプリカを読み取ることができます。これは、独自のニーズに基づいています。詳細については、次のセクションを参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB を使用して、分析処理のためにTiFlashレプリカを読み取ることができます。詳細については、次のセクションを参照してください。

</CustomContent>

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

-   TiFlashノードを使用して新しいクラスターをデプロイするには、 [TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   デプロイされたクラスターにTiFlashノードを追加するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md) .
-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlashの構成](/tiflash/tiflash-configuration.md) .
-   [TiFlashクラスターを監視する](/tiflash/monitor-tiflash.md) .
-   学ぶ[TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md) ．
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) .
-   [TiFlashでサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) .
-   [TiFlashでサポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
