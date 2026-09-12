---
title: 序列
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的序列操作，便于快速查阅。
---

# 序列

本页按功能分类，全面概述了 {{{ .lake }}} 中的序列操作，便于快速查阅。

## 序列管理 {#sequence-management}

| Command | 描述 |
|---------|-------------|
| [CREATE SEQUENCE](/tidb-cloud-lake/sql/create-sequence.md) | 创建新的序列生成器 |
| [DROP SEQUENCE](/tidb-cloud-lake/sql/drop-sequence.md) | 删除序列生成器 |

## 序列信息 {#sequence-information}

| Command | 描述 |
|---------|-------------|
| [DESC SEQUENCE](/tidb-cloud-lake/sql/desc-sequence.md) | 显示序列的详细信息 |
| [SHOW SEQUENCES](/tidb-cloud-lake/sql/show-sequences.md) | 列出当前或指定数据库中的所有序列 |

> **注意：**
>
> {{{ .lake }}} 中的序列用于按顺序生成唯一的数值，通常用于主键或其他唯一标识符。