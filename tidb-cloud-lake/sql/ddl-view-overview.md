---
title: 视图
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的视图操作，便于快速查阅。
---

# 视图

本页按功能分类，全面概述了 {{{ .lake }}} 中的视图操作，便于快速查阅。

## 视图管理 {#view-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE VIEW](/tidb-cloud-lake/sql/create-view.md) | 基于查询创建一个新视图 |
| [ALTER VIEW](/tidb-cloud-lake/sql/alter-view.md) | 为现有视图分配或移除标签 |
| [DROP VIEW](/tidb-cloud-lake/sql/drop-view.md) | 删除一个视图 |
| [物化视图](/tidb-cloud-lake/sql/materialized-view.md) | 创建并维护由物理存储支持的物化视图 |
| [REFRESH LINEAGE](/tidb-cloud-lake/sql/refresh-lineage.md) | 为现有视图回填或校正血缘关系 |

## 视图信息 {#view-information}

| 命令 | 描述 |
|---------|-------------|
| [DESC VIEW](/tidb-cloud-lake/sql/desc-view.md) | 显示视图的详细信息 |
| [SHOW VIEWS](/tidb-cloud-lake/sql/show-views.md) | 列出当前或指定数据库中的所有视图 |

> **Note:**
>
> {{{ .lake }}} 中的视图是存储在数据库中的命名查询，可以像表一样被引用。它们可用于简化复杂查询，并控制对底层数据的访问。