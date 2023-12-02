---
title: TiFlash Overview
summary: Learn the architecture and key features of TiFlash.
---

# TiFlashの概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash)は、TiDB を本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースにする重要なコンポーネントです。 TiFlash は、TiKV のカラムナ型storage拡張機能として、優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlashでは、柱状レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。これらのレプリカが読み取られるとき、 Raftインデックスとマルチバージョン同時実行制御 (MVCC) を検証することによって、スナップショット分離レベルの一貫性が実現されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上のTiFlashノードを指定することで、HTAP クラスターを簡単に作成できます。クラスターの作成時にTiFlashノード数が指定されていない場合、またはTiFlashノードをさらに追加したい場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上の図は、 TiFlashノードを含む HTAP 形式の TiDB のアーキテクチャです。

TiFlash は、ClickHouse によって効率的に実装されたコプロセッサレイヤーを備えたカラム型storageを提供します。 TiKV と同様に、 TiFlashにも Multi-Raft システムがあり、リージョン単位でのデータの複製と分散をサポートしています (詳細は[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照)。

TiFlash は、 TiKV への書き込みをブロックしない低コストで、TiKV ノード内のデータのリアルタイム レプリケーションを実行します。一方、TiKV と同じ読み取り一貫性が提供され、最新のデータが確実に読み取られます。 TiFlashのリージョンレプリカは、論理的には TiKV のレプリカと同一であり、TiKV のLeaderレプリカと同時に分割およびマージされます。

Linux AMD64アーキテクチャでTiFlashを導入するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを導入するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セット拡張を使用することにより、TiFlash のベクトル化エンジンはより優れたパフォーマンスを実現できます。

<CustomContent platform="tidb">

TiFlash はTiDB と TiSpark の両方と互換性があるため、これら 2 つのコンピューティング エンジンから自由に選択できます。

</CustomContent>

ワークロードを確実に分離するために、TiKV とは別のノードにTiFlashをデプロイすることをお勧めします。ビジネスの分離が必要ない場合は、 TiFlashと TiKV を同じノードに導入することもできます。

現在、データをTiFlashに直接書き込むことはできません。 TiKV はLearnerの役割として TiDB クラスターに接続するため、データを TiKV に書き込んでからTiFlashにレプリケートする必要があります。 TiFlash はテーブル単位でのデータ複製をサポートしていますが、展開後のデフォルトではデータは複製されません。指定したテーブルのデータを複製するには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)を参照してください。

TiFlashには、柱状storageモジュール、 `tiflash proxy` 、および`pd buddy`つのコンポーネントがあります。 `tiflash proxy` Multi-Raft コンセンサス アルゴリズムを使用した通信を担当します。 `pd buddy` PDと連携してTiKVからTiFlashへテーブル単位でデータを複製します。

TiDB がTiFlashにレプリカを作成する DDL コマンドを受信すると、 `pd buddy`コンポーネントはTiDB のステータス ポートを介してレプリケーション対象のテーブルの情報を取得し、その情報を PD に送信します。次に、PD は`pd buddy`によって提供された情報に従って、対応するデータ スケジューリングを実行します。

## 主な特徴 {#key-features}

TiFlashには次の主要な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [インテリジェントな選択](#intelligent-choice)
-   [コンピューティングの高速化](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlash内のレプリカは、特別なロールRaft Learnerとして非同期的にレプリケートされます。つまり、 TiFlashノードがダウンしている場合や、ネットワークレイテンシーが発生している場合でも、TiKV のアプリケーションは通常どおり続行できるということです。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlash は追加のレプリケーション チャネルに依存せず、多対多の方法で TiKV からデータを直接受信します。
-   TiKV 内のデータが失われない限り、いつでもTiFlashにレプリカを復元できます。

### 一貫性 {#consistency}

TiFlash は、 TiKV と同じスナップショット分離レベルの一貫性を提供し、最新のデータが確実に読み取られるようにします。つまり、以前に TiKV に書き込まれたデータを読み取ることができます。このような一貫性は、データ複製の進行状況を検証することによって実現されます。

TiFlash が読み取りリクエストを受信するたびに、リージョンレプリカは進行状況検証リクエスト (軽量 RPC リクエスト) をLeaderレプリカに送信します。 TiFlash は、現在のレプリケーションの進行状況に読み取りリクエストのタイムスタンプでカバーされるデータが含まれた後にのみ読み取り操作を実行します。

### インテリジェントな選択 {#intelligent-choice}

TiDB は、 TiFlash (列方向) または TiKV (行方向) の使用を自動的に選択したり、1 つのクエリで両方を使用して最高のパフォーマンスを保証したりできます。

この選択メカニズムは、クエリを実行するためにさまざまなインデックスを選択する TiDB のメカニズムと似ています。 TiDB オプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティングの高速化 {#computing-acceleration}

TiFlash は、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   カラム型storageエンジンは、読み取り操作の実行効率が高くなります。
-   TiFlash は、 TiDB のコンピューティング ワークロードの一部を共有します。

TiFlash は、 TiKVコプロセッサーと同じ方法でコンピューティング ワークロードを共有します。TiDB は、storageレイヤーで完了できるコンピューティングをプッシュダウンします。コンピューティングをプッシュダウンできるかどうかは、 TiFlashのサポートに依存します。詳細は[サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)を参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashの展開後、データ レプリケーションは自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

<CustomContent platform="tidb">

TiDB を使用して中規模の分析処理用にTiFlashレプリカを読み取ることも、TiSpark を使用して大規模な分析処理用にTiFlashレプリカを読み取ることもできますが、これは独自のニーズに基づいています。詳細については、次のセクションを参照してください。

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

## こちらも参照 {#see-also}

<CustomContent platform="tidb">

-   TiFlashノードを含む新しいクラスターをデプロイするには、 [TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。
-   デプロイされたクラスターにTiFlashノードを追加するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)を参照してください。
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md) 。
-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashを構成する](/tiflash/tiflash-configuration.md) 。
-   [TiFlashクラスターを監視する](/tiflash/monitor-tiflash.md) 。
-   [TiFlashアラート ルール](/tiflash/tiflash-alert-rules.md)を学びます。
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) 。
-   [TiFlashでサポートされるプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashでサポートされるプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
