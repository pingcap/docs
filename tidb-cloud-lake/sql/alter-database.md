---
title: ALTER DATABASE
summary: Changes the name of a database, or sets default storage options for a database.
---

# ALTER DATABASE

> **Note:**
>
> Introduced or updated in v1.2.866.

Changes the name of a database, or sets default storage options for a database.

## Syntax

```sql
-- Rename a database
ALTER DATABASE [ IF EXISTS ] <name> RENAME TO <new_db_name>

-- Set default storage options
ALTER DATABASE [ IF EXISTS ] <name> SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = '<connection_name>'
  | DEFAULT_STORAGE_PATH = '<path>'
)
```

## Parameters

| Parameter                    | Description                                                                                                                                      |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | The name of an existing connection (created via `CREATE CONNECTION`) to use as the default storage connection for tables in this database.        |
| `DEFAULT_STORAGE_PATH`       | The default storage path URI (e.g., `s3://bucket/path/`) for tables in this database. Must end with `/` and match the connection's storage type. |

> **Note:**
>
> - `SET OPTIONS` only affects tables created after the statement is executed. Existing tables are not changed.
> - You can update one option at a time, as long as the other option already exists on the database.

## Examples

### Rename a database

```sql
CREATE DATABASE LAKE;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| LAKE           |
| information_schema |
| default            |
| system             |
+--------------------+
```

```sql
ALTER DATABASE `LAKE` RENAME TO `NEW_LAKE`;
```

```sql
SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| NEW_LAKE       |
| default            |
| system             |
+--------------------+
```

### Set default storage options

```sql
ALTER DATABASE analytics SET OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics_v2/'
);
```

## Tag Operations

Assigns or removes tags on a database. Tags must be created with [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) first. For full details, see [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md).

### Syntax

```sql
ALTER DATABASE [ IF EXISTS ] <name> SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER DATABASE [ IF EXISTS ] <name> UNSET TAG <tag_name> [, <tag_name> ...]
```

### Examples

```sql
ALTER DATABASE mydb SET TAG env = 'prod', owner = 'team_a';
ALTER DATABASE mydb UNSET TAG env, owner;
```
