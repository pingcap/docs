---
title: Set Up External Stage for TiDB Cloud Data Pipeline
summary: Configure Amazon S3 storage for TiDB Cloud Lake external stages, and learn about the current Alibaba Cloud OSS limitations.
---

# Set Up External Stage for TiDB Cloud Data Pipeline

This guide explains how to prepare the external object storage used by the [TiDB Cloud Data Pipeline](/tidb-cloud/data-pipeline-overview.md). An external stage is the intermediate bucket where TiDB Cloud writes exported snapshots and row changes, and TiDB Cloud Lake reads from it to load data into the target warehouse.

Use the section that matches your cloud provider:

- [AWS](#aws)
- [Alibaba Cloud](#alibaba-cloud)

## AWS

This section covers the setup for Amazon S3. TiDB Cloud writes data to your S3 bucket, and TiDB Cloud Lake reads data from it.

### Prerequisites

- An AWS account with permissions to manage IAM, S3, and optionally SQS resources.
- A TiDB Cloud account with a TiDB Cloud Lake warehouse.
- An S3 bucket in the same region as your TiDB Cloud instance. If you do not have one yet, create it in [Create an S3 Bucket](#step-1-create-an-s3-bucket).

### Step 1. Create an S3 bucket

> **Tip:**
>
> If you already have an S3 bucket ready, skip this step and just make sure your bucket region matches the region of your TiDB Cloud instance.

1. Open the [AWS S3 Console](https://console.aws.amazon.com/s3/) and create a new bucket.
2. Select a region, and make sure this region matches the region of your TiDB Cloud instance.
3. (Optional) Create a folder (prefix) inside the bucket to organize TiDB Cloud data (for example, `s3://tidb-cloud-lake-data/my-cluster/`).

### Step 2. Configure bucket access

Choose one of the following options for bucket access, and then complete the steps in the corresponding section:

* **Option 1: Bucket access with role ARN (CloudFormation)** (recommended)
* **Option 2: Bucket access with role ARN (manual setup)**
* **Option 3: Bucket access with access key (not recommended)**

> **Tip:**
>
> **Decide whether to enable event-driven ingestion before you start.**
>
> By default, TiDB Cloud Lake periodically scans the bucket for new data after the data pipeline is created. If you need lower data latency, you can optionally enable event-driven ingestion with an SQS queue. When new data is written to the bucket, an S3 event notification is sent to the SQS queue, allowing TiDB Cloud Lake to detect and load the new data without waiting for the next scheduled scan. The changefeed still flushes data to the bucket according to its configured cadence. Because event-driven ingestion can cause TiDB Cloud Lake to load data more frequently, it can increase the TiDB Cloud Lake service hosting cost.
>
> - With **option 1**, if you choose to enable event-driven ingestion, you can have the CloudFormation stack create the SQS queue when you create the stack, or add an SQS queue later manually.
> - With **options 2 and 3**, if you choose to enable event-driven ingestion, you need to create and configure the SQS queue manually.

#### Option 1. Bucket access with role ARN (CloudFormation)

One IAM role is shared by TiDB Cloud (which writes to the bucket) and TiDB Cloud Lake (which reads from it). The role's trust policy allows both sides to assume it, each guarded by its own external ID, so no long-lived credential is stored. This is the recommended option because the CloudFormation stack creates the role, its trust relationship, its permissions, and optionally the SQS queue and its policy in one go.

##### 1.1 Create the role with CloudFormation

1. In the TiDB Cloud console, open the **Create Data Pipeline** page, go to the **External Stage** area, and enter your **Bucket URI**.
2. Under **Bucket Access**, select **AWS Role ARN**, and click the CloudFormation link below the field to open the dialog.
3. Click **AWS Console with CloudFormation Template**. A new browser tab opens the AWS CloudFormation console with all parameters pre-filled.
4. In the new tab, enter a **stack name**, and optionally enter an **SQS queue name** if you need event-driven ingestion. CloudFormation creates the queue and its notification policy automatically. Leave the SQS field empty to skip it.
5. Create the stack and wait until the status becomes `CREATE_COMPLETE`.
6. In the **Outputs** tab of the stack, record the values required when you configure the External Stage in the TiDB Cloud console:

    - **Role ARN**: the `RoleARN` value.
    - **SQS queue URL** (only if you enabled SQS): the queue URL in the format `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`.

##### 1.2 (Optional) Configure the S3 bucket notification

If you enabled SQS in [1.1](#11-create-the-role-with-cloudformation), the queue and its policy are already created by the stack. The only remaining step is to configure the notification on your bucket, which the provided CloudFormation stack does not configure because the bucket already exists. Follow the manual notification steps in [2.3.2](#232-configure-the-s3-bucket-notification).

#### Option 2. Bucket access with role ARN (manual setup)

Use this option if you cannot use CloudFormation, or if your organization requires every IAM resource to be created and reviewed manually. The IAM role itself is the same as in option 1; only the way you create it is different.

##### 2.1 Collect the required values

1. In the TiDB Cloud console, open the **Create Data Pipeline** page, go to the **External Stage** area, and enter your **Bucket URI**.
2. Under **Bucket Access**, select **AWS Role ARN**, and click the CloudFormation link below the field to open the dialog.
3. Copy the following values from the **Having trouble?** area of the dialog. You need all of them for the trust policy in [2.2](#22-create-the-role-and-attach-the-policies):

    - TiDB Cloud account ID
    - TiDB Cloud external ID
    - Lake external ID
    - Lake platform setup & validation role ARN
    - Lake platform data loading role ARN

##### 2.2 Create the role and attach the policies

1. Open the [IAM Console](https://console.aws.amazon.com/iam/), go to **Roles > Create role**.
2. Under **Trusted entity type**, select **Custom trust policy**, and paste the following into the policy document. Replace the placeholder values with the ones you collected:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowTiDBCloudAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<TiDB Cloud account ID>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<TiDB Cloud external ID>" } }
        },
        {
          "Sid": "AllowLakeSetupAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform setup & validation role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        },
        {
          "Sid": "AllowLakeLoadAssumeRole",
          "Effect": "Allow",
          "Principal": { "AWS": "<Lake platform data loading role ARN>" },
          "Action": "sts:AssumeRole",
          "Condition": { "StringEquals": { "sts:ExternalId": "<Lake external ID>" } }
        }
      ]
    }
    ```

3. Enter a role name (for example, `tidb-cloud-lake-role`) and click **Create role**.
4. Open the role you just created, go to the **Permissions** tab, and click **Add permissions > Create inline policy**.
5. Select the **JSON** tab, and paste the following. Replace `YOUR_BUCKET_NAME` and `your-prefix` with your actual values, and remove the `SQSConsumeAccess` statement if you do not need event-driven ingestion:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketMetadata",
          "Effect": "Allow",
          "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
        },
        {
          "Sid": "S3ObjectReadWrite",
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject"],
          "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
        },
        {
          "Sid": "SQSConsumeAccess",
          "Effect": "Allow",
          "Action": ["sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes", "sqs:ChangeMessageVisibility"],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

6. Enter a policy name (for example, `tidb-cloud-lake-access`) and click **Create policy**.
7. Copy the role ARN from the role details page. You need it when you configure the External Stage in the TiDB Cloud console, for example `arn:aws:iam::123456789012:role/tidb-cloud-lake-role`.

##### 2.3 (Optional) Enable event-driven ingestion with SQS

Skip this section if periodic scanning is acceptable for your workload. For details about when to use SQS, see the note in [Prerequisites](#prerequisites).

###### 2.3.1 Create the SQS queue and configure the queue policy

1. Open the [SQS Console](https://console.aws.amazon.com/sqs/), click **Create queue**, select **Standard** type, and enter a name (for example, `tidb-cloud-lake-sqs`). Click **Create queue**.
2. Open the queue, go to the **Access policy** tab, and replace the policy with the following. This allows S3 to send notifications to the queue:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

    > **Note:** Replace `REGION`, `ACCOUNT_ID`, `YOUR_QUEUE_NAME`, and `YOUR_BUCKET_NAME` with your actual values.

3. Make sure the `SQSConsumeAccess` statement from [2.2](#22-create-the-role-and-attach-the-policies) is included in the role's permissions policy.
4. Record the queue URL from the queue details page in the SQS console. You need it when you configure the External Stage in the TiDB Cloud console, in the format `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`.

###### 2.3.2 Configure the S3 bucket notification

Because the bucket already exists, the provided CloudFormation stack does not configure the bucket notification automatically. In this case, you need to configure the notification manually:

1. Open the [AWS S3 Console](https://console.aws.amazon.com/s3/) and navigate to your bucket.
2. Go to **Properties > Event notifications > Create event notification**.
3. Configure:
    - **Event types:** select **All object create events**.
    - **Destination:** select **SQS queue** and choose the queue created earlier.
4. Click **Save changes**.

#### Option 3. Bucket access with access key (not recommended)

> **Note:**
>
> Using Access Key/Secret Key (AK/SK) means you need to manage and rotate credentials manually, and there is a higher risk of accidental exposure. For simpler management and better security, it is recommended to follow the steps in [Option 1](#option-1-bucket-access-with-role-arn-cloudformation) or [Option 2](#option-2-bucket-access-with-role-arn-manual-setup) to create a Role ARN instead.

With this option, you create an IAM user and provide its **Access Key ID** and **Secret Access Key** to TiDB Cloud. TiDB Cloud accesses your S3 bucket directly with these credentials.

##### 3.1 Create an IAM user and access key

1. Open the [IAM Console](https://console.aws.amazon.com/iam/) and go to **Users > Create user**.
2. Enter a user name (for example, `tidb-cloud-lake-user`), and click **Next**.
3. On the **Set permissions** page, create or attach a policy that grants the required S3 and optional SQS permissions. Replace `YOUR_BUCKET_NAME` and `your-prefix` with your actual values, and remove the `SQSConsumerAccess` statement if you do not need event-driven ingestion:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "S3BucketAccess",
          "Effect": "Allow",
          "Action": [
            "s3:GetObject",
            "s3:PutObject",
            "s3:ListBucket",
            "s3:GetBucketLocation"
          ],
          "Resource": [
            "arn:aws:s3:::YOUR_BUCKET_NAME",
            "arn:aws:s3:::YOUR_BUCKET_NAME/your-prefix/*"
          ]
        },
        {
          "Sid": "SQSConsumerAccess",
          "Effect": "Allow",
          "Action": [
            "sqs:ReceiveMessage",
            "sqs:DeleteMessage",
            "sqs:GetQueueAttributes",
            "sqs:ChangeMessageVisibility"
          ],
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME"
        }
      ]
    }
    ```

4. Click **Next**. On the **Review and create** page, review the user settings, and then click **Create user**.
5. On the **Users** page, click the name of the user you just created, and go to the **Security credentials** tab.
6. In the **Access keys** section, click **Create access key**. On the **Access key best practices & alternatives** page, select **Other**, click **Next**, and then create the access key.
7. Save the **Access Key ID** and **Secret Access Key**. You need them when configuring the External Stage in the TiDB Cloud console.

    > **Note:**
    >
    > The Secret Access Key is only shown once at creation time. Make sure to save it immediately.

##### 3.2 (Optional) Enable event-driven ingestion with SQS

Skip this section if periodic scanning is acceptable for your workload.

1. Open the [SQS Console](https://console.aws.amazon.com/sqs/), click **Create queue**, select **Standard** type, and enter a name (for example, `tidb-cloud-lake-sqs`). Click **Create queue**.
2. Open the queue, go to the **Access policy** tab, and replace the policy with the following, so that S3 can send notifications to the queue. Replace the placeholder values with your actual values:

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "AllowS3ToSendMessage",
          "Effect": "Allow",
          "Principal": { "Service": "s3.amazonaws.com" },
          "Action": "sqs:SendMessage",
          "Resource": "arn:aws:sqs:REGION:ACCOUNT_ID:YOUR_QUEUE_NAME",
          "Condition": {
            "ArnLike": { "aws:SourceArn": "arn:aws:s3:::YOUR_BUCKET_NAME" },
            "StringEquals": { "aws:SourceAccount": "ACCOUNT_ID" }
          }
        }
      ]
    }
    ```

3. Configure the notification on your bucket:

    1. Open the [AWS S3 Console](https://console.aws.amazon.com/s3/) and navigate to your bucket.
    2. Go to **Properties > Event notifications > Create event notification**.
    3. Configure:
        - **Event types:** select **All object create events**.
        - **Destination:** select **SQS queue** and choose the queue created earlier.
    4. Click **Save changes**.

4. Record the queue URL from the queue details page in the SQS console. You need it when you configure the External Stage in the TiDB Cloud console, in the format `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`.

### What's next?

After completing the AWS setup, you have all the values required by the External Stage configuration:

- **S3 URI**: from **Create an S3 bucket**.
- **Bucket access**: the Role ARN (options 1 and 2), or the Access Key ID and Secret Access Key (option 3).
- **SQS queue URL** (optional).

In the [TiDB Cloud console](https://tidbcloud.com), navigate to the Data Pipeline configuration page for your TiDB Cloud instance, and enter these values in the **External Stage** settings to complete the data pipeline setup.

## Alibaba Cloud

> **Note:**
>
> Alibaba Cloud OSS is accepted during pipeline validation, but it has not yet been verified for end-to-end Data Pipeline setup (Export > Changefeed > Lake) like Amazon S3, and the required OSS endpoint and region handling are not yet finalized. If you need to use OSS, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) to confirm current availability for your scenario.
>
> **Limitations for Alibaba Cloud OSS:**
>
> - Only **Access Key** authentication is supported. Role ARN is not available for OSS.
> - Event-driven ingestion with SQS is not supported. The pipeline uses polling only.

This section describes the preliminary configuration for Object Storage Service (OSS). TiDB Cloud writes incremental data and snapshots to your OSS bucket, and TiDB Cloud Lake reads the data from it.

### Prerequisites

- An Alibaba Cloud account with permissions to manage OSS and RAM resources.
- A TiDB Cloud account with a TiDB Cloud Lake warehouse.

### Step 1. Create an OSS bucket

> **Tip:**
>
> If you already have an OSS bucket ready, skip this step. Using the same region as your TiDB Cloud instance is recommended but not strictly required for OSS.

1. Open the [OSS Console](https://oss.console.aliyun.com/) and create a new bucket.
2. Select a region. Using the same region as your TiDB Cloud instance is recommended.
3. Optionally, create a folder (prefix) inside the bucket to organize TiDB Cloud data (for example, `oss://tidb-cloud-lake-data/my-cluster/`).
4. Record the following values as you will need them in later steps:

    - **Bucket Name:** for example, `tidb-cloud-lake-data`
    - **OSS URI (with prefix):** for example, `oss://tidb-cloud-lake-data/my-cluster/`

### Step 2. Create a RAM user and AccessKey pair

1. Open the [RAM Console](https://ram.console.aliyun.com/) and go to **Users > Create user**.
2. Enter a display name (for example, `tidb-cloud-lake-user`) and select **OpenAPI calling** as the access method.
3. Click **Next**, then copy and save the **AccessKey ID** and **AccessKey Secret**.

    > **Note:**
    >
    > The AccessKey Secret is only shown once at creation time. Make sure to save it immediately.

4. Return to the **Users** page, click the name of the user you just created, go to the **Permissions** tab, and click **Add permissions**.
5. Select **Custom policy**, click **Create policy**, and then select the **Script** tab to create the policy from the following JSON:

    ```json
    {
      "Version": "1",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": [
            "oss:ListObjects",
            "oss:GetObject",
            "oss:PutObject",
            "oss:DeleteObject"
          ],
          "Resource": [
            "acs:oss:*:*:YOUR_BUCKET_NAME",
            "acs:oss:*:*:YOUR_BUCKET_NAME/*"
          ]
        }
      ]
    }
    ```

    > **Note:** Replace `YOUR_BUCKET_NAME` with the name of your OSS bucket.

6. Enter a policy name (for example, `tidb-cloud-lake-access`) and click **OK**.
7. Attach the policy to the RAM user.
8. Record the following values as you will need them when configuring TiDB Cloud:
    - **Access Key ID:** for example, `LTAI5t...`
    - **Access Key Secret:** saved at creation time

### Step 3. Configure the External Stage in TiDB Cloud

After the bucket, RAM user, and permissions are ready, contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) before configuring an OSS external stage because the required OSS endpoint configuration is not yet finalized.

- **Bucket URI**: the OSS URI from Step 1, such as `oss://tidb-cloud-lake-data/my-cluster/`
- **Access Key ID**: the RAM user's AccessKey ID
- **Access Key Secret**: the RAM user's AccessKey Secret

After TiDB Cloud Support confirms the current OSS configuration requirements, enter the required values in the **External Stage** settings and test the connection.

### What's next?

After completing the Alibaba Cloud setup, you have the following resources ready for the TiDB Cloud Lake **External Stage** configuration:

| Resource | Where to find it |
|----------|------------------|
| **OSS URI** | From Step 1, for example, `oss://tidb-cloud-lake-data/my-cluster/` |
| **Access Key ID** | From Step 2, for example, `LTAI5t...` |
| **Access Key Secret** | From Step 2, saved at creation time |

In the [TiDB Cloud console](https://tidbcloud.com), navigate to the Data Pipeline configuration page for your TiDB Cloud instance, and enter these values in the **External Stage** settings to complete the data pipeline setup.
