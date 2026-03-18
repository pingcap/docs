---
title: ATTACH TABLE
summary: ATTACH TABLE creates a read-only link to existing table data without copying it. This command is ideal for data sharing across environments, especially when migrating from a private Databend deployment to Databend Cloud.
---

> **Note:**
>
> Introduced or updated in v1.2.698.

ATTACH TABLE creates a read-only link to existing table data without copying it. This command is ideal for data sharing across environments, especially when migrating from a private Databend deployment to [Databend Cloud](https://www.databend.com).

## Key Features

- **Zero-Copy Data Access**: Links to source data without physical data movement
- **Real-Time Updates**: Changes in the source table are instantly visible in attached tables
- **Read-Only Mode**: Only supports SELECT queries (no INSERT, UPDATE, or DELETE operations)
- **Column-Level Access**: Optionally include only specific columns for security and performance

## Syntax

```sql
ATTACH TABLE <target_table_name> [ ( <column_list> ) ] '<source_table_data_URI>'
CONNECTION = ( CONNECTION_NAME = '<connection_name>' )
```

### Parameters

- **`<target_table_name>`**: Name of the new attached table to create

- **`<column_list>`**: Optional list of columns to include from the source table
  - When omitted, all columns are included
  - Provides column-level security and access control
  - Example: `(customer_id, product, amount)`

- **`<source_table_data_URI>`**: Path to the source table data in object storage
  - Format: `s3://<bucket-name>/<database_ID>/<table_ID>/`
  - Example: `s3://databend-toronto/1/23351/`

- **`CONNECTION_NAME`**: References a connection created with [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md)

### Finding the Source Table Path

Use the [FUSE_SNAPSHOT](/tidb-cloud-lake/sql/fuse-snapshot.md) function to get the database and table IDs:

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'employees');
-- Result contains: 1/23351/_ss/... → Path is s3://your-bucket/1/23351/
```

## Data Sharing Benefits

### How It Works

```
                Object Storage (S3, MinIO, Azure, etc.)
                         ┌─────────────┐
                         │ Source Data │
                         └──────┬──────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│ Marketing   │         │  Finance    │         │   Sales     │
│ Team View   │         │ Team View   │         │ Team View   │
└─────────────┘         └─────────────┘         └─────────────┘
```

### Key Advantages

| Traditional Approach | Databend ATTACH TABLE |
|---------------------|----------------------|
| Multiple data copies | Single copy shared by all |
| ETL delays, sync issues | Real-time, always current |
| Complex maintenance | Zero maintenance |
| More copies = more security risk | Fine-grained column access |
| Slower due to data movement | Full optimization on original data |

### Security and Performance

- **Column-Level Security**: Teams see only the columns they need
- **Real-Time Updates**: Source changes instantly visible in all attached tables
- **Strong Consistency**: Always see complete data snapshots, never partial updates
- **Full Performance**: Inherit all source table indexes and optimizations

## Examples

### Basic Usage

```sql
-- Step 1: Create a connection to your storage
CREATE CONNECTION my_s3_connection 
    STORAGE_TYPE = 's3' 
    ACCESS_KEY_ID = '<your_aws_key_id>'
    SECRET_ACCESS_KEY = '<your_aws_secret_key>';

-- Step 2: Attach a table with all columns
ATTACH TABLE population_all_columns 's3://databend-doc/1/16/' 
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### Column Selection for Security

```sql
-- Attach only specific columns for data security
ATTACH TABLE population_selected (city, population) 's3://databend-doc/1/16/' 
    CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

### Using IAM Role Authentication

```sql
-- Create a connection using IAM role (more secure than access keys)
CREATE CONNECTION s3_role_connection 
    STORAGE_TYPE = 's3' 
    ROLE_ARN = 'arn:aws:iam::123456789012:role/databend-role';

-- Attach table using the IAM role connection
ATTACH TABLE population_all_columns 's3://databend-doc/1/16/' 
    CONNECTION = (CONNECTION_NAME = 's3_role_connection');
```

### Team-Specific Views

```sql
-- Marketing: Customer behavior analysis
ATTACH TABLE marketing_view (customer_id, product, amount, order_date) 
's3://your-bucket/1/23351/' 
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

-- Finance: Revenue tracking (different columns)
ATTACH TABLE finance_view (order_id, amount, profit, order_date) 
's3://your-bucket/1/23351/' 
CONNECTION = (CONNECTION_NAME = 'my_s3_connection');
```

## Learn More

- [Linking Tables with ATTACH TABLE](/tidb-cloud-lake/tutorials/data-sharing-via-attach-table.md)
