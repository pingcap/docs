---
title: TiDB Tools Overview
summary: ツールと適用可能なシナリオを学習します。
---

# TiDB ツールの概要 {#tidb-tools-overview}

TiDB は、TiDB の導入と保守、データの管理 (データの移行、バックアップと復元、データの比較など)、TiKV での Spark SQL の実行に役立つ豊富なツール セットを提供します。ニーズに応じて適切なツールを選択できます。

## 導入・運用ツール {#deployment-and-operation-tools}

TiDB は、さまざまなシステム環境での展開と運用のニーズを満たすために、 TiUPとTiDB Operator を提供します。

### 物理マシンまたは仮想マシンに TiDB をデプロイて運用する - TiUP {#deploy-and-operate-tidb-on-physical-or-virtual-machines-tiup}

[TiUP](/tiup/tiup-overview.md) 、物理マシンまたは仮想マシン上の TiDB パッケージ マネージャーです。TiUPは、 TiDB、PD、TiKV などの複数の TiDB コンポーネントを管理できます。TiDB エコシステム内の任意のコンポーネントを起動するには、 TiUPコマンドを 1 行実行するだけです。

TiUP は、 Golangで記述されたクラスタ管理コンポーネント[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。TiUP クラスタを使用すると、 TiUPクラスタのデプロイ、起動、停止、破棄、スケーリング、アップグレードなどの日常的なデータベース操作を簡単に実行し、TiDB クラスタのパラメータを管理できます。

TiUPの基本は次のとおりです。

-   [用語と概念](/tiup/tiup-terminology-and-concepts.md)
-   [TiUP を使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)
-   [TiUPTiUPを管理する](/tiup/tiup-component-management.md)
-   適用可能な TiDB バージョン: v4.0 以降

### Kubernetes 上で TiDB をデプロイて運用する - TiDB Operator {#deploy-and-operate-tidb-on-kubernetes-tidb-operator}

[TiDB Operator](https://github.com/pingcap/tidb-operator) 、Kubernetes 上の TiDB クラスターを管理するための自動運用システムです。デプロイメント、アップグレード、スケーリング、バックアップ、構成変更など、TiDB のライフサイクル全体を管理します。TiDB TiDB Operatorを使用すると、パブリック クラウドまたはプライベート クラウドにデプロイされた Kubernetes クラスターで TiDB をシームレスに実行できます。

TiDB Operatorの基本は次のとおりです。

-   [TiDB Operatorアーキテクチャ](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
-   [Kubernetes でTiDB Operatorを使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
-   適用可能な TiDB バージョン: v2.1 以降

## データ管理ツール {#data-management-tools}

TiDB は、インポートとエクスポート、バックアップと復元、増分データ複製、データ検証などの複数のデータ管理ツールを提供します。

### データ移行 - TiDB データ移行 (DM) {#data-migration-tidb-data-migration-dm}

[TiDB データ移行](/dm/dm-overview.md) (DM) は、MySQL/MariaDB から TiDB への完全なデータ移行と増分データレプリケーションをサポートするツールです。

DM の基本は次のとおりです。

-   出典: MySQL/MariaDB
-   ターゲット: TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes サポート: Kubernetes に TiDB DM をデプロイするには[TiDB Operator](https://github.com/pingcap/tidb-operator)使用します。

データ量が 1 TB 未満の場合は、DM を使用して MySQL/MariaDB から TiDB にデータを直接移行することをお勧めします。移行プロセスには、完全なデータ移行と増分データレプリケーションが含まれます。

データ量が 1 TB を超える場合は、次の手順を実行します。

1.  MySQL/MariaDB から完全なデータをエクスポートするには[Dumpling](/dumpling-overview.md)使用します。
2.  [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して、手順 1 でエクスポートしたデータを TiDB クラスターにインポートします。
3.  TiDB DM を使用して、MySQL/MariaDB から TiDB に増分データを複製します。

> **注記：**
>
> Syncer ツールはメンテナンスされなくなりました。Syncer に関連するシナリオでは、増分レプリケーションを実行するために DM を使用することをお勧めします。

### 完全なデータエクスポート - Dumpling {#full-data-export-dumpling}

[Dumpling](/dumpling-overview.md) MySQL または TiDB からの論理的な完全データ エクスポートをサポートします。

Dumplingの基本は次のとおりです。

-   出典: MySQL/TiDB クラスター
-   出力: SQL/CSV ファイル
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes サポート: いいえ

> **注記：**
>
> PingCAP は以前、TiDB 固有の機能強化を加えた[mydumper プロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。v7.5.0 以降、 [マイダンパー](https://docs.pingcap.com/tidb/v4.0/mydumper-overview)非推奨となり、その機能のほとんどが[Dumpling](/dumpling-overview.md)に置き換えられました。mydumper ではなくDumpling を使用することを強くお勧めします。

### 完全なデータインポート - TiDB Lightning {#full-data-import-tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)大規模なデータセットの TiDB クラスターへの完全なデータ インポートをサポートします。

TiDB Lightning は次のモードをサポートしています。

-   `Physical Import Mode` : TiDB Lightning はデータを順序付けられたキーと値のペアに解析し、それらを TiKV に直接インポートします。このモードは通常、大量のデータ (TB レベル) を新しいクラスターにインポートするためのものです。インポート中、クラスターはサービスを提供できません。
-   `Logical Import Mode` : このモードでは、バックエンドとして TiDB/MySQL を使用します`Physical Import Mode`よりも低速ですが、オンラインで実行できます。また、MySQL へのデータのインポートもサポートしています。

TiDB Lightningの基本は次のとおりです。

-   データソース:
    -   Dumplingの出力ファイル
    -   その他の互換性のあるCSVファイル
    -   Amazon Auroraまたは Apache Hive からエクスポートされた Parquet ファイル
-   サポートされている TiDB バージョン: v2.1 以降
-   Kubernetes サポート: はい。詳細については[TiDB Lightningを使用して Kubernetes 上の TiDB クラスターにデータをすばやく復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)参照してください。

> **注記：**
>
> Loader ツールはメンテナンスされなくなりました。Loader に関連するシナリオでは、代わりに`Logical Import Mode`使用することをお勧めします。

### バックアップと復元 - バックアップと復元 (BR) {#backup-and-restore-backup-x26-restore-br}

[バックアップと復元](/br/backup-and-restore-overview.md) (BR) は、TiDB クラスター データの分散バックアップと復元のためのコマンドライン ツールです。BRは、膨大なデータ量の TiDB クラスターを効率的にバックアップおよび復元できます。

BRの基本は次のとおりです。

-   入力および出力データソース

    -   スナップショットのバックアップと復元: [SST + `backupmeta`ファイル](/br/br-snapshot-architecture.md#backup-files)
    -   ログバックアップとPITR: [ログバックアップファイル](/br/br-log-architecture.md#log-backup-files)

-   サポートされている TiDB バージョン: v4.0 以降

-   Kubernetes サポート: はい。詳細については[BR を使用して S3 互換ストレージにデータをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)と[BRを使用して S3 互換ストレージからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)参照してください。

### 増分データレプリケーション - TiCDC {#incremental-data-replication-ticdc}

[ティCDC](/ticdc/ticdc-overview.md) 、TiKV から変更ログを取得して TiDB の増分データを複製するために使用されるツールです。アップストリームの任意の TSO と一致する状態にデータを復元できます。TiCDC は、他のシステムがデータの変更をサブスクライブできるようにするための TiCDC オープン プロトコルも提供します。

TiCDC の基本は次のとおりです。

-   出典: TiDB クラスター
-   対象: TiDB クラスター、MySQL、Kafka、Confluent
-   サポートされている TiDB バージョン: v4.0.6 以降

### 同期差分インスペクター {#sync-diff-inspector}

[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) 、MySQL または TiDB データベースに保存されているデータを比較するツールです。また、少量のデータが不一致であるシナリオでは、sync-diff-inspector を使用してデータを修復することもできます。

sync-diff-inspector の基本は次のとおりです。

-   出典: MySQL/TiDB クラスター
-   ターゲット: MySQL/TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン

## OLAP クエリ ツール - TiSpark {#olap-query-tool-tispark}

[ティスパーク](/tispark-overview.md) 、OLAP クエリの複雑さに対処するために PingCAP によって開発された製品です。Spark の強みと、分散 TiKV クラスターおよび TiDB の機能を組み合わせて、ワンストップのハイブリッド トランザクションおよび分析処理 (HTAP) ソリューションを提供します。
