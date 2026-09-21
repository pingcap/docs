---
title: Stage
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的 stage 操作，便于参考。
---

# Stage

本页按功能分类，全面概述了 {{{ .lake }}} 中的 stage 操作，便于参考。

## Stage 管理 {#stage-management}

| Command | 描述 |
|---------|-------------|
| [CREATE STAGE](/tidb-cloud-lake/sql/create-stage.md) | 创建一个新的 stage 用于存储文件 |
| [DROP STAGE](/tidb-cloud-lake/sql/drop-stage.md) | 删除一个 stage |
| [PRESIGN](/tidb-cloud-lake/sql/presign.md) | 为 stage 访问生成预签名 URL |

## Stage 操作 {#stage-operations}

| Command | 描述 |
|---------|-------------|
| [LIST STAGE](/tidb-cloud-lake/sql/list-stage-files.md) | 列出 stage 中的文件 |
| [REMOVE STAGE](/tidb-cloud-lake/sql/remove-stage-files.md) | 删除 stage 中的文件 |

## Stage 信息 {#stage-information}

| Command | 描述 |
|---------|-------------|
| [DESC STAGE](/tidb-cloud-lake/sql/desc-stage.md) | 显示 stage 的详细信息 |
| [SHOW STAGES](/tidb-cloud-lake/sql/show-stages.md) | 列出当前或指定数据库中的所有 stage |

## 相关主题 {#related-topics}

- [从 Stage 加载](/tidb-cloud-lake/guides/load-from-stage.md)
- [查询与转换](/tidb-cloud-lake/guides/query-stage.md)
- [文件格式（DDL）](/tidb-cloud-lake/sql/file-format.md)

> **注意：**
>
> {{{ .lake }}} 中的 stage 用作临时存储位置，用于保存你希望加载到表中或从表中卸载的数据文件。