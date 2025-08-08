---
title: Data Migration Overview
summary: データ移行シナリオとソリューションの概要を学習します。
---

# データ移行の概要 {#data-migration-overview}

このドキュメントでは、TiDBで使用できるデータ移行ソリューションの概要を説明します。データ移行ソリューションは以下のとおりです。

-   完全なデータ移行。
    -   Amazon Auroraスナップショット、CSV ファイル、または SQL ダンプファイルを TiDB にインポートするには、 TiDB Lightningを使用して完全な移行を実行できます。
    -   すべての TiDB データを CSV ファイルまたは SQL ダンプ ファイルとしてエクスポートするには、 Dumplingを使用して完全な移行を実行できます。これにより、MySQL または MariaDB からのデータ移行が容易になります。
    -   データ サイズのボリュームが小さい (たとえば、1 TiB 未満) データベースからすべてのデータを移行するには、TiDB データ移行 (DM) を使用することもできます。

-   TiDBのクイック初期化。TiDB TiDB Lightningは、データの高速インポートをサポートし、TiDB内の特定のテーブルを高速に初期化できます。この機能を使用する前に、クイック初期化はTiDBに大きな影響を与え、初期化中はクラスタがサービスを提供できないことにご注意ください。

-   増分レプリケーション。TiDB DM を使用すると、MySQL、MariaDB、またはAuroraから TiDB にバイナリログをレプリケートできるため、レプリケーション期間中のウィンドウのダウンタイムが大幅に短縮されます。

-   TiDBクラスタ間のデータレプリケーション。TiDBはバックアップとリストアをサポートしています。この機能により、既存のTiDBクラスタのスナップショットを新しいTiDBクラスタに初期化できます。

-   TiDBクラスタ間の増分レプリケーション。TiDBは、同種データベース間のディザスタリカバリをサポートし、災害発生後のプライマリデータベースとセカンダリデータベースの最終的なデータ整合性を確保します。これは、プライマリクラスタとセカンダリクラスタの両方がTiDBである場合にのみ機能します。

データベースの種類、デプロイメントの場所、アプリケーションのデータサイズ、アプリケーションのニーズに応じて、さまざまな移行ソリューションを選択できます。以下のセクションでは、一般的な移行シナリオをいくつか紹介します。これらのセクションを参考に、ニーズに最適なソリューションを決定してください。

## Aurora MySQLからTiDBへのデータ移行 {#migrate-data-from-aurora-mysql-to-tidb}

Auroraから AWS にデプロイされた TiDB クラスターにデータを移行する場合、データ移行には完全なデータ移行と増分レプリケーションの 2 つの操作が必要です。アプリケーションのニーズに応じて、対応する操作を選択できます。

-   [Amazon Auroraから TiDB へのデータ移行](/migrate-aurora-to-tidb.md) 。

## MySQLからTiDBへのデータ移行 {#migrate-data-from-mysql-to-tidb}

クラウドstorage(S3) サービスを使用しておらず、ネットワーク接続が良好で、ネットワークレイテンシーが低い場合は、 [小規模データセットをMySQLからTiDBに移行する](/migrate-small-mysql-to-tidb.md)の手順に従って、MySQL から TiDB にデータを移行できます。

移行速度への要求が高い場合、またはデータサイズが大きい場合（例：1TiB以上）、かつ移行期間中に他のアプリケーションによるTiDBへの書き込みを許可しない場合は、 TiDB Lightningを使用してデータを迅速にインポートできます。その後、DMを使用して、アプリケーションのニーズに応じて増分データ（binlog）を複製できます。1 [大規模データセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)参照してください。

## MySQL シャードを TiDB に移行してマージする {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションでデータstorageにMySQLシャードを使用しており、これらのシャードを1つのテーブルとしてTiDBに移行する必要がある場合、DMを使用してシャードのマージと移行を実行できます。

-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)

シャードテーブルのデータサイズが大きく（例えば1TiB以上）、移行期間中に他のアプリケーションによるTiDBへの書き込みを許可しない場合は、 TiDB Lightningを使用してシャードテーブルを迅速にマージ・インポートできます。その後、DMを使用して、アプリケーションのニーズに応じて増分シャーディングデータ（binlog）を複製できます。

-   [大規模データセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## Vitess から TiDB へのデータの移行 {#migrate-data-from-vitess-to-tidb}

Vitess から TiDB にデータを移行するには、次のガイドが利用できます。

-   [Vitess から TiDB へのデータ移行](/migrate-from-vitess.md)

## ファイルから TiDB にデータを移行する {#migrate-data-from-files-to-tidb}

-   [CSVファイルからTiDBにデータを移行する](/migrate-from-csv-files-to-tidb.md)
-   [SQL ファイルから TiDB にデータを移行する](/migrate-from-sql-files-to-tidb.md)
-   [Parquet ファイルから TiDB にデータを移行する](/migrate-from-parquet-files-to-tidb.md)

## TiDB クラスタ間の増分レプリケーション {#incremental-replication-between-tidb-clusters}

TiCDCは、TiDBクラスタ間の増分データレプリケーションに使用できます。詳細については、 [TiCDCの概要](/ticdc/ticdc-overview.md)を参照してください。

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能により移行プロセスが改善され、アプリケーションのより多くのニーズを満たすことができる可能性があります。

-   [gh-ost または pt-osc を使用するデータベースからの継続的なレプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントをフィルタリングする](/filter-binlog-event.md)
-   [SQL 式を使用して DML イベントをフィルタリングする](/filter-dml-event.md)
