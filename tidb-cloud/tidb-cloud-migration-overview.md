---
title: Migration and Import Overview
summary: TiDB Cloudのデータ移行およびインポート シナリオの概要について説明します。
aliases: ['/tidbcloud/export-data-from-tidb-cloud']
---

# 移行とインポートの概要 {#migration-and-import-overview}

様々なデータソースからTiDB Cloudにデータを移行できます。このドキュメントでは、データ移行シナリオの概要を説明します。

## MySQL互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

MySQL互換データベースからデータを移行する場合、完全データ移行と増分データ移行を実行できます。移行シナリオと移行方法は次のとおりです。

-   Data Migration を使用して MySQL 互換データベースを移行する

    TiDBはMySQLとの互換性が非常に高く、 TiDB Cloudコンソールのデータ移行機能を使用することで、MySQL互換データベースからTiDB Cloudへのデータの移行をスムーズに行うことができます。詳細については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)ご覧ください。

-   AWS DMS を使用して移行する

    PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

    -   [AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
    -   [AWS DMS を使用して Amazon RDS for Oracle から移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)

-   MySQLシャードの移行とマージ

    アプリケーションでデータstorageにMySQLシャードを使用している場合は、これらのシャードを1つのテーブルとしてTiDB Cloudに移行できます。詳細については、 [大規模データセットの MySQL シャードをTiDB Cloudに移行および統合する](/tidb-cloud/migrate-sql-shards.md)ご覧ください。

-   TiDBセルフマネージドからの移行

    DumplingとTiCDCを介して、TiDBセルフマネージドクラスターからTiDB Cloud （AWS）にデータを移行できます。詳細については、 [TiDBセルフマネージドからTiDB Cloudへの移行](/tidb-cloud/migrate-from-op-tidb.md)ご覧ください。

## ファイルからTiDB Cloudにデータをインポートする {#import-data-from-files-to-tidb-cloud}

SQL、CSV、Parquet、またはAurora Snapshot形式のデータファイルをお持ちの場合は、これらのファイルをTiDB Cloudに一括でインポートできます。インポートのシナリオと方法は次のとおりです。

-   ローカルCSVファイルをTiDB Cloudにインポートする

    ローカルCSVファイルをTiDB Cloudにインポートできます。詳細については、 [ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

-   サンプルデータ（SQLファイル）をTiDB Cloudにインポートする

    TiDB Cloudにサンプルデータ（SQLファイル）をインポートすることで、 TiDB Cloud のインターフェースとインポートプロセスをすぐに理解することができます。詳細については、 [サンプルデータをTiDB Cloud StarterまたはEssentialにインポートする](/tidb-cloud/import-sample-data-serverless.md)と[サンプルデータをTiDB Cloud Dedicatedにインポート](/tidb-cloud/import-sample-data.md)ご覧ください。

-   Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、または Alibaba Cloud OSS から CSV ファイルをTiDB Cloudにインポートします。

    Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、またはAlibaba Cloud OSSからTiDB CloudにCSVファイルをインポートできます。詳細については、 [クラウドストレージからTiDB Cloud StarterまたはEssentialにCSVファイルをインポートする](/tidb-cloud/import-csv-files-serverless.md)と[クラウドストレージからTiDB Cloud DedicatedにCSVファイルをインポートする](/tidb-cloud/import-csv-files.md)ご覧ください。

-   Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage、または Alibaba Cloud OSS から Apache Parquet ファイルをTiDB Cloudにインポートします。

    Amazon S3、Google Cloud Storage（GCS）、Azure Blob Storage、またはAlibaba Cloud OSSからParquetファイルをTiDB Cloudにインポートできます。詳細については、 [Cloud Storage からTiDB Cloud Starter または Essential に Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files-serverless.md)と[Apache Parquet ファイルを Cloud Storage からTiDB Cloud Dedicated にインポートする](/tidb-cloud/import-parquet-files.md)ご覧ください。

## 参照 {#reference}

### クラウドstorageアクセスを構成する {#configure-cloud-storage-access}

ソースデータがAmazon S3、Google Cloud Storage（GCS）バケット、Azure Blob Storageコンテナ、またはAlibaba Cloud OSSバケットに保存されている場合、 TiDB Cloudにデータをインポートまたは移行する前に、storageへのアクセスを設定する必要があります。詳細については、 [TiDB Cloud Starter または Essential の外部ストレージアクセスを構成する](/tidb-cloud/configure-external-storage-access.md)と[TiDB Cloud Dedicatedの外部ストレージアクセスを構成する](/tidb-cloud/dedicated-external-storage.md)参照してください。

### データインポートの命名規則 {#naming-conventions-for-data-import}

データを確実にインポートするには、命名規則に準拠したスキーマファイルとデータファイルを準備する必要があります。詳細については、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)参照してください。

### Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

Amazon S3からTiDB Cloudにデータをインポートする際に発生する可能性のあるアクセス拒否エラーをトラブルシューティングできます。詳細については、 [Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。
