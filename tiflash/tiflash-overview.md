---
title: TiFlash Overview
summary: TiFlashのアーキテクチャと主な機能について学びます。
---

# TiFlashの概要 {#tiflash-overview}

[TiFlash](https://github.com/pingcap/tiflash) 、TiDBを本質的にハイブリッドトランザクション/分析処理（HTAP）データベースにする主要コンポーネントです。TiKVの列指向storage拡張であるTiFlashは、優れた分離レベルと強力な一貫性保証の両方を提供します。

TiFlashでは、列指向レプリカはRaft Learnerコンセンサスアルゴリズムに従って非同期的に複製されます。これらのレプリカが読み込まれると、 Raftインデックスと多版型同時実行制御（MVCC）の検証によって、スナップショット分離レベルの一貫性が実現されます。

<CustomContent platform="tidb-cloud">

TiDB Cloudを使用すると、HTAP ワークロードに応じて 1 つまたは複数のTiFlashノードを指定するだけで、HTAP クラスターを簡単に作成できます。クラスター作成時にTiFlashノード数を指定していない場合、またはTiFlashノードを追加したい場合は、ノード数を[クラスターのスケーリング](/tidb-cloud/scale-tidb-cluster.md)ずつ変更できます。

</CustomContent>

## アーキテクチャ {#architecture}

![TiFlash Architecture](/media/tidb-storage-architecture-1.png)

上図は、 TiFlashノードを含む HTAP 形式の TiDB のアーキテクチャです。

TiFlashは、ClickHouseによって効率的に実装されたコプロセッサレイヤーを備えた列指向storageを提供します。TiKVと同様に、 TiFlashにもMulti-Raftシステムが搭載されており、リージョン単位でのデータの複製と分散をサポートします（詳細は[データストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/)参照）。

TiFlashは、TiKVノード内のデータのリアルタイムレプリケーションを低コストで実行します。これにより、TiKVへの書き込みがブロックされることはありません。同時に、 TiFlashと同様の読み取り一貫性を提供し、最新のデータが読み取られることを保証します。TiFlashのリージョンレプリカはTiKVのレプリカと論理的に同一であり、TiKVのLeaderレプリカと同時に分割・統合されます。

Linux AMD64アーキテクチャでTiFlashを展開するには、CPUがAVX2命令セットをサポートしている必要があります`cat /proc/cpuinfo | grep avx2`出力されていることを確認してください。Linux ARM64アーキテクチャでTiFlashを展開するには、CPUがARMv8命令セットアーキテクチャをサポートしている必要があります。3 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`出力されていることを確認してください。命令セット拡張を使用することで、TiFlashのベクトル化エンジンはより優れたパフォーマンスを発揮できます。

<CustomContent platform="tidb">

TiFlash はTiDB と TiSpark の両方と互換性があり、これら 2 つのコンピューティング エンジンを自由に選択できます。

</CustomContent>

ワークロードの分離を確保するため、 TiFlash をTiKV とは別のノードにデプロイすることをお勧めします。業務上の分離が不要な場合は、 TiFlashと TiKV を同じノードにデプロイすることも可能です。

現在、 TiFlashに直接データを書き込むことはできません。TiKV は TiDB クラスターにLearnerロールとして接続するため、 TiFlashにデータを書き込み、それを複製する必要があります。TiFlashはテーブル単位でのデータ複製をサポートしていますが、デプロイ後、デフォルトではデータは複製されません。指定したテーブルのデータを複製するには、 [テーブルのTiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-tables)参照してください。

TiFlashは、列指向storageコンポーネントとTiFlashプロキシコンポーネントという2つの主要コンポーネントで構成されています。TiFlashプロキシコンポーネントは、Multi-Raftコンセンサスアルゴリズムを用いた通信を担当します。

TiFlash内のテーブルのレプリカを作成するための DDL コマンドを受信すると、TiDB は PD 内に対応する[配置ルール](https://docs.pingcap.com/tidb/stable/configure-placement-rules)自動的に作成し、その後 PD はこれらのルールに基づいて対応するデータ スケジューリングを実行します。

## 主な特徴 {#key-features}

TiFlashには次の主な機能があります。

-   [非同期レプリケーション](#asynchronous-replication)
-   [一貫性](#consistency)
-   [賢い選択](#intelligent-choice)
-   [コンピューティングの加速](#computing-acceleration)

### 非同期レプリケーション {#asynchronous-replication}

TiFlash内のレプリカは、特別な役割であるRaft Learnerとして非同期的に複製されます。つまり、 TiFlashノードがダウンしたり、ネットワークのレイテンシーが大きくなったりしても、TiKV内のアプリケーションは正常に動作し続けることができます。

このレプリケーション メカニズムは、自動負荷分散と高可用性という TiKV の 2 つの利点を継承しています。

-   TiFlash は追加のレプリケーション チャネルに依存せず、多対多の方法で TiKV からデータを直接受信します。
-   TiKV でデータが失われていない限り、いつでもTiFlashでレプリカを復元できます。

### 一貫性 {#consistency}

TiFlashはTiKVと同じスナップショット分離レベルの一貫性を提供し、最新のデータが読み取られることを保証します。つまり、TiKVに以前書き込まれたデータを読み取ることができます。このような一貫性は、データレプリケーションの進行状況を検証することで実現されます。

TiFlash が読み取り要求を受信するたびに、リージョンレプリカはLeaderレプリカに進行状況検証要求（軽量 RPC 要求）を送信します。TiFlashは、読み取り要求のタイムスタンプに含まれるデータが現在のレプリケーション進行状況に含まれるようになった場合にのみ、読み取り操作を実行します。

### 賢い選択 {#intelligent-choice}

TiDB は、 TiFlash (列単位) または TiKV (行単位) の使用を自動的に選択するか、または 1 つのクエリで両方を使用して、最高のパフォーマンスを確保できます。

この選択メカニズムは、クエリ実行時に異なるインデックスを選択するTiDBのメカニズムに似ています。TiDBオプティマイザーは、読み取りコストの統計に基づいて適切な選択を行います。

### コンピューティングの加速 {#computing-acceleration}

TiFlash は、次の 2 つの方法で TiDB のコンピューティングを高速化します。

-   列型storageエンジンは読み取り操作の実行においてより効率的です。
-   TiFlash はTiDB のコンピューティング ワークロードの一部を共有します。

TiFlashは、TiKVコプロセッサーと同様に、コンピューティングワークロードを分散します。TiDBは、storageレイヤーで完了可能なコンピューティングをプッシュダウンします。コンピューティングをプッシュダウンできるかどうかは、 TiFlashのサポート状況によって異なります。詳細については、 [サポートされているプッシュダウン計算](/tiflash/tiflash-supported-pushdown-calculations.md)参照してください。

## TiFlashを使用する {#use-tiflash}

TiFlashを導入しても、データのレプリケーションは自動的に開始されません。レプリケーションするテーブルを手動で指定する必要があります。

<CustomContent platform="tidb">

中規模の分析処理ではTiDBを使用してTiFlashレプリカを読み取るか、大規模な分析処理ではTiSparkを使用してTiFlashレプリカを読み取るか、お客様のニーズに合わせて選択できます。詳細については、以下のセクションをご覧ください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDBを使用してTiFlashレプリカを読み取り、分析処理を行うことができます。詳細については、以下のセクションをご覧ください。

</CustomContent>

-   [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)
-   [TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)

<CustomContent platform="tidb">

-   [TiSparkを使用してTiFlashレプリカを読み取る](/tiflash/use-tispark-to-read-tiflash.md)

</CustomContent>

-   [MPPモードを使用する](/tiflash/use-tiflash-mpp-mode.md)

<CustomContent platform="tidb">

TPC-H データセットでのデータのインポートからクエリまでのプロセス全体を体験するには、 [TiDB HTAPクイックスタートガイド](/quick-start-with-htap.md)を参照してください。

</CustomContent>

## 参照 {#see-also}

<CustomContent platform="tidb">

-   TiFlashノードを含む新しいクラスターを展開するには、 [TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)参照してください。
-   デプロイされたクラスターにTiFlashノードを追加するには、 [TiFlashクラスターのスケールアウト](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster)参照してください。
-   [TiFlashクラスターを管理](/tiflash/maintain-tiflash.md) 。
-   [TiFlashのパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashを設定する](/tiflash/tiflash-configuration.md) 。
-   [TiFlashクラスタを監視する](/tiflash/monitor-tiflash.md) 。
-   [TiFlashアラートルール](/tiflash/tiflash-alert-rules.md)を学びます。
-   [TiFlashクラスターのトラブルシューティング](/tiflash/troubleshoot-tiflash.md) 。
-   [TiFlashでプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashでのデータ検証](/tiflash/tiflash-data-validation.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

-   [TiFlashのパフォーマンスを調整する](/tiflash/tune-tiflash-performance.md) 。
-   [TiFlashでプッシュダウン計算をサポート](/tiflash/tiflash-supported-pushdown-calculations.md)
-   [TiFlashの互換性](/tiflash/tiflash-compatibility.md)

</CustomContent>
