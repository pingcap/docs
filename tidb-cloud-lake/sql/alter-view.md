---
title: ALTER VIEW
summary: Alter the existing view by using another QUERY.
---

# ALTER VIEW

Assigns or removes tags on an existing view. Tags must be created with [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) first. For full details, see [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

> **Note:**
>
> `ALTER VIEW ... AS ...` is not supported. To change a view's query or output columns, use [CREATE OR REPLACE VIEW](/tidb-cloud-lake/sql/create-view.md) instead.

## Syntax

```sql
ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER VIEW [ IF EXISTS ] [ <database_name>. ]<view_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## Examples

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
ALTER VIEW default.active_users UNSET TAG env, owner;
```
