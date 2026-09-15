---
title: 倒排索引
summary: 本页按功能分类，全面概述 {{{ .lake }}} 中的倒排索引操作，便于参考。
---

# 倒排索引

本页按功能分类，全面概述 {{{ .lake }}} 中的倒排索引操作，便于参考。

## 倒排索引管理 {#inverted-index-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE INVERTED INDEX](/tidb-cloud-lake/sql/create-inverted-index.md) | 为全文搜索创建新的倒排索引 |
| [DROP INVERTED INDEX](/tidb-cloud-lake/sql/drop-inverted-index.md) | 删除倒排索引 |
| [REFRESH INVERTED INDEX](/tidb-cloud-lake/sql/refresh-inverted-index.md) | 使用最新数据更新倒排索引 |

## 相关主题 {#related-topics}

- [全文索引](/tidb-cloud-lake/guides/full-text-index.md)

> **注意：**
>
> {{{ .lake }}} 中的倒排索引可为文本数据提供高效的全文搜索能力，从而支持在大型文本列中快速执行关键字搜索。