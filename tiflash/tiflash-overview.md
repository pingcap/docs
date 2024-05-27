---
title: TiFlash Overview
summary: TiFlashのアーキテクチャと主な機能について学びます。
---

# TiFlashの概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash)は、TiDB を本質的にハイブリッド トランザクション/分析処理 (HTAP) データベースにする重要なコンポーネントです。TiKV の列指向storage拡張機能として、 TiFlash は優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlashでは、列レプリカはRaft Learnerコンセンサス アルゴリズムに従って非同期的に複製されます。これらのレプリカが読み取られると、 Raftインデックスとマルチバージョン同時実行制御 (MVCC) を検証することで、スナップショット分離レベルの一貫性が実現されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つ以上のTiFlashノードを指定して、HTAP クラスターを簡単に作成できます。クラスターの作成時にTiFlashノード数が指定されていない場合、またはTiFlashノードをさらに追加したい場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上図は、 TiFlashノードを含む HTAP 形式の TiDB のアーキテクチャです。

TiFlash は、ClickHouse によって効率的に実装されたコプロセッサのレイヤーを備えた列指向storageを提供します。TiKV と同様に、 TiFlashにも Multi-Raft システムがあり、リージョン単位でのデータの複製と配布をサポートしています (詳細については[データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)を参照)。

TiFlashは、TiKV への書き込みをブロックしない低コストで、TiKV ノードのデータのリアルタイム レプリケーションを実行します。同時に、 TiFlashと同じ読み取り一貫性を提供し、最新のデータが読み取られることを保証します。TiFlash のリージョンレプリカは、TiKV のリージョン レプリカと論理的に同一であり、TiKV のLeaderレプリカと同時に分割および結合されます。

Linux AMD64アーキテクチャでTiFlashを展開するには、CPU が AVX2 命令セットをサポートしている必要があります`cat /proc/cpuinfo | grep avx2`が出力されていることを確認してください。Linux ARM64アーキテクチャでTiFlash を展開するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。3 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`出力されていることを確認してください。命令セット拡張を使用することで、TiFlash のベクトル化エンジンはより優れたパフォーマンスを発揮できます。

<CustomContent platform="tidb">

TiFlash はTiDB と TiSpark の両方と互換性があり、これら 2 つのコンピューティング エンジンを自由に選択できます。

</CustomContent>

ワークロードの分離を確実にするために、 TiFlash をTiKV とは別のノードにデプロイすることをお勧めします。ビジネス分離が不要な場合は、 TiFlashと TiKV を同じノードにデプロイすることもできます。

現在、データを直接TiFlashに書き込むことはできません。TiFlash はLearnerロールとして TiDB クラスターに接続するため、TiKV にデータを書き込んでからTiFlashに複製する必要があります。TiFlashはテーブル単位でのデータ複製をサポートしていますが、デプロイ後、デフォルトではデータは複製されません。指定したテーブルのデータを複製するには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)参照してください。

TiFlashには、列型storageモジュール、 `tiflash proxy` `pd buddy` 3 つのコンポーネントがあります。5 `tiflash proxy` 、Multi-Raft コンセンサス アルゴリズムを使用した通信を担当します。7 `pd buddy` PD と連携して、テーブル単位で TiKV からTiFlashにデータを複製します。

TiDBがTiFlashにレプリカを作成するためのDDLコマンドを受信すると、 `pd buddy`コンポーネントはTiDBのステータスポートを介して複製されるテーブルの情報を取得し、その情報をPDに送信します。次に、PDは`pd buddy`から提供された情報に従って対応するデータスケジューリングを実行します。

## 主な特徴 {#key-features}

TiFlashには次の主な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [賢い選択](#intelligent-choice)
-   [コンピューティングの高速化](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlash内のレプリカは、特別なロールであるRaft Learnerとして非同期的に複製されます。つまり、 TiFlashノードがダウンしたり、ネットワークのレイテンシーが長くなった場合でも、TiKV 内のアプリケーションは正常に処理を続行できます。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlash は追加のレプリケーション チャネルに依存せず、多対多の方法で TiKV からデータを直接受信します。
-   TiKV でデータが失われない限り、いつでもTiFlashでレプリカを復元できます。

### 一貫性 {#consistency}

TiFlash は、TiKV と同じスナップショット分離レベルの一貫性を提供し、最新のデータが読み取られることを保証します。つまり、TiKV に以前書き込まれたデータを読み取ることができます。このような一貫性は、データ レプリケーションの進行状況を検証することによって実現されます。

TiFlash が読み取り要求を受信するたびに、リージョンレプリカは進行状況検証要求 (軽量 RPC 要求) をLeaderレプリカに送信します。TiFlashは、現在のレプリケーション進行状況に読み取り要求のタイムスタンプでカバーされるデータが含まれた後にのみ、読み取り操作を実行します。

### 賢い選択 {#intelligent-choice}

TiDB は、 TiFlash (列単位) または TiKV (行単位) の使用を自動的に選択するか、または 1 つのクエリで両方を使用して最高のパフォーマンスを確保できます。

この選択メカニズムは、クエリを実行するために異なるインデックスを選択する TiDB のメカニズムに似ています。TiDB オプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティングの高速化 {#computing-acceleration}

TiFlash は、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   列型storageエンジンは読み取り操作の実行がより効率的です。
-   TiFlash はTiDB のコンピューティング ワークロードの一部を共有します。

TiFlash は、TiKVコプロセッサーと同じ方法でコンピューティング ワークロードを共有します。TiDB は、storageレイヤーで完了できるコンピューティングをプッシュダウンします。コンピューティングをプッシュダウンできるかどうかは、 TiFlashのサポートによって異なります。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashを展開した後、データのレプリケーションは自動的に開始されません。レプリケートするテーブルを手動で指定する必要があります。

<CustomContent platform="tidb">

中規模の分析処理のために TiDB を使用してTiFlashレプリカを読み取ることも、独自のニーズに基づいて、大規模な分析処理のために TiSpark を使用してTiFlashレプリカを読み取ることもできます。詳細については、次のセクションを参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB を使用して、分析処理のためにTiFlashレプリカを読み取ることができます。詳細については、次のセクションを参照してください。

</CustomContent>

-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

-   [TiSparkを使用してTiFlashレプリカを読み取る](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

TPC-H データセットでのデータのインポートからクエリまでのプロセス全体を体験するには、 [TiDB HTAPクイック スタート ガイド](/quick-start-with-htap.md)を参照してください。

</CustomContent>

## 参照 {#see-also}

<CustomContent platform="tidb">

-   TiFlashノードを使用して新しいクラスターを展開するには、 [TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)参照してください。
-   デプロイされたクラスターにTiFlashノードを追加するには、 [TiFlashクラスターをスケールアウトする](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md) 。
-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlash を設定する](/tiflash/tiflash-configuration.md) 。
-   [TiFlashクラスターを監視する](/tiflash/monitor-tiflash.md) 。
-   [TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)学びます。
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) 。
-   [TiFlashでのプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlash互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlash のパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashでのプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
