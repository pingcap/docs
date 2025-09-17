---
title: Import Snapshot Files into TiDB Cloud Dedicated
summary: Amazon Auroraまたは RDS for MySQL スナップショット ファイルをTiDB Cloud Dedicated にインポートする方法を学びます。
---

# スナップショットファイルをTiDB Cloud Dedicatedにインポートする {#import-snapshot-files-into-tidb-cloud-dedicated}

Amazon Auroraまたは RDS for MySQL からTiDB Cloud Dedicated にスナップショットファイルをインポートできます。これらのスナップショットは Parquet ファイルとしてエクスポートされます。インポートを正常に実行するには、データファイルが特定の命名規則に従う必要があります。例えば、各ソースデータファイルは`.parquet`サフィックスを持ち、 `{db_name}.{table_name}/`名前のフォルダに保存されている必要があります。詳細については[データインポートの命名規則](/tidb-cloud/naming-conventions-for-data-import.md)ご覧ください。

スナップショットファイルのインポートプロセスは、他のParquetファイルと同じです。手順については、 [Apache Parquet ファイルを Cloud Storage からTiDB Cloud Dedicated にインポートする](/tidb-cloud/import-parquet-files.md)参照してください。
