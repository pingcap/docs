---
title: 用户定义函数
summary: {{{ .lake }}} 中的用户定义函数（UDF）允许你创建适合特定数据处理需求的自定义操作。本页重点介绍你最常使用的命令，并帮助你为自己的使用场景选择合适的函数类型。
---

# 用户定义函数

{{{ .lake }}} 中的用户定义函数（UDF）允许你创建适合特定数据处理需求的自定义操作。本页重点介绍你最常使用的命令，并帮助你为自己的使用场景选择合适的函数类型。

> **Tip:**
>
> **先检查内置函数。** {{{ .lake }}} 提供了数百个内置函数，涵盖数学、字符串、日期、JSON、聚合等多种场景。在编写 UDF 之前，先浏览 [SQL 函数参考](/tidb-cloud-lake/sql/sql-function-reference.md)，看看是否已经有函数可以满足你的需求。当内置函数无法表达你的逻辑时，再使用 UDF。

## 函数管理命令 {#function-management-commands}

| 命令 | 描述 |
|---------|-------------|
| [CREATE AGGREGATE FUNCTION](/tidb-cloud-lake/sql/create-aggregate-function.md) | 脚本 UDAF（JavaScript/Python 运行时） |
| [CREATE TABLE FUNCTION](/tidb-cloud-lake/sql/create-table-function.md) | 仅使用 SQL 的表函数，返回结果集 |
| [SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md) | 列出所有用户定义函数 |
| [ALTER FUNCTION](/tidb-cloud-lake/sql/alter-function.md) | 修改现有函数 |
| [DROP FUNCTION](/tidb-cloud-lake/sql/drop-function.md) | 删除函数 |

## 函数类型对比 {#function-type-comparison}

| 功能 | Scalar (SQL) | Scalar (Python/JavaScript) | Aggregate (Script) | Tabular SQL |
|---------|-------------|----------------------------|--------------------|------------|
| **返回类型** | 单个值 | 单个值 | 单个值 | 表/结果集 |
| **语言** | SQL 表达式 | Python/JavaScript | JavaScript/Python 运行时 | SQL 查询 |
| **性能** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **需要企业版** | 否 | 仅 Python runtime 需要 | 仅 Python runtime 需要 | 否 |
| **包支持** | 否 | Python：是（PACKAGES） | Python：是（PACKAGES） | 否 |
| **最适合** | 数学计算<br/>字符串操作<br/>数据格式化 | 高级算法<br/>外部库<br/>控制流逻辑 | 需要脚本逻辑的自定义聚合 | 复杂查询<br/>多行结果<br/>数据转换 |

## 统一语法 {#unified-syntax}

所有本地 UDF 类型都使用一致的 `$$` 语法：

```sql
-- Scalar Function
CREATE FUNCTION func_name(param TYPE) RETURNS TYPE AS $$ expression $$;

-- Tabular Function
CREATE FUNCTION func_name(param TYPE) RETURNS TABLE(...) AS $$ query $$;

-- Scalar Function (Python/JavaScript)
CREATE FUNCTION func_name(param TYPE) RETURNS TYPE
LANGUAGE python
HANDLER = 'handler' AS $$ code $$;
```