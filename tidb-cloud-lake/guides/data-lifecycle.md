---
title: TiDB Cloud Lake 中的数据生命周期
summary: "{{{ .lake }}} 支持常见的数据定义语言（DDL）和数据操纵语言（DML）命令，让你能够轻松管理数据库。无论是组织、存储、查询、修改还是删除数据，{{{ .lake }}} 都遵循你所熟悉的行业标准。"
---

# TiDB Cloud Lake 中的数据生命周期

{{{ .lake }}} 支持常见的数据定义语言（DDL）和数据操纵语言（DML）命令，让你能够轻松管理数据库。无论是组织、存储、查询、修改还是删除数据，{{{ .lake }}} 都遵循你所熟悉的行业标准。

## {{{ .lake }}} 对象 {#lake-objects}

{{{ .lake }}} 支持以下对象的创建和修改：

- 数据库
- 表
- 外部表
- Stream
- 视图
- 索引
- Stage
- 文件格式
- 连接
- 用户定义函数（UDF）
- 外部函数
- 用户
- 角色
- 授权
- 计算集群 (Warehouse)
- 任务
- [快照标签](/tidb-cloud-lake/sql/table-versioning.md#snapshot-tags)

## 组织数据 {#organizing-data}

将数据组织到数据库和表中。

关键命令：

- [`CREATE DATABASE`](/tidb-cloud-lake/sql/create-database.md)：用于创建新数据库。
- [`ALTER DATABASE`](/tidb-cloud-lake/sql/alter-database.md)：用于修改现有数据库。
- [`CREATE TABLE`](/tidb-cloud-lake/sql/create-table.md)：用于创建新表。
- [`ALTER TABLE`](/tidb-cloud-lake/sql/alter-table.md)：用于修改现有表。

## 存储数据 {#storing-data}

直接将数据添加到表中。{{{ .lake }}} 还支持将外部文件中的数据导入到其表中。

关键命令：

- [`INSERT`](/tidb-cloud-lake/sql/insert.md)：用于向表中添加数据。
- [`COPY INTO <table>`](/tidb-cloud-lake/sql/copy-into-table.md)：用于从外部文件导入数据。

## 查询数据 {#querying-data}

当数据已存入表后，可以使用 `SELECT` 查看和分析数据。

关键命令：

- [`SELECT`](/tidb-cloud-lake/sql/select.md)：用于从表中获取数据。

## 处理数据 {#working-with-data}

当数据位于 {{{ .lake }}} 中后，你可以根据需要对其进行修改、替换、合并或删除。

关键命令：

- [`UPDATE`](/tidb-cloud-lake/sql/update.md)：用于修改表中的数据。
- [`REPLACE`](/tidb-cloud-lake/sql/replace.md)：用于替换现有数据。
- [`MERGE`](/tidb-cloud-lake/sql/merge.md)：用于通过比较主表与源表或子查询之间的数据，无缝执行插入、修改和删除操作。
- [`DELETE`](/tidb-cloud-lake/sql/delete.md)：用于从表中删除数据。

## 删除数据 {#removing-data}

{{{ .lake }}} 支持删除特定数据，也支持删除整个表和数据库。

关键命令：

- [`TRUNCATE TABLE`](/tidb-cloud-lake/sql/truncate-table.md)：用于清空表中的数据而不删除表结构。
- [`DROP TABLE`](/tidb-cloud-lake/sql/drop-table.md)：用于删除表。
- [`DROP DATABASE`](/tidb-cloud-lake/sql/drop-database.md)：用于删除数据库。