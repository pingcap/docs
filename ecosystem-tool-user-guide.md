---
title: TiDB Tools Overview
---

# TiDB ツールの概要 {#tidb-tools-overview}

TiDB は、展開操作、データ管理 (インポートとエクスポート、データ移行、バックアップと回復など)、および複雑な OLAP クエリを支援する豊富なツール セットを提供します。必要に応じて適切なツールを選択できます。

## 導入および運用ツール {#deployment-and-operation-tools}

さまざまなシステム環境での展開と運用のニーズを満たすために、TiDB は、TiUP とTiDB Operatorという 2 つの展開および運用ツールを提供します。

### TiDB を物理マシンまたは仮想マシンにデプロイして操作する {#deploy-and-operate-tidb-on-physical-or-virtual-machines}

[TiUP](/tiup/tiup-overview.md)は、物理マシンまたは仮想マシン上の TiDB パッケージ マネージャーです。 TiUP は、TiDB、PD、TiKV などの複数の TiDB コンポーネントを管理できます。 TiDB エコシステムの任意のコンポーネントを開始するには、TiUP コマンドを 1 つ実行するだけです。

TiUP は、Golang で記述されたクラスター管理コンポーネントである[TiUPクラスター](https://github.com/pingcap/tiup/tree/master/components/cluster)を提供します。 TiUP クラスターを使用すると、TiDB クラスターのデプロイ、開始、停止、破棄、スケーリング、およびアップグレードを含む日常のデータベース操作を簡単に実行し、TiDB クラスターのパラメーターを管理できます。

TiUP の基本は次のとおりです。

-   [用語と概念](/tiup/tiup-terminology-and-concepts.md)
-   [TiUP を使用して TiDBクラスタをデプロイする](/production-deployment-using-tiup.md)
-   [TiUP コマンドで TiUP コンポーネントを管理する](/tiup/tiup-component-management.md)
-   該当する TiDB バージョン: v4.0 以降

### TiDB を Kubernetes にデプロイして運用する {#deploy-and-operate-tidb-in-kubernetes}

[TiDB Operator](https://github.com/pingcap/tidb-operator)は Kubernetes の TiDB クラスターの自動運用システムです。展開、アップグレード、スケーリング、バックアップ、フェイルオーバー、構成変更など、TiDB の完全なライフサイクル管理を提供します。 TiDB Operatorを使用すると、パブリック クラウドまたはプライベート クラウドにデプロイされた Kubernetes クラスターで TiDB をシームレスに実行できます。

TiDB Operatorの基本は次のとおりです。

-   [TiDB Operatorのアーキテクチャ](https://docs.pingcap.com/tidb-in-kubernetes/stable/architecture)
-   [Kubernetes でTiDB Operatorを使い始める](https://docs.pingcap.com/tidb-in-kubernetes/stable/get-started/)
-   該当する TiDB バージョン: v2.1 以降

## データ管理ツール {#data-management-tools}

TiDB は、インポートとエクスポート、バックアップと復元、データ複製、データ移行、増分同期、データ検証など、複数のデータ管理ツールを提供します。

### 完全なデータのエクスポート {#full-data-export}

[Dumpling](/dumpling-overview.md)は、MySQL または TiDB から論理的にフル データをエクスポートするためのツールです。

Dumplingの基本は次のとおりです。

-   入力: MySQL/TiDB クラスター
-   出力: SQL/CSV ファイル
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes のサポート: いいえ

> **ノート：**
>
> PingCAP は以前、TiDB に固有の拡張機能を備えた[mydumper プロジェクト](https://github.com/maxbube/mydumper)のフォークを維持していました。このフォークはその後、Go で書き直された[Dumpling](/dumpling-overview.md)に置き換えられ、TiDB に固有のより多くの最適化をサポートしています。 mydumper の代わりにDumplingを使用することを強くお勧めします。

### 完全なデータのインポート {#full-data-import}

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) (Lightning) は、大量のデータを TiDB クラスターに完全にインポートするために使用されるツールです。現在、 TiDB LightningはDumplingまたは CSV データ ソース経由でエクスポートされた SQL ダンプの読み取りをサポートしています。

TiDB Lightningは 3 つのモードをサポートしています。

-   `local` : TiDB Lightningはデータを順序付けられたキーと値のペアに解析し、TiKV に直接インポートします。このモードは通常、大量のデータ (TB レベル) を新しいクラスターにインポートするためのものです。インポート中、クラスターはサービスを提供できません。
-   `importer` : このモードは`local`モードに似ています。このモードを使用するには、追加のコンポーネント`tikv-importer`をデプロイして、キーと値のペアをインポートできるようにする必要があります。ターゲット クラスタが v4.0 以降のバージョンの場合は、 `local`モードを使用することをお勧めします。
-   `tidb` : このモードは、TiDB/MySQL をバックエンドとして使用します。これは、 `local`モードおよび`importer`モードよりも低速ですが、オンラインで実行できます。また、MySQL へのデータのインポートもサポートしています。

TiDB Lightningの基本は次のとおりです。

-   入力データ ソース:
    -   Dumplingの出力ファイル
    -   その他の互換性のある CSV ファイル
-   サポートされている TiDB のバージョン: v2.1 以降
-   Kubernetes のサポート: はい。詳細は[TiDB Lightningを使用して、Kubernetes の TiDB クラスターにデータをすばやく復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-data-using-tidb-lightning)を参照してください。

> **ノート：**
>
> ローダー ツールはメンテナンスされなくなりました。ローダーに関連するシナリオでは、代わりに TiDB バックエンドを使用することをお勧めします。

### バックアップと復元 {#backup-and-restore}

[復元する](/br/backup-and-restore-overview.md) (BR) は、TiDB クラスター データの分散バックアップおよび復元用のコマンド ライン ツールです。 BR は、膨大なデータ量の TiDB クラスターを効果的にバックアップおよび復元できます。

BR の基本は次のとおりです。

-   [入力および出力データ ソース](/br/backup-and-restore-design.md#types-of-backup-files) : SST + `backupmeta`ファイル
-   サポートされている TiDB バージョン: v3.1 および v4.0
-   Kubernetes のサポート: はい。詳細については、 [BR を使用して S3 互換ストレージにデータをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/stable/backup-to-aws-s3-using-br)と[BR を使用して S3 互換ストレージからデータを復元する](https://docs.pingcap.com/tidb-in-kubernetes/stable/restore-from-aws-s3-using-br)を参照してください。

### 増分データ複製 {#incremental-data-replication}

[Binlog](/tidb-binlog/tidb-binlog-overview.md)は、TiDB クラスターの binlog を収集し、ほぼリアルタイムの同期とバックアップを提供するツールです。 TiDB クラスタをプライマリ TiDB クラスタのセカンダリ クラスタにするなど、TiDB クラスタ間の増分データ レプリケーションに使用できます。

TiDB Binlogの基本は次のとおりです。

-   入出力：
    -   入力: TiDB クラスター
    -   出力: TiDB クラスター、MySQL、Kafka、または増分バックアップ ファイル
-   サポートされている TiDB のバージョン: v2.1 以降
-   Kubernetes のサポート: はい。詳細については、 [TiDB Binlogクラスタの操作](https://docs.pingcap.com/tidb-in-kubernetes/stable/deploy-tidb-binlog)と[Kubernetes での TiDB BinlogDrainer](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-tidb-binlog-drainer)を参照してください。

### データ移行 {#data-migration}

[TiDB データ移行](/dm/dm-overview.md) (DM) は、MySQL/MariaDB から TiDB への完全なデータ移行と増分データ レプリケーションをサポートする統合データ レプリケーション タスク管理プラットフォームです。

DMの基本は以下の通りです。

-   入力: MySQL/MariaDB
-   出力: TiDB クラスター
-   サポートされている TiDB バージョン: すべてのバージョン
-   Kubernetes のサポート: いいえ、開発中です

データ量が TB レベルを下回る場合は、DM を使用して直接 MySQL/MariaDB から TiDB にデータを移行することをお勧めします。移行プロセスには、完全なデータのインポートとエクスポート、および増分データの複製が含まれます。

データ ボリュームが TB レベルの場合は、次の手順を実行します。

1.  [Dumpling](/dumpling-overview.md)を使用して、MySQL/MariaDB から完全なデータをエクスポートします。
2.  [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)を使用して、手順 1 でエクスポートしたデータを TiDB クラスターにインポートします。
3.  DM を使用して、MySQL/MariaDB から TiDB に増分データを複製します。

> **ノート：**
>
> Syncer ツールはメンテナンスされなくなりました。 Syncer に関連するシナリオでは、代わりに DM のインクリメンタル タスク モードを使用することをお勧めします。

## OLAP クエリ ツール {#olap-query-tool}

TiDB は OLAP クエリ ツール TiSpark を提供します。これにより、ネイティブの Spark を使用しているかのように TiDB テーブルにクエリを実行できます。

### Spark を使用して TiKV データ ソースにクエリを実行する {#query-tikv-data-source-using-spark}

[ティスパーク](/tispark-overview.md)は、TiKV 上で Apache Spark を実行して複雑な OLAP クエリに応答するために構築されたシンレイヤーです。 Spark プラットフォームと分散 TiKV クラスターの両方を利用し、TiDB にシームレスに接着し、ワンストップのハイブリッド トランザクションおよび分析処理 (HTAP) ソリューションを提供します。
