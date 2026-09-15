---
title: 数据库
summary: 本页按功能组织，全面概述了 {{{ .lake }}} 中的数据库操作，便于参考。
---

# 数据库

本页按功能组织，全面概述了 {{{ .lake }}} 中的数据库操作，便于参考。

## 数据库创建与管理 {#database-creation-management}

| 命令 | 描述 |
|---------|-------------|
| [CREATE DATABASE](/tidb-cloud-lake/sql/create-database.md) | 创建新数据库 |
| [ALTER DATABASE](/tidb-cloud-lake/sql/alter-database.md) | 修改数据库 |
| [DROP DATABASE](/tidb-cloud-lake/sql/drop-database.md) | 删除数据库 |
| [USE DATABASE](/tidb-cloud-lake/sql/use-database.md) | 设置当前工作数据库 |
| [UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md) | 恢复已删除的数据库 |

## 数据库信息 {#database-information}

| 命令 | 描述 |
|---------|-------------|
| [SHOW DATABASES](/tidb-cloud-lake/sql/show-databases.md) | 列出所有数据库 |
| [SHOW CREATE DATABASE](/tidb-cloud-lake/sql/show-create-database.md) | 显示某个数据库的 CREATE DATABASE 语句 |
| [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md) | 列出可恢复的已删除数据库 |

> **注意：**
>
> 数据库操作是你在 {{{ .lake }}} 中组织数据的基础。在执行这些命令之前，请确保你具有适当的权限。