---
title: Data Migration Scenarios
summary: Learn how to configure a data migration task in different scenarios.
---

# データ移行シナリオの概要 {#data-migration-scenario-overview}

> **ノート：**
>
> データ移行タスクを作成する前に、次の操作を実行する必要があります。
>
> 1.  [TiUPを使用してDMクラスターをデプロイする](/dm/deploy-a-dm-cluster-using-tiup.md) 。
> 2.  [データソースを作成する](/dm/quick-start-create-source.md) 。

このドキュメントでは、さまざまなシナリオでデータ移行タスクを実行する方法を紹介します。

シナリオベースのドキュメントに加えて、次のドキュメントも参照できます。

-   データ移行タスクの構成の完全な例については、 [DM高度なタスクConfiguration / コンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。
-   データ移行タスク構成ガイドについては、 [データ移行タスクConfiguration / コンフィグレーションガイド](/dm/dm-task-configuration-guide.md)を参照してください。

## AuroraからTiDBにデータを移行する {#migrate-data-from-amazon-aurora-to-tidb}

AuroraからAWSにデプロイされたTiDBクラスタにデータを移行する場合、データ移行には、完全なデータ移行と増分レプリケーションの2つの操作が必要です。アプリケーションのニーズに応じて、対応する操作を選択できます。

[AuroraからTiDBへのデータの移行](/migrate-aurora-to-tidb.md)

## MySQLからTiDBにデータを移行する {#migrate-data-from-mysql-to-tidb}

クラウドストレージ（S3）サービスが使用されておらず、ネットワーク接続が良好で、ネットワークレイテンシが低い場合は、次の方法を使用して、MySQLからTiDBにデータを移行できます。

-   [小さなデータセットのMySQLをTiDBに移行する](/migrate-small-mysql-to-tidb.md)

移行速度に対する要求が高い場合、またはデータサイズが大きい場合（たとえば、1 TiBより大きい場合）、移行期間中に他のアプリケーションがTiDBに書き込むことを許可しない場合は、TiDBLightningを使用してすばやく実行できます。データをインポートします。次に、DMを使用して、アプリケーションのニーズに基づいて増分データ（binlog）を複製できます。

[大規模なデータセットのMySQLをTiDBに移行する](/migrate-large-mysql-to-tidb.md)

## MySQLシャードをTiDBに移行およびマージします {#migrate-and-merge-mysql-shards-into-tidb}

アプリケーションがデータストレージにMySQLシャードを使用しており、これらのシャードを1つのテーブルとしてTiDBに移行する必要があるとします。この場合、DMを使用してシャードのマージと移行を実行できます。

-   [小さなデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)

シャーディングされたテーブルのデータサイズが大きく（たとえば、1 TiBより大きい）、移行期間中に他のアプリケーションがTiDBに書き込むことを許可しない場合は、TiDB Lightningを使用して、シャーディングされたテーブルをすばやくマージしてインポートできます。次に、DMを使用して、アプリケーションのニーズに基づいて増分シャーディングデータ（binlog）を複製できます。

-   [大規模なデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## より高度な移行ソリューション {#more-advanced-migration-solutions}

次の機能は、移行プロセスを改善し、アプリケーションのより多くのニーズを満たすことができます。

-   [gh-ostまたはpt-oscを使用するデータベースからの継続的なレプリケーション](/migrate-with-pt-ghost.md)
-   [より多くの列を持つダウンストリームTiDBテーブルにデータを移行する](/migrate-with-more-columns-downstream.md)
-   [Binlogイベントをフィルタリングする](/filter-binlog-event.md)
-   [SQL式を使用してDMLイベントをフィルタリングする](/filter-dml-event.md)
