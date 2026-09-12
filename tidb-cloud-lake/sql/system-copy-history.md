---
title: system.copy_history
summary: 包含有关复制历史的信息。
---

# system.copy_history

包含有关复制历史的信息。

## 语法 {#syntax}

```sql
SELECT * FROM copy_history('<table_name>');
```

- `table_name`：表名。

```sql
select * from copy_history('my_table');

╭──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                          file_name                          │ content_length │        last_modified       │       etag       │
│                            String                           │     UInt64     │     Nullable(Timestamp)    │ Nullable(String) │
├─────────────────────────────────────────────────────────────┼────────────────┼────────────────────────────┼──────────────────┤
│ data_0199db4c843a70b2b81f115f01c8de97_0000_00000000.parquet │          10531 │ 2025-10-13 02:00:49.083208 │ NULL             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

请注意，`system.copy_history` 的结果受设置项 `load_file_metadata_expire_hours` 的影响，该设置的默认值为 24 小时。