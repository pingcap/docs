---
title: SHOW CREATE TABLE
summary: 指定したテーブルの CREATE TABLE 文を表示します。結果に Fuse Engine のオプションを含めるには、hide_options_in_show_create_table を 0 に設定します。
---

# SHOW CREATE TABLE

指定したテーブルの CREATE TABLE 文を表示します。結果に Fuse Engine のオプションを含めるには、`hide_options_in_show_create_table` を `0` に設定します。

## 構文 {#syntax}

```sql
SHOW CREATE TABLE [ <database_name>. ]<table_name>
```

## 例 {#examples}

この例では、`hide_options_in_show_create_table` を `0` に設定することで、Fuse Engine のオプションを含む完全な CREATE TABLE 文を表示する方法を示します。

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