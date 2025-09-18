---
title: 将快照文件导入 TiDB Cloud Starter 或 Essential
summary: 了解如何将 Amazon Aurora 或 RDS for MySQL 的快照文件导入 TiDB Cloud Starter 或 Essential。
---

# 将快照文件导入 TiDB Cloud Starter 或 Essential

你可以将来自 Amazon Aurora 或 RDS for MySQL 的快照文件导入 TiDB Cloud Starter 或 Essential。你需要先将这些快照文件从 Amazon Aurora 或 RDS for MySQL 导出为 Parquet 文件。为了确保导入成功，你的数据文件必须遵循特定的命名规范。例如，每个源数据文件必须以 `.parquet` 作为后缀，并且位于名为 `{db_name}.{table_name}/` 的文件夹中。完整细节请参见 [数据导入的命名规范](/tidb-cloud/naming-conventions-for-data-import.md)。

快照文件的导入流程与其他 Parquet 文件相同。详细的分步操作请参见 [从云存储将 Apache Parquet 文件导入 TiDB Cloud Starter 或 Essential](/tidb-cloud/import-parquet-files-serverless.md)。