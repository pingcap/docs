---
title: "Databend Cloud: Data Sharing via ATTACH TABLE"
sidebar_label: "Data Sharing"
---

In this tutorial, we'll walk you through how to link a table in Databend Cloud with an existing Databend table stored in an S3 bucket using the [ATTACH TABLE](/sql/sql-commands/ddl/table/attach-table) command.

## Before You Start

Before you start, ensure you have the following prerequisites in place:

- [Docker](https://www.docker.com/) is installed on your local machine, as it will be used to launch a self-hosted Databend.
- An AWS S3 bucket used as storage for your self-hosted Databend. [Learn how to create an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).
- AWS Access Key ID and Secret Access Key with sufficient permissions for accessing your S3 bucket. [Manage your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).
- BendSQL is installed on your local machine. See [Installing BendSQL](/guides/connect/sql-clients/bendsql/#installing-bendsql) for instructions on how to install BendSQL using various package managers.

## Step 1: Launch Databend in Docker

1. Start a Databend container on your local machine. The command below launches a Databend container with S3 as the storage backend, using the `databend-doc` bucket, along with the specified S3 endpoint and authentication credentials.

```bash
docker run \
    -p 8000:8000 \
    -e QUERY_STORAGE_TYPE=s3 \
    -e AWS_S3_ENDPOINT="https://s3.us-east-2.amazonaws.com" \
    -e AWS_S3_BUCKET=databend-doc\
    -e AWS_ACCESS_KEY_ID=<your-aws-access-key-id> \ 
    -e AWS_SECRET_ACCESS_KEY=<your-aws-secrect-access-key> \ 
    datafuselabs/databend:v1.2.699-nightly
```

2. Create a table named `population` to store city, province, and population data, and insert sample records as follows:

```sql
CREATE TABLE population (
  city VARCHAR(50),
  province VARCHAR(50),  
  population INT
);

INSERT INTO population (city, province, population) VALUES
  ('Toronto', 'Ontario', 2731571),
  ('Montreal', 'Quebec', 1704694),
  ('Vancouver', 'British Columbia', 631486);
```

3. Run the following statement to retrieve the table's location in S3. As indicated in the result below, the S3 URI for the table is `s3://databend-doc/1/16/` for this tutorial.

```sql
SELECT snapshot_location FROM FUSE_SNAPSHOT('default', 'population');

┌──────────────────────────────────────────────────┐
│                 snapshot_location                │
├──────────────────────────────────────────────────┤
│ 1/16/_ss/513c5100aa0243fe863b4cc2df0e3046_v4.mpk │
└──────────────────────────────────────────────────┘
```

## Step 2: Set Up Attached Tables in Databend Cloud

1. Connect to Databend Cloud using BendSQL. If you're unfamiliar with BendSQL, refer to this tutorial: [Connecting to Databend Cloud using BendSQL](../getting-started/connect-to-databendcloud-bendsql.md).

2. Execute the following statements to create two attached tables:
    - The first table, `population_all_columns`, includes all columns from the source data.
    - The second table, `population_only`, includes only the selected columns (`city` & `population`).

```sql
-- Create an attached table with all columns from the source
ATTACH TABLE population_all_columns 's3://databend-doc/1/16/' CONNECTION = (
  ACCESS_KEY_ID = '<your_aws_key_id>',
  SECRET_ACCESS_KEY = '<your_aws_secret_key>'
);

-- Create an attached table with selected columns (city & population) from the source
ATTACH TABLE population_only (city, population) 's3://databend-doc/1/16/' CONNECTION = (
  ACCESS_KEY_ID = '<your_aws_key_id>',
  SECRET_ACCESS_KEY = '<your_aws_secret_key>'
);
```

## Step 3: Verify Attached Tables

1. Query the two attached tables to verify their contents:

```sql
SELECT * FROM population_all_columns;

┌───────────────────────────────────────────────────────┐
│       city       │     province     │    population   │
├──────────────────┼──────────────────┼─────────────────┤
│ Toronto          │ Ontario          │         2731571 │
│ Montreal         │ Quebec           │         1704694 │
│ Vancouver        │ British Columbia │          631486 │
└───────────────────────────────────────────────────────┘

SELECT * FROM population_only;

┌────────────────────────────────────┐
│       city       │    population   │
├──────────────────┼─────────────────┤
│ Toronto          │         2731571 │
│ Montreal         │         1704694 │
│ Vancouver        │          631486 │
└────────────────────────────────────┘
```

2. If you update the source table in Databend, you can observe the same changes reflected in the attached table on Databend Cloud. For example, if you change the population of Toronto to 2,371,571 in the source table:

```sql
UPDATE population
SET population = 2371571
WHERE city = 'Toronto';
```

After executing the update, you can query both attached tables to verify that the changes are reflected:

```sql
-- Check the updated population in the attached table with all columns  
SELECT population FROM population_all_columns WHERE city = 'Toronto';

-- Check the updated population in the attached table with only the population column  
SELECT population FROM population_only WHERE city = 'Toronto';
```

Expected output for both queries above:

```sql
┌─────────────────┐
│    population   │
├─────────────────┤
│         2371571 │
└─────────────────┘
```

3. If you drop the `province` column from the source table, it will no longer be available in the attached table for queries.

```sql
ALTER TABLE population DROP province;
```

After dropping the column, any queries referencing it will result in an error. However, the remaining columns can still be queried successfully.

For example, attempting to query the dropped `province` column will fail:

```sql
SELECT province FROM population_all_columns;
error: APIError: QueryFailed: [1065]error:
  --> SQL:1:8
  |
1 | SELECT province FROM population_all_columns
  |        ^^^^^^^^ column province doesn't exist
```

However, you can still retrieve the `city` and `population` columns:

```sql
SELECT city, population FROM population_all_columns;

┌────────────────────────────────────┐
│       city       │    population   │
├──────────────────┼─────────────────┤
│ Toronto          │         2371571 │
│ Montreal         │         1704694 │
│ Vancouver        │          631486 │
└────────────────────────────────────┘
```
