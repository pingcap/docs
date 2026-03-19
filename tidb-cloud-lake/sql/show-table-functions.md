---
title: SHOW TABLE FUNCTIONS
summary: Shows the list of supported table functions currently.
---

# SHOW TABLE FUNCTIONS

> **Note:**
>
> Introduced or updated in v1.2.190.

Shows the list of supported table functions currently.

## Syntax

```sql
SHOW TABLE_FUNCTIONS [LIKE '<pattern>' | WHERE <expr>] | [LIMIT <limit>]
```

## Example

```sql
SHOW TABLE_FUNCTIONS;
+------------------------+
| name                   |
+------------------------+
| numbers                |
| numbers_mt             |
| numbers_local          |
| fuse_snapshot          |
| fuse_segment           |
| fuse_block             |
| fuse_statistic         |
| clustering_information |
| sync_crash_me          |
| async_crash_me         |
| infer_schema           |
+------------------------+
```

Showing the table functions begin with `"number"`:
```sql
SHOW TABLE_FUNCTIONS LIKE 'number%';
+---------------+
| name          |
+---------------+
| numbers       |
| numbers_mt    |
| numbers_local |
+---------------+
```

Showing the table functions begin with `"number"` with `WHERE`:
```sql
SHOW TABLE_FUNCTIONS WHERE name LIKE 'number%';
+---------------+
| name          |
+---------------+
| numbers       |
| numbers_mt    |
| numbers_local |
+---------------+
```
