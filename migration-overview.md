---
title: Data Migration Overview
summary: Learn the overview of data migration scenarios and the solutions.
---

# データ移行の概要 {#data-migration-overview}

このドキュメントでは、TiDB で使用できるデータ移行ソリューションの概要を説明します。データ移行ソリューションは次のとおりです。

-   完全なデータ移行。
    -   Amazon Auroraスナップショット、CSV ファイル、または Mydumper SQL ファイルを TiDB にインポートするには、 TiDB Lightningを使用して完全な移行を実行できます。
    -   すべての TiDB データを CSV ファイルまたは Mydumper SQL ファイルとしてエクスポートするには、 Dumplingを使用して完全な移行を実行できます。これにより、MySQL または MariaDB からのデータ移行が容易になります。
    -   データ サイズ ボリュームが小さい (たとえば、1 TiB 未満) データベースからすべてのデータを移行するには、TiDB Data Migration (DM) を使用することもできます。

-   TiDB のクイック初期化。 TiDB Lightning はデータの迅速なインポートをサポートし、TiDB 内の特定のテーブルを迅速に初期化できます。この機能を使用する前に、迅速な初期化が TiDB に大きな影響を与え、初期化期間中はクラスターがサービスを提供しないことに注意してください。

-   増分レプリケーション。 TiDB DM を使用して、バイナリログを MySQL、MariaDB、またはAuroraから TiDB に複製できます。これにより、複製期間中のウィンドウのダウンタイムが大幅に短縮されます。

-   TiDB クラスター間のデータ複製。 TiDB はバックアップと復元をサポートしています。この機能は、既存の TiDB クラスターのスナップショットを新しい TiDB クラスターに初期化できます。

-   TiDB クラスター間の増分レプリケーション。 TiDB は同種のデータベース間のディザスタ リカバリをサポートし、災害イベント後のプライマリ データベースとセカンダリ データベースの最終的なデータ整合性を保証します。プライマリ クラスタとセカンダリ クラスタの両方が TiDB である場合にのみ機能します。

データベースの種類、展開場所、アプリケーション データのサイズ、およびアプリケーションのニーズに応じて、さまざまな移行ソリューションを選択できます。次のセクションでは、いくつかの一般的な移行シナリオを紹介します。これらのセクションを参照して、ニーズに応じて最適なソリューションを決定できます。

## Aurora MySQL から TiDB にデータを移行する {#migrate-data-from-aurora-mysql-to-tidb}

Auroraから AWS にデプロイされた TiDB クラスターにデータを移行する場合、データ移行には、完全なデータ移行と増分レプリケーションの 2 つの操作が必要です。アプリケーションのニーズに応じて、対応する操作を選択できます。

-   [Amazon Auroraから TiDB にデータを移行する](/migrate-aurora-to-tidb.md) .

## MySQL から TiDB にデータを移行する {#migrate-data-from-mysql-to-tidb}

クラウドstorage(S3) サービスが使用されておらず、ネットワーク接続が良好で、ネットワークレイテンシーが低い場合は、次の方法を使用して MySQL から TiDB にデータを移行できます。

-   [小さなデータセットの MySQL を TiDB に移行する](/migrate-small-mysql-to-tidb.md)

移行速度に対する要求が高い場合、またはデータ サイズが大きい (たとえば 1 TiB を超える) 場合で、移行期間中に他のアプリケーションが TiDB に書き込むことを許可しない場合は、 TiDB Lightningを使用してすばやくデータをインポートします。次に、DM を使用して、アプリケーションのニーズに基づいて増分データ (binlog) をレプリケートできます。

-   [大規模なデータセットの MySQL を TiDB に移行する](/migrate-large-mysql-to-tidb.md)

## MySQL シャードを TiDB に移行してマージする {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションがデータstorageに MySQL シャードを使用し、これらのシャードを 1 つのテーブルとして TiDB に移行する必要があるとします。この場合、DM を使用してシャードのマージと移行を実行できます。

-   [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)

シャード テーブルのデータ サイズが大きく (たとえば、1 TiB より大きい)、移行期間中に他のアプリケーションが TiDB に書き込むことを許可しない場合は、 TiDB Lightningを使用して、シャード テーブルをすばやくマージおよびインポートできます。次に、DM を使用して、アプリケーションのニーズに基づいて増分シャーディング データ (binlog) をレプリケートできます。

-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## ファイルから TiDB にデータを移行する {#migrate-data-from-files-to-tidb}

-   [CSV ファイルから TiDB にデータを移行する](/migrate-from-csv-files-to-tidb.md)
-   [SQL ファイルから TiDB にデータを移行する](/migrate-from-sql-files-to-tidb.md)

## TiDB クラスター間の増分レプリケーション {#incremental-replication-between-tidb-clusters}

TiDB クラスター間の増分データ複製に TiCDC を使用できます。詳細については、 [TiCDC の概要](/ticdc/ticdc-overview.md)を参照してください。

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能により、移行プロセスが改善され、アプリケーションのより多くのニーズを満たすことができます。

-   [gh-ost または pt-osc を使用するデータベースからの連続レプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を持つ下流の TiDB テーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントのフィルタリング](/filter-binlog-event.md)
-   [SQL 式を使用した DML イベントのフィルタリング](/filter-dml-event.md)
