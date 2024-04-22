---
title: Import Snapshot Files into TiDB Cloud
summary: Amazon AuroraまたはRDS for MySQLのスナップショットファイルをTiDB Cloudにインポートできます。`.parquet`サフィックスを持つすべてのソースデータファイルは、命名規則に準拠する必要があります。スナップショットファイルのインポートプロセスは、Parquetファイルのインポートプロセスと似ています。詳細については、Apache ParquetファイルをAmazon S3またはGCSからTiDB Cloudにインポートするを参照してください。
---

# スナップショット ファイルをTiDB Cloudにインポートする {#import-snapshot-files-into-tidb-cloud}

Amazon Auroraまたは RDS for MySQL スナップショット ファイルをTiDB Cloudにインポートできます。 `{db_name}.{table_name}/`フォルダー内の`.parquet`サフィックスを持つすべてのソース データ ファイルは、 [命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に準拠する必要があることに注意してください。

スナップショット ファイルをインポートするプロセスは、Parquet ファイルをインポートするプロセスと似ています。詳細については、 [Apache Parquet ファイルを Amazon S3 または GCS からTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md)を参照してください。
