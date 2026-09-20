---
title: VACUUM VIRTUAL COLUMN
summary: Removes obsolete virtual column files for a table.
---

# VACUUM VIRTUAL COLUMN

Removes obsolete virtual column files for a table.

> **Note:**
>
> This command requires the virtual column enterprise feature.

## Syntax

```sql
VACUUM VIRTUAL COLUMN FROM [ <catalog_name>. ][ <database_name>. ]<table_name>
```

## Output

Returns the number of removed files.
