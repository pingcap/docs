---
title: Delta Lake Engine
summary: "{{{ .lake }}} 的 Delta Lake engine 允许你无缝查询和分析存储在对象存储中的 Delta Lake 表数据。在 {{{ .lake }}} 中使用 Delta Lake engine 创建表时，你需要指定 Delta Lake 表数据文件的存储位置。通过这种方式，你可以直接访问该表，并在 {{{ .lake }}} 内无缝执行查询。"
---

# Delta Lake Engine

{{{ .lake }}} 的 [Delta Lake](https://delta.io/) engine 允许你无缝查询和分析存储在对象存储中的 Delta Lake 表数据。在 {{{ .lake }}} 中使用 Delta Lake engine 创建表时，你需要指定 Delta Lake 表数据文件的存储位置。通过这种方式，你可以直接访问该表，并在 {{{ .lake }}} 内无缝执行查询。

- {{{ .lake }}} 的 Delta Lake engine 当前仅支持只读操作。这意味着支持从 Delta Lake 表中查询数据，但不支持向表中写入数据。
- 使用 Delta Lake engine 创建的表，其 schema 会在创建时确定。若原始 Delta Lake 表的 schema 发生任何修改，则需要在 {{{ .lake }}} 中重新创建对应的表，以确保两者保持同步。
- {{{ .lake }}} 中的 Delta Lake engine 基于官方 [delta-rs](https://github.com/delta-io/delta-rs) 库构建。需要注意的是，delta-protocol 中定义的某些特性（包括 Deletion Vector、Change Data Feed、Generated Columns 和 Identity Columns）当前**不**受该 engine 支持。

## 语法 {#syntax}

```sql
CREATE TABLE <table_name>
ENGINE = Delta
LOCATION = 's3://<path_to_table>'
CONNECTION_NAME = '<connection_name>'
```

在使用 Delta Lake engine 创建表之前，你需要先创建一个 connection 对象，用于与 S3 存储建立连接。要在 {{{ .lake }}} 中创建 connection，请使用 [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md) 命令。

## 示例 {#examples}

```sql
--Set up connection
CREATE CONNECTION my_s3_conn
STORAGE_TYPE = 's3'
ACCESS_KEY_ID ='your-ak' SECRET_ACCESS_KEY ='your-sk';

-- Create table with Delta Lake engine
CREATE TABLE test_delta
ENGINE = Delta
LOCATION = 's3://testbucket/admin/data/delta/delta-table/'
CONNECTION_NAME = 'my_s3_conn';
```