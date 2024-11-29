---
title: Migration and Import Overview
summary: TiDB Cloudのデータ移行およびインポート シナリオの概要について説明します。
aliases: ['/tidbcloud/export-data-from-tidb-cloud']
---

# 移行とインポートの概要 {#migration-and-import-overview}

さまざまなデータ ソースからTiDB Cloudにデータを移行できます。このドキュメントでは、データ移行シナリオの概要を説明します。

## MySQL互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

MySQL 互換データベースからデータを移行する場合、完全なデータ移行と増分データ移行を実行できます。移行のシナリオと方法は次のとおりです。

-   データ移行を使用してMySQL互換データベースを移行する

    TiDB は MySQL と高い互換性があります。TiDB TiDB Cloudコンソールのデータ移行を使用して、MySQL 互換データベースからTiDB Cloudにデータをスムーズに移行できます。詳細については、 [データ移行を使用してMySQL互換データベースをTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-data-migration.md)参照してください。

-   AWS DMS を使用して移行する

    PostgreSQL、Oracle、SQL Server などの異種データベースをTiDB Cloudに移行する場合は、AWS Database Migration Service (AWS DMS) を使用することをお勧めします。

    -   [AWS DMS を使用して MySQL 互換データベースからTiDB Cloudに移行する](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
    -   [AWS DMS を使用して Amazon RDS for Oracle から移行する](/tidb-cloud/migrate-from-oracle-using-aws-dms.md)

-   MySQLシャードの移行とマージ

    アプリケーションがデータstorageに MySQL シャードを使用している場合は、これらのシャードを 1 つのテーブルとしてTiDB Cloudに移行できます。詳細については、 [大規模データセットの MySQL シャードをTiDB Cloudに移行して統合する](/tidb-cloud/migrate-sql-shards.md)参照してください。

-   TiDBセルフマネージドからの移行

    Dumplingと TiCDC を介して、TiDB セルフマネージド クラスターからTiDB Cloud (AWS) にデータを移行できます。詳細については、 [TiDBセルフマネージドからTiDB Cloudへの移行](/tidb-cloud/migrate-from-op-tidb.md)参照してください。

## ファイルからTiDB Cloudにデータをインポートする {#import-data-from-files-to-tidb-cloud}

SQL、CSV、Parquet、またはAurora Snapshot 形式のデータ ファイルがある場合は、これらのファイルを一度にTiDB Cloudにインポートできます。インポートのシナリオと方法は次のとおりです。

-   ローカルCSVファイルをTiDB Cloudにインポートする

    ローカル CSV ファイルをTiDB Cloudにインポートできます。詳細については、 [ローカルファイルをTiDB Cloudにインポートする](/tidb-cloud/tidb-cloud-import-local-files.md)参照してください。

-   サンプルデータ（SQLファイル）をTiDB Cloudにインポートする

    サンプル データ (SQL ファイル) をTiDB Cloudにインポートすると、 TiDB Cloud のインターフェイスとインポート プロセスにすぐに慣れることができます。詳細については、 [サンプルデータをTiDB Cloudにインポートする](/tidb-cloud/import-sample-data.md)参照してください。

-   Amazon S3 または GCS から CSV ファイルをTiDB Cloudにインポートする

    Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポートできます。詳細については、 [Amazon S3 または GCS から CSV ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md)参照してください。

-   Amazon S3 または GCS から Apache Parquet ファイルをTiDB Cloudにインポートする

    Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートできます。詳細については、 [Amazon S3 または GCS から Apache Parquet ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md)参照してください。

## 参照 {#reference}

### Amazon S3 アクセスと GCS アクセスを構成する {#configure-amazon-s3-access-and-gcs-access}

ソースデータが Amazon S3 または Google Cloud Storage (GCS) バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのアクセスを構成する必要があります。詳細については、 [Amazon S3 アクセスと GCS アクセスを構成する](/tidb-cloud/config-s3-and-gcs-access.md)参照してください。

### データインポートの命名規則 {#naming-conventions-for-data-import}

データが正常にインポートされるようにするには、命名規則に準拠したスキーマ ファイルとデータ ファイルを準備する必要があります。詳細については、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)参照してください。

### Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

Amazon S3 からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーをトラブルシューティングできます。詳細については、 [Amazon S3 からのデータインポート中に発生するアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)参照してください。
