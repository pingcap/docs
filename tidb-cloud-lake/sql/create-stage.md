---
title: CREATE STAGE
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.339"/>

Creates an internal or external stage.

## Syntax

```sql
-- Internal stage
CREATE [ OR REPLACE ] STAGE [ IF NOT EXISTS ] <internal_stage_name>
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC } [ formatTypeOptions ]
       ) ]
  [ COPY_OPTIONS = ( copyOptions ) ]
  [ COMMENT = '<string_literal>' ]

-- External stage
CREATE STAGE [ IF NOT EXISTS ] <external_stage_name>
    externalStageParams
  [ FILE_FORMAT = (
         FORMAT_NAME = '<your-custom-format>'
         | TYPE = { CSV | TSV | NDJSON | PARQUET | ORC } [ formatTypeOptions ]
       ) ]
  [ COPY_OPTIONS = ( copyOptions ) ]
  [ COMMENT = '<string_literal>' ]
```

### externalStageParams

:::tip
For external stages, it is recommended to use the `CONNECTION` parameter to reference pre-configured connection objects instead of inline credentials. This approach provides better security and maintainability.
:::

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

For the connection parameters available for different storage services, see [Connection Parameters](/00-sql-reference/51-connect-parameters.md).

For more information on `CONNECTION_NAME`, see [CREATE CONNECTION](../13-connection/create-connection.md).

### FILE_FORMAT

See [Input & Output File Formats](../../../00-sql-reference/50-file-format-options.md) for details.

### copyOptions

```sql
copyOptions ::=
  [ SIZE_LIMIT = <num> ]
  [ PURGE = <bool> ]
```

| Parameters           | Description                                                                                                                   | Required |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------|----------|
| `SIZE_LIMIT = <num>` | Number (> 0) that specifies the maximum rows of data to be loaded for a given COPY statement. Default `0`                     | Optional |
| `PURGE = <bool>`     | True specifies that the command will purge the files in the stage if they are loaded successfully into table. Default `false` | Optional |


## Access control requirements

| Privilege | Object Type   | Description                                                               |
|:----------|:--------------|:--------------------------------------------------------------------------|
| SUPER     | Global, Table | Operates a stage(Lists stages. Creates, Drops a stage), catalog or share. |

To create a stage, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the SUPER [privilege](/guides/security/access-control/privileges).

## Examples

### Example 1: Create Internal Stage

This example creates an internal stage named *my_internal_stage*:

```sql
CREATE STAGE my_internal_stage;

DESC STAGE my_internal_stage;

name             |stage_type|stage_params                                                  |copy_options                                                                                                                                                  |file_format_options             |number_of_files|creator           |comment|
-----------------+----------+--------------------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------+--------------------------------+---------------+------------------+-------+
my_internal_stage|Internal  |StageParams { storage: Fs(StorageFsConfig { root: "_data" }) }|CopyOptions { on_error: AbortNum(1), size_limit: 0, max_files: 0, split_size: 0, purge: false, single: false, max_file_size: 0, disable_variant_check: false }|Parquet(ParquetFileFormatParams)|              0|'root'@'127.0.0.1'|       |

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
+-------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------+--------------------------------------------------------------------------------------------------------------------+---------+
| name        | stage_type | stage_params                                                                                                                                                           | copy_options                                  | file_format_options                                                                                                | comment |
+-------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------+--------------------------------------------------------------------------------------------------------------------+---------+
| my_s3_stage | External   | StageParams { storage: S3(StageS3Storage { bucket: "load", path: "/files/", credentials_aws_key_id: "", credentials_aws_secret_key: "", encryption_master_key: "" }) } | CopyOptions { on_error: None, size_limit: 0 } | FileFormatOptions { format: Csv, skip_header: 0, field_delimiter: ",", record_delimiter: "\n", compression: None } |         |
+-------------+------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------+--------------------------------------------------------------------------------------------------------------------+---------+
```

### Example 3: Create External Stage with AWS IAM User

This example creates an external stage named *iam_external_stage* on Amazon S3 with an AWS Identity and Access Management (IAM) user.

#### Step 1: Create Access Policy for S3 Bucket

The procedure below creates an access policy named *databend-access* for the bucket *databend-toronto* on Amazon S3:

1. Log into the AWS Management Console, then select **Services** > **Security, Identity, & Compliance** > **IAM**.
2. Select **Account settings** in the left navigation pane, and go to the **Security Token Service (STS)** section on the right page. Make sure the status of AWS region where your account belongs is **Active**.
3. Select **Policies** in the left navigation pane, then select **Create policy** on the right page.
4. Click the **JSON** tab, copy and paste the following code to the editor, then save the policy as *databend_access*.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllObjectActions",
      "Effect": "Allow",
      "Action": [
        "s3:*Object"
      ],
      "Resource": "arn:aws:s3:::databend-toronto/*"
    },
    {
      "Sid": "ListObjectsInBucket",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket"
      ],
      "Resource": "arn:aws:s3:::databend-toronto"
    }
  ]
}
```

#### Step 2: Create IAM User

The procedure below creates an IAM user named *databend* and attach the access policy *databend-access* to the user.

1. Select **Users** in the left navigation pane, then select **Add users** on the right page.
2. Configure the user:
    - Set the user name to *databend*.
    - When setting permissions for the user, click **Attach policies directly**, then search for and select the access policy *databend-access*.
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
  ROLE_ARN = 'arn:aws:iam::123456789012:role/databend-access'
  EXTERNAL_ID = 'my-external-id-123';

-- Create stage using the connection
CREATE STAGE iam_external_stage 
  URL = 's3://databend-toronto' 
  CONNECTION = (CONNECTION_NAME = 'iam_s3_connection');
```

### Example 4: Create External Stage on Cloudflare R2

[Cloudflare R2](https://www.cloudflare.com/en-ca/products/r2/) is an object storage service introduced by Cloudflare that is fully compatible with Amazon's AWS S3 service. This example creates an external stage named *r2_stage* on Cloudflare R2.

#### Step 1: Create Bucket

The procedure below creates a bucket named *databend* on Cloudflare R2.

1. Log into the Cloudflare dashboard, and select **R2** in the left navigation pane.
2. Click **Create bucket** to create a bucket, and set the bucket name to *databend*. Once the bucket is successfully created, you can find the bucket endpoint right below the bucket name when you view the bucket details page.

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
  URL='s3://databend/'
  CONNECTION = (CONNECTION_NAME = 'r2_connection');
```
