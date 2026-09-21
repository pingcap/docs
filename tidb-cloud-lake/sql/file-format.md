---
title: 文件格式
summary: 本页按功能组织，全面概述了 {{{ .lake }}} 中的文件格式操作，便于参考。
---

# 文件格式

本页按功能组织，全面概述了 {{{ .lake }}} 中的文件格式操作，便于参考。

## 文件格式管理 {#file-format-management}

| Command | Description |
|---------|-------------|
| [CREATE FILE FORMAT](/tidb-cloud-lake/sql/create-file-format.md) | 创建一个具名的文件格式对象，用于数据加载和卸载 |
| [DROP FILE FORMAT](/tidb-cloud-lake/sql/drop-file-format.md) | 删除一个文件格式对象 |

## 文件格式信息 {#file-format-information}

| 命令 | 描述 |
|---------|-------------|
| [SHOW FILE FORMATS](/tidb-cloud-lake/sql/show-file-formats.md) | 列出当前数据库中的所有文件格式 |

> **注意：**
>
> {{{ .lake }}} 中的文件格式定义了在数据加载操作期间应如何解析数据文件，或在数据卸载操作期间应如何设置数据文件的格式。它们提供了一种可复用的方式，用于指定文件类型、字段分隔符、压缩方式以及其他格式选项。