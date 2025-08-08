---
title: TiDB Tools Overview
summary: ツールと適用可能なシナリオを学習します。
---

# TiDB ツールの概要 {#tidb-tools-overview}

TiDBは、TiDBの導入と保守、データ管理（データ移行、バックアップと復元、データ比較など）、TiKV上でのSpark SQLの実行を支援する豊富なツールセットを提供しています。ニーズに応じて適切なツールを選択できます。

## 導入・運用ツール {#deployment-and-operation-tools}

TiDB は、さまざまなシステム環境での導入および運用のニーズを満たすために、 TiUPとTiDB Operatorを提供します。

### 物理マシンまたは仮想マシンに TiDBをデプロイ運用する - TiUP {#deploy-and-operate-tidb-on-physical-or-virtual-machines-tiup}

[TiUP](/tiup/tiup-overview.md) 、物理マシンまたは仮想マシン上のTiDBパッケージマネージャです。TiUPは、TiDB、PD、TiKVなど、複数のTiDBコンポーネントを管理できます。TiDBエコシステム内の任意のコンポーネントを起動するには、 TiUPコマンドを1行実行するだけです。

TiUPは、 Golangで記述されたクラスタ管理コンポーネント[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)提供します。TiUPクラスタを使用することで、 TiUPクラスタのデプロイ、起動、停止、破棄、スケーリング、アップグレードといった日常的なデータベース操作や、TiDBクラスタパラメータの管理を容易に行うことができます。

TiUPの基本は次のとおりです。

-   [用語と概念](/tiup/tiup-terminology-and-concepts.md)
-   [TiUPを使用して TiDBクラスタをデプロイ](/production-deployment-using-tiup.md)
-   [TiUPコマンドを使用してTiUPコンポーネントを管理する](/tiup/tiup-component-management.md)
-   適用可能な TiDB バージョン: v4.0 以降

### Kubernetes 上で TiDBをデプロイ運用する - TiDB Operator {#deploy-and-operate-tidb-on-kubernetes-tidb-operator}

[TiDB Operator](https://github.com/pingcap/tidb-operator) 、Kubernetes上でTiDBクラスタを管理するための自動運用システムです。デプロイメント、アップグレード、スケーリング、バックアップ、設定変更など、TiDBのライフサイクル全体を管理します。TiDB TiDB Operatorを使用することで、パブリッククラウドまたはプライベートクラウドにデプロイされたKubernetesクラスタ内でTiDBをシームレスに実行できます。

TiDB Operatorの基本は次のとおりです。

-   [TiDB Operatorアーキテクチャ](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
-   [Kubernetes でTiDB Operatorを使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
-   適用可能な TiDB バージョン: v2.1 以降

## データ管理ツール {#data-management-tools}

TiDB は、インポートとエクスポート、バックアップと復元、増分データレプリケーション、データ検証など、複数のデータ管理ツールを提供します。

### データ移行 - TiDB データ移行 (DM) {#data-migration-tidb-data-migration-dm}

[TiDBデータ移行](/dm/dm-overview.md) (DM) は、MySQL/MariaDB から TiDB への完全なデータ移行と増分データレプリケーションをサポートするツールです。

DM の基本は次のとおりです。

-   出典: MySQL/MariaDB
-   ターゲット: TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes サポート: Kubernetes に TiDB DM をデプロイするには[TiDB Operator](https://github.com/pingcap/tidb-operator)使用します。

データ量が1TB未満の場合は、DMを使用してMySQL/MariaDBからTiDBに直接データを移行することをお勧めします。移行プロセスには、完全なデータ移行と増分データレプリケーションが含まれます。

データ量が 1 TB を超える場合は、次の手順を実行します。

1.  MySQL/MariaDB から完全なデータをエクスポートするには、 [Dumpling](/dumpling-overview.md)使用します。
2.  [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)使用して、手順 1 でエクスポートしたデータを TiDB クラスターにインポートします。
3.  TiDB DM を使用して、MySQL/MariaDB から TiDB に増分データを複製します。

> **注記：**
>
> Syncerツールはメンテナンスが終了しました。Syncerに関連するシナリオでは、DMを使用して増分レプリケーションを実行することをお勧めします。

### 完全なデータエクスポート - Dumpling {#full-data-export-dumpling}

[Dumpling](/dumpling-overview.md) 、MySQL または TiDB からの論理的な完全データ エクスポートをサポートします。

Dumplingの基本は次のとおりです。

-   出典: MySQL/TiDB クラスタ
-   出力: SQL/CSV ファイル
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetesサポート: いいえ

> **注記：**
>
> PingCAPは以前、TiDBに特化した機能強化を加えたバージョン[mydumperプロジェクト](https://github.com/maxbube/mydumper)のフォークを保守していました。バージョン7.5.0以降、 [マイダンパー](https://docs-archive.pingcap.com/tidb/v4.0/mydumper-overview/)非推奨となり、その機能の大部分は[Dumpling](/dumpling-overview.md)に置き換えられました。mydumperではなくDumplingを使用することを強くお勧めします。

### 完全なデータインポート - TiDB Lightning {#full-data-import-tidb-lightning}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 、大規模なデータセットの TiDB クラスターへの完全なデータインポートをサポートします。

TiDB Lightning は次のモードをサポートしています。

-   `Physical Import Mode` : TiDB Lightningはデータを順序付けられたキーと値のペアに解析し、TiKVに直接インポートします。このモードは通常、テラバイト単位の大容量データを新しいクラスターにインポートするために使用されます。インポート中は、クラスターはサービスを提供できません。
-   `Logical Import Mode` ：このモードでは、バックエンドとしてTiDB/MySQLを使用します。2 `Physical Import Mode`も速度は遅いですが、オンラインで実行できます。また、MySQLへのデータのインポートもサポートしています。

TiDB Lightningの基本は次のとおりです。

-   データソース:
    -   Dumplingの出力ファイル
    -   その他の互換性のあるCSVファイル
    -   Amazon Aurora、Apache Hive、またはSnowflakeからエクスポートされたParquetファイル
-   サポートされている TiDB バージョン: v2.1 以降
-   Kubernetes サポート: はい。詳細は[TiDB Lightningを使用して Kubernetes 上の TiDB クラスターにデータを迅速に復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)参照してください。

> **注記：**
>
> Loaderツールはメンテナンスされなくなりました。Loaderに関連するシナリオでは、代わりに`Logical Import Mode`使用することをお勧めします。

### バックアップと復元 - バックアップと復元 (BR) {#backup-and-restore-backup-x26-restore-br}

[バックアップと復元](/br/backup-and-restore-overview.md) (BR) は、TiDB クラスターデータの分散バックアップとリストアのためのコマンドラインツールです。BRは、膨大なデータ量の TiDB クラスターを効率的にバックアップおよびリストアできます。

BRの基本は次のとおりです。

-   入力および出力データソース

    -   スナップショットのバックアップと復元: [SST + `backupmeta`ファイル](/br/br-snapshot-architecture.md#backup-files)
    -   ログバックアップとPITR: [ログバックアップファイル](/br/br-log-architecture.md#log-backup-files)

-   サポートされている TiDB バージョン: v4.0 以降

-   Kubernetes サポート: はい。詳細は[BRを使用して S3 互換ストレージにデータをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)と[BRを使用して S3 互換ストレージからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)参照してください。

### 増分データレプリケーション - TiCDC {#incremental-data-replication-ticdc}

[TiCDC](/ticdc/ticdc-overview.md) 、TiKVから変更ログを取得することでTiDBの増分データを複製するためのツールです。上流のTSOと整合性のある状態にデータを復元できます。TiCDCは、他のシステムがデータ変更をサブスクライブできるように、TiCDCオープンプロトコルも提供しています。

TiCDC の基本は次のとおりです。

-   出典: TiDB クラスター
-   対象: TiDB クラスター、MySQL、Kafka、Confluent
-   サポートされている TiDB バージョン: v4.0.6 以降

### 同期差分インスペクター {#sync-diff-inspector}

[同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md) 、MySQLまたはTiDBデータベースに保存されているデータを比較するツールです。また、少量のデータに不整合がある場合、sync-diff-inspectorを使用してデータを修復することもできます。

sync-diff-inspector の基本は次のとおりです。

-   出典: MySQL/TiDB クラスタ
-   ターゲット: MySQL/TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン

## OLAPクエリツール - TiSpark {#olap-query-tool-tispark}

[ティスパーク](/tispark-overview.md) 、OLAPクエリの複雑さに対処するためにPingCAPが開発した製品です。Sparkの強みと、分散型TiKVクラスターおよびTiDBの機能を組み合わせることで、ワンストップのハイブリッドトランザクションおよび分析処理（HTAP）ソリューションを提供します。
