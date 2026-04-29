---
title: CREATE DATABASE
summary: Create a database.
---

# CREATE DATABASE

> **Note:**
>
> Introduced or updated in v1.2.866.

Create a database.

## Syntax

```sql
CREATE [ OR REPLACE ] DATABASE [ IF NOT EXISTS ] <database_name>
    [ OPTIONS (
        DEFAULT_STORAGE_CONNECTION = '<connection_name>',
        DEFAULT_STORAGE_PATH = '<path>'
    ) ]
```

## Parameters

| Parameter                    | Description                                                                                                                                      |
|:-----------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|
| `DEFAULT_STORAGE_CONNECTION` | The name of an existing connection (created via `CREATE CONNECTION`) to use as the default storage connection for tables in this database.        |
| `DEFAULT_STORAGE_PATH`       | The default storage path URI (e.g., `s3://bucket/path/`) for tables in this database. Must end with `/` and match the connection's storage type. |

> **Note:**
>
> - `DEFAULT_STORAGE_CONNECTION` and `DEFAULT_STORAGE_PATH` must be specified together. Specifying only one is an error.
> - When both options are set, {{{ .lake }}} validates that the connection exists, the path URI is well-formed, and the storage location is accessible.

## Access control requirements

| Privilege       | Object Type | Description         |
|:----------------|:------------|:--------------------|
| CREATE DATABASE | Global      | Creates a database. |

To create a database, the user performing the operation or the [current_role](/tidb-cloud-lake/guides/roles.md) must have the CREATE DATABASE [privilege](/tidb-cloud-lake/guides/privileges.md).

## Examples

The following example creates a database named `test`:

```sql
CREATE DATABASE test;
```

The following example creates a database with a default storage connection and path:

```sql
CREATE CONNECTION my_s3 STORAGE_TYPE = 's3' ACCESS_KEY_ID = '<key>' SECRET_ACCESS_KEY = '<secret>';

CREATE DATABASE analytics OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics/'
);
```
