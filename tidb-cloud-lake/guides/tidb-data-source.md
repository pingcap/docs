---
title: TiDB Data Source (Preview)
summary: Guide on setting up a TiDB data source in TiDB Cloud Lake, including storage and authentication configurations.
---

# TiDB Data Source (Preview)

A **TiDB** data source stores the object storage location, credentials, and optional event queue that TiDB Cloud Lake uses to read data staged by your TiDB cluster. It does not connect to the TiDB server itself. Dumpling and TiCDC write exports and change events to an object storage bucket, and TiDB Cloud Lake reads from that bucket.

## Use Cases

- Manage the staging bucket, credentials, and optional SQS queue centrally for multiple TiDB sync tasks
- Avoid re-entering the same bucket and authorization settings in every task
- Use IAM Role instead of static keys so TiDB Cloud Lake obtains short-lived credentials
- Update the bucket, role, or queue in one place when it is referenced by multiple tasks

## Prepare TiDB for Integration

TiDB Cloud exports full snapshots (Dumpling) and incremental changes (TiCDC) to an object storage bucket. Due to the differences across TiDB Cloud plans, we recommend a specific setup path for each plan to keep configuration minimal and ensure data compatibility.

<!--Links to be updated-->

- **Premium** or **BYOC**: use the [TiDB Cloud console **Data Pipeline**](https://docs.pingcap.com/tidbcloud/data-pipeline-lake-setup-for-premium/?plan=premium) UI to set up and manage export and import in one place.
- **Essential**, **Premium**, or **BYOC** users who prefer manual setup: use the console **Export** and **Change Feed** features to [configure Dumpling and TiCDC individually](https://docs.pingcap.com/tidbcloud/data-pipeline-lake-setup-for-essential).
- **Dedicated**: follow [the Dedicated integration guide](https://docs.pingcap.com/tidbcloud/data-pipeline-lake-setup-for-dedicated) for the recommended approach.

## Create TiDB Data Source

1. Navigate to **Data** > **Data Sources**, then click **Create**.
2. Select **TiDB** as the service, then fill in the **Name** of the data source.
3. Choose a **Storage Provider** and an **Authentication Method**, then fill in the connection details. The fields depend on the combination you select. See [Amazon S3](#amazon-s3) or [Alibaba Cloud OSS](#alibaba-cloud-oss) below.

    > **Note:**
    >
    > Use the same storage provider and region as your TiDB Cloud Lake deployment when possible.

4. Click **Test Connectivity** to validate the bucket and credentials. If the test succeeds, click **OK** to save the data source.

## Amazon S3

When the storage provider is **Amazon S3**, choose one of the following authentication methods.

### Authentication Method: Role ARN (Recommended)

Role ARN uses the AssumeRole model. TiDB Cloud Lake assumes an IAM Role in your AWS account and obtains temporary credentials, so you never hand static keys to TiDB Cloud Lake.

Before you can save the data source, your IAM Role's trust policy must trust the two platform roles (setup/validation and data loading) with the corresponding External ID as the `sts:ExternalId` condition. See [Authenticate with AWS IAM Role](https://docs.pingcap.com/tidbcloudlake/authenticate-with-aws-iam-role/) for the full trust policy setup.

| Field                     | Required | Description                                                                                                                                  |
| ------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Name**                  | Yes      | A descriptive name for this data source                                                                                                      |
| **Storage Provider**      | Yes      | Select **Amazon S3**                                                                                                                         |
| **Authentication Method** | Yes      | Select **Role ARN**                                                                                                                          |
| **Role ARN**              | Yes      | IAM Role ARN in your AWS account that TiDB Cloud Lake is allowed to assume, for example `arn:aws:iam::123456789012:role/tidbcloud-lake-tidb` |
| **S3 Bucket Name**        | Yes      | Bucket where TiCDC / Dumpling stages the data that TiDB Cloud Lake loads                                                                     |
| **S3 Region**             | Yes      | AWS Region of the bucket, for example `us-east-1`                                                                                            |
| **S3 Endpoint**           | No       | Only for S3-compatible storage such as MinIO, for example `http://localhost:9000`. Leave empty for Amazon S3                                 |
| **SQS Queue URL**         | No       | Optional SQS standard queue URL for event-driven mode. See [Optional SQS Queue](#optional-sqs-queue)                                         |

### Authentication Method: Access Key / Secret Key

Use this method when you prefer static credentials, for example for an S3-compatible store that does not support role assumption.

For more details, see [Amazon S3 - Credentials](https://docs.pingcap.com/tidbcloudlake/aws-credentials/).

| Field | Required | Description |
|-------|----------|-------------|
| **Name** | Yes | A descriptive name for this data source |
| **Storage Provider** | Yes | Select **Amazon S3** |
| **Authentication Method** | Yes | Select **Access Key / Secret Key** |
| **S3 Access Key** | Yes | Access key ID with access to the staging bucket |
| **S3 Secret Key** | Yes | Secret access key paired with the access key ID |
| **S3 Bucket Name** | Yes | Bucket where TiCDC / Dumpling stages the data that TiDB Cloud Lake loads |
| **S3 Region** | Yes | AWS Region of the bucket |
| **S3 Endpoint** | No | Only for S3-compatible storage. Leave empty for Amazon S3 |
| **SQS Queue URL** | No | Optional SQS standard queue URL for event-driven mode |

## Alibaba Cloud OSS

When the storage provider is **Alibaba Cloud OSS**, TiDB Cloud Lake reads the staging bucket from Alibaba Cloud. OSS supports **Access Key / Secret Key** authentication only.

| Field | Required | Description |
|-------|----------|-------------|
| **Name** | Yes | A descriptive name for this data source |
| **Storage Provider** | Yes | Select **Alibaba Cloud OSS** |
| **OSS Access Key ID** | Yes | OSS AccessKey ID |
| **OSS AccessKey Secret** | Yes | OSS AccessKey secret |
| **OSS Bucket** | Yes | OSS bucket where TiCDC / Dumpling stages the data |
| **OSS Region** | Read-only | The Lake's deployment region. It is displayed automatically and cannot be changed |

## Optional SQS Queue

The **SQS Queue URL** field is optional and applies to Amazon S3 only. When you provide a standard SQS queue that receives S3 `ObjectCreated` events for the staging bucket, TiDB Cloud Lake can discover newly written changefeed / export objects from the queue instead of waiting for the next poll.

- The queue must be a **standard** queue. FIFO queues are not supported, because S3 event notifications cannot be delivered to them.
- The S3 bucket and the SQS queue should be in the same Region.
- Polling the bucket remains the authoritative discovery path, and SQS is a latency optimization, not a replacement.
- If you leave this field empty, the task discovers objects by polling.

For queue, bucket notification, and trust policy setup, see [Amazon SQS (S3) - IAM Role](/tidb-cloud-lake/guides/amazon-sqs-s3-iam-role.md).

## Next Steps

After creating this data source, you can use it to create a [TiDB Integration Task](/tidb-cloud-lake/guides/integrate-with-tidb.md).
