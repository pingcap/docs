---
title: CREATE STAGE
summary: Creates an internal or external stage.
---

# CREATE STAGE

Creates an internal or external stage.

## Syntax

```sql
-- Internal stage
CREATE [ OR REPLACE ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]

-- External stage
CREATE STAGE [ IF NOT EXISTS ] <external_stage_name>
    externalStageParams
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC | AVRO | LANCE } [ formatTypeOptions ]
       ) ]
  [ COMMENT = '<string_literal>' ]
```

### externalStageParams

> **Tip:**
>
> For external stages, it is recommended to use the `CONNECTION` parameter to reference pre-configured connection objects instead of inline credentials. This approach provides better security and maintainability.

```sql
externalStageParams ::=
  '<protocol>://<location>'
  CONNECTION = (
        <connection_parameters>
  )
|
  CONNECTION = (
        CONNECTION_NAME = '<your-connection-name>'
  );
```

For the connection parameters available for different storage services, see [Connection Parameters](/tidb-cloud-lake/sql/connection-parameters.md).

For more information on `CONNECTION_NAME`, see [CREATE CONNECTION](/tidb-cloud-lake/sql/create-connection.md).

### FILE_FORMAT

See [Input & Output File Formats](/tidb-cloud-lake/sql/input-output-file-formats.md) for details.

## Access control requirements

| Privilege | Object Type   | Description                                                               |
|:----------|:--------------|:--------------------------------------------------------------------------|
| SUPER     | Global, Table | Operates a stage(Lists stages. Creates, Drops a stage), catalog or share. |

To create a stage, the user performing the operation or the [current_role](/tidb-cloud-lake/guides/roles.md) must have the SUPER [privilege](/tidb-cloud-lake/guides/privileges.md).

## Examples

### Example 1: Create Internal Stage

This example creates an internal stage named *my_internal_stage*:

```sql
CREATE STAGE my_internal_stage;

DESC STAGE my_internal_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│       name        │ stage_type │ storage_type │ url  │ endpoint │ has_credentials │ has_encryption_key │ storage_params │ file_format_options │  creator │         created_on         │ comment │     owner     │
├───────────────────┼────────────┼──────────────┼──────┼──────────┼─────────────────┼────────────────────┼────────────────┼─────────────────────┼──────────┼────────────────────────────┼─────────┼───────────────┤
│ my_internal_stage │ Internal   │ NULL         │ NULL │ NULL     │ false           │ false              │ NULL           │ {"compression":...} │ root@%   │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example 2: Create External Stage with Connection

This example creates an external stage named *my_s3_stage* on Amazon S3 using a connection:

```sql
-- First create a connection
CREATE CONNECTION my_s3_connection
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE my_s3_stage
  URL='s3://load/files/'
  CONNECTION = (CONNECTION_NAME = 'my_s3_connection');

DESC STAGE my_s3_stage;

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│    name     │ stage_type │ storage_type │       url        │ endpoint │ has_credentials │ has_encryption_key │   storage_params      │ file_format_options │ creator │         created_on         │ comment │     owner     │
├─────────────┼────────────┼──────────────┼──────────────────┼──────────┼─────────────────┼────────────────────┼───────────────────────┼─────────────────────┼─────────┼────────────────────────────┼─────────┼───────────────┤
│ my_s3_stage │ External   │ s3           │ s3://load/files/ │ NULL     │ true            │ false              │ {"bucket":"load",...} │ {"compression":...} │ root@%  │ 2026-06-16 22:21:19.000000 │         │ account_admin │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Example 3: Create External Stage with AWS IAM User

This example creates an external stage named *iam_external_stage* on Amazon S3 with an AWS Identity and Access Management (IAM) user.

#### Step 1: Create Access Policy for S3 Bucket

The procedure below creates an access policy named *lake-access* for the bucket *lake-toronto* on Amazon S3:

1. Log into the AWS Management Console, then select **Services** > **Security, Identity, & Compliance** > **IAM**.
2. Select **Account settings** in the left navigation pane, and go to the **Security Token Service (STS)** section on the right page. Make sure the status of AWS region where your account belongs is **Active**.
3. Select **Policies** in the left navigation pane, then select **Create policy** on the right page.
4. Click the **JSON** tab, copy and paste the following code to the editor, then save the policy as *lake_access*.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllObjectActions",
      "Effect": "Allow",
      "Action": ["s3:*Object"],
      "Resource": "arn:aws:s3:::lake-toronto/*"
    },
    {
      "Sid": "ListObjectsInBucket",
      "Effect": "Allow",
      "Action": ["s3:ListBucket"],
      "Resource": "arn:aws:s3:::lake-toronto"
    }
  ]
}
```

#### Step 2: Create IAM User

The procedure below creates an IAM user named *lake* and attaches the access policy *lake-access* to the user.

1. Select **Users** in the left navigation pane, then select **Add users** on the right page.
2. Configure the user:
    - Set the user name to *lake*.
    - When setting permissions for the user, click **Attach policies directly**, then search for and select the access policy *lake-access*.
3. After the user is created, click the user name to open the details page and select the **Security credentials** tab.
4. In the **Access keys** section, click **Create access key**.
5. Select **Third-party service** for the use case, and tick the checkbox below to confirm creation of the access key.
6. Copy and save the generated access key and secret access key to a safe place.

#### Step 3: Create External Stage

Use the IAM role to create an external stage with better security.

```sql
-- First create a connection using IAM role
CREATE CONNECTION iam_s3_connection
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-access'
  EXTERNAL_ID = 'my-external-id-123';

-- Create stage using the connection
CREATE STAGE iam_external_stage
  URL = 's3://lake-toronto'
  CONNECTION = (CONNECTION_NAME = 'iam_s3_connection');
```

### Example 4: Create External Stage on Cloudflare R2

[Cloudflare R2](https://www.cloudflare.com/en-ca/products/r2/) is an object storage service introduced by Cloudflare that is fully compatible with Amazon's AWS S3 service. This example creates an external stage named *r2_stage* on Cloudflare R2.

#### Step 1: Create Bucket

The procedure below creates a bucket named *lake* on Cloudflare R2.

1. Log into the Cloudflare dashboard, and select **R2** in the left navigation pane.
2. Click **Create bucket** to create a bucket, and set the bucket name to *lake*. Once the bucket is successfully created, you can find the bucket endpoint right below the bucket name when you view the bucket details page.

#### Step 2: Create R2 API Token

The procedure below creates an R2 API token that includes an Access Key ID and a Secret Access Key.

1. Click **Manage R2 API Tokens** on **R2** > **Overview**.
2. Click **Create API token** to create an API token.
3. When configuring the API token, select the necessary permission and set the **TTL** as needed.
4. Click **Create API Token** to obtain the Access Key ID and Secret Access Key. Copy and save them to a safe place.

#### Step 3: Create External Stage

Use the created Access Key ID and Secret Access Key to create an external stage named *r2_stage*.

```sql
-- First create a connection
CREATE CONNECTION r2_connection
  STORAGE_TYPE = 's3'
  REGION = 'auto'
  ENDPOINT_URL = '<your-bucket-endpoint>'
  ACCESS_KEY_ID = '<your-access-key-id>'
  SECRET_ACCESS_KEY = '<your-secret-access-key>';

-- Create stage using the connection
CREATE STAGE r2_stage
  URL='s3://lake/'
  CONNECTION = (CONNECTION_NAME = 'r2_connection');
```
