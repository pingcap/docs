---
title: SQL 变量
summary: SQL 变量允许你在会话中存储和管理临时数据，使脚本更具动态性和可复用性。
---

# SQL 变量

SQL 变量允许你在会话中存储和管理临时数据，使脚本更具动态性和可复用性。

## 变量命令 {#variable-commands}

| 命令 | 描述 |
|---------|-------------|
| [SET VARIABLE](/tidb-cloud-lake/sql/set-variable.md) | 创建或修改会话变量或用户变量。 |
| [UNSET VARIABLE](/tidb-cloud-lake/sql/unset-variable.md) | 删除用户定义的变量。 |
| [SHOW VARIABLES](/tidb-cloud-lake/sql/show-variables.md) | 显示系统变量和用户变量的当前值。 |

SHOW VARIABLES 命令还有一个对应的表函数 [`SHOW_VARIABLES`](/tidb-cloud-lake/sql/show-variables.md)，它以表格形式返回相同的信息，以便进行更丰富的过滤和查询。

## 使用变量进行查询 {#querying-with-variables}

你可以在语句中引用变量，以实现动态值替换或在运行时构建对象名称。

### 使用 `$` 和 `getvariable()` 访问变量 {#accessing-variables-with-and-getvariable}

使用 `$` 符号或 `getvariable()` 函数，可以将变量值直接嵌入查询中。

```sql title='Example:'
-- Set a variable to use as a filter value
SET VARIABLE threshold = 100;

-- Use the variable in a query with $
SELECT * FROM sales WHERE amount > $threshold;

-- Alternatively, use the getvariable() function
SELECT * FROM sales WHERE amount > getvariable('threshold');
```

### 使用 `IDENTIFIER` 访问对象 {#accessing-objects-with-identifier}

`IDENTIFIER` 关键字允许你引用名称存储在变量中的数据库对象，从而实现灵活的查询构造。（注意：LakeSQL 目前尚不支持 `IDENTIFIER`。）

```sql title='Example:'
-- Create a table with sales data
CREATE TABLE sales_data (region TEXT, sales_amount INT, month TEXT) AS
SELECT 'North', 5000, 'January' UNION ALL
SELECT 'South', 3000, 'January';

select * from sales_data;

-- Set variables for the table name and column name
SET VARIABLE table_name = 'sales_data';
SET VARIABLE column_name = 'sales_amount';

-- Use IDENTIFIER to dynamically reference the table and column in the query
SELECT region, IDENTIFIER($column_name)
FROM IDENTIFIER($table_name)
WHERE IDENTIFIER($column_name) > 4000;
```