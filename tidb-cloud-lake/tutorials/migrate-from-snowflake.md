---
title: Migrate from Snowflake to Databend
sidebar_label: Snowflake → Databend

---

> **Capabilities**: Full Load

This tutorial walks you through the process of migrating your data from Snowflake to Databend. The migration involves exporting data from Snowflake to an Amazon S3 bucket and then loading it into Databend. The process is broken down into three main steps:

![alt text](@site/static/img/load/snowflake-databend.png)

In this tutorial, we'll walk you through the process of exporting data from Snowflake in Parquet format to an Amazon S3 bucket, and then loading it into Databend Cloud.

## Before You Start

Before you start, ensure you have the following prerequisites in place:

- **Amazon S3 Bucket**: An S3 bucket where your exported data will be stored, along with the required permissions for uploading files. [Learn how to create an S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html). In this tutorial, we use `s3://databend-doc/snowflake/` as the location for staging the exported data.
- **AWS Credentials**: AWS Access Key ID and Secret Access Key with sufficient permissions for accessing the S3 bucket. [Manage your AWS credentials](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys).
- **Permissions to Manage IAM Roles and Policie**s: Ensure you have the necessary permissions to create and manage IAM roles and policies, which are required to configure access between Snowflake and Amazon S3. [Learn about IAM roles and policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

## Step 1: Configuring Snowflake Storage Integration for Amazon S3

In this step, we'll configure Snowflake to access Amazon S3 using IAM roles. First, we'll create an IAM role, and then use that role to establish a Snowflake Storage Integration for secure data access.

1. Sign in to the AWS Management Console, then create a policy on **IAM** > **Policies** with the following JSON code: 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
              "s3:PutObject",
              "s3:GetObject",
              "s3:GetObjectVersion",
              "s3:DeleteObject",
              "s3:DeleteObjectVersion"
            ],
            "Resource": "arn:aws:s3:::databend-doc/snowflake/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetBucketLocation"
            ],
            "Resource": "arn:aws:s3:::databend-doc",
            "Condition": {
                "StringLike": {
                    "s3:prefix": [
                        "snowflake/*"
                    ]
                }
            }
        }
    ]
}
```

This policy applies to the S3 bucket named `databend-doc` and specifically to the `snowflake` folder within that bucket.

- `s3:PutObject`, `s3:GetObject`, `s3:GetObjectVersion`, `s3:DeleteObject`, `s3:DeleteObjectVersion`: Allows operations on objects within the snowflake folder (e.g., `s3://databend-doc/snowflake/`). You can upload, read, and delete objects in this folder.
- `s3:ListBucket`, `s3:GetBucketLocation`: Allows listing the contents of the `databend-doc` bucket and retrieving its location. The `Condition` element ensures that listing is restricted to objects within the `snowflake` folder.

2. Create a role named `databend-doc-role` on **IAM** > **Roles** and attach the policy we created.
    - In the first step of creating the role, select **AWS account** for **Trusted entity type**, and **This account (xxxxx)** for **An AWS account**.

    ![alt text](../../../../static/img/documents/tutorials/trusted-entity.png)

    - After the role is created, copy and save the role ARN in a secure location, for example, `arn:aws:iam::123456789012:role/databend-doc-role`.
    - We'll update the **Trust Relationships** for the role later, after we obtain the IAM user ARN for the Snowflake account.


3. Open a SQL worksheet in Snowflake and create a storage integration named `my_s3_integration` using the role ARN. 

```sql
CREATE OR REPLACE STORAGE INTEGRATION my_s3_integration
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::123456789012:role/databend-doc-role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://databend-doc/snowflake/')
  ENABLED = TRUE; 
```

4. Show the storage integration details and obtain the value for the `STORAGE_AWS_IAM_USER_ARN` property in the result, for example, `arn:aws:iam::123456789012:user/example`. We'll use this value to update the **Trust Relationships** for the role `databend-doc-role` in the next step.

```sql
DESCRIBE INTEGRATION my_s3_integration;
```

5. Go back to the AWS Management Console, open the role `databend-doc-role`, and navigate to **Trust relationships** > **Edit trust policy**. Copy the following code into the editor:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::123456789012:user/example"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

    The ARN `arn:aws:iam::123456789012:user/example` is the IAM user ARN for the Snowflake account that we obtained in the previous step.


## Step 2: Preparing and Exporting Data to Amazon S3

1. Create an external stage in Snowflake with the Snowflake storage integration `my_s3_integration`:

```sql
CREATE OR REPLACE STAGE my_external_stage 
    URL = 's3://databend-doc/snowflake/' 
    STORAGE_INTEGRATION = my_s3_integration 
    FILE_FORMAT = (TYPE = 'PARQUET');
```

`URL = 's3://databend-doc/snowflake/'` specifies the S3 bucket and folder where the data will be staged. The path `s3://databend-doc/snowflake/` corresponds to the S3 bucket `databend-doc` and the folder `snowflake` within that bucket.

2. Prepare some data to export.

```sql
CREATE DATABASE doc;
USE DATABASE doc;

CREATE TABLE my_table (
    id INT,
    name STRING,
    age INT
);

INSERT INTO my_table (id, name, age) VALUES
(1, 'Alice', 30),
(2, 'Bob', 25),
(3, 'Charlie', 35);
```

3. Export the table data to the external stage using COPY INTO:

```sql
COPY INTO @my_external_stage/my_table_data_
  FROM my_table
  FILE_FORMAT = (TYPE = 'PARQUET') HEADER=true;
```

If you open the bucket `databend-doc` now, you should see a Parquet file in the `snowflake` folder:

![alt text](../../../../static/img/documents/tutorials/bucket-folder.png)

## Step 3: Loading Data into Databend Cloud

1. Create the target table in Databend Cloud:

```sql
CREATE DATABASE doc;
USE DATABASE doc;

CREATE TABLE my_target_table (
    id INT,
    name STRING,
    age INT
);
```

2. Load the exported data in the bucket using [COPY INTO](/sql/sql-commands/dml/dml-copy-into-table):

```sql
COPY INTO my_target_table
FROM 's3://databend-doc/snowflake'
CONNECTION = (
    ACCESS_KEY_ID = '<your-access-key-id>',
    SECRET_ACCESS_KEY = '<your-secret-access-key>'
)
PATTERN = '.*[.]parquet'
FILE_FORMAT = (
    TYPE = 'PARQUET'
);
```

3. Verify the loaded data:

```sql
SELECT * FROM my_target_table;

┌──────────────────────────────────────────────────────┐
│        id       │       name       │       age       │
├─────────────────┼──────────────────┼─────────────────┤
│               1 │ Alice            │              30 │
│               2 │ Bob              │              25 │
│               3 │ Charlie          │              35 │
└──────────────────────────────────────────────────────┘
```
