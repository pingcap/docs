---
title: Data Migration Overview
summary: Learn the overview of data migration scenarios and the solutions.
---

# データ移行の概要 {#data-migration-overview}

このドキュメントでは、TiDB で使用できるデータ移行ソリューションの概要を説明します。データ移行ソリューションは次のとおりです。

-   完全なデータ移行。
    -   Amazon Auroraスナップショット、CSV ファイル、または Mydumper SQL ファイルを TiDB にインポートするには、 TiDB Lightningを使用して完全な移行を実行できます。
    -   すべての TiDB データを CSV ファイルまたは Mydumper SQL ファイルとしてエクスポートするには、 Dumplingを使用して完全な移行を実行できます。これにより、MySQL または MariaDB からのデータ移行が容易になります。
    -   データ サイズが小さい (たとえば、1 TiB 未満) データベースからすべてのデータを移行するには、TiDB Data Migration (DM) を使用することもできます。

-   TiDB のクイック初期化。 TiDB Lightning はデータの迅速なインポートをサポートしており、TiDB 内の特定のテーブルを迅速に初期化できます。この機能を使用する前に、クイック初期化は TiDB に大きな影響を与え、クラスターは初期化期間中にサービスを提供しないことに注意してください。

-   増分レプリケーション。 TiDB DM を使用して、MySQL、MariaDB、またはAuroraから TiDB にバイナリログをレプリケートできます。これにより、レプリケーション期間中のダウンタイムが大幅に短縮されます。

-   TiDB クラスター間のデータ複製。 TiDB はバックアップと復元をサポートしています。この機能は、既存の TiDB クラスター内のスナップショットを新しい TiDB クラスターに初期化できます。

-   TiDB クラスター間の増分レプリケーション。 TiDB は、同種データベース間の災害復旧をサポートし、災害発生後のプライマリ データベースとセカンダリ データベースの最終的なデータ整合性を確保します。これは、プライマリ クラスターとセカンダリ クラスターの両方が TiDB である場合にのみ機能します。

データベースの種類、展開場所、アプリケーションのデータ サイズ、アプリケーションのニーズに応じて、さまざまな移行ソリューションを選択する場合があります。次のセクションでは、いくつかの一般的な移行シナリオを紹介します。これらのセクションを参照して、ニーズに応じて最適なソリューションを決定できます。

## Aurora MySQL から TiDB にデータを移行する {#migrate-data-from-aurora-mysql-to-tidb}

Auroraから AWS にデプロイされた TiDB クラスターにデータを移行する場合、データ移行には完全なデータ移行と増分レプリケーションという 2 つの操作が必要になります。アプリケーションのニーズに応じて、対応する操作を選択できます。

-   [Amazon Auroraから TiDB へのデータの移行](/migrate-aurora-to-tidb.md) 。

## MySQL から TiDB にデータを移行する {#migrate-data-from-mysql-to-tidb}

クラウドstorage(S3) サービスが使用されておらず、ネットワーク接続が良好でネットワークレイテンシーが低い場合は、 [小規模なデータセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)の手順に従って MySQL から TiDB にデータを移行できます。

移行速度に対する要求が高い場合、またはデータ サイズが大きい (たとえば、1 TiB を超える) 場合、移行期間中に他のアプリケーションによる TiDB への書き込みを許可しない場合は、 TiDB Lightningを使用して、データをインポートします。その後、DM を使用して、アプリケーションのニーズに基づいて増分データ (binlog) をレプリケートできます。 [大規模なデータセットを MySQL から TiDB に移行する](/migrate-large-mysql-to-tidb.md)を参照してください。

## MySQL シャードを TiDB に移行およびマージする {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションがデータstorageに MySQL シャードを使用しており、これらのシャードを 1 つのテーブルとして TiDB に移行する必要があるとします。この場合、DM を使用してシャードのマージと移行を実行できます。

-   [小規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)

シャードテーブルのデータサイズが大きく (たとえば、1 TiB を超える)、移行期間中に他のアプリケーションによる TiDB への書き込みを許可しない場合は、 TiDB Lightningを使用してシャードテーブルを迅速にマージおよびインポートできます。その後、DM を使用して、アプリケーションのニーズに基づいて増分シャーディング データ (binlog) をレプリケートできます。

-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## ファイルから TiDB へのデータの移行 {#migrate-data-from-files-to-tidb}

-   [CSV ファイルから TiDB にデータを移行する](/migrate-from-csv-files-to-tidb.md)
-   [SQL ファイルから TiDB にデータを移行する](/migrate-from-sql-files-to-tidb.md)
-   [Parquet ファイルから TiDB にデータを移行する](/migrate-from-parquet-files-to-tidb.md)

## TiDB クラスター間の増分レプリケーション {#incremental-replication-between-tidb-clusters}

TiCDC を使用して、TiDB クラスター間の増分データ複製を行うことができます。詳細は[TiCDC の概要](/ticdc/ticdc-overview.md)を参照してください。

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能により移行プロセスが改善され、アプリケーションのより多くのニーズを満たす可能性があります。

-   [gh-ost または pt-osc を使用するデータベースからの連続レプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を含むダウンストリーム TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントのフィルタリング](/filter-binlog-event.md)
-   [SQL式を使用したDMLイベントのフィルタリング](/filter-dml-event.md)
