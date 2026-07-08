---
title: DROP VIEW
summary: Drop the view.
---

# DROP VIEW

Drop the view.

## Syntax

```sql
DROP VIEW [ IF EXISTS ] [ <database_name>. ]view_name
```

## Examples

```sql
DROP VIEW IF EXISTS tmp_view;

SELECT * FROM tmp_view;
ERROR 1105 (HY000): Code: 1025, Text = Unknown table 'tmp_view'.
```
