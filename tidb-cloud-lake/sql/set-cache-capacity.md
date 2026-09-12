---
title: SYSTEM$SET_CACHE_CAPACITY
summary: 在运行时调整指定缓存的容量。
---

# SYSTEM$SET_CACHE_CAPACITY

在运行时为指定名称的缓存设置最大容量。更改会立即生效，但**不会持久化**——重启后，缓存会恢复为配置文件中的值。

另请参阅：[system.caches](/tidb-cloud-lake/sql/system-caches.md)。

## 语法 {#syntax}

```sql
CALL system$set_cache_capacity('<cache_name>', <new_capacity>)
```

| 参数 | 描述 |
|--------------|--------------------------------------------------------------------------|
| cache_name   | 缓存名称（参见 [system.caches](/tidb-cloud-lake/sql/system-caches.md) 中的缓存列表） |
| new_capacity | 新的容量值。单位（数量或字节）取决于缓存类型。 |

## 注意事项 {#notes}

- 如果新容量**大于**当前值，则会保留现有缓存条目。
- 如果新容量**小于**当前值，则可能会根据 LRU 策略逐出条目。
- 更改**不会持久化**。重启后，容量会恢复为配置文件中的值。
- `disk_cache_column_data` 不能使用此命令调整。

## 示例 {#examples}

将 bloom index metadata cache 设置为 5000 个条目：

```sql
CALL system$set_cache_capacity('memory_cache_bloom_index_file_meta_data', 5000);

┌────────────────────────┬────────┐
│ node                   │ result │
├────────────────────────┼────────┤
│ Gwo2DYOLZ9zAdYbGTWY9y6 │ Ok     │
└────────────────────────┴────────┘
```

为测试禁用 partition pruning cache：

```sql
CALL system$set_cache_capacity('memory_cache_prune_partitions', 0);
```