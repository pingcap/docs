---
title: 标签
summary: TiDB Cloud Lake 中标签管理与分配的概述。
---

# 标签

标签可用于为 {{{ .lake }}} 对象附加键值元信息，以支持数据治理、分类和合规性跟踪。你可以定义带有可选允许值的标签，将其分配给对象，并通过 `TAG_REFERENCES` 表函数查询标签分配情况。

## 标签管理 {#tag-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) | 创建一个新标签，并可选择设置允许值和注释 |
| [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md) | 删除一个标签（必须没有活动引用） |
| [SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md) | 列出标签定义 |

## 标签分配 {#tag-assignment}

| 命令 | 描述 |
|---------|-------------|
| [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) | 为数据库对象分配或移除标签 |
| [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md) | 查询特定对象上的标签分配情况 |