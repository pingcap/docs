---
title: SHOW CREATE TABLE
sidebar_position: 10
---

Shows the CREATE TABLE statement for the specified table. To include the Fuse Engine options in the result, set `hide_options_in_show_create_table` to `0`.

## Syntax

```sql
SHOW CREATE TABLE [ <database_name>. ]<table_name>
```

## Examples

This example shows how to display the full CREATE TABLE statement, including the Fuse Engine options, by setting `hide_options_in_show_create_table` to `0`:

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
