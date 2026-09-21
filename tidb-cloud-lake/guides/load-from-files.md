---
title: 从文件加载
summary: TiDB Cloud Lake 提供简单而强大的命令，可将数据文件加载到表中。大多数操作只需一条命令。
---

# 从文件加载

{{{ .lake }}} 提供简单而强大的命令，可将数据文件加载到表中。大多数操作只需一条命令。你的数据必须采用[支持的格式](/tidb-cloud-lake/sql/input-output-file-formats.md)。

![Data Loading and Unloading Overview](/media/tidb-cloud-lake/load-unload.png)

## 支持的文件格式 {#supported-file-formats}

| 格式 | 类型 | 描述 |
|--------|------|-------------|
| [**CSV**](/tidb-cloud-lake/guides/load-csv.md), [**TSV**](/tidb-cloud-lake/guides/load-tsv.md) | 分隔符分隔 | 可自定义分隔符的文本文件 |
| [**NDJSON**](/tidb-cloud-lake/guides/load-ndjson.md) | 半结构化 | 每行一个 JSON 对象 |
| [**Parquet**](/tidb-cloud-lake/guides/load-parquet.md) | 半结构化 | 高效的列式存储格式 |
| [**ORC**](/tidb-cloud-lake/guides/load-orc.md) | 半结构化 | 高性能列式格式 |
| [**Avro**](/tidb-cloud-lake/guides/load-avro.md) | 半结构化 | 带 schema 的紧凑二进制格式 |

## 按文件位置加载 {#loading-by-file-location}

选择文件所在的位置，以查找推荐的加载方法：

| 数据源 | 推荐工具 | 描述 | 文档 |
|-------------|-----------------|-------------|---------------|
| **暂存数据文件** | **COPY INTO** | 从内部/外部 stage 或用户 stage 快速高效地加载 | [从 stage 加载](/tidb-cloud-lake/guides/load-from-stage.md) |
| **云存储** | **COPY INTO** | 从 Amazon S3、Google Cloud Storage、Microsoft Azure 加载 | [从存储桶加载](/tidb-cloud-lake/guides/load-from-bucket.md) |
| **本地文件** | [**LakeSQL**](https://github.com/tidbcloud/lakesql) | {{{ .lake }}} 的原生 CLI 工具，用于加载本地文件 | [从本地文件加载](/tidb-cloud-lake/guides/load-from-local-file.md) |
| **远程文件** | **COPY INTO** | 从远程 HTTP/HTTPS 位置加载数据 | [从远程文件加载](/tidb-cloud-lake/guides/load-from-remote-file.md) |