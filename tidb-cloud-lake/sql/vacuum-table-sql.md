---
title: VACUUM TABLE
summary: 本页介绍 TiDB Cloud Lake 中的 VACUUM TABLE。
---

# VACUUM TABLE

`VACUUM TABLE` 命令通过永久删除表中的历史数据文件来释放存储空间，从而帮助优化系统性能。包括：

- 与该表关联的快照，以及其相关的 segments 和 blocks。

- 孤儿文件。在 {{{ .lake }}} 中，孤儿文件是指不再与该表关联的 snapshots、segments 和 blocks。孤儿文件可能由各种操作和错误产生，例如在数据备份和恢复期间，并且会占用宝贵的磁盘空间，随着时间推移还会降低系统性能。

另请参阅：[VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table-sql.md)

## 语法和示例 {#syntax-and-examples}

```sql
VACUUM TABLE <table_name> [ DRY RUN [SUMMARY] ]
```

- `DRY RUN [SUMMARY]`：指定此参数后，不会删除候选孤儿文件。相反，命令会返回最多 1,000 个候选文件及其大小（以字节为单位）的列表，展示如果未使用该选项本应删除的内容。包含可选参数 `SUMMARY` 时，命令会返回将要删除的文件总数及其合计大小（以字节为单位）。

### 输出 {#output}

`VACUUM TABLE` 命令（不带 `DRY RUN`）会返回一个表，用于汇总被 vacuum 的文件的重要统计信息，包含以下列：

| 列 | 描述 |
| -------------- | ----------------------------------------- |
| snapshot_files | 快照文件数量 |
| snapshot_size  | 快照文件总大小（字节） |
| segments_files | segment 文件数量 |
| segments_size  | segment 文件总大小（字节） |
| block_files    | block 文件数量 |
| block_size     | block 文件总大小（字节） |
| index_files    | 索引文件数量 |
| index_size     | 索引文件总大小（字节） |
| total_files    | 所有类型文件的总数量 |
| total_size     | 所有类型文件的总大小（字节） |

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ snapshot_files │ snapshot_size │ segments_files │ segments_size │ block_files │ block_size │ index_files │ index_size │ total_files │ total_size │
├────────────────┼───────────────┼────────────────┼───────────────┼─────────────┼────────────┼─────────────┼────────────┼─────────────┼────────────┤
│              3 │          1954 │              9 │          4802 │           9 │       1890 │           9 │       3060 │          30 │      11706 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

当 `VACUUM TABLE` 命令指定 `DRY RUN` 参数时，会返回最多 1,000 个候选文件及其大小（以字节为单位）的列表。如果指定 `DRY RUN SUMMARY`，命令会返回将要删除的文件总数及其合计大小。

```sql title='Example:'
// highlight-next-line
VACUUM TABLE c DRY RUN;

┌──────────────────────────────────────────────────────────────┐
│                       file                       │ file_size │
├──────────────────────────────────────────────────┼───────────┤
│ 1/67/_ss/61aaf678b9af41568b539099b4b09908_v4.mpk │       543 │
│ 1/67/_ss/dd149d21151c459d8c87076f9412c12c_v4.mpk │       516 │
│ 1/67/_ss/7ba0b2e2f63c4d42897a48830027dcf3_v4.mpk │       462 │
│ 1/67/_ss/db55dac72b29452db976cf0af0f8d962_v4.mpk │       588 │
│ 1/67/_ss/d8055967298f478d97cddaa66cf67e11_v4.mpk │       563 │
│ 1/67/_ss/00c4288dac014760808006f821f1ecbe_v4.mpk │       609 │
└──────────────────────────────────────────────────────────────┘
// highlight-next-line
VACUUM TABLE c DRY RUN SUMMARY;

┌──────────────────────────┐
│ total_files │ total_size │
├─────────────┼────────────┤
│           6 │       3281 │
└──────────────────────────┘
```

### 调整数据保留时间 {#adjusting-data-retention-time}

`VACUUM TABLE` 命令会删除早于 `data_retention_time_in_days` 设置的数据文件。可以根据需要调整该保留时间，例如设置为 2 天：

```sql
SET GLOBAL data_retention_time_in_days = 2;
```

`data_retention_time_in_days` 的默认值为 1 天（24 小时），最大值因 {{{ .lake }}} 版本而异：

| 版本 | 默认保留时间 | 最大保留时间 |
| ---------------------------------------- | ----------------- | ---------------- |
| {{{ .lake }}} 社区版和企业版 | 1 天（24 小时） | 90 天 |
| {{{ .lake }}} (Personal)                | 1 天（24 小时） | 1 天（24 小时） |
| {{{ .lake }}} (Business)                | 1 天（24 小时） | 90 天 |

要检查 `data_retention_time_in_days` 的当前值，请执行：

```sql
SHOW SETTINGS LIKE 'data_retention_time_in_days';
```

### VACUUM TABLE 与 OPTIMIZE TABLE 的区别 {#vacuum-table-vs-optimize-table}

{{{ .lake }}} 提供了两个命令用于删除表中的历史数据文件：`VACUUM TABLE` 和 [OPTIMIZE TABLE](/tidb-cloud-lake/sql/optimize-table.md)（带 `PURGE` 选项）。虽然这两个命令都可以永久删除数据文件，但它们在处理孤儿文件的方式上有所不同：`OPTIMIZE TABLE` 能够删除孤儿快照，以及相应的 segments 和 blocks。但是，也可能存在没有任何关联快照的孤儿 segments 和 blocks。在这种场景下，只有 `VACUUM TABLE` 能帮助清理它们。

`VACUUM TABLE` 和 `OPTIMIZE TABLE` 都允许你指定一个时间范围，以确定要删除哪些历史数据文件。不过，`OPTIMIZE TABLE` 需要你事先通过查询获取 snapshot ID 或时间戳，而 `VACUUM TABLE` 允许你直接指定要保留数据文件的小时数。`VACUUM TABLE` 还通过 `DRY RUN` 选项提供了更强的历史数据文件控制能力，使你可以在实际执行命令前预览将要删除的数据文件。这带来了更安全的删除体验，并帮助你避免意外的数据丢失。

|                                                  | VACUUM TABLE | OPTIMIZE TABLE |
| ------------------------------------------------ | ------------ | -------------- |
| 关联的快照（包括 segments 和 blocks） | Yes          | Yes            |
| 孤儿快照（包括 segments 和 blocks） | Yes          | Yes            |
| 仅孤儿 segments 和 blocks                  | Yes          | No             |
| DRY RUN                                          | Yes          | No             |