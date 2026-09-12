---
title: VACUUM DROP TABLE
summary: 本页介绍 TiDB Cloud Lake 中的 VACUUM DROP TABLE。
---

# VACUUM DROP TABLE

`VACUUM DROP TABLE` 命令通过永久删除已删除表的数据文件来帮助节省存储空间，从而释放存储空间，并使你能够高效地管理这一过程。它提供了可选参数，用于指定特定数据库、预览结果，以及限制要执行 vacuum 的数据文件数量。要列出某个数据库中已删除的表，请使用 [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-databases.md)。

另请参阅：[VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table-sql.md)

## 语法 {#syntax}

```sql
VACUUM DROP TABLE
    [ FROM <database_name> ]
    [ DRY RUN [SUMMARY] ]
    [ LIMIT <file_count> ]
```

- `FROM <database_name>`：此参数将已删除表的搜索范围限制在特定数据库中。如果未指定，命令将扫描所有数据库，包括那些已经被删除的数据库。

  ```sql title="Example:"
  -- Remove dropped tables from the "default" database
  // highlight-next-line
  VACUUM DROP TABLE FROM default;

  -- Remove dropped tables from all databases
  // highlight-next-line
  VACUUM DROP TABLE;
  ```

- `DRY RUN [SUMMARY]`：指定此参数时，不会删除数据文件；相反，它会返回一个结果，显示如果未指定此参数，本应被删除的数据文件。示例请参见[输出](#output)部分。

- `LIMIT <file_count>`：此参数可以与 `DRY RUN` 一起使用，也可以单独使用。与 `DRY RUN` 一起使用时，它会限制 `DRY RUN` 结果中显示的数据文件数量。不使用 `DRY RUN` 时，它会限制要执行 vacuum 的数据文件数量。

### 输出 {#output}

当指定 `DRY RUN` 或 `DRY RUN SUMMARY` 参数时，`VACUUM DROP TABLE` 命令会返回结果：

- `DRY RUN`：返回每个已删除表最多 1,000 个候选文件及其字节大小的列表。
- `DRY RUN SUMMARY`：返回每个已删除表将被删除的文件总数及其合计大小。

```sql title='Example:'
// highlight-next-line
VACUUM DROP TABLE DRY RUN;

┌──────────────────────────────────────────────────────────────────┐
│  table │                     file                    │ file_size │
├────────┼─────────────────────────────────────────────┼───────────┤
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v2.parquet │       210 │
│ b      │ 737f2215b8ac4a268d5b7f2218273358_v4.parquet │       340 │
│ b      │ 313ebd4da5cc493f9a7d491da8253ce2_v4.parquet │       340 │
│ b      │ last_snapshot_location_hint                 │        72 │
│ b      │ 7e01fa5c2e0a495298942671447dc8cb_v4.mpk     │       515 │
│ b      │ 2bc90e5be55c44258a736d27e5f7ac9e_v4.mpk     │       459 │
│ b      │ 85e73803aabc4eb48774db3d932312dd_v4.mpk     │       534 │
│ b      │ f0e507d0b825428dbfe57c8d8b620a15_v4.mpk     │       533 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v2.parquet │       210 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v2.parquet │       210 │
│ c      │ cee790e76f6e4e92bc9dab3b9e873dcf_v4.parquet │       340 │
│ c      │ 4bcb2cef3b6344cb951908ebee5ceb36_v4.parquet │       340 │
│ c      │ last_snapshot_location_hint                 │        71 │
│ c      │ 414fc6a8dc6746afbc576cf8fddfcdf3_v4.mpk     │       516 │
│ c      │ 8d0d115c438244c295e3bfd50d556e39_v4.mpk     │       458 │
│ c      │ 28e4f551cc634d3d8d7e648c3baa5f5c_v4.mpk     │       534 │
│ c      │ 007b57e08eda419fbb451a3a3ed71de8_v4.mpk     │       533 │
└──────────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM DROP TABLE DRY RUN SUMMARY;

┌───────────────────────────────────┐
│  table │ total_files │ total_size │
├────────┼─────────────┼────────────┤
│ b      │           9 │       3213 │
│ c      │           9 │       3212 │
└───────────────────────────────────┘
```

### 调整数据保留时间 {#adjusting-data-retention-time}

`VACUUM DROP TABLE` 命令会删除早于 `DATA_RETENTION_TIME_IN_DAYS` 设置的数据文件。可以根据需要调整此保留时间，例如设置为 2 天：

```sql
SET GLOBAL DATA_RETENTION_TIME_IN_DAYS = 2;
```

`DATA_RETENTION_TIME_IN_DAYS` 的默认值为 1 天（24 小时），最大值因 {{{ .lake }}} 版本而异：

| 版本 | 默认保留时间 | 最大保留时间 |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} 社区版和企业版 | 1 天（24 小时） | 90 天 |
| {{{ .lake }}} (Personal)                | 1 天（24 小时） | 1 天（24 小时） |
| {{{ .lake }}} (Business)                | 1 天（24 小时） | 90 天 |

要检查 `DATA_RETENTION_TIME_IN_DAYS` 的当前值：

```sql
SHOW SETTINGS LIKE 'DATA_RETENTION_TIME_IN_DAYS';
```