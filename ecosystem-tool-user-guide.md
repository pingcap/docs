---
title: TiDB Tools Overview
summary: Learn the tools and applicable scenarios.
---

# TiDB ツールの概要 {#tidb-tools-overview}

TiDB は、TiDB のデプロイと保守、データの管理 (データ移行、バックアップと復元、データ比較など)、TiKV での Spark SQL の実行に役立つ豊富なツール セットを提供します。ニーズに応じて適切なツールを選択できます。

## 導入および運用ツール {#deployment-and-operation-tools}

TiDB は、さまざまなシステム環境での導入と運用のニーズを満たすTiUPおよびTiDB Operatorを提供します。

### TiDB を物理マシンまたは仮想マシンにデプロイて運用する - TiUP {#deploy-and-operate-tidb-on-physical-or-virtual-machines-tiup}

[<a href="/tiup/tiup-overview.md">TiUP</a>](/tiup/tiup-overview.md)は、物理マシンまたは仮想マシン上の TiDB パッケージ マネージャーです。 TiUP は、 TiDB、PD、TiKV などの複数の TiDB コンポーネントを管理できます。 TiDB エコシステム内のコンポーネントを開始するには、 TiUPコマンドを 1 行実行するだけです。

TiUP は、 Golangで書かれたクラスター管理コンポーネント[<a href="https://github.com/pingcap/tiup/tree/master/components/cluster">TiUPクラスター</a>](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。 TiUPクラスターを使用すると、TiDB クラスターのデプロイ、開始、停止、破棄、スケーリング、アップグレードなどの日常的なデータベース操作を簡単に実行し、TiDB クラスターのパラメーターを管理できます。

TiUPの基本は次のとおりです。

-   [<a href="/tiup/tiup-terminology-and-concepts.md">用語と概念</a>](/tiup/tiup-terminology-and-concepts.md)
-   [<a href="/production-deployment-using-tiup.md">TiUPを使用した TiDBクラスタのデプロイ</a>](/production-deployment-using-tiup.md)
-   [<a href="/tiup/tiup-component-management.md">TiUPコマンドを使用してTiUPコンポーネントを管理する</a>](/tiup/tiup-component-management.md)
-   該当する TiDB バージョン: v4.0 以降のバージョン

### TiDB on Kubernetes のデプロイと運用 - TiDB Operator {#deploy-and-operate-tidb-on-kubernetes-tidb-operator}

[<a href="https://github.com/pingcap/tidb-operator">TiDB Operator</a>](https://github.com/pingcap/tidb-operator)は、Kubernetes上でTiDBクラスターを管理するための自動運用システムです。導入、アップグレード、スケーリング、バックアップ、構成変更など、TiDB の完全なライフサイクル管理を提供します。 TiDB Operatorを使用すると、TiDB はパブリック クラウドまたはプライベート クラウドにデプロイされた Kubernetes クラスター内でシームレスに実行できます。

TiDB Operatorの基本は次のとおりです。

-   [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture">TiDB Operatorのアーキテクチャ</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
-   [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/">Kubernetes でTiDB Operatorを使ってみる</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
-   該当する TiDB バージョン: v2.1 以降のバージョン

## データ管理ツール {#data-management-tools}

TiDB は、インポートとエクスポート、バックアップと復元、増分データ レプリケーション、データ検証などの複数のデータ管理ツールを提供します。

### データ移行 - TiDB データ移行 (DM) {#data-migration-tidb-data-migration-dm}

[<a href="/dm/dm-overview.md">TiDB データ移行</a>](/dm/dm-overview.md) (DM) は、MySQL/MariaDB から TiDB への完全なデータ移行と増分データ レプリケーションをサポートするツールです。

DMの基本は以下の通りです。

-   ソース: MySQL/MariaDB
-   ターゲット: TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes サポート: TiDB DM を Kubernetes にデプロイするには[<a href="https://github.com/pingcap/tidb-operator">TiDB Operator</a>](https://github.com/pingcap/tidb-operator)を使用します。

データ量が 1 TB 未満の場合は、DM を使用して MySQL/MariaDB から TiDB にデータを直接移行することをお勧めします。移行プロセスには、完全なデータ移行と増分データ レプリケーションが含まれます。

データボリュームが 1 TB を超える場合は、次の手順を実行します。

1.  MySQL/MariaDB から完全なデータをエクスポートするには[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)を使用します。
2.  ステップ 1 でエクスポートしたデータを TiDB クラスターにインポートするには、 [<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a>](/tidb-lightning/tidb-lightning-overview.md)使用します。
3.  TiDB DM を使用して、増分データを MySQL/MariaDB から TiDB にレプリケートします。

> **ノート：**
>
> Syncer ツールはメンテナンスされなくなりました。 Syncer に関連するシナリオでは、DM を使用して増分レプリケーションを実行することをお勧めします。

### フルデータのエクスポート -Dumpling {#full-data-export-dumpling}

[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md) MySQL または TiDB からの論理完全データ エクスポートをサポートします。

Dumplingの基本は以下の通りです。

-   出典: MySQL/TiDB クラスター
-   出力: SQL/CSV ファイル
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes のサポート: いいえ

> **ノート：**
>
> PingCAP は以前、TiDB に固有の拡張機能を備えた[<a href="https://github.com/maxbube/mydumper">マイダンパープロジェクト</a>](https://github.com/maxbube/mydumper)のフォークを維持していました。その後、このフォークはGolangで書き直された[<a href="/dumpling-overview.md">Dumpling</a>](/dumpling-overview.md)に置き換えられ、TiDB に固有の最適化がさらに強化されました。 mydumper の代わりにDumpling を使用することを強くお勧めします。

### 完全なデータのインポート - TiDB Lightning {#full-data-import-tidb-lightning}

[<a href="/tidb-lightning/tidb-lightning-overview.md">TiDB Lightning</a>](/tidb-lightning/tidb-lightning-overview.md) TiDB クラスターへの大規模なデータセットの完全なデータ インポートをサポートします。

TiDB Lightning は次のモードをサポートします。

-   `Physical Import Mode` : TiDB Lightning はデータを順序付けされたキーと値のペアに解析し、それらを TiKV に直接インポートします。このモードは通常、大量のデータ (TB レベル) を新しいクラスターにインポートするためのものです。インポート中、クラスターはサービスを提供できません。
-   `Logical Import Mode` : このモードはバックエンドとして TiDB/MySQL を使用します。これは`Physical Import Mode`よりも遅くなりますが、オンラインで実行できます。 MySQL へのデータのインポートもサポートしています。

TiDB Lightningの基本は次のとおりです。

-   情報元：
    -   Dumplingの出力ファイル
    -   その他の互換性のある CSV ファイル
    -   Amazon Auroraまたは Apache Hive からエクスポートされた Parquet ファイル
-   サポートされている TiDB バージョン: v2.1 以降のバージョン
-   Kubernetes のサポート: はい。詳細については[<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning">TiDB Lightningを使用して、Kubernetes 上の TiDB クラスターにデータを迅速に復元します</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)を参照してください。

> **ノート：**
>
> ローダー ツールはメンテナンスされなくなりました。ローダーに関連するシナリオでは、代わりに`Logical Import Mode`を使用することをお勧めします。

### バックアップと復元 - バックアップと復元 (BR) {#backup-and-restore-backup-x26-restore-br}

[<a href="/br/backup-and-restore-overview.md">復元する</a>](/br/backup-and-restore-overview.md) (BR) は、TiDB クラスター データの分散バックアップおよび復元のためのコマンドライン ツールです。 BR は、膨大なデータ量の TiDB クラスターを効果的にバックアップおよび復元できます。

BRの基本は次のとおりです。

-   入力および出力データ ソース

    -   スナップショットのバックアップと復元: [<a href="/br/br-snapshot-architecture.md#backup-files">SST + `backupmeta`ファイル</a>](/br/br-snapshot-architecture.md#backup-files)
    -   ログバックアップとPITR： [<a href="/br/br-log-architecture.md#log-backup-files">ログバックアップファイル</a>](/br/br-log-architecture.md#log-backup-files)

-   サポートされている TiDB バージョン: v4.0 以降のバージョン

-   Kubernetes のサポート: はい。詳細については、 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br">BRを使用して S3 互換ストレージにデータをバックアップする</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)と[<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br">BRを使用して S3 互換ストレージからデータを復元する</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)を参照してください。

### 増分データ レプリケーション - TiCDC {#incremental-data-replication-ticdc}

[<a href="/ticdc/ticdc-overview.md">TiCDC</a>](/ticdc/ticdc-overview.md)は、TiKV から変更ログを取得して、TiDB の増分データをレプリケートするために使用されるツールです。データをアップストリームの TSO と一致する状態に復元できます。 TiCDC は、他のシステムによるデータ変更のサブスクライブをサポートする TiCDC オープン プロトコルも提供します。

TiCDC の基本は次のとおりです。

-   出典: TiDB クラスター
-   ターゲット: TiDB クラスター、MySQL、Kafka、Confluent
-   サポートされている TiDB バージョン: v4.0.6 以降のバージョン

### 増分ログ複製 - TiDB Binlog {#incremental-log-replication-tidb-binlog}

[<a href="/tidb-binlog/tidb-binlog-overview.md">TiDBBinlog</a>](/tidb-binlog/tidb-binlog-overview.md)は、TiDB クラスターのbinlogを収集し、ほぼリアルタイムのデータ レプリケーションとバックアップを提供するツールです。 TiDB クラスターをプライマリ TiDB クラスターのセカンダリ クラスターにするなど、TiDB クラスター間の増分データ レプリケーションに使用できます。

TiDB Binlogの基本は次のとおりです。

-   出典: TiDB クラスター
-   ターゲット: TiDB クラスター、MySQL、Kafka、または増分バックアップ ファイル
-   サポートされている TiDB バージョン: v2.1 以降のバージョン
-   Kubernetes のサポート: はい。詳細については、 [<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog">TiDBBinlogクラスタの操作</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog)と[<a href="https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer">Kubernetes での TiDBBinlogDrainer構成</a>](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer)を参照してください。

### 同期差分インスペクター {#sync-diff-inspector}

[<a href="/sync-diff-inspector/sync-diff-inspector-overview.md">同期差分インスペクター</a>](/sync-diff-inspector/sync-diff-inspector-overview.md)は、MySQL または TiDB データベースに保存されているデータを比較するツールです。さらに、少量のデータに一貫性がないシナリオでは、sync-diff-inspector を使用してデータを修復することもできます。

以下は sync-diff-inspector の基本です。

-   出典: MySQL/TiDB クラスター
-   ターゲット: MySQL/TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン

## OLAP クエリツール - TiSpark {#olap-query-tool-tispark}

[<a href="/tispark-overview.md">ティスパーク</a>](/tispark-overview.md)複雑な OLAP クエリに対処するために PingCAP によって開発された製品です。 Spark の強み、分散 TiKV クラスターと TiDB の機能を組み合わせて、ワンストップのハイブリッド トランザクションおよび分析処理 (HTAP) ソリューションを提供します。
