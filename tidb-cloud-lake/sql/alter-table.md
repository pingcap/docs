---
title: ALTER TABLE
sidebar_position: 4
slug: /sql-commands/ddl/table/alter-table
---
 
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.845"/>

import EEFeature from '@site/src/components/EEFeature';

Use `ALTER TABLE` to modify the structure and properties of an existing table, including its columns, comment, storage options, external connection, or even swapping metadata with another table. The subsections below cover each supported capability.

## Column Operations {#column-operations}

<EEFeature featureName='MASKING POLICY'/>

Modify a table by adding, converting, renaming, changing, or removing columns.

### Syntax

```sql
-- Add a column to the end of the table
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
ADD [ COLUMN ] <column_name> <data_type> [ NOT NULL | NULL ] [ DEFAULT <constant_value> ]

-- Add a column to a specified position
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
ADD [ COLUMN ] <column_name> <data_type> [ NOT NULL | NULL ] [ DEFAULT <constant_value> ] [ FIRST | AFTER <column_name> ]

-- Add a virtual computed column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
ADD [ COLUMN ] <column_name> <data_type> AS (<expr>) VIRTUAL

-- Convert a stored computed column to a regular column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
MODIFY [ COLUMN ] <column_name> DROP STORED

-- Rename a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
RENAME [ COLUMN ] <column_name> TO <new_column_name>

-- Change data type
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
MODIFY [ COLUMN ] <column_name> <new_data_type> [ DEFAULT <constant_value> ]
       [ , [ COLUMN ] <column_name> <new_data_type> [ DEFAULT <constant_value> ] ]
       ...

-- Change comment
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> [ COMMENT '<comment>' ]
[ , [ COLUMN ] <column_name> [ COMMENT '<comment>' ] ]
...
    
-- Set / Unset masking policy for a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> SET MASKING POLICY <policy_name>
       [ USING ( <column_reference> [ , <column_reference> ... ] ) ]

ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> UNSET MASKING POLICY

-- Remove a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
DROP [ COLUMN ] <column_name>
```

:::note
- Only a constant value can be accepted as a default value when adding or modifying a column. If a non-constant expression is used, an error will occur.
- Adding a stored computed column with ALTER TABLE is not supported yet.
- When you change the data type of a table's columns, there's a risk of conversion errors. For example, if you try to convert a column with text (String) to numbers (Float), it might cause problems.
- When you set a masking policy for a column, make sure that the data type (refer to the parameter *arg_type_to_mask* in the syntax of [CREATE MASKING POLICY](../12-mask-policy/create-mask-policy.md)) defined in the policy matches the column.
- Use the optional `USING` clause when the policy definition expects additional parameters. List the column mapped to each policy argument in order; the first argument always represents the column being masked.
- If you include `USING`, provide at least the masked column plus any additional columns needed by the policy. The first identifier in `USING (...)` must match the column being modified.
- Masking policies can only be attached to regular tables. Views, streams, and temporary tables do not allow `SET MASKING POLICY`.
- A column can belong to at most one security policy (masking or row-level). Remove the existing policy before attaching a new one.
- Attaching, detaching, describing, or dropping a masking policy requires the global `APPLY MASKING POLICY` privilege or APPLY/OWNERSHIP on the specific masking policy.
- Adding, removing, describing, or dropping a row access policy requires the global `APPLY ROW ACCESS POLICY` privilege or APPLY/OWNERSHIP on that policy.
:::

:::caution
You must `ALTER TABLE ... MODIFY COLUMN <col> UNSET MASKING POLICY` before changing the column definition or dropping the column; otherwise the statement fails because the column is still protected by a security policy.
:::

### Examples

#### Example 1: Adding, Renaming, and Removing a Column

This example illustrates the creation of a table called "default.users" with columns 'username', 'email', and 'age'. It showcases the addition of columns 'id' and 'middle_name' with various constraints. The example also demonstrates the renaming and subsequent removal of the "age" column.

```sql
-- Create a table
CREATE TABLE default.users (
  username VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  age INT
);

-- Add a column to the end of the table
ALTER TABLE default.users
ADD COLUMN business_email VARCHAR(255) NOT NULL DEFAULT 'example@example.com';

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
username      |VARCHAR|NO  |''                   |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Add a column to the beginning of the table
ALTER TABLE default.users
ADD COLUMN id int NOT NULL FIRST;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Add a column after the column 'username'
ALTER TABLE default.users
ADD COLUMN middle_name VARCHAR(50) NULL AFTER username;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Rename a column
ALTER TABLE default.users
RENAME COLUMN age TO new_age;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
new_age       |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Remove a column
ALTER TABLE default.users
DROP COLUMN new_age;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
```

#### Example 2: Modify Columns and Masking Policies

```sql
-- Change column types and defaults
ALTER TABLE users
MODIFY COLUMN age BIGINT DEFAULT 18,
       COLUMN email VARCHAR(320) DEFAULT '';

-- Add masking policy that expects extra arguments
ALTER TABLE users
MODIFY COLUMN email SET MASKING POLICY pii_email USING (email, username);

-- To drop or alter the column, remove the policy first
ALTER TABLE users
MODIFY COLUMN email UNSET MASKING POLICY;
```

## Table Comment {#table-comment}

Modifies the comment of a table. If the table does not have a comment yet, this command adds the specified comment to the table.

### Syntax

```sql
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name> 
COMMENT = '<comment>'
```

### Examples

```sql
-- Create a table with a comment
CREATE TABLE t(id INT) COMMENT ='original-comment';

SHOW CREATE TABLE t;

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  Table │                                 Create Table                                │
├────────┼─────────────────────────────────────────────────────────────────────────────┤
│ t      │ CREATE TABLE t (\n  id INT NULL\n) ENGINE=FUSE COMMENT = 'original-comment' │
└──────────────────────────────────────────────────────────────────────────────────────┘

-- Modify the comment
ALTER TABLE t COMMENT = 'new-comment';

SHOW CREATE TABLE t;

┌─────────────────────────────────────────────────────────────────────────────────┐
│  Table │                              Create Table                              │
├────────┼────────────────────────────────────────────────────────────────────────┤
│ t      │ CREATE TABLE t (\n  id INT NULL\n) ENGINE=FUSE COMMENT = 'new-comment' │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- Create a table without comment
CREATE TABLE t(id INT);

-- Add a comment later
ALTER TABLE t COMMENT = 'new-comment';
```

## Fuse Engine Options {#fuse-engine-options}

Sets or unsets [Fuse Engine options](../../../00-sql-reference/30-table-engines/00-fuse.md#fuse-engine-options) for a table.

### Syntax

```sql
-- Set Fuse Engine options
ALTER TABLE [ <database_name>. ]<table_name> SET OPTIONS (<options>)

-- Unset Fuse Engine options, reverting them to their default values
ALTER TABLE [ <database_name>. ]<table_name> UNSET OPTIONS (<options>)
```

Only the following Fuse Engine options can be unset:

- `block_per_segment`
- `block_size_threshold`
- `data_retention_period_in_hours`
- `data_retention_num_snapshots_to_keep`
- `row_avg_depth_threshold`
- `row_per_block`
- `row_per_page`

### Examples

```sql
CREATE TABLE fuse_table (a int);

SET hide_options_in_show_create_table=0;

-- Show current options
SHOW CREATE TABLE fuse_table;

-- Change Fuse options
ALTER TABLE fuse_table SET OPTIONS (block_per_segment = 500, data_retention_period_in_hours = 240);

-- Show updated options
SHOW CREATE TABLE fuse_table;
```

```sql
-- Limit snapshots and enable auto vacuum
CREATE OR REPLACE TABLE t(c INT);
ALTER TABLE t SET OPTIONS(data_retention_num_snapshots_to_keep = 1);
SET enable_auto_vacuum = 1;
INSERT INTO t VALUES(1);
INSERT INTO t VALUES(2);
INSERT INTO t VALUES(3);

-- Revert options to defaults
ALTER TABLE fuse_table UNSET OPTIONS (block_per_segment, data_retention_period_in_hours);
```

## External Table Connection {#external-table-connection}

Updates the connection settings for an external table. Only credential-related fields (`access_key_id`, `secret_access_key`, `role_arn`) are applied when the command runs. Other properties such as `bucket`, `region`, or `root` remain unchanged.

### Syntax

```sql
ALTER TABLE [ <database_name>. ]<table_name> CONNECTION = ( connection_name = '<connection_name>' )
```

| Parameter | Description | Required |
|-----------|-------------|----------|
| connection_name | Name of the connection to be used for the external table. The connection must already exist in the system. | Yes |

This command is particularly useful when credentials need to be rotated or when IAM roles change. The specified connection must already exist before it can be used with this command.

**Security best practices**

When working with external tables, AWS IAM roles provide significant security advantages over access keys:

- No stored credentials: Eliminates the need to store access keys in your configuration
- Automatic rotation: Handles credential rotation automatically
- Fine-grained control: Allows for more precise access control

To use IAM roles with Databend Cloud, see [Authenticate with AWS IAM Role](/guides/cloud/security/iam-role).

### Examples

```sql
-- Create connections
CREATE CONNECTION external_table_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE CONNECTION external_table_conn_new
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-new-access-key-id>'
    SECRET_ACCESS_KEY = '<your-new-secret-access-key>';

-- Create an external table using the first connection
CREATE OR REPLACE TABLE external_table_test (
    id INT,
    name VARCHAR,
    age INT
)
's3://testbucket/13_fuse_external_table/'
CONNECTION=(connection_name = 'external_table_conn');

-- Update to use the new connection
ALTER TABLE external_table_test CONNECTION=( connection_name = 'external_table_conn_new' );
```

```sql
-- Migrate to IAM role authentication
CREATE CONNECTION s3_access_key_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE TABLE sales_data (
    order_id INT,
    product_name VARCHAR,
    quantity INT
)
's3://sales-bucket/data/'
CONNECTION=(connection_name = 's3_access_key_conn');

CREATE CONNECTION s3_role_conn
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::123456789012:role/databend-access';

ALTER TABLE sales_data CONNECTION=( connection_name = 's3_role_conn' );
```

## Swap Tables {#swap-tables}

Swaps all table metadata and data between two tables atomically in a single transaction. This operation exchanges the table schemas, including all columns, constraints, and data, effectively making each table take on the identity of the other.

### Syntax

```sql
ALTER TABLE [ IF EXISTS ] <source_table_name> SWAP WITH <target_table_name>
```

| Parameter            | Description                                    |
|----------------------|------------------------------------------------|
| `source_table_name`  | The name of the first table to swap            |
| `target_table_name`  | The name of the second table to swap with      |

### Usage Notes

- Only available for Fuse Engine tables. External tables, system tables, and other non-Fuse tables are not supported.
- Temporary tables cannot be swapped with permanent or transient tables.
- The current role must be the owner of both tables to perform the swap operation.
- Both tables must be in the same database. Cross-database swapping is not supported.
- The swap operation is atomic. Either both tables are swapped successfully, or neither is changed.
- All data and metadata are preserved during the swap. No data is lost or modified.

### Examples

```sql
-- Create two tables with different schemas
CREATE OR REPLACE TABLE t1(a1 INT, a2 VARCHAR, a3 DATE);
CREATE OR REPLACE TABLE t2(b1 VARCHAR);

-- Check table schemas before swap
DESC t1;
DESC t2;

-- Swap the tables
ALTER TABLE t1 SWAP WITH t2;

-- After swapping, t1 now has t2's schema, and t2 has t1's schema
DESC t1;
DESC t2;
```
