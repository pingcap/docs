---
title: SHOW VIRTUAL COLUMNS
summary: 显示系统中已创建的虚拟列。等同于 SELECT * FROM system.virtual_columns。
---

# SHOW VIRTUAL COLUMNS

显示系统中已创建的虚拟列。等同于 `SELECT * FROM system.virtual_columns`。

从 v1.2.832 开始，默认启用虚拟列。

另请参阅：[system.virtual_columns](/tidb-cloud-lake/sql/system-virtual-columns.md)

## 首选语法 {#preferred-syntax}

使用该命令最简单且最实用的形式来查看特定表，或列出所有虚拟列：

```sql
SHOW VIRTUAL COLUMNS [WHERE table = '<table_name>' AND database = '<database_name>']
```

## 示例 {#example}

```sql
CREATE TABLE test(id int, val variant);

INSERT INTO
  test
VALUES
  (
    1,
    '{"id":1,"name":"datalake"}'
  ),
  (
    2,
    '{"id":2,"name":"databricks"}'
  );

SHOW VIRTUAL COLUMNS WHERE table = 'test' AND database = 'default';
╭───────────────────────────────────────────────────────────────────────────────────────────────────╮
│ database │  table │ source_column │ virtual_column_id │ virtual_column_name │ virtual_column_type │
│  String  │ String │     String    │       UInt32      │        String       │        String       │
├──────────┼────────┼───────────────┼───────────────────┼─────────────────────┼─────────────────────┤
│ default  │ test   │ val           │        3000000000 │ ['id']              │ UInt64              │
│ default  │ test   │ val           │        3000000001 │ ['name']            │ String              │
╰───────────────────────────────────────────────────────────────────────────────────────────────────╯
```