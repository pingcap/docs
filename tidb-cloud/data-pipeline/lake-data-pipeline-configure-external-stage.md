---
title: Set Up External Stage for TiDB Cloud Data Pipeline
summary: Configure AWS S3 and Alibaba Cloud OSS storage for TiDB Cloud Lake external stages.
---

# Set Up External Stage for TiDB Cloud Data Pipeline

> Configure AWS S3 and Alibaba Cloud OSS buckets for TiDB Cloud Lake data pipelines

This guide explains how to prepare the object storage used by the TiDB Cloud Data Pipeline. An external stage is the intermediate bucket where TiDB Cloud writes exported snapshots and row changes, and TiDB Cloud Lake reads from it to load data into the target warehouse.

Use the section that matches your cloud provider:

- [AWS](#aws)
- [Alibaba Cloud](#alibaba-cloud)

---

# AWS

This section covers the setup for Amazon S3. TiDB Cloud writes data to your S3 bucket, and TiDB Cloud Lake reads data from it.

## Prerequisites

- An AWS account with permissions to manage IAM, S3, and optionally SQS resources.
- A TiDB Cloud account with a TiDB Cloud Lake deployment.
- An S3 bucket in the same region as your TiDB Cloud instance. If you do not have one yet, create it in [Create an S3 Bucket](#step-1-create-an-s3-bucket).

> 💡 **Decide on event-driven ingestion before you start.** By default, TiDB Cloud Lake loads new data by scanning the bucket at the sync interval you configure for the data pipeline. If you need lower data latency, enable **event-driven ingestion** with an SQS queue. TiDB Cloud Lake is notified whenever new data is written to the bucket and loads the data as soon as it arrives. This mode does not follow the sync interval and increases the TiDB Cloud Lake service hosting cost.
>
> - With **option 1**, the queue is created by the CloudFormation stack, so you must decide before you create the stack. Otherwise, follow the manual SQS steps in [Option 2 → 2.3](#23-optional-enable-event-driven-ingestion-with-sqs).
> - With **options 2 and 3**, the queue is always created manually.

## Step 1: Create an S3 bucket

> 💡 If you already have an S3 bucket ready, skip this step — just make sure the bucket region matches the region of your TiDB Cloud instance.

1. Open the [AWS S3 Console](https://console.aws.amazon.com/s3/) and create a new bucket.
2. Select a region, **make sure this region matches the region of your TiDB Cloud instance.**
3. Optionally, create a folder (prefix) inside the bucket to organize TiDB Cloud data (for example, `s3://tidb-cloud-lake-data/my-cluster/`).

## Step 2: Configure bucket access

Choose one of the following options for bucket access, and then complete the steps in the corresponding section:

- **Option 1: Bucket Access with Role ARN (CloudFormation)** (recommended)
- **Option 2: Bucket Access with Role ARN (Manual Setup)**
- **Option 3: Bucket Access with Access Key (Not Recommended)**

### Option 1: Bucket Access with Role ARN (CloudFormation)

One IAM role is shared by TiDB Cloud (which writes to the bucket) and TiDB Cloud Lake (which reads from it). The role's trust policy allows both sides to assume it, each guarded by its own external ID, so no long-lived credential is stored. This is the recommended option because the CloudFormation stack creates the role, its trust relationship, its permissions, and optionally the SQS queue and its policy in one go.

#### 1.1 Create the role with CloudFormation

1. In the TiDB Cloud console, open the **Create Data Pipeline** page, go to the **External Stage** area, and enter your **Bucket URI**.
2. Under **Bucket Access**, select **AWS Role ARN**, and click the CloudFormation link below the field to open the dialog.
3. Click **AWS Console with CloudFormation Template**. A new browser tab opens the AWS CloudFormation console with all parameters pre-filled.
4. In the new tab, enter a **stack name**, and optionally enter an **SQS queue name** if you need event-driven ingestion. CloudFormation creates the queue and its notification policy automatically. Leave the SQS field empty to skip it.
5. Create the stack and wait until the status becomes `CREATE_COMPLETE`.
6. In the **Outputs** tab of the stack, record the values required when you configure the External Stage in the TiDB Cloud console:

    - **Role ARN**: the `RoleARN` value.
    - **SQS queue URL** (only if you enabled SQS): the queue URL in the format `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`.

#### 1.2 (Optional) Configure the S3 bucket notification

If you enabled SQS in [1.1](#11-create-the-role-with-cloudformation), the queue and its policy are already created by the stack. The only remaining step is to configure the notification on your bucket, which CloudFormation cannot do because the bucket is created in advance. Follow the manual notification steps in [2.3.2](#232-configure-the-s3-bucket-notification).

### Option 2: Bucket Access with Role ARN (Manual Setup)

Use this option if you cannot use CloudFormation, or if your organization requires every IAM resource to be created and reviewed manually. The IAM role itself is the same as in option 1; only the way you create it is different.

#### 2.1 Collect the required values

1. In the TiDB Cloud console, open the **Create Data Pipeline** page, go to the **External Stage** area, and enter your **Bucket URI**.
2. Under **Bucket Access**, select **AWS Role ARN**, and click the CloudFormation link below the field to open the dialog.
3. Copy the following values from the **Having trouble?** area of the dialog. You need all of them for the trust policy in [2.2](#22-create-the-role-and-attach-the-policies):

    - TiDB Cloud account ID
    - TiDB Cloud external ID
    - Lake external ID
    - Lake platform setup & validation role ARN
    - Lake platform data loading role ARN

#### 2.2 Create the role and attach the policies

1. Open the [IAM Console](https://console.aws.amazon.com/iam/), go to **Roles → Create role**.
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
4. Open the role you just created, go to the **Permissions** tab, and click **Add permissions → Create inline policy**.
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

#### 2.3 (Optional) Enable event-driven ingestion with SQS

Skip this section if periodic scanning is acceptable for your workload. For details about when to use SQS, see the note in [Prerequisites](#prerequisites).

##### 2.3.1 Create the SQS queue and configure the queue policy

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

##### 2.3.2 Configure the S3 bucket notification

The bucket is created in advance, so the queue cannot be wired to the bucket automatically. Configure the notification manually:

1. Open the [AWS S3 Console](https://console.aws.amazon.com/s3/) and navigate to your bucket.
2. Go to **Properties → Event notifications → Create event notification**.
3. Configure:
    - **Event types:** select **All object create events**.
    - **Destination:** select **SQS queue** and choose the queue created earlier.
4. Click **Save changes**.

### Option 3: Bucket Access with Access Key (Not Recommended)

> 💡 Using Access Key/Secret Key (AK/SK) means you need to manage and rotate credentials manually, and there is a higher risk of accidental exposure. For simpler management and better security, we recommend using a Role ARN instead — see [Option 1](#option-1-bucket-access-with-role-arn-cloudformation) or [Option 2](#option-2-bucket-access-with-role-arn-manual-setup).

With this option, you create an IAM user and provide its **Access Key ID** and **Secret Access Key** to TiDB Cloud. TiDB Cloud accesses your S3 bucket directly with these credentials.

#### 3.1 Create an IAM user and access key

1. Open the [IAM Console](https://console.aws.amazon.com/iam/), go to **Users → Create user**.
2. Enter a user name (for example, `tidb-cloud-lake-user`).
3. Select **Access key**, and attach the following **inline policy** (or create a managed policy and attach it). Replace `YOUR_BUCKET_NAME` and `your-prefix` with your actual values, and remove the `SQSConsumerAccess` statement if you do not need event-driven ingestion:

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

4. Complete the user creation, and save the **Access Key ID** and **Secret Access Key**. You need them when you configure the External Stage in the TiDB Cloud console.

    > **The Secret Access Key is only shown once at creation time.** Make sure to save it immediately.

#### 3.2 (Optional) Enable event-driven ingestion with SQS

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
    2. Go to **Properties → Event notifications → Create event notification**.
    3. Configure:
        - **Event types:** select **All object create events**.
        - **Destination:** select **SQS queue** and choose the queue created earlier.
    4. Click **Save changes**.

4. Record the queue URL from the queue details page in the SQS console. You need it when you configure the External Stage in the TiDB Cloud console, in the format `https://sqs.<region>.amazonaws.com/<account-id>/<queue-name>`.

## What's next?

After completing the AWS setup, you have all the values required by the External Stage configuration:

- **S3 URI**: from **Create an S3 bucket**.
- **Bucket access**: the Role ARN (options 1 and 2), or the Access Key ID and Secret Access Key (option 3).
- **SQS queue URL** (optional).

Open the TiDB Cloud console data pipeline configuration and enter these values in the **External Stage** settings to complete the data pipeline setup.

---

# Alibaba Cloud

> **Note:**
>
> Alibaba Cloud OSS support for the full Data Pipeline path (Export → Changefeed → Lake) is not yet fully verified. The instructions below cover bucket and credential setup, but the end-to-end behavior may differ from AWS S3. If you encounter issues, contact TiDB Cloud Support.

This section covers the setup for Object Storage Service (OSS). TiDB Cloud writes incremental data and snapshots to your OSS bucket, and TiDB Cloud Lake reads the data from it.

## Prerequisites

- An Alibaba Cloud account with permissions to manage OSS and RAM resources.
- A TiDB Cloud account with a TiDB Cloud Lake deployment.

## Step 1: Create an OSS bucket

> 💡 If you already have an OSS bucket ready, skip this step — just make sure the bucket region matches the region of your TiDB Cloud instance.

1. Open the [OSS Console](https://oss.console.aliyun.com/) and create a new bucket.
2. Select a region, **make sure this region matches the region of your TiDB Cloud instance.**
3. Optionally, create a folder (prefix) inside the bucket to organize TiDB Cloud data (for example, `oss://tidb-cloud-lake-data/my-cluster/`).

> **Record the following — you will need them in later steps:**
> - **Bucket Name:** e.g. `tidb-cloud-lake-data`
> - **OSS URI (with prefix):** e.g. `oss://tidb-cloud-lake-data/my-cluster/`

## Step 2: Create a RAM user and AccessKey pair

1. Open the [RAM Console](https://ram.console.aliyun.com/), go to **Users → Create user**.
2. Enter a display name (for example, `tidb-cloud-lake-user`) and select **OpenAPI calling** as the access method.
3. Click **Next**, then copy and save the **AccessKey ID** and **AccessKey Secret**.

    > **The AccessKey Secret is only shown once at creation time.** Make sure to save it immediately.

4. Open the user you just created, go to the **Permissions** tab, and click **Add permissions**.
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

> **Record the following — you will need them when configuring TiDB Cloud:**
> - **Access Key ID:** e.g. `LTAI5t...`
> - **Access Key Secret:** saved at creation time

## Step 3: Configure the External Stage in TiDB Cloud

After the bucket, RAM user, and permissions are ready, open the TiDB Cloud console and configure the External Stage with the following values:

- **Bucket URI**: the OSS URI from Step 1, such as `oss://tidb-cloud-lake-data/my-cluster/`
- **Access Key ID**: the RAM user's AccessKey ID
- **Access Key Secret**: the RAM user's AccessKey Secret

Then test the connection to validate the configuration.

## What's next?

After completing the Alibaba Cloud setup, you have the following resources ready for the TiDB Cloud Lake **External Stage** configuration:

| Resource | Where to find it |
|----------|------------------|
| **OSS URI** | From Step 1, for example, `oss://tidb-cloud-lake-data/my-cluster/` |
| **Access Key ID** | From Step 2, for example, `LTAI5t...` |
| **Access Key Secret** | From Step 2, saved at creation time |

Open the TiDB Cloud Console, navigate to your Lake deployment, and enter these values in the **External Stage** settings to complete the data pipeline setup.