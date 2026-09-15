---
title: STREAM_STATUS
summary: 提供有关指定 stream 状态的信息，并返回单列结果（has_data），其值可以为 true 或 false。
---

# STREAM_STATUS

提供有关指定 stream 状态的信息，并返回单列结果（`has_data`），其值可以为 `true` 或 `false`：

- `true`：表示该 stream **可能包含** change data capture 记录。
- `false`：表示该 stream 当前不包含任何 change data capture 记录。

> **Note:**
>
> 结果（`has_data`）中出现 `true` **并不** 能确保一定存在 change data capture 记录。其他操作（例如执行表 compact 操作）也可能导致返回 `true`，即使实际上并不存在任何 change data capture 记录。

> **Note:**
>
> 在任务中使用 `STREAM_STATUS` 时，引用 stream 必须包含数据库名（例如：`STREAM_STATUS('mydb.stream_name')`）。

## 语法 {#syntax}

```sql
SELECT * FROM STREAM_STATUS('<database_name>.<stream_name>');
-- OR
SELECT * FROM STREAM_STATUS('<stream_name>');  -- Uses current database
```

## 示例 {#examples}

```sql
-- Create a table 't' with a column 'c'
CREATE TABLE t (c int);

-- Create a stream 's' on the table 't'
CREATE STREAM s ON TABLE t;

-- Check the initial status of the stream 's'
SELECT * FROM STREAM_STATUS('s');

-- The result should be 'false' indicating no change data capture records initially
┌──────────┐
│ has_data │
├──────────┤
│ false    │
└──────────┘

-- Insert a value into the table 't'
INSERT INTO t VALUES (1);

-- Check the updated status of the stream 's' after the insertion
SELECT * FROM STREAM_STATUS('s');

-- The result should now be 'true' indicating the presence of change data capture records
┌──────────┐
│ has_data │
├──────────┤
│ true     │
└──────────┘

-- Example with database name specified
SELECT * FROM STREAM_STATUS('mydb.s');
```