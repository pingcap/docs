---
title: DROP TAG
summary: Removes a tag. A tag cannot be dropped if it is still referenced by any object.
---

# DROP TAG

> **Note:**
>
> Introduced or updated in v1.2.863.

Removes a tag. A tag cannot be dropped if it is still referenced by any object — you must first unset the tag from all objects or drop those objects.

See also: [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md), [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

## Syntax

```sql
DROP TAG [ IF EXISTS ] <tag_name>
```

## Examples

```sql
-- Fails if the tag is still in use
DROP TAG env;
-- Error: Tag 'env' still has references

-- Remove the tag reference first
ALTER TABLE my_table UNSET TAG env;

-- Now it succeeds
DROP TAG env;
```

Drop a tag only if it exists:

```sql
DROP TAG IF EXISTS env;
```
