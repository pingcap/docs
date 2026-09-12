---
title: CREATE TEMP TABLE
summary: 创建一个在会话结束时自动删除的临时表。
---

# CREATE TEMP TABLE

创建一个在会话结束时自动删除的临时表。

- 临时表仅在创建它的会话内可见，并会在会话结束时自动删除，同时清理其中的所有数据。
       - 如果临时表的自动清理失败——例如由于查询节点崩溃——你可以使用 [FUSE_VACUUM_TEMPORARY_TABLE](/tidb-cloud-lake/sql/fuse-vacuum-temporary-table.md) 函数手动清理临时表遗留的文件。
- 要显示当前会话中已有的临时表，请查询 [system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) 系统表。参见 [Example-1](#example-1)。
- 如果临时表与普通表同名，则临时表优先生效，在其被删除之前会隐藏普通表。参见 [Example-2](#example-2)。
- 创建或操作临时表不需要任何权限。
- {{{ .lake }}} 支持使用 [Fuse Engine](/tidb-cloud-lake/sql/table-engines.md) 创建临时表。
- 要使用 LakeSQL 创建临时表，请确保你使用的是最新版本的 LakeSQL。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] { TEMPORARY | TEMP } TABLE
       [ IF NOT EXISTS ]
       [ <database_name>. ]<table_name>
       ...
```

省略的部分遵循 [CREATE TABLE](/tidb-cloud-lake/sql/create-table.md) 的语法。

## 示例 {#examples}

### Example-1 {#example-1}

本示例演示如何创建临时表，并通过查询 [system.temporary_tables](/tidb-cloud-lake/sql/system-tables.md) 系统表来验证其是否存在：

```sql
CREATE TEMP TABLE my_table (id INT, description STRING);

SELECT * FROM system.temporary_tables;

┌────────────────────────────────────────────────────┐
│ database │   name   │       table_id      │ engine │
├──────────┼──────────┼─────────────────────┼────────┤
│ default  │ my_table │ 4611686018427407904 │ FUSE   │
└────────────────────────────────────────────────────┘
```

### Example-2 {#example-2}

本示例演示同名临时表如何优先生效。当两张表同时存在时，操作会作用于临时表，从而有效隐藏普通表。临时表删除后，普通表将再次可访问：

```sql
-- Create a normal table
CREATE TABLE my_table (id INT, name STRING);

-- Insert data into the normal table
INSERT INTO my_table VALUES (1, 'Alice'), (2, 'Bob');

-- Create a temporary table with the same name
CREATE TEMP TABLE my_table (id INT, description STRING);

-- Insert data into the temporary table
INSERT INTO my_table VALUES (1, 'Temp Data');

-- Query the table: This will access the temporary table, hiding the normal table
SELECT * FROM my_table;

┌────────────────────────────────────┐
│        id       │    description   │
├─────────────────┼──────────────────┤
│               1 │ Temp Data        │
└────────────────────────────────────┘

-- Drop the temporary table
DROP TABLE my_table;

-- Query the table again: Now the normal table is accessible
SELECT * FROM my_table;

┌────────────────────────────────────┐
│        id       │       name       │
├─────────────────┼──────────────────┤
│               1 │ Alice            │
│               2 │ Bob              │
└────────────────────────────────────┘
```