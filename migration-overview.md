---
title: Data Migration Overview
summary: Learn the overview of data migration scenarios and the solutions.
---

# データ移行の概要 {#data-migration-overview}

このドキュメントでは、TiDBで使用できるデータ移行ソリューションの概要を説明します。データ移行ソリューションは次のとおりです。

-   完全なデータ移行。
    -   Amazon Auroraスナップショット、CSVファイル、またはMydumper SQLファイルをTiDBにインポートするには、TiDBLightningを使用して完全な移行を実行できます。
    -   すべてのTiDBデータをCSVファイルまたはMydumperSQLファイルとしてエクスポートするには、 Dumplingを使用して完全な移行を実行できます。これにより、MySQLまたはMariaDBからのデータ移行が容易になります。
    -   データサイズが小さい（たとえば、1 TiB未満）データベースからすべてのデータを移行するには、TiDBデータ移行（DM）を使用することもできます。

-   TiDBのクイック初期化。 TiDB Lightningは、データの迅速なインポートをサポートし、TiDBの特定のテーブルを迅速に初期化できます。この機能を使用する前に、クイック初期化はTiDBに大きな影響を与え、初期化期間中はクラスタがサービスを提供しないことに注意してください。

-   インクリメンタルレプリケーション。 TiDB DMを使用して、MySQL、MariaDB、またはAuroraからTiDBにbinlogを複製できます。これにより、複製期間中のウィンドウのダウンタイムが大幅に短縮されます。

-   TiDBクラスター間のデータレプリケーション。 TiDBはバックアップと復元をサポートしています。この機能により、既存のTiDBクラスタのスナップショットを新しいTiDBクラスタに初期化できます。

データベースの種類、展開場所、アプリケーションデータのサイズ、およびアプリケーションのニーズに応じて、さまざまな移行ソリューションを選択できます。次のセクションでは、いくつかの一般的な移行シナリオを紹介します。これらのセクションを参照して、ニーズに応じて最適なソリューションを決定できます。

## AuroraMySQLからAuroraにデータを移行する {#migrate-data-from-aurora-mysql-to-tidb}

AuroraからAWSにデプロイされたTiDBクラスタにデータを移行する場合、データ移行には、完全なデータ移行と増分レプリケーションの2つの操作が必要です。アプリケーションのニーズに応じて、対応する操作を選択できます。

-   [AuroraからTiDBへのデータの移行](/migrate-aurora-to-tidb.md) 。

## MySQLからTiDBにデータを移行する {#migrate-data-from-mysql-to-tidb}

クラウドストレージ（S3）サービスが使用されておらず、ネットワーク接続が良好で、ネットワークレイテンシが低い場合は、次の方法を使用して、MySQLからTiDBにデータを移行できます。

-   [小さなデータセットのMySQLをTiDBに移行する](/migrate-small-mysql-to-tidb.md)

移行速度に対する要求が高い場合、またはデータサイズが大きい場合（たとえば、1 TiBより大きい場合）、移行期間中に他のアプリケーションがTiDBに書き込むことを許可しない場合は、TiDBLightningを使用してすばやく実行できます。データをインポートします。次に、DMを使用して、アプリケーションのニーズに基づいて増分データ（binlog）を複製できます。

-   [大規模なデータセットのMySQLをTiDBに移行する](/migrate-large-mysql-to-tidb.md)

## MySQLシャードをTiDBに移行およびマージします {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションがデータストレージにMySQLシャードを使用しており、これらのシャードを1つのテーブルとしてTiDBに移行する必要があるとします。この場合、DMを使用してシャードのマージと移行を実行できます。

-   [小さなデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)

シャーディングされたテーブルのデータサイズが大きく（たとえば、1 TiBより大きい）、移行期間中に他のアプリケーションがTiDBに書き込むことを許可しない場合は、TiDB Lightningを使用して、シャーディングされたテーブルをすばやくマージしてインポートできます。次に、DMを使用して、アプリケーションのニーズに基づいて増分シャーディングデータ（binlog）を複製できます。

-   [大規模なデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## ファイルからTiDBへのデータの移行 {#migrate-data-from-files-to-tidb}

-   [CSVファイルからTiDBへのデータの移行](/migrate-from-csv-files-to-tidb.md)
-   [SQLファイルからTiDBへのデータの移行](/migrate-from-sql-files-to-tidb.md)

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能は、移行プロセスを改善し、アプリケーションのより多くのニーズを満たす可能性があります。

-   [gh-ostまたはpt-oscを使用するデータベースからの継続的なレプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を持つダウンストリームTiDBテーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントをフィルタリングする](/filter-binlog-event.md)
-   [SQL式を使用してDMLイベントをフィルタリングする](/filter-dml-event.md)
