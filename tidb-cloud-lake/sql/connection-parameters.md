---
title: Connection Parameters
---
import FunctionDescription from '@site/src/components/FunctionDescription';

<FunctionDescription description="Introduced or updated: v1.2.294"/>

Connection parameters are key-value pairs you supply when creating reusable connections with `CREATE CONNECTION`. After a connection is created, reference it from stages, COPY commands, and other SQL features by using `CONNECTION = (CONNECTION_NAME = '<connection-name>')`. For full syntax and usage, see [CREATE CONNECTION](../10-sql-commands/00-ddl/13-connection/create-connection.md).

For storage-specific connection details, see the tables below.

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs groupId="operating-systems">
<TabItem value="Amazon S3" label="Amazon S3">

The following table lists connection parameters for accessing an Amazon S3-like storage service:

| Parameter                 	| Required? 	| Description                                                  	|
|---------------------------	|-----------	|--------------------------------------------------------------	|
| endpoint_url              	| Yes       	| Endpoint URL for Amazon S3-like storage service.             	|
| access_key_id             	| Yes       	| Access key ID for identifying the requester.                 	|
| secret_access_key         	| Yes       	| Secret access key for authentication.                        	|
| enable_virtual_host_style 	| No        	| Whether to use virtual host-style URLs. Defaults to *false*. 	|
| master_key                	| No        	| Optional master key for advanced data encryption.            	|
| region                    	| No        	| AWS region where the bucket is located.                      	|
| security_token            	| No        	| Security token for temporary credentials.                    	|

:::note
- If the **endpoint_url** parameter is not specified in the command, Databend will create the stage on Amazon S3 by default. Therefore, when you create an external stage on an S3-compatible object storage or other object storage solutions, be sure to include the **endpoint_url** parameter.

- The **region** parameter is not required because Databend can automatically detect the region information. You typically don't need to manually specify a value for this parameter. In case automatic detection fails, Databend will default to using 'us-east-1' as the region. When deploying Databend with MinIO and not configuring the region information, it will automatically default to using 'us-east-1', and this will work correctly. However, if you receive error messages such as "region is missing" or "The bucket you are trying to access requires a specific endpoint. Please direct all future requests to this particular endpoint", you need to determine your region name and explicitly assign it to the **region** parameter.
:::

```sql title='Examples'
-- Create a reusable connection for Amazon S3
CREATE CONNECTION my_s3_conn
  STORAGE_TYPE = 's3'
  ACCESS_KEY_ID = '<your-ak>'
  SECRET_ACCESS_KEY = '<your-sk>';

-- Use the connection when creating a stage
CREATE STAGE my_s3_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_s3_conn');
  
-- Create a reusable connection for an S3-compatible service such as MinIO
CREATE CONNECTION my_minio_conn
  STORAGE_TYPE = 's3'
  ENDPOINT_URL = 'http://localhost:9000'
  ACCESS_KEY_ID = 'ROOTUSER'
  SECRET_ACCESS_KEY = 'CHANGEME123';

CREATE STAGE my_minio_stage
  URL = 's3://databend'
  CONNECTION = (CONNECTION_NAME = 'my_minio_conn');
```


To access your Amazon S3 buckets, you can also specify an AWS IAM role and external ID for authentication. By specifying an AWS IAM role and external ID, you can provide more granular control over which S3 buckets a user can access. This means that if the IAM role has been granted permissions to access only specific S3 buckets, then the user will only be able to access those buckets. An external ID can further enhance security by providing an additional layer of verification. For more information, see https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html

The following table lists connection parameters for accessing Amazon S3 storage service using AWS IAM role authentication:

| Parameter    	| Required? 	| Description                                           	|
|--------------	|-----------	|-------------------------------------------------------	|
| endpoint_url 	| No        	| Endpoint URL for Amazon S3.                           	|
| role_arn     	| Yes       	| ARN of the AWS IAM role for authorization to S3.      	|
| external_id  	| No        	| External ID for enhanced security in role assumption. 	|

```sql title='Examples'
-- Create the connection using IAM role authentication
CREATE CONNECTION my_iam_conn
  STORAGE_TYPE = 's3'
  ROLE_ARN = 'arn:aws:iam::123456789012:role/my-role'
  EXTERNAL_ID = 'my-external-id';

-- Reference the connection when creating a stage
CREATE STAGE my_iam_stage
  URL = 's3://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_iam_conn');
```

</TabItem>

<TabItem value="Azure Blob" label="Azure Blob">

The following table lists connection parameters for accessing Azure Blob Storage:

| Parameter    	 | Required? 	 | Description                                         	 |
|----------------|-------------|-------------------------------------------------------|
| endpoint_url 	 | Yes       	 | Endpoint URL for Azure Blob Storage.                	 |
| account_key  	 | Yes       	 | Azure Blob Storage account key for authentication.  	 |
| account_name 	 | Yes       	 | Azure Blob Storage account name for identification. 	 |

```sql title='Examples'
-- Create a connection for Azure Blob Storage
CREATE CONNECTION my_azure_conn
  STORAGE_TYPE = 'azblob'
  ACCOUNT_NAME = 'myaccount'
  ACCOUNT_KEY = 'myaccountkey'
  ENDPOINT_URL = 'https://<your-storage-account-name>.blob.core.windows.net';

-- Create a stage that uses the connection
CREATE STAGE my_azure_stage
  URL = 'azblob://my-container'
  CONNECTION = (CONNECTION_NAME = 'my_azure_conn');
```

</TabItem>

<TabItem value="Google GCS" label="Google GCS">

The following table lists connection parameters for accessing Google Cloud Storage:

| Parameter    	 | Required? 	 | Description                                         	 |
|----------------|-------------|-------------------------------------------------------|
| credential   	 | Yes       	 | Google Cloud Storage credential for authentication. 	 |

To get the `credential`, you could follow the topic [Create a service account key](https://cloud.google.com/iam/docs/keys-create-delete#creating)
from the Google documentation to create and download a service account key file. After downloading the service account key file, you could
convert it into a base64 string via the following command:

```
base64 -i -o ~/Desktop/base64-encoded-key.txt
```

```sql title='Examples'
-- Create the connection with the base64-encoded credential
CREATE CONNECTION my_gcs_conn
  STORAGE_TYPE = 'gcs'
  CREDENTIAL = '<your-base64-encoded-credential>';

-- Use the connection when creating a stage
CREATE STAGE my_gcs_stage
  URL = 'gcs://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_gcs_conn');
```

</TabItem>

<TabItem value="Alibaba OSS" label="Alibaba Cloud OSS">

The following table lists connection parameters for accessing Alibaba Cloud OSS:

| Parameter            	| Required? 	| Description                                             	|
|----------------------	|-----------	|---------------------------------------------------------	|
| access_key_id        	| Yes       	| Alibaba Cloud OSS access key ID for authentication.     	|
| access_key_secret    	| Yes       	| Alibaba Cloud OSS access key secret for authentication. 	|
| endpoint_url         	| Yes       	| Endpoint URL for Alibaba Cloud OSS.                     	|
| presign_endpoint_url 	| No        	| Endpoint URL for presigning Alibaba Cloud OSS URLs.     	|

```sql title='Examples'
-- Create a connection for Alibaba Cloud OSS
CREATE CONNECTION my_oss_conn
  STORAGE_TYPE = 'oss'
  ACCESS_KEY_ID = '<your-ak>'
  ACCESS_KEY_SECRET = '<your-sk>'
  ENDPOINT_URL = 'https://<bucket-name>.<region-id>[-internal].aliyuncs.com';

-- Create a stage using the connection
CREATE STAGE my_oss_stage
  URL = 'oss://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_oss_conn');
```

</TabItem>

<TabItem value="Tencent COS" label="Tencent COS">

The following table lists connection parameters for accessing Tencent Cloud Object Storage (COS):

| Parameter    	| Required? 	| Description                                                 	|
|--------------	|-----------	|-------------------------------------------------------------	|
| endpoint_url 	| Yes       	| Endpoint URL for Tencent Cloud Object Storage.              	|
| secret_id    	| Yes       	| Tencent Cloud Object Storage secret ID for authentication.  	|
| secret_key   	| Yes       	| Tencent Cloud Object Storage secret key for authentication. 	|

```sql title='Examples'
-- Create a connection for Tencent COS
CREATE CONNECTION my_cos_conn
  STORAGE_TYPE = 'cos'
  SECRET_ID = '<your-secret-id>'
  SECRET_KEY = '<your-secret-key>'
  ENDPOINT_URL = '<your-endpoint-url>';

-- Create a stage that uses the connection
CREATE STAGE my_cos_stage
  URL = 'cos://my-bucket'
  CONNECTION = (CONNECTION_NAME = 'my_cos_conn');
```

</TabItem>

<TabItem value="Hugging Face" label="HuggingFace">

The following table lists connection parameters for accessing Hugging Face:

| Parameter | Required?             | Description                                                                                                     |
|-----------|-----------------------|-----------------------------------------------------------------------------------------------------------------|
| repo_type | No (default: dataset) | The type of the Hugging Face repository. Can be `dataset` or `model`.                                           |
| revision  | No (default: main)    | The revision for the Hugging Face URI. Could be a branch, tag, or commit of the repository.                     |
| token     | No                    | The API token from Hugging Face, which may be required for accessing private repositories or certain resources. |

```sql title='Examples'
-- Create a connection for Hugging Face
CREATE CONNECTION my_hf_conn
  STORAGE_TYPE = 'hf'
  REPO_TYPE = 'dataset'
  REVISION = 'main';

-- Create a stage that uses the connection
CREATE STAGE my_huggingface_stage
  URL = 'hf://opendal/huggingface-testdata/'
  CONNECTION = (CONNECTION_NAME = 'my_hf_conn');
```

</TabItem>

</Tabs>
