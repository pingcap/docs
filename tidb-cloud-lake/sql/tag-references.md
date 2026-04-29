---
title: TAG_REFERENCES
summary: Returns all tags assigned to a specified database object.
---

# TAG_REFERENCES

> **Note:**
>
> Introduced or updated in v1.2.866.

Returns all tags assigned to a specified database object. Use this function to audit tag assignments for governance and compliance.

See also: [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

## Syntax

```sql
SELECT * FROM TAG_REFERENCES('<object_name>', '<domain>')
```

| Parameter       | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| `object_name`   | Name of the object. For tables/views/streams, use `db.name` format. For procedures, include the type signature (e.g., `my_proc(INT)`). |
| `domain`        | Object type: `DATABASE`, `TABLE`, `VIEW`, `STREAM`, `STAGE`, `CONNECTION`, `USER`, `ROLE`, `UDF`, or `PROCEDURE`.        |

## Output Columns

| Column            | Type             | Description                                 |
|-------------------|------------------|---------------------------------------------|
| `tag_name`        | String           | Name of the tag                                              |
| `tag_value`       | String           | Value assigned to the tag                                    |
| `object_database` | Nullable(String) | Database name (NULL for STAGE, CONNECTION, USER, ROLE, UDF, PROCEDURE) |
| `object_id`       | Nullable(UInt64) | Object ID (non-NULL only for DATABASE, TABLE, VIEW)          |
| `object_name`     | String           | Name of the object                                           |
| `domain`          | String           | Object type                                                  |

## Examples

### Query Tags on a Table

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

CREATE TABLE default.users (id INT, name STRING);
ALTER TABLE default.users SET TAG env = 'prod', owner = 'team_a';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default.users', 'TABLE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ users       │ TABLE        │
│ owner    │ team_a    │ default         │ users       │ TABLE        │
└───────────────────────────────────────────────────────────────────────┘
```

### Query Tags on a Stage

```sql
CREATE STAGE data_stage;
ALTER STAGE data_stage SET TAG env = 'staging', owner = 'data_team';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('data_stage', 'STAGE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ staging   │ NULL            │ data_stage  │ STAGE        │
│ owner    │ data_team │ NULL            │ data_stage  │ STAGE        │
└───────────────────────────────────────────────────────────────────────┘
```

### Query Tags on a Database

```sql
ALTER DATABASE default SET TAG env = 'prod';

SELECT * EXCLUDE(object_id) FROM TAG_REFERENCES('default', 'DATABASE');

┌───────────────────────────────────────────────────────────────────────┐
│ tag_name │ tag_value │ object_database │ object_name │    domain    │
├──────────┼───────────┼─────────────────┼─────────────┼──────────────┤
│ env      │ prod      │ default         │ default     │ DATABASE     │
└───────────────────────────────────────────────────────────────────────┘
```
