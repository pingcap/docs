---
title: Migration Overview
summary: Learn an overview of data migration scenarios and the solutions for TiDB Cloud.
---

# 移行の概要 {#migration-overview}

さまざまなデータ ソースからTiDB Cloudにデータを移行できます。このドキュメントでは、データ移行シナリオの概要について説明します。

## Amazon S3 アクセスと GCS アクセスを設定する {#configure-amazon-s3-access-and-gcs-access}

ソース データが Amazon S3 または Google Cloud Storage (GCS) バケットに保存されている場合は、データをTiDB Cloudにインポートまたは移行する前に、バケットへのアクセスを構成する必要があります。詳細については、 [Amazon S3 アクセスと GCS アクセスを設定する](/tidb-cloud/config-s3-and-gcs-access.md)を参照してください。

## MySQL 互換データベースからデータを移行する {#migrate-data-from-mysql-compatible-databases}

TiDB は MySQL との互換性が高いです。データが自己ホスト型の MySQL インスタンスからのものであろうと、パブリック クラウドによって提供される RDS サービスであろうと、MySQL 互換データベースからTiDB Cloudにデータをスムーズに移行できます。詳細については、 [MySQL 互換データベースからデータを移行する](/tidb-cloud/migrate-data-into-tidb.md)を参照してください。

完全なデータ移行の後、MySQL 互換データベースからTiDB Cloudへの増分データ移行を実行することもできます。詳細については、 [MySQL 互換データベースからの増分データの移行](/tidb-cloud/migrate-incremental-data-from-mysql.md)を参照してください。

アプリケーションがデータ ストレージに MySQL シャードを使用している場合、これらのシャードを 1 つのテーブルとしてTiDB Cloudに移行できます。詳細については、 [大規模なデータセットの MySQL シャードをTiDB Cloudに移行およびマージする](/tidb-cloud/migrate-sql-shards.md)を参照してください。

## Amazon Aurora MySQL からTiDB Cloudへの一括移行 {#migrate-from-amazon-aurora-mysql-to-tidb-cloud-in-bulk}

TiDB Cloudコンソールのインポート ツールを使用して、Amazon Aurora MySQL からTiDB Cloudにデータを一括移行できます。

詳細については、 [Amazon Aurora MySQL からTiDB Cloudに一括移行する](/tidb-cloud/migrate-from-aurora-bulk-import.md)を参照してください。

## Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行 {#import-or-migrate-from-amazon-s3-or-gcs-to-tidb-cloud}

TiDB Cloudにデータをインポートまたは移行するためのステージング領域として、Amazon Simple Storage Service (Amazon S3) または Google Cloud Storage (GCS) を使用できます。

詳細については、 [Amazon S3 または GCS からTiDB Cloudへのインポートまたは移行](/tidb-cloud/migrate-from-amazon-s3-or-gcs.md)を参照してください。

## ファイルからTiDB Cloudにデータを移行する {#migrate-data-from-files-to-tidb-cloud}

-   [Amazon S3 または GCS からTiDB Cloudに CSV ファイルをインポートする](/tidb-cloud/import-csv-files.md)
-   [Amazon S3 または GCS からTiDB Cloudに Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files.md)

## Amazon S3 からのデータ インポート中のアクセス拒否エラーのトラブルシューティング {#troubleshoot-access-denied-errors-during-data-import-from-amazon-s3}

Amazon S3 からTiDB Cloudにデータをインポートするときに発生する可能性のあるアクセス拒否エラーをトラブルシューティングできます。詳細については、 [Amazon S3 からのデータ インポート中のアクセス拒否エラーのトラブルシューティング](/tidb-cloud/troubleshoot-import-access-denied-error.md)を参照してください。
