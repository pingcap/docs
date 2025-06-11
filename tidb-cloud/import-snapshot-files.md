---
title: Import Snapshot Files into TiDB Cloud
summary: Amazon Auroraまたは RDS for MySQL スナップショット ファイルをTiDB Cloudにインポートする方法を学びます。
---

# スナップショットファイルをTiDB Cloudにインポートする {#import-snapshot-files-into-tidb-cloud}

Amazon Auroraまたは RDS for MySQL のスナップショットファイルを`{db_name}.{table_name}/` TiDB Cloudにインポートできます。3 フォルダ内のサフィックスが`.parquet`であるすべてのソースデータファイルは、 [命名規則](/tidb-cloud/naming-conventions-for-data-import.md)に準拠している必要があることに注意してください。

スナップショットファイルのインポートプロセスは、Parquetファイルのインポートプロセスと似ています。詳細については、 [クラウドストレージからTiDB Cloud DedicatedにApache Parquetファイルをインポートする](/tidb-cloud/import-parquet-files.md)参照してください。
