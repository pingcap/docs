---
title: Data Migration Overview
summary: データ移行シナリオとソリューションの概要を学習します。
aliases: ['/tidb/stable/migrate-full-data-from-mysql']
---

# データ移行の概要 {#data-migration-overview}

このドキュメントでは、TiDB で使用できるデータ移行ソリューションの概要を説明します。データ移行ソリューションは次のとおりです。

-   完全なデータ移行。
    -   Amazon Auroraスナップショット、CSV ファイル、または SQL ダンプファイルを TiDB にインポートするには、 TiDB Lightning を使用して完全な移行を実行できます。
    -   すべての TiDB データを CSV ファイルまたは SQL ダンプ ファイルとしてエクスポートするには、 Dumpling を使用して完全な移行を実行します。これにより、MySQL または MariaDB からのデータ移行が容易になります。
    -   データ サイズのボリュームが小さい (たとえば、1 TiB 未満) データベースからすべてのデータを移行するには、TiDB データ移行 (DM) を使用することもできます。

-   TiDB の迅速な初期化。TiDB TiDB Lightning は、データの迅速なインポートをサポートし、TiDB 内の特定のテーブルを迅速に初期化できます。この機能を使用する前に、迅速な初期化は TiDB に大きな影響を与え、初期化期間中はクラスターがサービスを提供しないことに注意してください。

-   増分レプリケーション。TiDB DM を使用すると、MySQL、MariaDB、またはAuroraから TiDB にバイナリログをレプリケートできるため、レプリケーション期間中のウィンドウのダウンタイムが大幅に短縮されます。

-   TiDB クラスター間のデータ レプリケーション。TiDB はバックアップと復元をサポートしています。この機能により、既存の TiDB クラスターのスナップショットを新しい TiDB クラスターに初期化できます。

-   TiDB クラスター間の増分レプリケーション。TiDB は、同種のデータベース間の災害復旧をサポートし、災害発生後のプライマリ データベースとセカンダリ データベースの最終的なデータ整合性を保証します。これは、プライマリ クラスターとセカンダリ クラスターの両方が TiDB である場合にのみ機能します。

データベースの種類、展開場所、アプリケーション データのサイズ、アプリケーションのニーズに応じて、さまざまな移行ソリューションを選択できます。次のセクションでは、一般的な移行シナリオをいくつか紹介します。これらのセクションを参照して、ニーズに応じて最適なソリューションを決定してください。

## Aurora MySQLからTiDBへのデータの移行 {#migrate-data-from-aurora-mysql-to-tidb}

Auroraから AWS にデプロイされた TiDB クラスターにデータを移行する場合、データ移行には完全なデータ移行と増分レプリケーションの 2 つの操作が必要です。アプリケーションのニーズに応じて、対応する操作を選択できます。

-   [Amazon Auroraから TiDB へのデータ移行](/migrate-aurora-to-tidb.md) 。

## MySQLからTiDBへのデータの移行 {#migrate-data-from-mysql-to-tidb}

クラウドstorage(S3) サービスを使用しておらず、ネットワーク接続が良好で、ネットワークレイテンシーが低い場合は、 [小規模データセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)手順に従って MySQL から TiDB にデータを移行できます。

移行速度に対する要求が高い場合、またはデータ サイズが大きい場合 (たとえば、1 TiB より大きい)、および移行期間中に他のアプリケーションによる TiDB への書き込みを許可しない場合は、 TiDB Lightning を使用してデータをすばやくインポートできます。その後、アプリケーションのニーズに基づいて、DM を使用して増分データ (binlog) を複製できます[大規模なデータセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)参照してください。

## MySQL シャードを TiDB に移行してマージする {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションがデータstorageに MySQL シャードを使用しており、これらのシャードを 1 つのテーブルとして TiDB に移行する必要がある場合、DM を使用してシャードのマージと移行を実行できます。

-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)

シャードされたテーブルのデータ サイズが大きく (たとえば、1 TiB より大きい)、移行期間中に他のアプリケーションが TiDB に書き込むことを許可しない場合は、 TiDB Lightning を使用してシャードされたテーブルをすばやくマージしてインポートできます。その後、アプリケーションのニーズに基づいて、DM を使用して増分シャーディング データ (binlog) を複製できます。

-   [大規模データセットの MySQL シャードを TiDB に移行してマージする](/migrate-large-mysql-shards-to-tidb.md)

## ファイルからTiDBにデータを移行する {#migrate-data-from-files-to-tidb}

-   [CSVファイルからTiDBにデータを移行する](/migrate-from-csv-files-to-tidb.md)
-   [SQL ファイルから TiDB にデータを移行する](/migrate-from-sql-files-to-tidb.md)
-   [Parquet ファイルから TiDB にデータを移行する](/migrate-from-parquet-files-to-tidb.md)

## TiDB クラスター間の増分レプリケーション {#incremental-replication-between-tidb-clusters}

TiCDC を使用すると、TiDB クラスター間の増分データ レプリケーションを行うことができます。詳細については、 [TiCDC の概要](/ticdc/ticdc-overview.md)を参照してください。

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能により移行プロセスが改善され、アプリケーションのより多くのニーズを満たすことができます。

-   [gh-ost または pt-osc を使用するデータベースからの継続的なレプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントをフィルタリングする](/filter-binlog-event.md)
-   [SQL 式を使用して DML イベントをフィルタリングする](/filter-dml-event.md)
