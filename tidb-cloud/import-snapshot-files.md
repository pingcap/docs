---
title: Import Snapshot Files into TiDB Cloud Dedicated
summary: Learn how to import Amazon Aurora or RDS for MySQL snapshot files into TiDB Cloud Dedicated.
---

# 将快照文件导入 TiDB Cloud Dedicated

你可以将来自 Amazon Aurora 或 RDS for MySQL 的快照文件导入到 TiDB Cloud Dedicated。这些快照会被导出为 Parquet 文件。为了确保导入成功，你的数据文件必须遵循特定的命名规范。例如，每个源数据文件必须以 `.parquet` 作为后缀，并且位于名为 `{db_name}.{table_name}/` 的文件夹中。完整细节请参见 [Naming Conventions for Data Import](/tidb-cloud/naming-conventions-for-data-import.md)。

快照文件的导入流程与其他 Parquet 文件相同。分步操作说明请参见 [Import Apache Parquet Files from Cloud Storage into TiDB Cloud Dedicated](/tidb-cloud/import-parquet-files.md)。