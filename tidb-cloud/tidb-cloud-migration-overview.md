---
title: Migration and Import Overview
summary: Learn an overview of data migration and import scenarios for TiDB Cloud.
---

# 移行とインポートの概要 {#migration-and-import-overview}

さまざまなデータ ソースからTiDB Cloudにデータを移行できます。このドキュメントでは、データ移行シナリオの概要を説明します。

## MySQL 互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

MySQL 互換データベースからデータを移行する場合、完全なデータ移行と増分データ移行を実行できます。移行のシナリオと方法は次のとおりです。

-   データ移行を使用して MySQL 互換データベースを移行する

    TiDB は MySQL と高い互換性があります。 TiDB Cloudコンソールでデータ移行を使用すると、MySQL 互換データベースからTiDB Cloudにデータをスムーズに移行できます。詳細については、 [データ移行を使用して MySQL 互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)を参照してください。

-   AWS DMS を使用して移行する

    PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

    -   [AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
    -   [AWS DMS を使用した Amazon RDS for Oracle からの移行](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)

-   MySQL シャードの移行とマージ

    アプリケーションがデータstorageに MySQL シャードを使用している場合、これらのシャードを 1 つのテーブルとしてTiDB Cloudに移行できます。詳細については、 [大規模なデータセットの MySQL シャードをTiDB Cloudに移行およびマージ](/tidb-cloud/migrate-sql-shards.md)を参照してください。

-   TiDB セルフホスト型からの移行

    Dumplingと TiCDC を通じて、TiDB セルフホスト クラスターからTiDB Cloud(AWS) にデータを移行できます。詳細については、 [TiDB セルフホストからTiDB Cloudへの移行](/tidb-cloud/migrate-from-op-tidb.md)を参照してください。

## ファイルからTiDB Cloudにデータをインポート {#import-data-from-files-to-tidb-cloud}

SQL、CSV、Parquet、またはAuroraスナップショット形式のデータ ファイルがある場合は、これらのファイルを一度にTiDB Cloudにインポートできます。インポートのシナリオと方法は次のとおりです。

-   ローカル CSV ファイルをTiDB Cloudにインポートする

    ローカル CSV ファイルをTiDB Cloudにインポートできます。詳細については、 [ローカル ファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)を参照してください。

-   サンプルデータ(SQLファイル)をTiDB Cloudにインポート

    サンプル データ (SQL ファイル) をTiDB Cloudにインポートして、 TiDB Cloudインターフェイスとインポート プロセスにすぐに慣れることができます。詳細については、 [サンプル データをTiDB Cloudにインポートする](/tidb-cloud/import-sample-data.md)を参照してください。

-   CSV ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする

    CSV ファイルを Amazon S3 または GCS からTiDB Cloudにインポートできます。詳細については、 [Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポート](/tidb-cloud/import-csv-files.md)を参照してください。

-   Apache Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする

    Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートできます。詳細については、 [Apache Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md)を参照してください。

## 参照 {#reference}

### Amazon S3 アクセスと GCS アクセスを構成する {#configure-amazon-s3-access-and-gcs-access}

ソース データが Amazon S3 または Google Cloud Storage (GCS) バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのアクセスを構成する必要があります。詳細については、 [Amazon S3 アクセスと GCS アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md)を参照してください。

### データインポートの命名規則 {#naming-conventions-for-data-import}

データを正常にインポートできるようにするには、命名規則に準拠したスキーマ ファイルとデータ ファイルを準備する必要があります。詳細については、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)を参照してください。

### Amazon S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

Amazon S3 からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーのトラブルシューティングを行うことができます。詳細については、 [Amazon S3 からのデータインポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。
