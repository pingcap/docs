---
title: Ngram Index
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中 Ngram 索引的相关操作，便于快速查阅。
---

# Ngram 索引

本页按功能分类，全面概述了 {{{ .lake }}} 中 Ngram 索引的相关操作，便于快速查阅。

## Ngram 索引管理 {#ngram-index-management}

| Command                                       | 描述 |
|-----------------------------------------------|----------------------------------------------------------|
| [CREATE NGRAM INDEX](/tidb-cloud-lake/sql/create-ngram-index.md)   | 创建新的 Ngram 索引，以高效执行子字符串搜索 |
| [刷新 NGRAM 索引](/tidb-cloud-lake/sql/refresh-ngram-index.md) | 刷新 Ngram 索引 |
| [DROP NGRAM INDEX](/tidb-cloud-lake/sql/drop-ngram-index.md)       | 删除 Ngram 索引 |

> **注意：**
>
> {{{ .lake }}} 中的 Ngram 索引支持在文本数据中高效执行子字符串搜索和模式匹配，从而提升 LIKE 及类似操作的性能。