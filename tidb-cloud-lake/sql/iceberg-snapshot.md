---
title: ICEBERG_SNAPSHOT
summary: 返回 Iceberg 表快照的元信息，包括有关数据变更、操作和汇总统计的信息。
---

# ICEBERG_SNAPSHOT

返回 Iceberg 表快照的元信息，包括有关数据变更、操作和汇总统计的信息。

## 语法 {#syntax}

```sql
ICEBERG_SNAPSHOT('<database_name>', '<table_name>');
```

## 输出 {#output}

该函数返回一个包含以下列的表：

- `committed_at` (`TIMESTAMP`)：提交该快照时的时间戳。
- `snapshot_id` (`BIGINT`)：快照的唯一标识符。
- `parent_id` (`BIGINT`)：父快照 ID（如果适用）。
- `operation` (`STRING`)：执行的操作类型（例如 append、overwrite、delete）。
- `manifest_list` (`STRING`)：与该快照关联的 manifest list 文件路径。
- `summary` (`MAP<STRING, STRING>`)：一种类似 JSON 的结构，包含附加元信息，例如：
    - `added-data-files`：新添加的数据文件数量。
    - `added-records`：新添加的记录数。
    - `total-records`：该快照中的记录总数。
    - `total-files-size`：所有数据文件的总大小（以字节为单位）。
    - `total-data-files`：该快照中的数据文件总数。
    - `total-delete-files`：删除文件总数。

## 示例 {#examples}

```sql
SELECT * FROM ICEBERG_SNAPSHOT('tpcds', 'catalog_returns');

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│        committed_at        │     snapshot_id     │ parent_id │ operation │                     manifest_list                    │                       summary                       │
├────────────────────────────┼─────────────────────┼───────────┼───────────┼──────────────────────────────────────────────────────┼─────────────────────────────────────────────────────┤
│ 2025-03-12 23:18:26.626000 │ 7565767416590411866 │         0 │ append    │ s3://warehouse/catalog_returns/metadata/snap-7565767 │ {'spark.app.id':'local-1741821433430','added-data-f │
│                            │                     │           │           │ 416590411866-1-fa1ea4d5-a382-497a-9f22-1acb9a74a346. │ iles':'2','added-records':'144067','total-equality- │
│                            │                     │           │           │ avro                                                 │ deletes':'0','changed-partition-count':'1','total-r │
│                            │                     │           │           │                                                      │ ecords':'144067','total-files-size':'7679811','tota │
│                            │                     │           │           │                                                      │ l-data-files':'2','added-files-size':'7679811','tot │
│                            │                     │           │           │                                                      │ al-delete-files':'0','total-position-deletes':'0'}  │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```