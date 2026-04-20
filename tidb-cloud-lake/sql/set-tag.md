---
title: SET TAG and UNSET TAG
summary: Assigns or removes tags on database objects.
---

# SET TAG and UNSET TAG

> **Note:**
>
> Introduced or updated in v1.2.866.

Assigns or removes tags on database objects. Tags must be created with [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) before they can be assigned.

See also: [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md), [TAG_REFERENCES](/tidb-cloud-lake/sql/tag-references.md).

## Syntax

```sql
-- Assign tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

-- Remove tags
ALTER { DATABASE | TABLE | VIEW | STAGE | CONNECTION
      | USER | ROLE | STREAM | FUNCTION | PROCEDURE }
    [ IF EXISTS ] <object_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

## Supported Object Types

| Object Type | Object Name Format | Example |
|-------------|-------------------|---------|
| DATABASE    | `<database>` | `ALTER DATABASE mydb SET TAG env = 'prod'` |
| TABLE       | `[<database>.]<table>` | `ALTER TABLE mydb.users SET TAG env = 'prod'` |
| VIEW        | `[<database>.]<view>` | `ALTER VIEW mydb.active_users SET TAG env = 'prod'` |
| STAGE       | `<stage>` | `ALTER STAGE my_stage SET TAG env = 'prod'` |
| CONNECTION  | `<connection>` | `ALTER CONNECTION my_conn SET TAG env = 'prod'` |
| USER        | `'<user>'` | `ALTER USER 'alice' SET TAG env = 'prod'` |
| ROLE        | `<role>` | `ALTER ROLE analyst SET TAG env = 'prod'` |
| STREAM      | `[<database>.]<stream>` | `ALTER STREAM mydb.my_stream SET TAG env = 'prod'` |
| FUNCTION    | `<function>` | `ALTER FUNCTION my_udf SET TAG env = 'prod'` |
| PROCEDURE   | `<name>(<arg_types>)` | `ALTER PROCEDURE my_proc(INT) SET TAG env = 'prod'` |

> **Notes:**
>
> - If the tag has `ALLOWED_VALUES`, the value must be one of the allowed values.
> - `UNSET TAG` with a non-existent tag name returns an error, unless the object itself does not exist and `IF EXISTS` is specified.
> - For PROCEDURE, you must include the argument type signature in the object name.

## Examples

### Tag a Database and Table

```sql
CREATE TAG env ALLOWED_VALUES = ('dev', 'staging', 'prod');
CREATE TAG owner;

ALTER DATABASE default SET TAG env = 'prod';
ALTER TABLE default.my_table SET TAG env = 'staging', owner = 'team_a';
```

### Tag a Stage and Connection

```sql
ALTER STAGE data_stage SET TAG env = 'dev', owner = 'data_team';
ALTER CONNECTION my_s3 SET TAG env = 'prod';
```

### Tag a View

```sql
ALTER VIEW default.active_users SET TAG env = 'prod', owner = 'analytics';
```

### Tag a User and Role

```sql
ALTER USER 'alice' SET TAG env = 'prod', owner = 'security';
ALTER ROLE analyst SET TAG env = 'dev';
```

### Tag a UDF and Procedure

```sql
ALTER FUNCTION my_udf SET TAG env = 'dev';
ALTER PROCEDURE my_proc(DECIMAL(10,2)) SET TAG env = 'prod';
```

### Remove Tags

```sql
ALTER TABLE default.my_table UNSET TAG env, owner;
ALTER STAGE data_stage UNSET TAG env;
ALTER USER 'alice' UNSET TAG env, owner;
```
