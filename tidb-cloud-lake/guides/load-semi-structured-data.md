---
title: 加载半结构化格式
summary: 半结构化数据包含用于分隔语义元素的标签或标记，但不遵循严格的数据库结构。{{{ .lake }}} 使用 `COPY INTO` 命令高效加载这些格式，并可选择在加载过程中进行即时数据转换。
---

# 加载半结构化数据

半结构化数据包含用于分隔语义元素的标签或标记，但不遵循严格的数据库结构。{{{ .lake }}} 使用 `COPY INTO` 命令高效加载这些格式，并可选择在加载过程中进行即时数据转换。

## 支持的文件格式 {#supported-file-formats}

| 文件格式 | 描述 | 指南 |
| ----------- | ----------- | ----- |
| **Parquet** | 高效的列式存储格式 | [加载 Parquet](/tidb-cloud-lake/guides/load-parquet.md) |
| **CSV** | 逗号分隔值 | [加载 CSV](/tidb-cloud-lake/guides/load-csv.md) |
| **TSV** | 制表符分隔值 | [加载 TSV](/tidb-cloud-lake/guides/load-tsv.md) |
| **NDJSON** | 按换行符分隔的 JSON | [加载 NDJSON](/tidb-cloud-lake/guides/load-ndjson.md) |
| **ORC** | 优化的行列式格式 | [加载 ORC](/tidb-cloud-lake/guides/load-orc.md) |
| **Avro** | 带有模式定义的行式格式 | [加载 Avro](/tidb-cloud-lake/guides/load-avro.md) |