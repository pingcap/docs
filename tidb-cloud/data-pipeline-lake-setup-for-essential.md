---
title: Set Up Data Pipeline to TiDB Cloud Lake (Essential)
summary: Manual setup guide for building a TiDB Cloud Lake data pipeline on Essential V1/V2 instances using Export, CDC Changefeed, and Lake integration.
---

TiDB Cloud Essential instances do not support the native Data Pipeline UI. This guide describes the manual configuration process end-to-end, using Export for full snapshots and CDC Changefeed for incremental data, and integrating both with TiDB Cloud Lake.

# Restrictions

- The TiDB Cloud Lake warehouse must be in the **same region** as your Essential instance.
- Only tables with a **primary key** can be replicated incrementally.
- The pipeline requires manual setup and maintenance of IAM roles, changefeeds, and Lake integrations.
- For details on DDL, DML, and column type support, see [Data Pipeline Support Matrix](/tidb-cloud/data-pipeline/lake-data-pipeline-support-matrix.md).

# Prerequisites

Before you begin, make sure that you have:

- A TiDB Cloud Essential instance deployed in a specific region.
- Access to the TiDB Cloud Open API for this tenant. To create an API key, refer to [Create an API Key](https://docs.pingcap.com/tidbcloud/api-overview#create-an-api-key). Make sure to save the **Public Key** and **Private Key**, they are required for all Open API calls in this guide.
- An S3 bucket in the same region (for example, `s3://my-datapipeline-bucket`).
- A TiDB Cloud Lake warehouse in the same region.

> **Note:**
>
> This guide assumes you already have data in the source TiDB database that you want to replicate. For details on preparing sample data, see the original Essential data pipeline SOP.

---

# Prepare Bucket Access

The data pipeline components (Export, Changefeed, and Lake) all require access to the same S3 bucket. Choose one of the following methods:

- **Role ARN**: a single IAM role shared by all three components. More secure, no long-lived credentials.
- **Access Key**: simpler to set up and required when Role ARN is unavailable; requires manual credential management and rotation.

## Use a Role ARN

The Export CloudFormation stack creates the IAM role initially; you then extend its trust policy and permissions to support Changefeed and Lake.

### Step 1: Create the role with Export CloudFormation

In the TiDB Cloud console, navigate to **Data → Import**, click **Export Data to** in the upper-right corner, and choose **Amazon S3**. When configuring the S3 destination with **Role ARN** authentication, TiDB Cloud provides a CloudFormation link. Use it to create the IAM role.

After the stack is created, record the **Role ARN** from the stack **Outputs** (for example, `arn:aws:iam::<account-id>:role/<role-name>`).

> **Note:**
>
> The CloudFormation-created role includes an S3 permissions policy scoped to the **export snapshot path** only (for example, `s3://bucket/prefix/snapshot/*`). You will expand this policy in Step 3 to cover the full data pipeline prefix (for example, `s3://bucket/prefix/*`). To modify the policy in AWS Console, navigate to the newly created role, under the **Permissions** tab, click the policy name, and edit the policy.

### Step 2: Consolidate trust relationships

The role must trust three TiDB Cloud services. Collect the following values, then append them all as a single trust policy. In the AWS Console, navigate to the role created in Step 1, go to the **Trust relationships** tab, and click **Edit trust policy** to replace the policy.

**Collect values:**

- **Export**: trust relationship is already configured by CloudFormation. No action needed.
- **Changefeed**: call the Open API to get the required values:

    ```shell
    curl -L -X GET 'https://serverless.tidbapi.com/v1beta1/clusters/{clusterId}/changefeeds:getCloudStorageAuthConfig' \
      -u '<Public Key>:<Private Key>' --digest
    ```

    Record `tidbCloudAccountId` and `tidbCloudAccountExternalId` from the response.
- **Lake**: in the Lake staging console, navigate to **Data → Data Sources → Create**, in the **Basic Info** section select **Service: TiDB**, then under **Trust Cloud Platform roles**, record the following values:
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

### Step 3: Expand permissions to cover the full pipeline prefix

The CloudFormation-created permissions policy is scoped to the snapshot export path only. The Changefeed writes to `{prefix}/incremental/` and the Lake reads from both `{prefix}/snapshot/` and `{prefix}/incremental/`, so the policy must cover the parent prefix.

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

> **Important:**
>
> The CloudFormation-created policy uses a narrower resource like `s3://bucket/prefix/snapshot/*`. You must change this to `s3://bucket/prefix/*` so that both Changefeed (which writes to `prefix/incremental/`) and Lake (which reads from both sub-paths) have sufficient access.

## Use an Access Key

> **Note:**
>
> Using an Access Key and Secret Key (AK/SK) requires manual credential management and rotation, which increases security risks. For stronger security, use **Role ARN** instead.

If you prefer Access Key authentication, create an IAM user with the following permissions and provide its credentials when configuring Export, Changefeed, and Lake.

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

---

# Export full snapshot to S3

In the TiDB Cloud console, navigate to **Data → Import**, click **Export Data to** in the upper-right corner, and choose **Amazon S3** to create a new export task.

**Configuration:**

- **Selected Data**: choose the databases to export.
- **Data Format**: `CSV`
    - Click **Edit CSV Configuration** and set:
        - **Dialect**: `Snowflake`
        - **Escape backslash**: `false`
- **Compression**: `None`
- **Amazon S3 Settings**:
    - **Bucket URI**: `s3://<bucket>/<prefix>/snapshot/` (use the recommended snapshot sub-path)
    - **Role ARN** or **Access Key**: use the credentials from [Prepare Bucket Access](#prepare-bucket-access).

After the export task completes, open the task detail and record the **Snapshot TSO** value. This TSO is required when creating the CDC changefeed.

---

# Create CDC changefeed for incremental data

Since the Essential console does not support creating a cloud-storage sink, you must use the Open API.

## Create the changefeed

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

---

# Configure TiDB Cloud Lake

> **Note:**
>
> The Lake production environment does not yet support the TiDB data source. Use the **staging** environment for now.

## Create a data source

1. In the Lake staging console, navigate to **Data → Data Sources → Create**.
2. Select **Service: TiDB**.
3. Choose **Role ARN** or **Access Key** authentication and fill in:
    - **Role ARN**: the ARN from [Step 1](#step-1-create-the-role-with-export-cloudformation), or **Access Key ID** / **Secret Access Key** from [Use an Access Key](#use-an-access-key).
    - **S3 Bucket Name**: the bucket name only (for example, `my-datapipeline-bucket`, not the full URI).
    - **S3 Region**: the same region as your Essential instance.
4. **SQS Queue URL** is optional. If you want to enable event-driven ingestion, set up an SQS queue and configure the S3 bucket notification first. For details, see [Amazon SQS and S3 IAM Role for TiDB Cloud Lake](https://docs.pingcap.com/tidbcloudlake/amazon-sqs-s3-iam-role/).
5. Under **Trust Cloud Platform roles**, verify the Lake platform roles and external ID match the values you added to the consolidated trust policy in [Step 2](#step-2-consolidate-trust-relationships).

## Create an integration

1. Navigate to **Data → Integration → Create**.
2. Fill in the following fields:
    - **Data Source**: select the data source created above.
    - **Name**: a name for this integration task.
    - **Table Rules**: `*.*` to sync all exported tables.
    - **Changefeed S3 Prefix**: `<prefix>/incremental/`.
    - **Dumpling S3 Prefix**: `<prefix>/snapshot/`.
    - **Poll Interval**: the interval at which Lake scans the external stage for new data. Default is 60 seconds. A shorter interval reduces data latency but increases Lake hosting cost.
    - **Merge Interval**: the interval at which Lake merges incremental data into the warehouse. Default is 30 seconds. A shorter interval reduces data latency but increases Lake hosting cost.
    - **Warehouse**: select the target warehouse.
3. Click **Create**.
4. After creation, the integration is **Stopped** by default. Click the integration action button → **Start** to begin data loading.

---

For frequently asked questions about Data Pipeline, see [Data Pipeline FAQ](/tidb-cloud/data-pipeline/lake-data-pipeline-faq.md).
