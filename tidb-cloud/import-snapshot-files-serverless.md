---
title: Import Snapshot Files into TiDB Cloud Starter or Essential
summary: Amazon Auroraまたは RDS for MySQL スナップショット ファイルをTiDB Cloud Starter または Essential にインポートする方法を学びます。
---

# スナップショットファイルをTiDB Cloud StarterまたはEssentialにインポートする {#import-snapshot-files-into-tidb-cloud-starter-or-essential}

Amazon Auroraまたは RDS for MySQL からTiDB Cloud Starter または Essential にスナップショットファイルをインポートできます。まず、これらのスナップショットファイルを Amazon Auroraまたは RDS for MySQL から Parquet ファイルとしてエクスポートする必要があります。インポートを正常に実行するには、データファイルは特定の命名規則に従う必要があります。例えば、各ソースデータファイルは`.parquet`サフィックスを持ち、 `{db_name}.{table_name}/`というフォルダに保存されている必要があります。詳細については、 [データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)参照してください。

スナップショットファイルのインポートプロセスは、他のParquetファイルと同じです。手順については、 [Cloud Storage からTiDB Cloud Starter または Essential に Apache Parquet ファイルをインポートする](/tidb-cloud/import-parquet-files-serverless.md)参照してください。
