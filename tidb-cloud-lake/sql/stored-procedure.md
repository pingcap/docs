---
title: 存储过程
summary: 本页按功能分类，全面概述了 {{{ .lake }}} 中的存储过程操作，便于快速查阅。
---

# 存储过程

本页按功能分类，全面概述了 {{{ .lake }}} 中的存储过程操作，便于快速查阅。

## 存储过程管理 {#procedure-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE PROCEDURE](/tidb-cloud-lake/sql/create-procedure.md) | 创建新的存储过程 |
| [DROP PROCEDURE](/tidb-cloud-lake/sql/drop-procedure.md) | 删除存储过程 |
| [CALL](/tidb-cloud-lake/sql/call-procedure.md) | 执行存储过程 |

## 存储过程信息 {#procedure-information}

| 命令 | 描述 |
|---------|-------------|
| [DESCRIBE PROCEDURE](/tidb-cloud-lake/sql/desc-procedure.md) | 显示特定存储过程的详细信息 |
| [SHOW PROCEDURES](/tidb-cloud-lake/sql/show-procedures.md) | 列出当前数据库中的所有存储过程 |

> **Note:**
>
> {{{ .lake }}} 中的存储过程允许你将一系列 SQL 语句封装为可复用的单元，并作为单个命令执行，从而提升代码组织性和可维护性。

## 延伸阅读 {#further-reading}

如需完整的语言参考，请参阅 [存储过程与 SQL 脚本](/tidb-cloud-lake/sql/stored-procedure-scripting.md)，其中包括变量处理、控制流、游标以及在存储过程中使用动态 SQL 等内容。