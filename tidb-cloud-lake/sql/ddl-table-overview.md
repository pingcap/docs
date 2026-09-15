---
title: 表
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的表操作，便于快速查阅。
---

# 表

本页按功能分类，全面概述了 {{{ .lake }}} 中的表操作，便于快速查阅。

## 表创建 {#table-creation}

| 命令 | 描述 |
|---------|-------------|
| [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) | 使用指定的列和选项创建新表 |
| [CREATE TABLE ... LIKE](/tidb-cloud-lake/sql/create-table.md#create-table--like) | 使用与现有表相同的列定义创建表 |
| [CREATE TABLE ... AS](/tidb-cloud-lake/sql/create-table.md#create-table--as) | 创建表，并基于 SELECT 查询结果插入数据 |
| [CREATE TRANSIENT TABLE](/tidb-cloud-lake/sql/create-transient-table.md) | 创建不支持 Time Travel 的表 |
| [CREATE EXTERNAL TABLE](/tidb-cloud-lake/sql/create-external-table.md) | 创建一个表，其数据存储在指定的外部位置 |
| [ATTACH TABLE](/tidb-cloud-lake/sql/attach-table.md) | 通过将表与现有表关联来创建表 |

## 表修改 {#table-modification}

| 命令 | 描述 |
|---------|-------------|
| [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md) | 修改表列、注释、Fuse 选项、外部连接，或与另一张表交换元信息 |
| [RENAME TABLE](/tidb-cloud-lake/sql/rename-table.md) | 更改表名 |

## 表信息 {#table-information}

| 命令 | 描述 |
|---------|-------------|
| [DESCRIBE TABLE](/tidb-cloud-lake/sql/describe-table.md) / [SHOW FIELDS](/tidb-cloud-lake/sql/show-fields.md) | 显示指定表中列的信息 |
| [SHOW FULL COLUMNS](/tidb-cloud-lake/sql/show-columns.md) | 获取指定表中列的完整详细信息 |
| [SHOW CREATE TABLE](/tidb-cloud-lake/sql/show-create-table.md) | 显示用于创建指定表的 CREATE TABLE 语句 |
| [SHOW TABLES](/tidb-cloud-lake/sql/show-tables.md) | 列出当前数据库或指定数据库中的表 |
| [SHOW TABLE STATUS](/tidb-cloud-lake/sql/show-table-status.md) | 显示数据库中各表的状态 |
| [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md) | 列出当前数据库或指定数据库中已删除的表 |

## 表删除与恢复 {#table-deletion-recovery}

| 命令 | 描述 | 恢复选项 |
|---------|-------------|----------------|
| [TRUNCATE TABLE](/tidb-cloud-lake/sql/truncate-table.md) | 删除表中的所有数据，同时保留表结构 | [FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md) |
| [DROP TABLE](/tidb-cloud-lake/sql/drop-table.md) | 删除表 | [UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) |
| [VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md) | 永久删除表的历史数据文件（企业版） | 不可恢复 |
| [VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md) | 永久删除已删除表的数据文件（企业版） | 不可恢复 |

## 表优化 {#table-optimization}

| 命令 | 描述 |
|---------|-------------|
| [OPTIMIZE TABLE](/tidb-cloud-lake/sql/optimize-table.md) | 压缩或清理历史数据以节省存储空间并提升查询性能 |
| [SET CLUSTER KEY](/tidb-cloud-lake/sql/set-cluster-key.md) | 配置 cluster key，以提升大表的查询性能 |

> **注意：**
>
> 表优化属于高级操作。请在执行前仔细阅读相关文档，以避免潜在的数据丢失。