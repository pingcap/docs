---
title: 从 TiDB Cloud Lake 卸载数据
summary: 了解如何使用 `COPY INTO` 命令将 TiDB Cloud Lake 中的数据卸载为多种文件格式，并导出到不同的存储目标。
---

# 从 TiDB Cloud Lake 卸载数据

{{{ .lake }}} 的 `COPY INTO` 命令支持将数据导出为多种文件格式，并写入不同的存储位置，同时提供灵活的格式化选项。

## 支持的文件格式 {#supported-file-formats}

| 格式 | 示例语法 | 主要使用场景 |
|--------|---------------|------------------|
| [**卸载 Parquet 文件**](/tidb-cloud-lake/guides/unload-parquet-file.md) | `FILE_FORMAT = (TYPE = PARQUET)` | 分析型工作负载，高效存储 |
| [**卸载 CSV 文件**](/tidb-cloud-lake/guides/unload-csv-file.md) | `FILE_FORMAT = (TYPE = CSV)` | 数据交换，通用兼容性 |
| [**卸载 TSV 文件**](/tidb-cloud-lake/guides/unload-tsv-file.md) | `FILE_FORMAT = (TYPE = TSV)` | 带逗号值的表格数据 |
| [**卸载 NDJSON 文件**](/tidb-cloud-lake/guides/unload-ndjson-file.md) | `FILE_FORMAT = (TYPE = NDJSON)` | 半结构化数据，灵活 schema |
| [**卸载 Lance 数据集**](/tidb-cloud-lake/guides/unload-lance-dataset.md) | `FILE_FORMAT = (TYPE = LANCE)` | 机器学习和向量工作负载，Arrow/Lance 使用方 |

## 存储目标 {#storage-destinations}

| 目标 | 示例 | 适用场景 |
|-------------|---------|-------------|
| **命名 stage** | `COPY INTO my_stage FROM my_table` | 适用于重复导出到同一位置的场景 |
| **S3 兼容存储** | `COPY INTO 's3://bucket/path/' FROM my_table` | 使用 Amazon S3 的云对象存储 |