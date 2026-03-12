---
title: CREATE CONNECTION
sidebar_position: 1
---
import FunctionDescription from '@site/src/components/FunctionDescription';
import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<FunctionDescription description="Introduced or updated: v1.2.780"/>

Creates a connection to external storage.

:::warning
IMPORTANT: When objects (stages, tables, etc.) use a connection, they copy and store the connection's parameters permanently. If you later modify the connection using CREATE OR REPLACE CONNECTION, existing objects will continue using the old parameters. To update objects with new connection parameters, you must drop and recreate those objects.
:::

## Syntax

```sql
CREATE [ OR REPLACE ] CONNECTION [ IF NOT EXISTS ] <connection_name>
    STORAGE_TYPE = '<type>'
    [ <storage_params> ]
```

| Parameter        | Description                                                                                                                                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| STORAGE_TYPE     | Type of storage service. Possible values include: `s3`, `azblob`, `gcs`, `oss`, and `cos`.                                                         |
| storage_params   | Vary based on storage type and authentication method. See [Connection Parameters](../../../00-sql-reference/51-connect-parameters.md) for the complete list. |

## Connection Parameters

Connections encapsulate the credentials and configuration for a specific storage backend. Choose the appropriate `STORAGE_TYPE` and provide the required parameters when creating the connection. The table highlights common options:

| STORAGE_TYPE | Typical parameters | Description |
|--------------|-------------------|-------------|
| `s3`         | `ACCESS_KEY_ID`/`SECRET_ACCESS_KEY`, or `ROLE_ARN`/`EXTERNAL_ID`, optional `ENDPOINT_URL`, `REGION` | Amazon S3 and S3-compatible services (MinIO, Cloudflare R2, etc.). |
| `azblob`     | `ACCOUNT_NAME`, `ACCOUNT_KEY`, `ENDPOINT_URL` | Azure Blob Storage. |
| `gcs`        | `CREDENTIAL` (base64-encoded service account key) | Google Cloud Storage. |
| `oss`        | `ACCESS_KEY_ID`, `ACCESS_KEY_SECRET`, `ENDPOINT_URL` | Alibaba Cloud Object Storage Service. |
| `cos`        | `SECRET_ID`, `SECRET_KEY`, `ENDPOINT_URL` | Tencent Cloud Object Storage. |
| `hf`         | `REPO_TYPE`, `REVISION`, optional `TOKEN` | Hugging Face Hub datasets and models. |

For parameter meanings, optional flags, and additional storage types, refer to [Connection Parameters](../../../00-sql-reference/51-connect-parameters.md). Expand the tabs below to see storage-specific examples:

<Tabs groupId="connection-storage-types">
<TabItem value="s3" label="Amazon S3">

Choose an authentication method for Amazon S3 and S3-compatible services:

<Tabs groupId="s3-auth-methods">
<TabItem value="access-keys" label="Access Keys">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';
```

| Parameter | Description |
|-----------|-------------|
| ACCESS_KEY_ID | Your AWS access key ID. |
| SECRET_ACCESS_KEY | Your AWS secret access key. |

</TabItem>
<TabItem value="iam-role" label="IAM Role">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 's3'
    ROLE_ARN = '<your-role-arn>';
```

| Parameter | Description |
|-----------|-------------|
| ROLE_ARN  | The Amazon Resource Name (ARN) of the IAM role that Databend will assume to access your S3 resources. |

</TabItem>
</Tabs>

</TabItem>
<TabItem value="azblob" label="Azure Blob">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'azblob'
    ACCOUNT_NAME = '<account-name>'
    ACCOUNT_KEY = '<account-key>'
    ENDPOINT_URL = 'https://<account-name>.blob.core.windows.net';
```

</TabItem>
<TabItem value="gcs" label="Google Cloud Storage">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'gcs'
    CREDENTIAL = '<base64-encoded-service-account>';
```

</TabItem>
<TabItem value="oss" label="Alibaba Cloud OSS">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'oss'
    ACCESS_KEY_ID = '<your-ak>'
    ACCESS_KEY_SECRET = '<your-sk>'
    ENDPOINT_URL = 'https://<bucket-name>.<region-id>[-internal].aliyuncs.com';
```

</TabItem>
<TabItem value="cos" label="Tencent COS">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'cos'
    SECRET_ID = '<your-secret-id>'
    SECRET_KEY = '<your-secret-key>'
    ENDPOINT_URL = '<your-endpoint-url>';
```

</TabItem>
<TabItem value="hf" label="Hugging Face">

```sql
CREATE CONNECTION <connection_name>
    STORAGE_TYPE = 'hf'
    REPO_TYPE = 'dataset'
    REVISION = 'main'
    TOKEN = '<optional-access-token>';
```

Omit `TOKEN` for public repositories; include it for private or rate-limited assets.

</TabItem>
</Tabs>


## Access control requirements

| Privilege         | Object Type | Description           |
|:------------------|:------------|:----------------------|
| CREATE CONNECTION | Global      | Creates a connection. |


To create a connection, the user performing the operation or the [current_role](/guides/security/access-control/roles) must have the CREATE CONNECTION [privilege](/guides/security/access-control/privileges).

## Update Table Connections

To switch an existing table to a new connection, use [`ALTER TABLE ... CONNECTION`](/sql/sql-commands/ddl/table/alter-table#external-table-connection). This command rebinds external tables to a different connection without recreating the table.

## Examples

### Using Access Keys

This example creates a connection to Amazon S3 named 'toronto' and establishes an external stage named 'my_s3_stage' linked to the 's3://databend-toronto' URL, using the 'toronto' connection. For more practical examples about connection, see [Usage Examples](index.md#usage-examples).

```sql
CREATE CONNECTION toronto
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE STAGE my_s3_stage
    URL = 's3://databend-toronto'
    CONNECTION = (CONNECTION_NAME = 'toronto');
```

### Using AWS IAM Role

This example creates a connection to Amazon S3 using an IAM role and then creates a stage that uses this connection. This approach is more secure as it doesn't require storing access keys in Databend.

```sql
CREATE CONNECTION databend_test
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::987654321987:role/databend-test';

CREATE STAGE databend_test
    URL = 's3://test-bucket-123'
    CONNECTION = (CONNECTION_NAME = 'databend_test');

-- You can now query data from your S3 bucket
SELECT * FROM @databend_test/test.parquet LIMIT 1;
```

:::info
To use IAM roles with Databend Cloud, you need to set up a trust relationship between your AWS account and Databend Cloud. See [Authenticate with AWS IAM Role](/guides/cloud/security/iam-role) for detailed instructions.
:::
