---
title: CREATE TAG
summary: Creates a new tag with optional allowed values and comment.
---

# CREATE TAG

> **Note:**
>
> Introduced or updated in v1.2.863.

Creates a new tag. Tags are tenant-level metadata objects that can be assigned to database objects for governance and classification.

See also: [DROP TAG](/tidb-cloud-lake/sql/drop-tag.md), [SHOW TAGS](/tidb-cloud-lake/sql/show-tags.md), [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

## Syntax

```sql
CREATE TAG [ IF NOT EXISTS ] <tag_name>
    [ ALLOWED_VALUES = ( '<value1>' [, '<value2>', ... ] ) ]
    [ COMMENT = '<string>' ]
```

| Parameter        | Description                                              |
|------------------|----------------------------------------------------------|
| `tag_name`       | Name of the tag to create.                                                                                            |
| `ALLOWED_VALUES` | Optional list of permitted values. When set, only these values can be used in SET TAG. Duplicate values are removed automatically. |
| `COMMENT`        | Optional description for the tag.                                                                                     |

## Examples

Create a tag with allowed values and a comment:

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod') COMMENT = 'Environment classification';
```

Create a tag that accepts any value:

```sql
CREATE TAG owner COMMENT = 'Data owner';
```

Create a tag with no restrictions:

```sql
CREATE TAG cost_center;
```

Verify tag definitions:

```sql
SELECT name, allowed_values, comment FROM system.tags ORDER BY name;

┌──────────────────────────────────────────────────────────────────────┐
│      name      │       allowed_values       │         comment        │
├────────────────┼────────────────────────────┼────────────────────────┤
│ cost_center    │ NULL                       │                        │
│ env            │ ['dev', 'staging', 'prod'] │ Environment classific… │
│ owner          │ NULL                       │ Data owner             │
└──────────────────────────────────────────────────────────────────────┘
```
