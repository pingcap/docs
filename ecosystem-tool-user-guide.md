---
title: TiDB Tools Overview
summary: Learn the tools and applicable scenarios.
---

# TiDB ツールの概要 {#tidb-tools-overview}

TiDB は、TiDB のデプロイと保守、データの管理 (データ移行、バックアップと復元、データ比較など)、および TiKV での Spark SQL の実行に役立つ豊富なツール セットを提供します。必要に応じて適切なツールを選択できます。

## 導入および運用ツール {#deployment-and-operation-tools}

TiDB は、さまざまなシステム環境での展開と運用のニーズを満たすために、 TiUPとTiDB Operatorを提供します。

### TiDB を物理マシンまたは仮想マシンにデプロイ操作する - TiUP {#deploy-and-operate-tidb-on-physical-or-virtual-machines-tiup}

[TiUP](/tiup/tiup-overview.md)は、物理マシンまたは仮想マシン上の TiDB パッケージ マネージャーです。 TiUP は、 TiDB、PD、TiKV などの複数の TiDB コンポーネントを管理できます。 TiDB エコシステムのコンポーネントを開始するには、 TiUPコマンドを 1 行実行するだけです。

TiUP は、 Golangで記述されたクラスター管理コンポーネント[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。 TiUPクラスターを使用すると、TiDB クラスターのデプロイ、開始、停止、破棄、スケーリング、およびアップグレードを含む日常のデータベース操作を簡単に実行し、TiDB クラスターのパラメーターを管理できます。

TiUPの基本は次のとおりです。

-   [用語と概念](/tiup/tiup-terminology-and-concepts.md)
-   [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)
-   [TiUPコマンドでTiUPコンポーネントを管理する](/tiup/tiup-component-management.md)
-   該当する TiDB バージョン: v4.0 以降のバージョン

### TiDB を Kubernetes にデプロイ運用する - TiDB Operator {#deploy-and-operate-tidb-on-kubernetes-tidb-operator}

[TiDB Operator](https://github.com/pingcap/tidb-operator)は、Kubernetes 上の TiDB クラスターを管理するための自動運用システムです。展開、アップグレード、スケーリング、バックアップ、および構成変更を含む、TiDB の完全なライフサイクル管理を提供します。 TiDB Operatorを使用すると、パブリック クラウドまたはプライベート クラウドにデプロイされた Kubernetes クラスターで TiDB をシームレスに実行できます。

TiDB Operatorの基本は次のとおりです。

-   [TiDB Operatorのアーキテクチャ](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
-   [Kubernetes でTiDB Operatorを使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
-   該当する TiDB バージョン: v2.1 以降のバージョン

## データ管理ツール {#data-management-tools}

TiDB は、インポートとエクスポート、バックアップと復元、増分データ複製、データ検証など、複数のデータ管理ツールを提供します。

### データ移行 - TiDB データ移行 (DM) {#data-migration-tidb-data-migration-dm}

[TiDB データ移行](/dm/dm-overview.md) (DM) は、MySQL/MariaDB から TiDB への完全なデータ移行と増分データ レプリケーションをサポートするツールです。

DMの基本は以下の通りです。

-   ソース: MySQL/MariaDB
-   ターゲット: TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes サポート: [TiDB Operator](https://github.com/pingcap/tidb-operator)を使用して、TiDB DM を Kubernetes にデプロイします。

データ量が 1 TB 未満の場合は、DM を使用して直接 MySQL/MariaDB から TiDB にデータを移行することをお勧めします。移行プロセスには、完全なデータ移行と増分データ レプリケーションが含まれます。

データ ボリュームが 1 TB を超える場合は、次の手順を実行します。

1.  [Dumpling](/dumpling-overview.md)使用して、MySQL/MariaDB から完全なデータをエクスポートします。
2.  [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して、手順 1 でエクスポートしたデータを TiDB クラスターにインポートします。
3.  TiDB DM を使用して、MySQL/MariaDB から TiDB に増分データを複製します。

> **ノート：**
>
> Syncer ツールはメンテナンスされなくなりました。 Syncer に関連するシナリオでは、DM を使用して増分レプリケーションを実行することをお勧めします。

### 完全なデータ エクスポート -Dumpling {#full-data-export-dumpling}

[Dumpling](/dumpling-overview.md) MySQL または TiDB からの論理フル データ エクスポートをサポートします。

Dumplingの基本は次のとおりです。

-   出典: MySQL/TiDB クラスター
-   出力: SQL/CSV ファイル
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes のサポート: いいえ

> **ノート：**
>
> PingCAP は以前、TiDB に固有の拡張機能を備えた[mydumper プロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。このフォークは、 Golangで書き直された[Dumpling](/dumpling-overview.md)に置き換えられ、TiDB に固有の最適化をさらに提供します。 mydumper の代わりにDumpling を使用することを強くお勧めします。

### 完全なデータのインポート - TiDB Lightning {#full-data-import-tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) TiDB クラスターへの大規模なデータセットの完全なデータ インポートをサポートします。

TiDB Lightning は次のモードをサポートしています。

-   `Physical Import Mode` : TiDB Lightning はデータを順序付けられたキーと値のペアに解析し、TiKV に直接インポートします。このモードは通常、大量のデータ (TB レベル) を新しいクラスターにインポートするためのものです。インポート中、クラスターはサービスを提供できません。
-   `Logical Import Mode` : このモードは、TiDB/MySQL をバックエンドとして使用します。これは`Physical Import Mode`よりも低速ですが、オンラインで実行できます。また、MySQL へのデータのインポートもサポートしています。

TiDB Lightningの基本は次のとおりです。

-   情報元：
    -   Dumplingの出力ファイル
    -   その他の互換性のある CSV ファイル
    -   Amazon Auroraまたは Apache Hive からエクスポートされた Parquet ファイル
-   サポートされている TiDB バージョン: v2.1 以降のバージョン
-   Kubernetes のサポート: はい。詳細は[TiDB Lightningを使用して、Kubernetes 上の TiDB クラスターにデータをすばやく復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)を参照してください。

> **ノート：**
>
> ローダー ツールはメンテナンスされなくなりました。ローダーに関連するシナリオでは、代わりに`Logical Import Mode`を使用することをお勧めします。

### バックアップと復元 - バックアップと復元 (BR) {#backup-and-restore-backup-x26-restore-br}

[復元する](/br/backup-and-restore-overview.md) (BR) は、TiDB クラスター データの分散バックアップおよび復元用のコマンド ライン ツールです。 BR は、膨大なデータ量の TiDB クラスターを効果的にバックアップおよび復元できます。

BRの基本は次のとおりです。

-   入力および出力データ ソース

    -   スナップショットのバックアップと復元: [SST + `backupmeta`ファイル](/br/br-snapshot-architecture.md#backup-files)
    -   ログのバックアップと PITR: [ログ バックアップ ファイル](/br/br-log-architecture.md#log-backup-files)

-   サポートされている TiDB バージョン: v4.0 以降のバージョン

-   Kubernetes のサポート: はい。詳細については、 [BRを使用して S3 互換ストレージにデータをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)と[BRを使用して S3 互換ストレージからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)を参照してください。

### 増分データ複製 - TiCDC {#incremental-data-replication-ticdc}

[TiCDC](/ticdc/ticdc-overview.md) 、TiKV から変更ログをプルして、TiDB の増分データを複製するために使用されるツールです。アップストリームの任意の TSO と一致する状態にデータを復元できます。 TiCDC は、データ変更をサブスクライブする他のシステムをサポートする TiCDC オープン プロトコルも提供します。

TiCDC の基本は次のとおりです。

-   出典: TiDB クラスター
-   ターゲット: TiDB クラスター、MySQL、Kafka、および Confluent
-   サポートされている TiDB バージョン: v4.0.6 以降のバージョン

### 増分ログ レプリケーション - TiDB Binlog {#incremental-log-replication-tidb-binlog}

[TiDBBinlog](/tidb-binlog/tidb-binlog-overview.md)は、TiDB クラスターのbinlog を収集し、ほぼリアルタイムのデータ複製とバックアップを提供するツールです。 TiDB クラスタをプライマリ TiDB クラスタのセカンダリ クラスタにするなど、TiDB クラスタ間の増分データ レプリケーションに使用できます。

TiDB Binlogの基本は次のとおりです。

-   出典: TiDB クラスター
-   ターゲット: TiDB クラスター、MySQL、Kafka、または増分バックアップ ファイル
-   サポートされている TiDB バージョン: v2.1 以降のバージョン
-   Kubernetes のサポート: はい。詳細については、 [TiDB Binlogクラスタの操作](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog)と[Kubernetes での TiDB Binlog Drainer構成](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer)を参照してください。

### 同期差分インスペクター {#sync-diff-inspector}

[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)は、MySQL または TiDB データベースに保存されているデータを比較するツールです。さらに、sync-diff-inspector を使用して、少量のデータに一貫性がないシナリオでデータを修復することもできます。

以下は、sync-diff-inspector の基本です。

-   出典: MySQL/TiDB クラスター
-   ターゲット: MySQL/TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン

## OLAP クエリ ツール - TiSpark {#olap-query-tool-tispark}

[ティスパーク](/tispark-overview.md)複雑な OLAP クエリに対処するために PingCAP によって開発された製品です。 Spark の強みと、分散型 TiKV クラスターおよび TiDB の機能を組み合わせて、ワンストップのハイブリッド トランザクションおよび分析処理 (HTAP) ソリューションを提供します。
