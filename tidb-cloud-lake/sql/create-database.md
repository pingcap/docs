---
title: CREATE DATABASE
summary: Create a database.
---

# CREATE DATABASE

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

### Creating a Basic Database

The following example creates a database named `test`:

```sql
CREATE DATABASE test;
```

### Creating a Database with a Default Storage Connection

The following example creates a connection using an AWS IAM role and then creates a database that uses this connection as its default storage. Using an IAM role is more secure than access keys because it doesn't require storing credentials in {{{ .lake }}}.

```sql
CREATE CONNECTION my_s3
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/lake-test';

CREATE DATABASE analytics OPTIONS (
    DEFAULT_STORAGE_CONNECTION = 'my_s3',
    DEFAULT_STORAGE_PATH = 's3://mybucket/analytics/'
);
```

> **Note:**
>
> To use IAM roles with {{{ .lake }}}, you need to set up a trust relationship between your AWS account and {{{ .lake }}}. See [Authenticate with AWS IAM Role](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) for detailed instructions.
