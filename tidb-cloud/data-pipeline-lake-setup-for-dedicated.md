---
title: Set Up Data Pipeline from TiDB Cloud Essential to TiDB Cloud Lake
summary: Manual setup guide for building a TiDB Cloud Lake data pipeline on TiDB Cloud Essential instances using export, a changefeed, and TiDB Cloud Lake integration.
---

# Set Up Data Pipeline from TiDB Cloud Essential to TiDB Cloud Lake

TiDB Cloud Essential does not provide the native Data Pipeline setup experience in the TiDB Cloud console. To replicate data from a TiDB Cloud Essential instance to TiDB Cloud Lake, you need to configure the pipeline manually.

This guide walks you through the end-to-end setup: export a full snapshot to Amazon S3, create a changefeed to continuously write incremental changes to the same S3 location, and configure TiDB Cloud Lake to load both the snapshot and incremental data.

## Restrictions

- The TiDB Cloud Lake warehouse must be in the **same region** as your Essential instance.
- Only tables with a **primary key** can be replicated incrementally.
- The pipeline requires manual setup and maintenance of AWS IAM resources and credentials, changefeeds, and TiDB Cloud Lake integrations.
- For details on DDL, DML, and column type support, see [Data Pipeline Support Matrix](/tidb-cloud/data-pipeline-lake-support-matrix.md).

## Prerequisites

Before you begin, make sure that you have:

- A TiDB Cloud Essential instance deployed in a specific region.
- Access to the TiDB Cloud API for this organization. You can create an API key on the [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) page in the [TiDB Cloud console](https://tidbcloud.com/). Make sure to save the **Public Key** and **Private Key** because they are required for all API calls in this guide.
- An Amazon S3 bucket in the same region (for example, `s3://my-datapipeline-bucket`) as your TiDB Cloud Essential instance.
- A TiDB Cloud Lake warehouse in the same region as your TiDB Cloud Essential instance.

> **Note:**
>
> This guide assumes you already have data in the source TiDB database that you want to replicate. If you need sample data, prepare it before continuing.

## Prepare S3 bucket access

The data pipeline components (export, changefeed, and TiDB Cloud Lake) all require access to the same S3 bucket. Choose one of the following methods to access the S3 bucket:

- **Role ARN** (for TiDB Cloud Essential instances hosted on AWS): a single IAM role shared by all three components. This method avoids long-lived credentials and provides stronger security.
- **Access Key**: simpler to set up and required when Role ARN is unavailable; requires manual credential management and rotation.

### Method 1: Use a Role ARN

In this method, you first use the CloudFormation stack provided by the Export feature in the TiDB Cloud console to create an IAM role configured for Export. Then, you extend the same role's trust policy and permissions so that the changefeed and TiDB Cloud Lake can also use it to access the S3 bucket.

#### Step 1. Create the role with Export CloudFormation

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the overview page for your TiDB Cloud Essential instance.
2. Click **Data > Import** in the left navigation pane, and then click **Export Data to** in the upper-right corner.
3. Choose **Amazon S3**. When configuring the S3 destination with **Role ARN** authentication, TiDB Cloud provides a CloudFormation link. Use it to create the IAM role.

After the stack is created, record the **Role ARN** from the stack **Outputs** (for example, `arn:aws:iam::<account-id>:role/<role-name>`).

> **Note:**
>
> The CloudFormation-created role includes an S3 permissions policy scoped to the **export snapshot path** only (for example, `arn:aws:s3:::bucket/prefix/snapshot/*`). You will expand this policy in Step 3 to cover the full data pipeline prefix (for example, `arn:aws:s3:::bucket/prefix/*`). To modify the policy in AWS Console, navigate to the newly created role, under the **Permissions** tab, click the policy name, and edit the policy.

#### Step 2. Consolidate trust relationships

The IAM role created in the previous step is initially configured for exporting data from TiDB Cloud Essential to S3. Because the same role is also used by the changefeed and TiDB Cloud Lake to access the S3 bucket, update its trust policy to allow these components to assume the role as well.

Collect the following values required for the additional trust relationships, and then update the role's trust policy. In the AWS Console, navigate to the role created in [Step 1](#step-1-create-the-role-with-export-cloudformation), go to the **Trust relationships** tab, and click **Edit trust policy**.

- **Export**: before replacing the trust policy, record the existing Export AWS account ID and external ID so that you can preserve this trust relationship in the consolidated policy.
- **Changefeed**: call the TiDB Cloud API to get the required values:

    ```shell
    curl -L -X GET 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds:getCloudStorageAuthConfig' \
      -u '<Public Key>:<Private Key>' --digest
    ```

    Record `tidbCloudAccountId` and `tidbCloudAccountExternalId` from the response.
- **TiDB Cloud Lake**: in the TiDB Cloud Lake staging console, navigate to **Data > Data Sources > Create**. In the **Basic Info** section, select **Service: TiDB**, and then under **Trust Cloud Platform roles**, record the following values:
    - Lake Setup & Validation Role ARN
    - Lake Data Loading Role ARN
    - Lake External ID

**Replace** the role's trust policy with the consolidated policy below:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExportAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Export_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Export_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowChangefeedAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Changefeed_TiDB_Cloud_Account_ID>:root"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Changefeed_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeSetupAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Setup_and_Validation_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    },
    {
      "Sid": "AllowLakeLoadAssumeRole",
      "Effect": "Allow",
      "Principal": {
        "AWS": "<Lake_Data_Loading_Role_ARN>"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "sts:ExternalId": "<Lake_External_ID>"
        }
      }
    }
  ]
}
```

#### Step 3. Expand permissions to cover the full pipeline prefix

The CloudFormation-created permissions policy is scoped to the snapshot export path only. The changefeed writes to `{prefix}/incremental/`, and TiDB Cloud Lake reads from both `{prefix}/snapshot/` and `{prefix}/incremental/`, so the policy must cover the parent prefix.

In the AWS Console, navigate to the role created in Step 1, under the **Permissions** tab, click the policy name, and edit the policy to replace the resource scope.

**Replace** the role's inline permissions policy with:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>"
    },
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:GetObjectVersion",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
    }
  ]
}
```

> **Note:**
>
> The CloudFormation-created policy uses a narrower resource like `arn:aws:s3:::bucket/prefix/snapshot/*`. You must change this to `arn:aws:s3:::bucket/prefix/*` so that both changefeed (which writes to `prefix/incremental/`) and TiDB Cloud Lake (which reads from both sub-paths) have sufficient access.

### Method 2: Use an Access Key

> **Note:**
>
> Using an Access Key and Secret Key (AK/SK) requires manual credential management and rotation, which increases security risks. For stronger security, use **Role ARN** instead.

If you prefer Access Key authentication, create an IAM user with the following permissions and provide its credentials when configuring Export, changefeed, and TiDB Cloud Lake.

**Permissions policy:**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3BucketAccess",
      "Effect": "Allow",
      "Action": [
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>"
    },
    {
      "Sid": "S3ObjectAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:GetObjectVersion",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::<your-bucket-name>/<your-prefix>/*"
    }
  ]
}
```

Record the **Access Key ID** and **Secret Access Key** for use in later steps.

## Export full snapshot to S3

In the TiDB Cloud console, navigate to **Data > Import**, click **Export Data to** in the upper-right corner, and choose **Amazon S3** to create a new export task.

**Configuration:**

- **Selected Data**: choose the databases and tables to export.
- **Data Format**: `CSV`
    - Click **Edit CSV Configuration** and set:
        - **Dialect**: `Snowflake`
        - **Escape backslash**: `false`
- **Compression**: `None`
- **Amazon S3 Settings**:
    - **Bucket URI**: `s3://<bucket>/<prefix>/snapshot/` (use the recommended snapshot sub-path)
    - **Role ARN** or **Access Key**: use the credentials from [Prepare Bucket Access](#prepare-bucket-access).

After the export task completes, open the task details and record the **Snapshot TSO** value. This TSO is required when creating the changefeed.

## Create a changefeed for incremental data

Since the Essential console does not support creating a cloud-storage sink, you must use the TiDB Cloud API.

### Create the changefeed

Call the changefeed creation API with the following required fields:

| Field | Required Value |
|-------|---------------|
| `sink.cloudStorage.dataFormat.protocol` | `CANAL_JSON` |
| `sink.cloudStorage.dataFormat.canalJsonConfig.enableTidbExtension` | `true` |
| `sink.cloudStorage.dataFormat.contentCompatible` | `true` |
| `startPosition.mode` | `FROM_TSO` |
| `startPosition.tso` | `<snapshot_tso from the export step>` |

**Request example:**

```shell
curl -L -X POST 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds' \
  -H 'Content-Type: application/json' \
  -u '<Public Key>:<Private Key>' --digest \
  -d '{
    "displayName": "<changefeed-name>",
    "sink": {
      "type": "CLOUD_STORAGE",
      "cloudStorage": {
        "storage": {
          "type": "S3",
          "s3": {
            "uri": "s3://<bucket>/<prefix>/incremental/",
            "authType": "ROLE_ARN",
            "roleArn": "<role-arn>"
          }
        },
        "dataFormat": {
          "protocol": "CANAL_JSON",
          "contentCompatible": true,
          "canalJsonConfig": {
            "enableTidbExtension": true
          }
        }
      }
    },
    "filter": {
      "mode": "IGNORE_NOT_SUPPORT_TABLE",
      "filterRule": ["*.*"]
    },
    "startPosition": {
      "mode": "FROM_TSO",
      "tso": "<snapshot_tso>"
    },
    "rcu": 2
  }'
```

> **Note:**
>
> The changefeed URI must use the `incremental/` sub-path under the same prefix as the export snapshot. The IAM role's permissions (from [Step 3](#step-3-expand-permissions-to-cover-the-full-pipeline-prefix)) must cover this path.
>
> If you are using **Access Key** instead of Role ARN, replace the `s3` block in the request body with:
>
> ```json
> "s3": {
>   "uri": "s3://<bucket>/<prefix>/incremental/",
>   "authType": "ACCESS_KEY",
>   "accessKey": {
>     "id": "<access-key-id>",
>     "secret": "<access-key-secret>"
>   }
> }
> ```
>

## Configure TiDB Cloud Lake

> **Note:**
>
> The TiDB Cloud Lake production environment does not yet support the TiDB data source. Use the **staging** environment for now.

### Create a data source

1. In the Lake staging console, navigate to **Data > Data Sources > Create**.
2. Select **Service: TiDB**.
3. Choose **Role ARN** or **Access Key** authentication and fill in:
    - **Role ARN**: the ARN from [Step 1](#step-1-create-the-role-with-export-cloudformation), or **Access Key ID** / **Secret Access Key** from [Method 2: Use an Access Key](#method-2-use-an-access-key).
    - **S3 Bucket Name**: the bucket name only (for example, `my-datapipeline-bucket`, not the full URI).
    - **S3 Region**: the same region as your Essential instance.
4. **SQS Queue URL** is optional. If you want to enable event-driven ingestion, set up an SQS queue and configure the S3 bucket notification first. For details, see [Amazon SQS and S3 IAM Role for TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/).
5. Under **Trust Cloud Platform roles**, verify the TiDB Cloud Lake platform roles and external ID match the values you added to the consolidated trust policy in [Step 2](#step-2-consolidate-trust-relationships).

### Create an integration

1. In the Lake staging console, navigate to **Data > Integration > Create**.
2. Fill in the following fields:
    - **Data Source**: select the data source created above.
    - **Name**: a name for this integration task.
    - **Table Rules**: `*.*` to sync all exported tables.
    - **Changefeed S3 Prefix**: `<prefix>/incremental/`.
    - **Dumpling S3 Prefix**: `<prefix>/snapshot/`.
    - **Poll Interval**: the interval at which TiDB Cloud Lake scans the external stage for new data. The default value is 60 seconds. A shorter interval reduces data latency but increases TiDB Cloud Lake hosting cost.
    - **Merge Interval**: the interval at which TiDB Cloud Lake merges incremental data into the warehouse. The default value is 30 seconds. A shorter interval reduces data latency but increases TiDB Cloud Lake hosting cost.
    - **Warehouse**: select the target warehouse.
3. Click **Create**.
4. After creation, the integration is **Stopped** by default. Click the integration action button > **Start** to begin data loading.

## See also

- For frequently asked questions about Data Pipeline, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline-lake-faq.md).
- For details on DDL, DML, and column type support, see [Data Pipeline Support Matrix](/tidb-cloud/data-pipeline-lake-support-matrix.md).
