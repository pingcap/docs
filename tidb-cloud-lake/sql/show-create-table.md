---
title: SHOW CREATE TABLE
summary: 显示指定表的 CREATE TABLE 语句。要在结果中包含 Fuse Engine 选项，请将 hide_options_in_show_create_table 设置为 0。
---

# SHOW CREATE TABLE

显示指定表的 CREATE TABLE 语句。要在结果中包含 Fuse Engine 选项，请将 `hide_options_in_show_create_table` 设置为 `0`。

## 语法 {#syntax}

```sql
SHOW CREATE TABLE [ <database_name>. ]<table_name>
```

## 示例 {#examples}

以下示例展示了如何通过将 `hide_options_in_show_create_table` 设置为 `0` 来显示完整的 CREATE TABLE 语句，包括 Fuse Engine 选项：

```sql
CREATE TABLE fuse_table (a int);

SHOW CREATE TABLE fuse_table;

-[ RECORD 1 ]-----------------------------------
       Table: fuse_table
Create Table: CREATE TABLE fuse_table (
  a INT NULL
) ENGINE=FUSE

SET hide_options_in_show_create_table=0;

SHOW CREATE TABLE fuse_table;

-[ RECORD 1 ]-----------------------------------
       Table: fuse_table
Create Table: CREATE TABLE fuse_table (
  a INT NULL
) ENGINE=FUSE COMPRESSION='lz4' DATA_RETENTION_PERIOD_IN_HOURS='240' STORAGE_FORMAT='native'
```