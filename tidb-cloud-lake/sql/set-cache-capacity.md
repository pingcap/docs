---
title: SYSTEM$SET_CACHE_CAPACITY
summary: Adjusts the capacity of a named cache at runtime.
---

# SYSTEM$SET_CACHE_CAPACITY

Sets the maximum capacity for a named cache at runtime. Changes take effect immediately but are **not persisted** — the cache reverts to the value in the configuration file after a restart.

See also: [system.caches](/tidb-cloud-lake/sql/system-caches.md).

## Syntax

```sql
CALL system$set_cache_capacity('<cache_name>', <new_capacity>)
```

| Parameter    | Description                                                              |
|--------------|--------------------------------------------------------------------------|
| cache_name   | The name of the cache (see the cache list in [system.caches](/tidb-cloud-lake/sql/system-caches.md)) |
| new_capacity | New capacity value. Unit (count or bytes) depends on the cache type.                                                                 |

## Notes

- If the new capacity is **larger** than the current value, existing cache entries are retained.
- If the new capacity is **smaller**, entries may be evicted according to the LRU policy.
- Changes are **not persisted**. After a restart, the capacity reverts to the configuration file value.
- `disk_cache_column_data` cannot be adjusted with this command.

## Examples

Set the bloom index metadata cache to 5000 entries:

```sql
CALL system$set_cache_capacity('memory_cache_bloom_index_file_meta_data', 5000);

┌────────────────────────┬────────┐
│ node                   │ result │
├────────────────────────┼────────┤
│ Gwo2DYOLZ9zAdYbGTWY9y6 │ Ok     │
└────────────────────────┴────────┘
```

Disable partition pruning cache for testing:

```sql
CALL system$set_cache_capacity('memory_cache_prune_partitions', 0);
```
