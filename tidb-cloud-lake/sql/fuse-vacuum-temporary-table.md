---
title: FUSE_VACUUM_TEMPORARY_TABLE
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.666"/>

## Overview

Temporary tables are typically cleaned up automatically at session end (details in [CREATE TEMP TABLE](../../10-sql-commands/00-ddl/01-table/10-ddl-create-temp-table.md)). However, this process can fail due to events like query node crashes or abnormal session terminations, leaving orphaned temporary files.

`FUSE_VACUUM_TEMPORARY_TABLE()` manually removes these leftover files to reclaim storage.

**When to use this function:**
- After known system failures or abnormal session terminations.
- If you suspect orphaned temporary data is consuming storage.
- As a periodic maintenance task in environments prone to such issues.

## Operational Safety

The `FUSE_VACUUM_TEMPORARY_TABLE()` function is designed to be a safe and reliable operation.
- **Targets Only Temporary Data:** It specifically identifies and removes only orphaned data and metadata files that belong to temporary tables.
- **No Impact on Regular Tables:** The function will not affect any regular, persistent tables or their data. Its scope is strictly limited to the cleanup of unreferenced temporary table remnants.

## Syntax

```sql
FUSE_VACUUM_TEMPORARY_TABLE();
```


## Examples

```sql
SELECT * FROM FUSE_VACUUM_TEMPORARY_TABLE();

┌────────┐
│ result │
├────────┤
│ Ok     │
└────────┘
```
